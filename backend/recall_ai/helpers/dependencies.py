
import os
import time
from functools import cache
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from recall_ai.helpers.utils import setup_logging


load_dotenv()

logger = setup_logging()

vectorstore = None

@cache
def get_llm():
    logger.info("Initializing LLM model...")
    start = time.time()
    groq_api_key = os.getenv('GROQ_API_KEY')
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")
    logger.info(f"LLM initialized in {time.time() - start:.2f} seconds")
    return llm


@cache
def get_embeddings_model():
    logger.info("Initializing embeddings model...")
    start = time.time()
    model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    logger.info(f"Embeddings model initialized in {time.time() - start:.2f} seconds")
    return model


def get_vectorstore():
    global vectorstore
    if vectorstore is None:
        logger.info("Loading vector store from disk...")
        start = time.time()
        embeddings = get_embeddings_model()
        vector_store_path = os.path.join(os.getcwd(), "img_vector_store")
        try:
            vectorstore = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
            logger.info(f"Vector store loaded in {time.time() - start:.2f} seconds")
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            vectorstore = None
    return vectorstore