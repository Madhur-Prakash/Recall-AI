import os
import glob
from datetime import datetime
import shutil
from recall_ai.helpers.utils import setup_logging
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


logger = setup_logging()

vectorstore = None
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

def store_embeddings(img_dir: str = "images_taken/"):
    try:
        # Get all relevant log files (including rotated logs)
        img_files = glob.glob(os.path.join(img_dir, "*.txt"))
        logger.info(f"✅Found {len(img_files)} img -> text files")

        all_text_lines = []
        total_lines = 0
        for img_file in img_files:
            try:
                with open(img_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = [line.strip() for line in f if line.strip()]
                all_text_lines.extend(lines)
                total_lines += len(lines)
            except Exception as e:
                logger.error(f"Failed to read {img_file}: {e}")

        if total_lines == 0:
            logger.error("No log lines found in any files.")
            return {"error": "No log lines found."}

        logger.info(f"Total lines aggregated from all files: {total_lines}")

        global vectorstore
        vector_store_path = os.path.join(os.getcwd(), "img_vector_store")
        
        # Check if existing vector store exists
        if os.path.exists(vector_store_path) and os.path.exists(os.path.join(vector_store_path, "index.faiss")):
            try:
                # Load existing vector store
                logger.info("Loading existing vector store...")
                vectorstore = FAISS.load_local(vector_store_path, embeddings_model, allow_dangerous_deserialization=True)
                
                # Create new embeddings for the new text lines
                new_vectorstore = FAISS.from_texts(all_text_lines, embeddings_model)
                
                # Merge the new embeddings with existing ones
                logger.info("Merging new embeddings with existing vector store...")
                vectorstore.merge_from(new_vectorstore)
                
                logger.info(f"✅ Successfully appended {total_lines} new embeddings to existing vector store")
                
            except Exception as e:
                logger.error(f"Failed to load existing vector store: {e}")
                logger.info("Creating new vector store...")
                vectorstore = FAISS.from_texts(all_text_lines, embeddings_model)
        else:
            # Create new vector store if none exists
            logger.info("No existing vector store found. Creating new one...")
            vectorstore = FAISS.from_texts(all_text_lines, embeddings_model)

        try:
            # Save the updated vector store
            vectorstore.save_local(vector_store_path)
            logger.info(f"✅ Embeddings stored successfully")
            
            # Only delete text files after successful storage
            logger.info("✅ Removing text files after storing embeddings.")
            shutil.rmtree(img_dir)       # deletes everything
            os.makedirs(img_dir, exist_ok=True)  # recreate the directory
            
        except Exception as e:
            logger.error("❌ Failed to store embeddings.")
            return {"error": "Failed to store embeddings."}
        return {"message": "Embeddings stored successfully.", "total_lines": total_lines}

    except Exception as e:
        logger.error(f"❌Error storing embeddings: {e}")
        return {"error": str(e)}