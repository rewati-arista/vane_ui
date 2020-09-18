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
@pytest.mark.interface_baseline_health
@pytest.mark.interface
class InterfaceStatusTests():
    """ Interface Status Test Suite
    """

    def test_if_intf_protocol_status_is_connected_on_(self,
                                                      dut,
                                                      tests_definitions):
        """ Verify the interfaces of interest protocol statuses are up

            Args:
                dut (dict): Encapsulates dut details including name, connection
                tests_definitions (dict): Test parameters
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaceStatuses']
            actual_output = int_ptr[interface_name]['lineProtocolStatus']

            output_msg = (f"On interface |{interface_name}|: interface link "
                          f"line protocol status is set to: |{actual_output}|"
                          f", correct state is |{expected_output}|")

            test_result = actual_output == expected_output
            comment = (f'TEST if interface |{interface_name}| link prootocol '
                       f'statuses on |{dut_name}|.\nGIVEN interface '
                       f'status is |{expected_output}|.\nWHEN interface '
                       f'status is |{actual_output}|.\nTHEN test case result '
                       f'is |{test_result}|.\nOUTPUT of |{show_cmd}| is:'
                       f'\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output == expected_output

    def test_if_intf_link_status_is_connected_on_(self,
                                                  dut,
                                                  tests_definitions):
        """ Verify the interfaces of interest link statuses are up

            Args:
                dut (dict): Encapsulates dut details including name, connection
                tests_definitions (dict): Test parameters
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:

            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaceStatuses']
            actual_output = int_ptr[interface_name]['linkStatus']

            print(f"  - On interface |{interface_name}|: interface link line "
                  f"protocol status is set to: |{actual_output}|, correct "
                  f"state is |{expected_output}|")

            output_msg = (f"On interface |{interface_name}|: interface link "
                          f" status is set to: |{actual_output}|"
                          f", correct state is |{expected_output}|")

            test_result = actual_output == expected_output
            comment = (f'TEST if interface |{interface_name}| link '
                       f'status on |{dut_name}|.\nGIVEN interface '
                       f'status is |{expected_output}|.\nWHEN interface '
                       f'status is |{actual_output}|.\nTHEN test case result '
                       f'is |{test_result}|.\nOUTPUT of |{show_cmd}| is:'
                       f'\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output == expected_output


@pytest.mark.nrfu
@pytest.mark.interface_baseline_health
@pytest.mark.interface
class InterfacePhyTests():
    """ Interface Status Test Suite
    """

    def test_if_intf_phy_status_connected_on_(self,
                                              dut,
                                              tests_definitions):
        """ Verify the interfaces of interest physical state is link up

            Args:
                dut (dict): Encapsulates dut details including name, connection
                tests_definitions (dict): Test parameters
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        veos_bool = tests_tools.verify_veos(dut)

        if not veos_bool:
            print(f"\nOn router |{dut_name}|:")

            for interface in interfaces_list:
                interface_name = interface['interface_name'].replace(" ", "")
                int_ptr = dut["output"][show_cmd]['json']['interfacePhyStatuses']
                raw_output = int_ptr[interface_name]['phyStatuses'][0]['text']

                split_output = raw_output.split('\n')

                for line_output in split_output:
                    if "PHY state" in line_output:
                        actual_output = line_output.split()[2]

                        output_msg = (f"On interface |{interface_name}|: "
                                      f"physical detail PHY state is set to: "
                                      f"|{actual_output}|, correct state is "
                                      f"|{expected_output}|")

                        test_result = actual_output == expected_output

                        comment = (f'TEST if interface |{interface_name}| '
                                   f'physical status on |{dut_name}|.\nGIVEN '
                                   f'interface status is |{expected_output}|.'
                                   '\nWHEN interface status is '
                                   f'|{actual_output}|.\nTHEN test case '
                                   f'result is |{test_result}|.\nOUTPUT of '
                                   f'|{show_cmd}| is:\n\n{show_cmd_txt}')

                        print(f"  - {output_msg}\n{comment}")

                        tests_tools.post_testcase(test_parameters, comment,
                                                  test_result, output_msg,
                                                  actual_output, dut_name)

                        assert actual_output == expected_output
        else:
            comment = f"{dut_name} is vEOS instance.  Test is not valid."
            test_result, output_msg, actual_output = True, None, None
            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)


@pytest.mark.nrfu
@pytest.mark.interface_baseline_health
@pytest.mark.interface
class InterfaceCountersTests():
    """ Interface Status Test Suite
    """

    def test_if_intf_counters_has_input_errors_on_(self,
                                                   dut,
                                                   tests_definitions):
        """ Verify the interfaces of interest does not have input errors

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaceErrorCounters']
            actual_output = int_ptr[interface_name]['inErrors']

            output_msg = (f"On interface |{interface_name}|: interface "
                          f"counter errors has |{actual_output}| inErrors"
                          f", correct state is |{expected_output}|")

            test_result = actual_output == expected_output
            comment = (f'TEST if interface |{interface_name}| counters have '
                       f'input errors on |{dut_name}|.\nGIVEN interface input '
                       f'errors is |{expected_output}|.\nWHEN interface input'
                       f'errors is |{actual_output}|.\nTHEN test case result '
                       f'is |{test_result}|.\nOUTPUT of |{show_cmd}| is:'
                       f'\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output <= expected_output

    def test_if_intf_counters_has_output_errors_on_(self,
                                                    dut,
                                                    tests_definitions):
        """ Verify the interfaces of interest does not have output errors

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaceErrorCounters']
            actual_output = int_ptr[interface_name]['outErrors']

            output_msg = (f"On interface |{interface_name}|: interface "
                          f"counter errors has |{actual_output}| outErrors"
                          f", correct state is |{expected_output}|")

            test_result = actual_output == expected_output
            comment = (f'TEST if interface |{interface_name}| has output '
                       f'errors on |{dut_name}|.\nGIVEN interface output '
                       f'errors is |{expected_output}|.\nWHEN interface output'
                       f'errors is |{actual_output}|.\nTHEN test case result '
                       f'is |{test_result}|.\nOUTPUT of |{show_cmd}| is:'
                       f'\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output <= expected_output

    def test_if_intf_counters_has_frame_too_short_errors_on_(self,
                                                             dut,
                                                             tests_definitions):
        """  Verify the interfaces of interest have no frameTooShorts errors

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaceErrorCounters']
            actual_output = int_ptr[interface_name]['frameTooShorts']

            output_msg = (f"On interface |{interface_name}|: interface "
                          f"counter errors has |{actual_output}| "
                          "frameTooShorts, correct state is "
                          f"|{expected_output}|")

            test_result = actual_output == expected_output
            comment = (f'TEST if interface |{interface_name}| counters have '
                       f'frameTooShorts errors on |{dut_name}|.\nGIVEN '
                       'interface frameTooShorts errors is '
                       f'|{expected_output}|.\nWHEN interface frameTooShorts'
                       f'errors is |{actual_output}|.\nTHEN test case result '
                       f'is |{test_result}|.\nOUTPUT of |{show_cmd}| is:'
                       f'\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output <= expected_output

    def test_if_intf_counters_has_frame_too_long_errors_on_(self,
                                                            dut,
                                                            tests_definitions):
        """  Verify the interfaces of interest have no frameLongShorts errors

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaceErrorCounters']
            actual_output = int_ptr[interface_name]['frameTooLongs']

            output_msg = (f"On interface |{interface_name}|: interface "
                          f"counter errors has |{actual_output}| "
                          "frameTooLongs, correct state is "
                          f"|{expected_output}|")

            test_result = actual_output == expected_output
            comment = (f'TEST if interface |{interface_name}| counters have '
                       f'frameTooLongs errors on |{dut_name}|.\nGIVEN '
                       'interface frameTooLongs errors is '
                       f'|{expected_output}|.\nWHEN interface frameTooLongs'
                       f'errors is |{actual_output}|.\nTHEN test case result '
                       f'is |{test_result}|.\nOUTPUT of |{show_cmd}| is:'
                       f'\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output <= expected_output

    def test_if_intf_counters_has_fcs_errors_on_(self,
                                                 dut,
                                                 tests_definitions):
        """  Verify the interfaces of interest have no fcsErrors errors

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaceErrorCounters']
            actual_output = int_ptr[interface_name]['fcsErrors']

            output_msg = (f"On interface |{interface_name}|: interface "
                          f"counter errors has |{actual_output}| "
                          "fcsErrors, correct state is "
                          f"|{expected_output}|")

            test_result = actual_output == expected_output
            comment = (f'TEST if interface |{interface_name}| counters have '
                       f'fcsErrors errors on |{dut_name}|.\nGIVEN '
                       'interface fcsErrors errors is '
                       f'|{expected_output}|.\nWHEN interface fcsErrors'
                       f'errors is |{actual_output}|.\nTHEN test case result '
                       f'is |{test_result}|.\nOUTPUT of |{show_cmd}| is:'
                       f'\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output <= expected_output

    def test_if_intf_counters_has_alignment_errors_on_(self,
                                                       dut,
                                                       tests_definitions):
        """  Verify the interfaces of interest have no alignmentErrors errors

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaceErrorCounters']
            actual_output = int_ptr[interface_name]['alignmentErrors']

            output_msg = (f"On interface |{interface_name}|: interface "
                          f"counter errors has |{actual_output}| "
                          "alignmentErrors, correct state is "
                          f"|{expected_output}|")

            test_result = actual_output == expected_output
            comment = (f'TEST if interface |{interface_name}| counters have '
                       f'alignmentErrors errors on |{dut_name}|.\nGIVEN '
                       'interface alignmentErrors errors is '
                       f'|{expected_output}|.\nWHEN interface alignmentErrors'
                       f'errors is |{actual_output}|.\nTHEN test case result '
                       f'is |{test_result}|.\nOUTPUT of |{show_cmd}| is:'
                       f'\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output <= expected_output

    def test_if_intf_counters_has_symbol_errors_on_(self,
                                                    dut,
                                                    tests_definitions):
        """  Verify the interfaces of interest have no alignmentErrors errors

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaceErrorCounters']
            actual_output = int_ptr[interface_name]['symbolErrors']

            output_msg = (f"On interface |{interface['interface_name']}|: "
                          f"interface counter errors has |{actual_output}| "
                          "symbolErrors, correct state is "
                          f"|{expected_output}|")

            test_result = actual_output == expected_output
            comment = (f'TEST if interface |{interface_name}| counters have '
                       f'symbolErrors errors on |{dut_name}|.\nGIVEN '
                       'interface symbolErrors errors is '
                       f'|{expected_output}|.\nWHEN interface symbolErrors'
                       f'errors is |{actual_output}|.\nTHEN test case result '
                       f'is |{test_result}|.\nOUTPUT of |{show_cmd}| is:'
                       f'\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output <= expected_output


@pytest.mark.nrfu
@pytest.mark.interface_baseline_health
@pytest.mark.interface
class InterfaceDiscardTests():
    """ Interface Discard Test Suite
    """

    def test_if_intf_out_counters_are_discarding_on_(self,
                                                     dut,
                                                     tests_definitions):
        """  Verify the interfaces of interest have no outDiscards

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaces']
            actual_output = int_ptr[interface_name]['outDiscards']

            output_msg = (f"On interface |{interface_name}|: interface "
                          f"counter discards has |{actual_output}| "
                          f"outDiscards, correct state is |{expected_output}|")

            test_result = actual_output <= expected_output

            comment = (f'TEST if interface |{interface_name}| counters has'
                       f' outbound discards on |{dut_name}| \nGIVEN '
                       f'interface outbound discards are |{expected_output}|\n'
                       'WHEN interface outbound discards are '
                       f'|{actual_output}|\nTHEN test case result is '
                       f'|{test_result}|.\nOUTPUT of |{show_cmd}| is:'
                       f'\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output <= expected_output

    def test_if_intf_in_counters_are_discarding_on_(self,
                                                    dut,
                                                    tests_definitions):
        """  Verify the interfaces of interest have no inDiscards

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaces']
            actual_output = int_ptr[interface_name]['inDiscards']

            output_msg = (f"On interface |{interface_name}|: interface "
                          f"counter discards has |{actual_output}| "
                          f"inDiscards, correct state is |{expected_output}|")

            test_result = actual_output <= expected_output
            comment = (f'TEST if interface |{interface_name}| counters has '
                       f'inbound discards on |{dut_name}|.\nGIVEN interface '
                       f'inbound discards are |{expected_output}|.\nWHEN '
                       f'interface inbound discards are |{actual_output}|.\n'
                       f'THEN test case result is |{test_result}|.\nOUTPUT of '
                       f'|{show_cmd}| is:\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output <= expected_output


@pytest.mark.nrfu
@pytest.mark.interface_baseline_health
@pytest.mark.interface
class InterfaceMtuTests():
    """ Interface MTU Test Suite
    """

    def test_if_intf_mtu_is_correct_on_(self, dut, tests_definitions):
        """  Verify the interfaces of interest have no inDiscards

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:
            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaces']
            actual_output = int_ptr[interface_name]['mtu']

            output_msg = (f"On interface |{interface_name}|: interface "
                          f"MTU is |{actual_output}|, correct MTU is "
                          f"|{expected_output}|")

            test_result = actual_output == expected_output
            comment = (f'TEST if interface |{interface_name}| MTU is correct '
                       f'on |{dut_name}|.\nGIVEN MTU of |{expected_output}|.\n'
                       f'WHEN interface MTU is |{actual_output}|.\nTHEN test '
                       f'case result is |{test_result}|.\nOUTPUT of '
                       f'|{show_cmd}| is:\n\n{show_cmd_txt}')

            print(f"  - {output_msg}\n{comment}")

            tests_tools.post_testcase(test_parameters, comment, test_result,
                                      output_msg, actual_output, dut_name)

            assert actual_output == expected_output
