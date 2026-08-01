import logging


def setup_logging():
    log_config = "INFO"
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(level=log_config, format=log_format)


logger = logging.getLogger("tg-bot")
