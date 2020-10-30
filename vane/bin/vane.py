#!/usr/local/bin/python3
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

""" A weather vane is an instrument used for showing the direction of the wind.
Just like a weather vane, Vane is a network certification tool that shows a
network's readiness for production based on validation tests. """

import argparse
import logging
import tests_client
import report_client
import xcel_client
import sys


logging.basicConfig(level=logging.INFO, filename='vane.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info('Starting vane.log file')

DEFINITIONS_FILE = "/project/vane/bin/definitions.yaml"


def parse_cli():
    """Parse cli options.

    Returns:
        args (obj): An object containing the CLI arguments.
    """

    parser = argparse.ArgumentParser(
        description=('Network Certification Tool'))

    parser.add_argument('--definitions_file',
                        default=DEFINITIONS_FILE,
                        help='Specify the name of the defintions file')

    parser.add_argument('--input',
                        action='store_true',
                        default=False,
                        help='Use spreadsheet for input')

    args = parser.parse_args()

    return args


def input_spreadsheet(definitions_file):
    """ Input data from a spreadsheet
    """

    vane_xcel_client = xcel_client.XcelClient(definitions_file)
    vane_xcel_client.import_spreadsheet()
    vane_xcel_client.parse_spreadsheet()
    sys.exit(0)


def run_tests(definitions_file):
    """ Make request to test client to run tests

        Args:
            definitions_file (str): Path and name of definition file
    """

    logging.info('Using class TestsClient to create vane_tests_client '
                 'object')
    vane_tests_client = tests_client.TestsClient(definitions_file)
    vane_tests_client.test_runner()


def write_results(definitions_file):
    """ Write results document

        Args:
            definitions_file (str): Path and name of definition file
    """

    logging.info('Using class ReportClient to create vane_report_client '
                 'object')
    vane_report_client = report_client.ReportClient(definitions_file)
    vane_report_client.write_result_doc()


def main():
    """ main function
    """

    logging.info('Accept input from command-line')
    args = parse_cli()

    if args.definitions_file:
        logging.warning('Changing Definitions name to '
                        f'{args.definitions_file}')
        DEFINITIONS_FILE = args.definitions_file

    if args.input:
        input_spreadsheet(DEFINITIONS_FILE)

    run_tests(DEFINITIONS_FILE)
    write_results(DEFINITIONS_FILE)

    logging.info('\n\n!VANE has completed without errors!\n\n')


if __name__ == "__main__":
    main()
