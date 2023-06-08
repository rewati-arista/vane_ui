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

"""
Collection of misc functions that dont fit anywhere else but are still required.
"""

import sys
import collections
import time
import paramiko

CMD_WAIT = 5


def make_iterable(value):
    """Converts the supplied value to a list object
    This function will inspect the supplied value and return an
    iterable in the form of a list.
    Args:
        value (object): An valid Python object
    Returns:
        An iterable object of type list
    """
    if sys.version_info <= (3, 0) and isinstance(value, str):
        # Convert unicode values to strings for Python 2
        value = str(value)
    if isinstance(value, (dict, str)):
        value = [value]

    if sys.version_info <= (3, 3):
        if not isinstance(value, collections.Iterable):
            raise TypeError("value must be an iterable object")
    else:
        if not isinstance(value, collections.abc.Iterable):
            raise TypeError("value must be an iterable object")

    return value


def get_current_fixture_testclass(request):
    """
    Method to get the name of the Test Function's class
    from the request fixture.
    Args: request - is the pytest request fixture
    Returns: Name of the test functions's class
    """

    nodeid = request.node.nodeid.split("::")
    test_class = nodeid[1] if len(nodeid) >= 2 else None
    return test_class


def get_current_fixture_testname(request):
    """
    Method to get the name of the Test Function
    from the request fixture.
    Args: request - is the pytest request fixture
    Returns: Name of the test function
    """

    nodeid = request.node.nodeid.split("::")
    test_name = nodeid[2] if len(nodeid) >= 3 else None
    return test_name.split("[")[0]


def get_ssh_connection(host, user, pwd):
    """
    Utility to get ssh connection object
    Args:
        host(str): IP address of device.
        user(str): username for device login.
        pwd(str): password for device login
    Returns:
        obj: ssh connection object
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        paramiko.util.log_to_file("filename.log")
        ssh.connect(hostname=host, username=user, password=pwd)
        print("connected to host", host)
        return ssh
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials")
        return None


def run_commands_ssh(ssh, cmd_list, cmd_wait=CMD_WAIT):
    """
    Utility to run commands using paramiko ssh connection
    Args:
        ssh(obj): ssh connection object
        cmd_list(list): list of commands
    Returns:
        str: Output of show command
    """
    try:
        channel = ssh.invoke_shell()
        for cmd in cmd_list:
            channel.send(cmd)
            time.sleep(cmd_wait)
        out = channel.recv(99999999)
        result = out.decode("ascii")
        print(out.decode("ascii"))
    except paramiko.AuthenticationException:
        print("Error while executing the command on device")
        result = None
    return result


def get_ssh_cmd_output(host, user, password, config_cmds, cmd_wait=CMD_WAIT):
    """
    Utility to execute commands on device and return the output

    Args:
        host(str): IP address of device.
        user(str): username for device login.
        password(str): password for device login.
        config_cmds(list): list of commands to execute on the device.
    Returns:
        str: output of command executed on the device
    """
    ssh = get_ssh_connection(host, user, password)
    output = run_commands_ssh(ssh, config_cmds, cmd_wait)
    ssh.close()
    return output
