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

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)
        show_cmds = []

        urls = tops.test_parameters["urls"]
        dut_conn = dut['connection']

        for url in urls:
            show_cmd = f"ping {url}"
            show_cmds.append(show_cmd)

            show_cmd_txt = dut_conn.run_commands(show_cmd, encoding='text')
            show_cmd_txt = show_cmd_txt[0]['output']

            tops.actual_output = 'Name or service not known' not in show_cmd_txt
            tops.test_result = tops.actual_output is tops.expected_output

            tops.output_msg += (f"\nOn router |{tops.dut_name}|, DNS resolution is"
                                f"|{tops.test_result}| for {url}.\n")

            tops.comment += (f'TEST can |{tops.dut_name}| resolve |{url}|.\n'
                             f'GIVEN URL is |{url}|.\n'
                             'WHEN exception is |Name or service not known| '
                             'string.\n'
                             f'THEN test case result is |{tops.test_result}|.\n'
                             f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}.\n')

            tops.actual_results.append(tops.actual_output)
            tops.expected_results.append(tops.expected_output)

        print(f"{tops.output_msg}\n{tops.comment}")

        tops.show_cmd = show_cmds
        tops.actual_output, tops.expected_output = tops.actual_results, tops.expected_results
        tops.post_testcase()

        assert tops.actual_results == tops.expected_results
