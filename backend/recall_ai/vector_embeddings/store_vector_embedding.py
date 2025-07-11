import os
import glob
from datetime import datetime
import shutil
from recall_ai.helpers.utils import setup_logging
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = setup_logging()

vectorstore = None
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

def store_embeddings(img_dir: str = "images_taken/"):
    try:
        img_files = glob.glob(os.path.join(img_dir, "*.txt"))
        logger.info(f"✅ Found {len(img_files)} img -> text files")

        raw_lines = []
        for img_file in img_files:
            try:
                with open(img_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = [line.strip() for line in f if len(line.strip()) > 10]
                raw_lines.extend(lines)
            except Exception as e:
                logger.error(f"Failed to read {img_file}: {e}")

        if not raw_lines:
            logger.error("No valid log lines found.")
            return {"error": "No valid log lines found."}

        # Smart chunking
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        documents = text_splitter.create_documents(raw_lines)
        chunked_texts = [doc.page_content for doc in documents]
        logger.info(f"Chunked into {len(chunked_texts)} documents")

        global vectorstore
        vector_store_path = os.path.join(os.getcwd(), "img_vector_store")

        if os.path.exists(os.path.join(vector_store_path, "index.faiss")):
            try:
                logger.info("Loading existing vector store...")
                vectorstore = FAISS.load_local(vector_store_path, embeddings_model, allow_dangerous_deserialization=True)
                new_vectorstore = FAISS.from_texts(chunked_texts, embeddings_model)
                vectorstore.merge_from(new_vectorstore)
                logger.info(f"✅ Appended {len(chunked_texts)} new embeddings")
            except Exception as e:
                logger.warning(f"Fallback to new vectorstore: {e}")
                vectorstore = FAISS.from_texts(chunked_texts, embeddings_model)
        else:
            logger.info("No existing vector store. Creating new...")
            vectorstore = FAISS.from_texts(chunked_texts, embeddings_model)

        vectorstore.save_local(vector_store_path)
        logger.info(f"✅ Embeddings stored successfully")

        shutil.rmtree(img_dir)
        os.makedirs(img_dir, exist_ok=True)

        return {"message": "Embeddings stored successfully.", "total_chunks": len(chunked_texts)}
    except Exception as e:
        logger.error(f"❌ Error storing embeddings: {e}")
        return {"error": str(e)}
