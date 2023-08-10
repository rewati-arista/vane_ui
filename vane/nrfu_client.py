#!/usr/bin/env python3
#
# Copyright (c) 2023, Arista Networks EOS+
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
# pylint: disable=too-few-public-methods, unused-variable

"""Utilities for NRFU testing"""
import getpass
import os
import sys
import yaml
from cvprac.cvp_client import CvpClient
from cvprac.cvp_api import CvpApi
from vane.vane_logging import logging


class NrfuClient:
    """Creates an instance of the NRFU Client."""

    def __init__(self):
        """NrfuClient initialisation"""

        # Getting credentials from user
        self.username, self.password = self.get_credentials()

        # Determine if Vane is running as CVP application
        self.cvp = self.determine_if_cvp_application()

        # Depending on if it is CVP application or not,
        # get the device data to generate duts.yaml file
        if self.cvp:
            device_data, source = self.cvp_application()
        else:
            device_data, source = self.not_cvp_application()

        # Generate duts_nrfu.yaml file from the duts data gathered above
        self.generate_duts_file(device_data, source)

    def get_credentials(self):
        """Ask user to enter credentials for EOS/CloudVision

        Returns:
        username (string): EOS/CloudVision username
        password (string): EOS/CloudVision password
        """

        username = input("Please input Arista device username: ")
        password = getpass.getpass("Please input Arista device password: ")
        return username, password

    def determine_if_cvp_application(self):
        """Determine if Vane is running as CVP application

        Returns:
        boolean: flag indicating if Vane is running as CVP application
        """

        logging.info("Determining if Vane is running as a CVP application")
        if os.environ.get("VANE_CVP"):
            logging.info("Vane is running as a CVP application")
            return True

        logging.info("Vane is not running as a CVP application")
        return False

    def cvp_application(self):
        """Steps to take if Vane is running as CVP application

        Returns:
        device_data (list(list)): Device data read from CVP
        source (string): flag indicating the source of device data
        """

        ip_address = "127.0.0.1"
        source = "cvp"
        logging.info("Using CVP to gather duts data")
        print("Using CVP to gather duts data")
        device_data = self.get_duts_data(ip_address)
        return device_data, source

    def not_cvp_application(self):
        """Steps to take if Vane is not running as CVP application

        Returns:
        device_data (list(list) or list): Device data read from either CVP or device file
        source (string): flag indicating the source of device data
        """

        user_choice = ""
        device_data = []
        while user_choice not in ("y", "yes", "n", "no"):
            user_choice = input("Do you wish to use CVP for DUTs [y/yes/n/no]: ")
            user_choice = user_choice.lower()

        if user_choice in ("y", "yes"):
            source = "cvp"
            ip_address = input("Please input CVP IP address: ")
            device_data = self.get_duts_data(ip_address)

        else:
            source = "non-cvp"
            device_list_file = ""
            text_flag = False
            while not os.path.exists(device_list_file) or not text_flag:
                device_list_file = input("Please input Name/Path of device list file (.txt): ")
                if len(device_list_file) > 4 and device_list_file[-4:] == ".txt":
                    text_flag = True
            device_data = self.read_device_list_file(device_list_file)
        return device_data, source

    def get_duts_data(self, ip_address):
        """Gets inventory data from CVP

        Args:
        ip_address (string): CVP's ip address

        Returns:
        device_data (list(list)): Device data gathered from CVP
        """

        logging.info("Connecting to CVP to gather duts data")

        device_data = []
        client = CvpClient()
        client.connect([ip_address], self.username, self.password)
        cvp_api = CvpApi(client)

        # Get the inventory using get_inventory API call
        inventory = cvp_api.get_inventory()

        # Process inventory data as specified to generate duts.yaml
        for device in inventory:
            if device["streamingStatus"] == "active":
                current_device_data = [device["hostname"], device["ipAddress"]]
                device_data.append(current_device_data)

        return device_data

    def read_device_list_file(self, device_list_file):
        """Read IP addresses per DUT

        Args:
        device_list_file (str): Name of the DUT ip file

        Returns:
        device_data (list): Device data in the form of list of DUT ips"""

        device_data = []
        try:
            with open(device_list_file, "r", encoding="utf-8") as text_in:
                logging.info("Reading in dut ip data from device list file")
                line = text_in.readline()
                while line:
                    # Process each line here, use strip() to remove newline characters
                    device_data.append(line.strip())
                    line = text_in.readline()
        except OSError as err:
            logging.error(f"ERROR OPENING DEVICE LIST FILE: {err}")
            sys.exit(1)

        return device_data

    def generate_duts_file(self, device_data, source):
        """Processes the duts data to be written to the duts.yaml file

        Args:
        device_data (list): Device data provided by source
        source (string): flag indicating if source of data is cvp or not
        """

        duts_yaml_data = []

        for device in device_data:
            # device data in this case is a list of [device hostnames, device ips]
            if source == "cvp":
                name = device[0]
                ip_address = device[1]
            # device data in this case is a list of device ips
            else:
                ip_address = name = device
            current_device_data = {
                "mgmt_ip": ip_address,
                "name": name,
                "neighbors": [],
                "password": self.password,
                "transport": "https",
                "username": self.username,
                "role": "unknown",
            }
            duts_yaml_data.append(current_device_data)
        final_duts_data = {"duts": duts_yaml_data}

        logging.info("Generating duts_nrfu.yaml file for NRFU testing")
        self.write_duts(final_duts_data)

    def write_duts(self, final_duts_data):
        """Generates and writes to the duts.yaml file the processed data which is passed in

        Args:
        final_duts_data (list(dict)): List of device data (ip, name, neighbors, ...)
        """

        duts_file = "duts_nrfu.yaml"

        try:
            with open(duts_file, "w", encoding="utf-8") as file:
                try:
                    yaml.dump(final_duts_data, file, default_flow_style=False)
                except yaml.YAMLError as err:
                    logging.error(f"ERROR IN YAML FILE: {err}")
                    sys.exit(1)
        except OSError as err:
            print(f">>> {duts_file} YAML FILE MISSING")
            logging.error(f"ERROR YAML FILE: {duts_file} NOT " + f"FOUND. {err}")
            sys.exit(1)
