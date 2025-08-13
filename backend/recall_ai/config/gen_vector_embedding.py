from kafka import KafkaConsumer
from kafka.errors import CommitFailedError
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from recall_ai.helpers.utils import setup_logging
import traceback
import json
import time
from dotenv import load_dotenv

import time
print("Before importing store_embeddings")
st = time.time()
from recall_ai.vector_embeddings.store_vector_embedding import store_embeddings
print("After importing store_embeddings")
fn = time.time() - st
print(f"Time taken to import store_embeddings: {fn:.2f} seconds")

logger = setup_logging()
load_dotenv()  # Load environment variables from .env file

DEVELOPMENT_ENV = os.getenv('DEVELOPMENT_ENV', 'local')  # Default to 'local' if not set

def create_consumer():
    """Create a new Kafka consumer with optimized settings"""

    if DEVELOPMENT_ENV == "docker":
        bootstrap_servers = ['kafka:29092']
    else:
        bootstrap_servers = ['localhost:9092']

    return KafkaConsumer(
        'vector_embeddings',
        bootstrap_servers=bootstrap_servers,
        group_id='embeddings_worker',
        auto_offset_reset='earliest',
        enable_auto_commit=False,  # We'll commit manually after success
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        # Increased timeouts to prevent session expiration
        session_timeout_ms=30000,  # 30 seconds
        heartbeat_interval_ms=10000,  # 10 seconds (must be < session_timeout_ms/3)
        max_poll_interval_ms=300000,  # 5 minutes - adjust based on your processing time
        max_poll_records=10,  # Limit records per poll to prevent timeout
        # Connection settings
        connections_max_idle_ms=540000,  # 9 minutes
        request_timeout_ms=40000,  # 40 seconds (must be > session_timeout_ms)
    )

def insert_batch(batch):
    """Insert batch with retry logic"""
    for attempt in range(3):  # Retry 3 times
        try:
            res = store_embeddings()
            logger.info(f"Inserted batch of {len(batch)} OCRs.")
            if res is None:
                logger.error("⚠️No embeddings generated.")
                print("⚠️ No embeddings generated.")
                return {"error": "No embeddings generated"}
            print(f"✅ Inserted {len(batch)} OCRs text successfully.")
            logger.info(f"Inserted {len(batch)} OCRs successfully.")
            return {"success": True, "count": len(batch)}
        except Exception as e:
            logger.error(f"Failed to insert OCR data: {e}")
            print(f"⚠️ Insert failed. Retrying... Attempt {attempt+1}")
            time.sleep(2)  # Wait before retry
    
    print("❌ Insert failed after 3 attempts. Logging error...")
    formatted_traceback = traceback.format_exc()
    logger.error(f"Insert failed after 3 attempts: {formatted_traceback}")
    return False

def safe_commit(consumer, max_retries=3):
    """Safely commit with retry logic"""
    for attempt in range(max_retries):
        try:
            consumer.commit()
            logger.info("Successfully committed offset")
            return True
        except CommitFailedError as e:
            logger.warning(f"Commit failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
            else:
                logger.error("All commit attempts failed")
                return False
        except Exception as e:
            logger.error(f"Unexpected error during commit: {e}")
            return False
    return False

def run_kafka():
    BATCH_SIZE = 34
    IMAGE_TEXT_BATCH = []  # Temporary storage for batch
    consumer = None
    
    try:
        consumer = create_consumer()
        print("Worker started, waiting for text files...")
        
        consecutive_failures = 0
        max_consecutive_failures = 5
        
        for message in consumer:
            try:
                user_data = message.value
                IMAGE_TEXT_BATCH.append(user_data)
                
                if len(IMAGE_TEXT_BATCH) >= BATCH_SIZE:
                    success = insert_batch(IMAGE_TEXT_BATCH)
                    
                    if success:
                        # Try to commit, but handle failures gracefully
                        if safe_commit(consumer):
                            IMAGE_TEXT_BATCH = []  # Clear batch only on successful commit
                            consecutive_failures = 0
                        else:
                            consecutive_failures += 1
                            logger.warning(f"Commit failed, consecutive failures: {consecutive_failures}")
                            
                            # If too many consecutive failures, recreate consumer
                            if consecutive_failures >= max_consecutive_failures:
                                logger.error("Too many consecutive commit failures, recreating consumer...")
                                consumer.close()
                                consumer = create_consumer()
                                consecutive_failures = 0
                                IMAGE_TEXT_BATCH = []  # Clear batch to avoid reprocessing
                    else:
                        logger.error("Batch insert failed, not committing offset")
                        consecutive_failures += 1
                        
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                consecutive_failures += 1
                
                if consecutive_failures >= max_consecutive_failures:
                    logger.error("Too many consecutive processing failures, recreating consumer...")
                    if consumer:
                        consumer.close()
                    consumer = create_consumer()
                    consecutive_failures = 0
                    IMAGE_TEXT_BATCH = []
                    
    except KeyboardInterrupt:
        print("Shutting down worker...")
        logger.info("Worker shutdown requested")
    except Exception as e:
        logger.error(f"Unexpected error in run_kafka: {e}")
        logger.error(traceback.format_exc())
    finally:
        if consumer:
            try:
                # Try to commit any remaining batch before closing
                if IMAGE_TEXT_BATCH:
                    logger.info(f"Processing remaining {len(IMAGE_TEXT_BATCH)} messages before shutdown")
                    success = insert_batch(IMAGE_TEXT_BATCH)
                    if success:
                        safe_commit(consumer)
                consumer.close()
                logger.info("Consumer closed successfully")
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    run_kafka()