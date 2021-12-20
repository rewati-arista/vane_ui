import pytest
import logging
from vane import tests_tools
from vane.config import DEFINITIONS_FILE, DUTS_FILE

def return_duts():
            """ Do tasks to setup test suite """

            logging.info("Starting Test Suite setup")

            test_duts = tests_tools.import_yaml(DUTS_FILE)
            test_parameters = tests_tools.import_yaml(DEFINITIONS_FILE)
            tests_tools.init_show_log(test_parameters)

            logging.info("Discovering show commands from definitions")
            test_defs = tests_tools.return_test_defs(test_parameters)
            show_cmds = tests_tools.return_show_cmds(test_defs)
            duts = tests_tools.init_duts(show_cmds, test_parameters, test_duts)

            logging.info(f"Return to test suites: \nduts: {duts}")
            return duts


def return_duts_names():
            """ Do tasks to setup test suite """

            logging.info("Starting Test Suite setup")
            test_parameters = tests_tools.import_yaml(DUTS_FILE)
            duts_names = tests_tools.return_dut_list(test_parameters)

            logging.info(f"Return to test suites: \nduts_lists: {duts_names}")
            return duts_names


class TestsBase:
    @pytest.fixture(params=return_duts(), ids=return_duts_names(),
                scope="session", autouse=True)
    def dut(self, request):
        """Parameterize each dut for a test case

        Args:
            request (dict): duts from return_duts

        Returns:
            [dict]: a single dut in duts data structure
        """

        dut = request.param
        yield dut



    @pytest.fixture()
    def tests_definitions(self):
        """Return test definitions to each test case

        Args:
            scope (str, optional): Defaults to 'session'.

        Yields:
            [dict]: Return test definitions to test case
        """

        test_parameters = tests_tools.import_yaml(DEFINITIONS_FILE)
        yield tests_tools.return_test_defs(test_parameters)


    
