import vane.tests_client
import logging
import pytest

from pytest import ExitCode
from unittest.mock import call

# LOGGER = logging.getLogger("vane_logs")

DEFINITIONS = "tests/unittests/fixtures/definitions.yaml"
DUTS = "tests/fixtures/duts.yaml"
TC = vane.tests_client.TestsClient(DEFINITIONS, DUTS)


@pytest.fixture
def logger(mocker):
    return mocker.patch("vane.tests_client.logging.info")


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


def test_generate_test_definitions(logger):
    """Validate creating test definitions using master definitions"""

    # Load a definitions file with generate_test_definitions set to false
    definitions_file = "tests/unittests/fixtures/definitions.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Generate test definitions
    client.generate_test_definitions()

    # Verify logging message was called
    logger.assert_called_with("Attempting to regenerate test definition files")


def test_generate_test_definitions_regen(logger, mocker):
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
    logger.assert_called_with("Regenerated test definition files")


def test_generate_test_definitions_neg(capsys):
    """Validate key errors are handled by generate_test_definitions"""

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


def test_test_runner(mocker, capsys, logger):

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
    logger.assert_called_with("Starting Test with parameters: []")


def test_test_runner_no_tests(mocker, capsys):

    # Load a definitions file with generate_test_definitions set to false
    definitions_file = "tests/unittests/fixtures/definitions.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Mock a NO_TESTS_COLLECTED result
    mocker.patch("vane.tests_client.pytest.main", return_value=pytest.ExitCode.NO_TESTS_COLLECTED)

    # Mock sys.exit for this run
    ntc_exit = mocker.patch("vane.tests_client.sys.exit")

    # Run the tests
    client.test_runner()

    captured = capsys.readouterr()
    assert (
        "No tests collected with pytest command" in captured.out
    ), "tests_client.test_runner did not fail when no tests were collected"

    # Assert sys.exit called one time with 1
    ntc_exit.assert_called_once_with(1)


def test_test_runner_usage_err(mocker, capsys):

    # Load a definitions file with generate_test_definitions set to false
    definitions_file = "tests/unittests/fixtures/definitions.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Mock a USAGE_ERROR result
    mocker.patch("vane.tests_client.pytest.main", return_value=pytest.ExitCode.USAGE_ERROR)

    # Mock sys.exit for this run
    ue_exit = mocker.patch("vane.tests_client.sys.exit")

    # Run the tests
    client.test_runner()

    captured = capsys.readouterr()
    assert (
        "Pytest usage error with parameters" in captured.out
    ), "tests_client.test_runner did not fail when usage error detected"

    # Assert sys.exit called one time with 1
    ue_exit.assert_called_once_with(1)


def test__set_test_parameters(logger):

    # Load a definitions file built for _set_test_parameters
    definitions_file = "tests/unittests/fixtures/defs_set_test_params.yaml"
    duts_file = "tests/fixtures/duts.yaml"
    client = vane.tests_client.TestsClient(definitions_file, duts_file)

    # Run _set_test_parameters
    client._set_test_parameters()

    # XXX
    print(logger.call_args_list)

    # Validate the following messages are logged in order
    logger_calls = [
        call("Use data-model to create test parameters"),
        call("Setting test parameters"),
        call("Initialize test parameter values"),
        call("Enable pytest output True"),
        call("Enable pytest output True"),
        call("Enable pytest output True"),
        call("Run the following tests: All"),
        call("Running All test cases."),
        call('Set HTML report name to: --html=tests/unittests/fixtures/reports/report.html'),
        call('Set --json report name to: --json=tests/unittests/fixtures/reports/report.json'),
        call('Not Setting PyTest -n'),
        call('Set PyTest -m to: demo'),
    ]
    logger.assert_has_calls(logger_calls, any_order=True)



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
# def test_rendering_eapi_cfg():
#     """ Verify .eapi.conf file renders
#     """
#
#     eapi_file = TC.data_model['parameters']['eapi_file']
#     file_life = 0
#
#     if os.path.exists(eapi_file):
#         file_life = os.path.getmtime(eapi_file)
#
#     TC._render_eapi_cfg()
#     new_file_life = os.path.getmtime(eapi_file)
#
#     assert new_file_life > file_life
#
# def test_eapi_cfg_data():
#     """ Verify if eapi cfg data is rendered correctly
#     """
#
#     eapi_file = TC.data_model['parameters']['eapi_file']
#     duts = TC.duts_model['duts']
#
#     TC._render_eapi_cfg()
#
#     config = configparser.ConfigParser()
#     config.read(eapi_file)
#     dut_names = config.sections()
#
#     for dut in duts:
#         dut_name = f'connection:{dut["name"]}'
#
#         assert True == (dut_name in dut_names)
#
#         assert config[dut_name]['host'] == dut['mgmt_ip']
#         assert config[dut_name]['username'] == dut['username']
#         assert config[dut_name]['password'] == dut['password']
#
# def test_no_eapi_template():
#     """ Verify an exception is created for Jinja2 template that doesn't exist
#     """
#
#     eapi_file = TC.data_model['parameters']['eapi_file']
#     file_life = 0
#
#     if os.path.exists(eapi_file):
#         file_life = os.path.getmtime(eapi_file)
#
#     TC.data_model['parameters']['eapi_template'] = 'not_a_file.j2'
#
#     try:
#         TC._render_eapi_cfg()
#
#         assert False
#
#     except: # noqa: E722
#         new_file_life = os.path.getmtime(eapi_file)
#
#     assert new_file_life == file_life
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
