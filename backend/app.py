from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
import os
import sys
import time
from dotenv import load_dotenv

# Adjust import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recall_ai.helpers.utils import setup_logging
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

# Global variables to be initialized during lifespan
llm = None
embeddings_model = None
vectorstore = None

logger = setup_logging()

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm, embeddings_model
    logger.info("Starting application with lifespan handler...")

    try:
        t0 = time.time()

        # Initialize Groq LLM
        groq_api_key = os.getenv('GROQ_API_KEY')
        os.environ['GROQ_API_KEY'] = groq_api_key
        llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")
        logger.info("Groq LLM initialized.")

        # Initialize HuggingFace embeddings
        embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
        logger.info("Embeddings model loaded.")

        logger.info(f"Startup completed in {time.time() - t0:.2f} seconds.")
    except Exception as e:
        logger.error(f"Startup error: {e}")

    yield

    logger.info("Shutting down application...")

# FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

# Prompt template
prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context only.
Please provide the most accurate response based on the question.
<context>
{context}
<context>
Question: {input}
""")

# Endpoint: /chat
@app.get("/chat")
async def chat_with_logs(query: str):
    global vectorstore, llm, embeddings_model

    # Check model initialization
    if not llm or not embeddings_model:
        return {"error": "Models not initialized yet."}

    # Load vectorstore if not loaded
    if vectorstore is None:
        try:
            app_dir = os.path.dirname(os.path.abspath(__file__))
            load_path = os.path.join(app_dir, "img_vector_store")
            vectorstore = FAISS.load_local(load_path, embeddings_model, allow_dangerous_deserialization=True)
            logger.info("Vector store loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load vector store: {str(e)}")
            return {"error": "Vector store not found. Please run /store to initialize it."}

    try:
        # Retrieval logic
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vectorstore.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        response = retrieval_chain.invoke({"input": query})
        answer = response.get("answer")

        if not answer:
            return {"error": "No answer generated."}

        return {"response": answer}
    except Exception as e:
        logger.error(f"Retrieval error: {str(e)}")
        return {"error": "An error occurred during retrieval."}
