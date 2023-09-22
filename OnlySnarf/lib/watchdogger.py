import time

# pip install watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(event.event_type, event.src_path)

    def on_created(self, event):
        print("on_created", event.src_path)
        print(event.src_path.strip())

        # pass file to appropriate API resource

        # TODO: create appropriate folders for each resource / response framework
        #   message
        #   post
        #   AI

        # ala images uploaded to AI folder are processed with generated text & keywords
        # media in /post are uploaded spontaneously (directories treated as galleries)


event_handler = MyHandler()
observer = Observer()

observer.schedule(event_handler, path='/home/skeetzo/.onlysnarf/uploads', recursive=False)
observer.start()


if __name__ == "__main__":
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()