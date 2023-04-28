#!/usr/bin/env python3
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

""" Tests to validate LLDP status."""

import pytest
from pyeapi.eapilib import EapiError
from vane.config import dut_objs, test_defs
from vane import tests_tools
from vane.vane_logging import logging


TEST_SUITE = __file__
LOG_FILE = {"parameters": {"show_log": "show_output.log"}}


@pytest.mark.nrfu
@pytest.mark.l2_protocols
@pytest.mark.lldp
@pytest.mark.virtual
@pytest.mark.physical
class LldpTests:
    """LLDP Test Suite"""

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_if_lldp_rx_is_enabled_on_"]["duts"]
    test_ids = dut_parameters["test_if_lldp_rx_is_enabled_on_"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_if_lldp_rx_is_enabled_on_(self, dut, tests_definitions):
        """Verify LLDP receive is enabled on interesting interfaces

        Args:
            dut (dict): Encapsulates dut details including name, connection
            tests_definitions (dict): Test parameters
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)

        try:
            """
            TS: Collecting the output of 'show lldp' command from DUT
            """

            output = dut["output"][tops.show_cmd]["json"]

            for interface in tops.interface_list:
                interface_name = interface["interface_name"].replace(" ", "")
                assert output.get("lldpInterfaces").get(
                    interface_name
                ), f"Show LLDP interface: {interface_name} details are not found"

                logging.info(
                    f"On device {tops.dut_name} output of {tops.show_cmd} command is: {output}"
                )

                tops.actual_output = output["lldpInterfaces"][interface_name][
                    "rxEnabled"
                ]

                """
                TS: Verify LLDP interface RX state on DUT
                """
                if tops.actual_output == tops.expected_output:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {interface_name} LLDP RX is enabled\n"
                    )
                else:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {interface_name} LLDP RX is NOT enabled\n"
                    )

                tops.actual_results.append(tops.actual_output)
                tops.expected_results.append(tops.expected_output)

        except (AttributeError, LookupError, EapiError) as exp:
            tops.actual_output = str(exp)
            logging.error(
                "On device %s: Error while running testcase on DUT is: %s",
                tops.dut_name,
                str(exp),
            )
            tops.output_msg += (
                f" EXCEPTION encountered on device {tops.dut_name}, while "
                f"investigating LLDP rxEnabled: {interface_name}. Vane recorded error: {exp} "
            )

        print(
            f"\n{tops.dut_name}# {tops.test_parameters['show_cmd']}\n"
            f"{dut['output'][tops.show_cmd]['text']}"
        )

        """
        TS: Creating test report based on results
        """
        tops.actual_output, tops.expected_output = (
            tops.actual_results,
            tops.expected_results,
        )
        tops.parse_test_steps(self.test_if_lldp_rx_is_enabled_on_)
        tops.test_result = tops.actual_results == tops.expected_results
        tops.generate_report(tops.dut_name, output)

        """
        TS: Determing pass or fail based on test criteria
        """
        assert tops.actual_results == tops.expected_results

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_if_lldp_tx_is_enabled_on_"]["duts"]
    test_ids = dut_parameters["test_if_lldp_tx_is_enabled_on_"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_if_lldp_tx_is_enabled_on_(self, dut, tests_definitions):
        """Verify LLDP transmit is enabled on interesting interfaces

        Args:
            dut (dict): Encapsulates dut details including name, connection
            tests_definitions (dict): Test parameters
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)

        try:
            """
            TS: Collecting the output of 'show lldp' command from DUT
            """

            output = dut["output"][tops.show_cmd]["json"]

            for interface in tops.interface_list:
                interface_name = interface["interface_name"].replace(" ", "")
                assert output.get("lldpInterfaces").get(
                    interface_name
                ), f"Show LLDP interface: {interface_name} details are not found"

                logging.info(
                    f"On device {tops.dut_name} output of {tops.show_cmd} command is: {output}"
                )

                tops.actual_output = output["lldpInterfaces"][interface_name][
                    "txEnabled"
                ]

                """
                TS: Verify LLDP interface TX state on DUT
                """
                if tops.actual_output == tops.expected_output:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {interface_name} LLDP TX is enabled\n"
                    )
                else:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {interface_name} LLDP TX is NOT enabled\n"
                    )

                tops.actual_results.append(tops.actual_output)
                tops.expected_results.append(tops.expected_output)

        except (AttributeError, LookupError, EapiError) as exp:
            tops.actual_output = str(exp)
            logging.error(
                "On device %s: Error while running testcase on DUT is: %s",
                tops.dut_name,
                str(exp),
            )
            tops.output_msg += (
                f" EXCEPTION encountered on device {tops.dut_name}, while "
                f"investigating LLDP txEnabled: {interface_name}. Vane recorded error: {exp} "
            )

        print(
            f"\n{tops.dut_name}# {tops.test_parameters['show_cmd']}\n"
            f"{dut['output'][tops.show_cmd]['text']}"
        )

        """
        TS: Creating test report based on results
        """
        tops.actual_output, tops.expected_output = (
            tops.actual_results,
            tops.expected_results,
        )
        tops.parse_test_steps(self.test_if_lldp_tx_is_enabled_on_)
        tops.test_result = tops.actual_results == tops.expected_results
        tops.generate_report(tops.dut_name, output)

        """
        TS: Determing pass or fail based on test criteria
        """
        assert tops.actual_results == tops.expected_results


@pytest.mark.nrfu
@pytest.mark.l2_protocols
@pytest.mark.lldp
@pytest.mark.virtual
@pytest.mark.physical
class LldpLocalInfoTests:
    """LLDP Local-Info Test Suite"""

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_if_lldp_system_name_is_correct_on_"]["duts"]
    test_ids = dut_parameters["test_if_lldp_system_name_is_correct_on_"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_if_lldp_system_name_is_correct_on_(self, dut, tests_definitions):
        """Verify show lldp local-info hostname is the system's name

        Args:
            dut (dict): Encapsulates dut details including name, connection
            tests_definitions (dict): Test parameters
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)

        try:
            """
            TS: Collecting the output of 'show lldp local-info' command from DUT
            """
            output = dut["output"][tops.show_cmd]["json"]
            tops.expected_output = tops.dut_name

            assert output.get("systemName"), "Show LLDP details are not found"
            tops.actual_output = output["systemName"]

            logging.info(
                f"On device {tops.dut_name} output of {tops.show_cmd} command is: {output}"
            )

            """
            TS: Verify LLDP system name
            """
            if tops.actual_output == tops.expected_output:
                tops.output_msg = (
                    f"{tops.dut_name}'s LLDP System Name is correct: "
                    f"{tops.expected_output}"
                )
            else:
                tops.output_msg = (
                    f"{tops.dut_name}'s LLDP System Name is NOT correct: {tops.actual_output}. "
                    f"LLDP System Name should be set to: {tops.expected_output}"
                )

        except (AttributeError, LookupError, EapiError) as exp:
            tops.actual_output = str(exp)
            logging.error(
                "On device %s: Error while running testcase on DUT is: %s",
                tops.dut_name,
                str(exp),
            )
            tops.output_msg += (
                f" EXCEPTION encountered on device {tops.dut_name}, while "
                f"investigating LLDP system name. Vane recorded error: {exp} "
            )

        print(
            f"\n{tops.dut_name}# {tops.test_parameters['show_cmd']}\n"
            f"{dut['output'][tops.show_cmd]['text']}"
        )

        """
        TS: Creating test report based on results
        """
        tops.parse_test_steps(self.test_if_lldp_system_name_is_correct_on_)
        tops.test_result = tops.actual_output == tops.expected_output
        tops.generate_report(tops.dut_name, output)

        """
        TS: Determing pass or fail based on test criteria
        """
        assert tops.actual_output == tops.expected_output

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_if_lldp_max_frame_size_is_correct_on_"]["duts"]
    test_ids = dut_parameters["test_if_lldp_max_frame_size_is_correct_on_"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_if_lldp_max_frame_size_is_correct_on_(self, dut, tests_definitions):
        """Verify show lldp local-info maxFrameSize is correct

        Args:
            dut (dict): Encapsulates dut details including name, connection
            tests_definitions (dict): Test parameters
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)

        try:
            """
            TS: Collecting the output of 'show lldp local-info' command from DUT
            """

            output = dut["output"][tops.show_cmd]["json"]

            for interface in tops.interface_list:
                interface_name = interface["interface_name"].replace(" ", "")
                assert output.get("localInterfaceInfo").get(
                    interface_name
                ), f"Show LLDP interface: {interface_name} details are not found"

                logging.info(
                    f"On device {tops.dut_name} output of {tops.show_cmd} command is: {output}"
                )

                tops.actual_output = output["localInterfaceInfo"][interface_name][
                    "maxFrameSize"
                ]

                """
                TS: Verify LLDP interface max frame size on DUT
                """
                if tops.actual_output == tops.expected_output:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {interface_name} Max frame size is correct: "
                        f"{tops.actual_output}\n"
                    )
                else:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {interface_name} Max frame size is NOT correct: "
                        f"{tops.expected_output}.  Max frame size should be {tops.actual_output}\n"
                    )

                tops.actual_results.append(tops.actual_output)
                tops.expected_results.append(tops.expected_output)

        except (AttributeError, LookupError, EapiError) as exp:
            tops.actual_output = str(exp)
            logging.error(
                "On device %s: Error while running testcase on DUT is: %s",
                tops.dut_name,
                str(exp),
            )
            tops.output_msg += (
                f" EXCEPTION encountered on device {tops.dut_name}, while "
                f"investigating Max frame size for {interface_name}. Vane recorded error: {exp} "
            )

        print(
            f"\n{tops.dut_name}# {tops.test_parameters['show_cmd']}\n"
            f"{dut['output'][tops.show_cmd]['text']}"
        )

        """
        TS: Creating test report based on results
        """
        tops.actual_output, tops.expected_output = (
            tops.actual_results,
            tops.expected_results,
        )
        tops.parse_test_steps(self.test_if_lldp_max_frame_size_is_correct_on_)
        tops.test_result = tops.actual_results == tops.expected_results
        tops.generate_report(tops.dut_name, output)

        """
        TS: Determing pass or fail based on test criteria
        """
        assert tops.actual_results == tops.expected_results

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_if_lldp_interface_id_is_correct_on_"]["duts"]
    test_ids = dut_parameters["test_if_lldp_interface_id_is_correct_on_"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_if_lldp_interface_id_is_correct_on_(self, dut, tests_definitions):
        """Verify show lldp local-info interfaceIdType is correct

        Args:
            dut (dict): Encapsulates dut details including name, connection
            tests_definitions (dict): Test parameters
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)

        try:
            """
            TS: Collecting the output of 'show lldp local-info' command from DUT
            """

            output = dut["output"][tops.show_cmd]["json"]

            for interface in tops.interface_list:
                interface_name = interface["interface_name"].replace(" ", "")
                assert output.get("localInterfaceInfo").get(
                    interface_name
                ), f"Show LLDP interface: {interface_name} details are not found"

                logging.info(
                    f"On device {tops.dut_name} output of {tops.show_cmd} command is: {output}"
                )

                tops.actual_output = output["localInterfaceInfo"][interface_name][
                    "interfaceIdType"
                ]

                """
                TS: Verify LLDP interface ID on DUT
                """
                if tops.actual_output == tops.expected_output:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {interface_name} interface ID is correct: "
                        f"{tops.actual_output}\n"
                    )
                else:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {interface_name} interface ID is NOT correct: "
                        f"{tops.expected_output}.  Interface ID should be {tops.actual_output}\n"
                    )

                tops.actual_results.append(tops.actual_output)
                tops.expected_results.append(tops.expected_output)

        except (AttributeError, LookupError, EapiError) as exp:
            tops.actual_output = str(exp)
            logging.error(
                "On device %s: Error while running testcase on DUT is: %s",
                tops.dut_name,
                str(exp),
            )
            tops.output_msg += (
                f" EXCEPTION encountered on device {tops.dut_name}, while "
                f"investigating interface ID for {interface_name}. Vane recorded error: {exp} "
            )

        print(
            f"\n{tops.dut_name}# {tops.test_parameters['show_cmd']}\n"
            f"{dut['output'][tops.show_cmd]['text']}"
        )

        """
        TS: Creating test report based on results
        """
        tops.actual_output, tops.expected_output = (
            tops.actual_results,
            tops.expected_results,
        )
        tops.parse_test_steps(self.test_if_lldp_interface_id_is_correct_on_)
        tops.test_result = tops.actual_results == tops.expected_results
        tops.generate_report(tops.dut_name, output)

        """
        TS: Determing pass or fail based on test criteria
        """
        assert tops.actual_results == tops.expected_results
