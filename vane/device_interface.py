#!/usr/bin/env python3
#
# Copyright (c) 2022, Arista Networks EOS+
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

"""Device connection drivers - two types of drivers
   1. EAPI driver - uses pyeapi package
   2. ssh driver - uses Netmiko package
"""

import configparser
import pyeapi
from netmiko.ssh_autodetect import SSHDetect
from netmiko import Netmiko
import json

error_responses = [
    '% This is an unconverted command\n{\n    "errors": [\n        "This is an unconverted command"\n    ]\n}',
    '% Invalid input',
    ]

class CommandError(Exception):
    """Base exception raised for command errors
    The CommandError instance provides a custom exception that can be used
    if the Netmiko command(s) fail.  It provides some additional information
    that can be used to understand what caused the exception.
    Args:
        error_text (string): The error text message that coincides with the
            error_code
        commands (array): The list of commands that were sent to the node
            that generated the error
    """
    def __init__(self, message, commands):
        self.error_text = message
        self.commands = commands
        super(CommandError, self).__init__(message)

    @property
    def trace(self):
        return self.get_trace()

    def get_trace(self):
        trace = list()
        index = None

        for index, out in enumerate(self.error_text):
            _entry = {'command': self.commands[index], 'output': out}
            trace.append(_entry)

        if index:
            index += 1
            for cmd in self.commands[index:]:
                _entry = {'command': cmd, 'output': None}
                trace.append(_entry)

        return trace

class DeviceConn:
    def set_conn_params(self, conf_file):
        """Set the Device connection parameters"""
        pass
    def set_up_conn(self, device_name: str):
        """Connect to the mentioned device"""
        pass

    def send_commands(self, cmds, encoding, send_enable, **kwargs):
        """Send commands over the device conn"""
        pass

class PyeapiConn(DeviceConn):
    def connection(self):
        return self._connection

    def set_conn_params(self, conf_file):
        pyeapi.load_config(conf_file)

    def set_up_conn(self, device_name):
        self._connection =  pyeapi.connect_to(device_name)

    def send_commands(self, cmds, encoding='json', send_enable=True, **kwargs):
        output = self._connection.run_commands(cmds, encoding, send_enable)
        return output

class NetmikoConn(DeviceConn):
    def connection(self):
        return self._connection

    def set_conn_params(self, conf_file):
        self._config = configparser.ConfigParser()
        self._config.read(conf_file)

    def set_up_conn(self, device_name):
        name = 'connection:{}'.format(device_name)
        if not self._config.has_section(name):
            raise AttributeError('connection profile not found')

        device_attributes = dict(self._config.items(name)) 

        default_device_type = 'arista_eos'
        remote_device = {
                'device_type': device_attributes.get('device_type', default_device_type),
                'host': device_attributes['host'],
                'username': device_attributes['username'],
                'password': device_attributes['password'],
                'secret': device_attributes.get('enable_mode_secret', ""),
                }
        if remote_device['device_type'] == 'autodetect':
            guesser = SSHDetect(**remote_device)
            remote_device['device_type'] = guesser.autodetect()
        self._connection = Netmiko(**remote_device)

    def send_commands(self, cmds, encoding='json', send_enable=True, **kwargs):
        output = ''
        local_cmds = []
        if send_enable == True:
            self._connection.enable()
        if encoding == 'json':
            """for json encoding, lets try to run cmds
            using |json"""
            if type(cmds) is list:
                local_cmds = cmds.copy()
                for i,cmd in enumerate(local_cmds):
                    local_cmds[i] = cmd + ' | json'
            elif type(cmds) is str:
                cmds = cmds + ' | json'
        elif encoding == 'text':
            if type(cmds) is list:
                local_cmds = cmds.copy()
        cmds_op = []
        if type(cmds) is list:
            for i, cmd in enumerate(local_cmds):
                output = self._connection.send_command(cmd)
                if not output in error_responses:
                    if encoding == 'json':
                        output = json.loads(output)
                else:
                    err_msg = ('Could not execute %s. '
                            'Got error: %s' %(cmds[i], output))
                    raise CommandError(err_msg, cmds)

                if encoding == 'text':
                    """ for text encoding, creating the 
                    format similar to one returned by
                    eapi format"""
                    text_ob = {"output": output}
                    cmds_op.append(text_ob)
                else:
                    cmds_op.append(output)
        elif type(cmds) is str:
            output = self._connection.send_command(cmds)
            if not output in error_responses :
                if encoding == 'json':
                    output = json.loads(output)
            else:
                err_msg = ('Could not execute %s. '
                        'Got error: %s' %(cmds[i], output))
                raise CommandError(err_msg, cmds)

            if encoding == 'text':
                text_ob = {"output": output}
                cmds_op.append(text_ob)
            else:
                cmds_op.append(output)

        return cmds_op
