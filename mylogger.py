import logging.config


def setup_logging(log_file):
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {"default": {"format": "[%(levelname)s|%(name)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s", "datefmt": "%Y-%m-%dT%H:%M:%S%z"}},
            "handlers": {
                "file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": log_file,
                    "formatter": "default",
                    "when": "midnight",
                    "interval": 1,
                    "backupCount": 30,
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "root": {"handlers": ["file", "console"]},
        }
    )
