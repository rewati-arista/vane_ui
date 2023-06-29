""" Logger functionality for Vane testcases to add logs to vane html report and vane_test.log"""

import logging

logger = logging.getLogger("test_case_logs")
logger.setLevel(logging.INFO)
formatter_test = logging.Formatter(
    "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
)

# Logger functionality for Vane testcases to add logs to vane_test.log file
file_handler_test = logging.FileHandler("vane_test.log", mode="w")
file_handler_test.setFormatter(formatter_test)
logger.addHandler(file_handler_test)

# Logger functionality for Vane testcases to add logs to vane html report"""
console_handler_test = logging.StreamHandler()
console_handler_test.setFormatter(formatter_test)
logger.addHandler(console_handler_test)
