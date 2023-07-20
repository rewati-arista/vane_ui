"""Test class for test_step_client.py"""

from unittest.mock import call
import pytest
from vane import test_step_client


# Global test parameters
TEST_DIR = "sample_network_tests/host"
TEST_FILE = ["sample_network_tests/host/test_host.py"]
TEST_STEP = [
    "01/01/2023 00:00:00",
    "TD: Verify hostname is set on device is correct",
    "TS: Collecting the output of 'show hostname' command from DUT",
    "TS: Verify LLDP system name",
    "TS: Creating test report based on results",
]
NO_TEST_STEPS = [
    "01/01/2023 00:00:00",
    "N/a no Test Steps found",
]


# pylint: disable=redefined-outer-name
@pytest.fixture
def loginfo(mocker):
    """Fixture to mock logger info calls from vane.test_step_client"""
    return mocker.patch("vane.vane_logging.logging.info")


@pytest.fixture
def logdebug(mocker):
    """Fixture to mock logger debug calls from vane.test_step_client"""
    return mocker.patch("vane.vane_logging.logging.debug")


def test_test_step_client_constructor(loginfo, logdebug):
    "Unit Test for TestStepClient object __init__ method"

    _ = test_step_client.TestStepClient(TEST_DIR)

    loginfo_calls = [
        call("Creating Test Step Client object"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    logdebug_calls = [
        call(f"Set Test Step Client object directory to {TEST_DIR}"),
    ]
    logdebug.assert_has_calls(logdebug_calls, any_order=False)


def test_write_test_steps(loginfo, mocker):
    "Unit Test for TestStepClient object, write_test_steps method"

    mocker_object = mocker.patch("vane.test_step_client.TestStepClient.walk_dir")
    test_steps = test_step_client.TestStepClient(TEST_DIR)
    test_steps.write_test_steps()
    mocker_object.assert_called_once()

    loginfo_calls = [
        call("Start writing test case steps"),
        call("Ending writing test case steps"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)


def test_write_walk_dir(logdebug, mocker):
    "Unit Test for TestStepClient object, method walk_dir"

    mocker_object = mocker.patch("vane.test_step_client.TestStepClient.parse_file")
    test_steps = test_step_client.TestStepClient([TEST_DIR])
    test_steps.walk_dir()
    mocker_object.assert_called_once()

    files = [
        "test_definition.yaml",
        "__init__.py",
        "test_host.py",
        "setup.yml",
        "test_host.json",
        "test_host.md",
    ]

    logdebug_calls = [
        call(f"Walking directory {TEST_DIR} for test cases"),
        call(f"Discovered files {files} in directory {TEST_DIR}"),
        call(f"Discovered test files: {TEST_FILE} for parsing"),
    ]
    logdebug.assert_has_calls(logdebug_calls, any_order=False)


def test_parse_file(loginfo, logdebug, mocker):
    "Unit Test for TestStepClient object module parse_file"

    # Set datetime to a known value
    mocker.patch(
        "vane.test_step_client.TestStepClient.now",
        return_value="01/01/2023 00:00:00",
    )
    mocker_object_one = mocker.patch("vane.test_step_client.TestStepClient.output_json")
    mocker_object_two = mocker.patch("vane.test_step_client.TestStepClient.output_md")
    test_steps = test_step_client.TestStepClient([TEST_DIR])
    test_steps.parse_file(TEST_FILE)
    mocker_object_one.assert_called_once()
    mocker_object_two.assert_called_once()

    loginfo_calls = [
        call("Parsing files for test steps and definitions"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    logdebug_calls = [
        call(f"Create JSON and MD files for {TEST_FILE[0]} using {TEST_STEP}"),
    ]
    logdebug.assert_has_calls(logdebug_calls, any_order=False)


def test_parse_file_no_steps(loginfo, logdebug, mocker):
    "Unit Test for TestStepClient object module walk_dir."

    # Set datetime to a known value
    mocker.patch(
        "vane.test_step_client.TestStepClient.now",
        return_value="01/01/2023 00:00:00",
    )
    mocker_object_one = mocker.patch("vane.test_step_client.TestStepClient.output_json")
    mocker_object_two = mocker.patch("vane.test_step_client.TestStepClient.output_md")

    test_steps = test_step_client.TestStepClient([TEST_DIR])
    test_steps.parse_file(["sample_network_tests/host/test_definition.yaml"])
    mocker_object_one.assert_called_once()
    mocker_object_two.assert_called_once()

    loginfo_calls = [
        call("Parsing files for test steps and definitions"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    logdebug_calls = [
        call(
            "Create JSON and MD files for sample_network_tests/host/test_definition.yaml"
            f" using {NO_TEST_STEPS}"
        ),
    ]
    logdebug.assert_has_calls(logdebug_calls, any_order=False)


def test_output_json():
    "Unit Test for TestStepClient object module output_json"

    with open("tests/unittests/fixtures/test_host.json", encoding="utf_8") as f_name:
        expected_output = f_name.read()

    test_steps = test_step_client.TestStepClient([TEST_DIR])
    test_steps.output_json({TEST_FILE[0]: TEST_STEP})

    with open("sample_network_tests/host/test_host.json", encoding="utf_8") as j_file:
        actual_output = j_file.read()

    assert expected_output == actual_output


def test_output_md():
    "Unit Test for TestStepClient object module output_md"

    with open("tests/unittests/fixtures/test_host.md", encoding="utf_8") as f_name:
        expected_output = f_name.read()

    test_steps = test_step_client.TestStepClient([TEST_DIR])
    test_steps.output_md({TEST_FILE[0]: TEST_STEP})

    with open("sample_network_tests/host/test_host.md", encoding="utf_8") as f_name:
        actual_output = f_name.read()

    assert expected_output == actual_output


def test_output_md_no_steps():
    "Unit Test for TestStepClient object module output_md"

    with open("tests/unittests/fixtures/test_host_no_steps.md", encoding="utf_8") as f_name:
        expected_output = f_name.read()

    test_steps = test_step_client.TestStepClient([TEST_DIR])
    test_steps.output_md({TEST_FILE[0]: NO_TEST_STEPS})

    with open("sample_network_tests/host/test_host.md", encoding="utf_8") as f_name:
        actual_output = f_name.read()

    assert expected_output == actual_output


def test_output_md_multiple_tests():
    "Unit Test for TestStepClient object module output_md"

    test_dirs = ["sample_network_tests/api"]
    test_files = "sample_network_tests/api/api.py"
    test_step = [
        "01/01/2023 00:00:00",
        "TD: Verify management api https server is running",
        "TS: Collecting the output of 'show management api http-commands' command from DUT",
        "TS: Check HTTPS Server running status",
        "TS: Creating test report based on results",
        "TD: Verify https server is enabled on port 443",
        "TS: Collecting the output of 'show management api http-commands' command from DUT",
        "TS: Check HTTPS Server port",
        "TS: Creating test report based on results",
        "TD: Verify management api https server is enabled",
        "TS: Collecting the output of 'show management api http-commands' command from DUT",
        "TS: Check HTTPS Server is enabled",
        "TS: Creating test report based on results",
        "TD: Verify management api http server is not running",
        "TS: Collecting the output of 'show management api http-commands' command from DUT",
        "TS: Check HTTP Server running status",
        "TS: Creating test report based on results",
        "TD: Verify management api local httpserver is not running",
        "TS: Collecting the output of 'show management api http-commands' command from DUT",
        "TS: Check Local HTTP Server running status",
        "TS: Creating test report based on results",
    ]

    with open("tests/unittests/fixtures/test_api.md", encoding="utf_8") as f_name:
        expected_output = f_name.read()

    test_steps = test_step_client.TestStepClient(test_dirs)
    test_steps.output_md({test_files: test_step})

    with open("sample_network_tests/api/api.md", encoding="utf_8") as f_name:
        actual_output = f_name.read()

    assert expected_output == actual_output
