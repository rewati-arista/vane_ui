import vane.tests_client as tests_client

DEFINITIONS = 'tests/unittests/fixtures/definitions.yaml'
DUTS = 'tests/fixtures/duts.yaml'
def test_assert():
    assert True

def test_object_creation():
    """ Verify spreadsheet can be inputted
    """

    tc = tests_client.TestsClient(DEFINITIONS, DUTS)
