import vane.bin.tests_client as tests_client

def test_assert():
    assert True

def test_object_creation():
    """ Verify spreadsheet can be inputted
    """

    tc = tests_client.TestsClient('/project/vane/bin/definitions.yaml')