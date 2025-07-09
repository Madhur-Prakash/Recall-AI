import os
import glob
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from recall_ai.helpers.utils import setup_logging
from datetime import datetime

logger = setup_logging()

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
output_folder = "generated_embedding"
full_output_folder = os.path.join(base_dir, output_folder)
os.makedirs(full_output_folder, exist_ok=True)  # Ensure output directory exists


def generate_image_embeddings_from_textfiles(image_text_directory='images_taken', output_folder=output_folder):
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
    image_text_files = glob.glob(os.path.join(base_dir, image_text_directory, "*.txt"))

    logger.info(f"Found {len(image_text_files)} text files in {image_text_directory}.")

    if not image_text_files:
        logger.warning(f"⚠️ No text files found in {image_text_directory}. Please ensure the directory contains .txt files.")
        return None, None

    all_image_lines = []
    for image_text_file in image_text_files:
        try:
            with open(image_text_file, 'r', encoding='utf-8', errors='ignore') as f:
                line = f.readline().strip()
                if line:
                    all_image_lines.append(line)
        except Exception as e:
            logger.error(f"⚠️ Error reading file {image_text_file}. Error: {e}")
            continue

    if not all_image_lines:
        logger.warning("⚠️ No valid lines found in the text files. Please ensure the files are not empty and contain valid text.")
        return None, None

    logger.info(f"Generating embeddings for {len(all_image_lines)} lines from {len(image_text_files)} files.")
    embeddings = embeddings_model.embed_documents(all_image_lines)
    embeddings_array = np.array(embeddings)
    logger.info(f"Generated embeddings shape: {embeddings_array.shape}")

    # Construct and save file to correct output path
    filename = f"embeddings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.npy"
    output_file_path = os.path.join(full_output_folder, filename)
    np.save(output_file_path, embeddings_array)
    logger.info(f"Saved embeddings to {output_file_path}")

    return embeddings_array, all_image_lines


def find_similar_images(query_text, embeddings_array, image_lines, top_k=5):
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
    query_embedding = embeddings_model.embed_query(query_text)
    query_embedding = np.array(query_embedding).reshape(1, -1)

    similarities = cosine_similarity(query_embedding, embeddings_array)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            'image_line': image_lines[idx],
            'similarity': float(similarities[idx]),
            'index': int(idx)
        })

    return results
