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

    definitions = {
        'verbose': [False, True],
        'stdout': [True, False],
        'test_cases': ["All", "evpn", None],
        'html_report': [None, "report"],
        'excel_report': ["report", None],
        'json_report': [None, "report"],
        'processes': [3, 2, 1, None],
        'setup_show': [False, True],
        'mark': ['nrfu', 'cpu', 'memory', None]
    }

    extensions = {
        'verbose': '-v',
        'stdout': '-s',
        'setup_show': '--setup-show',
        'test_cases': '-k',
        'html_report': 'html',
        'json_report': 'json',
        'excel_report': 'excel',
        'processes': '-n',
        'mark': '-m',
    }

    processes = [3, 2, 1, None]
    marks = ['nrfu', 'cpu', 'memory', None]

    for definition in definitions:
        report_dir = TC.data_model['parameters']['report_dir']

        if definition in ['verbose', 'stdout', 'setup_show']:
            for definition_value in definitions[definition]:
                TC.data_model['parameters'][definition] = definition_value
                test_parameters = TC._set_test_parameters()

                assert definition_value == (extensions[definition] in test_parameters)

        elif definition in ['test_cases']:
            for definition_value in definitions[definition]:
                TC.data_model['parameters'][definition] = definition_value
                test_parameters = TC._set_test_parameters()
                extension = extensions[definition]

                if definition_value == 'All' or not definition_value:
                    assert False == (extension in test_parameters)
                else:
                    assert True == (f'{extension} {definition_value}' in test_parameters)
        
        elif definition in ['html_report', 'json_report', 'excel_report']:
            for definition_value in definitions[definition]:
                TC.data_model['parameters'][definition] = definition_value
                test_parameters = TC._set_test_parameters()

                if extensions[definition] == 'excel':
                    extension = f'--{extensions[definition]}report'
                    suffix = 'xlsx'
                else:
                    extension = f'--{extensions[definition]}'
                    suffix = extensions[definition]

                if definition_value:
                    assert True == (f'{extension}={report_dir}/{definition_value}.{suffix}' in test_parameters)
                else:
                    list_output = [x for x in test_parameters if extension in x]
                    assert True == (len(list_output) == 0)

        elif definition in ['processes', 'mark']:
            for definition_value in definitions[definition]:
                TC.data_model['parameters'][definition] = definition_value
                test_parameters = TC._set_test_parameters()
                extension = extensions[definition]

                if definition_value:
                    assert True == (f'{extension} {definition_value}' in test_parameters)
                else:
                    list_output = [x for x in test_parameters if extension in x]
                    assert True == (len(list_output) == 0)

def test_test_parameters_not_set():
    """ Validate that test parametters are settable based on a definition file
    """

    definitions = ['verbose', 'stdout', 'test_cases', 'html_report', 
                   'excel_report', 'json_report', 'processes', 'mark',
                   'setup_show']
    tc = tests_client.TestsClient(DEFINITIONS)

    for definition in definitions:
        _ = tc.data_model['parameters'].pop(definition, 1)
        test_parameters = tc._set_test_parameters()
        print(f'>>>>>>> {test_parameters}')
        assert None == tc.data_model['parameters'][definition]

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
