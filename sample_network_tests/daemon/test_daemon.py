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

""" Tests to validate daemon status."""

import pytest
from pyeapi.eapilib import EapiError
from vane.config import dut_objs, test_defs
from vane import tests_tools
from vane.vane_logging import logging


TEST_SUITE = __file__
LOG_FILE = {"parameters": {"show_log": "show_output.log"}}


@pytest.mark.demo
@pytest.mark.nrfu
@pytest.mark.base_feature
@pytest.mark.daemons
@pytest.mark.virtual
@pytest.mark.physical
class DaemonTests:
    """EOS Daemon Test Suite"""

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_if_daemons_are_running_on_"]["duts"]
    test_ids = dut_parameters["test_if_daemons_are_running_on_"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_if_daemons_are_running_on_(self, dut, tests_definitions):
        """TD: Verify a list of daemons are running on DUT

        Args:
          dut (dict): Encapsulates dut details including name, connection
          tests_definitions (dict): Test parameters
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)

        try:
            """
            TS: Collecting the output of 'show daemon' command from DUT
            """

            output = dut["output"][tops.show_cmd]["json"]
            daemons = tops.test_parameters["daemons"]

            for daemon in daemons:
                assert (
                    (output.get("daemons")).get(daemon).get("running")
                ), "Show daemon details are not found"

                logging.info(
                    f"On device {tops.dut_name} output of {tops.show_cmd} command is: {output}"
                )

                tops.actual_output = output["daemons"][daemon]["running"]

                """
                TS: Verify daemons are running on DUT
                """
                if tops.actual_output == tops.expected_output["daemon_running"]:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {daemon} daemon has expected running "
                        f"state: {tops.actual_output}. "
                    )
                else:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {daemon} daemon has unexpected running state: "
                        f"{tops.actual_output} and should be in running state: "
                        f"{tops.expected_output['daemon_running']}. "
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
                f"investigating daemon: {daemon}. Vane recorded error: {exp} "
            )

        print(
            f"\n{tops.dut_name}# {tops.test_parameters['show_cmd']}\n"
            f"{dut['output'][tops.show_cmd]['text']}"
        )

        """
        TS: Creating test report based on results
        """
        tops.parse_test_steps(self.test_if_daemons_are_running_on_)
        tops.test_result = tops.actual_output == tops.expected_output["daemon_running"]
        tops.generate_report(tops.dut_name, output)

        """
        TS: Determing pass or fail based on test criteria
        """
        assert tops.actual_output == tops.expected_output["daemon_running"]

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_if_daemons_are_enabled_on_"]["duts"]
    test_ids = dut_parameters["test_if_daemons_are_enabled_on_"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_if_daemons_are_enabled_on_(self, dut, tests_definitions):
        """TD: Verify a list of daemons are enabled on DUT

        Args:
          dut (dict): Encapsulates dut details including name, connection
          tests_definitions (dict): Test parameters
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)

        try:
            """
            TS: Collecting the output of 'show daemon' command from DUT
            """

            output = dut["output"][tops.show_cmd]["json"]
            daemons = tops.test_parameters["daemons"]

            for daemon in daemons:
                assert (
                    (output.get("daemons")).get(daemon).get("enabled")
                ), "Show daemon details are not found"

                logging.info(
                    f"On device {tops.dut_name} output of {tops.show_cmd} command is: {output}"
                )

                tops.actual_output = output["daemons"][daemon]["enabled"]

                """
                TS: Verify daemons are enabled on DUT
                """
                if tops.actual_output == tops.expected_output["daemon_enabled"]:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {daemon} daemon has expected enabled "
                        f"state: {tops.actual_output}. "
                    )
                else:
                    tops.output_msg += (
                        f"{tops.dut_name}'s {daemon} daemon has unexpected enabled state: "
                        f"{tops.actual_output} and should be in enabled state: "
                        f"{tops.expected_output['daemon_enabled']}. "
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
                f"investigating daemon: {daemon}. Vane recorded error: {exp} "
            )

        print(
            f"\n{tops.dut_name}# {tops.test_parameters['show_cmd']}\n"
            f"{dut['output'][tops.show_cmd]['text']}"
        )

        """
        TS: Creating test report based on results
        """
        tops.parse_test_steps(self.test_if_daemons_are_enabled_on_)
        tops.test_result = tops.actual_output == tops.expected_output["daemon_enabled"]
        tops.generate_report(tops.dut_name, output)

        """
        TS: Determing pass or fail based on test criteria
        """
        assert tops.actual_output == tops.expected_output["daemon_enabled"]
