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

"""Tests to validate interfaces status."""

from pprint import pprint
import pytest
from . import common_nrfu_infra
import os
from . import definitions

# List EOS show commands to use in test cases
EOS_SHOW_CMDS = ["show interfaces",
                 "show interfaces status",
                 "show interfaces phy detail",
                 "show interfaces transceiver detail",
                 "show interfaces transceiver properties",
                 "show interfaces mac detail",
                 "show interfaces negotiation detail",
                 "show interfaces counters errors",
                 "show interfaces counters discards",
                 "show interfaces"]

# PyTest from Test Engine 
if os.path.isfile(definitions.TEST_DEFINITION_FILE): 
    TEST_DEFINITION = common_nrfu_infra.import_test_definition()
    CONNECTION_LIST = common_nrfu_infra.generate_connection_list(TEST_DEFINITION)
    common_nrfu_infra.open_log_file()
    TEST_SUITE = __file__.split("/")[-1]
    DUTS = common_nrfu_infra.generate_dut_info_threaded(EOS_SHOW_CMDS, TEST_SUITE)
#Native PyTest
else:
    XLSX_WORKBOOK = common_nrfu_infra.import_spreadsheet()
    CONNECTION_LIST = common_nrfu_infra.return_connection_list(XLSX_WORKBOOK)
    common_nrfu_infra.open_log_file()
    TEST_SUITE = __file__.split("/")[-1]
    DUTS = common_nrfu_infra.return_dut_info_threaded(EOS_SHOW_CMDS, TEST_SUITE)


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_description(dut):
    """ Verify the interfaces of interest have the correct description

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        candidate_description = "%s-Eth%s" % (
            interface['z_hostname'], interface['z_interface_name'].split()[1])
        interface_name = interface['interface_name'].replace(" ", "")
        production_description = \
            dut["output"][show_cmd]['json']['interfaces'][interface_name]['description\
']

        print(f"  - On interface |{interface_name}|: correct interface description \
is set to: |{candidate_description}|, production interface description is \
set to: |{production_description}|")

        assert candidate_description == production_description


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_phy_detail_interfacestate(dut):
    """ Verify the interfaces of interest Interface state is link up

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces phy detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        show_phys = \
            dut["output"][show_cmd]['json']['interfacePhyStatuses\
'][interface_name]['phyStatuses'][0]['text']
        show_phys = show_phys.split('\n')

        for phyiscial_property in show_phys:
            if "Interface state" in phyiscial_property:
                phy_state = phyiscial_property.split()[2]

                print(f"  - On interface |{interface['interface_name']}|: interface physical \
detail interface state is set to: |{phy_state}|, correct state is |up|")

                assert phy_state == 'up'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_phy_detail_diagmode(dut):
    """ Verify the interfaces of interest Diags mode is normal Operation

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces phy detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        show_phys = \
            dut["output"][show_cmd]['json']['interfacePhyStatuses\
'][interface_name]['phyStatuses'][0]['text']
        show_phys = show_phys.split('\n')

        for phyiscial_property in show_phys:
            if "Diags mode" in phyiscial_property:
                phy_state = phyiscial_property.split()[2]

                print(f"  - On interface |{interface['interface_name']}|: \
interface physical detail diagnosis mode is set to: |{phy_state}|, \
correct state is |normalOperation|")

                assert phy_state == 'normalOperation'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_phy_loopback(dut):
    """ Verify the interfaces of loopback is none

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces phy detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        show_phys = \
            dut["output"][show_cmd]['json']['interfacePhyStatuses\
'][interface_name]['phyStatuses'][0]['text']
        show_phys = show_phys.split('\n')

        for phyiscial_property in show_phys:
            if "Loopback" in phyiscial_property:
                phy_state = phyiscial_property.split()[1]

                print(f"  - On interface |{interface['interface_name']}|: interface physical \
loopback mode is set to: |{phy_state}|, correct state is |none|")

                assert phy_state == 'none'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_phy_pmapmd_rx(dut):
    """ Verify the interfaces of PMA/PMD RX signal detect is ok

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces phy detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        show_phys = \
            dut["output"][show_cmd]['json']['interfacePhyStatuses\
'][interface_name]['phyStatuses'][0]['text']
        show_phys = show_phys.split('\n')

        for phyiscial_property in show_phys:
            if "PMA/PMD RX signal detect" in phyiscial_property:
                phy_state = phyiscial_property.split()[4]

                print(f"  - On interface |{interface['interface_name']}|: interface PMA/PMD \
RX signal detect is set to: |{phy_state}|, correct state is |ok|")

                assert phy_state == 'ok'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_phy_pcs_rx_link_status(dut):
    """ Verify the interfaces of PCS RX link status is up

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces phy detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        show_phys = \
            dut["output"][show_cmd]['json']['interfacePhyStatuses\
'][interface_name]['phyStatuses'][0]['text']
        show_phys = show_phys.split('\n')

        for phyiscial_property in show_phys:
            if "PCS RX link status" in phyiscial_property:
                phy_state = phyiscial_property.split()[4]

                print(f"  - On interface |{interface['interface_name']}|: interface PCS RX \
link status is set to: |{phy_state}|, correct state is |up|")

                assert phy_state == 'up'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_phy_pcs_high_ber(dut):
    """ Verify the interfaces of PCS high BER is ok

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces phy detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        show_phys = \
            dut["output"][show_cmd]['json']['interfacePhyStatuses\
'][interface_name]['phyStatuses'][0]['text']
        show_phys = show_phys.split('\n')

        for phyiscial_property in show_phys:
            if "PCS high BER" in phyiscial_property:
                phy_state = phyiscial_property.split()[3]

                print(f"  - On interface |{interface['interface_name']}|: interface PCS high \
BER is set to: |{phy_state}|, correct state is |ok|")

                assert phy_state == 'ok'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_phy_pcs_block_lock(dut):
    """ Verify the interfaces of PCS block lock is ok

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces phy detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        show_phys = \
            dut["output"][show_cmd]['json']['interfacePhyStatuses\
'][interface_name]['phyStatuses'][0]['text']
        show_phys = show_phys.split('\n')

        for phyiscial_property in show_phys:
            if "PCS block lock" in phyiscial_property:
                phy_state = phyiscial_property.split()[3]

                print(f"  - On interface |{interface['interface_name']}|: interface PCS block \
lock is set to: |{phy_state}|, correct state is |ok|")

                assert phy_state == 'ok'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_phy_pcs_ber(dut):
    """ Verify the interfaces of PCS BER is ok

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces phy detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        show_phys = \
            dut["output"][show_cmd]['json']['interfacePhyStatuses\
'][interface_name]['phyStatuses'][0]['text']
        show_phys = show_phys.split('\n')

        for phyiscial_property in show_phys:
            if "PCS BER" in phyiscial_property:
                phy_state = phyiscial_property.split()[3]

                print(f"  - On interface |{interface['interface_name']}|: interface PCS BER is \
set to: |{phy_state}|, correct state is |0|")

                assert int(phy_state) == 0


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
@pytest.mark.xfail
def test_show_idprom_transceiver(dut):
    """ Verify the ethernet idprom tranceiver

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show idprom transceiver"
    show_idprom = dut["output"][show_cmd]['text']

    print(f"\nNO AUTOMATED TEST.  MUST TEST MANUALLY")
    print(f"On router |{dut['name']}| show idprom transceiver:\
        \n{show_idprom}")

    assert False


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_transceiver_properties(dut):
    """ Verify the interface transceiver speed is auto

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    test_show_interfaces_transceiver_properties_speed(dut)
    test_show_interfaces_transceiver_properties_duplex(dut)
    test_show_interfaces_transceiver_properties_operational_duplex(dut)
    test_show_interfaces_transceiver_media_type(dut)


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_transceiver_properties_speed(dut):
    """ Verify the interface transceiver speed is auto

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces transceiver properties"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_nunmber = interface['interface_name'].split()[1]
        show_name = f"Name : Et{interface_nunmber}"
        show_transceivers = dut["output"][show_cmd]['text']
        show_transceivers = show_transceivers.split('\n')
        in_scope_flag = False

        for show_transceiver in show_transceivers:
            if show_name == show_transceiver:
                in_scope_flag = True
            elif "Name :" in show_transceiver and in_scope_flag:
                in_scope_flag = False

            if "Administrative Speed" in show_transceiver and in_scope_flag:
                phy_state = show_transceiver.split()[2]

                print(f"  - On interface |{interface['interface_name']}|: interface \
transceiver properties speed is set to: |{phy_state}|, correct state is \
|auto|")

                assert phy_state == "auto"


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_transceiver_properties_duplex(dut):
    """ Verify the interface transceiver duplex is auto

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces transceiver properties"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_nunmber = interface['interface_name'].split()[1]
        show_name = f"Name : Et{interface_nunmber}"
        show_transceivers = dut["output"][show_cmd]['text']
        show_transceivers = show_transceivers.split('\n')
        in_scope_flag = False

        for show_transceiver in show_transceivers:
            if show_name == show_transceiver:
                in_scope_flag = True
            elif "Name :" in show_transceiver and in_scope_flag:
                in_scope_flag = False

            if "Administrative Duplex" in show_transceiver and in_scope_flag:
                phy_state = show_transceiver.split()[2]

                print(f"  - On interface |{interface['interface_name']}|: interface \
transceiver properties duplex is set to: |{phy_state}|, correct state \
is |auto|")

                assert phy_state == "auto"


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_transceiver_properties_operational_duplex(dut):
    """ Verify the interface transceiver operational duplex is full

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces transceiver properties"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_nunmber = interface['interface_name'].split()[1]
        show_name = f"Name : Et{interface_nunmber}"
        show_transceivers = dut["output"][show_cmd]['text']
        show_transceivers = show_transceivers.split('\n')
        in_scope_flag = False

        for show_transceiver in show_transceivers:
            if show_name == show_transceiver:
                in_scope_flag = True
            elif "Name :" in show_transceiver and in_scope_flag:
                in_scope_flag = False

            if "Operational Duplex" in show_transceiver and in_scope_flag:
                phy_state = show_transceiver.split()[2]

                print(f"  - On interface |{interface['interface_name']}|: interface \
transceiver properties operational duplex is set to: \
|{('full' in phy_state)}|, correct state is |True|")

                assert ("full" in phy_state) is True


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_transceiver_media_type(dut):
    """ Verify the interface transceiver media type is correct

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces transceiver properties"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_nunmber = interface['interface_name'].split()[1]
        show_name = f"Name : Et{interface_nunmber}"
        show_transceivers = dut["output"][show_cmd]['text']
        show_transceivers = show_transceivers.split('\n')
        in_scope_flag = False

        for show_transceiver in show_transceivers:
            if show_name == show_transceiver:
                in_scope_flag = True
            elif "Name :" in show_transceiver and in_scope_flag:
                in_scope_flag = False

            if "Media Type" in show_transceiver and in_scope_flag:
                phy_state = show_transceiver.split()[2]

                print(f"  - On interface |{interface['interface_name']}|: interface \
transceiver media type is set to: |{phy_state}|, correct state is \
|{interface['media_type']}|")

                assert phy_state == interface['media_type']


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
@pytest.mark.xfail
def test_show_interfaces_transceiver_detail(dut):
    """ Verify the ethernet idprom tranceiver

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces transceiver detail"
    show_transceiver = dut["output"][show_cmd]['text']

    print(f"\nNO AUTOMATED TEST.  MUST TEST MANUALLY")
    print(f"On router |{dut['name']}| show interfaces transceiver \
detail:\n{show_transceiver}")

    assert False


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_mac_detail(dut):
    """ Verify the interface mac detail interface state is linkUp

       Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    test_show_interfaces_mac_detail_phy_state(dut)
    test_show_interfaces_mac_detail_interface_state(dut)
    test_show_interfaces_mac_detail_mac_rx_local_fault(dut)
    test_show_interfaces_mac_detail_mac_rx_remote_fault(dut)


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_mac_detail_phy_state(dut):
    """ Verify the interface mac detail physical state is linkUp

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces mac detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        show_name = interface['interface_name'].replace(" ", "")
        show_macs = dut["output"][show_cmd]['text']
        show_macs = show_macs.split('\n')
        in_scope_flag = False

        for show_mac in show_macs:
            if show_name == show_mac:
                in_scope_flag = True
            elif "Ethernet" in show_mac and in_scope_flag:
                in_scope_flag = False

            if "PHY State" in show_mac and in_scope_flag:
                phy_state = show_mac.split()[2]

                print(f"  - On interface |{interface['interface_name']}|: interface MAC detail \
PHY state is set to: |{phy_state}|, correct state is |linkUp|")

                assert phy_state == 'linkUp'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_mac_detail_interface_state(dut):
    """ Verify the interface mac detail interface state is linkUp

       Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces mac detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        show_name = interface['interface_name'].replace(" ", "")
        show_macs = dut["output"][show_cmd]['text']
        show_macs = show_macs.split('\n')
        in_scope_flag = False

        for show_mac in show_macs:
            if show_name == show_mac:
                in_scope_flag = True
            elif "Ethernet" in show_mac and in_scope_flag:
                in_scope_flag = False

            if "Interface State" in show_mac and in_scope_flag:
                phy_state = show_mac.split()[2]

                print(f"  - On interface |{interface['interface_name']}|: interface MAC detail \
interface state is set to: |{phy_state}|, correct state is |linkUp|")

                assert phy_state == 'linkUp'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_mac_detail_mac_rx_local_fault(dut):
    """ Verify the interface mac detail MAC Rx Local Fault is False

       Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces mac detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        show_name = interface['interface_name'].replace(" ", "")
        show_macs = dut["output"][show_cmd]['text']
        show_macs = show_macs.split('\n')
        in_scope_flag = False

        for show_mac in show_macs:
            if show_name == show_mac:
                in_scope_flag = True
            elif "Ethernet" in show_mac and in_scope_flag:
                in_scope_flag = False

            if "MAC Rx Local Fault" in show_mac and in_scope_flag:
                phy_state = show_mac.split()[4]

                print(f"  - On interface |{interface['interface_name']}|: interface MAC detail \
Rx Local Fault state is set to: |{phy_state}|, correct state is |False|")

                assert phy_state == 'False'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_mac_detail_mac_rx_remote_fault(dut):
    """ Verify the interface mac detail MAC Rx remote Fault is False

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces mac detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        show_name = interface['interface_name'].replace(" ", "")
        show_macs = dut["output"][show_cmd]['text']
        show_macs = show_macs.split('\n')
        in_scope_flag = False

        for show_mac in show_macs:
            if show_name == show_mac:
                in_scope_flag = True
            elif "Ethernet" in show_mac and in_scope_flag:
                in_scope_flag = False

            if "MAC Rx Remote Fault" in show_mac and in_scope_flag:
                phy_state = show_mac.split()[4]

                print(f"  - On interface |{interface['interface_name']}|: interface MAC \
detail Rx remote Fault state is set to: |{phy_state}|, \
correct state is |False|")

                assert phy_state == 'False'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_negotiation_detail(dut):
    """ Verify the interface negotiation detail is successful

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces negotiation detail"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        show_name = interface['interface_name'].replace(" ", "")
        show_macs = dut["output"][show_cmd]['text']
        show_macs = show_macs.split('\n')
        in_scope_flag = False

        for show_mac in show_macs:
            if show_name == show_mac:
                in_scope_flag = True
            elif "Ethernet" in show_mac and in_scope_flag:
                in_scope_flag = False

            if "Auto-Negotiation Status" in show_mac and in_scope_flag:
                phy_state = show_mac.split()[2]

                print(f"  - On interface |{interface['interface_name']}|: interface \
negotiation detail Rx auto-negotiation status is set to: \
|{phy_state}|, correct state is |Success|")

                assert phy_state == 'Success'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_count_discards(dut):
    """ Verify the interfaces of interest have no inDiscards

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    test_show_interfaces_count_discards_out_discards(dut)
    test_show_interfaces_count_discards_in_discards(dut)


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_count_discards_out_discards(dut):
    """ Verify the interfaces of interest have no outDiscards

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces counters discards"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        int_discards = \
            dut["output"][show_cmd]['json']['interfaces\
'][interface_name]['outDiscards']

        print(f"  - On interface |{interface_name}|: interface counter discards has \
            |{int_discards}| outDiscards, correct state is |0|")

        assert int(int_discards) == 0


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_count_discards_in_discards(dut):
    """ Verify the interfaces of interest have no inDiscards

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces counters discards"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        int_discards = \
            dut["output"][show_cmd]['json']['interfaces\
'][interface_name]['inDiscards']

        print(f"  - On interface |{interface_name}|: interface counter discards has \
|{int_discards}| inDiscards, correct state is |0|")

        assert int(int_discards) == 0


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_interfaces_mtu(dut):
    """ Verify the interfaces of interest have mtu of 10178

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show interfaces"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        int_mtu = \
            dut["output"][show_cmd]['json']['interfaces\
'][interface_name]['mtu']

        print(f"  - On interface |{interface_name}|: interface MTU is|{int_mtu}|, \
correct state is |10178|")

        assert int(int_mtu) == 10178
