import datetime
import os
import glob
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter, FieldCondition, Range, FilterSelector
from recall_ai.helpers.dependencies import get_embeddings_model
from recall_ai.helpers.utils import setup_logging
from recall_ai.helpers.decrypt import decrypt_file_data
import traceback
from dotenv import load_dotenv
from filelock import FileLock

logger = setup_logging()
load_dotenv()
IMAGE_DIR = os.getenv("IMAGES_DIR")
DEVELOPMENT_ENV = os.getenv('DEVELOPMENT_ENV', 'local')  # Default to 'local' if not set

def quad_store_embeddings(text_dir: str = IMAGE_DIR):
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
        if DEVELOPMENT_ENV == "docker":
            qdrant_host = "qdrant"  # Docker Compose service name
        else:
            qdrant_host = "localhost"
        try:
            client = QdrantClient(host=qdrant_host, port=6333)
        except Exception as conn_err:
            logger.error(f"❌ Could not connect to Qdrant at {qdrant_host}:6333 - {conn_err}")
            return {"error": str(conn_err)}
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
        try:
            QdrantVectorStore.from_texts(
                texts=chunked_texts,
                embedding=embeddings_model,
                metadatas=[{"timestamp": now_ts}] * len(chunked_texts),  # float timestamp
                collection_name=collection_name,
                url=f"http://{qdrant_host}:6333"
            )
        except Exception as qdrant_err:
            logger.error(f"❌ Error storing embeddings in Qdrant: {qdrant_err}")
            return {"error": str(qdrant_err)}

        # Confirm insertion
        count = client.count(collection_name=collection_name).count
        logger.info(f"📦 Collection '{collection_name}' now contains {count} points")

        # Clear old embeddings (older than 30 days)
        cutoff_ts = time.time() - (30 * 24 * 60 * 60)
        cutoff_human = datetime.datetime.fromtimestamp(cutoff_ts).isoformat()
        timestamp_filter = Filter(
            must=[
                FieldCondition(
                    key="timestamp",
                    range=Range(lt=cutoff_ts)
                )
            ]
        )

        # Count points that match the filter BEFORE deletion
        points_to_delete = client.count(
            collection_name=collection_name,
            count_filter=timestamp_filter
        ).count

        if points_to_delete > 0:
            client.delete(
                collection_name=collection_name,
                points_selector=FilterSelector(filter=timestamp_filter)
            )
            logger.info(
                f"🧹 Deleted {points_to_delete} embeddings older than {cutoff_human}"
            )
        else:
            logger.info("🧹 No old embeddings to delete")

        # Mark this service as done
        done_file = os.path.join(text_dir, ".qdrant_done")
        with open(done_file, 'w') as f:
            f.write(str(time.time()))
        logger.info("✅ Qdrant processing complete")

        # Check if both services are done, then delete files
        faiss_done = os.path.exists(os.path.join(text_dir, ".faiss_done"))
        if faiss_done:
            logger.info("✅ Qdrant service is done. Cleaning up...running in Qdrant block")
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
            logger.info("⏳ Waiting for FAISS service to complete before cleanup")

        return {"message": "Embeddings stored successfully.", "total_chunks": len(chunked_texts)}

    except Exception as e:
        logger.error(f"❌ Error storing embeddings: {e}")
        return {"error": str(e)}