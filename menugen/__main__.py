import logging
import atexit
import sys

from menugen.application import MenuGenApp

APP_NAME = "menugen"
APP_VERSION = 1.0


# Helper function to ensure we capture stack traces via logging
# (Note: This method does not work with threads until Python 3.8)
def log_excepthook(exc_type, exc_value, traceback, logger=logging.getLogger()):
    logger.error("Logging an uncaught exception",
                 exc_info=(exc_type, exc_value, traceback))


# Helper function to clean up and alert that we are ending runtime
@atexit.register
def shutdown():
    logging.info(f"{APP_NAME} {APP_VERSION} - Shutting down...")


# Stub code to bootstrap environment and launch into main application
def run():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] [%(funcName)s] [%(levelname)s]  %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler("{0}/{1}.log".format("./", APP_NAME.lower()))
        ]
    )

    # Ensure we capture stack traces in our log
    sys.excepthook = log_excepthook

    # Announce that we are starting up.
    logging.info(f'{APP_NAME} {APP_VERSION} - Starting up...')

    # Launch into the main application run code
    MenuGenApp.run()


if __name__ == '__main__':
    run()
