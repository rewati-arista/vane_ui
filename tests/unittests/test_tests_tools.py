"""Test class for tests_tools.py"""
import logging
import os
import shutil
import sys
from unittest.mock import call
import pytest
import yaml
import vane
from tests.unittests.fixtures.test_steps import test_steps
from vane import tests_tools


# Test Utility functions


@pytest.fixture
def loginfo(mocker):
    """Fixture to mock logger info calls from vane.tests_tools"""
    return mocker.patch("vane.vane_logging.logging.info")


@pytest.fixture
def logerr(mocker):
    """Fixture to mock logger error  calls from vane.tests_tools"""
    return mocker.patch("vane.vane_logging.logging.error")


@pytest.fixture
def logdebug(mocker):
    """Fixture to mock logger debug calls from vane.tests_tools"""
    return mocker.patch("vane.vane_logging.logging.debug")


@pytest.fixture
def logcritical(mocker):
    """Fixture to mock logger critical calls from vane.tests_tools"""
    return mocker.patch("vane.vane_logging.logging.critical")


@pytest.fixture
def logerror(mocker):
    """Fixture to mock logger critical calls from vane.tests_tools"""
    return mocker.patch("vane.vane_logging.logging.error")


def read_yaml(yaml_file):
    """Import YAML file as python data structure

    Args:
        yaml_file (str): Name of YAML file

    Returns:
        yaml_data (dict): YAML data structure
    """
    try:
        with open(yaml_file, "r", encoding="utf-8") as input_yaml:
            try:
                yaml_data = yaml.safe_load(input_yaml)
                return yaml_data
            except yaml.YAMLError as err:
                print(">>> ERROR IN YAML FILE")
                logging.error(f"ERROR IN YAML FILE: {err}")
                logging.error("EXITING TEST RUNNER")
                sys.exit(1)
    except OSError as err:
        print(f">>> {yaml_file} YAML FILE MISSING")
        logging.error(f"ERROR YAML FILE: {yaml_file} NOT FOUND. {err}")
        logging.error("EXITING TEST RUNNER")
        sys.exit(1)


# NON TEST-OPS METHODS


def test_filter_duts(loginfo):
    """Validates the method which filters duts according to criteria and dut filter by
    passing different combinations of those inputs"""
    duts = [
        {"role": "Role1", "name": "Test Dut 1"},
        {"role": "Role2", "name": "Test Dut 2"},
    ]

    # check when no criteria or filter is set
    output_duts, output_names = tests_tools.filter_duts(duts, "", "")
    assert len(output_duts) == 2
    assert len(output_names) == 2
    loginfo.assert_called_with("Filter:  by criteria: ")

    # check when criteria is set but filter is not
    output_duts, output_names = tests_tools.filter_duts(duts, "roles", "")
    assert len(output_duts) == 0
    assert len(output_names) == 0
    loginfo.assert_called_with("Filter:  by criteria: roles")

    # check when criteria is not set but filter is set
    output_duts, output_names = tests_tools.filter_duts(duts, "", "Role1")
    assert len(output_duts) == 2
    assert len(output_names) == 2
    loginfo.assert_called_with("Filter: Role1 by criteria: ")

    # check when criteria and filter both are set
    # Criteria: Roles
    # One filter value
    output_duts, output_names = tests_tools.filter_duts(duts, "roles", ["Role1"])
    assert len(output_duts) == 1
    assert len(output_names) == 1

    # Two filter values
    output_duts, output_names = tests_tools.filter_duts(duts, "roles", ["Role1", "Role2"])
    assert len(output_duts) == 2
    assert len(output_names) == 2

    # Criteria: Names
    # One filter value
    output_duts, output_names = tests_tools.filter_duts(duts, "names", ["Test Dut 1"])
    assert len(output_duts) == 1
    assert len(output_names) == 1

    # Two filter values
    output_duts, output_names = tests_tools.filter_duts(duts, "names", ["Test Dut 1", "Test Dut 2"])
    assert len(output_duts) == 2
    assert len(output_names) == 2

    # Criteria: Regex
    # Regex match
    output_duts, output_names = tests_tools.filter_duts(duts, "regex", "Te")
    assert len(output_duts) == 2
    assert len(output_names) == 2
    loginfo.assert_called_with("Filter: Te by criteria: regex")

    # Regex mismatch
    output_duts, output_names = tests_tools.filter_duts(duts, "regex", "R")
    assert len(output_duts) == 0
    assert len(output_names) == 0
    loginfo.assert_called_with("Filter: R by criteria: regex")


def test_parametrize_duts(loginfo, logdebug):
    """Validates the parametrize_duts method"""
    # defining parameters to pass to method under test
    test_fname = "vane-tests-bofa/tests/nrfu_tests/baseline_mgmt_tests"
    test_defs = {
        "test_suites": [
            {
                "name": "baseline_mgmt_tests",
                "testcases": [
                    {"name": "test_local_user_access"},
                    {"name": "test_tacacs_functionality", "criteria": "names", "filter": ["DLFW3"]},
                ],
            }
        ]
    }
    duts = [
        {"role": "Role1", "name": "DLFW3"},
        {"role": "Role2", "name": "Test Dut 2"},
    ]
    actual_dut_parameters = tests_tools.parametrize_duts(test_fname, test_defs, duts)
    loginfo_calls = [
        call("Discover test suite name"),
        call("Filtering test definitions by test suite name: baseline_mgmt_tests"),
        call("Unpack testcases by defining dut and criteria"),
        call("Filter:  by criteria: "),
        call("Filter: ['DLFW3'] by criteria: names"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    logdebug_calls = [
        call(
            "Creating dut parameters.  \nDuts: [{'role': 'Role1', 'name': 'DLFW3'}, "
            "{'role': 'Role2', 'name': 'Test Dut 2'}] \nIds: ['DLFW3', 'Test Dut 2']"
        ),
        call(
            "Creating dut parameters.  \nDuts: [{'role': 'Role1', 'name': 'DLFW3'}]"
            " \nIds: ['DLFW3']"
        ),
    ]
    logdebug.assert_has_calls(logdebug_calls, any_order=False)

    # defining expected output
    expected_dut_parameters = {}
    expected_dut_parameters["test_local_user_access"] = {}
    expected_dut_parameters["test_local_user_access"]["duts"] = duts
    expected_dut_parameters["test_local_user_access"]["ids"] = [duts[0]["name"], duts[1]["name"]]
    expected_dut_parameters["test_tacacs_functionality"] = {}
    expected_dut_parameters["test_tacacs_functionality"]["duts"] = [duts[0]]
    expected_dut_parameters["test_tacacs_functionality"]["ids"] = [duts[0]["name"]]

    assert expected_dut_parameters == actual_dut_parameters


# def test_setup_import_yaml():
#     pass


def test_import_yaml():
    """Validates import yaml method
    FIXTURE NEEDED: test_import_yaml.yaml"""
    logging.info("FIXTURE NEEDED: test_import_yaml.yaml")
    yaml_file = "tests/unittests/fixtures/test_import_yaml.yaml"
    expected_yaml = read_yaml(yaml_file)
    actual_yaml = tests_tools.import_yaml(yaml_file)
    assert expected_yaml == actual_yaml
    logging.info(f"ACTUAL {actual_yaml}")


def test_init_duts(loginfo, logdebug, mocker):
    """Validates the functionality of init_duts
    FIXTURE NEEDED: test_import_yaml.yaml, test_duts_two.yaml"""
    show_cmds = ["show version", "show clock"]
    test_parameters = read_yaml("tests/unittests/fixtures/test_import_yaml.yaml")
    test_duts = read_yaml("tests/unittests/fixtures/test_duts_two.yaml")

    mocker.patch("vane.tests_tools.login_duts", return_value="DUTS")
    mocker.patch("vane.tests_tools.dut_worker")
    actual_output = tests_tools.init_duts(show_cmds, test_parameters, test_duts)

    assert actual_output == "DUTS"

    loginfo_calls = [
        call(
            "Find DUTs and then execute inputted show commands "
            "on each dut. Return structured data of DUTs output "
            "data, hostname, and connection."
        ),
        call("Returning duts data structure"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    logdebug_calls = [
        call("Duts login info: DUTS and create 4 workers"),
        call("Passing the following show commands to workers: ['show version', 'show clock']"),
        call("Future object generated successfully"),
        call("Return duts data structure: DUTS"),
    ]
    logdebug.assert_has_calls(logdebug_calls, any_order=False)


def test_login_duts():
    """Validates the functionality of login_duts
    FIXTURE NEEDED: test_import_yaml.yaml, test_duts_two.yaml"""

    test_parameters = read_yaml("tests/unittests/fixtures/test_import_yaml.yaml")
    test_duts = read_yaml("tests/unittests/fixtures/test_duts_two.yaml")

    tests_tools.login_duts(test_parameters, test_duts)


def test_send_cmds(loginfo, logdebug, logerror, mocker):
    """Validates the functionality of send_cmds method"""

    # mocking call to run commands method on connection object
    mocker_object = mocker.patch("vane.device_interface.PyeapiConn.run_commands")
    mocker_object.side_effect = [
        "output_in_json",
        "output_in_text",
        Exception("show version is erring"),
        "",
    ]

    show_cmds = ["show version"]
    show_cmds_output, show_cmd_list_output = tests_tools.send_cmds(
        show_cmds, vane.device_interface.PyeapiConn, "json"
    )

    # asserting return values when encoding is json
    assert show_cmds_output == "output_in_json"
    assert show_cmd_list_output == show_cmds
    loginfo.assert_called_with("Ran all show commands on dut")
    logdebug_calls = [
        call("List of show commands in show_cmds with encoding json: ['show version']"),
        call("Ran all show cmds with encoding json: ['show version']"),
        call("Return all show cmds: output_in_json"),
    ]
    logdebug.assert_has_calls(logdebug_calls, any_order=False)

    show_cmds_output, show_cmd_list_output = tests_tools.send_cmds(
        show_cmds, vane.device_interface.PyeapiConn, "text"
    )

    # asserting return values when encoding is text
    assert show_cmds_output == "output_in_text"
    assert show_cmd_list_output == show_cmds

    # asserting when run_commands raises an exception
    show_cmds_output, show_cmd_list_output = tests_tools.send_cmds(
        show_cmds, vane.device_interface.PyeapiConn, "text"
    )
    assert show_cmds_output == ""
    assert show_cmd_list_output == []
    loginfo_calls = [
        call("New show_cmds: []"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    logerror.assert_called_with("Error running all cmds: show version is erring")


def test_remove_cmd():
    """Validates functionality of remove_cmd method"""

    error = "show lldp neighbors has an error in it"
    show_cmds = ["show version", "show clock", "show lldp neighbors", "show lldp neighbors status"]
    expected_output = ["show version", "show clock", "show lldp neighbors status"]
    actual_output = tests_tools.remove_cmd(error, show_cmds)
    assert expected_output == actual_output

    error = "show lldp neighbors status has an error in it"
    show_cmds = ["show version", "show clock", "show lldp neighbors", "show lldp neighbors status"]
    expected_output = ["show version", "show clock", "show lldp neighbors"]
    actual_output = tests_tools.remove_cmd(error, show_cmds)
    assert expected_output == actual_output


# def test_dut_worker():
#     pass


def test_return_interfaces(loginfo, logdebug):
    """Validates if interfaces are being read properly from test parameters
    FIXTURE NEEDED: test_return_interfaces_input.yaml"""
    test_parameters = read_yaml("tests/unittests/fixtures/test_return_interfaces_input.yaml")
    actual_output = tests_tools.return_interfaces("DSR01", test_parameters)
    excepted_output = [
        {
            "hostname": "DSR01",
            "interface_name": "Ethernet1",
            "z_hostname": "DCBBW1",
            "z_interface_name": "Ethernet1",
            "media_type": "",
        },
        {
            "hostname": "DSR01",
            "interface_name": "Ethernet2",
            "z_hostname": "DCBBW2",
            "z_interface_name": "Ethernet1",
            "media_type": "",
        },
        {
            "hostname": "DSR01",
            "interface_name": "Ethernet3",
            "z_hostname": "DCBBE1",
            "z_interface_name": "Ethernet1",
            "media_type": "",
        },
        {
            "hostname": "DSR01",
            "interface_name": "Ethernet4",
            "z_hostname": "DCBBE2",
            "z_interface_name": "Ethernet1",
            "media_type": "",
        },
    ]
    assert actual_output == excepted_output
    loginfo_calls = [
        call("Parse test_parameters for interface connections and return them to test"),
        call("Discovering interface parameters for: DSR01"),
        call("Returning interface list."),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)
    logdebug_calls = [
        call(
            "Adding interface parameters:"
            " {'neighborDevice': 'DCBBW1', 'neighborPort': 'Ethernet1', 'port': 'Ethernet1'}"
            " neighbor for: DSR01"
        ),
        call(
            "Adding interface parameters:"
            " {'neighborDevice': 'DCBBW2', 'neighborPort': 'Ethernet1', 'port': 'Ethernet2'}"
            " neighbor for: DSR01"
        ),
        call(
            "Adding interface parameters:"
            " {'neighborDevice': 'DCBBE1', 'neighborPort': 'Ethernet1', 'port': 'Ethernet3'}"
            " neighbor for: DSR01"
        ),
        call(
            "Adding interface parameters:"
            " {'neighborDevice': 'DCBBE2', 'neighborPort': 'Ethernet1', 'port': 'Ethernet4'}"
            " neighbor for: DSR01"
        ),
        call(
            "Returning interface list:"
            " [{'hostname': 'DSR01', 'interface_name': 'Ethernet1',"
            " 'z_hostname': 'DCBBW1', 'z_interface_name': 'Ethernet1', 'media_type': ''},"
            " {'hostname': 'DSR01', 'interface_name': 'Ethernet2',"
            " 'z_hostname': 'DCBBW2', 'z_interface_name': 'Ethernet1', 'media_type': ''},"
            " {'hostname': 'DSR01', 'interface_name': 'Ethernet3',"
            " 'z_hostname': 'DCBBE1', 'z_interface_name': 'Ethernet1', 'media_type': ''},"
            " {'hostname': 'DSR01', 'interface_name': 'Ethernet4',"
            " 'z_hostname': 'DCBBE2', 'z_interface_name': 'Ethernet1', 'media_type': ''}]"
        ),
    ]
    logdebug.assert_has_calls(logdebug_calls, any_order=False)


def test_get_parameters(loginfo, logdebug):
    """Validates getting test case details from test parameters, suites and name
    FIXTURES NEEDED: test_return_show_cmds.yaml"""
    tests_parameters = read_yaml("tests/unittests/fixtures/test_return_show_cmds.yaml")
    test_suite = "sample_network_tests/aaa/test_aaa.py"
    test_case = "test_if_exec_authorization_methods_set_on_"

    expected_output = {
        "name": "test_if_exec_authorization_methods_set_on_",
        "description": "Verify AAA exec authorization are method-lists set correct",
        "exec_auth": ["none"],
        "show_cmd": "show aaa methods all",
        "expected_output": None,
        "comment": None,
        "result": True,
        "test_suite": "test_aaa.py",
    }

    actual_output = tests_tools.get_parameters(tests_parameters, test_suite, test_case)
    assert expected_output == actual_output

    loginfo_calls = [
        call("Identify test case and return parameters"),
        call("Return testcases for Test Suite: test_aaa.py"),
        call("Return parameters for Test Case: test_if_exec_authorization_methods_set_on_"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    logdebug_calls = [
        call(
            "Suite_parameters:"
            " [{'name': 'test_aaa.py',"
            " 'testcases': [{'name': 'test_if_authentication_counters_are_incrementing_on_',"
            " 'description': 'Verify AAA counters are working correctly',"
            " 'show_cmds': ['show lldp neighbors', 'show aaa counters'], 'expected_output': None,"
            " 'comment': None, 'result': True},"
            " {'name': 'test_if_aaa_session_logging_is_working_on_',"
            " 'description': 'Verify AAA session logging is working by"
            " identifying eapi connection',"
            " 'show_cmd': 'show users detail', 'expected_output': 'commandApi',"
            " 'comment': None, 'result': True},"
            " {'name': 'test_if_commands_authorization_methods_set_on_',"
            " 'description': 'Verify AAA command authorization are method-lists set correct',"
            " 'cmd_auth': ['none'], 'show_cmd': 'show aaa methods all', 'expected_output': None,"
            " 'comment': None, 'result': True},"
            " {'name': 'test_if_exec_authorization_methods_set_on_',"
            " 'description': 'Verify AAA exec authorization are method-lists set correct',"
            " 'exec_auth': ['none'], 'show_cmd': 'show aaa methods all', 'expected_output': None,"
            " 'comment': None, 'result': True}]}]"
        ),
        call(
            "Case_parameters: {'name': 'test_if_exec_authorization_methods_set_on_',"
            " 'description': 'Verify AAA exec authorization are method-lists set correct',"
            " 'exec_auth': ['none'], 'show_cmd': 'show aaa methods all', 'expected_output': None,"
            " 'comment': None, 'result': True}"
        ),
    ]
    logdebug.assert_has_calls(logdebug_calls, any_order=False)


def test_verify_show_cmd(loginfo, logdebug, logcritical):
    """Validates verification of show commands being executed on given dut"""
    dut = {"output": {"show clock": ""}, "name": "Test Dut"}
    show_cmd = "show clock"
    tests_tools.verify_show_cmd(show_cmd, dut)
    loginfo.assert_called_with(
        "Verifying if show command show clock was successfully executed on Test Dut dut"
    )
    logdebug.assert_called_with("Verified output for show command show clock on Test Dut")

    show_cmd = "show lldp neighbors"

    # handling the assert False raised in the verify_show_cmd method
    # when show_cmd is not executed on the dut
    with pytest.raises(AssertionError):
        tests_tools.verify_show_cmd(show_cmd, dut)
    logcritical.assert_called_with("Show command show lldp neighbors not executed on Test Dut")


def test_verify_tacacs(loginfo, logdebug):
    """Validates verification of tacacs servers on duts"""
    dut = {"output": {"show tacacs": {"json": {"tacacsServers": []}}}, "name": "Test Dut"}
    actual_output = tests_tools.verify_tacacs(dut)
    assert not actual_output
    loginfo.assert_called_with("Verifying if tacacs server(s) are configured on Test Dut dut")
    dut["output"]["show tacacs"]["json"]["tacacsServers"] = [{"One": "value1"}, {"Two": "value2"}]
    actual_output = tests_tools.verify_tacacs(dut)
    assert actual_output
    logdebug.assert_called_with("2 tacacs servers are configured so returning True")


def test_verify_veos(loginfo, logdebug):
    """Validates verification of dut instances' model"""
    dut = {"output": {"show version": {"json": {"modelName": "vEOS"}}}, "name": "Test Dut"}
    actual_output = tests_tools.verify_veos(dut)
    loginfo.assert_called_with("Verifying if Test Dut DUT is a VEOS instance. Model is vEOS")
    logdebug.assert_called_with("Test Dut is a VEOS instance so returning True")
    assert actual_output
    dut["output"]["show version"]["json"]["modelName"] = "cEOS"
    actual_output = tests_tools.verify_veos(dut)
    loginfo.assert_called_with("Verifying if Test Dut DUT is a VEOS instance. Model is cEOS")
    logdebug.assert_called_with("Test Dut is not a VEOS instance so returning False")
    assert not actual_output


def test_return_show_cmds(loginfo, logdebug):
    """Validates if correct show commands get returned given test suites
    FIXTURES NEEDED: test_return_show_cmds.yaml"""
    test_parameters = read_yaml("tests/unittests/fixtures/test_return_show_cmds.yaml")
    expected_output = [
        "show version",
        "show lldp neighbors",
        "show aaa counters",
        "show users detail",
        "show aaa methods all",
    ]
    actual_output = tests_tools.return_show_cmds(test_parameters)
    assert expected_output == actual_output
    loginfo_calls = [
        call("Finding show commands in test suite: test_aaa.py"),
        call(
            "The following show commands are required for test cases: "
            "['show version', 'show lldp neighbors', 'show aaa counters', "
            "'show users detail', 'show aaa methods all']"
        ),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    logdebug_calls = [
        call(
            "Discover the names of test suites from"
            " {'test_suites':"
            " [{'name': 'test_aaa.py',"
            " 'testcases': [{'name': 'test_if_authentication_counters_are_incrementing_on_',"
            " 'description': 'Verify AAA counters are working correctly',"
            " 'show_cmds': ['show lldp neighbors', 'show aaa counters'], 'expected_output': None,"
            " 'comment': None, 'result': True},"
            " {'name': 'test_if_aaa_session_logging_is_working_on_',"
            " 'description': 'Verify AAA session logging is working by"
            " identifying eapi connection',"
            " 'show_cmd': 'show users detail', 'expected_output': 'commandApi',"
            " 'comment': None, 'result': True},"
            " {'name': 'test_if_commands_authorization_methods_set_on_',"
            " 'description': 'Verify AAA command authorization are method-lists set correct',"
            " 'cmd_auth': ['none'], 'show_cmd': 'show aaa methods all', 'expected_output': None,"
            " 'comment': None, 'result': True},"
            " {'name': 'test_if_exec_authorization_methods_set_on_',"
            " 'description': 'Verify AAA exec authorization are method-lists set correct',"
            " 'exec_auth': ['none'], 'show_cmd': 'show aaa methods all', 'expected_output': None,"
            " 'comment': None, 'result': True}]}]}"
        ),
        call("Found show commands ['show lldp neighbors', 'show aaa counters']"),
        call("Adding Show commands show lldp neighbors"),
        call("Adding Show commands show aaa counters"),
        call("Found show command show users detail"),
        call("Adding Show command show users detail"),
        call("Found show command show aaa methods all"),
        call("Adding Show command show aaa methods all"),
        call("Found show command show aaa methods all"),
    ]
    logdebug.assert_has_calls(logdebug_calls, any_order=False)


def test_return_test_defs(logdebug):
    """Validates if test definitions are being generated correctly
    Creates a temporary reports/test_definition and deletes it before exiting
    FIXTURE NEEDED: test_return_test_defs"""
    logging.info("FIXTURE NEEDED: test_return_test_defs")
    expected_yaml = {
        "parameters": {
            "report_dir": "reports",
            "test_cases": "test_tacacs.py",
            "test_dirs": ["sample_network_tests/tacacs"],
            "test_definitions": "test_definition.yaml",
        }
    }
    os.makedirs(os.path.dirname("reports/test_definition.yaml"), exist_ok=True)
    actual_output = tests_tools.return_test_defs(expected_yaml)
    expected_output = read_yaml("tests/unittests/fixtures/test_return_test_defs.yaml")
    assert (
        actual_output["test_suites"][0]["testcases"]
        == expected_output["test_suites"][0]["testcases"]
    )
    assert actual_output["test_suites"][0]["name"] == expected_output["test_suites"][0]["name"]
    assert actual_output == expected_output

    logdebug.assert_called_with(
        "Return the following test definitions data structure "
        "{'test_suites': [{'name': 'test_tacacs.py', "
        "'testcases': [{'name': 'test_if_tacacs_is_sending_messages_on_', "
        "'description': 'Verify tacacs messages are sending correctly', 'show_cmd': 'show tacacs', "
        "'expected_output': None, 'report_style': 'modern', "
        "'test_criteria': 'Verify tacacs messages are sending correctly', "
        "'criteria': 'names', 'filter': ['DSR01', 'DCBBW1'], 'comment': None, 'result': True}, "
        "{'name': 'test_if_tacacs_is_receiving_messages_on_', "
        "'description': 'Verify tacacs messages are received correctly', "
        "'show_cmd': 'show tacacs', "
        "'expected_output': None, 'report_style': 'modern', "
        "'test_criteria': 'Verify tacacs messages are received correctly', "
        "'criteria': 'names', 'filter': ['DSR01', 'DCBBW1'], 'comment': None, 'result': True}], "
        "'dir_path': 'sample_network_tests/tacacs'}]}"
    )
    shutil.rmtree("reports", ignore_errors=True)


def test_export_yaml():
    """Validates exporting of data into a yaml file"""
    yaml_file = "export_file.yaml"
    yaml_data = {
        "parameters": {
            "report_dir": "reports",
            "test_cases": "test_tacacs.py",
            "test_dirs": ["../systests/tacacs"],
            "test_definitions": "test_definition.yaml",
        }
    }
    assert not os.path.isfile(yaml_file)
    tests_tools.export_yaml(yaml_file, yaml_data)

    # check if yaml file got created
    assert os.path.isfile(yaml_file)

    # check if yaml file got written to correctly
    with open(yaml_file, "r", encoding="utf-8") as input_yaml:
        assert yaml_data == yaml.safe_load(input_yaml)
    os.remove(yaml_file)


def test_export_text():
    """Validates exporting of data to text file"""
    text_file = "text/export_file.txt"
    text_data = {
        "report_dir": "reports",
        "test_cases": "test_tacacs.py",
        "test_dirs": ["../systests/tacacs"],
        "test_definitions": "test_definition.yaml",
    }
    expected_data = ""
    for key, value in text_data.items():
        expected_data += str(key) + str(value) + "\n"

    assert not os.path.exists(text_file)
    tests_tools.export_text(text_file, text_data)

    # check if text file got created
    assert os.path.exists(text_file)

    # # check if text file got written to correctly
    with open("text/export_file.txt", "r", encoding="utf-8") as file:
        contents = file.read()
        assert contents == expected_data

    shutil.rmtree("text", ignore_errors=True)


def test_generate_duts_file():
    """Validates generation of duts file from duts data"""
    dut_file = "dut_file.yml"
    dut = {
        "DSR01": {
            "ip_addr": "192.168.0.9",
            "node_type": "veos",
            "neighbors": [
                {"neighborDevice": "DCBBW1", "neighborPort": "Ethernet1", "port": "Ethernet1"},
                {"neighborDevice": "DCBBW2", "neighborPort": "Ethernet1", "port": "Ethernet2"},
            ],
        }
    }

    assert not os.path.exists(dut_file)
    with open(dut_file, "w", encoding="utf-8") as file:
        tests_tools.generate_duts_file(dut, file, "username", "password!")

    # check if yaml file got created
    assert os.path.isfile(dut_file)

    # check if yaml file got written to correctly
    with open(dut_file, "r", encoding="utf-8") as input_yaml:
        actual = yaml.safe_load(input_yaml)
        assert dut["DSR01"]["neighbors"] == actual[0]["neighbors"]
        assert dut["DSR01"]["ip_addr"] == actual[0]["mgmt_ip"]
    os.remove(dut_file)


def test_create_duts_file():
    """Validates generation of duts file from topology and inventory file
    FIXTURES NEEDED: test_topology.yaml, test_inventory.yaml"""
    topology_data = "tests/unittests/fixtures/test_topology.yaml"
    inventory_data = "tests/unittests/fixtures/test_inventory.yaml"

    expected_data = {
        "duts": [
            {
                "mgmt_ip": "10.255.99.253",
                "name": "DCBBW1",
                "neighbors": [
                    {"neighborDevice": "DSR01", "neighborPort": "Ethernet1", "port": "Ethernet1"}
                ],
                "password": "cvp123!",
                "transport": "https",
                "username": "cvpadmin",
                "role": "unknown",
            }
        ],
        "servers": [],
    }

    file = tests_tools.create_duts_file(topology_data, inventory_data)
    assert os.path.isfile(file)
    with open(file, "r", encoding="utf-8") as input_yaml:
        assert expected_data == yaml.safe_load(input_yaml)
    os.remove(file)


# TEST-OPS METHODS

# global variables

TEST_DEFINITION = read_yaml("tests/unittests/fixtures/test_test_definitions.yaml")
TEST_SUITE = "test_memory.py"
DUT = read_yaml("tests/unittests/fixtures/test_duts.yaml")

# utility method for creating tops object


def return_test_ops_object(mocker):
    """Utility function to create tops object needed for testing TestOps methods"""
    # creating test ops object and mocking inspect_stack call
    mocker.patch("inspect.stack", return_value=["", ["", "", "", "test_memory_utilization_on_"]])

    tops = tests_tools.TestOps(TEST_DEFINITION, TEST_SUITE, DUT)

    return tops


def test_init(mocker):
    "Validates that TestOPs object gets initialized correctly"

    # mocking the call to _verify_show_cmd and _get_parameters in init()
    mocker.patch(
        "vane.tests_tools.TestOps._get_parameters",
        return_value=read_yaml("tests/unittests/fixtures/test_test_parameters.yaml"),
    )
    mocker.patch("vane.tests_tools.TestOps._verify_show_cmd", return_value=True)
    tops = return_test_ops_object(mocker)

    # assert all the object values are set correctly
    assert tops.test_case == "test_memory_utilization_on_"
    assert tops.test_parameters == read_yaml("tests/unittests/fixtures/test_test_parameters.yaml")
    assert tops.expected_output == 80
    assert tops.dut == read_yaml("tests/unittests/fixtures/test_duts.yaml")
    assert tops.dut_name == "DCBBW1"
    assert tops.interface_list == [
        {
            "hostname": "DCBBW1",
            "interface_name": "Ethernet1",
            "media_type": "",
            "z_hostname": "DSR01",
            "z_interface_name": "Ethernet1",
        },
        {
            "hostname": "DCBBW1",
            "interface_name": "Ethernet3",
            "media_type": "",
            "z_hostname": "BLFW1",
            "z_interface_name": "Ethernet1",
        },
        {
            "hostname": "DCBBW1",
            "interface_name": "Ethernet4",
            "media_type": "",
            "z_hostname": "BLFW2",
            "z_interface_name": "Ethernet1",
        },
    ]
    assert tops.results_dir == "reports/results"
    assert tops.report_dir == "reports"

    assert tops.show_cmds == ["show version", "show version"]
    assert tops._show_cmds == ["show version", "show version"]
    assert tops.show_cmd == "show version"

    output = """Arista vEOS-lab
Hardware version: 
Serial number: SN-DCBBW1
Hardware MAC address: a486.49d7.e2d9
System MAC address: a486.49d7.e2d9

Software image version: 4.27.2F
Architecture: x86_64
Internal build version: 4.27.2F-26069621.4272F
Internal build ID: 2fd003fd-04c4-4b44-9c26-417e6ca42009
Image format version: 1.0
Image optimization: None

Uptime: 3 days, 4 hours and 56 minutes
Total memory: 3938900 kB
Free memory: 2755560 kB\n\n"""

    assert tops.show_cmd_txts == tops._show_cmd_txts == [output, output]
    assert tops.show_cmd_txt == output

    assert tops.show_output == ""
    assert not tops.test_steps

    assert tops.comment == ""
    assert tops.output_msg == ""
    assert not tops.actual_results
    assert not tops.expected_results
    assert tops.actual_output == ""
    assert not tops.test_result
    assert tops.test_id == tops.test_parameters.get("test_id", None)


def test_test_ops_verify_show_cmd(loginfo, logdebug, logcritical, mocker):
    """Validates verification of show commands being executed on given dut"""

    # mocking the call to _get_parameters in init()
    mocker.patch(
        "vane.tests_tools.TestOps._get_parameters",
        return_value=read_yaml("tests/unittests/fixtures/test_test_parameters.yaml"),
    )
    tops = return_test_ops_object(mocker)

    # handling the true case
    show_cmds = ["show version"]
    tops._verify_show_cmd(show_cmds, DUT)
    loginfo.assert_called_with(
        "Verifying if show command ['show version'] were successfully executed on DCBBW1 dut"
    )
    logdebug.assert_called_with("Verified output for show command show version on DCBBW1")

    # handling the false case
    show_cmd = ["show lldp neighbors"]

    # handling the assert False raised in the verify_show_cmd method
    # when show_cmd is not executed on the dut
    with pytest.raises(AssertionError):
        tops._verify_show_cmd(show_cmd, DUT)
    logcritical.assert_called_with("Show command show lldp neighbors not executed on DCBBW1")


def test_write_results(loginfo, logdebug, mocker):
    "Validates functionality of write_results method"

    # mocking the call to _verify_show_cmd and _get_parameters in init()
    mocker.patch(
        "vane.tests_tools.TestOps._get_parameters",
        return_value=read_yaml("tests/unittests/fixtures/test_test_parameters.yaml"),
    )
    mocker.patch("vane.tests_tools.TestOps._verify_show_cmd", return_value=True)

    # mocking call to export_yaml
    mocker_object = mocker.patch("vane.tests_tools.export_yaml")

    tops = return_test_ops_object(mocker)
    tops._write_results()

    # assert the logs
    loginfo.assert_called_with("Preparing to write results")
    logdebug.assert_called_with(
        "Creating results file named reports/results/result-test_memory_utilization_on_-DSR01.yml"
    )

    # assert export_yaml got called with correctly processed arguments
    test_params = read_yaml("tests/unittests/fixtures/test_test_parameters.yaml")
    mocker_object.assert_called_once_with(
        "reports/results/result-test_memory_utilization_on_-DSR01.yml", test_params
    )


# def test_write_text_results():
#     pass


def test_test_ops_get_parameters(loginfo, logdebug, mocker):
    """Validates getting test case details from test parameters, suites and name"""

    # mocking the call to _verify_show_cmd in init()
    mocker.patch("vane.tests_tools.TestOps._verify_show_cmd", return_value=True)
    tops = return_test_ops_object(mocker)

    expected_output = {
        "name": "test_memory_utilization_on_",
        "description": "Verify memory is not exceeding high utilization",
        "show_cmd": "show version",
        "expected_output": 80,
        "report_style": "modern",
        "test_criteria": "Verify memory is not exceeding high utilization",
        "criteria": "names",
        "filter": ["DSR01", "DCBBW1"],
        "comment": None,
        "result": True,
        "test_suite": "test_memory.py",
    }

    actual_output = tops._get_parameters(TEST_DEFINITION, TEST_SUITE, "test_memory_utilization_on_")
    assert expected_output == actual_output

    loginfo_calls = [
        call("Identify test case and return parameters"),
        call("Returning parameters for Test Case: test_memory_utilization_on_"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    logdebug_calls = [
        call("Return testcases for Test Suite: test_memory.py"),
        call(
            "Suite_parameters: [{'name': 'test_memory.py', 'testcases': "
            "[{'name': 'test_memory_utilization_on_', "
            "'description': 'Verify memory is not exceeding high utilization', "
            "'show_cmd': 'show version', 'expected_output': 80, 'report_style': 'modern', "
            "'test_criteria': 'Verify memory is not exceeding high utilization', "
            "'criteria': 'names', 'filter': ['DSR01', 'DCBBW1'], 'comment': None, "
            "'result': True}]}]"
        ),
        call(
            "Case_parameters: {'name': 'test_memory_utilization_on_', "
            "'description': 'Verify memory is not exceeding high utilization', "
            "'show_cmd': 'show version', 'expected_output': 80, 'report_style': 'modern', "
            "'test_criteria': 'Verify memory is not exceeding high utilization', "
            "'criteria': 'names', 'filter': ['DSR01', 'DCBBW1'], 'comment': None, "
            "'result': True}"
        ),
    ]
    logdebug.assert_has_calls(logdebug_calls, any_order=False)


# def test_generate_report(self, dut_name, output):
#     pass


# def test_html_report():
#     pass


def test_test_ops_verify_veos(loginfo, logdebug, mocker):
    """Validates verification of the model of the dut"""

    # mocking the call to _verify_show_cmd and _get_parameters in init()
    mocker.patch(
        "vane.tests_tools.TestOps._get_parameters",
        return_value=read_yaml("tests/unittests/fixtures/test_test_parameters.yaml"),
    )
    mocker.patch("vane.tests_tools.TestOps._verify_show_cmd", return_value=True)
    tops = return_test_ops_object(mocker)

    # handling the true case
    tops.verify_veos()
    loginfo.assert_called_with("Verifying if DCBBW1 DUT is a VEOS instance. Model is vEOS-lab")
    logdebug.assert_called_with("DCBBW1 is a VEOS instance so returning True")

    # handling the false case
    DUT["output"]["show version"]["json"]["modelName"] = "cEOS"
    tops.verify_veos()
    logdebug.assert_called_with("DCBBW1 is not a VEOS instance so returning False")


def test_parse_test_steps(loginfo, mocker):
    """Validates verification of the parse_test_steps method
    FIXTURE NEEDED: tests/unittests/fixtures/test_steps/test_steps.py"""

    # mocking the call to _verify_show_cmd and _get_parameters in init()
    mocker.patch(
        "vane.tests_tools.TestOps._get_parameters",
        return_value=read_yaml("tests/unittests/fixtures/test_test_parameters.yaml"),
    )
    mocker.patch("vane.tests_tools.TestOps._verify_show_cmd", return_value=True)
    tops = return_test_ops_object(mocker)
    tops.parse_test_steps(test_steps.TestSyslogFunctionality.test_syslog_functionality_on_server)

    # assert the test steps log call
    loginfo.assert_called_with(
        "These are test steps "
        "[' Creating Testops class object and initializing the variable', "
        "' Running Tcpdump on syslog server and entering in config mode\\n"
        "             and existing to verify logging event are captured.',"
        " ' Comparing the actual output and expected output. Generating docx report']"
    )


# def test_run_show_cmds(self, show_cmds, encoding="json"):
#     pass

# will write test for run_show_cmd, write_text_results, generate_report,
# html, test_setup_import_yaml once change is in
# name fixtures

# ASK FOR NAME CHANGE TO show_cmds
# ask about duplicate functions (verify veos/tacacs/show command/get params)

# BUG in parse_test_Steps
# HTML report will need changes

# mock init calls?
# key errors (also in init)
