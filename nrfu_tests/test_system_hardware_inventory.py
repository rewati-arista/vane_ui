# Copyright (c) 2023 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""
Testcases for the verification of system hardware inventory on the device
"""

import re
import pytest
from pyeapi.eapilib import EapiError
from vane import tests_tools
from vane.logger import logger
from vane.config import dut_objs, test_defs

TEST_SUITE = "nrfu_tests"


@pytest.mark.nrfu_test
@pytest.mark.system
class SystemHardwareInventoryTests:
    """
    Testcases for the verification of system hardware inventory on the device
    """

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_hardware_inventory_status"]["duts"]
    test_ids = dut_parameters["test_hardware_inventory_status"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_hardware_inventory_status(self, dut, tests_definitions):
        """
        TD: Test case for the verification of system hardware inventory on the device.
        Args:
          dut(dict): Details related to a particular device.
          tests_definitions(dict): Test suite and test case parameters
        """
        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)
        self.output = ""
        test_params = tops.test_parameters
        tops.actual_output = {"hardware_inventory_details": {}}
        tops.expected_output = {"hardware_inventory_details": {}}
        actual_output, expected_output = {}, {}

        # Forming output message if test result is pass
        tops.output_msg = (
            "Power supply, fan tray and other card slots are inserted and present on the device."
        )

        try:
            """
            TS: Running 'show version' command on device and skipping the test case
            for device if platform is vEOS.
            """
            version_output = dut["output"]["show version"]["json"]
            logger.info(
                "On device %s, output of `show version` command is: \n%s\n",
                tops.dut_name,
                version_output,
            )
            self.output += f"\n\nOutput of {tops.show_cmd} command is: \n{version_output}"

            # Skipping testcase if device is vEOS.
            if "vEOS" in version_output.get("modelName"):
                pytest.skip(f"{tops.dut_name} is vEOS device, hence test skipped.")

            """
            TS: Running `show inventory` command on the device and verifying the power supply
            slots, fan tray slots and other card slots are inserted on the device.
            """
            output = dut["output"][tops.show_cmd]["json"]
            logger.info(
                "On device %s, output of %s command is: \n%s\n",
                tops.dut_name,
                tops.show_cmd,
                output,
            )
            self.output += f"\n\nOutput of {tops.show_cmd} command is: \n{output}"

            for slot, verify_slot in test_params["hardware_inventory_checks"].items():
                if verify_slot and "CardSlots" not in slot:
                    slot = slot.split("_")[1]
                    # Converting slot name from camel case.
                    converted_slot_name = re.sub("([A-Z])", r"_\1", slot).lower()
                    slot_output = output[slot]
                    expected_output.update({converted_slot_name: {}})
                    actual_output.update({converted_slot_name: {}})
                    for slot_name, slot_details in slot_output.items():
                        expected_output[converted_slot_name].update(
                            {slot_name: {"card_slot_name_found": True}}
                        )
                        actual_output[converted_slot_name].update(
                            {
                                slot_name: {
                                    "card_slot_name_found": (
                                        "Not Inserted" not in slot_details["name"]
                                    )
                                }
                            }
                        )

            for slot, verify_slot in test_params["hardware_inventory_checks"].items():
                if verify_slot and "CardSlots" in slot:
                    slot = slot.split("_")[1]
                    # Converting slot name from camel case.
                    converted_slot_name = re.sub("([A-Z])", r"_\1", slot).lower()
                    card_name = converted_slot_name.split("_")[0]
                    slot_output = output["cardSlots"]
                    expected_output.update({converted_slot_name: {}})
                    actual_output.update({converted_slot_name: {}})
                    for slot_name, slot_details in slot_output.items():
                        if card_name.capitalize() in slot_name:
                            expected_output[converted_slot_name].update(
                                {slot_name: {"card_slot_name_found": True}}
                            )
                            actual_output[converted_slot_name].update(
                                {
                                    slot_name: {
                                        "card_slot_name_found": (
                                            "Not Inserted" not in slot_details["modelName"]
                                        )
                                    }
                                }
                            )

            tops.actual_output["hardware_inventory_details"].update(actual_output)
            tops.expected_output["hardware_inventory_details"].update(expected_output)

            # Forming the output message if the testcase is failed
            if tops.expected_output != tops.actual_output:
                tops.output_msg = "The following cards are not inserted:"
                output_msg = []
                for slot_name, slot_details in tops.actual_output[
                    "hardware_inventory_details"
                ].items():
                    slot_status = []
                    for card_slot, card_slot_status in slot_details.items():
                        if not card_slot_status["card_slot_name_found"]:
                            slot_status.append(card_slot)
                    if slot_status:
                        message = f"\nFor {slot_name.replace('_', ' ')}: \n"
                        message += f"{', '.join(slot_status)}\n"
                        output_msg.append(message)
                tops.output_msg += "".join(output_msg)

        except (AssertionError, AttributeError, LookupError, EapiError) as excp:
            tops.actual_output = tops.output_msg = str(excp).split("\n", maxsplit=1)[0]
            logger.error(
                "On device %s: Error occurred while running testcase is:\n%s",
                tops.dut_name,
                tops.actual_output,
            )

        tops.test_result = tops.expected_output == tops.actual_output
        tops.parse_test_steps(self.test_hardware_inventory_status)
        tops.generate_report(tops.dut_name, self.output)
        assert tops.expected_output == tops.actual_output
