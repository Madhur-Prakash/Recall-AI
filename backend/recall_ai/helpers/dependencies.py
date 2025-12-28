from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
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
DEVELOPMENT_ENV = os.getenv('DEVELOPMENT_ENV', 'local')  # Default to 'local' if not set
FAISS_VECTOR_STORE_DIR = os.getenv('FAISS_VECTOR_STORE_DIR')

faiss_vectorstore = None
qdrant_vectorstore = None

@cache
def get_llm():
    logger.info("Initializing LLM model...")
    start = time.time()
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        raise RuntimeError("❌ GROQ_API_KEY is missing in environment")
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
    global faiss_vectorstore
    if faiss_vectorstore is None:
        logger.info("Loading vector store from disk...")
        start = time.time()
        embeddings = get_embeddings_model()
        vector_store_path = os.path.join(FAISS_VECTOR_STORE_DIR)
        try:
            faiss_vectorstore = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
            logger.info(f"Vector store loaded in {time.time() - start:.2f} seconds")
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            faiss_vectorstore = None
    return faiss_vectorstore



def get_quad_vectorstore():
    global qdrant_vectorstore
    if qdrant_vectorstore is None:
        logger.info("Connecting to Qdrant...")
        try:
            embeddings = get_embeddings_model()
            client = QdrantClient(host="qdrant" if DEVELOPMENT_ENV == "docker" else "localhost", port=6333)
            collection_name = "img_embeddings"
            
            # Check if collection exists, if not create it
            try:
                client.get_collection(collection_name)
                logger.info(f"✅ Collection '{collection_name}' exists.")
            except Exception:
                # Collection doesn't exist, create it
                logger.info(f"Collection '{collection_name}' doesn't exist. Creating...")
                from qdrant_client.models import Distance, VectorParams
                
                # Get vector dimension from embeddings model
                test_vector = embeddings.embed_query("test")
                vector_dim = len(test_vector)
                
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=vector_dim, distance=Distance.COSINE)
                )
                logger.info(f"✅ Created collection '{collection_name}'")
            
            vectorstore = QdrantVectorStore(
                client=client,
                collection_name=collection_name,
                embedding=embeddings,
            )
            logger.info("✅ Qdrant vector store initialized.")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Qdrant: {e}")
            vectorstore = None
    return vectorstore
