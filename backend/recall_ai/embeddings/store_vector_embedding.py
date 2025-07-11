import os
import glob
from recall_ai.helpers.utils import setup_logging
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


logger = setup_logging()


vectorstore = None
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

def store_embeddings(img_dir: str = "images_taken/"):
    # Get all relevant log files (including rotated logs)
    img_files = glob.glob(os.path.join(img_dir, "*.txt"))
    logger.info(f"Found {len(img_files)} img -> text files: {img_files}")

    all_text_lines = []
    total_lines = 0
    for img_file in img_files:
        try:
            with open(img_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
            logger.info(f"Read {len(lines)} lines from {img_file}")
            all_text_lines.extend(lines)
            total_lines += len(lines)
        except Exception as e:
            logger.error(f"Failed to read {img_file}: {e}")

    if total_lines == 0:
        logger.error("No log lines found in any files.")
        return {"error": "No log lines found."}

    logger.info(f"Total lines aggregated from all files: {total_lines}")

    global vectorstore
    vectorstore = FAISS.from_texts(all_text_lines, embeddings_model)

    save_path = os.path.join(os.getcwd(), "img_vector_store")
    vectorstore.save_local(save_path)
    logger.info(f"Embeddings stored successfully at {save_path}")

    return {"message": "Embeddings stored successfully.", "total_lines": total_lines}