import vane.bin.xcel_client as xcel_client

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
