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
@pytest.mark.l2_protocols
@pytest.mark.lldp
class LldpTests():
    """ LLDP Test Suite
    """

    def test_if_lldp_rx_is_enabled_on_(self, dut, tests_definitions):
        """  Verify LLDP receive is enabled on interesting interfaces

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        (test_parameters,
         expected_output,
         interfaces_list,
         dut_name,
         show_cmd_txt,
         show_cmd) = tests_tools.pre_testcase(tests_definitions,
                                              TEST_SUITE,
                                              dut)

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['lldpInterfaces']
            actual_output = int_ptr[interface_name]['rxEnabled']

            output_msg = (f"On interface |{interface_name}|: interface LLDP"
                          f"rxEnabled is in state |{actual_output}|, correct "
                          f"LLDP rxEnabled state is |{expected_output}|")

            test_result = actual_output == expected_output
            comment = (f'TEST if interface |{interface_name}| LLDP receive is '
                       f'enabled on |{dut_name}|.\nGIVEN LLDP receive state '
                       f'is |{expected_output}|.\nWHEN LLDP receive state is '
                       f'|{actual_output}|.\nTHEN test case result is '
                       f'|{test_result}|.\nOUTPUT of |{show_cmd}| is:\n\n'
                       f'{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output == expected_output

    def test_if_lldp_tx_is_enabled_on_(self, dut, tests_definitions):
        """  Verify LLDP transmit is enabled on interesting interfaces

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        (test_parameters,
         expected_output,
         interfaces_list,
         dut_name,
         show_cmd_txt,
         show_cmd) = tests_tools.pre_testcase(tests_definitions,
                                              TEST_SUITE,
                                              dut)

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['lldpInterfaces']
            actual_output = int_ptr[interface_name]['rxEnabled']

            output_msg = (f"On interface |{interface_name}|: interface LLDP"
                          f"rxEnabled is in state |{actual_output}|, correct "
                          f"LLDP txEnabled state is |{expected_output}|")

            test_result = actual_output == expected_output

            comment = (f'TEST if interface |{interface_name}| LLDP transmit '
                       f'is enabled on |{dut_name}|.\nGIVEN LLDP transmit '
                       f'state is |{expected_output}|.\nWHEN LLDP receive '
                       f'state is |{actual_output}|.\nTHEN test case result '
                       f'is |{test_result}|.\nOUTPUT of |{show_cmd}| is:\n\n'
                       f'{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output == expected_output

    def test_if_lldp_system_name_is_correct_on_(self, dut, tests_definitions):
        """  Verify show lldp local-info hostname is the system's name

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        (test_parameters,
         expected_output,
         _, dut_name,
         show_cmd_txt,
         show_cmd) = tests_tools.pre_testcase(tests_definitions,
                                              TEST_SUITE,
                                              dut)

        test_parameters['expected_output'] = expected_output = dut_name
        actual_output = dut["output"][show_cmd]["json"]['systemName']

        output_msg = (f"On router |{dut_name}|: the LLDP local-info system "
                      f"name is |{actual_output}|, correct name is "
                      f"|{expected_output}|")
        test_result = actual_output == expected_output

        comment = ('TEST if lldp system name matches hostname on dut '
                   f'{dut_name}.\n'
                   f'GIVEN hostname is |{expected_output}|.\n'
                   f'WHEN LLDP system name is |{actual_output}|.\n'
                   f'THEN test case result is |{test_result}|.\n'
                   f'OUTPUT of |{show_cmd}| is:\n\n{show_cmd_txt}')

        print(f"{output_msg}\n{comment}")

        tests_tools.post_testcase(test_parameters, comment, test_result,
                                  output_msg, actual_output, dut_name)
        assert actual_output == expected_output
