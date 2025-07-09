from kafka import KafkaConsumer
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from recall_ai.helpers.utils import setup_logging
from recall_ai.embeddings.embedding import generate_image_embeddings_from_textfiles
import traceback
import json
import time
import asyncio

# Kafka Consumer
consumer = KafkaConsumer(
    'ocr_results',
    bootstrap_servers=['localhost:9092'],
    group_id='ocr_results_worker',
    auto_offset_reset='earliest',
    enable_auto_commit=False,  # We'll commit manually after success
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


logger = setup_logging()
output_dir = 'images_taken'

def insert_batch(batch):
    for attempt in range(3):  # Retry 3 times
        try:
            embeddings, image_text_lines = generate_image_embeddings_from_textfiles()
            logger.info(f"Inserted batch of {len(batch)} OCRs.")
            if embeddings is None:
                logger.error("⚠️No embeddings generated.")
                print("⚠️ No embeddings generated.")
                return {"error": "No embeddings generated"}
            print(f"✅ Inserted {len(batch)} OCRs successfully.")
            logger.info(f"Inserted {len(batch)} OCRs successfully.")
            return {"embeddings": embeddings.tolist(), "total_lines": len(image_text_lines)}
        except Exception as e:
            logger.error(f"Failed to insert OCR data: {e}")
            print(f"⚠️ Insert failed. Retrying... Attempt {attempt+1}")
            time.sleep(2)  # Wait before retry
    print("❌ Insert failed after 3 attempts. Logging error...")
    formatted_traceback = traceback.format_exc()
    # (Optional) Save failed data somewhere safe
    return False

print("Worker started, waiting for OCRs...")
async def run_kafka():
    BATCH_SIZE = 2 
    IMAGE_TEXT_BATCH = []  # Temporary storage for batch
    try:
        for message in consumer:
            user_data = message.value
            IMAGE_TEXT_BATCH.append(user_data)

            if len(IMAGE_TEXT_BATCH) >= BATCH_SIZE:
                success = insert_batch(IMAGE_TEXT_BATCH)
                if success:
                    consumer.commit()  # Only commit Kafka offset after successful DB write
                    IMAGE_TEXT_BATCH = []  # Clear batch

    except KeyboardInterrupt:
        print("Shutting down worker...")
    finally:
        consumer.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_kafka())
    loop.close()
