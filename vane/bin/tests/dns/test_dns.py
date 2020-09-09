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
@pytest.mark.dns
class DNSTests():
    """ DNS Test Suite
    """

    def test_if_dns_resolves_on_(self, dut, tests_definitions):
        """ Verify DNS is running by performing pings and verifying name resolution

             Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        urls = test_parameters["urls"]
        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        dut_conn = dut['connection']

        for url in urls:
            show_cmd = f"ping {url}"
            logging.info(f'TEST can |{dut_name}| resolve {url}')
            logging.info(f'GIVEN URL is |{url}|')
            logging.info('WHEN exception is |Name or service not known| '
                         'string')

            show_cmd_txt = dut_conn.run_commands(show_cmd, encoding='text')
            show_cmd_txt = show_cmd_txt[0]['output']
            actual_output = show_cmd_txt

            if 'Name or service not known' in show_cmd_txt:
                print(f"\nOn router |{dut_name}| DNS resolution |Failed| for "
                      f"{url}")
                logging.info('THEN test case result is |Failed|')
                logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

                assert False
            else:
                print(f"\nOn router |{dut_name}| DNS resolution |Passed| for "
                      f"{url}")
                logging.info('THEN test case result is |Passed|')
                logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

                assert True
