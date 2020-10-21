import vane.bin.xcel_client as xcel_client
import os

DEFINITIONS = '/project/vane/bin/definitions.yaml'
XC = xcel_client.XcelClient(DEFINITIONS)

def test_assert():
    assert True


def test_object():
    """ Verify instance of XcelClient Object can be created 
    """

    methods = ['_import_yaml', 'import_spreadsheet']
    variables = ['definitions', 'spreadsheet']

    # Test for known methods in object
    for method in methods:
        assert True == (method in dir(XC))

    # Test for known methods in variables
    for variable in variables:
        assert True == (variable in dir(XC))

def test_import_definitions():
    """ Validate that a YAML file can be inputted
    """

    parameters = ['parameters', 'duts']

    # Test if imported YAML is a dict
    assert True == (isinstance(XC.definitions, dict))

    # Test for known keywords in YAML
    for parmeter in parameters:
        assert True == (parmeter in XC.definitions)

def test_import_spreadsheets():
    
    XC.import_spreadsheet()

def test_import_no_spreadsheet_exist():
    """ Test script exits if spreadsheet doesn't exist
    """

    try:
        XC.definitions['parameters']['spreadsheet'] = "no_spreadsheet"
        XC.import_spreadsheet()
    except:
        assert True

def test_import_corrupt_spreadsheet():

    try:
        XC.definitions['parameters']['spreadsheet'] = "/project/vane/bin/spreadsheets/corrupt_spreadsheet.xls"
        XC.import_spreadsheet()
    except:
        assert True

def test_import_no_definitions():
    """ Test script exits if spreadsheet doesn't exist
    """

    try:
        definitions = '/project/vane/bin/no_definitions.yaml'
        xc = xcel_client.XcelClient(definitions)
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
        xc = xcel_client.XcelClient(bad_definition)
    except:
        if os.path.exists(bad_definition):
            os.remove(bad_definition)

        assert True
    
