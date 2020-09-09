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
@pytest.mark.platform_status
@pytest.mark.logging
class LoggingTests():
    """ Logging Test Suite
    """

    def test_if_log_messages_appear_on_(self, dut, tests_definitions):
        """ Verify local log messages

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        sys_msgs = test_parameters["sys_msgs"]
        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']
        actual_output = show_cmd_txt

        for sys_msg in sys_msgs:
            logging.info(f'TEST for local log message {sys_msg} on '
                         f'|{dut_name}|')

            if sys_msg in show_cmd_txt:
                print(f"\nOn router |{dut_name}| message |{sys_msg}| found "
                      "in local log")
                logging.info('THEN test case result is |Failed|')
                logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')
                assert False
            else:
                print(f"\nOn router |{dut_name}| message |{sys_msg}| NOT "
                      "found in local log")
                logging.info('THEN test case result is |Passed|')
                logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')
                assert True
