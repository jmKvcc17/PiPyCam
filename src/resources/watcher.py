import time
from resources import const_vars
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from resources import logging_custom

logger = logging_custom.get_logger(__name__)


class Watcher():


    DIRECTORY_TO_WATCH = const_vars.MOTION_PATH

    def __init__(self, dir_queue=None):
        logger.info('Starting to watch directory...')
        self.observer = Observer()
        self.dir_queue = dir_queue

    def run(self):

        event_handler = Handler(dir_queue=self.dir_queue)
        self.observer.schedule(event_handler,
            self.DIRECTORY_TO_WATCH,
            recursive=True)

        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print('Error')

        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, dir_queue=None):
        super().__init__()
        self.dir_queue = dir_queue
        logger.info('Starting dir event handler...')

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            logger.info('New image created: {0}'.format(event.src_path))
            self.dir_queue.put(event.src_path)
