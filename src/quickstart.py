from resources import parallel_execution
from resources import logging_custom

logger = logging_custom.get_logger(__name__)


def start_processes():
    try:
        logger.info('Beginning process creation...')
        parallel_execution.ParallelExecution()
    except Exception as err:
        logger.info(err)

def main():

    start_processes()

    logger.info('Beginning upload watch...')


# Start the program
if __name__ == "__main__":
    logger.info('Starting program.')
    main()
