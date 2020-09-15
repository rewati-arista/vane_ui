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

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

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

            logging.info(f'TEST if interface |{interface_name}| link '
                         f'prootocol statuses are up on |{dut_name}|')
            logging.info(f'GIVEN interface status is |{expected_output}|')
            print(f"  - On interface |{interface_name}|: interface link line "
                  f"protocol status is set to: |{actual_output}|, correct "
                  f"state is |{expected_output}|")
            logging.info(f'WHEN interface status is |{actual_output}|')

            test_result = actual_output == expected_output
            logging.info(f'THEN test case result is |{test_result}|')
            logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

            tests_tools.write_results(test_parameters,
                                      dut_name,
                                      TEST_SUITE,
                                      actual_output,
                                      test_result)

            assert actual_output == expected_output

    def test_if_intf_link_status_is_connected_on_(self,
                                                  dut,
                                                  tests_definitions):
        """ Verify the interfaces of interest link statuses are up

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
        interfaces_list = dut["output"]["interface_list"]

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        print(f"\nOn router |{dut_name}|:")

        for interface in interfaces_list:

            interface_name = interface['interface_name'].replace(" ", "")
            int_ptr = dut["output"][show_cmd]['json']['interfaceStatuses']
            actual_output = int_ptr[interface_name]['linkStatus']

            logging.info(f'TEST if interface |{interface_name}| link '
                         f' status is up on |{dut_name}|')
            logging.info(f'GIVEN interface status is |{expected_output}|')
            print(f"  - On interface |{interface_name}|: interface link line "
                  f"protocol status is set to: |{actual_output}|, correct "
                  f"state is |{expected_output}|")
            logging.info(f'WHEN interface status is |{actual_output}|')

            test_result = actual_output == expected_output
            logging.info(f'THEN test case result is |{test_result}|')
            logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

            tests_tools.write_results(test_parameters,
                                      dut_name,
                                      TEST_SUITE,
                                      actual_output,
                                      test_result)

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
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

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

                logging.info(f'TEST if interface |{interface_name}| physical '
                             f' status is up on |{dut_name}|')
                logging.info(f'GIVEN interface status is |{expected_output}|')

                split_output = raw_output.split('\n')

                for line_output in split_output:
                    if "PHY state" in line_output:
                        actual_output = line_output.split()[2]
                        logging.info('WHEN interface status is '
                                     f'|{actual_output}|')

                        print(f"  - On interface |{interface_name}|: interface"
                              " physical detail PHY state is set to: "
                              f"|{actual_output}|, correct state is "
                              f"|{expected_output}|")

                        test_result = actual_output == expected_output
                        logging.info('THEN test case result is '
                                     f'|{test_result}|')
                        logging.info(f'OUTPUT of |{show_cmd}| is '
                                     f':\n\n{show_cmd_txt}')

                        tests_tools.write_results(test_parameters,
                                                  dut_name,
                                                  TEST_SUITE,
                                                  actual_output,
                                                  test_result)

                        assert actual_output == expected_output
        else:
            tests_tools.write_results(test_parameters,
                                      dut_name,
                                      TEST_SUITE)


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

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

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

            logging.info(f'TEST if interface |{interface_name}| counters '
                         f' has input errors on |{dut_name}|')
            logging.info('GIVEN interface input errors of '
                         f'|{expected_output}|')
            logging.info('WHEN interface input errors is |{actual_output}|')

            print(f"  - On interface |{interface['interface_name']}|: "
                  f"interface counter errors has |{actual_output}| inErrors, "
                  f"correct state is |{expected_output}|")

            test_result = actual_output <= expected_output
            logging.info('THEN test case result is |{test_result}|')
            logging.info(f'OUTPUT of |{show_cmd}| is:\n\n{show_cmd_txt}')

            tests_tools.write_results(test_parameters,
                                      dut_name,
                                      TEST_SUITE,
                                      actual_output,
                                      test_result)

            assert actual_output == expected_output

    def test_if_intf_counters_has_output_errors_on_(self,
                                                    dut,
                                                    tests_definitions):
        """ Verify the interfaces of interest does not have output errors

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

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

            logging.info(f'TEST if interface |{interface_name}| counters '
                         f' has output errors on |{dut_name}|')
            logging.info('GIVEN interface output errors of '
                         f'|{expected_output}|')
            logging.info('WHEN interface output errors is |{actual_output}|')

            print(f"  - On interface |{interface['interface_name']}|: "
                  f"interface counter errors has |{actual_output}| outErrors, "
                  f"correct state is |{expected_output}|")

            test_result = actual_output <= expected_output
            logging.info('THEN test case result is |{test_result}|')
            logging.info(f'OUTPUT of |{show_cmd}| is:\n\n{show_cmd_txt}')

            tests_tools.write_results(test_parameters,
                                      dut_name,
                                      TEST_SUITE,
                                      actual_output,
                                      test_result)

            assert actual_output == expected_output

    def test_if_intf_counters_has_frame_too_short_errors_on_(self,
                                                             dut,
                                                             tests_definitions):
        """  Verify the interfaces of interest have no frameTooShorts errors

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

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

            logging.info(f'TEST if interface |{interface_name}| counters '
                         f' has frameTooShorts errors on |{dut_name}|')
            logging.info('GIVEN interface frameTooShorts errors of '
                         f'|{expected_output}|')
            logging.info('WHEN interface frameTooShorts errors is '
                         f'|{actual_output}|')

            print(f"  - On interface |{interface['interface_name']}|: "
                  f"interface counter errors has |{actual_output}| "
                  f"frameTooShorts, correct state is |{expected_output}|")

            test_result = actual_output <= expected_output
            logging.info('THEN test case result is |{test_result}|')
            logging.info(f'OUTPUT of |{show_cmd}| is:\n\n{show_cmd_txt}')

            tests_tools.write_results(test_parameters,
                                      dut_name,
                                      TEST_SUITE,
                                      actual_output,
                                      test_result)

            assert actual_output == expected_output

    def test_if_intf_counters_has_frame_too_long_errors_on_(self,
                                                            dut,
                                                            tests_definitions):
        """  Verify the interfaces of interest have no frameLongShorts errors

            Args:
                dut (dict): Encapsulates dut details including name, connection
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

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

            logging.info(f'TEST if interface |{interface_name}| counters '
                         f' has frameTooLongs errors on |{dut_name}|')
            logging.info('GIVEN interface frameTooLongs errors of '
                         f'|{expected_output}|')
            logging.info('WHEN interface frameTooLongs errors is '
                         f'|{actual_output}|')

            print(f"  - On interface |{interface['interface_name']}|: "
                  f"interface counter errors has |{actual_output}| "
                  f"frameTooLongs, correct state is |{expected_output}|")

            test_result = actual_output <= expected_output
            logging.info('THEN test case result is |{test_result}|')
            logging.info(f'OUTPUT of |{show_cmd}| is:\n\n{show_cmd_txt}')

            tests_tools.write_results(test_parameters,
                                      dut_name,
                                      TEST_SUITE,
                                      actual_output,
                                      test_result)

            assert actual_output == expected_output
