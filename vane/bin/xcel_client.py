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

"""Utilities for using PyTest in network testing"""

import logging
import yaml
import sys
import openpyxl


logging.basicConfig(level=logging.INFO, filename='vane.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class XcelClient:
    """ Creates an instance of the Excel Client.
    """

    def __init__(self, definitions_file):
        """ Initializes the excel client

            Args:
                spreadsheet (obj): Spreadsheet 
        """

        self.definitions = self._import_yaml(definitions_file)
        self.spreadsheet = ""

    def _import_yaml(self, yaml_file):
        """ Import YAML file as python data structure

            Args:
                yaml_file (str): Name of YAML file
        """

        logging.info(f'Opening {yaml_file} for read')
        try:
            with open(yaml_file, 'r') as input_yaml:
                try:
                    yaml_data = yaml.safe_load(input_yaml)
                    logging.info(f'Inputed the following yaml: '
                                 f'{yaml_data}')
                    return yaml_data
                except yaml.YAMLError as err_data:
                    logging.error(f'Error in YAML file. {err_data}')
                    sys.exit(1)
        except OSError as err_data:
            logging.error(f'Defintions file: {yaml_file} not '
                          f'found. {err_data}')
            sys.exit(1)

    def import_spreadsheet(self):
        """ import spreadsheet for parsing

            return:
                lld_spreadsheet (obj):    Abstraction of spreadsheet,
        """

        file_object = pathlib.Path(self.lld_spreadsheet)

        if not file_object.exists():
            self._record_error_entry(self.lld_spreadsheet,
                                     None, None, "006", "002")
            self.generate_error_report()

        try:
            lld_spreadsheet = openpyxl.load_workbook(self.lld_spreadsheet)
            return lld_spreadsheet
        except:
            self._record_error_entry(self.lld_spreadsheet,
                                     None,
                                     None,
                                     "006",
                                     "001")
            self.generate_error_report()