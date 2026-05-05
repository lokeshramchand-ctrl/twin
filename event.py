from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

from rag import load_documents, build_index, save_index

DATA_PATH = "project/data/v1"   # start watching V1 folder


class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        print(f"\n[EVENT] File changed: {event.src_path}")
        print("[EVENT] Rebuilding index...")

        docs = load_documents(DATA_PATH)
        index, chunks = build_index(docs)
        save_index(index, chunks)

        print("[EVENT] Index updated successfully.\n")


def start_watcher():
    event_handler = ChangeHandler()
    observer = Observer()

    observer.schedule(event_handler, path=DATA_PATH, recursive=False)
    observer.start()

    print("🚀 Watching for changes in:", DATA_PATH)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_watcher()