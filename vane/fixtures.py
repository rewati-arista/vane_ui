import pytest
import logging
from vane import tests_tools
import os
from vane.config import dut_objs, test_defs, test_duts
from jinja2 import Template

def idfn(val):
    """id function for the current fixture data

    Args:
        val (dict): current value of the fixture param

    Returns:
        [string]: name of the current dut
    """
    return val['name']


@pytest.fixture(scope="session", params=dut_objs, ids=idfn)
def dut(request):
    """Parameterize each dut for a test case

    Args:
        request (dict): duts from return_duts

    Returns:
        [dict]: a single dut in duts data structure
    """

    dut = request.param
    yield dut

@pytest.fixture(scope="session")
def duts():
    """Returns all the duts under test

    Returns:
        [dict]: a list of duts
    """
    logging.info("Invoking fixture to get list of duts")
    duts_dict = {}
    for dut in dut_objs:
        duts_dict[dut['name']] = dut
    return duts_dict

@pytest.fixture()
def tests_definitions():
    """Return test definitions to each test case

    Args:
        scope (str, optional): Defaults to 'session'.

    Yields:
        [dict]: Return test definitions to test case
    """

    yield test_defs

@pytest.fixture(autouse=True, scope="class")
def setup_dut(request, duts):
    testname = request.node.fspath
    test_suites = test_defs['test_suites']
    setup_config = []
    for s in test_suites:
        tests = s['testcases']
        for t in tests:
            if s['name'] == os.path.basename(testname):
                setup_config_file = t.get('test_setup', "")
                if setup_config_file != "":
                    setup_config = tests_tools.import_yaml(f"{s['dir_path']}/{setup_config_file}")
                    print(setup_config)
                for dev_name in setup_config:
                    dut = duts[dev_name]
                    setup_schema = setup_config[dev_name]["schema"]
                    if setup_schema is None:
                        config = setup_config[dev_name]["template"].splitlines()
                    else:
                        setup_template = Template(setup_config[dev_name]["template"])
                        config = setup_template.render(setup_schema).splitlines()
                    print(config)
                    gold_config = ['copy running-config flash:gold-config', 'write memory']
                    dut['connection'].enable(gold_config)
                    dut['connection'].config(config)
    yield
    for dev_name in setup_config:
        dut = duts[dev_name]
        restore_config = ['copy flash:gold-config running-config', 'write memory']
        dut['connection'].config(restore_config)


