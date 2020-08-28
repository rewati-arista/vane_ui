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
import re


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

@pytest.mark.nrfu
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

    @pytest.mark.accounting
    def test_if_exec_accounting_methods_set_on_(self, dut, tests_definitions):
        """ Verify AAA method-lists are correctly set
            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        default_acct = test_parameters["default_acct"]
        console_acct = test_parameters["console_acct"]

        logging.info(f'TEST is exec accounting methods list set correct on |{dut_name}| ')
        logging.info(f'GIVEN exec system accounting method list: '
                     f'|{default_acct}| and exec system accounting method'
                     f'list: |{console_acct}|')
    
        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        eos_default_acct = \
            dut["output"][show_cmd]['json']['accounting']['execAcctMethods']['exec']['defaultMethods']
        eos_console_acct = \
            dut["output"][show_cmd]['json']['accounting']['execAcctMethods']['exec']['consoleMethods']

        print(f"\nOn router |{dut['name']}| AAA accounting exec methods for console: |{eos_console_acct}|")
        logging.info(f'WHEN default exec accounting method list: '
                     f'|{eos_default_acct}| and console exec accounting method'
                     f'list: |{eos_console_acct}|')

        test_result = (eos_default_acct == default_acct) and (eos_console_acct == console_acct)
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert eos_default_acct == default_acct
        assert eos_console_acct == console_acct

    @pytest.mark.accounting
    def test_if_priviledge_accounting_methods_set_on_(self, dut, tests_definitions):
        """ Verify AAA method-lists are correctly set

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        default_acct = test_parameters["default_acct"]
        console_acct = test_parameters["console_acct"]

        logging.info(f'TEST is priviledge accounting methods list set correct on |{dut_name}| ')
        logging.info(f'GIVEN priviledge system accounting method list: '
                     f'|{default_acct}| and priviledge system accounting method'
                     f'list: |{console_acct}|')
    
        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        eos_default_acct = \
            dut["output"][show_cmd]['json']['accounting']['commandsAcctMethods']['privilege0-15']['defaultMethods']
        eos_console_acct = \
            dut["output"][show_cmd]['json']['accounting']['commandsAcctMethods']['privilege0-15']['consoleMethods']

        print(f"\nOn router |{dut['name']}| AAA accounting exec methods for console: |{eos_console_acct}|")
        logging.info(f'WHEN default privilege accounting method list: '
                     f'|{eos_default_acct}| and console privilege accounting method'
                     f'list: |{eos_console_acct}|')

        test_result = (eos_default_acct == default_acct) and (eos_console_acct == console_acct)
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert eos_default_acct == default_acct
        assert eos_console_acct == console_acct
    
    @pytest.mark.accounting
    def test_if_dot1x_accounting_methods_set_on_(self, dut, tests_definitions):
        """ Verify AAA method-lists are correctly set

             Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        default_acct = test_parameters["default_acct"]
        console_acct = test_parameters["console_acct"]

        logging.info(f'TEST is dot1x accounting methods list set correct on |{dut_name}| ')
        logging.info(f'GIVEN dot1x system accounting method list: '
                     f'|{default_acct}| and dot1x system accounting method'
                     f'list: |{console_acct}|')
    
        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        eos_default_acct = \
            dut["output"][show_cmd]['json']['accounting']['dot1xAcctMethods']['dot1x']['defaultMethods']
        eos_console_acct = \
            dut["output"][show_cmd]['json']['accounting']['dot1xAcctMethods']['dot1x']['consoleMethods']

        print(f"\nOn router |{dut['name']}| AAA accounting exec methods for dot1x: |{eos_console_acct}|")
        logging.info(f'WHEN default dot1x accounting method list: '
                     f'|{eos_default_acct}| and console dot1x accounting method'
                     f'list: |{eos_console_acct}|')

        test_result = (eos_default_acct == default_acct) and (eos_console_acct == console_acct)
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert eos_default_acct == default_acct
        assert eos_console_acct == console_acct

@pytest.mark.base_feature
@pytest.mark.api
class apiTests():
    """ AAA Test Suite
    """

    def test_if_management_https_api_server_is_running_on_(self, dut, tests_definitions):
        """ Verify management api is running, httpsserver is enabled on port 443,
            httpserver is not running, and local httpserver is not running

             Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        https_status = test_parameters["expected_output"]

        logging.info(f'TEST is HTTPS API running on |{dut_name}| ')
        logging.info(f'GIVEN HTTPS API state is |{https_status}|')

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        eos_https_status = dut["output"][show_cmd]['json']['httpsServer']['running']

        print(f"\nOn router |{dut_name}| HTTPS Server is running state: |{eos_https_status}|")
        logging.info(f'WHEN HTTPS API state is |{eos_https_status}|')

        test_result = https_status == eos_https_status
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert https_status == eos_https_status

    def test_if_management_https_api_server_port_is_correct_on_(self, dut, tests_definitions):
        """ Verify management api is running, httpsserver is enabled on port 443,
            httpserver is not running, and local httpserver is not running

             Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        https_port = test_parameters["expected_output"]

        logging.info(f'TEST is HTTPS API port on |{dut_name}| ')
        logging.info(f'GIVEN HTTPS API port is |{https_port}|')

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        eos_https_port = dut["output"][show_cmd]['json']['httpsServer']['port']

        print(f"\nOn router |{dut_name}| HTTPS Server is running on port: |{eos_https_port}|")
        logging.info(f'WHEN HTTPS API port is |{eos_https_port}|')

        test_result = https_port == eos_https_port
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')
    
        assert eos_https_port == https_port

    def test_if_management_https_api_server_is_enabled_on_(self, dut, tests_definitions):
        """ Verify management api is running, httpsserver is enabled on port 443,
            httpserver is not running, and local httpserver is not running

             Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        https_enabled = test_parameters["expected_output"]

        logging.info(f'TEST is HTTPS API enabled on |{dut_name}| ')
        logging.info(f'GIVEN HTTPS API enabled is |{https_enabled}|')

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        eos_https_enabled = dut["output"][show_cmd]['json']['enabled']

        print(f"\nOn router |{dut_name}| API is enabled state: |{eos_https_enabled}|")
        logging.info(f'WHEN HTTPS API enabled is |{eos_https_enabled}|')

        test_result = https_enabled == eos_https_enabled
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')
    
        assert https_enabled == eos_https_enabled

    def test_if_management_http_api_server_is_running_on_(self, dut, tests_definitions):
        """ Verify management api is running, httpsserver is enabled on port 443,
            httpserver is not running, and local httpserver is not running

             Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        http_status = test_parameters["expected_output"]

        logging.info(f'TEST is HTTP API running on |{dut_name}| ')
        logging.info(f'GIVEN HTTP API state is |{http_status}|')

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        eos_http_status = dut["output"][show_cmd]['json']['httpServer']['running']

        print(f"\nOn router |{dut_name}| HTTP Server is running state: |{eos_http_status}|")
        logging.info(f'WHEN HTTP API state is |{eos_http_status}|')

        test_result = http_status == eos_http_status
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert http_status is eos_http_status

    def test_if_management_local_http_api_server_is_running_on_(self, dut, tests_definitions):
        """ Verify management api is running, httpsserver is enabled on port 443,
            httpserver is not running, and local httpserver is not running

             Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        dut_name = dut['name']
        http_status = test_parameters["expected_output"]

        logging.info(f'TEST is local HTTP API running on |{dut_name}| ')
        logging.info(f'GIVEN local HTTP API state is |{http_status}|')

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        eos_http_status = \
            dut["output"][show_cmd]['json']['localHttpServer']['running']

        print(f"\nOn router |{dut['name']}| Local HTTP Server is running state: |{http_status}|")
        logging.info(f'WHEN HTTP API state is |{eos_http_status}|')

        test_result = http_status == eos_http_status
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert http_status is eos_http_status

@pytest.mark.base_feature
@pytest.mark.dns
class dnsTests():
    """ DNS Test Suite
    """

    def test_if_dns_resolves_on_(self, dut, tests_definitions):
        """ Verify DNS is running by performing pings and verifying name resolution

             Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        urls = test_parameters["urls"]
        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        dut_conn = dut['connection']

        for url in urls:
            show_cmd = f"ping {url}"
            logging.info(f'TEST can |{dut_name}| resolve {url}')
            logging.info(f'GIVEN URL is |{url}|')
            logging.info(f'WHEN exception is |Name or service not known| string')

            show_cmd_txt = dut_conn.run_commands(show_cmd, encoding='text')
            show_cmd_txt = show_cmd_txt[0]['output']

            if 'Name or service not known' in show_cmd_txt:
                print(f"\nOn router |{dut_name}| DNS resolution |Failed| for {url}")
                logging.info(f'THEN test case result is |Failed|')  
                logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')
                assert False
            else:
                print(f"\nOn router |{dut_name}| DNS resolution |Passed| for {url}")
                logging.info(f'THEN test case result is |Passed|')  
                logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

@pytest.mark.base_feature
@pytest.mark.logging
class loggingTests():
    """ Logging Test Suite
    """
    
    def test_if_log_messages_appear_on_(self, dut, tests_definitions):
        """ Verify local log messages

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        sys_msgs = test_parameters["sys_msgs"]
        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        for sys_msg in sys_msgs:
            logging.info(f'TEST for local log message {sys_msg} on |{dut_name}|')

            if sys_msg in show_cmd_txt:
                print(f"\nOn router |{dut_name}| message |{sys_msg}| found in local log")
                logging.info(f'THEN test case result is |Failed|')  
                logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')
                assert False
            else:
                print(f"\nOn router |{dut_name}| message |{sys_msg}| NOT found in local log")
                logging.info(f'THEN test case result is |Passed|')  
                logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

@pytest.mark.base_feature
@pytest.mark.ztp
class ztpTests():
    """ Zero Touch Provisioning Test Suite
    """    

    def test_if_zerotouch_is_disabled_on_(self, dut, tests_definitions):
        """ Verify ztp is disabled

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is ZTP disabled on |{dut_name}| ')
        logging.info(f'GIVEN ZTP state is |{expected_output}|')

        actual_output = dut["output"][show_cmd]['json']['mode']

        print(f"\nOn router |{dut['name']}| ZTP process is in mode: |{actual_output}|")
        logging.info(f'WHEN ZTP state is |{actual_output}|')

        test_result = actual_output == expected_output
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert actual_output == expected_output

    def test_for_zerotouch_config_file_on_(self, dut, tests_definitions):
        """ Verify zerotoucn-config file is on flash

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is ZTP configuration file is on |{dut_name}| ')
        logging.info(f'GIVEN ZTP configuration file is |{expected_output}|')

        actual_output = ("zerotouch-config" in show_cmd_txt) is expected_output

        print(f"\nOn router |{dut_name}| ZTP configuration file is on flash: |{actual_output}|")
        logging.info(f'WHEN ZTP configuration file is |{actual_output}|')

        test_result = actual_output == expected_output
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert actual_output == expected_output

@pytest.mark.base_feature
@pytest.mark.ntp
class ntpTests():
    """ NTP Test Suite
    """  

    def test_if_ntp_is_synchronized_on_(self, dut, tests_definitions):
        """ Verify ntp is setup and working correctly

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is NTP synchronized on |{dut_name}| ')
        logging.info(f'GIVEN NTP synchronized is |{expected_output}|')

        actual_output = ("synchronised" in show_cmd_txt)

        print(f"\nOn router |{dut['name']}| NTP synchronized status is: |{actual_output}|")
        logging.info(f'WHEN NTP configuration file is |{actual_output}|')

        test_result = actual_output == expected_output
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert actual_output == expected_output

    def test_if_ntp_associated_with_peers_on_(self, dut, tests_definitions):
        """ Verify ntp peers are correct

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is NTP associations with peers on |{dut_name}| ')
        logging.info(f'GIVEN NTP associated are greater than or equal to |{expected_output}|')

        actual_output = dut["output"][show_cmd]['json']['peers']

        print(f"\nOn router |{dut_name}| has |{len(actual_output)}| NTP peer associations")
        logging.info(f'WHEN NTP associated peers fare |{len(actual_output)}|')

        test_result = len(actual_output) >= expected_output
        logging.info(f'THEN test case result is |{test_result}|')  
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert len(actual_output) >= expected_output

    @pytest.mark.ntp
    def test_if_process_is_running_on_(self, dut, tests_definitions):
        """ Verify ntp processes are running

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions, TEST_SUITE, test_case)

        expected_output = test_parameters["expected_output"]
        processes = test_parameters["processes"]
        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        actual_output = dut["output"][show_cmd]['json']['processes']

        process_list = []
        for process_num in actual_output:
            process_list.append(actual_output[process_num]["cmd"])

        for process in processes:
            logging.info(f'TEST is {process} running on |{dut_name}| ')
            logging.info(f'GIVEN {process} state is |{expected_output}|')

            results = [i for i in process_list if process in i]

            print(f"\nOn router |{dut_name}| has |{len(results)}| process for {process}")
            logging.info(f'WHEN {process} number is |{len(results)}|')

            test_result = len(results) >= expected_output
            logging.info(f'THEN test case result is |{test_result}|')  
            logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

            assert len(results) >= expected_output
