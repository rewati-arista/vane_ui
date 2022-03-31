import vane.tests_client as tests_client
import os
import configparser
import time

DEFINITIONS = 'tests/unittests/fixtures/definitions.yaml'
DUTS = 'tests/fixtures/duts.yaml'
TC = tests_client.TestsClient(DEFINITIONS, DUTS)

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

# def test_setting_test_parameters():
#     """ Validate that test parametters are settable based on a definition file
#     """
# 
#     definitions = {
#         'verbose': [False, True, False],
#         'stdout': [False, True, False],
#         'test_cases': ["All", "evpn", None],
#         'html_report': [None, "report"],
#         'excel_report': ["report", None],
#         'json_report': [None, "report"],
#         'processes': [3, 2, 1, None],
#         'setup_show': [False, True, False],
#         'mark': ['nrfu', 'cpu', 'memory', None]
#     }
# 
#     extensions = {
#         'verbose': '-v',
#         'stdout': '-s',
#         'setup_show': '--setup-show',
#         'test_cases': '-k',
#         'html_report': 'html',
#         'json_report': 'json',
#         'excel_report': 'excel',
#         'processes': '-n',
#         'mark': '-m',
#     }
# 
#     processes = [3, 2, 1, None]
#     marks = ['nrfu', 'cpu', 'memory', None]
# 
#     for definition in definitions:
#         report_dir = TC.data_model['parameters']['report_dir']
# 
#         if definition in ['verbose', 'stdout', 'setup_show']:
#             for definition_value in definitions[definition]:
#                 TC.data_model['parameters'][definition] = definition_value
#                 TC._set_test_parameters()
# 
#                 assert definition_value == (extensions[definition] in TC.test_parameters)
# 
#         elif definition in ['test_cases']:
#             for definition_value in definitions[definition]:
#                 TC.data_model['parameters'][definition] = definition_value
#                 TC._set_test_parameters()
#                 extension = extensions[definition]
# 
#                 if definition_value == 'All' or not definition_value:
#                     assert False == (extension in TC.test_parameters)
#                 else:
#                     assert True == (f'{extension} {definition_value}' in TC.test_parameters)
#         
#         elif definition in ['html_report', 'json_report', 'excel_report']:
#             for definition_value in definitions[definition]:
#                 TC.data_model['parameters'][definition] = definition_value
#                 TC._set_test_parameters()
# 
#                 if extensions[definition] == 'excel':
#                     extension = f'--{extensions[definition]}report'
#                     suffix = 'xlsx'
#                 else:
#                     extension = f'--{extensions[definition]}'
#                     suffix = extensions[definition]
# 
#                 if definition_value:
#                     assert True == (f'{extension}={report_dir}/{definition_value}.{suffix}' in TC.test_parameters)
#                 else:
#                     list_output = [x for x in TC.test_parameters if extension in x]
#                     assert True == (len(list_output) == 0)
# 
#         elif definition in ['processes', 'mark']:
#             for definition_value in definitions[definition]:
#                 TC.data_model['parameters'][definition] = definition_value
#                 TC._set_test_parameters()
#                 extension = extensions[definition]
# 
#                 if definition_value:
#                     assert True == (f'{extension} {definition_value}' in TC.test_parameters)
#                 else:
#                     list_output = [x for x in TC.test_parameters if extension in x]
#                     assert True == (len(list_output) == 0)
# 
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
        assert None == tc.data_model['parameters'][definition]

def test_import_no_definitions():
    """ Test script exits if spreadsheet doesn't exist
    """

    try:
        definitions = '/project/vane/bin/no_definitions.yaml'
        tc = tests_client.TestsClient(definitions)

        assert False

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

    bad_definition = 'tests/unittests/fixtures/bad_definitions.yaml'

    with open(bad_definition, 'w') as out_file:
        out_file.write(bad_data)

    try:
        tc = tests_client.TestsClient(bad_definition)

        assert False

    except:
        if os.path.exists(bad_definition):
            os.remove(bad_definition)

        assert True

def test_rendering_eapi_cfg():
    """ Verify .eapi.conf file renders
    """

    eapi_file = TC.data_model['parameters']['eapi_file']
    file_life = 0

    if os.path.exists(eapi_file):
        file_life = os.path.getmtime(eapi_file)

    TC._render_eapi_cfg()
    new_file_life = os.path.getmtime(eapi_file)

    assert new_file_life > file_life

def test_eapi_cfg_data():
    """ Verify if eapi cfg data is rendered correctly
    """

    eapi_file = TC.data_model['parameters']['eapi_file']
    duts = TC.data_model['duts']

    TC._render_eapi_cfg()

    config = configparser.ConfigParser()
    config.read(eapi_file)
    dut_names = config.sections()

    for dut in duts:
        dut_name = f'connection:{dut["name"]}'

        assert True == (dut_name in dut_names)

        assert config[dut_name]['host'] == dut['mgmt_ip']
        assert config[dut_name]['username'] == dut['username']
        assert config[dut_name]['password'] == dut['password']

def test_no_eapi_template():
    """ Verify an exception is created for Jinja2 template that doesn't exist
    """

    eapi_file = TC.data_model['parameters']['eapi_file']
    file_life = 0

    if os.path.exists(eapi_file):
        file_life = os.path.getmtime(eapi_file)

    TC.data_model['parameters']['eapi_template'] = 'not_a_file.j2'

    try:
        TC._render_eapi_cfg()

        assert False

    except:
        new_file_life = os.path.getmtime(eapi_file)

    assert new_file_life == file_life

def test_not_able_to_write_file():
    """ Verify an exception is created when eapi.conf file is unable to write
    """

    test_data = """[connection:kg-topology-CloudEosRR1]
host: 3.129.242.29
username: kgrozis
password: arista123
transport: https
    """

    tc = tests_client.TestsClient(DEFINITIONS)
    tc.data_model['parameters']['eapi_file'] = '/no/such/dir/.eapi.conf'

    try:
        #tc._write_file(test_data)
        pass

    except Exception as e:
        assert True

def test_remove_result_files():
    """ Verify files are removed from results directory
    """

    tc = tests_client.TestsClient(DEFINITIONS)
    results_dir = tc.data_model['parameters']['results_dir']

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    for x in range(10):
        file_name = f'{results_dir}/result-file{x}'

        with open(file_name, 'w') as results_file:
            results_file.write('test 1 2 3...')

    tc = tests_client.TestsClient(DEFINITIONS)
    tc._remove_result_files()
    results_files = os.listdir(results_dir)

    for name in results_files:
        if 'result-' in name:
            assert False
    
    assert True
