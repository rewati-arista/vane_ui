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
import pathlib


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

        xcel_defs = self.definitions['parameters']['xcel_definitions']
        self.xcel_defs = self._import_yaml(xcel_defs)

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

        spreadsheet_path = self.definitions['parameters']['spreadsheet']
        file_object = pathlib.Path(spreadsheet_path)

        if not file_object.exists():
            logging.error(f'Spreadsheet {spreadsheet_path} does not exist')
            print(f'SPREADSHEET {spreadsheet_path} DOES NOT EXIST')
            sys.exit(1)

        try:
            self.spreadsheet = openpyxl.load_workbook(spreadsheet_path)
            logging.info(f'Successfully importted spreadsheet {spreadsheet_path}')
        except:
            logging.error(f'Error opening spreadsheet {spreadsheet_path}')
            print(f'ERROR OPENING SPREADSHEET {spreadsheet_path}')
            sys.exit(1)

    def parse_spreadsheet(self):
        """ Use excel definitioins to parse informations from spreadsheet
        """

        worksheet = self._return_worksheet('HostnameMgmt')
        self._parse_host_tab(worksheet)

    def _return_worksheet(self, ws_role):
        """ Returns worksheet name

        Args:
            ws_role (str): Excel Worksheet role

        Returns:
            str: Excel worksheet name
        """

        tab = None
        worksheets = self.xcel_defs['worksheets']
        ws_data = [x for x in worksheets if ws_role == x['role']]
        logging.info(f'Found Worksheet role {ws_data}')
        ws_name = ws_data[0]['name']
        logging.info(f'Worksheet name is {ws_name}')

        for worksheet in self.spreadsheet.sheetnames:
            logging.info(f'Comparing criteria |{ws_name}| to tab |{worksheet}|')
            if ws_name == worksheet:
                logging.info(f"Matched tab {worksheet}")
                tab = worksheet
        
        if tab:
            logging.info(f'Found tab {tab}')
            return tab
        else:
            logging.error(f'Error spreadsheet worksheet not found {ws_name}')
            print(f'ERROR NO SPREADSHEET TAB NOT FOUND {ws_name}')
            sys.exit(1)
                
    def _parse_host_tab(self, ws_name):

        worksheets = self.xcel_defs['worksheets']
        ws_data = [x for x in worksheets if ws_name == x['name']]
        header_row = ws_data[0]['header_row']

        hosts, host_col = self._return_header(header_row, 'hostname')
        devices, device_col = self._return_header(header_row, 'device_function')

        # hosts = [x for x in ws_data if 'hostname' == x['role']]
        # host_col = hosts['column']
        # hosts = [x for x in ws_data if 'hostname' == x['role']]
        # host_col = hosts['column']
# 
        # for header_field in header_row:
        #     name = header_field['name']
        #     column = header_field['column']
        #     last_row = len(self.spreadsheet[ws_name][column])
        #     print(f'{name} {column}')

    def _return_header(self, header, field):

        header_data = [x for x in header if field == x['role']]
        header_col = header_data[0]['column']
        print(header_data[0], header_col)

        return header_data[0], header_col

