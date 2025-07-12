import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import glob
from datetime import timedelta
import shutil
from recall_ai.helpers.dependencies import get_vectorstore, get_embeddings_model
from recall_ai.helpers.utils import setup_logging, get_file_creation_age
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = setup_logging()

vectorstore = get_vectorstore()
embeddings_model = get_embeddings_model()

def store_embeddings(img_dir: str = "images_taken/"):
    try:
        img_files = glob.glob(os.path.join(img_dir, "*.txt"))
        logger.info(f"✅ Found {len(img_files)} img -> text files")
        if (len(img_files) == 0):
            logger.error("❌ No image files found to process.")
            return {"error": "No image files found to process."}

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
        chunked_texts = [f"passage: {doc.page_content}" for doc in documents]
        logger.info(f"Chunked into {len(chunked_texts)} documents")

        vector_store_path = os.path.join(os.getcwd(), "img_vector_store")


        if os.path.exists(os.path.join(vector_store_path, "index.faiss")):
            try:
                #  check when file was created
                age_of_vector_store = get_file_creation_age(vector_store_path)
                logger.info(f"✌️ Vector store age: {age_of_vector_store} days")
                if (age_of_vector_store >= timedelta(days=30)): # delete vector store if older than 30 days
                    logger.info(f"✅ file was created {age_of_vector_store} days ago, removing old vector store")
                    shutil.rmtree(vector_store_path) # remove old vector store
                    logger.info("✅ Removed old vector store")
                    os.makedirs(vector_store_path, exist_ok=True) # create new vector store
                    logger.info("✅ Created new vector store directory")
                    vectorstore = FAISS.from_texts(chunked_texts, embeddings_model)

                else: 
                    logger.info("Vector store is less than 30 days old, appending new embeddings")
                    # Load existing vector store and append new embeddings
                    logger.info(f"✅ Existing vector store found at {vector_store_path}")
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

        # Clear cache so next get_vectorstore() reloads fresh vector store
        vectorstore = None

        shutil.rmtree(img_dir)
        logger.info(f"✅ Cleared image directory {img_dir}")
        os.makedirs(img_dir, exist_ok=True)
        logger.info(f"✅ Created new image directory {img_dir}")

        return {"message": "Embeddings stored successfully.", "total_chunks": len(chunked_texts)}
    except Exception as e:
        logger.error(f"❌ Error storing embeddings: {e}")
        return {"error": str(e)}
