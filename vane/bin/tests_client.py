#!/usr/bin/python3.7
#
# Copyright (c) 2020, Arista Networks EOS+
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the Arista nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

""" Uses Test Definition to run NRFU.  Results are recorded in JSON and the
    external interface transmits the results to Kafka Bus.

    When PS runs NRFU tests outside of CAS the following output is created:

    - HTML report: HTML based report to visualize results

    - Log file: NRFU logs the plain-text show command output used for each
                test.

    - Excel report: Tabular representation of results. """

# from pprint import pprint
import pathlib
import json
import re
import pytest
import yaml
import logging
import sys

class TestsReporting:

    def __init__(self, test_value):
        self.test_value = test_value
    
    def print_value(self):
        print(f'\n\n\n\ >>>>> {self.test_value}\n\n\n')

class TestsClient:
    """ Creates an instance of the rendering engine.
    """

    def __init__(self, test_definition):
        """ Initializes the rendering engine

            Args:
                test_definition (str): YAML representation of NRFU tests

        """

        logging.info('Convert yaml data-model to a python data structure')
        self.data_model = self._import_yaml(test_definition)
        logging.info('Internal test data-model initialized with value: '
                     f'{self.data_model}')

    def _import_yaml(self, yaml_file):
        """ Import YAML file as python data structure

            Args:
                yaml_file (str): Name of YAML file
        """

        logging.info(f'Opening {yaml_file} for read')
        try:
            with open(yaml_file, 'r') as input_yaml:
                try:
                    yaml_data = yaml.safe_load(input_yaml)
                    logging.info(f'Inputed the following yaml: '
                                 f'{yaml_data}')
                    return yaml_data
                except yaml.YAMLError as e:
                    logging.error(f'Error in YAML file. {e}')
                    sys.exit(1)
        except OSError as e:
            logging.error(f'Defintions file: {yaml_file} not '
                          f'found. {e}')
            sys.exit(1)

    def test_runner(self):
        """ Run tests
        """


        test_paramters = self._set_test_parameters()

        logging.info(f'Starting Test')
        nrfu_results = pytest.main(test_paramters)
        #print("\n\n\n >>>>>", nrfu_results)

        #test_results = self._compile_test_results(nrfu_results)
        #return test_results, error_entry

    def _set_test_parameters(self):
        """ Use data-model to create test parameters
        """

        logging.info('Setting test parameters')
        test_parameters = ['-v', '-s']
        test_cases = self.data_model['parameters']['test_cases']
        test_suites = self.data_model['parameters']['test_suites']
        report_dir = self.data_model['parameters']['report_dir']
        html_report = self.data_model['parameters']['html_report']
        excel_report = self.data_model['parameters']['excel_report']
        json_report = self.data_model['parameters']['json_report']
        processes = self.data_model['parameters']['processes']

        logging.info(f'Run the following tests: {test_cases}')
        if test_cases == 'All':
            pass
        else:
            test_parameters.append(f'-k {test_cases}')

        if html_report:
            html_report = f'{report_dir}/{html_report}'
            logging.info(f'Set HTML report name to: {html_report}')
            test_parameters.append(f'--html={html_report}.html')
        else:
            logging.warning(f'HTML report will NOT be created')

        if excel_report:
            excel_report = f'{report_dir}/{excel_report}'
            logging.info(f'Set excel report name to: {excel_report}')
            test_parameters.append(f'--excelreport={excel_report}.xlsx')
        else:
            logging.warning(f'Excel report will NOT be created')

        if json_report:
            json_report = f'{report_dir}/{json_report}'
            logging.info(f'Set json report name to: {json_report}')
            test_parameters.append(f'--json={json_report}.json')
        else:
            logging.warning(f'JSON report will NOT be created')

        if processes:
            logging.info(f'Set number of PyTest process to: {processes}')
            test_parameters.append(f'-n {processes}')
        else:
            logging.warning(f'Using single PyTest processes')

        test_obj = TestsReporting('hello world')
        #test_obj.print_value()
        object_id = id(test_obj)
        #print('>>>>>>', object_id)
        #print(dir(test_obj))

        # pytest.main(["-qq"], plugins=[MyPlugin()])
        # https://docs.pytest.org/en/3.0.4/usage.html
        test_parameters.append(f'--definitions={object_id}')
        #test_parameters.append('test_obj')

        if test_suites:
            logging.info(f'Run the following tests suites: {test_cases}')
            test_parameters.append(f'{test_suites}')
        else:
            logging.info('Run all tests suites')
 
        logging.info(f'Setting the following PyTest parmaters: {test_parameters}')
        return test_parameters

    def evaluate_nrfu_reports(self,
                              report_name,
                              report_dir,
                              file_extension,
                              error_sub_code):
        """ Evaluate output and verify correctness

            Args:
                report_name (str):    NRFU report name
                report_dir (str):     NRFU report directory
                file_extension (str): NRFU file extension
                error_sub_code (str): Error sub code
        """

        nrfu_report = f'{report_dir}{report_name}.{file_extension}'
        file_object = pathlib.Path(nrfu_report)
        error_entry = {}

        if not file_object.exists():
            error_entry = {"error_field": nrfu_report,
                           "worksheet": None,
                           "row_index": None,
                           "error_condition": "043",
                           "error_sub_code": error_sub_code}

        return error_entry

    def _compile_test_results(self, nrfu_results):
        """ Parse NRFU results and compile:

            test_results: <Pass/Fail>
            Pass: <number passed>
            Fail: <number failed>
            Duts:
              - test_results: <Pass/Fail>
                Pass: <number passed>
                FAil: <number failed>
        """

        json_report = f"../nrfu_logs/{definitions.JSON_REPORT_NAME}.json"
        test_results = {}
        test_results["overallResults"] = nrfu_results

        # Open JSON report
        with open(json_report, 'r') as json_file:
            test_data = json.load(json_file)
            test_results["summaryResults"] = test_data["report"]["summary"]
            test_results["duts"] = \
                self._parse_testcases(test_data["report"]["tests"])
        
        kafka_payload = {"messageType": "003", "messageSubType": "001", "payload": test_results}

        return kafka_payload

    def _parse_testcases(self, testcases):
        """ Parse Test cases and return compilation per DUT
        """
        testcases_results = []
        dut_list = []

        for testcase in testcases:
            if re.search('\[.*\]', testcase["name"]):
                dut_name = re.findall('\[.*\]', testcase["name"])[0][1:-1]
                test_result = testcase["outcome"]

                if dut_name not in dut_list:
                    dut_list.append(dut_name)
                    testcases_results.append({})
                    testcases_results[-1]["PASS"] = 0
                    testcases_results[-1]["FAIL"] = 0

                dut_index = dut_list.index(dut_name)
                testcases_results[dut_index]["name"] = dut_name

                if test_result == "passed":
                    testcases_results[dut_index]["PASS"] += 1
                elif test_result == "failed":
                    testcases_results[dut_index]["FAIL"] += 1

        return testcases_results
