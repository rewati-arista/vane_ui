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
from vane.vane_logging import logging


class NrfuClient:
    """Creates an instance of the NRFU Client."""

    def __init__(self):
        """NrfuClient initialisation"""
        # Getting credentials from user
        username, password = self.get_credentials()

        # Determine if Vane is running as CVP application
        cvp = self.determine_if_cvp_application()

        if cvp:
            self.cvp_application()
        else:
            self.not_cvp_application()

    def get_credentials(self):
        """Ask user to enter credentials for EOS/CloudVision"""
        username = input("Please input Arista device username: ")
        password = getpass.getpass("Please input Arista device password: ")
        return username, password

    def determine_if_cvp_application(self):
        """Determine if Vane is running as CVP application"""
        return False

    def cvp_application(self):
        """Steps to take if Vane is running as CVP application"""
        pass

    def not_cvp_application(self):
        """Steps to take if Vane is not running as CVP application"""
        source = ""
        while source not in ("y", "yes", "n", "no"):
            source = input("Do you wish to use CVP for DUTs [y/yes/n/no]: ")
            source = source.lower()

        if source in ("y", "yes"):
            ip_address = input("Please input CVP IP address: ")
        else:
            device_list_file = ""
            text_flag = False
            while not os.path.exists(device_list_file) or not text_flag:
                device_list_file = input("Please input Name/Path of device list file (.txt): ")
                if len(device_list_file) > 4 and device_list_file[-4:] == ".txt":
                    text_flag = True
            device_list = self.read_device_list_file(device_list_file)

    def read_device_list_file(self, device_list_file):
        """Read IP addresses per DUT

        Args:
        device_list_file (str): Name of the DUT ip file

        Returns:
        device_list (list): List of DUT ips"""

        device_list = []
        try:
            with open(device_list_file, "r", encoding="utf-8") as text_in:
                line = text_in.readline()
                while line:
                    # Process each line here, use strip() to remove newline characters
                    device_list.append(line.strip())
                    line = text_in.readline()
        except OSError as err:
            logging.error(f"ERROR OPENING DEVICE LIST FILE: {err}")
            sys.exit(1)

        return device_list
