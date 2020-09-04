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

from pprint import pprint
import concurrent.futures
import openpyxl
import jinja2
import pyeapi
import yaml
import logging
import sys
import os
import stat
import fcntl
import time 


logging.basicConfig(level=logging.INFO, filename='vane.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_suite_setup():
    """ Do tasks to setup test suite """

    logging.info('Starting Test Suite setup')
    # TODO: Don't hard code yaml_file
    yaml_file = "definitions.yaml"
    test_parameters = import_yaml(yaml_file)
    duts_list = return_dut_list(test_parameters)
    init_show_log(test_parameters)
    duts = init_duts(EOS_SHOW_CMDS, test_parameters)

    logging.info(f'Return to test suites: \nduts_lists: {duts_list}'
                 f'\nduts: {duts}')
    return duts, duts_list


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
            print(f">>>  ERROR IN DEFINITIONS FILE")
            logging.error('NO SHOW_LOG CONFIGURED IN TEST DEFs')
            logging.error('EXITING TEST RUNNER')
            sys.exit(1)
    else:
        logging.error('NO PARAMETERS CONFIGURED IN TEST DEFs')
        logging.error('EXITING TEST RUNNER')
        sys.exit(1)

    logging.info(f'Opening {log_file} for write')
    try:
        with open(log_file, 'w') as show_log_file:
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
                except yaml.YAMLError as e:
                    print(f">>> ERROR IN YAML FILE")
                    logging.error(f'ERROR IN YAML FILE: {e}')
                    logging.error('EXITING TEST RUNNER')
                    sys.exit(1)
        except OSError as e:
            print(f">>> YAML FILE MISSING")
            logging.error(f'ERROR YAML FILE: {yaml_file} NOT '
                          f'FOUND. {e}')
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
        print(f">>> NO DUTS CONFIGURED")
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

    logging.info('Finding DUTs and then execute inputted show commands on '
                 'each dut.  Return structured data of DUTs output data, '
                 'hostname, and connection.')
    duts = login_duts(test_parameters)
    workers = len(duts)

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

    for show_cmd in show_cmds:
        function_def = f'test_{("_").join(show_cmd.split())}'
        logging.info(f'Executing show command: {show_cmd} for test {function_def}')

        dut["output"]["interface_list"] = return_interfaces(name, test_parameters)

        json_output, text_output = return_show_cmd(show_cmd, dut, function_def, test_parameters)
        logging.info(f'Returned JSON output {json_output}')
        logging.info(f'Returned text output {text_output}')

        logging.info(f'Adding output of {show_cmd} to duts data structure')

        dut["output"][show_cmd] = {}
        dut["output"][show_cmd]["json"] = json_output[0]["result"]
        dut["output"][show_cmd]["text"] = text_output[0]["output"]

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

    logging.info(f'Return model data and text output from show commands and log text output')
    conn = dut['connection']
    name = dut["name"]

    show_output = conn.enable(show_cmd)
    logging.info(f'Raw json output of {show_cmd} on dut {name}: {show_output}')

    show_output_text = conn.run_commands(show_cmd, encoding='text')
    logging.info(f'Raw text output of {show_cmd} on dut {name}: {show_output_text}')
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

    logging.info(f'Parse test_parameters for interface connections and return them to test')
    interface_list = []
    duts = test_parameters["duts"]

    for dut in duts:
        dut_name = dut["name"]

        if dut_name == hostname:
            logging.info(f'Discovering interface parameters for: {hostname}')
            neighbors = dut["neighbors"]

            for neighbor in neighbors:
                interface = {}
                logging.info(f'Adding interface parameters: {neighbor} neighbor for: {dut_name}')
                
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
        logging.info(f'Openig file {show_log} and append show output: {output}')
        with open(show_log, 'a') as log_file:
            log_file.write(f"\ntest_suite::{test_name}[{hostname}]:\n{output}")
    except BaseException as error:
        print(f">>>  ERROR OPENING LOG FILE: {error}")
        logging.error(f"ERROR OPENING LOG FILE: {error}")
        logging.error('EXITING TEST RUNNER')
        sys.exit(1)


def get_parameters(tests_parameters, test_suite, test_case):
    """ Return test parameters for a test case

        Args:
            tests_parameter 
    """

    logging.info('Identify test case and return parameters')
    test_suite = test_suite.split('/')[-1]

    logging.info(f'Return testcases for Test Suite: {test_suite}')
    suite_parameters = [param for param in tests_parameters['test_suites'] if param['name'] == test_suite]
    logging.info(f'Suite_parameters: {suite_parameters}')

    logging.info(f'Return parameters for Test Case: {test_case}')
    case_parameters = [param for param in suite_parameters[0]['testcases'] if param['name'] == test_case]
    logging.info(f'Case_parameters: {case_parameters[0]}')

    return case_parameters[0]


def verify_show_cmd(show_cmd, dut):
    """ Verify if show command was successfully executed on dut

        show_cmd (str): show command 
        dut (dict): data structure of dut parameters
    """

    dut_name = dut["name"]
    logging.info(f'Verify if show command |{show_cmd}| was successfully executed '
                 f'on {dut_name} dut')

    if show_cmd in dut["output"]:
        logging.info(f'Verified output for show command |{show_cmd}| on {dut_name}')
    else:
        logging.critical(f'Show command |{show_cmd}| not executed on {dut_name}')
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

    logging.info(f'{tacacs_servers} tacacs serverws are configured so returning {tacacs_bool}')

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
        logging.info(f'{dut_name} is not a VEOS instance so returning {veos_bool}')

    return veos_bool


def output_to_log_file(test_suite, test_name, hostname, output):
    """ Open log file for logging test show commands

        Args:
          LOG_FILE (str): path and name of log file
    """

    try:
        with open(LOG_FILE, 'a') as log_file:
            log_file.write("\n%s::%s[%s]:\n%s" % (
                test_suite, test_name, hostname, output))

    except BaseException as error:
        print(f">>>  Error opening log file: {error}")
        raise


def return_show_cmd_output(show_cmd, dut, test_suite, test_name):
    """ Return model data and text output from show commands and log text output.

        Args:
          show_cmd (str): show command
          dut (dict): Dictionary containing dut name and connection
          test_suite (str): test suite name
          test_name (str): test case name

        return:
          show_output (dict): json output of cli command
          show_output (dict): plain-text output of cli command
    """

    show_output = dut['connection'].enable(show_cmd)
    show_output_text = dut['connection'].run_commands(
        show_cmd, encoding='text')
    output_to_log_file(
        test_suite, test_name, dut['name'], show_output_text[0]['output'])

    return show_output, show_output_text


def return_dut_info(show_cmds, test_suite):
    """ Use PS LLD spreadsheet to find interesting duts and then execute
        inputted show commands on each dut.  Return structured data of
        dut's output data, hostname, and connection

        Args:
          show_cmds (str):  list of interesting show commands
          test_suite (str): test suite name

        return:
          duts (dict): structured data of dut's output data, hostname, and
                       connection
    """

    xlsx_workbook = import_spreadsheet()
    mgmt_addresses = parse_management_addressing(xlsx_workbook)
    render_eapi_config(mgmt_addresses)
    duts = connect_to_duts(mgmt_addresses)

    for dut in duts:
        dut["output"] = {}

        for show_cmd in show_cmds:
            function_def = f'test_{("_").join(show_cmd.split())}'
            dut["output"][show_cmd] = {}
            json_output, text_output = return_show_cmd_output(
                show_cmd, dut, test_suite, function_def)
            dut["output"][show_cmd]["json"] = json_output[0]["result"]
            dut["output"][show_cmd]["text"] = text_output[0]["output"]

    return duts


def return_dut_info_threaded(show_cmds, test_suite):
    """ Use PS LLD spreadsheet to find interesting duts and then execute
        inputted show commands on each dut.  Return structured data of
        dut's output data, hostname, and connection.  Using threading to
        make method more efficent.

        Args:
          show_cmds (str):  list of interesting show commands
          test_suite (str): test suite name

        return:
          duts (dict): structured data of duts output data, hostname, and
                       connection
    """

    xlsx_workbook = import_spreadsheet()
    mgmt_addresses = parse_management_addressing(xlsx_workbook)
    render_eapi_config(mgmt_addresses)
    duts = connect_to_duts(mgmt_addresses)
    workers = len(duts)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        {executor.submit(
            dut_thread, dut, show_cmds, test_suite, xlsx_workbook): dut for dut in duts}

    return duts


def dut_thread(dut, show_cmds, test_suite, xlsx_workbook):
    """ Execute inputted show commands on dut.  Update dut structured data
        with show output.

        Args:

          dut (dict): structured data of a dut output data, hostname, and
          connection test_suite (str): test suite name
    """

    dut["output"] = {}

    for show_cmd in show_cmds:
        function_def = f'test_{("_").join(show_cmd.split())}'
        dut["output"][show_cmd] = {}
        dut["output"]["interface_list"] = return_interfaces(dut["name"], xlsx_workbook)
        json_output, text_output = return_show_cmd_output(
            show_cmd, dut, test_suite, function_def)
        dut["output"][show_cmd]["json"] = json_output[0]["result"]
        dut["output"][show_cmd]["text"] = text_output[0]["output"]

def import_test_definition():
    """ import spreadsheet for parsing

        return:
           test_definition (dict): Abstraction of testing parameters
    """

    try:
        with open(definitions.TEST_DEFINITION_FILE, 'r') as test_definition:
            return yaml.load(test_definition, Loader=yaml.FullLoader)
    except BaseException as error:
        print(f">>>  Error Test Definition failed to open with following error: \
{error}")
        raise


def generate_dut_info_threaded(show_cmds, test_suite):
    """ Use PS LLD spreadsheet to find interesting duts and then execute
        inputted show commands on each dut.  Return structured data of
        dut's output data, hostname, and connection.  Using threading to
        make method more efficent.

        Args:
          show_cmds (str):  list of interesting show commands
          test_suite (str): test suite name

        return:
          duts (dict): structured data of duts output data, hostname, and
                       connection
    """

    test_definition = import_test_definition()
    #render_eapi_config(test_definition['duts'])
    duts = connect_to_duts(test_definition['duts'])
    workers = len(duts)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        {executor.submit(
            dut_thread2, dut, show_cmds, test_suite, test_definition): dut for dut in duts}

    return duts


def dut_thread2(dut, show_cmds, test_suite, test_definition):
    """ Execute inputted show commands on dut.  Update dut structured data
        with show output.

        Args:
          dut (dict): structured data of a dut output data, hostname, and
          connection test_suite (str): test suite name
    """

    dut["output"] = {}

    for show_cmd in show_cmds:
        function_def = f'test_{("_").join(show_cmd.split())}'
        dut["output"][show_cmd] = {}
        dut["output"]["interface_list"] = generate_interface_list(dut["name"], test_definition)
        json_output, text_output = return_show_cmd_output(
            show_cmd, dut, test_suite, function_def)
        dut["output"][show_cmd]["json"] = json_output[0]["result"]
        dut["output"][show_cmd]["text"] = text_output[0]["output"]


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

def write_results(test_parameters, dut_name, test_suite, actual_output=None, test_result=None):
    """ Write test results to YAML file for post-processing

        Args:
            test_parameters (dict): Input DUT test definitions
            actual_output (?): Output of test case
            test_result (bool): Pass / Fail condition 
            dut_name (str): Name of Device Under Test
            test_suite (str): Name of Test Suite 

        YAML Data structure:
            testsuites:
             - name: <test suite>
               testcases:
                 - name: <test name>
                   duts:
                     - dut: <dut name>
                       description:
    """

    test_suite = test_suite.split('/')[-1]
    test_parameters['actual_output'] = actual_output
    test_parameters['test_result'] = test_result
    test_parameters['dut'] = dut_name

    test_case = test_parameters['name']

    #TODO: remove hard code
    yaml_file = 'result.yml'
    yaml_data = yaml_io(yaml_file, 'read')

    if not yaml_data:
        yaml_data = {'test_suites': 
                        [ {'name': test_suite, 
                            'test_cases': [
                                {'name': test_case,
                                 'duts': []
                                }
                         ]}
                      ]
                    }

    logging.info(f'Find Index for test suite: {test_suite} on dut {dut_name}')
    test_suites = [param['name'] for param in yaml_data['test_suites']]
    if test_suite in test_suites:
        suite_index = test_suites.index(test_suite)
        logging.info(f'Test suite {test_suite} exists in results file at index {suite_index}')
    else:
        logging.info(f'Create test suite {test_suite} in results file')
        suite_stub = {'name': test_suite, 'test_cases': []}
        yaml_data['test_suites'].append(suite_stub)
        suite_index = (len(yaml_data['test_suites']) - 1)

    logging.info(f'Find Index for test case: {test_case} on dut {dut_name}')
    test_cases = [param['name'] for param in yaml_data['test_suites'][suite_index]['test_cases']]
    if test_case in test_cases:
        test_index = test_cases.index(test_case)
        logging.info(f'Test case {test_case} exists in results file at index {test_index}')
    else:
        logging.info(f'Create test case {test_case} in results file')
        test_stub = {'name': test_case, 'duts': []}
        yaml_data['test_suites'][suite_index]['test_cases'].append(test_stub)
        test_index = (len(yaml_data['test_suites'][suite_index]['test_cases']) - 1)    

    logging.info(f'Add DUT {dut_name} to test case {test_case} with parameters {test_parameters}')
    yaml_data['test_suites'][suite_index]['test_cases'][test_index]['duts'].append(test_parameters)

    _ = yaml_io(yaml_file, 'write', yaml_data)


def yaml_io(yaml_file, io, yaml_data=None):
    """ Write test results to YAML file for post-processing

        Args:
            yaml_file (str): Name of YAML file
            io (str): Read or write to YAML file
    """

    while True:
        try:
            if io == 'read':
                with open(yaml_file, 'r') as yaml_in:
                    fcntl.flock(yaml_in, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    yaml_data = yaml.safe_load(yaml_in)
                    fcntl.flock(yaml_in, fcntl.LOCK_UN)
                    break
            else:
                with open(yaml_file, 'w') as yaml_out:
                    fcntl.flock(yaml_out, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    yaml.dump(yaml_data, yaml_out, default_flow_style=False)
                    fcntl.flock(yaml_out, fcntl.LOCK_UN)
                    break
        except:
            time.sleep(0.05)
    
    return yaml_data
