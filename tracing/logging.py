import logging
import datetime


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.fmt.format(
                self.reset, self.bold_red, self.blue, self.yellow, self.red, self.grey
            ),
            logging.INFO: self.fmt.format(
                self.reset, self.bold_red, self.blue, self.yellow, self.red, self.grey
            ),
            logging.WARNING: self.fmt.format(
                self.reset, self.bold_red, self.blue, self.yellow, self.red, self.grey
            ),
            logging.ERROR: self.fmt.format(
                self.reset, self.bold_red, self.blue, self.yellow, self.red, self.grey
            ),
            logging.CRITICAL: self.fmt.format(
                self.reset, self.bold_red, self.blue, self.yellow, self.red, self.grey
            ),
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Create custom logger logging all five levels
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define format for logs
fmt = "{1}%(asctime)s {0}| {2}%(levelname)8s{0} | {3}%(filename)s{0} | {4}%(funcName)s(){0} | {5}%(message)s{0}"
fmt_file = "%(asctime)s | %(levelname)8s | %(filename)s | %(funcName)s() | %(message)s"

# Create stdout handler for logging to the console (logs all five levels)
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter(fmt))

# Create file handler for logging to a file (logs all five levels)
today = datetime.date.today()
file_handler = logging.FileHandler("mcp_{}.log".format(today.strftime("%Y_%m_%d")))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(fmt_file))

# Add both handlers to the logger
logger.addHandler(stdout_handler)
logger.addHandler(file_handler)
