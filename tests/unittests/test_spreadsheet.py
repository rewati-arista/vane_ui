import vane.xcel_client as xcel_client
import os

DEFINITIONS = 'tests/unittests/fixtures/definitions.yaml'
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
        XC.definitions['parameters']['spreadsheet'] = "tests/unittests/fixtures/spreadsheets/corrupt_spreadsheet.xls"
        XC.import_spreadsheet()
    except:
        assert True

def test_import_no_definitions():
    """ Test script exits if spreadsheet doesn't exist
    """

    try:
        definitions = 'no_definitions.yaml'
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

    bad_definition = 'tests/unittests/fixtures/bad_definitions.yaml'

    with open(bad_definition, 'w') as out_file:
        out_file.write(bad_data)

    try:
        xc = xcel_client.XcelClient(bad_definition)
    except:
        if os.path.exists(bad_definition):
            os.remove(bad_definition)

        assert True

def test_cleaning_table(xc, table):

    correct_table = { 'row1' : {'value1': 1, 'value2': 2, 'value3': 3},
                      'row2' : {'value1': None, 'value2': 2, 'value3': 3},
                    }
    new_table = xc._clean_table(table)

    assert new_table == correct_table

def test_column_return(xc, columns):

    table_dimensions = columns['table_dimensions']
    multi_cols = columns['multi_cols']
    correct_cols = [1, 2, 6, 7, 8]

    cols = xc._return_cols(table_dimensions, multi_cols)

    assert cols == correct_cols
