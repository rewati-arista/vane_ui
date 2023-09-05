# Copyright (c) 2023 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""
Testcase for verification of ACLs are applied to each VRF the API is enabled on.
"""

import pytest
from pyeapi.eapilib import EapiError
from vane.logger import logger
from vane.config import dut_objs, test_defs
from vane import tests_tools

TEST_SUITE = "nrfu_tests"


@pytest.mark.nrfu_test
@pytest.mark.security
class AclsApiAccessTests:
    """
    Testcase for verification of ACLs are applied to each VRF the API is enabled on.
    """

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_acls_api_vrfs_enabled"]["duts"]
    test_ids = dut_parameters["test_acls_api_vrfs_enabled"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_acls_api_vrfs_enabled(self, dut, tests_definitions):
        """
        TD: Testcase for verification of ACLs are applied to each VRF the API is enabled on.
        Args:
            dut(dict): details related to a particular DUT
            tests_definitions(dict): test suite and test case parameters.
        """
        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)
        tops.expected_output = {"vrf_details": {}}
        tops.actual_output = {"vrf_details": {}}
        self.output = ""

        # Forming output message if test result is passed.
        tops.output_msg = "All VRFs that the API is active are ACL configured."

        try:
            """
            TS: Running `show management api http-commands` and
            `show management api http-commands ip access-list summary` commands
            and verifying that all the VRFs are ACL configured.
            """
            output_api_vrfs = dut["output"][tops.show_cmds[tops.dut_name][0]]["json"]
            output_api_acls = dut["output"][tops.show_cmds[tops.dut_name][1]]["json"]
            logger.info(
                "On device %s, output of %s command is:\n%s\n",
                tops.dut_name,
                [tops.show_cmds[tops.dut_name][0]],
                output_api_vrfs,
            )
            self.output = (
                f"Output of {[tops.show_cmds[tops.dut_name][0]]} command is:\n{output_api_vrfs}\n"
            )
            logger.info(
                "On device %s, output of %s command is:\n%s\n",
                tops.dut_name,
                [tops.show_cmds[tops.dut_name][1]],
                output_api_acls,
            )
            self.output = (
                f"Output of {[tops.show_cmds[tops.dut_name][1]]} command is:\n{output_api_acls}\n"
            )

            # Collecting VRFs and ACLs from output.
            api_vrfs = output_api_vrfs.get("vrfs")
            api_acls = output_api_acls.get("ipAclList").get("aclList")
            assert api_vrfs, "Vrfs details are not found in output."

            assert api_acls, "ACL details for APIs is not found in output."

            # Collecting actual and expected output.
            for vrf in api_vrfs:
                acl_found = False
                for acl in api_acls:
                    tops.expected_output["vrf_details"].update({vrf: "Configured"})
                    if vrf in acl["activeVrfs"]:
                        acl_found = True
                        tops.actual_output["vrf_details"].update({vrf: "Configured"})
                    if not acl_found:
                        tops.actual_output["vrf_details"].update({vrf: "Not Configured"})

            # Forming output message if test result is failed.
            if tops.actual_output != tops.expected_output:
                tops.output_msg = "\n"
                non_configured_vrfs = []
                for vrf_name, vrf_status in tops.expected_output["vrf_details"].items():
                    if vrf_status != tops.actual_output["vrf_details"].get(vrf_name):
                        non_configured_vrfs.append(vrf_name)
                vrf_configured_status = ", ".join(non_configured_vrfs)
                tops.output_msg += (
                    f"Following vrfs are not ACL configured: {vrf_configured_status}."
                )

        except (AssertionError, AttributeError, LookupError, EapiError) as excep:
            tops.output_msg = tops.actual_output = str(excep).split("\n", maxsplit=1)[0]
            logger.error(
                "On device %s, Error while running the testcase is:\n%s",
                tops.dut_name,
                tops.actual_output,
            )

        tops.test_result = tops.expected_output == tops.actual_output
        tops.parse_test_steps(self.test_acls_api_vrfs_enabled)
        tops.generate_report(tops.dut_name, self.output)
        assert tops.expected_output == tops.actual_output
