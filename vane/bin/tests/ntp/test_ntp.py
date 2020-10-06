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
@pytest.mark.ntp
class NTPTests():
    """ NTP Test Suite
    """

    def test_if_ntp_is_synchronized_on_(self, dut, tests_definitions):
        """ Verify ntp is synchronzied

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)
        tops.actual_output = dut["output"][tops.show_cmd]['json']['status']
        tops.test_result = tops.actual_output == tops.expected_output

        tops.output_msg = (f"\nOn router |{tops.dut_name}| NTP "
                           f"synchronised status is |{tops.actual_output}| "
                           f" correct status is |{tops.expected_output}|.\n")
        tops.comment = (f'TEST is NTP synchronized on |{tops.dut_name}|.\n'
                        f'GIVEN NTP synchronized is |{tops.expected_output}|'
                        '.\n'
                        f'WHEN NTP synchronized is |{tops.actual_output}|.\n'
                        f'THEN test case result is |{tops.test_result}|.\n'
                        f'OUTPUT of |{tops.show_cmd}| is:\n{tops.show_cmd_txt}'
                        '.\n')

        print(f"{tops.output_msg}\n{tops.comment}")

        tops.post_testcase()

        assert tops.actual_output == tops.expected_output

    def test_if_ntp_associated_with_peers_on_(self, dut, tests_definitions):
        """ Verify ntp peers are correct

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)
        tops.actual_output = dut["output"][tops.show_cmd]['json']['peers']
        tops.actual_output = len(tops.actual_output)

        tops.output_msg = (f"\nOn router |{tops.dut_name}| has "
                           f"|{tops.actual_output}| NTP peer associations, "
                           f"correct associations is |{tops.expected_output}|")

        tops.test_result = tops.actual_output >= tops.expected_output

        tops.comment = ('TEST is NTP associations with peers on '
                        f'|{tops.dut_name}|.\n'
                        'GIVEN associated are greater than or equal to '
                        f'|{tops.expected_output}|.\n'
                        f'WHEN NTP associated peers are |{tops.actual_output}|'
                        '.\n'
                        f'THEN test case result is |{tops.test_result}|.\n'
                        f'OUTPUT of |{tops.show_cmd}| is:\n{tops.show_cmd_txt}'
                        '.\n')

        print(f"{tops.output_msg}\n{tops.comment}")

        tops.post_testcase()

        assert tops.actual_output == tops.expected_output

    def test_if_process_is_running_on_(self, dut, tests_definitions):
        """ Verify ntp processes are running

            Args:
              dut (dict): Encapsulates dut details including name, connection
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)
        processes = tops.test_parameters["processes"]
        process_nums = dut["output"][tops.show_cmd]['json']['processes']

        process_list = []

        for process_num in process_nums:
            process_list.append(process_nums[process_num]["cmd"])

        for process in processes:
            results = [i for i in process_list if process in i]
            tops.actual_output = len(results)

            tops.output_msg = (f"\nOn router |{tops.dut_name}| has "
                               f"{tops.actual_output} NTP processes, "
                               " correct processes is equal to or greater "
                               f"|{tops.expected_output}|.\n")

            tops.test_result = tops.actual_output >= tops.expected_output

            tops.comment = (f'TEST is {process} running on |{tops.dut_name}|'
                            '.\n'
                            f'GIVEN {process} number is '
                            f'|{tops.expected_output}|.\n'
                            f'WHEN {process} number is '
                            f'|{tops.actual_output}|.\n'
                            f'THEN test case result is |{tops.test_result}|.\n'
                            f'OUTPUT of |{tops.show_cmd}| is:\n'
                            f'{tops.show_cmd_txt}.\n')
    
            print(f"{tops.output_msg}\n{tops.comment}")
    
            tops.post_testcase()

            assert tops.actual_output == tops.expected_output
