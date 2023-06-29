""" Logger functionality for Vane to add logs to vane.log file"""

import logging as log_module

logging = log_module.getLogger("vane_logs")
logging.setLevel(log_module.INFO)
formatter = log_module.Formatter(
    "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
)

# Logger functionality for Vane to add logs to vane.log file
file_handler = log_module.FileHandler("vane.log", mode="w")
file_handler.setFormatter(formatter)
logging.addHandler(file_handler)
