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
                 "show ntp associations"]

def pytest_addoption(parser):
    parser.addoption(
        "--definitions", action="store", default="definitons.yaml", help="my option: type1 or type2"
    )


@pytest.fixture
def definitions(request):
    cli_arg = request.config.getoption("--definitions")
    return cli_arg

@pytest.fixture(scope='function')
def test_suite_setup():
    """ Do tasks to setup test suite """

    logging.info('Starting Test Suite setup')
    # TODO: Don't hard code yaml_file
    yaml_file = "definitions.yaml"
    test_parameters = tests_tools.import_yaml(yaml_file)
    duts_list = tests_tools.return_dut_list(test_parameters)
    tests_tools.init_show_log(test_parameters)
    duts_struct = tests_tools.init_duts(EOS_SHOW_CMDS, test_parameters)

@pytest.fixture
def parameter_is_terminattr_daemon_running():
    return True

@pytest.fixture
def parameter_is_terminattr_daemon_enabled():
    return True

@pytest.fixture
def tests_parameters():
    return tests_tools.import_yaml('tests_definitions.yaml') 
