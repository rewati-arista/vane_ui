# Copyright (c) 2023 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""
Testcase for verification of mlag interfaces status check.
"""

import pytest
from pyeapi.eapilib import EapiError
from vane.logger import logger
from vane.config import dut_objs, test_defs
from vane import tests_tools

TEST_SUITE = "nrfu_tests"


@pytest.mark.nrfu_test
@pytest.mark.interfaces
class InterfacesMlagStatusCheckTests:
    """
    Testcase for verification of mlag interfaces status check.
    """

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_interfaces_mlag_status_check"]["duts"]
    test_ids = dut_parameters["test_interfaces_mlag_status_check"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_interfaces_mlag_status_check(self, dut, tests_definitions):
        """
        TD: Testcase for verification of mlag interfaces status check.
        Args:
            dut(dict): details related to a particular DUT
            tests_definitions(dict): test suite and test case parameters
        """
        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)
        self.output = ""
        tops.actual_output = {"mlag_details": {}}
        tops.expected_output = {"mlag_details": {}}

        # Forming output message if test result is passed
        tops.output_msg = "MLAG is configured on the device."

        try:
            """
            TS: Running 'show mlag' command on DUT and verifying that the MLAG is configured
            on the device.
            """
            output = dut["output"][tops.show_cmd]["json"]
            logger.info(
                "On device %s, output of %s command is: \n%s\n",
                tops.dut_name,
                tops.show_cmd,
                output,
            )
            self.output += f"\nOutput of {tops.show_cmd} command is: \n{output}"
            assert output, "MLAG details are not found"

            # collecting actual output.
            if output["state"] != "disabled":
                tops.actual_output["mlag_details"].update(
                    {
                        "state": output.get("state"),
                        "negStatus": output.get("negStatus"),
                        "configSanity": output.get("configSanity"),
                    }
                )
                tops.expected_output["mlag_details"].update(
                    {"state": "active", "negStatus": "connected", "configSanity": "consistent"}
                )
            else:
                pytest.skip(f"For {tops.dut_name} MLAG is not configured, hence test skipped.")

            # Output message formation in case of testcase fails.
            if tops.actual_output != tops.expected_output:
                tops.output_msg = ""
                for mlag_key, mlag_value in tops.expected_output["mlag_details"].items():
                    if mlag_value != tops.actual_output["mlag_details"].get(mlag_key):
                        tops.output_msg += (
                            f"Expected value of {mlag_key.replace('_', ' ')} is '{mlag_value}',"
                            " however actual found as"
                            f" '{tops.actual_output['mlag_details'].get(mlag_key)}'.\n"
                        )

        except (AssertionError, AttributeError, LookupError, EapiError) as excep:
            tops.output_msg = tops.actual_output = str(excep).split("\n", maxsplit=1)[0]
            logger.error(
                "On device %s, Error while running the testcase is:\n%s",
                tops.dut_name,
                tops.actual_output,
            )

        tops.test_result = tops.expected_output == tops.actual_output
        tops.parse_test_steps(self.test_interfaces_mlag_status_check)
        tops.generate_report(tops.dut_name, self.output)
        assert tops.expected_output == tops.actual_output
