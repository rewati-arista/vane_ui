import vane.bin.report_client as report_client
import os
import time
import datetime


DEFINITIONS = '/project/vane/bin/definitions.yaml'
RC = report_client.ReportClient(DEFINITIONS)

def test_assert():
    assert True


def test_object():
    """ Verify instance of TestsClient Object can be created 
    """

    methods = ['_compile_yaml_data', '_reconcile_results', '_import_yaml', 
               'write_result_doc', '_return_date', '_write_title_page',
               '_write_toc_page', '_write_summary_report', 
               '_write_summary_results', '_write_dut_summary_results', 
               '_write_suite_summary_results', '_compile_test_results',
               '_parse_testcases', '_totals', '_write_tests_case_report',
               '_write_detail_report', '_write_detail_major_section', 
               '_write_detail_minor_section', '_write_detail_dut_section',
               '_add_dut_table_row', '_compile_suite_results',
               '_compile_testcase_results', '_format_ts_name', '_format_tc_name',
               '_format_test_field']
    variables = ['data_model', '_summary_results', '_results_datamodel',
                 '_document', '_major_section', '_test_id']

    # Test for known methods in object
    for method in methods:
        assert True == (method in dir(RC))

    # Test for known methods in variables
    for variable in variables:
        assert True == (variable in dir(RC))

def test_date_creation():
    """ Verify object returns date field correctly formatted
    """

    date_obj = datetime.datetime.now()
    old_format_date = date_obj.strftime("%B %d, %Y %I:%M:%S%p")
    old_file_date = date_obj.strftime("%y%m%d%H%M")

    format_date, file_date = RC._return_date()

    assert old_file_date == file_date
    assert old_file_date < format_date

def test_formating_test_case_name(test_names, report_names):
    """ Verify object can format a test case name correctly
    """

    test_range = len(test_names)

    for test_index in range(test_range):
        test_name = test_names[test_index]
        report_name = report_names[test_index]

        format_name = RC._format_tc_name(test_name)

        assert format_name == report_name
