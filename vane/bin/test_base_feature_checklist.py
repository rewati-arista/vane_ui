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

""" Tests to validate base feature status."""

from pprint import pprint
import inspect
import pytest
import tests_tools
import os
import argparse
import logging


logging.basicConfig(level=logging.INFO, filename='base_features.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info('Starting base_features.log file')


TEST_SUITE = __file__
logging.info('Starting base feature test cases')
# TODO: Remove hard code reference
LOG_FILE = {"parameters": {"show_log": "show_output.log"}}


class pytestTests():
    """ EOS Extensions Test Suite
    """

    def test_assert_true(self):
        """ Prior to running any tests this test Validates that PyTest is working
            correct by verifying PyTest can assert True.
        """
        logging.info('Prior to running any tests this test Validates that PyTest '
                    'is working correct by verifying PyTest can assert True.')
        assert True

@pytest.mark.platform_status
@pytest.mark.host
class hostTests():
    """ Host status Test Suite
    """

    def test_if_hostname_is_correcet_on_(self, dut, tests_definitions):
        """ Verify hostname is set on device is correct

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
    
        expected_output = dut['name']
        dut_name = dut['name']    
        eos_hostname = dut["output"][show_cmd]["json"]["hostname"]

        logging.info(f'TEST is hostname {dut_name} correct')
        logging.info(f'GIVEN hostname {dut_name}')
        logging.info(f'WHEN hostname is {eos_hostname}')    

        print(f"\nOn router |{dut_name}| the configured hostname is "
              f"|{eos_hostname}| and the correct hostname is |{expected_output}|")
        
        test_result = eos_hostname is expected_output
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}') 

        assert eos_hostname == expected_output

@pytest.mark.base_feature
@pytest.mark.filesystem
class filesystemTests():
    """ EOS File System Test Suite
    """

    def test_if_files_on_(self, dut, tests_definitions):
        """ Verify filesystem is correct and expected files are present

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        files = test_parameters["files"]
        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        for file_name in files:
            show_cmd = f"show file information {file_name}"
            logging.info(f'TEST is {file_name} file present on |{dut_name}|')
            logging.info(f'GIVEN expected {file_name} isDir state: '
                         f'|{expected_output}|')

            show_output, show_cmd_txt = tests_tools.return_show_cmd(show_cmd, dut, test_case, LOG_FILE)
            file_state = show_output[0]["result"]['isDir']

            logging.info(f'WHEN {file_name} file isDir state is |{file_state}|')    

            test_result = file_state is expected_output
            logging.info(f'THEN test case result is |{test_result}|')  
            logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}') 

            print(f"\nOn router |{dut_name}|: {file_name} file isDir state is "
                f"|{file_state}|")        
            assert expected_output is file_state

@pytest.mark.base_feature
@pytest.mark.daemons
class daemonTests():
    """ EOS Daemon Test Suite
    """

    def test_if_daemons_are_running_on_(self, dut, tests_definitions):
        """ Verify a list of daemons are running on DUT

            Args:
              dut (dict): Encapsulates dut details including name, connection
              tests_definitions (dict): Test parameters
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        daemons = test_parameters["daemons"]

        for daemon in daemons:
            logging.info(f'TEST is {daemon} daemon running on |{dut_name}|')
            logging.info(f'GIVEN expected {daemon} running state: '
                         f'|{expected_output}|')

            eos_daemon = \
                dut["output"][show_cmd]['json']['daemons'][daemon]['running']
            logging.info(f'WHEN {daemon} device running state is |{eos_daemon}|')    

            test_result = eos_daemon is expected_output
            logging.info(f'THEN test case result is |{test_result}|')  
            logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}') 

            print(f"\nOn router |{dut_name}|: {daemon} daemon running is "
                f"|{eos_daemon}|")
            assert eos_daemon is expected_output


    def test_if_daemons_are_enabled_on_(self,dut, tests_definitions):
        """ Verify a list of daemons are enabled on DUT

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        logging.info(f'TEST is terminattr daemon enabled on |{dut_name}|')
        logging.info(f'GIVEN expected terminattr​ enabled state: |{expected_output}|')

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        eos_daemon = \
            dut["output"][show_cmd]['json']['daemons']['TerminAttr']['enabled']
        logging.info(f'WHEN terminattr​ device enabled state is |{eos_daemon}|')    

        test_result = eos_daemon is expected_output
        logging.info(f'THEN test case result is |{test_result}|')
        logging.info(f'OUTPUT of |{show_cmd}|:\n\n{show_cmd_txt}') 

        print(f"\nOn router |{dut['name']}|: TerminAttr daemon enabled is "
              f"|{eos_daemon}| and expected value is |{expected_output}|.\nTest "
              f"result is {test_result}")
        assert eos_daemon is expected_output

@pytest.mark.base_feature
@pytest.mark.extensions
class extensionsTests():
    """ EOS Extensions Test Suite
    """

    def test_if_extensions_are_installed_on_(self, dut, tests_definitions):
        """ Verify a list of extension are installed on a DUT

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        extensions = test_parameters["extensions"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        for extension in extensions:
            logging.info(f'TEST is {extension} extension installed on |{dut_name}|')
            logging.info(f'GIVEN expected {extension} extension status: '
                         f'|{expected_output}|')

            if extension in dut["output"][show_cmd]['json']['extensions']:
                eos_extension = dut["output"][show_cmd]['json']['extensions'][extension]['status']
                print(f"\nOn router |{dut['name']}| {extension} extension is "
                      f"|{eos_extension}|")
                logging.info(f'WHEN {extension} extenstion installation state is |{eos_extension}|')

                test_result = (eos_extension == expected_output)
                logging.info(f'THEN test case result is |{test_result}|\n') 
                logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}') 
            else:
                print(f"\nOn router |{dut['name']}| {extension} extension "
                    f"is |NOT installed|")
                assert False

            assert eos_extension == expected_output

    def test_if_extensions_are_erroring_on_(self, dut, tests_definitions):
        """ Verify a list of extension are not erroring on a DUT

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        extensions = test_parameters["extensions"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        for extension in extensions:
            logging.info(f'TEST is {extension} extension not erroring on |{dut_name}|')
            logging.info(f'GIVEN expected {extension} extension status: |{expected_output}|')

            if extension in dut["output"][show_cmd]['json']['extensions']:
                eos_extension = dut["output"][show_cmd]['json']['extensions'][extension]['error']
                print(f"\nOn router |{dut['name']}| {extension} extension error is "
                    f"|{eos_extension}|")

                logging.info(f'WHEN {extension} extenstion error state is |{eos_extension}|')

                test_result = (eos_extension == expected_output)
                logging.info(f'THEN test case result is |{test_result}|\n')   
                logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}') 
            else:
                print(f"\nOn router |{dut['name']}| {extension} extension "
                    f"is |NOT installed|")
                assert False

            assert eos_extension is False

@pytest.mark.base_feature
@pytest.mark.users
class usersTests():
    """ EOS Users Test Suite
    """

    def test_if_usernames_are_configured_on_(self, dut, tests_definitions):
        """ Verify username is set correctly

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        usernames = test_parameters["usernames"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        for username in usernames:
            logging.info(f'TEST is {username} username configured |{dut_name}|')
            logging.info(f'GIVEN {username} username configured status: |{expected_output}|')

            if username in show_cmd_txt:
                print(f"\nOn router |{dut['name']}| |admin| username is |configured|")
                logging.info(f'WHEN {username} username configured status is |True|')
                logging.info(f'THEN test case result is |True|\n')
                logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}') 
            else:
                print(f"\nOn router |{dut['name']}| |{username}| username is "
                       "|NOT configured|")

            assert (username in show_cmd_txt) is True

@pytest.mark.base_feature
@pytest.mark.tacacs
class tacacsTests():
    """ AAA TACACS Test Suite
    """

    def test_if_tacacs_is_sending_messages_on_(self, dut, tests_definitions):
        """ Verify tacacs is working correctly

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        tacacs_servers = tests_tools.verify_tacacs(dut)

        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is |{dut_name}| sending messages to TACACS server')

        if tacacs_servers:
            eos_messages_sent_1 = \
                dut["output"][show_cmd]['json']['tacacsServers'][0]['messagesSent']
            logging.info(f'GIVEN {eos_messages_sent_1} TACACS messages sent at time 1')

            show_output, _ = tests_tools.return_show_cmd(show_cmd, dut, test_case, LOG_FILE)
            eos_messages_sent_2 = \
                show_output[0]['result']['tacacsServers'][0]['messagesSent']
            logging.info(f'WHEN {eos_messages_sent_2} TACACS messages sent at time 2')

            if eos_messages_sent_1 < eos_messages_sent_2:
                print(f"\nOn router |{dut_name}| TACACS messages2 sent: |{eos_messages_sent_2}| "
                      f"increments from TACACS messages1 sent: |{eos_messages_sent_1}|")
                logging.info(f'THEN test case result is |True|')  
            else:
                print(f"\nOn router |{dut_name}| TACACS messages2 sent: |{eos_messages_sent_2}| "
                      f"doesn't increments from TACACS messages1 sent: |{eos_messages_sent_1}|")
                logging.info(f'THEN test case result is |False|')  

            logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

            assert eos_messages_sent_1 < eos_messages_sent_2
        else:
            print(f"\nOn router |{dut_name}| does not have TACACS servers configured")       


    def test_show_if_tacacs_is_receiving_messages_on_(self, dut, tests_definitions):
        """ Verify tacacs is working correctly

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        tacacs_servers = tests_tools.verify_tacacs(dut)

        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is |{dut_name}| receiving messages to TACACS server')

        if tacacs_servers:
            eos_messages_received_1 = \
                dut["output"][show_cmd]['json']['tacacsServers'][0]['messagesReceived']
            logging.info(f'GIVEN {eos_messages_sent_1} TACACS messages recieved at time 1')


            show_output, _ = tests_tools.return_show_cmd(show_cmd, dut, test_case, LOG_FILE)
            eos_messages_received_2 = \
                show_output[0]['result']['tacacsServers'][0]['messagesReceived']
            logging.info(f'WHEN {eos_messages_sent_2} TACACS messages sent at time 2')

            if eos_messages_received_1 < eos_messages_received_2:
                print(f"\nOn router |{dut['name']}| TACACS messages2 received: "
                      f"|{eos_messages_received_2}| increments from TACACS messages1 "
                      f"received: |{eos_messages_received_1}|")
                logging.info(f'THEN test case result is |True|')  
            else:
                print(f"\nOn router |{dut['name']}| TACACS messages2 received: "
                      f"|{eos_messages_received_2}| doesn't increments from TACACS "
                      f"messages1 received: |{eos_messages_received_1}|")
                logging.info(f'THEN test case result is |False|')  

            logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

            assert eos_messages_received_1 < eos_messages_received_2
        else:
            print(f"\nOn router |{dut_name}| does not have TACACS servers configured")

@pytest.mark.base_feature
@pytest.mark.aaa
class aaaTests():
    """ AAA Test Suite
    """

    @pytest.mark.skip(reason="No AAA setup on DUTs")
    def test_if_authentication_counters_are_incrementing_on_(self, dut, tests_definitions):
        """ Verify AAA counters are working correctly

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is |{dut_name}| authentication counters incrementing')

        eos_authorization_allowed_1 = \
            dut["output"][show_cmd]['json']['authorizationAllowed']
        logging.info(f'GIVEN {eos_authorization_allowed_1} authentication counters at time 1')

        show_output, _ = tests_tools.return_show_cmd(show_cmd, dut, test_case, LOG_FILE)
        eos_authorization_allowed_2 = \
            show_output[0]['result']['authorizationAllowed']
        logging.info(f'WHEN {eos_authorization_allowed_2} authentication counters at time 2')

        if eos_authorization_allowed_1 < eos_authorization_allowed_2:
            print(f"\nOn router |{dut['name']}| AAA authorization allowed "
                  f"messages2: |{eos_authorization_allowed_2}| increments from AAA authorization "
                  f"allowed message1: |{eos_authorization_allowed_1}|")
            logging.info(f'THEN test case result is |True|')  
        else:
            print(f"\nOn router |{dut['name']}| AAA authorization allowed "
                  f"messages2: |{eos_authorization_allowed_2}| doesn't increments from AAA "
                  f"authorization allowed message1: |{eos_authorization_allowed_1}|")
            logging.info(f'THEN test case result is |False|')  

        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')
        assert eos_authorization_allowed_1 < eos_authorization_allowed_2

    def test_if_aaa_session_logging_is_working_on_(self, dut, tests_definitions):
        """ Verify AAA session logging is working by identifying eapi connection

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is |{dut_name}| AAA session logging is working by identifying eapi connection')

        eos_non_interactives = dut["output"][show_cmd]['json']['nonInteractives']
        aaa_flag = False

        for non_interactive in eos_non_interactives:
            service = eos_non_interactives[non_interactive]['service']
            logging.info(f'GIVEN {service} nonInteractive sessions')

            if service == 'commandApi':
                print(f"\nOn router |{dut['name']}| identified eAPi AAA session: \
    |{eos_non_interactives[non_interactive]['service']}|")
                aaa_flag = True

        if not aaa_flag:
            print(f"\nOn router |{dut['name']}| did NOT identified eAPi AAA session: \
    |{eos_non_interactives[non_interactive]['service']}|")

        for non_interactive in eos_non_interactives:
            assert eos_non_interactives[non_interactive]['service'] == 'commandApi'

    @pytest.mark.authorization
    def test_if_commands_authorization_methods_set_on_(self, dut, tests_definitions):
        """ Verify AAA method-lists are correctly set

            Args:
            dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        cmd_auth = test_parameters["cmd_auth"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is command authorization methods list set correct on |{dut_name}| ')
        logging.info(f'GIVEN command authorization method list: |{cmd_auth}|')

        eos_cmd_auth = \
            dut["output"][show_cmd]['json']['authorization']['commandsAuthzMethods']['privilege0-15']['methods']
        logging.info(f'WHEN EOS command authorization method list is set to |{eos_cmd_auth}|')

        test_result = eos_cmd_auth == cmd_auth
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        print(f"\nOn router |{dut_name}| AAA authorization methods for privilege0-15: |{eos_cmd_auth}|")

        assert eos_cmd_auth == cmd_auth

    @pytest.mark.authorization
    def test_if_exec_authorization_methods_set_on_(self, dut, tests_definitions):
        """ Verify AAA method-lists are correctly set

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        exec_auth = test_parameters["exec_auth"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is exec authorization methods list set correct on |{dut_name}| ')
        logging.info(f'GIVEN exec authorization method list: |{exec_auth}|')

        eos_exec_auth = \
            dut["output"][show_cmd]['json']['authorization']['execAuthzMethods']['exec']['methods']
        logging.info(f'WHEN EOS exec authorization method list is set to |{eos_exec_auth}|')

        test_result = eos_exec_auth == exec_auth
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        print(f"\nOn router |{dut_name}| AAA authorization methods for exec: |{eos_exec_auth}|")

        assert eos_exec_auth == exec_auth

    @pytest.mark.authentication
    def test_if_default_login_authentication_methods_set_on_(self, dut, tests_definitions):
        """ Verify AAA method-lists are correctly set

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        login_auth = test_parameters["login_auth"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is login authentication methods list set correct on |{dut_name}| ')
        logging.info(f'GIVEN login authentication method list: |{login_auth}|')

        eos_login_auth = \
            dut["output"][show_cmd]['json']['authentication']['loginAuthenMethods']['default']['methods']
        logging.info(f'WHEN EOS login authentication method list is set to |{eos_login_auth}|')

        test_result = eos_login_auth == login_auth
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        print(f"\nOn router |{dut_name}| AAA authentication methods for default login: |{eos_login_auth}|")

        assert eos_login_auth == login_auth

    @pytest.mark.authentication
    def test_if_login_authentication_methods_set_on_(self, dut, tests_definitions):
        """ Verify AAA method-lists are correctly set

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        login_auth = test_parameters["login_auth"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is login authentication methods list set correct on |{dut_name}| ')
        logging.info(f'GIVEN login authentication method list: |{login_auth}|')

        if login_auth:
            eos_login_auth = \
                dut["output"][show_cmd]['json']['authentication']['loginAuthenMethods']['login']['methods']
            logging.info(f'WHEN EOS login authentication method list is set to |{eos_login_auth}|')

            test_result = eos_login_auth == login_auth
            logging.info(f'THEN test case result is |{test_result}|')  
            logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

            print(f"\nOn router |{dut_name}| AAA authentication methods for login: |{eos_login_auth}|")

            assert eos_login_auth == login_auth
        else:
            logging.info(f'WHEN EOS login authentication method list is set to |None|')

            logging.info(f'THEN test case result is |True|')  
            logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

    @pytest.mark.authentication
    def test_if_dot1x_authentication_methods_set_on_(self, dut, tests_definitions):
        """ Verify AAA method-lists are correctly set

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        dot1x_auth = test_parameters["dot1x_auth"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is dot1x authentication methods list set correct on |{dut_name}| ')
        logging.info(f'GIVEN dot1x authentication method list: |{dot1x_auth}|')

        eos_dot1x_auth = \
            dut["output"][show_cmd]['json']['authentication']['dot1xAuthenMethods']['default']['methods']
        logging.info(f'WHEN EOS dot1x authentication method list is set to |{eos_dot1x_auth}|')

        test_result = eos_dot1x_auth == dot1x_auth
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        print(f"\nOn router |{dut_name}| AAA authentication methods for dot1x default: |{eos_dot1x_auth}|")

        assert eos_dot1x_auth == dot1x_auth

    @pytest.mark.authentication
    def test_if_enable_authentication_methods_set_on_(self, dut, tests_definitions):
        """ Verify AAA method-lists are correctly set

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        enable_auth = test_parameters["enable_auth"]

        logging.info(f'TEST is enable authentication methods list set correct on |{dut_name}| ')
        logging.info(f'GIVEN enable authentication method list: |{enable_auth}|')
    
        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        eos_enable_auth = \
            dut["output"][show_cmd]['json']['authentication']['enableAuthenMethods']['default']['methods']

        print(f"\nOn router |{dut['name']}| AAA authentication methods for enable default: |{eos_enable_auth}|")
        logging.info(f'WHEN EOS enable authentication method list is set to |{eos_enable_auth}|')

        test_result = eos_enable_auth == enable_auth
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert eos_enable_auth == enable_auth

    @pytest.mark.accounting
    def test_if_system_accounting_methods_set_on_(self, dut, tests_definitions):
        """ Verify AAA method-lists are correctly set

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        default_acct = test_parameters["default_acct"]
        console_acct = test_parameters["console_acct"]

        logging.info(f'TEST is system accounting methods list set correct on |{dut_name}| ')
        logging.info(f'GIVEN default system accounting method list: '
                     f'|{default_acct}| and console system accounting method'
                     f'list: |{console_acct}|')
    
        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        eos_default_acct = \
            dut["output"][show_cmd]['json']['accounting']['systemAcctMethods']['system']['defaultMethods']
        eos_console_acct = \
            dut["output"][show_cmd]['json']['accounting']['systemAcctMethods']['system']['consoleMethods']

        print(f"\nOn router |{dut['name']}| AAA accounting methods for default: |{eos_default_acct}|")
        logging.info(f'WHEN default system accounting method list: '
                     f'|{eos_default_acct}| and console system accounting method'
                     f'list: |{eos_console_acct}|')

        test_result = (eos_default_acct == default_acct) and (eos_console_acct == console_acct)
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert eos_default_acct == default_acct
        assert eos_console_acct == console_acct


# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_method_list_all_acct_exec(dut):
#     """ Verify AAA method-lists are correctly set
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show aaa methods all"
#     eos_acct_exec_methods = \
#         dut["output"][show_cmd]['json']['accounting']['execAcctMethods\
# ']['exec']['consoleMethods']
# 
#     print(f"\nOn router |{dut['name']}| AAA accounting exec methods for \
# console: |{eos_acct_exec_methods}|")
# 
#     assert eos_acct_exec_methods == ['logging']
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_method_list_all_acct_priv15(dut):
#     """ Verify AAA method-lists are correctly set
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show aaa methods all"
#     eos_acct_priv15_methods = \
#         dut["output"][show_cmd]['json']['accounting']['commandsAcctMethods\
# ']['privilege0-15']['consoleMethods']
# 
#     print(f"\nOn router |{dut['name']}| AAA accounting methods for \
# privilege0-15: |{eos_acct_priv15_methods}|")
# 
#     assert eos_acct_priv15_methods == ['logging']
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_method_list_all_acct_dot1x(dut):
#     """ Verify AAA method-lists are correctly set
# 
#          Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show aaa methods all"
#     eos_acct_dot1x_methods = \
#         dut["output"][show_cmd]['json']['accounting']['dot1xAcctMethods']['dot1x\
# ']['consoleMethods']
# 
#     print(f"\nOn router |{dut['name']}| AAA accounting methods for \
# dot1x: |{eos_acct_dot1x_methods}|")
# 
#     assert eos_acct_dot1x_methods == []
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_management_api_http_cmds_https_server_running(dut):
#     """ Verify management api is running, httpsserver is enabled on port 443,
#         httpserver is not running, and local httpserver is not running
# 
#          Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show management api http-commands"
#     eos_show_mgmt = dut["output"][show_cmd]['json']['httpsServer']['running']
# 
#     print(f"\nOn router |{dut['name']}| HTTPS Server is running state: \
# |{eos_show_mgmt}|")
# 
#     assert eos_show_mgmt is True
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_management_api_http_cmds_https_server_port(dut):
#     """ Verify management api is running, httpsserver is enabled on port 443,
#         httpserver is not running, and local httpserver is not running
# 
#          Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show management api http-commands"
#     eos_show_mgmt = dut["output"][show_cmd]['json']['httpsServer']['port']
# 
#     print(f"\nOn router |{dut['name']}| HTTPS Server is running on port: \
# |{eos_show_mgmt}|")
# 
#     assert eos_show_mgmt == 443
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_management_api_http_cmds_enabled(dut):
#     """ Verify management api is running, httpsserver is enabled on port 443,
#         httpserver is not running, and local httpserver is not running
# 
#          Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show management api http-commands"
#     eos_show_mgmt = dut["output"][show_cmd]['json']['enabled']
# 
#     print(f"\nOn router |{dut['name']}| API is enabled state: \
# |{eos_show_mgmt}|")
# 
#     assert eos_show_mgmt is True
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_management_api_http_cmds_http_server_running(dut):
#     """ Verify management api is running, httpsserver is enabled on port 443,
#         httpserver is not running, and local httpserver is not running
# 
#          Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show management api http-commands"
#     eos_show_mgmt = dut["output"][show_cmd]['json']['httpServer']['running']
# 
#     print(f"\nOn router |{dut['name']}| HTTP Server is running state: \
# |{eos_show_mgmt}|")
# 
#     assert eos_show_mgmt is False
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_management_api_http_cmds_local_http_server_running(dut):
#     """ Verify management api is running, httpsserver is enabled on port 443,
#         httpserver is not running, and local httpserver is not running
# 
#          Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show management api http-commands"
#     eos_show_mgmt = \
#         dut["output"][show_cmd]['json']['localHttpServer']['running']
# 
#     print(f"\nOn router |{dut['name']}| Local HTTP Server is running state: \
# |{eos_show_mgmt}|")
# 
#     assert eos_show_mgmt is False
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_dns(dut):
#     """ Verify DNS is running by performing pings and verifying name resolution
# 
#          Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "ping google.com"
#     _, show_output_text = common_nrfu_infra.return_show_cmd_output(
#         show_cmd, dut, TEST_SUITE, inspect.stack()[0][3])
#     show_ping = dut['connection'].run_commands(
#         'ping google.com', encoding='text')
# 
#     if 'failure' in show_output_text[0]['output']:
#         print(f"\nOn router |{dut['name']}| ping |Failed|")
#     else:
#         print(f"\nOn router |{dut['name']}| ping |Passed|")
# 
#     assert ('failure' in show_ping[0]['output']) is False
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# @pytest.mark.xfail
# def test_show_logging(dut):
#     """ Verify local log messages
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show logging"
#     eos_show_logging = dut["output"][show_cmd]["text"]
# 
#     print(f"NO AUTOMATED TEST.  MUST TEST MANUALLY")
#     print(f"\nOn router |{dut['name']}| logs:\n{eos_show_logging}")
# 
#     assert False
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_zerotouch(dut):
#     """ Verify ztp is disabled
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show zerotouch"
#     eos_show_ztp = dut["output"][show_cmd]['json']['mode']
# 
#     print(f"\nOn router |{dut['name']}| ZTP process is in mode: \
# |{eos_show_ztp}|")
# 
#     assert eos_show_ztp == 'disabled'
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_zerotouch_config(dut):
#     """ Verify zerotoucn-config file is on flash
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "dir flash:zerotouch-config"
#     eos_dir_ztp_cfg = dut["output"][show_cmd]["text"]
# 
#     print(f"\nOn router |{dut['name']}| ZTP configuration file is on flash: \
# |{('zerotouch-config' in eos_dir_ztp_cfg)}|")
# 
#     assert ("zerotouch-config" in eos_dir_ztp_cfg) is True
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_show_ntp_status(dut):
#     """ Verify ntp is setup and working correctly
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show ntp status"
#     eos_show_ntp = dut["output"][show_cmd]['text']
# 
#     print(f"\nOn router |{dut['name']}| NTP synchronized status is: \
# |{('synchronised' in eos_show_ntp)}|")
# 
#     assert ("synchronised" in eos_show_ntp) is True
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_show_ntp_associations(dut):
#     """ Verify ntp peers are correct
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show ntp associations"
#     eos_show_ntp = dut["output"][show_cmd]['json']['peers']
# 
#     print(f"\nOn router |{dut['name']}| has \
# |{len(eos_show_ntp)}| NTP peer associations")
# 
#     assert len(eos_show_ntp) > 0
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# @pytest.mark.xfail
# def test_ntp_process(dut):
#     """ Verify ntp process is running
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "bash ps -ef | grep ntp"
#     _, show_output_text = common_nrfu_infra.return_show_cmd_output(
#         show_cmd, dut, TEST_SUITE, inspect.stack()[0][3])
# 
#     print(f"NO AUTOMATED TEST.  MUST TEST MANUALLY")
#     print(f"\nOn router |{dut['name']}| NTP process:\
# \n{show_output_text[0]['output']}")
# 
#     assert False
# 