import time
import os
import zipfile
from glob import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

LOG_DIR = "logs"
ZIP_DIR = "logs/zips"
MAX_FILES = 50

os.makedirs(ZIP_DIR, exist_ok=True)


class LogHandler(FileSystemEventHandler):
    def process_logs(self):
        # Match files like recallAi.log.1, recallAi.log.2
        log_files = sorted(
            glob(os.path.join(LOG_DIR, "recallAi.log.*")),
            key=os.path.getmtime
        )

        if len(log_files) < MAX_FILES:
            return

        # Take first 50 files
        batch = log_files[:MAX_FILES]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"recallAi_logs_{timestamp}.zip"
        zip_path = os.path.join(ZIP_DIR, zip_name)

        print(f"📦 Creating ZIP: {zip_name}")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in batch:
                zipf.write(file, arcname=os.path.basename(file))

        # Delete zipped files
        for file in batch:
            os.remove(file)

        print(f"🗑️ Deleted {len(batch)} log files after zipping")

    def on_created(self, event):
        if not event.is_directory:
            self.process_logs()

    def on_modified(self, event):
        if not event.is_directory:
            self.process_logs()


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(LogHandler(), path=LOG_DIR, recursive=False)
    observer.start()

    print("👀 Watching logs/ for log rotation...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🚫 Stopping observer...")
        observer.stop()

    observer.join()
