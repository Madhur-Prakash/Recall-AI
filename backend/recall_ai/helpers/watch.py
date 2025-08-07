import time
from glob import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"{event.src_path} has been modified")
        text_files = glob(os.path.join("images_taken/", "*.txt"))
        print(f"Found {len(text_files)} text files in 'images_taken/' directory")

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
