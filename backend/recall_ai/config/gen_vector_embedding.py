from glob import glob
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from recall_ai.helpers.utils import setup_logging
from dotenv import load_dotenv
load_dotenv()

logging = setup_logging()

import time
logging.info("Before importing store_embeddings")
st = time.time()
from recall_ai.vector_embeddings.store_vector_embedding import store_embeddings
logging.info("After importing store_embeddings")
fn = time.time() - st
logging.info(f"Time taken to import store_embeddings: {fn:.2f} seconds")


IMAGE_DIR = os.getenv("IMAGES_DIR")
if not IMAGE_DIR:
    raise RuntimeError("IMAGES_DIR env variable is not set inside container")

TEXT_FILE_LIMIT = int(os.getenv("TEXT_FILE_LIMIT"))
if not TEXT_FILE_LIMIT:
    raise RuntimeError("TEXT_FILE_LIMIT env variable is not set inside container")

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".enc"):
            enc_text_files = glob(os.path.join(IMAGE_DIR, "*.enc"))
            if len(enc_text_files) > 0:
                logging.info(f"🔄️Current encrypted text files count: {len(enc_text_files)}")

            if len(enc_text_files) >= TEXT_FILE_LIMIT:
                logging.info(f"⚡ Threshold reached: {len(enc_text_files)} encrypted files. Triggering embedding generation...")
                res = store_embeddings()
                if(res['message'] != "Embeddings stored successfully."):
                    logging.error(f"❌Error occurred while storing embeddings: {res['message']}")
                logging.info(f"✅ Embeddings stored successfully. Current count: {len(enc_text_files)}")


# check for already existing directory
def initial_scan():
    enc_text_files = glob(os.path.join(IMAGE_DIR, "*.enc"))
    logging.info(f"🔍 Initial scan found {len(enc_text_files)} encrypted files in {IMAGE_DIR}")

    if len(enc_text_files) >= TEXT_FILE_LIMIT:
        logging.info(f"⚡ Threshold reached: {len(enc_text_files)} encrypted files. Triggering embedding generation...")
        store_embeddings()

if __name__ == "__main__":
    if not os.path.isdir(IMAGE_DIR):
        raise RuntimeError(f"IMAGES_DIR does not exist or is not mounted: {IMAGE_DIR}")
    observer = PollingObserver(timeout=1)
    observer.schedule(MyHandler(), path=IMAGE_DIR, recursive=False)
    initial_scan()
    observer.start()
    logging.info(f"👀 Watching for changes in '{IMAGE_DIR}/'...")

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        print("\n🚫 Stopping observer...")
        observer.stop()
    observer.join()
