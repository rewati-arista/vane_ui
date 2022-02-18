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

""" SwitchConfig/Section Class definitions
"""

import collections
import re

INDENT = 3

EOF_COMMANDS = [
    'banner login',
    'banner motd',
    'comment',
    'protocol https certificate',
    'ssl certificate',
    'ssl key'
]

def is_eof_command(line):
    """ Test if line begins with an EOF command
    """
    for cmd in EOF_COMMANDS:
        if line.lstrip().startswith(cmd):
            return True
    return False


class SectionOrderedDict(collections.OrderedDict):
    """ OrderedDict with extra functionallity.
    """
    PREV = 0
    NEXT = 1
    KEY = 2

    # def __init__(self, *args, **kwargs):
    #     super(SectionOrderedDict, self).__init__(*args, **kwargs)

    def last(self):
        """ Get the last (value) in this OrderedDict
        """
        key = next(reversed(self))  # pylint: disable=E0111
        return (key, self[key])


class SectionError(Exception):
    """ Base class for all Section Errors
    """
    def __init__(self, msg, data=None):
        Exception.__init__(self)
        self.msg = msg
        self.data = data

    def __str__(self):
        return "Error: {}: {}".format(self.msg, self.data)


class Section(object):
    """ Section of config
    """
    def __init__(self, line=None, parent=None):
        self._line = line
        self._parent = parent
        self.children = SectionOrderedDict()

    def get_child(self, line):
        """ Get a child Section
            Returns None if non-existent
        """
        return self.children.get(line, None)

    def get_all_sections(self):
        """ Returns all Sections associated with this Section
        """
        return list(self.children.items())

    def add_child(self, child):
        """ Add child Section
        """
        self.children[child.line] = child

    @property
    def line(self):
        """ Getter method for our line
        """
        return self._line

    @line.setter
    def line(self, line):
        """ Setter for line
        """
        self._line = line

    @property
    def parent(self):
        """ Getter method for our parent
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """ Setter for parent
        """
        self._parent = parent

    def is_parent(self):
        """ Checks to see if we have children (we are a parent)
        """
        size = len(self.children)
        if size > 0:
            return True
        return False

    def get_command_list(self):
        """ Get the command list
        """
        config = []
        append_break = False
        if self._line:
            config.append('{}'.format(self._line))

        for _, child in self.children.items():
            if child.is_parent():
                if append_break:
                    config.append('!')
                    append_break = False
                results = child.get_command_list()
                config.extend(results)
            else:
                config.append('{}'.format(child.line))
                # append_break = True
        if self._line:
            config.append('!')
        return config


class SwitchConfigError(Exception):
    """ Base class for all SwitchConfig Errors
    """
    def __init__(self, msg, data=None):
        Exception.__init__(self)
        self.msg = msg
        self.data = data

    def __str__(self):
        return "Error: {}: {}".format(self.msg, self.data)


class ParseError(SwitchConfigError):
    """ SwitchConfig Parse Error
    """
    def __init__(self, msg):
        SwitchConfigError.__init__(self, msg)


class SwitchConfig(object):
    """ SwitchConfig Class
    """
    def __init__(self, config=None):
        self.base_sections = 0
        if config is None:
            config = []
        elif isinstance(config, str):
            config = config.split('\n')
        elif isinstance(config, Section):
            self.config_root = config.copy()
            return
        elif not isinstance(config, list):
            raise ParseError('Config must be type list')
        self.config_root = self.parse(config)

    def parse(self, config=None):
        """ Parse a provided list of config commands and return a root Section
        """
        if not isinstance(config, list):
            raise ParseError('Config must be type list')

        prev_indent = 0
        section_stack = []
        look_for_eof = False

        # init root of tree
        current_section = Section()
        root = current_section
        # for line in config:
        for num, line in enumerate(config):
            # if we are still looking for EOF
            if look_for_eof:
                # Add the line to the current section
                new_section = Section(line, current_section)
                current_section.add_child(new_section)

                # OK..this is the EOF
                if line.lstrip().startswith('EOF'):
                    current_section = section_stack.pop()
                    look_for_eof = False
                continue

            # Handle these separately...but ignore.
            line_size = len(line)
            if line.isspace() or (line_size == 0):
                continue

            # get the indent level
            indent_level = len(line) - len(line.lstrip())

            if indent_level % INDENT != 0:
                msg = 'line[{}] improper indent:{} ' \
                      'SwitchConfig indentation must be multiple '\
                      'of {}.'.format(num, indent_level, INDENT)
                raise ParseError(msg)

            # ignore if line starts with '!' (but not '!!'), 'end',
            # or if line is exactly '!'
            if re.match(r'^\s*![^!]', line) or line == '!' or \
               line.startswith('end '):
                # reset our previous indent level, clear the
                # stack, and set our current_section to root.
                prev_indent = indent_level
                del section_stack[:]
                current_section = root
                continue

            # if indent level > previous indent level
            if indent_level > prev_indent:
                self.base_sections += 1
                # get last key,value from children hash
                last_child = current_section.children.last()[1]
                # New Section
                new_section = Section(line, last_child)
                # push the current level
                section_stack.append(current_section)
                # Add new section to children
                last_child.add_child(new_section)
                # move up the tree
                current_section = last_child
                prev_indent = indent_level

            # if the indent_level is < previous_indent
            elif indent_level < prev_indent:
                levels_diff = \
                    (prev_indent - indent_level) / INDENT
                if levels_diff > 1:
                    del section_stack[len(section_stack) - (levels_diff - 1):]
                current_section = section_stack.pop()

                # Add the line to the current section
                new_section = Section(line, current_section)
                current_section.add_child(new_section)

                prev_indent = indent_level
            else:
                # Add the line to the current section
                new_section = Section(line, current_section)
                current_section.add_child(new_section)

            if is_eof_command(line):
                # push the current level
                section_stack.append(current_section)
                # set to the new section
                current_section = new_section
                look_for_eof = True
        return root
