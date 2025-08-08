import os
import glob
import shutil
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter, FieldCondition, Range, FilterSelector
from recall_ai.helpers.dependencies import get_embeddings_model
from recall_ai.helpers.utils import setup_logging
from recall_ai.helpers.decrypt import decrypt_file_data
import traceback

logger = setup_logging()

def quad_store_embeddings(text_dir: str = "images_taken/"):
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
        raw_lines = []
        for text_file in text_files:
            try:
                with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = [line.strip() for line in f if len(line.strip()) > 10]
                raw_lines.extend(lines)
            except Exception as e:
                formatted_traceback = traceback.format_exc()
                logger.error(f"Traceback (most recent call last):{formatted_traceback}")
                logger.error(f"Failed to read {text_file}: {e}")

        if not raw_lines:
            return {"error": "No valid log lines found."}

        # Chunk text
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        documents = splitter.create_documents(raw_lines)
        chunked_texts = [doc.page_content for doc in documents]
        logger.info(f"✅ Chunked into {len(chunked_texts)} documents")

        # Prepare Qdrant
        embeddings_model = get_embeddings_model()
        client = QdrantClient("localhost", port=6333)
        collection_name = "img_embeddings"

        # Auto-create collection if it doesn't exist
        vector = embeddings_model.embed_query("test")
        vector_dim = len(vector)

        existing_collections = [c.name for c in client.get_collections().collections]
        if collection_name not in existing_collections:
            logger.info(f"ℹ️ Creating collection '{collection_name}' with vector size {vector_dim}")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_dim, distance=Distance.COSINE)
            )

        # Use float timestamp for metadata
        now_ts = time.time()
        Qdrant.from_texts(
            texts=chunked_texts,
            embedding=embeddings_model,
            metadatas=[{"timestamp": now_ts}] * len(chunked_texts),  # float timestamp
            collection_name=collection_name
        )

        # Confirm insertion
        count = client.count(collection_name=collection_name).count
        logger.info(f"📦 Collection '{collection_name}' now contains {count} points")

        # Clear old embeddings (older than 30 days)
        cutoff_ts = time.time() - (30 * 24 * 60 * 60)
        timestamp_filter = Filter(
            must=[
                FieldCondition(
                    key="timestamp",
                    range=Range(lt=cutoff_ts)
                )
            ]
        )

        deleted_count = client.delete(
            collection_name=collection_name,
            points_selector=FilterSelector(filter=timestamp_filter)
        )
        logger.info(f"🧹 Deleted old embeddings older than {cutoff_ts}: {deleted_count}")

        # Reset image directory
        shutil.rmtree(text_dir)
        os.makedirs(text_dir, exist_ok=True)
        logger.info(f"✅ Cleared and recreated image directory: {text_dir}")

        return {"message": "Embeddings stored successfully.", "total_chunks": len(chunked_texts)}

    except Exception as e:
        logger.error(f"❌ Error storing embeddings: {e}")
        return {"error": str(e)}