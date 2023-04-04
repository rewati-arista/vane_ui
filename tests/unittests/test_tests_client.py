"""
tests_client.py unit tests
"""

# pylint: disable=redefined-outer-name, protected-access

import os
import unittest

from unittest.mock import call

import pytest
import vane.tests_client

# LOGGER = logging.getLogger("vane_logs")

DEFINITIONS = "tests/unittests/fixtures/definitions.yaml"
DUTS = "tests/fixtures/duts.yaml"
TC = vane.tests_client.TestsClient(DEFINITIONS, DUTS)


@pytest.fixture
def loginfo(mocker):
    """Fixture to mock logger calls from vane.tests_client"""
    return mocker.patch("vane.tests_client.logging.info")


@pytest.fixture
def logerr(mocker):
    """Fixture to mock logger calls from vane.tests_client"""
    return mocker.patch("vane.tests_client.logging.error")


def test_object():
    """Verify instance of TestsClient Object can be created"""

    methods = [
        "_get_markers",
        "_init_parameters",
        "_remove_result_files",
        "_remove_test_results_dir",
        "_render_eapi_cfg",
        "_set_cmdline_input",
        "_set_cmdline_no_input",
        "_set_cmdline_report",
        "_set_excel_report",
        "_set_html_report",
        "_set_json_report",
        "_set_junit",
        "_set_mark",
        "_set_processes",
        "_set_setup_show",
        "_set_stdout",
        "_set_test_cases",
        "_set_test_dirs",
        "_set_test_parameters",
        "_set_verbosity",
        "_write_file",
        "generate_test_definitions",
        "setup_test_runner",
        "test_runner",
        "write_test_def_file",
    ]
    variables = ["data_model", "duts_model"]

    # Test for known methods in object
    for method in methods:
        assert method in dir(TC)

    # Test for known methods in variables
    for variable in variables:
        assert variable in dir(TC)


def test_generate_test_definitions(loginfo):
    """Validate creating test definitions using master definitions"""

    # Load a definitions file with generate_test_definitions set to false
    definitions_file = "tests/unittests/fixtures/definitions.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Generate test definitions
    client.generate_test_definitions()

    # Verify logging message was called
    loginfo.assert_called_with("Attempting to regenerate test definition files")


def test_generate_test_definitions_regen(loginfo, mocker):
    """Validate creating test definitions with generate_test_definitions set to true"""

    # Mocke the file open function so we don't actually change anything
    mocker.patch("vane.tests_client.open")

    # Load a definitions file with generate_test_definitions set to true
    definitions_file = "tests/unittests/fixtures/definitions-generate.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Generate test definitions
    client.generate_test_definitions()

    # Verify logging message was called (implying files were regenerated)
    loginfo.assert_called_with("Regenerated test definition files")


def test_generate_test_definitions_neg(capsys):
    """Validate key errors are handled by generate_test_definitions"""

    # Multiple key errors are tested in a single test case here because they
    # are dependent sequentially. If one fails, all the following tests cannot
    # proceed, etc. Rather than having an early test fail and trigger cascading
    # failures that we need to trace back to a single point, we keep them
    # together so we can resolve all the key error problems together.

    # Load a definitions file with no generate_test_definitions key
    definitions_file = "tests/unittests/fixtures/definitions-no-generate-key.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Generate test definitions
    client.generate_test_definitions()

    captured = capsys.readouterr()
    assert captured.out == "Unable to regenerate test definition files.\n", (
        "tests_client.generate_test_definitions() did not handle missing key "
        "'generate_test_definitions'"
    )

    # -----------------------------------------------------------------

    # Load a definitions file with no master_definitions key
    definitions_file = "tests/unittests/fixtures/definitions-no-master-def-key.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Generate test definitions
    client.generate_test_definitions()

    captured = capsys.readouterr()
    assert (
        captured.out == "Unable to regenerate test definition files.\n"
    ), "tests_client.generate_test_definitions() did not handle missing key 'master_definitions'"

    # -----------------------------------------------------------------

    # Load a definitions file with no template_definitions key
    definitions_file = "tests/unittests/fixtures/definitions-no-template-def-key.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Generate test definitions
    client.generate_test_definitions()

    captured = capsys.readouterr()
    assert (
        captured.out == "Unable to regenerate test definition files.\n"
    ), "tests_client.generate_test_definitions() did not handle missing key 'template_definitions'"

    # -----------------------------------------------------------------

    # Load a definitions file with no test_definitions key
    definitions_file = "tests/unittests/fixtures/definitions-no-test-def-key.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Generate test definitions
    client.generate_test_definitions()

    captured = capsys.readouterr()
    assert (
        captured.out == "Unable to regenerate test definition files.\n"
    ), "tests_client.generate_test_definitions() did not handle missing key 'test_definitions'"

    # -----------------------------------------------------------------

    # Load a definitions file with no test_dirs key
    definitions_file = "tests/unittests/fixtures/definitions-no-test-dirs-key.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Generate test definitions
    client.generate_test_definitions()

    captured = capsys.readouterr()
    assert (
        captured.out == "Unable to regenerate test definition files.\n"
    ), "tests_client.generate_test_definitions() did not handle missing key 'test_dirs'"


def test_test_runner(mocker, capsys, loginfo):
    """Validate test_runner function without generating test definitions"""

    # Load a definitions file with generate_test_definitions set to false
    definitions_file = "tests/unittests/fixtures/definitions.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Mock a NO_TESTS_COLLECTED result
    mocker.patch("vane.tests_client.pytest.main", return_value=None)

    # Run the tests
    client.test_runner()

    captured = capsys.readouterr()
    assert (
        captured.out == "Starting test with command: pytest \n\n"
    ), "tests_client.test_runner failed when expected to pass"

    # Verify logging message was called
    loginfo.assert_called_with("Starting Test with parameters: []")


def test_test_runner_no_tests(mocker, capsys):
    """Validate test_runner with no tests collected error returned"""

    # Load a definitions file with generate_test_definitions set to false
    definitions_file = "tests/unittests/fixtures/definitions.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Mock a NO_TESTS_COLLECTED result
    mocker.patch("vane.tests_client.pytest.main", return_value=pytest.ExitCode.NO_TESTS_COLLECTED)

    # Catch the system exit during the pytest
    with pytest.raises(SystemExit) as pytest_exit:
        # Run the tests
        client.test_runner()

    captured = capsys.readouterr()
    assert (
        "No tests collected with pytest command" in captured.out
    ), "tests_client.test_runner did not fail when no tests were collected"

    # Validate the system exit was called
    assert pytest_exit.type == SystemExit
    assert pytest_exit.value.code == 1


def test_test_runner_usage_err(mocker, capsys):
    """Validate test_runner with usage error returned"""

    # Load a definitions file with generate_test_definitions set to false
    definitions_file = "tests/unittests/fixtures/definitions.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Mock a USAGE_ERROR result
    mocker.patch("vane.tests_client.pytest.main", return_value=pytest.ExitCode.USAGE_ERROR)

    # Catch the system exit during the pytest
    with pytest.raises(SystemExit) as pytest_exit:
        # Run the tests
        client.test_runner()

    captured = capsys.readouterr()
    assert (
        "Pytest usage error with parameters" in captured.out
    ), "tests_client.test_runner did not fail when usage error detected"

    # Validate the system exit was called
    assert pytest_exit.type == SystemExit
    assert pytest_exit.value.code == 1


def test__set_test_parameters(loginfo):
    """Validate _set_test_parameters with various values"""

    # pylint: disable-next=fixme
    # XXX several options all output "enable pytest output true/false" instead of
    # something descriptive of what is being set. A future issue will correct this,
    # requiring changes to the test case here to match the updated output strings.

    # Load a definitions file built for _set_test_parameters
    definitions_file = "tests/unittests/fixtures/defs_set_test_params.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Run _set_test_parameters
    client._set_test_parameters()

    # Validate the following messages are logged in order
    loginfo_calls = [
        call("Use data-model to create test parameters"),
        call("Setting test parameters"),
        call("Initialize test parameter values"),
        call("Enable pytest output True"),
        call("Enable pytest output True"),
        call("Enable pytest output True"),
        call("Run the following tests: All"),
        call("Running All test cases."),
        call("Set HTML report name to: --html=tests/unittests/fixtures/reports/report.html"),
        call("Set --json report name to: --json=tests/unittests/fixtures/reports/report.json"),
        call("Not Setting PyTest -n"),
        call("Set PyTest -m to: demo"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)


def test__set_test_parameters_unset():
    """Validate _set_test_parameters that unsets parameters in functions"""

    # pylint: disable-next=fixme
    # XXX needs implemented
    assert False


def test__render_eapi_cfg(loginfo):
    """Validate _render_eapi_config"""

    # Load a definitions file built for _render_eapi_cfg
    # This definition file has an eapi file that is named eapi_rendered.conf
    definitions_file = "tests/unittests/fixtures/defs_render_eapi_cfg.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Make sure the rendered eapi file does not exist
    filepath = client.data_model["parameters"]["eapi_file"]
    if os.path.exists(filepath):
        os.remove(filepath)

    # Run _render_eapi_cfg
    client._render_eapi_cfg()

    # Assert the expected file was created
    print(client.data_model["parameters"]["eapi_file"])
    assert os.path.exists(filepath)

    # Assert the new eapi file contains the expected data (compare with known eapi file)
    # pylint: disable=consider-using-with
    unittest.TestCase().assertListEqual(
        list(open(filepath, mode="r", encoding="utf-8")),
        list(open("tests/unittests/fixtures/eapi.conf", mode="r", encoding="utf-8")),
    )

    # Validate the following messages are logged in order
    loginfo_calls = [
        call("Render .eapi.conf file for device access"),
        call("Open tests/fixtures/templates/eapi.conf.j2 Jinja2 template for reading"),
        call("Read and save contents of tests/fixtures/templates/eapi.conf.j2 Jinja2 template"),
        call(
            "Using tests/fixtures/templates/eapi.conf.j2 Jinja2 template to render "
            "tests/unittests/fixtures/eapi_rendered.conf file with parameters "
            "[{'mgmt_ip': '10.255.74.38', 'name': 'BL1', 'neighbors': [{'neighborDevice': "
            "'leaf1', 'neighborPort': 'Ethernet1', 'port': 'Ethernet1'}, {'neighborDevice': "
            "'leaf2', 'neighborPort': 'Ethernet1', 'port': 'Ethernet2'}], 'password': 'cvp123!', "
            "'transport': 'https', 'username': 'cvpadmin', 'role': 'leaf'}, {'mgmt_ip': "
            "'10.255.22.26', 'name': 'BL2', 'neighbors': [{'neighborDevice': 'leaf1', "
            "'neighborPort': 'Ethernet1', 'port': 'Ethernet1'}, {'neighborDevice': 'leaf2', "
            "'neighborPort': 'Ethernet1', 'port': 'Ethernet2'}], 'password': 'cvp123!', "
            "'transport': 'https', 'username': 'cvpadmin', 'role': 'leaf'}]"
        ),
        call(
            "Rendered tests/unittests/fixtures/eapi_rendered.conf as: [connection:BL1]\n"
            "host: 10.255.74.38\nusername: cvpadmin\n\npassword: cvp123!\n\ntransport: "
            "https\n\n[connection:BL2]\nhost: 10.255.22.26\nusername: cvpadmin\n\n"
            "password: cvp123!\n\ntransport: https\n\n"
        ),
        call("Open tests/unittests/fixtures/eapi_rendered.conf for writing"),
        call("Change permissions of tests/unittests/fixtures/eapi_rendered.conf to 777"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)


def test__render_eapi_cfg_neg(loginfo, logerr, capsys):
    """Validate failure when eapi_template does not exist"""

    # Load a definitions file built for _render_eapi_cfg
    # This definition file has an eapi file that is named eapi_rendered.conf
    definitions_file = "tests/unittests/fixtures/defs_render_eapi_cfg_no_template.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    template = client.data_model["parameters"]["eapi_template"]

    # Catch the system exit during the pytest
    with pytest.raises(SystemExit) as pytest_exit:
        # Run _render_eapi_cfg
        client._render_eapi_cfg()

    captured = capsys.readouterr()
    err_msg = f"[Errno 2] No such file or directory: '{template}'"
    assert (
        f">>> ERROR READING {template}: {err_msg}" in captured.out
    ), "tests_client._render_eapi_cfg did not fail when template file could not be read"

    # Validate the system exit was called
    assert pytest_exit.type == SystemExit
    assert pytest_exit.value.code == 1

    # Validate the following messages are logged in order
    loginfo_calls = [
        call("Render .eapi.conf file for device access"),
        call("Open tests/fixtures/templates/eapi.missing.conf.j2 Jinja2 template for reading"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    # Validate the following messages are logged in order
    logerr_calls = [
        call(f"ERROR READING {template}: {err_msg}"),
        call("EXITING TEST RUNNER"),
    ]
    logerr.assert_has_calls(logerr_calls, any_order=False)


def test__write_file_neg(loginfo, logerr, capsys):
    """Validate failure when eapi_file path is not writable"""

    # Load a definitions file built for _render_eapi_cfg
    # This definition file has an eapi file that with a path that does not exist
    definitions_file = "tests/unittests/fixtures/defs_render_eapi_cfg_bad_path.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    filepath = client.data_model["parameters"]["eapi_file"]

    # Catch the system exit during the pytest
    with pytest.raises(SystemExit) as pytest_exit:
        # Run _render_eapi_cfg
        client._render_eapi_cfg()

    captured = capsys.readouterr()
    err_msg = f"[Errno 2] No such file or directory: '{filepath}'"
    assert (
        f">>> ERROR WRITING {filepath}: {err_msg}" in captured.out
    ), "tests_client._write_file did not fail when eapi file path could not be opened"

    # Validate the system exit was called
    assert pytest_exit.type == SystemExit
    assert pytest_exit.value.code == 1

    # Validate the following messages are logged in order
    loginfo_calls = [
        call("Render .eapi.conf file for device access"),
        call("Open tests/fixtures/templates/eapi.conf.j2 Jinja2 template for reading"),
        call("Read and save contents of tests/fixtures/templates/eapi.conf.j2 Jinja2 template"),
        call(
            "Using tests/fixtures/templates/eapi.conf.j2 Jinja2 template to render "
            "tests/unittests/fixtures/invalid/path/eapi_rendered.conf file with parameters "
            "[{'mgmt_ip': '10.255.74.38', 'name': 'BL1', 'neighbors': [{'neighborDevice': "
            "'leaf1', 'neighborPort': 'Ethernet1', 'port': 'Ethernet1'}, {'neighborDevice': "
            "'leaf2', 'neighborPort': 'Ethernet1', 'port': 'Ethernet2'}], 'password': 'cvp123!', "
            "'transport': 'https', 'username': 'cvpadmin', 'role': 'leaf'}, {'mgmt_ip': "
            "'10.255.22.26', 'name': 'BL2', 'neighbors': [{'neighborDevice': 'leaf1', "
            "'neighborPort': 'Ethernet1', 'port': 'Ethernet1'}, {'neighborDevice': 'leaf2', "
            "'neighborPort': 'Ethernet1', 'port': 'Ethernet2'}], 'password': 'cvp123!', "
            "'transport': 'https', 'username': 'cvpadmin', 'role': 'leaf'}]"
        ),
        call(
            "Rendered tests/unittests/fixtures/invalid/path/eapi_rendered.conf as: "
            "[connection:BL1]\nhost: 10.255.74.38\nusername: cvpadmin\n\npassword: cvp123!\n\n"
            "transport: https\n\n[connection:BL2]\nhost: 10.255.22.26\nusername: cvpadmin\n\n"
            "password: cvp123!\n\ntransport: https\n\n"
        ),
        call("Open tests/unittests/fixtures/invalid/path/eapi_rendered.conf for writing"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    # Validate the following messages are logged in order
    logerr_calls = [
        call(f"ERROR WRITING {filepath}: {err_msg}"),
        call("EXITING TEST RUNNER"),
    ]
    logerr.assert_has_calls(logerr_calls, any_order=False)


def test__remove_result_files():
    """Validate _remove_result_files removes pre-existing results files"""

    # pylint: disable-next=fixme
    # XXX needs implemented
    assert False


def test_remove_test_results_dir():
    """Validate _tremove_test_results_dir removes the TEST RESULTS directory"""

    # pylint: disable-next=fixme
    # XXX needs implemented
    assert False
