import logging


def getDefaultLogHandler() -> logging.Handler:
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    return handler


logger = logging.getLogger("discord.client")
logger.setLevel(logging.DEBUG)
logger.addHandler(getDefaultLogHandler())
