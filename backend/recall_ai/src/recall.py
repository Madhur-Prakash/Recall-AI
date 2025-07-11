from contextlib import asynccontextmanager
import os
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, status, HTTPException, APIRouter
from recall_ai.helpers.utils import setup_logging
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()
recall = APIRouter()

# Load environment variables

# Global variables to be initialized during lifespan
llm = None
embeddings_model = None
vectorstore = None

logger = setup_logging()

# Initialize Groq LLM
groq_api_key = os.getenv('GROQ_API_KEY')
os.environ['GROQ_API_KEY'] = groq_api_key
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

# Initialize HuggingFace embeddings
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

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

Always maintain a polite, friendly, and human-like tone. Strictly adhere to all the rules stated above in every response.
<context>
{context}
<context>
Question: {input}
""")


@recall.get("/chat")
async def chat_with_logs(query: str):
    global vectorstore, llm, embeddings_model

    if not llm or not embeddings_model:
        return {"error": "Models not initialized yet."}

    if vectorstore is None:
        try:
            load_path = os.path.join(os.getcwd(), "img_vector_store")
            vectorstore = FAISS.load_local(load_path, embeddings_model, allow_dangerous_deserialization=True)
            logger.info("Vector store loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load vector store: {str(e)}")
            return {"error": "Vector store not found. Please run /store to initialize it."}

    try:
        # Retrieve top k context
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(query)
        context = "\n".join([doc.page_content for doc in docs])

        full_prompt = prompt.format_messages(context=context, input=query)

        # Stream response from LLM
        def stream():
            # Use regular for loop instead of async for
            for chunk in llm.stream(full_prompt):
                yield chunk.content

        return StreamingResponse(stream(), media_type="text/plain")

    except Exception as e:
        logger.error(f"Streaming chat error: {str(e)}")
        return {"error": str(e)}