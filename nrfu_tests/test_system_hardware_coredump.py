# Copyright (c) 2023 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""
Test case for verification of core dump files
"""

import pytest
from pyeapi.eapilib import EapiError
from vane.logger import logger
from vane.config import dut_objs, test_defs
from vane import tests_tools

TEST_SUITE = "nrfu_tests"


@pytest.mark.nrfu_test
@pytest.mark.system
class CoreDumpFilesTests:
    """
    Test case for verification of core dump files
    """

    dut_parameters = tests_tools.parametrize_duts(TEST_SUITE, test_defs, dut_objs)
    test_duts = dut_parameters["test_hardware_core_dump_files"]["duts"]
    test_ids = dut_parameters["test_hardware_core_dump_files"]["ids"]

    @pytest.mark.parametrize("dut", test_duts, ids=test_ids)
    def test_hardware_core_dump_files(self, dut, tests_definitions):
        """
        TD: Test case for verification of core dump files
        Args:
            dut(dict): details related to a particular DUT
            tests_definitions(dict): test suite and test case parameters.
        """

        tops = tests_tools.TestOps(tests_definitions, TEST_SUITE, dut)
        self.output = ""
        tops.actual_output = {}
        tops.output_msg = "Core dump files are not found on the device."

        try:
            """
            TS: Running `show system coredump` command on dut and verifying that core dump files
            should not found on the device.
            """
            core_dump = dut["output"][tops.show_cmd]["json"]
            logger.info(
                "On device %s, output of %s command is:\n%s\n",
                tops.dut_name,
                tops.show_cmd,
                core_dump,
            )
            self.output = f"Output of {tops.show_cmd} command is:\n{core_dump}"
            core_dump = core_dump["coreFiles"]
            tops.actual_output["core_dump_files_not_found"] = not bool(core_dump)

            # Output message formation in case of testcase fails.
            if tops.actual_output != tops.expected_output:
                tops.output_msg = "Core dump files are found on the device."

        except (AttributeError, LookupError, EapiError) as excep:
            tops.output_msg = tops.actual_output = str(excep).split("\n", maxsplit=1)[0]
            logger.error(
                "On device %s, Error while running the testcase is:\n%s",
                tops.dut_name,
                tops.actual_output,
            )

        tops.test_result = tops.expected_output == tops.actual_output
        tops.parse_test_steps(self.test_hardware_core_dump_files)
        tops.generate_report(tops.dut_name, self.output)
        assert tops.expected_output == tops.actual_output
