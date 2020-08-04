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
import _ctypes
import tests_tools


logging.basicConfig(level=logging.INFO, filename='base_features.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info('Starting base_features.log file')


DUTS, DUTS_NAME = tests_tools.test_suite_setup()
TEST_SUITE = __file__


logging.info('Starting base feature test cases')
#@pytest.mark.usefixtures('test_suite_setup')
#@pytest.mark.parametrize("dut", duts, ids=['spine1', 'spine2'])
def test_assert_true():
#def test_assert_true(test_suite_setup):
    """ Prior to running any tests this test Validates that PyTest is working
        correct by verifying PyTest can assert True.
    """
    logging.info('Prior to running any tests this test Validates that PyTest '
                 'is working correct by verifying PyTest can assert True.')
    #print('\n\n>>>>>>>>>>>>>>> ', definitions)
    #print('hello world')
    #test_report = _ctypes.PyObj_FromPtr(int(definitions))
    #test_report = id(cmdopt)
    #print(dir(test_report))
    assert True


@pytest.mark.parametrize("dut", DUTS, ids=DUTS_NAME)
@pytest.mark.xfail
def test_dir(dut):
    """ Verify filesystem is correct

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "dir"
    eos_dir = dut["output"][show_cmd]["text"]

    print(f"\nNO AUTOMATED TEST.  MUST TEST MANUALLY")
    print(f"\nOn router |{dut['name']}|: dir:\n{eos_dir}")

    assert False


@pytest.mark.parametrize("dut", DUTS, ids=DUTS_NAME)
def test_is_terminattr_daemon_running_on_(dut, tests_parameters):
    """ Verify TerminAttr daemon is running

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    test_case = inspect.currentframe().f_code.co_name
    test_parameters = tests_tools.get_parameters(tests_parameters, TEST_SUITE, test_case)

    daemon_state = test_parameters["expected_output"]
    dut_name = dut['name']
    logging.info(f'TEST is terminattr daemon running on |{dut_name}|')
    logging.info(f'GIVEN expected terminattr​ running state: |{daemon_state}|')

    show_cmd = "show daemon"
    eos_daemon = \
        dut["output"][show_cmd]['json']['daemons']['TerminAttr']['running']
    logging.info(f'WHEN terminattr​ device running state is |{eos_daemon}|')    

    test_result = eos_daemon is daemon_state
    logging.info(f'THEN test case result is |{test_result}|')  

    print(f"\nOn router |{dut_name}|: TerminAttr daemon running is "
          f"|{eos_daemon}|")
    assert eos_daemon is daemon_state


@pytest.mark.parametrize("dut", DUTS, ids=DUTS_NAME)
def test_is_daemon_enabled_on_(dut, tests_parameters):
    """ Verify TerminAttr daemon is enabled

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    test_case = inspect.currentframe().f_code.co_name
    test_parameters = tests_tools.get_parameters(tests_parameters, TEST_SUITE, test_case)

    daemon_state = test_parameters["expected_output"]
    dut_name = dut['name']
    logging.info(f'TEST is terminattr daemon enabled on |{dut_name}|')
    logging.info(f'GIVEN expected terminattr​ enabled state: |{daemon_state}|')

    show_cmd = "show daemon"
    show_cmd_txt = dut["output"][show_cmd]['text']
    eos_daemon = \
        dut["output"][show_cmd]['json']['daemons']['TerminAttr']['enabled']
    logging.info(f'WHEN terminattr​ device enabled state is |{eos_daemon}|')    

    test_result = eos_daemon is daemon_state
    logging.info(f'THEN test case result is |{test_result}|')
    logging.info(f'OUTPUT of |{show_cmd}|:\n\n{show_cmd_txt}') 

    print(f"\nOn router |{dut['name']}|: TerminAttr daemon enabled is "
          f"|{eos_daemon}| and expected value is |{daemon_state}|.\nTest "
          f"result is {test_result}")
    assert eos_daemon is True


@pytest.mark.parametrize("dut", DUTS, ids=DUTS_NAME)
def test_is_aws_extension_installed_on_(dut, tests_parameters):
    """ Verify awslogs extension is installed and not erroring

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    test_case = inspect.currentframe().f_code.co_name
    test_parameters = tests_tools.get_parameters(tests_parameters, TEST_SUITE, test_case)

    expected_output = test_parameters["expected_output"]
    dut_name = dut['name']
    logging.info(f'TEST is awslogs extension installed on |{dut_name}|')
    logging.info(f'GIVEN expected awslog extension status: |{expected_output}|')

    show_cmd = test_parameters["show_cmd"]
    show_cmd_txt = dut["output"][show_cmd]['text']

    if 'awslogs.swix' in dut["output"][show_cmd]['json']['extensions']:

        eos_extension = dut["output"][show_cmd]['json']['extensions\
']['awslogs.swix']['status']
        print(f"\nOn router |{dut['name']}| TerminAttr-1.6.1-1.swix extension is \
|{eos_extension}|")
    else:
        print(f"\nOn router |{dut['name']}| TerminAttr-1.6.1-1.swix extension \
            is |NOT installed|")
        assert False

    assert eos_extension == 'installed'


# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_extensions_status(dut):
#     """ Verify TerminAttr extension is installed and not erroring
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show extensions"
# 
#     if 'TerminAttr-1.6.1-1.swix' in dut["output"][show_cmd]['json\
# ']['extensions']:
# 
#         eos_extension = dut["output"][show_cmd]['json']['extensions\
# ']['TerminAttr-1.6.1-1.swix']['status']
#         print(f"\nOn router |{dut['name']}| TerminAttr-1.6.1-1.swix extension is \
# |{eos_extension}|")
#     else:
#         print(f"\nOn router |{dut['name']}| TerminAttr-1.6.1-1.swix extension \
#             is |NOT installed|")
#         assert False
# 
#     assert eos_extension == 'installed'
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_extensions_error(dut):
#     """ Verify TerminAttr extension is installed and not erroring
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show extensions"
# 
#     if 'TerminAttr-1.6.1-1.swix' in dut["output"][show_cmd]['json\
# ']['extensions']:
#         eos_extension = dut["output"][show_cmd]['json']['extensions\
# ']['TerminAttr-1.6.1-1.swix']['error']
#         print(f"\nOn router |{dut['name']}| TerminAttr-1.6.1-1.swix extension error is \
# |{eos_extension}|")
#     else:
#         print(f"\nOn router |{dut['name']}| TerminAttr-1.6.1-1.swix extension is \
# |NOT installed|")
#         assert False
# 
#     assert eos_extension is False
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_show_username(dut):
#     """ Verify username is set correctly
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show running-config section username"
#     eos_username = dut["output"][show_cmd]['text']
# 
#     if "admin" in eos_username:
#         print(f"\nOn router |{dut['name']}| |admin| username is |configured|")
#     else:
#         print(f"\nOn router |{dut['name']}| |admin| username is \
# |NOT configured|")
# 
#     assert ("admin" in eos_username) is True
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_show_tacacs(dut):
#     """ Verify tacacs is working correctly
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     test_show_tacacs_sent(dut)
#     test_show_tacacs_received(dut)
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_show_tacacs_sent(dut):
#     """ Verify tacacs is working correctly
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show tacacs"
#     eos_messages_sent_1 = \
#         dut["output"][show_cmd]['json']['tacacsServers'][0]['messagesSent']
# 
#     show_output, _ = common_nrfu_infra.return_show_cmd_output(
#         show_cmd, dut, TEST_SUITE, inspect.stack()[0][3])
#     eos_messages_sent_2 = \
#         show_output[0]['result']['tacacsServers'][0]['messagesSent']
# 
#     if eos_messages_sent_1 < eos_messages_sent_2:
#         print(f"\nOn router |{dut['name']}| TACACS messages2 sent: |{eos_messages_sent_2}| \
# increments from TACACS messages1 sent: |{eos_messages_sent_1}|")
#     else:
#         print(f"\nOn router |{dut['name']}| TACACS messages2 sent: |{eos_messages_sent_2}| \
# doesn't increments from TACACS messages1 sent: |{eos_messages_sent_1}|")
# 
#     assert eos_messages_sent_1 < eos_messages_sent_2
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_show_tacacs_received(dut):
#     """ Verify tacacs is working correctly
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show tacacs"
#     eos_messages_received_1 = \
#         dut["output"][show_cmd]['json']['tacacsServers'][0]['messagesReceived']
# 
#     show_output, _ = common_nrfu_infra.return_show_cmd_output(
#         show_cmd, dut, TEST_SUITE, inspect.stack()[0][3])
#     eos_messages_received_2 = \
#         show_output[0]['result']['tacacsServers'][0]['messagesReceived']
# 
#     if eos_messages_received_1 < eos_messages_received_2:
#         print(f"\nOn router |{dut['name']}| TACACS messages2 received: \
#             |{eos_messages_received_2}| increments from TACACS messages1 \
#             received: |{eos_messages_received_1}|")
#     else:
#         print(f"\nOn router |{dut['name']}| TACACS messages2 received: \
#             |{eos_messages_received_2}| doesn't increments from TACACS \
#             messages1 received: |{eos_messages_received_1}|")
# 
#     assert eos_messages_received_1 < eos_messages_received_2
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_counters(dut):
#     """ Verify AAA counters are working correctly
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show aaa counters"
#     eos_authorization_allowed_1 = \
#         dut["output"][show_cmd]['json']['authorizationAllowed']
# 
#     show_output, _ = common_nrfu_infra.return_show_cmd_output(
#         show_cmd, dut, TEST_SUITE, inspect.stack()[0][3])
#     eos_authorization_allowed_2 = \
#         show_output[0]['result']['authorizationAllowed']
# 
#     if eos_authorization_allowed_1 < eos_authorization_allowed_2:
#         print(f"\nOn router |{dut['name']}| AAA authorization allowed \
# messages2: |{eos_authorization_allowed_2}| increments from AAA authorization \
# allowed message1: |{eos_authorization_allowed_1}|")
#     else:
#         print(f"\nOn router |{dut['name']}| AAA authorization allowed \
# messages2: |{eos_authorization_allowed_2}| doesn't increments from AAA \
# authorization allowed message1: |{eos_authorization_allowed_1}|")
# 
#     assert eos_authorization_allowed_1 < eos_authorization_allowed_2
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_sessions(dut):
#     """ Verify AAA session logging is working by identifying eapi connection
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show users detail"
#     eos_non_interactives = dut["output"][show_cmd]['json']['nonInteractives']
#     aaa_flag = False
# 
#     for non_interactive in eos_non_interactives:
#         if eos_non_interactives[non_interactive]['service'] == 'commandApi':
#             print(f"\nOn router |{dut['name']}| identified eAPi AAA session: \
# |{eos_non_interactives[non_interactive]['service']}|")
#             aaa_flag = True
# 
#     if not aaa_flag:
#         print(f"\nOn router |{dut['name']}| did NOT identified eAPi AAA session: \
# |{eos_non_interactives[non_interactive]['service']}|")
# 
#     for non_interactive in eos_non_interactives:
#         assert eos_non_interactives[non_interactive]['service'] == 'commandApi'
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_method_list_all(dut):
#     """ Verify AAA method-lists are correctly set
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     test_aaa_method_list_all_author_priv15(dut)
#     test_aaa_method_list_all_author_exec(dut)
#     test_aaa_method_list_all_authen_default(dut)
#     test_aaa_method_list_all_authen_login(dut)
#     test_aaa_method_list_all_authen_dot1x(dut)
#     test_aaa_method_list_all_authen_enable(dut)
#     test_aaa_method_list_all_acct_system(dut)
#     test_aaa_method_list_all_acct_exec(dut)
#     test_aaa_method_list_all_acct_priv15(dut)
#     test_aaa_method_list_all_acct_dot1x(dut)
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_method_list_all_author_priv15(dut):
#     """ Verify AAA method-lists are correctly set
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show aaa methods all"
#     eos_auth_priv15_methods = \
#         dut["output"][show_cmd]['json']['authorization']['commandsAuthzMethods\
# ']['privilege0-15']['methods']
# 
#     print(f"\nOn router |{dut['name']}| AAA authorization methods for \
# privilege0-15: |{eos_auth_priv15_methods}|")
# 
#     assert eos_auth_priv15_methods == ['group tacacs+', 'local']
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_method_list_all_author_exec(dut):
#     """ Verify AAA method-lists are correctly set
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show aaa methods all"
#     eos_auth_exec_methods = \
#         dut["output"][show_cmd]['json']['authorization']['execAuthzMethods\
# ']['exec']['methods']
# 
#     print(f"\nOn router |{dut['name']}| AAA authorization methods for exec: \
# |{eos_auth_exec_methods}|")
# 
#     assert eos_auth_exec_methods == ['group tacacs+', 'local']
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_method_list_all_authen_default(dut):
#     """ Verify AAA method-lists are correctly set
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show aaa methods all"
#     auth_default_methods = \
#         dut["output"][show_cmd]['json']['authentication']['loginAuthenMethods\
# ']['default']['methods']
# 
#     print(f"\nOn router |{dut['name']}| AAA authentication methods for \
# default login: |{auth_default_methods}|")
# 
#     assert auth_default_methods == ['group tacacs+', 'local']
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_method_list_all_authen_login(dut):
#     """ Verify AAA method-lists are correctly set
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show aaa methods all"
#     eos_auth_local_methods = \
#         dut["output"][show_cmd]['json']['authentication']['loginAuthenMethods\
# ']['login']['methods']
# 
#     print(f"\nOn router |{dut['name']}| AAA authentication methods for login: \
# |{eos_auth_local_methods}|")
# 
#     assert eos_auth_local_methods == ['local']
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_method_list_all_authen_dot1x(dut):
#     """ Verify AAA method-lists are correctly set
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show aaa methods all"
#     eos_auth_dot1x_methods = \
#         dut["output"][show_cmd]['json']['authentication']['dot1xAuthenMethods\
# ']['default']['methods']
# 
#     print(f"\nOn router |{dut['name']}| AAA authentication methods for \
# dot1x default: |{eos_auth_dot1x_methods}|")
# 
#     assert eos_auth_dot1x_methods == []
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_method_list_all_authen_enable(dut):
#     """ Verify AAA method-lists are correctly set
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show aaa methods all"
#     eos_auth_enable_methods = \
#         dut["output"][show_cmd]['json']['authentication']['enableAuthenMethods\
# ']['default']['methods']
# 
#     print(f"\nOn router |{dut['name']}| AAA authentication methods for \
# enable default: |{eos_auth_enable_methods}|")
# 
#     assert eos_auth_enable_methods == ['group tacacs+', 'local']
# 
# 
# @pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
# def test_aaa_method_list_all_acct_system(dut):
#     """ Verify AAA method-lists are correctly set
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     show_cmd = "show aaa methods all"
#     eos_acct_system_methods = \
#         dut["output"][show_cmd]['json']['accounting']['systemAcctMethods\
# ']['system']['defaultMethods']
# 
#     print(f"\nOn router |{dut['name']}| AAA accounting methods for default: \
# |{eos_acct_system_methods}|")
# 
#     assert eos_acct_system_methods == ['logging']
# 
# 
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
# def test_management_api_http_cmds(dut):
#     """ Verify management api is running, httpsserver is enabled on port 443,
#         httpserver is not running, and local httpserver is not running
# 
#          Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     test_management_api_http_cmds_https_server_running(dut)
#     test_management_api_http_cmds_https_server_port(dut)
#     test_management_api_http_cmds_enabled(dut)
#     test_management_api_http_cmds_http_server_running(dut)
#     test_management_api_http_cmds_local_http_server_running(dut)
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
# def test_show_ntp(dut):
#     """ Verify ntp is setup and working correctly
# 
#         Args:
#           dut (dict): Encapsulates dut details including name, connection
#     """
# 
#     test_show_ntp_status(dut)
#     test_show_ntp_associations(dut)
#     test_ntp_process(dut)
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