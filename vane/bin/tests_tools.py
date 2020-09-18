#!/usr/bin/python3
#
# Copyright (c) 2019, Arista Networks EOS+
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

"""Utilities for using PyTest in network testing"""

import concurrent.futures
import time
import fcntl
import sys
import logging
import os
import inspect
import pyeapi
import yaml


logging.basicConfig(level=logging.INFO, filename='vane.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def init_show_log(test_parameters):
    """ Open log file for logging test show commands

        Args:
            test_parameters (dict): Abstraction of testing parameters
    """

    logging.info('Open log file for logging test show commands')

    if "parameters" in test_parameters:
        parameters_ptr = test_parameters["parameters"]
        if "show_log" in parameters_ptr:
            log_file = parameters_ptr["show_log"]
        else:
            print(">>>  ERROR IN DEFINITIONS FILE")
            logging.error('NO SHOW_LOG CONFIGURED IN TEST DEFs')
            logging.error('EXITING TEST RUNNER')
            sys.exit(1)
    else:
        logging.error('NO PARAMETERS CONFIGURED IN TEST DEFs')
        logging.error('EXITING TEST RUNNER')
        sys.exit(1)

    logging.info(f'Opening {log_file} for write')
    try:
        with open(log_file, 'w'):
            logging.info(f'Opened {log_file} for write')
    except BaseException as error:
        print(f">>>  ERROR OPENING LOG FILE: {error}")
        logging.error(f"ERROR OPENING LOG FILE: {error}")
        logging.error('EXITING TEST RUNNER')
        sys.exit(1)


def import_yaml(yaml_file):
    """ Import YAML file as python data structure
        Args:
            yaml_file (str): Name of YAML file

        Returns:
            yaml_data (dict): YAML data structure
    """

    logging.info(f'Opening {yaml_file} for read')
    try:
        with open(yaml_file, 'r') as input_yaml:
            try:
                yaml_data = yaml.safe_load(input_yaml)
                logging.info(f'Inputed the following yaml: '
                             f'{yaml_data}')
                return yaml_data
            except yaml.YAMLError as err:
                print(">>> ERROR IN YAML FILE")
                logging.error(f'ERROR IN YAML FILE: {err}')
                logging.error('EXITING TEST RUNNER')
                sys.exit(1)
    except OSError as err:
        print(">>> YAML FILE MISSING")
        logging.error(f'ERROR YAML FILE: {yaml_file} NOT '
                      f'FOUND. {err}')
        logging.error('EXITING TEST RUNNER')
        sys.exit(1)
    sys.exit(1)


def return_dut_list(test_parameters):
    """ test_parameters to create a duts_list for a list of ids
        that will identify individual test runs

        Args:
            test_parameters (dict): Abstraction of testing parameters

        Returns:
            duts (list): List of DUT hostnames
    """

    logging.info('Creating a list of duts from test defintions')
    if 'duts' in test_parameters:
        logging.info('Duts configured in test defintions')
        duts = [dut['name'] for dut in test_parameters['duts']]
    else:
        print(">>> NO DUTS CONFIGURED")
        logging.error('NO DUTS CONFIGURED')
        logging.error('EXITING TEST RUNNER')
        sys.exit(1)

    logging.info(f'Returning duts: {duts}')
    return duts


def init_duts(show_cmds, test_parameters):
    """ Use PS LLD spreadsheet to find interesting duts and then execute
        inputted show commands on each dut.  Return structured data of
        dut's output data, hostname, and connection.  Using threading to
        make method more efficent.

        Args:
          show_cmds (str): list of interesting show commands
          test_parameters (dict): Abstraction of testing parameters
          test_suite (str): test suite name

        return:
          duts (dict): structured data of duts output data, hostname, and
                       connection
    """

    logging.info('Finding DUTs and then execute inputted show commands '
                 'on each dut.  Return structured data of DUTs output '
                 'data, hostname, and connection.')
    duts = login_duts(test_parameters)
    workers = len(duts)
    logging.info(f'Duts login info: {duts} and create {workers} workers')

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        {executor.submit(dut_worker, dut, show_cmds, test_parameters):
            dut for dut in duts}

    logging.info(f'Return duts data structure: {duts}')
    return duts


def login_duts(test_parameters):
    """ Use eapi to connect to Arista switches for testing

        Args:
          test_parameters (dict): Abstraction of testing parameters

        return:
          logins (list): List of dictionaries with connection and name
                         of DUTs
    """

    logging.info('Using eapi to connect to Arista switches for testing')
    duts = test_parameters["duts"]
    logins = []

    for dut in duts:
        name = dut['name']
        login_index = len(logins)
        logins.append({})
        login_ptr = logins[login_index]
        logging.info(f'Connecting to switch: {name} using parameters: {dut}')
        login_ptr['connection'] = pyeapi.connect_to(name)
        login_ptr['name'] = name

    logging.info(f'Returning duts logins: {logins}')
    return logins


def dut_worker(dut, show_cmds, test_parameters):
    """ Execute inputted show commands on dut.  Update dut structured data
        with show output.

        Args:
          dut (dict): structured data of a dut output data, hostname, and
          connection test_suite (str): test suite name
    """

    dut["output"] = {}
    name = dut["name"]
    logging.info(f'Executing show commands on {name}')
    logging.info(f'List of show commands {show_cmds}')
    logging.info(f'Number of show commands {len(show_cmds)}')

    for show_cmd in show_cmds:
        logging.info(f'In for looop and iterating on {show_cmd}')
        function_def = f'test_{("_").join(show_cmd.split())}'
        logging.info(f'Executing show command: {show_cmd} for test '
                     f'{function_def}')

        dut["output"]["interface_list"] = return_interfaces(name,
                                                            test_parameters)

        json_output, text_output = return_show_cmd(show_cmd,
                                                   dut,
                                                   function_def,
                                                   test_parameters)
        logging.info(f'Returned JSON output {json_output}')
        logging.info(f'Returned text output {text_output}')

        logging.info(f'Adding output of {show_cmd} to duts data structure')

        dut["output"][show_cmd] = {}
        dut["output"][show_cmd]["json"] = json_output[0]["result"]
        dut["output"][show_cmd]["text"] = text_output[0]["output"]

    logging.info(f'{name} updated with show output')


def return_show_cmd(show_cmd, dut, test_name, test_parameters):
    """ Return model data and text output from show commands and log text output.

        Args:
          show_cmd (str): show command
          dut (dict): Dictionary containing dut name and connection
          test_name (str): test case name

        return:
          show_output (dict): json output of cli command
          show_output (dict): plain-text output of cli command
    """

    logging.info(f'Raw Input for return_show_cmd \nshow_cmd: {show_cmd}\ndut: '
                 f'{dut} \ntest_name: {test_name} \ntest_parameters: '
                 f'{test_parameters}')
    conn = dut['connection']
    name = dut["name"]
    logging.info('Return model data and text output from show commands and '
                 f'log text output for {show_cmd} with connnection {conn}')

    show_output = conn.enable(show_cmd)
    logging.info(f'Raw json output of {show_cmd} on dut {name}: {show_output}')

    show_output_text = conn.run_commands(show_cmd, encoding='text')
    logging.info(f'Raw text output of {show_cmd} on dut {name}: '
                 f'{show_output_text}')
    raw_text = show_output_text[0]['output']

    export_logs(test_name, name, raw_text, test_parameters)

    return show_output, show_output_text


def return_interfaces(hostname, test_parameters):
    """ parse test_parameters for interface connections and return them to test

        Args:
            dut_name (str):      hostname of dut
            xlsx_workbook (obj): Abstraction of spreadsheet,

        return:
          interface_list (list): list of interesting interfaces based on
                                 PS LLD spreadsheet
    """

    logging.info('Parse test_parameters for interface connections and return '
                 'them to test')
    interface_list = []
    duts = test_parameters["duts"]

    for dut in duts:
        dut_name = dut["name"]

        if dut_name == hostname:
            logging.info(f'Discovering interface parameters for: {hostname}')
            neighbors = dut["neighbors"]

            for neighbor in neighbors:
                interface = {}
                logging.info(f'Adding interface parameters: {neighbor} '
                             f'neighbor for: {dut_name}')

                interface['hostname'] = dut_name
                interface['interface_name'] = neighbor['port']
                interface['z_hostname'] = neighbor['neighborDevice']
                interface['z_interface_name'] = neighbor['neighborPort']
                interface['media_type'] = ''
                interface_list.append(interface)

    logging.info(f'Returning interface list: {interface_list}')
    return interface_list


def export_logs(test_name, hostname, output, test_parameters):
    """ Open log file for logging test show commands

        Args:
          LOG_FILE (str): path and name of log file
    """

    logging.info('Open log file for logging test show commands')
    show_log = test_parameters["parameters"]["show_log"]

    try:
        logging.info(f'Opening file {show_log} and append show output: '
                     f'{output}')
        with open(show_log, 'a') as log_file:
            log_file.write(f"\ntest_suite::{test_name}[{hostname}]:\n{output}")
    except BaseException as error:
        print(f">>>  ERROR OPENING LOG FILE: {error}")
        logging.error(f"ERROR OPENING LOG FILE: {error}")
        logging.error('EXITING TEST RUNNER')
        sys.exit(1)


def get_parameters(tests_parameters, test_suite, test_case=""):
    """ Return test parameters for a test case

        Args:
            tests_parameter
    """

    if not test_case:
        test_case = inspect.stack()[1][3]
        logging.info(f'Setting testcase name to {test_case}')

    logging.info('Identify test case and return parameters')
    test_suite = test_suite.split('/')[-1]

    logging.info(f'Return testcases for Test Suite: {test_suite}')
    suite_parameters = [param for param in tests_parameters['test_suites']
                        if param['name'] == test_suite]
    logging.info(f'Suite_parameters: {suite_parameters}')

    logging.info(f'Return parameters for Test Case: {test_case}')
    case_parameters = [param for param in suite_parameters[0]['testcases']
                       if param['name'] == test_case]
    logging.info(f'Case_parameters: {case_parameters[0]}')

    case_parameters[0]['test_suite'] = test_suite

    return case_parameters[0]


def verify_show_cmd(show_cmd, dut):
    """ Verify if show command was successfully executed on dut

        show_cmd (str): show command
        dut (dict): data structure of dut parameters
    """

    dut_name = dut["name"]
    logging.info(f'Verify if show command |{show_cmd}| was successfully '
                 f'executed on {dut_name} dut')

    if show_cmd in dut["output"]:
        logging.info(f'Verified output for show command |{show_cmd}| on '
                     f'{dut_name}')
    else:
        logging.critical(f'Show command |{show_cmd}| not executed on '
                         f'{dut_name}')
        assert False


def verify_tacacs(dut):
    """ Verify if tacacs servers are configured

        dut (dict): data structure of dut parameters
    """

    dut_name = dut["name"]
    show_cmd = "show tacacs"

    tacacs_bool = True
    tacacs = dut["output"][show_cmd]['json']['tacacsServers']
    tacacs_servers = len(tacacs)
    logging.info(f'Verify if tacacs server(s) are configured '
                 f'on {dut_name} dut')

    if tacacs_servers == 0:
        tacacs_bool = False

    logging.info(f'{tacacs_servers} tacacs serverws are configured so '
                 f'returning {tacacs_bool}')

    return tacacs_bool


def verify_veos(dut):
    """ Verify DUT is a VEOS instance

        dut (dict): data structure of dut parameters
    """

    dut_name = dut["name"]
    show_cmd = "show version"

    veos_bool = False
    veos = dut["output"][show_cmd]['json']['modelName']
    logging.info(f'Verify if {dut_name} DUT is a VEOS instance')

    if veos == 'vEOS':
        veos_bool = True
        logging.info(f'{dut_name} is a VEOS instance so returning {veos_bool}')
        print(f'{dut_name} is a VEOS instance so test NOT valid')
    else:
        logging.info(f'{dut_name} is not a VEOS instance so returning '
                     f'{veos_bool}')

    return veos_bool


def generate_interface_list(dut_name, test_definition):
    """ test_definition is used to createa a interface_list for active
        DUT interfaces and attributes

        Returns:
            interface_list (list): list of active DUT interfaces and attributes
    """

    dut_hostnames = [dut['name'] for dut in test_definition['duts']]
    dut_index = dut_hostnames.index(dut_name)
    interface_list = test_definition['duts'][dut_index]['test_criteria'][0]['criteria']

    return interface_list


def post_testcase(test_parameters, comment, test_result, output_msg,
                  actual_output, dut_name):
    """ Do post processing for test case

        Args:
            test_parameters (dict): Input DUT test definitions
            comment (str): description on test operations
            test_result (bool): test result
            output_msg (str): failure reason
            actual_output (?): output of test operations
            dut_name (str): name of dut
    """

    test_parameters['comment'] = comment
    test_parameters["test_result"] = test_result
    test_parameters["output_msg"] = output_msg
    test_parameters["actual_output"] = actual_output
    test_parameters["dut"] = dut_name

    test_parameters["fail_reason"] = ""
    if not test_parameters["test_result"]:
        test_parameters["fail_reason"] = test_parameters["output_msg"]

    write_results(test_parameters)


def write_results(test_parameters):
    """ Write test results to YAML file for post-processing

        Args:
            test_parameters (dict): Input DUT test definitions

        YAML Data structure:
            testsuites:
             - name: <test suite>
               testcases:
                 - name: <test name>
                   duts:
                     - dut: <dut name>
                       description:
    """

    test_suite = test_parameters['test_suite']
    test_suite = test_suite.split('/')[-1]
    dut_name = test_parameters['dut']
    test_case = test_parameters['name']

    # TODO: remove hard code
    yaml_file = 'result.yml'

    while True:
        try:
            yaml_in = open(yaml_file, 'r+')
            fcntl.flock(yaml_in, fcntl.LOCK_EX | fcntl.LOCK_NB)
            yaml_data = yaml.safe_load(yaml_in)
            break
        except:
            time.sleep(0.05)

    if not yaml_data:
        yaml_data = {'test_suites':
                        [
                            {'name': test_suite,
                            'test_cases': [
                                    {'name': test_case,
                                     'duts': []
                                    }
                                ]
                            }
                        ]
                    }
    else:
        yaml_in.seek(0)
        yaml_in.truncate()

    logging.info(f'\n\n\rFind the Index for test suite: {test_suite} on dut '
                 f'{dut_name}\n\n\r')
    logging.info(yaml_data['test_suites'])
    test_suites = [param['name'] for param in yaml_data['test_suites']]

    if test_suite in test_suites:
        suite_index = test_suites.index(test_suite)
        logging.info(f'Test suite {test_suite} exists in results file at '
                     f'index {suite_index}')
    else:
        logging.info(f'Create test suite {test_suite} in results file')
        suite_stub = {'name': test_suite, 'test_cases': []}
        yaml_data['test_suites'].append(suite_stub)
        suite_index = (len(yaml_data['test_suites']) - 1)

    logging.info(f'Find Index for test case: {test_case} on dut {dut_name}')
    test_cases = [param['name'] for param in yaml_data['test_suites'][suite_index]['test_cases']]

    if test_case in test_cases:
        test_index = test_cases.index(test_case)
        logging.info(f'Test case {test_case} exists in results file at index '
                     f'{test_index}')
    else:
        logging.info(f'Create test case {test_case} in results file')
        test_stub = {'name': test_case, 'duts': []}
        yaml_data['test_suites'][suite_index]['test_cases'].append(test_stub)
        test_index = (len(yaml_data['test_suites'][suite_index]['test_cases']) - 1)

    logging.info(f'Find Index for dut {dut_name}')
    duts = [param['dut'] for param in yaml_data['test_suites'][suite_index]['test_cases'][test_index]['duts']]

    if dut_name not in duts:
        logging.info(f'Add DUT {dut_name} to test case {test_case} with '
                     f'parameters {test_parameters}')
        yaml_data['test_suites'][suite_index]['test_cases'][test_index]['duts'].append(test_parameters)

    yaml.dump(yaml_data, yaml_in, default_flow_style=False)
    fcntl.flock(yaml_in, fcntl.LOCK_UN)

    yaml_in.close()


def yaml_io(yaml_file, io_type, yaml_data=None):
    """ Write test results to YAML file for post-processing

        Args:
            yaml_file (str): Name of YAML file
            io (str): Read or write to YAML file
    """

    while True:
        try:
            if io_type == 'read':
                with open(yaml_file, 'r') as yaml_in:
                    fcntl.flock(yaml_in, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    yaml_data = yaml.safe_load(yaml_in)
                    break
            else:
                with open(yaml_file, 'w') as yaml_out:
                    yaml.dump(yaml_data, yaml_out, default_flow_style=False)
                    fcntl.flock(yaml_out, fcntl.LOCK_UN)
                    break
        except:
            time.sleep(0.05)

    return yaml_data


def return_show_cmds(test_parameters):
    """Return show commands from the test_defintions

    Args:
        test_parameters (dict): Input DUT test definitions
    """

    show_cmds = []

    logging.info(f'Discover the names of test suites from {test_parameters}')
    test_data = test_parameters['test_suites']
    test_suites = [param['name'] for param in test_data]

    for test_suite in test_suites:
        test_index = test_suites.index(test_suite)
        test_cases = test_data[test_index]['testcases']
        logging.info(f'Find show commands in test suite: {test_suite}')

        for test_case in test_cases:
            show_cmd = test_case['show_cmd']
            logging.info(f'Found show command {show_cmd}')

            if show_cmd not in show_cmds and show_cmd is not None:
                logging.info(f'Adding Show command {show_cmd}')
                show_cmds.append(show_cmd)

    logging.info('The following show commands are required for test cases: '
                 f'{show_cmds}')
    return show_cmds


def return_test_defs(test_parameters):
    """Return show commands from the test_defintions

    Args:
        def_file (test_parameters): Name of definitions file
    """

    test_defs = {'test_suites': []}
    test_dir = test_parameters['parameters']['tests_dir']
    tests_info = os.walk(test_dir)

    for dir_path, _, file_names in tests_info:
        for file_name in file_names:
            if 'test_definition.yaml' == file_name:
                file_path = f'{dir_path}/{file_name}'
                test_def = import_yaml(file_path)
                test_defs['test_suites'].append(test_def)

    export_yaml('tests_definitions.yaml', test_defs)
    logging.info('Return the following test definitions data strcuture '
                 f'{test_defs}')

    return test_defs


def export_yaml(yaml_file, yaml_data):
    """ Export python data structure as a YAML file

        Args:
            yaml_file (str): Name of YAML file
    """

    logging.info(f'Opening {yaml_file} for write')
    try:
        with open(yaml_file, 'w') as yaml_out:
            try:
                logging.info(f'Output the following yaml: '
                             f'{yaml_data}')
                yaml.dump(yaml_data, yaml_out, default_flow_style=False)
            except yaml.YAMLError as err:
                print(">>> ERROR IN YAML FILE")
                logging.error(f'ERROR IN YAML FILE: {err}')
                logging.error('EXITING TEST RUNNER')
                sys.exit(1)
    except OSError as err:
        print(">>> YAML FILE MISSING")
        logging.error(f'ERROR YAML FILE: {yaml_file} NOT '
                      f'FOUND. {err}')
        logging.error('EXITING TEST RUNNER')
        sys.exit(1)
