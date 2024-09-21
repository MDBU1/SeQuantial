import logging
from datetime import datetime


def func_generate_logger_date() -> str:
    date = datetime.now().strftime("%Y%m%d")
    return date


def func_return_str_logfile_name() -> str:
    """

    :return: logfile name (string)
    """
    str_logfile = "LOGFILE_" + func_generate_logger_date() + "_SeQuantial.log"
    return str_logfile


def func_return_int_logging_value(cmds) -> int:
    """

    :param cmds: logging_level
    :return: selects logging level based on passed argparse command
    """
    if cmds.logging_level == "INFO":
        level = logging.INFO
    elif cmds.logging_level == "DEBUG":
        level = logging.DEBUG
    elif cmds.logging_level == "WARNING":
        level = logging.WARNING
    elif cmds.logging_level == "ERROR":
        level = logging.ERROR
    elif cmds.logging_level == "CRITICAL":
        level = logging.CRITICAL
    else:
        level = logging.INFO
    return level


def func_setup_logger(path_save, cmds):
    """

    :param path_save:
    :param cmds:
    :return: formats logfile and saves logger to scan output directory
    """
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        filename=f"{path_save}/{func_return_str_logfile_name()}",
        filemode="a",
        level=func_return_int_logging_value(cmds),
        format="%(asctime)s\n%(levelname)s: %(message)s\n",
        datefmt="%d/%m/%y %H:%M:%S",
    )
    logging.info("logfile initiated: running SeQuantial")
    logging.info(cmds)
