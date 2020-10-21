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
import stat
import os
import sys
import logging
import pytest
import yaml
import jinja2


logging.basicConfig(level=logging.INFO, filename='vane.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class TestsClient:
    """ Creates an instance of the Test Client.
    """

    def __init__(self, test_definition):
        """ Initializes the Test Client

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
                except yaml.YAMLError as err_data:
                    logging.error(f'Error in YAML file. {err_data}')
                    sys.exit(1)
        except OSError as err_data:
            logging.error(f'Defintions file: {yaml_file} not '
                          f'found. {err_data}')
            sys.exit(1)

    def test_runner(self):
        """ Run tests
        """

        logging.info('Start test setup')
        self._render_eapi_cfg()
        self._remove_result_files()
        test_paramters = self._set_test_parameters()

        logging.info('Starting Test')
        pytest.main(test_paramters)

    def _set_test_parameters(self):
        """ Use data-model to create test parameters
        """

        logging.info('Use data-model to create test parameters')

        logging.info('Setting test parameters')
        test_parameters = []
        test_cases = self.data_model['parameters']['test_cases']
        test_suites = self.data_model['parameters']['test_suites']
        report_dir = self.data_model['parameters']['report_dir']
        html_report = self.data_model['parameters']['html_report']
        excel_report = self.data_model['parameters']['excel_report']
        json_report = self.data_model['parameters']['json_report']
        processes = self.data_model['parameters']['processes']
        setup_show = self.data_model['parameters']['setup_show']
        verbose = self.data_model['parameters']['verbose']
        stdout = self.data_model['parameters']['stdout']
        mark = self.data_model['parameters']['mark']

        test_parameters.append('--junit-xml=../reports/report.xml')

        if verbose:
            logging.info('Enable pytest output verbosity')
            test_parameters.append('-v')
        else:
            logging.warning('Disable pytest output verbosity')

        if stdout:
            logging.info('Enable pytest printf to stdout')
            test_parameters.append('-s')
        else:
            logging.warning('Disable pytest printf to stdout')

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
            logging.warning('HTML report will NOT be created')

        if excel_report:
            excel_report = f'{report_dir}/{excel_report}'
            logging.info(f'Set excel report name to: {excel_report}')
            test_parameters.append(f'--excelreport={excel_report}.xlsx')
        else:
            logging.warning('Excel report will NOT be created')

        if json_report:
            json_report = f'{report_dir}/{json_report}'
            logging.info(f'Set json report name to: {json_report}')
            test_parameters.append(f'--json={json_report}.json')
        else:
            logging.warning('JSON report will NOT be created')

        if processes:
            logging.info(f'Set number of PyTest process to: {processes}')
            test_parameters.append(f'-n {processes}')
        else:
            logging.warning('Using single PyTest processes')

        if setup_show:
            logging.info('Enable debug for setup and teardown')
            test_parameters.append('--setup-show')
        else:
            logging.warning('Disable debug for setup and teardown')

        if mark:
            logging.info(f'Run the test cases with mark: {mark}')
            test_parameters.append(f'-m {mark}')
        else:
            logging.info('Do NOT use marking within test run')

        if test_suites:
            logging.info(f'Run the following tests suites: {test_cases}')
            test_parameters.append(f'{test_suites}')
        else:
            logging.info('Run all tests suites')

        logging.info('Setting the following PyTest parmaters: '
                     f'{test_parameters}')
        return test_parameters

    def _render_eapi_cfg(self):
        """ Render .eapi.conf file so pytests can log into devices
        """

        logging.info('Render .eapi.conf file for device access')
        eapi_template = self.data_model["parameters"]["eapi_template"]
        eapi_file = self.data_model["parameters"]["eapi_file"]
        duts = self.data_model["duts"]

        try:
            logging.info(f'Open {eapi_template} Jinja2 template for reading')
            with open(eapi_template, 'r') as jinja_file:
                logging.info(f'Read and save contents of {eapi_template} '
                             'Jinja2 template')
                jinja_template = jinja_file.read()
                logging.info(f'Using {eapi_template} Jinja2 template to '
                             f'render {eapi_file} file with parameters {duts}')
                resource_file = jinja2.Environment().from_string(jinja_template).render(duts=duts)
        except IOError as err_data:
            print(f">>> ERROR READING {eapi_template}: {err_data}")
            logging.error(f'ERROR READING {eapi_template}: {err_data}')
            logging.error('EXITING TEST RUNNER')
            sys.exit(1)

        logging.info(f'Rendered {eapi_file} as: {resource_file}')
        try:
            logging.info(f'Open {eapi_file} for writing')
            with open(eapi_file, 'w') as output_file:
                output_file.write(resource_file)
        except IOError as err_data:
            print(f">>> ERROR WRITING {eapi_file}: {err_data}")
            logging.error(f'ERROR WRITING {eapi_file}: {err_data}')
            logging.error('EXITING TEST RUNNER')
            sys.exit(1)

        logging.info(f'Change permissions of {eapi_file} to 777')
        os.chmod(eapi_file, stat.S_IRWXU)
    
    def _remove_result_files(self):
        """ Remove pre-existing results file
        """

        results_dir = self.data_model["parameters"]["results_dir"]
        logging.info('Remove any existing results files in results directory '
                     f'{results_dir}')

        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        results_files = os.listdir(results_dir)
        logging.info(f'Result files are {results_files}')

        for name in results_files:
            if 'result-' in name:
                result_file = f'{results_dir}/{name}'
                logging.info(f'Remove result file: {result_file}')
                os.remove(result_file)
            else:
                logging.warning(f'Not removing file: {name}')
