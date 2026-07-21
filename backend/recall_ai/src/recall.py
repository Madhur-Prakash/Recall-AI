import os
from fastapi.responses import StreamingResponse
from fastapi import status, HTTPException, APIRouter
from recall_ai.helpers.dependencies import get_vectorstore, get_embeddings_model, get_llm
from recall_ai.helpers.utils import setup_logging, ThinkStripper
from langchain_community.vectorstores import FAISS
import recall_ai.helpers.dependencies as deps
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import asyncio

load_dotenv()
recall = APIRouter()

logger = setup_logging()
FAISS_VECTOR_STORE_DIR = os.getenv('FAISS_VECTOR_STORE_DIR')

# Prompt template
prompt = ChatPromptTemplate.from_template("""
Please answer the question as accurately as possible using only the information provided in the context. Avoid generic phrases like "Based on the context" or "According to the information provided." Do not mention, infer, guess, reconstruct, or store any login credentials, passwords, tokens, API keys, or other sensitive personal data. If asked, respond with: "I cannot provide that information" or "I can't answer that."

Do not assist with or provide responses related to:

Age-restricted or explicit content

Illegal activities of any kind

Sensitive personal, private, or confidential information

Malware, exploits, phishing, or reverse engineering

Forging identities, bypassing security, or evading detection systems

If the user is involved in or requests anything related to the above, respond clearly with: "I cannot provide that information" or "I can't answer that."

Never infer or fabricate details that are not explicitly stated or reasonably inferred from the provided context. If the answer is not contained within the context, respond with: "The context doesn't contain that information."

Do not repeat the question unless explicitly asked to paraphrase. Do not use unnecessary filler or be overly verbose unless a detailed explanation is requested. Use a clear, concise, and conversational tone. When summarizing or listing items, use bullet points or numbered lists. For direct answers, use single, well-structured sentences.
If no context is provided, respond with: "I don't have any context to answer that question." 

If the user ask for a summary of the context, provide a concise summary without repeating the entire context verbatim.
If user ask "what he was doing on this day" or "what was he doing on this date", provide a concise summary of the context by searching for any date or time mentioned in the context.

Always maintain a polite, friendly, and human-like tone. Strictly adhere to all the rules stated above in every response.
<context>
{context}
<context>
Question: {input}
""")


@recall.get("/chat", status_code=status.HTTP_200_OK)
async def chat_with_history(query: str):
    """
    Streaming endpoint for chat
    """
    logger.info("✌️ FAISS Triggered")
    logger.info(f"Received streaming chat query: {query}")
    llm = get_llm()
    embeddings_model = get_embeddings_model()
    vectorstore = get_vectorstore()

    if vectorstore is None:
        try:
            load_path = os.path.join(FAISS_VECTOR_STORE_DIR)
            vectorstore = FAISS.load_local(load_path, embeddings_model, allow_dangerous_deserialization=True)
            logger.info("Vector store loaded successfully.")
        
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vector store not found.")
        
    try:
        # Step 1: Embed and retrieve top-k chunks
        retriever = vectorstore.as_retriever(search_kwargs={"k": 16})
        query_emb = f"query: {query}"
        docs = retriever.invoke(query_emb)

        if not docs:
            logger.warning("No relevant documents found for query.")
            return {"response": "No relevant information found in the context."}

        # Step 2: Format the context
        context = "\n".join([doc.page_content for doc in docs])
        full_prompt = prompt.format_messages(context=context, input=query)

        # Step 3: Stream LLM output
        async def stream_generator():
            stripper = ThinkStripper()  # hide any <think>...</think> reasoning from the client
            try:
                if hasattr(llm, 'astream'):
                    logger.info("Using async streaming for LLM response.")
                    async for chunk in llm.astream(full_prompt):
                        piece = stripper.feed(chunk.content or "")
                        if piece:
                            yield piece
                else:
                    logger.info("Using sync streaming for LLM response.")
                    loop = asyncio.get_running_loop()

                    def sync_stream():
                        for chunk in llm.stream(full_prompt):
                            yield chunk.content

                    # Create iterator from sync_stream
                    iterator = sync_stream()

                    # Pull chunks in a background thread one-by-one
                    while True:
                        chunk = await loop.run_in_executor(None, lambda: next(iterator, None))
                        if chunk is None:
                            break
                        piece = stripper.feed(chunk or "")
                        if piece:
                            yield piece
                        await asyncio.sleep(0.001)

                tail = stripper.flush()
                if tail:
                    yield tail

            except Exception as e:
                logger.error(f"Error during LLM streaming: {e}")
                yield "❌ Error occurred during LLM response generation."

        
        # Clear cache so next get_vectorstore() reloads fresh vector store
        deps.faiss_vectorstore = None

        return StreamingResponse(stream_generator(), media_type="text/plain")

    except Exception as e:
        logger.error(f"❌ Streaming chat error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))