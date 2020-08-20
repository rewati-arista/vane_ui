import pytest
import yaml 
import logging
import tests_tools


logging.basicConfig(level=logging.INFO, filename='conftest.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info('Starting conftest.log file')


# TODO: Remove from conftest.py
EOS_SHOW_CMDS = ["show daemon",
                 "dir",
                 "show extensions",
                 "show running-config section username",
                 "show tacacs",
                 "show aaa counters",
                 "show users detail",
                 "show aaa methods all",
                 "show management api http-commands",
                 "show logging",
                 "show zerotouch",
                 "dir flash:zerotouch-config",
                 "show ntp status",
                 "show ntp associations",
                 "show hostname"]

def pytest_addoption(parser):
    parser.addoption(
        "--definitions", action="store", default="definitons.yaml", help="my option: type1 or type2"
    )


@pytest.fixture
def definitions(request):
    cli_arg = request.config.getoption("--definitions")
    return cli_arg

def return_duts():
    """ Do tasks to setup test suite """

    logging.info('Starting Test Suite setup')
    # TODO: Don't hard code yaml_file
    yaml_file = "definitions.yaml"
    test_parameters = tests_tools.import_yaml(yaml_file)
    duts_list = tests_tools.return_dut_list(test_parameters)
    tests_tools.init_show_log(test_parameters)
    duts = tests_tools.init_duts(EOS_SHOW_CMDS, test_parameters)

    logging.info(f'Return to test suites: \nduts: {duts}')
    return duts

def return_duts_names():
    """ Do tasks to setup test suite """

    logging.info('Starting Test Suite setup')
    # TODO: Don't hard code yaml_file
    yaml_file = "definitions.yaml"
    test_parameters = tests_tools.import_yaml(yaml_file)
    duts_names = tests_tools.return_dut_list(test_parameters)

    logging.info(f'Return to test suites: \nduts_lists: {duts_names}')
    return duts_names

@pytest.fixture(params=return_duts(), ids=return_duts_names(), scope='session')
def dut(request):
    dut = request.param
    return dut


@pytest.fixture
def tests_definitions(scope='session'):
    yield tests_tools.import_yaml('tests_definitions.yaml') 
    logging.info('Cleaning up test_defintions fixture')
