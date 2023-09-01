# Copyright (c) 2023 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""
Testcases for verification of redundant supervisor card.
"""

import pytest
from pyeapi.eapilib import EapiError
from vane.logger import logger
from vane.config import dut_objs, test_defs
from vane import tests_tools

TEST_SUITE = "nrfu_tests"


@pytest.mark.nrfu_test
@pytest.mark.base_services
class RedundantSupervisorCardTests:
    """
    Testcases for verification of redundant supervisor card.
    """

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_redundant_sso_card"]["duts"]
    test_ids = dut_parameters["test_redundant_sso_card"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_redundant_sso_card(self, dut, tests_definitions):
        """
        TD: Testcase for verification of redundant supervisor card.
        Args:
            dut(dict): details related to a particular device.
            tests_definitions(dict): test suite and test case parameters.
        """
        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)
        self.output = ""
        tops.actual_output = {"sso_protocol_details": {}}

        # Forming output message if test result is passed
        tops.output_msg = (
            "Redundancy SSO protocol is configured, operational and ready for switchover."
        )

        try:
            """
            TS: Running 'show redundancy status' command on the device and
            verifying that the SSO protocol is configured, operational and ready for switchover.
            """
            output = dut["output"][tops.show_cmd]["json"]
            logger.info(
                "On device %s, output of %s command is: \n%s\n",
                tops.dut_name,
                tops.show_cmd,
                output,
            )
            self.output += f"\n\nOutput of {tops.show_cmd} command is: \n{output}"
            peer_card_details = output["peerState"] != "notInserted"
            assert (
                peer_card_details
            ), f"Peer supervisor card is not inserted on device {tops.dut_name}"

            # Skipping testcase if SSO protocol is not configured on the device.
            if output.get("configuredProtocol") != "sso":
                pytest.skip(
                    f"SSO is not configured on {tops.dut_name}, hence skipping the testcase."
                )

            tops.actual_output["sso_protocol_details"].update(
                {
                    "configured_protocol": output["configuredProtocol"],
                    "operational_protocol": output["operationalProtocol"],
                    "switch_over_ready": output["switchoverReady"],
                }
            )

            # Forming the output message if the testcase is failed
            if tops.expected_output != tops.actual_output:
                tops.output_msg = "\n"
                expected_details = tops.expected_output["sso_protocol_details"]
                actual_details = tops.actual_output["sso_protocol_details"]
                if (
                    expected_details["operational_protocol"]
                    != actual_details["operational_protocol"]
                ):
                    tops.output_msg += (
                        "Expected operational protocol is"
                        f" '{expected_details['operational_protocol']}', however in actual it is"
                        f" found as '{actual_details['operational_protocol']}'.\n"
                    )
                if not actual_details["switch_over_ready"]:
                    tops.output_msg += "Redundancy protocol sso is not ready for switch over.\n"

        except (AssertionError, AttributeError, LookupError, EapiError) as excep:
            tops.output_msg = tops.actual_output = str(excep).split("\n", maxsplit=1)[0]
            logger.error(
                "On device %s, Error while running the testcase is:\n%s",
                tops.dut_name,
                tops.actual_output,
            )

        tops.test_result = tops.expected_output == tops.actual_output
        tops.parse_test_steps(self.test_redundant_sso_card)
        tops.generate_report(tops.dut_name, self.output)
        assert tops.expected_output == tops.actual_output
