import vane.bin.tests_client as tests_client
import os

DEFINITIONS = '/project/vane/bin/definitions.yaml'
TC = tests_client.TestsClient(DEFINITIONS)

def test_assert():
    assert True


def test_object():
    """ Verify instance of TestsClient Object can be created 
    """

    methods = ['_import_yaml', '_remove_result_files', '_render_eapi_cfg', '_set_test_parameters', 'test_runner']
    variables = ['data_model']

    # Test for known methods in object
    for method in methods:
        assert True == (method in dir(TC))

    # Test for known methods in variables
    for variable in variables:
        assert True == (variable in dir(TC))


def test_import_definitions():
    """ Validate that a YAML file can be inputted
    """

    parameters = ['parameters', 'duts']

    # Test if imported YAML is a dict
    assert True == (isinstance(TC.data_model, dict))

    # Test for known keywords in YAML
    for parmeter in parameters:
        assert True == (parmeter in TC.data_model)

def test_setting_test_parameters():
    """ Validate that test parametters are settable based on a definition file
    """

    verbosity_levels = [False, True]
    stdout_levels = [True, False]
    testcases = ["All", "evpn", None]
    html_reports = [None, "../reports/report"]

    # Test verbosity level can be changed
    for verbosity_level in verbosity_levels:
        TC.data_model['parameters']['verbose'] = verbosity_level
        test_parameters = TC._set_test_parameters()
        assert verbosity_level == ('-v' in test_parameters)

    # Test stdout level can be changed
    for stdout_level in stdout_levels:
        TC.data_model['parameters']['stdout'] = stdout_level
        test_parameters = TC._set_test_parameters()
        assert stdout_level == ('-s' in test_parameters)
    
    # Test testcase specific entries
    for testcase in testcases:
        TC.data_model['parameters']['test_cases'] = testcase
        test_parameters = TC._set_test_parameters()

        if testcase == 'All':
            assert False == ('-k' in test_parameters)
        else:
            assert True == (f'-k {testcase}' in test_parameters)

    for html_report in html_reports:
        TC.data_model['parameters']['html_report'] = html_report
        test_parameters = TC._set_test_parameters()

        if html_report:
            assert True == (f'--html={html_report}.html' in test_parameters)
        else:
            html_expr = [for x in ]

def test_import_no_definitions():
    """ Test script exits if spreadsheet doesn't exist
    """

    try:
        definitions = '/project/vane/bin/no_definitions.yaml'
        tc = tests_client.TestsClient(definitions)
    except:
        assert True

def test_import_bad_definitions():
    """ Test script exits if spreadsheet doesn't exist
    """

    bad_data = """ blahs: jalfjdaipeqelue
    feq;j;ejf;eqwj
    f;djjad;sjds;iefje2''';
    asd;jsda;j:::
    L:aere
    00---
    """

    bad_definition = '/project/vane/bin/bad_definitions.yaml'

    with open(bad_definition, 'w') as out_file:
        out_file.write(bad_data)

    try:
        tc = tests_client.TestsClient(bad_definition)
    except:
        if os.path.exists(bad_definition):
            os.remove(bad_definition)

        assert True
