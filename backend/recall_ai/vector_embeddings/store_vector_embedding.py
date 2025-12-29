import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import glob
import time
from datetime import timedelta
from recall_ai.helpers.decrypt import decrypt_file_data
import shutil
from recall_ai.helpers.dependencies import get_embeddings_model
import recall_ai.helpers.dependencies as deps
from recall_ai.helpers.utils import setup_logging, get_file_creation_age
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from filelock import FileLock

load_dotenv()
logger = setup_logging()
IMAGE_DIR = os.getenv("IMAGES_DIR")
FAISS_VECTOR_STORE_DIR = os.getenv('FAISS_VECTOR_STORE_DIR')

def store_embeddings(text_dir: str = IMAGE_DIR):
    try:
        enc_files = glob.glob(os.path.join(text_dir, "*.enc"))
        if not enc_files:
            logger.error("❌ No encrypted files found to process.")
            return {"error": "No encrypted files found to process."}
        success = decrypt_file_data()
        if not success:
            logger.error("❌ Decryption failed.")
            return {"error": "Decryption failed."}
        logger.info("✅ Decryption successful.")

        text_files = glob.glob(os.path.join(text_dir, "*.txt"))
        logger.info(f"✅ Found {len(text_files)} img -> text files")
        if not text_files:
            logger.error("❌ No text files found to process.")
            return {"error": "No text files found to process."}
        
        # Read files without lock
        raw_lines = []
        for text_file in text_files:
            try:
                with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = [line.strip() for line in f if len(line.strip()) > 10]
                raw_lines.extend(lines)
            except Exception as e:
                logger.error(f"Failed to read {text_file}: {e}")

        if not raw_lines:
            logger.error("No valid log lines found.")
            return {"error": "No valid log lines found."}

        # Smart chunking
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        documents = text_splitter.create_documents(raw_lines)
        chunked_texts = [f"passage: {doc.page_content}" for doc in documents]
        logger.info(f"Chunked into {len(chunked_texts)} documents")

        vector_store_path = os.path.join(FAISS_VECTOR_STORE_DIR)
        index_path = os.path.join(vector_store_path, "index.faiss")
        embeddings_model = get_embeddings_model()
        
        if os.path.exists(index_path):
            try:
                #  check when file was created
                age_of_vector_store, age_str = get_file_creation_age(index_path)
                logger.info(f"✌️ Vector store age: {age_str}")
                if age_of_vector_store is not None and age_of_vector_store >= timedelta(days=30):  # delete vector store if older than 30 days
                    logger.info(f"✅ Vector store was created {age_str} ago, removing old vector store")
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
        deps.faiss_vectorstore = None

        # Mark this service as done
        done_file = os.path.join(text_dir, ".faiss_done")
        with open(done_file, 'w') as f:
            f.write(str(time.time()))
        logger.info("✅ FAISS processing complete")

        # Check if both services are done, then delete files
        qdrant_done = os.path.exists(os.path.join(text_dir, ".qdrant_done"))
        if qdrant_done:
            logger.info("✅ FAISS service is done. Cleaning up...running in FAISS block")
            logger.info("✅ Both services are done. Cleaning up...")
            lock_file = os.path.join(text_dir, ".cleanup.lock")
            lock = FileLock(lock_file, timeout=10)
            try:
                with lock:
                    # Delete all txt files and done markers
                    for text_file in text_files:
                        try:
                            if os.path.exists(text_file):
                                os.remove(text_file)
                        except Exception as del_err:
                            logger.warning(f"Could not delete {text_file}: {del_err}")
                    
                    # Remove done markers
                    for marker in [".qdrant_done", ".faiss_done"]:
                        marker_path = os.path.join(text_dir, marker)
                        if os.path.exists(marker_path):
                            os.remove(marker_path)
                    
                    logger.info(f"✅ Cleared all text files from {text_dir}")
            except Exception as lock_err:
                logger.warning(f"Could not acquire cleanup lock: {lock_err}")
        else:
            logger.info("⏳ Waiting for Qdrant service to complete before cleanup")

        return {"message": "Embeddings stored successfully.", "total_chunks": len(chunked_texts)}
    except Exception as e:
        logger.error(f"❌ Error storing embeddings: {e}")
        return {"error": str(e)}
