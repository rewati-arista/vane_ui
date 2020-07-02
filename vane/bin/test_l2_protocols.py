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

"""Tests to validate L2 protocol status."""

from pprint import pprint
import pytest
from . import common_nrfu_infra
import os
from . import definitions

# List EOS show commands to use in test cases
EOS_SHOW_CMDS = ["show lldp",
                 "show lldp local-info",
                 "show lldp neighbors",
                 "show lldp counters"]

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


@pytest.mark.xpass
def test_assert_true():
    """ Prior to running any tests this test Validates that PyTest is working
        correct by verifying PyTest can assert True.
    """

    assert True


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp(dut):
    """ Verify show lldp output is correct

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    test_show_lldp_rx_enabled(dut)
    test_show_lldp_tx_enabled(dut)


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_rx_enabled(dut):
    """ Verify show lldp output is correct

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        sh_lldp = \
            dut["output"][show_cmd]['json']['lldpInterfaces\
'][interface_name]['rxEnabled']

        print(f"  - On interface |{interface['interface_name']}|: interface LLDP \
rxEnabled is in state |{sh_lldp}|, correct state is |True|")

        assert sh_lldp is True


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_tx_enabled(dut):
    """ Verify show lldp output is correct

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        sh_lldp = \
            dut["output"][show_cmd]['json']['lldpInterfaces\
'][interface_name]['txEnabled']

        print(f"  - On interface |{interface['interface_name']}|: interface LLDP \
rxEnabled is in state |{sh_lldp}|, correct state is |True|")

        assert sh_lldp is True


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_local_info(dut):
    """ Verify show lldp local-info interfaceDescription is correct

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    test_show_lldp_local_info_system_name(dut)
    test_show_lldp_local_info_interface_description(dut)
    test_show_lldp_local_info_max_frame_size(dut)
    test_show_lldp_local_info_interface_id_type(dut)
    test_show_lldp_local_info_interface_id(dut)


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_local_info_system_name(dut):
    """ Verify show lldp local-info hostname is the system's name

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp local-info"
    sh_lldp = dut["output"][show_cmd]["json"]['systemName']

    print(f"\nOn router |{dut['name']}|: the LLDP the local-info hostname is \
set to |{sh_lldp}|, correct name is |{dut['name']}|")

    assert sh_lldp == dut['name']


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_local_info_interface_description(dut):
    """ Verify show lldp local-info interfaceDescription is correct

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp local-info"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        sh_lldp = \
            dut["output"][show_cmd]["json"]['localInterfaceInfo\
'][interface_name]['interfaceDescription']
        interface_description = "%s-Eth%s" % \
            (interface['z_hostname'], interface['z_interface_name'].split()[1])

        print(f"  - On interface |{interface['interface_name']}|: LLDP local-info \
description is |{sh_lldp}|, correct description is |{interface_description}|")

        assert sh_lldp == interface_description


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_local_info_max_frame_size(dut):
    """ Verify show lldp local-info maxFrameSize is 10200

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp local-info"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        sh_lldp = \
            dut["output"][show_cmd]["json"]['localInterfaceInfo\
'][interface_name]['maxFrameSize']

        print(f"  - On interface |{interface['interface_name']}|: LLDP local-info \
            maxFrameSize is |{sh_lldp}|, correct maxFrameSize is |10200|")

        assert int(sh_lldp) == 10200


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_local_info_interface_id_type(dut):
    """ Verify show lldp local-info interfaceIdType is interfaceName

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp local-info"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        sh_lldp = \
            dut["output"][show_cmd]["json"]['localInterfaceInfo\
'][interface_name]['interfaceIdType']

        print(f"  - On interface |{interface['interface_name']}|: LLDP local-info \
interfaceIdType is |{sh_lldp}|, correct interfaceIdType is |interfaceName|")

        assert sh_lldp == 'interfaceName'


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_local_info_interface_id(dut):
    """ Verify show lldp local-info interfaceId is interface name

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp local-info"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        sh_lldp = \
            dut["output"][show_cmd]["json"]['localInterfaceInfo\
'][interface_name]['interfaceId']

        print(f"  - On interface |{interface['interface_name']}|: LLDP local-info \
interfaceIdType state is |{(interface_name in sh_lldp)}|, \
correct interfaceIdType state is |True|")

        assert (interface_name in sh_lldp) is True


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_neighbor(dut):
    """ Verify show lldp neighbor device is correct

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    test_show_lldp_neighbor_neighbor_device(dut)
    test_show_lldp_neighbor_neighbor_port(dut)
    test_show_lldp_neighbor_ttl(dut)


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_neighbor_neighbor_device(dut):
    """ Verify show lldp neighbor device is correct

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp neighbors"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        sh_lldp = dut["output"][show_cmd]["json"]['lldpNeighbors']
        lldp_port_list = [lldp_neighbor_dict['port']
                          for lldp_neighbor_dict in sh_lldp]

        if interface_name in lldp_port_list:
            lldp_port_index = lldp_port_list.index(interface_name)
            lldp_device = sh_lldp[lldp_port_index]['neighborDevice']

            print(f"  - On interface |{interface['interface_name']}|: LLDP neighbor \
device is |{lldp_device}|, correct neighbor device is \
|{interface['z_hostname']}|")

            assert lldp_device == interface['z_hostname']


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_neighbor_neighbor_port(dut):
    """ Verify show lldp neighbor port is correct

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp neighbors"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        sh_lldp = dut["output"][show_cmd]["json"]['lldpNeighbors']
        lldp_port_list = [lldp_neighbor_dict['port']
                          for lldp_neighbor_dict in sh_lldp]

        if interface_name in lldp_port_list:
            lldp_port_index = lldp_port_list.index(interface_name)
            lldp_port = sh_lldp[lldp_port_index]['neighborPort']

            print(f"  - On interface |{interface['interface_name']}|: LLDP neighbor \
interface is |{lldp_port}|, correct neighbor interface is \
|{interface['z_interface_name'].replace(' ', '')}|")

            assert lldp_port == interface['z_interface_name'].replace(" ", "")


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_neighbor_ttl(dut):
    """ Verify show lldp neighbor ttl is 120

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp neighbors"
    sh_lldps = dut["output"][show_cmd]["json"]['lldpNeighbors']

    print(f"\nOn router |{dut['name']}|:")

    for sh_lldp in sh_lldps:
        print(f"  - On interface |{sh_lldp['port']}|: LLDP neighbor TTL is \
|{sh_lldp['ttl']}|, correct neighbor LLDP TTL is |120|")

        assert sh_lldp['ttl'] == 120


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_traffic(dut):
    """ Verify show lldp traffic tlvsDiscarded is 0

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    test_show_lldp_traffic_tlvs_discarded(dut)
    test_show_lldp_traffic_rx_discards(dut)
    test_show_lldp_traffic_rx_errors(dut)
    test_show_lldp_traffic_tlvs_unknown(dut)
    test_show_lldp_traffic_tx_frames_length_exceeded(dut)


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_traffic_tlvs_discarded(dut):
    """ Verify show lldp traffic tlvsDiscarded is 0

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp counters"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        lldp_counter = \
            dut["output"][show_cmd]["json"]['interfaces\
'][interface_name]['tlvsDiscarded']

        print(f"  - On interface |{interface['interface_name']}|: LLDP traffic counter \
tlvsDiscarded is |{lldp_counter}|, correct counter is |0|")

        assert int(lldp_counter) == 0


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_traffic_rx_discards(dut):
    """ Verify show lldp traffic rxDiscards is 0

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp counters"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        lldp_counter = \
            dut["output"][show_cmd]["json"]['interfaces\
'][interface_name]['rxDiscards']

        print(f"  - On interface |{interface['interface_name']}|: LLDP traffic counter \
rxDiscards is |{lldp_counter}|, correct counter is |0|")

        assert int(lldp_counter) == 0


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_traffic_rx_errors(dut):
    """ Verify show lldp traffic rxErrors is 0

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp counters"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        lldp_counter = \
            dut["output"][show_cmd]["json"]['interfaces\
'][interface_name]['rxErrors']

        print(f"  - On interface |{interface['interface_name']}|: LLDP traffic counter \
rxErrors is |{lldp_counter}|, correct counter is |0|")

        assert int(lldp_counter) == 0


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_traffic_tlvs_unknown(dut):
    """ Verify show lldp traffic tlvsUnknown is 0

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp counters"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        lldp_counter = \
            dut["output"][show_cmd]["json"]['interfaces\
'][interface_name]['tlvsUnknown']

        print(f"  - On interface |{interface['interface_name']}|: LLDP traffic counter \
tlvsUnknown is |{lldp_counter}|, correct counter is |0|")

        assert int(lldp_counter) == 0


@pytest.mark.parametrize("dut", DUTS, ids=CONNECTION_LIST)
def test_show_lldp_traffic_tx_frames_length_exceeded(dut):
    """ Verify show lldp traffic txFramesLengthExceeded is 0

        Args:
          dut (dict): Encapsulates dut details including name, connection
    """

    show_cmd = "show lldp counters"
    interfaces_list = dut["output"]["interface_list"]

    print(f"\nOn router |{dut['name']}|:")

    for interface in interfaces_list:
        interface_name = interface['interface_name'].replace(" ", "")
        lldp_counter = \
            dut["output"][show_cmd]["json"]['interfaces\
'][interface_name]['txFramesLengthExceeded']

        print(f"  - On interface |{interface['interface_name']}|: LLDP traffic counter \
txFramesLengthExceeded is |{lldp_counter}|, correct counter is |0|")

        assert int(lldp_counter) == 0
