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
