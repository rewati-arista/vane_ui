import vane.tests_client
import logging
import pytest
import os
import io
import unittest

from pytest import ExitCode
from unittest.mock import call

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
        assert True == (method in dir(TC))

    # Test for known methods in variables
    for variable in variables:
        assert True == (variable in dir(TC))


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
    assert (
        captured.out == "Unable to regenerate test definition files.\n"
    ), "tests_client.generate_test_definitions() did not handle missing key 'generate_test_definitions'"

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


def test__set_test_parameters_unset(loginfo):
    """Validate _set_test_parameters that unsets parameters in functions"""

    # XXX needs implemented
    pass


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
    unittest.TestCase().assertListEqual(
        list(io.open(filepath)), list(io.open("tests/unittests/fixtures/eapi.conf"))
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
        call("Using tests/fixtures/templates/eapi.conf.j2 Jinja2 template to render "
             "tests/unittests/fixtures/invalid/path/eapi_rendered.conf file with parameters "
             "[{'mgmt_ip': '10.255.74.38', 'name': 'BL1', 'neighbors': [{'neighborDevice': "
             "'leaf1', 'neighborPort': 'Ethernet1', 'port': 'Ethernet1'}, {'neighborDevice': "
             "'leaf2', 'neighborPort': 'Ethernet1', 'port': 'Ethernet2'}], 'password': 'cvp123!', "
             "'transport': 'https', 'username': 'cvpadmin', 'role': 'leaf'}, {'mgmt_ip': "
             "'10.255.22.26', 'name': 'BL2', 'neighbors': [{'neighborDevice': 'leaf1', "
             "'neighborPort': 'Ethernet1', 'port': 'Ethernet1'}, {'neighborDevice': 'leaf2', "
             "'neighborPort': 'Ethernet1', 'port': 'Ethernet2'}], 'password': 'cvp123!', "
             "'transport': 'https', 'username': 'cvpadmin', 'role': 'leaf'}]"),
        call("Rendered tests/unittests/fixtures/invalid/path/eapi_rendered.conf as: "
             "[connection:BL1]\nhost: 10.255.74.38\nusername: cvpadmin\n\npassword: cvp123!\n\n"
             "transport: https\n\n[connection:BL2]\nhost: 10.255.22.26\nusername: cvpadmin\n\n"
             "password: cvp123!\n\ntransport: https\n\n"),
        call("Open tests/unittests/fixtures/invalid/path/eapi_rendered.conf for writing"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    # Validate the following messages are logged in order
    logerr_calls = [
        call(f"ERROR WRITING {filepath}: {err_msg}"),
        call("EXITING TEST RUNNER"),
    ]
    logerr.assert_has_calls(logerr_calls, any_order=False)


# def test_import_definitions():
#     """ Validate that a YAML file can be inputted
#     """
#
#     parameters = ['parameters']
#
#     # Test if imported YAML is a dict
#     assert True == (isinstance(TC.data_model, dict))
#
#     # Test for known keywords in YAML
#     for parmeter in parameters:
#         assert True == (parmeter in TC.data_model)
#
# # def test_setting_test_parameters():
# #     """ Validate that test parametters are settable based on a definition file
# #     """
# #
# #     definitions = {
# #         'verbose': [False, True, False],
# #         'stdout': [False, True, False],
# #         'test_cases': ["All", "evpn", None],
# #         'html_report': [None, "report"],
# #         'excel_report': ["report", None],
# #         'json_report': [None, "report"],
# #         'processes': [3, 2, 1, None],
# #         'setup_show': [False, True, False],
# #         'mark': ['nrfu', 'cpu', 'memory', None]
# #     }
# #
# #     extensions = {
# #         'verbose': '-v',
# #         'stdout': '-s',
# #         'setup_show': '--setup-show',
# #         'test_cases': '-k',
# #         'html_report': 'html',
# #         'json_report': 'json',
# #         'excel_report': 'excel',
# #         'processes': '-n',
# #         'mark': '-m',
# #     }
# #
# #     processes = [3, 2, 1, None]
# #     marks = ['nrfu', 'cpu', 'memory', None]
# #
# #     for definition in definitions:
# #         report_dir = TC.data_model['parameters']['report_dir']
# #
# #         if definition in ['verbose', 'stdout', 'setup_show']:
# #             for definition_value in definitions[definition]:
# #                 TC.data_model['parameters'][definition] = definition_value
# #                 TC._set_test_parameters()
# #
# #                 assert definition_value == (extensions[definition] in TC.test_parameters)
# #
# #         elif definition in ['test_cases']:
# #             for definition_value in definitions[definition]:
# #                 TC.data_model['parameters'][definition] = definition_value
# #                 TC._set_test_parameters()
# #                 extension = extensions[definition]
# #
# #                 if definition_value == 'All' or not definition_value:
# #                     assert False == (extension in TC.test_parameters)
# #                 else:
# #                     assert True == (f'{extension} {definition_value}' in TC.test_parameters)
# #
# #         elif definition in ['html_report', 'json_report', 'excel_report']:
# #             for definition_value in definitions[definition]:
# #                 TC.data_model['parameters'][definition] = definition_value
# #                 TC._set_test_parameters()
# #
# #                 if extensions[definition] == 'excel':
# #                     extension = f'--{extensions[definition]}report'
# #                     suffix = 'xlsx'
# #                 else:
# #                     extension = f'--{extensions[definition]}'
# #                     suffix = extensions[definition]
# #
# #                 if definition_value:
# #                     assert True == (f'{extension}={report_dir}/{definition_value}.{suffix}' in TC.test_parameters)
# #                 else:
# #                     list_output = [x for x in TC.test_parameters if extension in x]
# #                     assert True == (len(list_output) == 0)
# #
# #         elif definition in ['processes', 'mark']:
# #             for definition_value in definitions[definition]:
# #                 TC.data_model['parameters'][definition] = definition_value
# #                 TC._set_test_parameters()
# #                 extension = extensions[definition]
# #
# #                 if definition_value:
# #                     assert True == (f'{extension} {definition_value}' in TC.test_parameters)
# #                 else:
# #                     list_output = [x for x in TC.test_parameters if extension in x]
# #                     assert True == (len(list_output) == 0)
# #
# def test_test_parameters_not_set():
#     """ Validate that test parametters are settable based on a definition file
#     """
#
#     definitions = ['verbose', 'stdout', 'test_cases', 'html_report',
#                    'excel_report', 'json_report', 'processes', 'mark',
#                    'setup_show']
#     duts_file = 'tests/fixtures/duts.yaml'
#
#     tc = tests_client.TestsClient(DEFINITIONS, duts_file)
#
#     for definition in definitions:
#         _ = tc.data_model['parameters'].pop(definition, 1)
#         _ = tc._set_test_parameters()
#         assert tc.data_model['parameters'][definition] is None
#
# def test_import_no_definitions():
#     """ Test script exits if spreadsheet doesn't exist
#     """
#
#     try:
#         definitions = '/project/vane/bin/no_definitions.yaml'
#         _ = tests_client.TestsClient(definitions)
#
#         assert False
#
#     except Exception:
#         assert True
#
# def test_import_bad_definitions():
#     """ Test script exits if spreadsheet doesn't exist
#     """
#
#     bad_data = """ blahs: jalfjdaipeqelue
#     feq;j;ejf;eqwj
#     f;djjad;sjds;iefje2''';
#     asd;jsda;j:::
#     L:aere
#     00---
#     """
#
#     bad_definition = 'tests/unittests/fixtures/bad_definitions.yaml'
#
#     with open(bad_definition, 'w') as out_file:
#         out_file.write(bad_data)
#
#     try:
#         _ = tests_client.TestsClient(bad_definition)
#
#         assert False
#
#     except Exception:
#         if os.path.exists(bad_definition):
#             os.remove(bad_definition)
#
#         assert True
#
#
#
#
# def test_remove_result_files():
#     """ Verify files are removed from results directory
#     """
#
#     tc = tests_client.TestsClient(DEFINITIONS, DUTS)
#     results_dir = tc.data_model['parameters']['results_dir']
#
#     if not os.path.exists(results_dir):
#         os.makedirs(results_dir)
#
#     for x in range(10):
#         file_name = f'{results_dir}/result-file{x}'
#
#         with open(file_name, 'w') as results_file:
#             results_file.write('test 1 2 3...')
#
#     tc = tests_client.TestsClient(DEFINITIONS, DUTS)
#     tc._remove_result_files()
#     results_files = os.listdir(results_dir)
#
#     for name in results_files:
#         if 'result-' in name:
#             assert False
#
#     assert True
