#!/usr/bin/env python3
#
# Copyright (c) 2023, Arista Networks EOS+
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

# pylint: disable=too-few-public-methods

""" Uses Test Definition to run NRFU.  Results are recorded in JSON and the
    external interface transmits the results to Kafka Bus.

    When PS runs NRFU tests outside of CAS the following output is created:

    - HTML report: HTML based report to visualize results

    - Log file: NRFU logs the plain-text show command output used for each
                test.

    - Excel report: Tabular representation of results. """

import os
import stat
import sys
import shutil

import configparser
import jinja2
import pytest
import yaml

from jinja2 import Template, Undefined
from pytest import ExitCode
from vane.vane_logging import logging
from vane import tests_tools


class NullUndefined(Undefined):
    """NullUndefined Class"""

    def __getattr__(self, key):
        return ""


class TestsClient:
    """Creates an instance of the Test Client."""

    get_pytest_file = "pytest.ini"

    def __init__(self, test_definition, test_duts):
        """Initializes the Test Client

        Args:
            test_definition (str): YAML representation of NRFU tests
        """

        logging.info("Convert yaml data-model to a python data structure")
        self.data_model = tests_tools.import_yaml(test_definition)
        self.duts_model = tests_tools.import_yaml(test_duts)

        logging.info(f"Internal test data-model initialized with value: {self.data_model}")
        self.test_parameters = []

    def write_test_def_file(
        self, template_definitions, master_definitions, test_dir, test_definitions
    ):
        """Reads templates and creates test definitions using master definitions

        Args:
            template_definitions (str): template test definition file name
            master_definitions (dict): master schema to used to render template
            test_dir (str): the directory for which test definitons need to be generated
            test_definitions (str): name of the test defnition file to be created
        """

        # Traverses given test directory
        for root, _, files in os.walk(test_dir):
            # Iterates over files in a given dir and checks if they
            # are a template test definition file

            for file in files:
                if file == template_definitions:
                    # Inputs template yaml data
                    with open(os.path.join(root, file), "r", encoding="utf-8") as template_file:
                        template = template_file.read()

                        # Uses Jinja2 templating to generate new test definition
                        # file and replace the given templates
                        test_template = Template(str(template), undefined=NullUndefined)
                        master_template = Template(str(master_definitions), undefined=NullUndefined)
                        replace_data = yaml.safe_load(master_template.render())

                        new = test_template.render(replace_data)
                        yaml_new = yaml.safe_load(new)

                        new_file = os.path.join(root, test_definitions)
                        with open(new_file, "w", encoding="utf-8") as outfile:
                            yaml.safe_dump(yaml_new, outfile, sort_keys=False)
                        logging.info("Regenerared test definition files")

    def generate_test_definitions(self):
        """
        Generates test_definition files using master test definition file
        and template test definition files
        """

        try:
            logging.info("Attempting to regenerate test definition files")
            definitions = self.data_model["parameters"]

            # Checks if generate_test_definitions is true
            if definitions["generate_test_definitions"]:
                # Inputs relevant test_definition files information
                master_definitions = tests_tools.import_yaml(definitions["master_definitions"])
                template_definitions = definitions["template_definitions"]
                test_definitions = definitions["test_definitions"]

                # Iterates through test directories
                for test_dir in definitions["test_dirs"]:
                    self.write_test_def_file(
                        template_definitions=template_definitions,
                        master_definitions=master_definitions,
                        test_dir=test_dir,
                        test_definitions=test_definitions,
                    )
        except OSError:
            print("Unable to regenerate test definition files.")

    def setup_test_runner(self):
        """Setup eapi cfg, remove result files, set test params"""

        logging.info("Starting test setup")
        self._render_eapi_cfg()
        self._remove_result_files()
        self._remove_test_results_dir()
        self._set_test_parameters()

    def test_runner(self):
        """Run tests"""

        joined_params = " ".join(self.test_parameters)
        logging.info(f"Starting Test with parameters: {self.test_parameters}")
        print(f"Starting test with command: pytest {joined_params}\n")

        pytest_result = pytest.main(self.test_parameters)

        if pytest_result == ExitCode.NO_TESTS_COLLECTED:
            print(f"No tests collected with pytest command: pytest {joined_params}")
            sys.exit(1)
        elif pytest_result == ExitCode.USAGE_ERROR:
            print(f"Pytest usage error with parameters: pytest {joined_params}")
            sys.exit(1)

    def _init_parameters(self):
        """Initialize all test values"""

        parameter_keys = [
            "verbose",
            "stdout",
            "test_cases",
            "html_report",
            "excel_report",
            "json_report",
            "processes",
            "mark",
            "setup_show",
        ]

        logging.info("Initialize test parameter values")
        for parameter_key in parameter_keys:
            if parameter_key not in self.data_model["parameters"]:
                self.data_model["parameters"][parameter_key] = None

    def _set_verbosity(self):
        """Set verbosity for test run"""

        verbose = self.data_model["parameters"]["verbose"]
        self._set_cmdline_no_input(verbose, "-v")

    def _set_stdout(self):
        """Set stdout for test run"""

        stdout = self.data_model["parameters"]["stdout"]
        self._set_cmdline_no_input(stdout, "-s")

    def _set_setup_show(self):
        """Set setup-show for test run"""

        setup_show = self.data_model["parameters"]["setup_show"]
        self._set_cmdline_no_input(setup_show, "--setup-show")

    def _set_cmdline_no_input(self, parameter, ext):
        """Set parameters for test run"""
        if parameter and ext not in self.test_parameters:
            logging.info(f"Enable pytest output {parameter}")
            self.test_parameters.append(ext)
        if not parameter and ext in self.test_parameters:
            logging.info(f"Remove and disable pytest output {parameter}")
            parameter_index = self.test_parameters.index(ext)
            self.test_parameters.pop(parameter_index)
        else:
            logging.warning(f"Disable pytest output {parameter}")

    def _set_test_cases(self):
        """Set test cases for test run"""

        test_cases = self.data_model["parameters"]["test_cases"]

        logging.info(f"Run the following tests: {test_cases}")
        if test_cases == "All":
            logging.info("Running All test cases.")
        elif not test_cases:
            logging.info("Could not find test cases.")
        else:
            self.test_parameters.append(f"-k {test_cases}")

    def _set_html_report(self):
        """Set html_report for test run"""

        html_report = self.data_model["parameters"]["html_report"]
        html_name = f"--html={html_report}.html"
        list_out = [x for x in self.test_parameters if "--html" in x]

        if html_report and html_name not in self.test_parameters:
            logging.info(f"Set HTML report name to: {html_name}")
            self.test_parameters.append(html_name)
        elif not html_report and len(list_out) > 0:
            for list_item in list_out:
                parameter_index = self.test_parameters.index(list_item)
                self.test_parameters.pop(parameter_index)
        else:
            logging.warning("HTML report will NOT be created")

    def _set_excel_report(self, report_dir):
        """Set excel_report for test run"""

        excel_report = self.data_model["parameters"]["excel_report"]
        excel_name = f"--excelreport={report_dir}/{excel_report}.xlsx"
        self._set_cmdline_report(excel_report, excel_name, "--excelreport")

    def _set_json_report(self):
        """Set json_report for test run"""

        json_report = self.data_model["parameters"]["json_report"]
        json_name = f"--json={json_report}.json"
        self._set_cmdline_report(json_report, json_name, "--json")

    def _set_cmdline_report(self, parameter, report, ext):
        """Set report name for test run"""
        list_out = [x for x in self.test_parameters if ext in x]

        if parameter and report not in self.test_parameters:
            logging.info(f"Set {ext} report name to: {report}")
            self.test_parameters.append(report)
        elif not parameter and len(list_out) > 0:
            for list_item in list_out:
                parameter_index = self.test_parameters.index(list_item)
                self.test_parameters.pop(parameter_index)
        else:
            logging.warning(f"{ext} report will NOT be created")

    def _set_processes(self):
        """Set processes for test run"""
        processes = self.data_model["parameters"]["processes"]
        self._set_cmdline_input(processes, "-n")

    def _get_markers(self):
        """Get markers for test run"""
        config = configparser.ConfigParser()
        config.read(self.get_pytest_file)
        markers = config.get("pytest", "markers")
        markers = list(filter(None, [marker.split(":")[0] for marker in markers.split("\n")]))
        return markers

    def _set_mark(self):
        """Set mark for test run"""
        mark = self.data_model["parameters"].get("mark")
        if mark and mark not in self._get_markers():
            print(f"Marker {mark} is not supported. Update marker parameter in definition file")
            sys.exit(0)
        self._set_cmdline_input(mark, "-m")

    def _set_junit(self, report_dir):
        """Set junit-xml for test run"""
        self.test_parameters.append(f"--junit-xml={report_dir}/report.xml")

    def _set_test_dirs(self, test_dirs):
        """Append test dirs for test run"""
        for test_dir in test_dirs:
            self.test_parameters.append(test_dir)

    def _set_cmdline_input(self, parameter, ext):
        """Set command line params for test run"""
        list_out = [x for x in self.test_parameters if ext in x]

        if parameter and len(list_out) == 0:
            logging.info(f"Set PyTest {ext} to: {parameter}")
            self.test_parameters.append(f"{ext} {parameter}")
        elif parameter and len(list_out) > 0:
            for list_item in list_out:
                parameter_index = self.test_parameters.index(list_item)
                self.test_parameters.pop(parameter_index)
            logging.info(f"Set PyTest {ext} to: {parameter}")
            self.test_parameters.append(f"{ext} {parameter}")
        elif not parameter and len(list_out) > 0:
            for list_item in list_out:
                parameter_index = self.test_parameters.index(list_item)
                self.test_parameters.pop(parameter_index)
        else:
            logging.info(f"Not Setting PyTest {ext}")

    def _set_test_parameters(self):
        """Use data-model to create test parameters"""

        report_dir = self.data_model["parameters"]["report_dir"]
        test_dirs = self.data_model["parameters"]["test_dirs"]

        logging.info("Use data-model to create test parameters")
        logging.info("Setting test parameters")
        self._init_parameters()
        self._set_verbosity()
        self._set_stdout()
        self._set_setup_show()
        self._set_test_cases()
        self._set_html_report()
        self._set_excel_report(report_dir)
        self._set_json_report()
        self._set_processes()
        self._set_mark()
        self._set_junit(report_dir)
        self._set_test_dirs(test_dirs)

    def _render_eapi_cfg(self):
        """Render .eapi.conf file so pytests can log into devices"""

        logging.info("Render .eapi.conf file for device access")
        eapi_template = self.data_model["parameters"]["eapi_template"]
        eapi_file = self.data_model["parameters"]["eapi_file"]
        duts = self.duts_model["duts"]

        try:
            logging.info(f"Open {eapi_template} Jinja2 template for reading")

            with open(eapi_template, "r", encoding="utf-8") as jinja_file:
                logging.info(f"Read and save contents of {eapi_template} Jinja2 template")
                jinja_template = jinja_file.read()
                logging.info(
                    f"Using {eapi_template} Jinja2 template to "
                    f"render {eapi_file} file with parameters {duts}"
                )
                resource_file = (
                    jinja2.Environment(autoescape=True)
                    .from_string(jinja_template)
                    .render(duts=duts)
                )
        except IOError as err_data:
            print(f">>> ERROR READING {eapi_template}: {err_data}")
            logging.error(f"ERROR READING {eapi_template}: {err_data}")
            logging.error("EXITING TEST RUNNER")
            sys.exit(1)

        self._write_file(resource_file)

    def _write_file(self, file_data):
        """Write data to a file

        Args:
            file_data (str): Data to write to file
        """

        eapi_file = self.data_model["parameters"]["eapi_file"]

        logging.info(f"Rendered {eapi_file} as: {file_data}")
        try:
            logging.info(f"Open {eapi_file} for writing")

            with open(eapi_file, "w", encoding="utf-8") as output_file:
                output_file.write(file_data)
        except (IOError, FileNotFoundError) as err_data:
            print(f">>> ERROR WRITING {eapi_file}: {err_data}")
            logging.error(f"ERROR WRITING {eapi_file}: {err_data}")
            logging.error("EXITING TEST RUNNER")
            sys.exit(1)

        logging.info(f"Change permissions of {eapi_file} to 777")
        os.chmod(eapi_file, stat.S_IRWXU)

    def _remove_result_files(self):
        """Remove pre-existing results file"""

        results_dir = self.data_model["parameters"]["results_dir"]
        logging.info(f"Remove any existing results files in results directory {results_dir}")

        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        results_files = os.listdir(results_dir)
        logging.info(f"Result files are {results_files}")

        for name in results_files:
            if "result-" in name:
                result_file = f"{results_dir}/{name}"
                logging.info(f"Remove result file: {result_file}")
                os.remove(result_file)
            else:
                logging.warning(f"Not removing file: {name}")

    def _remove_test_results_dir(self):
        """Removing the subdirectories and the files within them belonging to TEST RESULTS dir"""

        test_results_dir = "reports/TEST RESULTS"

        if os.path.exists(test_results_dir):
            # Deleting a non-empty folder
            shutil.rmtree(test_results_dir, ignore_errors=True)
            logging.info(f"Deleted {test_results_dir} directory successfully")
