import pytest
import yaml 
import logging
import tests_tools
from datetime import datetime
from py.xml import html
import re

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
                 "show hostname",
                 "show processes",
                 "show system environment temperature"]

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


def find_nodeid(nodeid):

    if re.match('.*\[(.*)\]',nodeid):
        return re.match('.*\[(.*)\]',nodeid)[1]
    else:
        return "NONE"

def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Device', class_='sortable string', col='device'))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(find_nodeid(report.nodeid), class_='col-device'))
    cells.pop()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if str(item.function.__doc__).split('Args:')[0]:
        report.description = str(item.function.__doc__).split('Args:')[0]
    elif str(item.function.__doc__):
        report.description = str(item.function.__doc__)
    else:
        report.description = "No Description"
