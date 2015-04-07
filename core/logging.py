import logging


from misc.logging_handler import DailyRotationHandler, local_time_offset

FORMAT = '%(asctime)s  [%(levelname)s] --[%(name)s:%(module)s/%(funcName)s]-- %(message)s'
CHATFORMAT = '[%(asctime)] %(message)'

TIMEFORMAT = '%H:%M:%S'

LOGGINGLEVELS = {"NOTSET": logging.NOTSET, "DEBUG": logging.DEBUG,
                 "INFO": logging.INFO, "WARNING": logging.WARNING,
                 "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL}


def setup_logging(loglevel="INFO", console_loglevel=None,
                  log_path_format="%Y/%m/%Y-%m-%d.log"):

    nullhandler = logging.NullHandler()
    logging.basicConfig(level=loglevel,
                        handlers=[nullhandler])

    if console_loglevel is None:
        console_loglevel = loglevel

    logLevel = LOGGINGLEVELS[loglevel]
    console_loglevel = LOGGINGLEVELS[console_loglevel]

    logging_format = logging.Formatter(FORMAT, datefmt=TIMEFORMAT)
    chat_logging_format = logging.Formatter(CHATFORMAT, datefmt=TIMEFORMAT)

    # Set up the handler for logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_loglevel)
    console_handler.setFormatter(logging_format)

    # A logger that only logs to the console.
    console_logger = logging.getLogger("console")
    console_logger.addHandler(console_handler)

    # Set up handler for logging to file that is changed
    # every day so that the log files are organized.
    file_handler = DailyRotationHandler(log_path_format, encoding="utf-8")
    file_handler.setFormatter(logging_format)
    file_handler.setLevel(loglevel)

    # The bot logger logs to file as well as to console.
    bot_logger = logging.getLogger("bot")
    bot_logger.addHandler(console_handler)
    bot_logger.addHandler(file_handler)


    bot_logger.info("IRC Bot Logger initialised.")

    offset, tzname = local_time_offset()
    if offset >= 0:
        offset = "+"+str(offset)
    else:
        offset = str(offset)

    bot_logger.info("All time stamps are in UTC%s (%s)", offset, tzname)
    print("Well, we tried something.", loglevel)
