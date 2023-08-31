# Copyright (c) 2023 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""Testcases for verification of security root port EOS no configurations functionality"""

import pytest
from pyeapi.eapilib import EapiError
from vane import tests_tools
from vane.logger import logger
from vane.config import dut_objs, test_defs

TEST_SUITE = "nrfu_tests"


@pytest.mark.nrfu_test
@pytest.mark.security
class EosNoConfigTests:

    """Testcases for verification of security root port EOS no configurations functionality"""

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_eos_no_config_functionality"]["duts"]
    test_ids = dut_parameters["test_eos_no_config_functionality"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_eos_no_config_functionality(self, dut, tests_definitions):
        """
        TD: Testcases for verification of security root port EOS no configurations functionality
        Args:
          dut(dict): Details related to the switches
          tests_definitions(dict): Test suite and test case parameters
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)
        self.output = ""
        tops.expected_output = {"rp_eos_configurations": {}}
        tops.actual_output = {"rp_eos_configurations": {}}

        # Forming output message if test result is pass
        tops.output_msg = "No localhost found in LLDP information on device."

        try:
            """
            TS: Running 'show lldp neighbors detail' command and Verifying device is configured
            successfully with EOS configurations.
            """
            lldp_info = dut["output"][tops.show_cmd]["json"]
            logger.info(
                "On device %s, Output of %s command is:\n%s\n",
                tops.dut_name,
                tops.show_cmd,
                lldp_info,
            )
            self.output += (
                f"On device {tops.dut_name}, Output of {tops.show_cmd} is:\n{lldp_info}\n"
            )
            neighbor_details = lldp_info.get("lldpNeighbors")
            assert neighbor_details, f"lldp neighbor details not found on device {tops.dut_name}."

            for interface, interface_details in lldp_info.get("lldpNeighbors").items():
                if not interface_details.get("lldpNeighborInfo"):
                    tops.actual_output["rp_eos_configurations"][interface] = True
                    tops.expected_output["rp_eos_configurations"][interface] = True
                    continue

                system_name = interface_details.get("lldpNeighborInfo", [])[0].get("systemName")
                system_description = interface_details.get("lldpNeighborInfo", [])[0].get(
                    "systemDescription"
                )
                # If details for above keys are not found then skipping the verification part for
                # the same considering no localhost in configurations.
                if not system_description or not system_name:
                    continue

                if system_name == "localhost":
                    if "Arista" in system_description:
                        tops.expected_output["rp_eos_configurations"][interface] = True
                        tops.actual_output["rp_eos_configurations"][interface] = False

            # forming output message if test result is fail
            if tops.actual_output != tops.expected_output:
                localhost_found_interfaces = []
                for interface in tops.actual_output["rp_eos_configurations"]:
                    if not tops.actual_output["rp_eos_configurations"][interface]:
                        localhost_found_interfaces.append(interface)
                tops.output_msg = (
                    f"\nOn device {tops.dut_name}, following interfaces found with localhost in"
                    f" LLDP information:\n{', '.join(localhost_found_interfaces)}"
                )

        except (AssertionError, AttributeError, LookupError, EapiError) as excep:
            tops.actual_output = tops.output_msg = str(excep).split("\n", maxsplit=1)[0]
            logger.error(
                "On device %s: Error while running the testcase is:\n%s",
                tops.dut_name,
                tops.actual_output,
            )

        tops.test_result = tops.expected_output == tops.actual_output
        tops.parse_test_steps(self.test_eos_no_config_functionality)
        tops.generate_report(tops.dut_name, self.output)
        assert tops.expected_output == tops.actual_output
