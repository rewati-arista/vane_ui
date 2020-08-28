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

import inspect
import logging
import pytest
import tests_tools


TEST_SUITE = __file__
LOG_FILE = {"parameters": {"show_log": "show_output.log"}}


@pytest.mark.nrfu
@pytest.mark.base_feature
@pytest.mark.api
class APITests():
    """ API Test Suite
    """

    def test_if_management_https_api_server_is_running_on_(self,
                                                           dut,
                                                           tests_definitions):
        """ Verify management api https server is running

             Args:
              dut (dict): Encapsulates dut details including name, connection
              tests_definitions (dict): Test parameters
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        dut_name = dut['name']
        expected_output = test_parameters["expected_output"]

        logging.info(f'TEST is HTTPS API running on |{dut_name}| ')
        logging.info(f'GIVEN HTTPS API state is |{expected_output}|')

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        ptr = dut["output"][show_cmd]['json']
        actual_output = ptr['httpsServer']['running']

        print(f"\nOn router |{dut_name}| HTTPS Server is running state: "
              f"|{expected_output}|")
        logging.info(f'WHEN HTTPS API state is |{actual_output}|')

        test_result = expected_output == actual_output
        logging.info(f'THEN test case result is |{test_result}|')
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert expected_output == actual_output

    def test_if_management_https_api_server_port_is_correct_on_(self,
                                                                dut,
                                                                tests_definitions):
        """ Verify https server is enabled on port 443

             Args:
              dut (dict): Encapsulates dut details including name, connection
              tests_definitions (dict): Test parameters
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        dut_name = dut['name']
        expected_output = test_parameters["expected_output"]

        logging.info(f'TEST is HTTPS API port on |{dut_name}| ')
        logging.info(f'GIVEN HTTPS API port is |{expected_output}|')

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        actual_output = dut["output"][show_cmd]['json']['httpsServer']['port']

        print(f"\nOn router |{dut_name}| HTTPS Server is running on port: "
              f"|{actual_output}|")
        logging.info(f'WHEN HTTPS API port is |{actual_output}|')

        test_result = expected_output == actual_output
        logging.info(f'THEN test case result is |{test_result}|')
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert actual_output == expected_output

    def test_if_management_https_api_server_is_enabled_on_(self,
                                                           dut,
                                                           tests_definitions):
        """ Verify management api https server is enabled

             Args:
              dut (dict): Encapsulates dut details including name, connection
              tests_definitions (dict): Test parameters
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        dut_name = dut['name']
        expect_output = test_parameters["expected_output"]

        logging.info(f'TEST is HTTPS API enabled on |{dut_name}| ')
        logging.info(f'GIVEN HTTPS API enabled is |{expect_output}|')

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        actual_output = dut["output"][show_cmd]['json']['enabled']

        print("\nOn router |{dut_name}| API is enabled state: "
              f"|{actual_output}|")
        logging.info(f'WHEN HTTPS API enabled is |{actual_output}|')

        test_result = expect_output == actual_output
        logging.info(f'THEN test case result is |{test_result}|')
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert expect_output == actual_output

    def test_if_management_http_api_server_is_running_on_(self,
                                                          dut,
                                                          tests_definitions):
        """ Verify management api http server is not running

             Args:
              dut (dict): Encapsulates dut details including name, connection
              tests_definitions (dict): Test parameters
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        dut_name = dut['name']
        expect_output = test_parameters["expected_output"]

        logging.info(f'TEST is HTTP API running on |{dut_name}| ')
        logging.info(f'GIVEN HTTP API state is |{expect_output}|')

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        ptr = dut["output"][show_cmd]['json']
        actual_output = ptr['httpServer']['running']

        print("\nOn router |{dut_name}| HTTP Server is running state: "
              f"|{actual_output}|")
        logging.info(f'WHEN HTTP API state is |{actual_output}|')

        test_result = expect_output == actual_output
        logging.info(f'THEN test case result is |{test_result}|')
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert expect_output is actual_output

    def test_if_management_local_http_api_server_is_running_on_(self,
                                                                dut,
                                                                tests_definitions):
        """ Verify management api local httpserver is not running

             Args:
              dut (dict): Encapsulates dut details including name, connection
              tests_definitions (dict): Test parameters
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        dut_name = dut['name']
        expect_output = test_parameters["expected_output"]

        logging.info(f'TEST is local HTTP API running on |{dut_name}| ')
        logging.info(f'GIVEN local HTTP API state is |{expect_output}|')

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        actual_output = \
            dut["output"][show_cmd]['json']['localHttpServer']['running']

        print(f"\nOn router |{dut['name']}| Local HTTP Server is running "
              f"state: |{expect_output}|")
        logging.info(f'WHEN HTTP API state is |{actual_output}|')

        test_result = expect_output == actual_output
        logging.info(f'THEN test case result is |{test_result}|')
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert expect_output is actual_output
