from glob import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from recall_ai.helpers.utils import setup_logging

import time
print("Before importing store_embeddings")
st = time.time()
from recall_ai.vector_embeddings.quad_vecor_embedding import quad_store_embeddings
print("After importing store_embeddings")
fn = time.time() - st
print(f"Time taken to import store_embeddings: {fn:.2f} seconds")


logging = setup_logging()

TEXT_FILE_LIMIT = 34

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".enc"):
            enc_text_files = glob(os.path.join("images_taken", "*.enc"))
            logging.info(f"🔄️Current encrypted text files count: {len(enc_text_files)}")

            if len(enc_text_files) >= TEXT_FILE_LIMIT:
                res = quad_store_embeddings()
                if(res['message'] != "Embeddings stored successfully."):
                    logging.error(f"❌Error occurred while storing embeddings: {res['message']}")
                logging.info(f"✅ Embeddings stored successfully. Current count: {len(enc_text_files)}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(MyHandler(), path="images_taken", recursive=False)
    observer.start()
    print("👀 Watching for changes in 'images_taken/'...")

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        print("\n🚫 Stopping observer...")
        observer.stop()
    observer.join()
