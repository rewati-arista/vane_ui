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
@pytest.mark.ztp
class ZTPTests():
    """ Zero Touch Provisioning Test Suite
    """

    def test_if_zerotouch_is_disabled_on_(self, dut, tests_definitions):
        """ Verify ztp is disabled

            Args:
              dut (dict): Encapsulates dut details including name, connection
              tests_definitions (dict): Test parameters
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is ZTP disabled on |{dut_name}| ')
        logging.info(f'GIVEN ZTP state is |{expected_output}|')

        actual_output = dut["output"][show_cmd]['json']['mode']

        print(f"\nOn router |{dut['name']}| ZTP process is in mode: "
              f"|{actual_output}|")
        logging.info(f'WHEN ZTP state is |{actual_output}|')

        test_result = actual_output == expected_output
        logging.info(f'THEN test case result is |{test_result}|')
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert actual_output == expected_output

    def test_for_zerotouch_config_file_on_(self, dut, tests_definitions):
        """ Verify zerotoucn-config file is on flash

            Args:
              dut (dict): Encapsulates dut details including name, connection
              tests_definitions (dict): Test parameters
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is ZTP configuration file is on |{dut_name}| ')
        logging.info(f'GIVEN ZTP configuration file is |{expected_output}|')

        actual_output = ("zerotouch-config" in show_cmd_txt) is expected_output

        print(f"\nOn router |{dut_name}| ZTP configuration file is on flash: "
              f"|{actual_output}|")
        logging.info(f'WHEN ZTP configuration file is |{actual_output}|')

        test_result = actual_output == expected_output
        logging.info(f'THEN test case result is |{test_result}|')
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

        assert actual_output == expected_output
