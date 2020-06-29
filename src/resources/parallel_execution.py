import sys
import signal
from multiprocessing import Pool, Queue
from resources import logging_custom
from resources import watcher
from resources import drive_uploader

logger = logging_custom.get_logger(__name__)

def signal_term_handler(signal, frame):
        logger.info('Got kill signal. Exiting.')
        sys.exit(0)

class ParallelExecution():

    def __init__(self):
        logger.info('Creating multiprocess pool.')

        run_process_bool = True
        dir_queue = Queue()

        process_pool = Pool(
            1,
            initializer=self.process_init,
            initargs=(run_process_bool, dir_queue)
        )

        logger.info('Starting directory update process...')
        try:
            process_pool.map_async(self.directory_update_process, ['A'])
        except Exception as err:
            logger.info(err)

        signal.signal(signal.SIGTERM, signal_term_handler)

        logger.info('Beginning image uploader...')

        # Create the Google Drive object
        g_drive = drive_uploader.DriveUp(
            dir_queue=dir_queue,
            run_processes_bool=run_process_bool)
        g_drive.upload_files()  # Begin file upload

        logger.info('Stopping Processes...')

        process_pool.close()
        process_pool.join()

        logger.info('Processes stopped.')

    def process_init(self, passed_run_process, passed_dir_queue):
        logger.info('Creating global variables')

        global run_process_bool
        run_process_bool = passed_run_process
        global dir_queue
        dir_queue = passed_dir_queue

    def directory_update_process(self, args):

        logger.info("Created directory watcher process...")

        # Create the dir watch obj
        w = watcher.Watcher(dir_queue=dir_queue)
        w.run()