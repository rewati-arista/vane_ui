#! /usr/bin/env python
#
# Copyright (c) 2018, Arista Networks EOS+
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

""" Parse running-config information

Parse the output from 'show running-config' or 'show running-config sanitized'
and record the data in a dictionary.
"""

import re

from showtech.parsers._switchconfig import SwitchConfig

SECTIONS = [
    'show running-config',
    'show running-config sanitized',
]

STRIP_RE = re.compile('^($|Building configuration|Current configuration)')


def sections():
    """ Return the list of sections this parser covers

    Args:
        None

    Returns:
        list: Contains the show tech sections that this parser handles
    """
    return SECTIONS


def parse(data, section, lines):
    """ Parse the set of lines in the given section and store
    the parsed information in the data dictionary

    Args:
        data (dictionary): The show tech data dictionary in which
            the parsed data will be stored.
        section (string): The name of the show tech section that is
            being parsed. Becomes the key for the data dictionary
            under which the parsed data is stored.
        lines (list of strings): The list of lines from the show
            tech section that is being parsed.

    Returns:
        None: The parsed information is stored in the data dictionary
            passed in as the first argument.
    """

    # Strip any non-config lines from the beginning of the block
    while STRIP_RE.match(lines[0]):
        lines.pop(0)
        # If we delete every line from the list, we have nothing to
        # process. Return without doing anything.
        if not lines:
            return

    # Store the running-config lines as a simple list first
    line_key = '{} lines'.format(section)
    data[line_key] = lines

    # Convert the running-config lines into a SwitchConfig object
    switch_config = SwitchConfig(lines)

    # Store the SwitchConfig object as a dictionary, starting
    # at the root of the config
    data[section] = _store_config(switch_config.config_root)


def _store_config(config_section):
    """ Convert a Section of a SwitchConfig object to a dictionary

    Args:
        config_section (object): A Section of a SwitchConfig object.

    Returns:
        dictionary: The SwitchConfig Section and all its children,
            converted to a dictionary structure.
    """

    # Initialize the dictionary object
    section_d = {}

    # Retrieve the children of the current Section and process
    # each of those children, populating the dictionary with each.
    subs = config_section.get_all_sections()
    for name, section_obj in subs:
        # If the name of the child section contains 'banner', just
        # store the list of strings under that section, without modifying
        # any of the data (to keep the exact string structure of the banner).
        # Otherwise, call _store_config on each child Section and store
        # it in the dictionary object.
        if 'banner' in name:
            lines = section_obj.get_command_list()
            # The get_command_list returns the lines under the section,
            # with the section line itself as the first line, and a '!'
            # as the final line. Remove the first and last lines so
            # we only have the actual banner stored.
            lines.pop(0)
            lines.pop()
            section_d[name.lstrip()] = lines
        else:
            config_d = _store_config(section_obj)
            section_d[name.lstrip()] = config_d if config_d else {}

    # Return the populated dictionary
    return section_d
