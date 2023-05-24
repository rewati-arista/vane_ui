"""vane_cli.py uni tests"""
import argparse
import os
from unittest.mock import call
import pytest
from vane import vane_cli


@pytest.fixture
def loginfo(mocker):
    """Fixture to mock logger calls from vane.vane_cli"""
    return mocker.patch("vane.vane_logging.logging.info")


@pytest.fixture
def logerr(mocker):
    """Fixture to mock logger calls from vane.vane_cli"""
    return mocker.patch("vane.vane_logging.logging.error")


@pytest.fixture
def logwarning(mocker):
    """Fixture to mock logger calls from vane.vane_cli"""
    return mocker.patch("vane.vane_logging.logging.warning")


def test_parse_cli():
    """Validates functionality of parse_cli method"""

    arguments = vane_cli.parse_cli()
    assert len(vars(arguments)) == 7
    # checking for default values for these cli arguments
    assert arguments.definitions_file == "definitions.yaml"
    assert arguments.duts_file == "duts.yaml"
    assert arguments.environment == "test"
    assert not arguments.markers


def test_setup_vane(loginfo, mocker):
    """Validates functionality of setup_vane method"""

    # mocking these methods since they have been tested in tests_tools tests
    mocker.patch("vane.tests_tools.import_yaml")
    mocker.patch("vane.tests_tools.return_test_defs")
    mocker.patch("vane.tests_tools.return_show_cmds")
    mocker.patch("vane.tests_tools.init_duts")

    vane_cli.setup_vane()

    # assert logs to ensure the method executed without errors
    loginfo_calls = [
        call("Starting Test Suite setup"),
        call("Discovering show commands from definitions"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)


def test_run_tests(loginfo, mocker):
    """Validates functionality of run_tests method"""

    # mocking these methods since they have been tested in tests_client tests
    mocker.patch("vane.tests_client.TestsClient")
    mocker.patch("vane.vane_cli.setup_vane")

    vane_cli.run_tests("", "")

    loginfo.assert_called_with("Using class TestsClient to create vane_tests_client object")


def test_write_results(loginfo, mocker):
    """Validates functionality of write_results method"""

    # mocking these methods since they have been tested in report_client tests
    mocker.patch("vane.report_client.ReportClient")

    vane_cli.write_results("")
    loginfo.assert_called_with("Using class ReportClient to create vane_report_client object")


def test_write_steps():
    """Validates the functionality of the script which writes .md and .json with test steps
    for test files. REQUIRES there to be a unittests/fixtures/test_steps/test_steps.py existing
    in this folder for test to pass"""

    assert not os.path.exists("fixtures/test_steps/test_steps.md")
    assert not os.path.exists("fixtures/test_steps/test_steps.json")

    vane_cli.write_test_steps(["fixtures/test_steps"])
    expected_output = [
        "#  Testcase for verification of syslog logging server and\n",
        "            source-interface information\n",
        "\n",
        "1.  Running show logging command on dut and collecting the text output\n",
        "2.  Checking logging source interface and Logging to string in output\n",
        "3.  Collecting logging interface and IP address from command output\n",
        "4.  Collecting information of syslog logging port and vrf details from command\n",
        "            output\n",
        "5.  Comparing source-interface, port and vrf details from actual output\n",
        "        with the expected output details\n",
        "\n",
        "#  Testcase for veification of syslog events on configured server\n",
        "\n",
        "1.  Creating Testops class object and initializing the variable\n",
        "2.  Running Tcpdump on syslog server and entering in config mode\n",
        "            and existing to verify logging event are captured.\n",
        "3.  Comparing the actual output and expected output. Generating docx report\n",
    ]

    assert os.path.exists("fixtures/test_steps/test_steps.md")
    assert os.path.exists("fixtures/test_steps/test_steps.json")

    with open("fixtures/test_steps/test_steps.md", "r", encoding="utf-8") as file_pointer:
        content = file_pointer.readlines()
        # trimming out the date and time details from the md file
        # as they will vary per test run
        final_content = content[5:]
        assert final_content == expected_output

    os.remove("fixtures/test_steps/test_steps.md")
    os.remove("fixtures/test_steps/test_steps.json")


def test_show_markers():
    """Validates the functionality of show_markers method and ensures
    we keep a log of available markers"""

    expected_output = [
        {"marker": "filesystem", "description": "EOS File System Test Suite"},
        {"marker": "daemons", "description": "EOS daemons Test Suite"},
        {"marker": "extensions", "description": "EOS extensions Test Suite"},
        {"marker": "users", "description": "EOS users Test Suite"},
        {"marker": "tacacs", "description": "TACACS Test Suite"},
        {"marker": "aaa", "description": "AAA Test Suite"},
        {"marker": "host", "description": "Host status Test Suite"},
        {"marker": "base_feature", "description": "Run all base feature test suites"},
        {"marker": "platform_status", "description": "Run all DUT platform status test suites"},
        {
            "marker": "authorization",
            "description": "Run all authorization test cases in AAA Test Suite",
        },
        {
            "marker": "authentication",
            "description": "Run all authentication test cases in AAA Test Suite",
        },
        {"marker": "accounting", "description": "Run all accounting test cases in AAA Test Suite"},
        {"marker": "api", "description": "API Test Suite"},
        {"marker": "dns", "description": "DNS Test Suite"},
        {"marker": "logging", "description": "Logging Test Suite"},
        {"marker": "ztp", "description": "Zero Touch Provisioning Test Suite"},
        {"marker": "ntp", "description": "NTP Test Suite"},
        {"marker": "nrfu", "description": "Network Ready For Use Test Cases"},
        {"marker": "pytest", "description": "PyTest Test Suite"},
        {"marker": "environment", "description": "Environment Test Suite"},
        {"marker": "cpu", "description": "CPU Test Suite"},
        {"marker": "memory", "description": "Memory Test Suite"},
        {"marker": "interface", "description": "Interface Test Suite"},
        {
            "marker": "interface_baseline_health",
            "description": "Run all interface baseline health test suites",
        },
        {"marker": "l2_protocols", "description": "Run all L2 protocol test suites"},
        {"marker": "lldp", "description": "Memory Test Suite"},
        {"marker": "system", "description": "System Test Suite"},
        {"marker": "demo", "description": "Tests ready to demo"},
        {"marker": "physical", "description": "Tests that can run on physical hardware"},
        {"marker": "virtual", "description": "Tests that can run on vEOS"},
        {"marker": "eos424", "description": "Validated tests with EOS 4.24"},
        {"marker": "ssh", "description": "Verify SSH version"},
        {
            "marker": "xdist_group",
            "description": "specify group for tests should run in "
            "same session.in relation to one another. Provided by pytest-xdist.",
        },
    ]
    actual_output = vane_cli.show_markers()
    assert actual_output == expected_output


def test_create_duts_from_topo():
    """Validates functionality of create_duts_from_topo method.
    REQUIRES there to be a unittests/fixtures/test_topology.yaml
    in this folder for test to pass"""

    topology_file = "fixtures/test_topology.yaml"
    vane_cli.create_duts_from_topo(topology_file)
    # validates the creation of the duts file, its content is tested in the test
    # written for test_tools.generate_duts_file
    assert os.path.isfile("fixtures/test_topology.yaml_duts.yaml")
    os.remove("fixtures/test_topology.yaml_duts.yaml")


def test_download_test_results(loginfo, mocker):
    """Validates if a zip archive got created and stored in the TEST RESULTS
    ARCHIVE folder"""

    # mocking these methods since ...
    mocker.patch("os.path.exists")
    mocker.patch("shutil.make_archive")

    vane_cli.download_test_results()

    loginfo.assert_called_with("Downloading a zip file of the TEST RESULTS folder")


def test_main(loginfo, logwarning, mocker):
    """Validates the main method gets executed correctly and for given cli flag
    correct steps get executed"""

    # mocking these common methods across all subtests defined below
    mocker.patch("vane.vane_cli.run_tests")
    mocker.patch("vane.vane_cli.write_results")
    mocker.patch("vane.vane_cli.download_test_results")

    def test_main_definitions_and_duts(mocker):
        """Tests the --definitions-file and --duts-file flag"""
        # mocking parse cli to test --definitions-file and --duts-file flag
        mocker.patch(
            "vane.vane_cli.parse_cli",
            return_value=argparse.Namespace(
                definitions_file="definitions_sample.yaml",
                duts_file="duts_sample.yaml",
                environment="test",
                generate_duts_file=None,
                generate_duts_from_topo=None,
                generate_test_steps=None,
                markers=False,
            ),
        )
        vane_cli.main()

    def test_main_create_duts_file(mocker):
        """Tests the --generate-duts-file flag"""
        mocker.patch("vane.tests_tools.create_duts_file")
        # mocking parse cli to test --generate-duts-file
        mocker.patch(
            "vane.vane_cli.parse_cli",
            return_value=argparse.Namespace(
                definitions_file="definitions_sample.yaml",
                duts_file="duts_sample.yaml",
                environment="test",
                generate_duts_file=["topology.yaml", "inventory.yaml"],
                generate_duts_from_topo=None,
                generate_test_steps=None,
                markers=False,
            ),
        )
        vane_cli.main()

    def test_main_generate_duts_from_topo(mocker):
        """Tests the --generate-duts-from-topo flag"""
        mocker.patch("vane.vane_cli.create_duts_from_topo")
        # mocking parse cli to test --generate-duts-from-topo
        mocker.patch(
            "vane.vane_cli.parse_cli",
            return_value=argparse.Namespace(
                definitions_file="definitions_sample.yaml",
                duts_file="duts_sample.yaml",
                environment="test",
                generate_duts_file=None,
                generate_duts_from_topo=["topology.yaml"],
                generate_test_steps=None,
                markers=False,
            ),
        )
        vane_cli.main()

    def test_main_write_test_steps(mocker):
        """Tests the --generate-test-steps flag"""
        mocker.patch("vane.vane_cli.write_test_steps")
        # mocking parse cli to test --generate-test-steps
        mocker.patch(
            "vane.vane_cli.parse_cli",
            return_value=argparse.Namespace(
                definitions_file="definitions_sample.yaml",
                duts_file="duts_sample.yaml",
                environment="test",
                generate_duts_file=None,
                generate_duts_from_topo=None,
                generate_test_steps="test_directory",
                markers=False,
            ),
        )
        vane_cli.main()

    test_main_definitions_and_duts(mocker)
    test_main_create_duts_file(mocker)
    test_main_generate_duts_from_topo(mocker)
    test_main_write_test_steps(mocker)

    # assert info logs to ensure all the above methods executed without errors
    loginfo_calls = [
        call("Reading in input from command-line"),
        call("\n\n!VANE has completed without errors!\n\n"),
        call("Reading in input from command-line"),
        call(
            "Generating DUTS File from topology: topology.yaml and "
            "inventory: inventory.yaml file.\n"
        ),
        call("\n\n!VANE has completed without errors!\n\n"),
        call("Reading in input from command-line"),
        call("Generating DUTS File from topology: topology.yaml file.\n"),
        call("\n\n!VANE has completed without errors!\n\n"),
        call("Reading in input from command-line"),
        call("Generating test steps for test cases within test_directory test directory\n"),
    ]
    loginfo.assert_has_calls(loginfo_calls, any_order=False)

    # assert warning logs to ensure all the above methods executed without errors
    logwarning_calls = [
        call("Changing Definitions file name to definitions_sample.yaml"),
        call("Changing DUTS file name to duts_sample.yaml"),
        call("Changing Definitions file name to definitions_sample.yaml"),
        call("Changing DUTS file name to duts_sample.yaml"),
        call("Changing Definitions file name to definitions_sample.yaml"),
        call("Changing DUTS file name to duts_sample.yaml"),
    ]
    logwarning.assert_has_calls(logwarning_calls, any_order=False)
