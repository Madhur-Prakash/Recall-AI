from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from recall_ai.helpers.utils import setup_logging
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from recall_ai.embeddings.store_vector_embedding import vectorstore as imported_vectorstore

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")
logger = setup_logging()
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based on the context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Question:{input}
    """
)
vectorstore = imported_vectorstore

@app.get("/chat")
async def chat_with_logs(query: str):
    global vectorstore
    if vectorstore is None:
        try:
            app_dir = os.path.dirname(os.path.abspath(__file__))
            load_path = os.path.join(app_dir, "img_vector_store")
            vectorstore = FAISS.load_local(load_path, embeddings_model, allow_dangerous_deserialization=True)
            logger.info("Vector store loaded successfully.")
        except Exception as e:
            logger.error(f"Vector store not found or failed to load. Error: {str(e)}")
            return {"error": "Vector store not found. Please run /store to initialize it."}

    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectorstore.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": query})

    answer = response.get("answer")
    if not answer:
        return {"error": "No answer generated."}
    return {"response": answer}