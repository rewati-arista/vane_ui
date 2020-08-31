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

    args = parser.parse_args()

    return args


def run_tests(definitions_file):
    """ Make request to test client to run tests

        Args:
             definitions_file (str): Path and name of definition file
    """

    logging.info('Using class TestsClient to create vane_tests_client '
                 'object')
    vane_tests_client = tests_client.TestsClient(definitions_file)
    vane_tests_client.test_runner()


# def error_check(input_data, DEFINITIONS_FILE):
#     """ Error check input
#
#         Args:
#             input_data (dict): Input VPC specific data from ADO in JSON
#                                format
#             DEFINITIONS_FILE (str): Path and name of definition file
#
#         return:
#             raw_input_data (dict): combined definitions, input data, and aws
#                                    data
#     """
#
#     logging.info('Creating cas_input_client object')
#     cas_input_client = input_client.InputClient(DEFINITIONS_FILE, input_data)
#     logging.info('Querying AWS for addiitonal VPC data')
#     cas_input_client.query_aws()
#     logging.info('Checking data for errors')
#     raw_input_data = cas_input_client.error_check()
#
#     return raw_input_data
#
#
# def render_data(raw_input_data):
#     """ Model data and then render templates
#
#         Args:
#             raw_input_data (dict): combined definitions, input data, and aws
#                                    data
#     """
#     logging.info('Creating cas_render_client object')
#     cas_render_client = render_client.RenderClient(raw_input_data)
#     logging.info('Creating common data-model using raw_input_data')
#     cas_render_client.create_data_model()
#     logging.info('Use common data-model to render configlets and TerraForm '
#                  'templates')
#     cas_render_client.render_client(terraform=True, ipsec=False, bgp=False)
#
#
# def cvaas_export(cas_cvaas_client, DEFINITIONS_FILE):
#     """ Export configlets to CVaaS
#
#         Args:
#             cas_cvaas_client (obj): cvaas object
#             DEFINITIONS_FILE (str): name / path to definitions file
#     """
#
#     logging.info('Import definitions')
#     input_data = import_definitions(DEFINITIONS_FILE)
#
#     logging.info('Creating cas_render_client object')
#     cas_render_client = render_client.RenderClient(input_data)
#     logging.info('Use common data-model to render configlets and TerraForm '
#                  'templates')
#     cas_render_client.render_client(terraform=False, ipsec=True, bgp=True)
#
#     logging.info('Login into CVaaS')
#     cas_cvaas_client.cvaas_login()
#     cas_cvaas_client.apply_configlets('ipsec')
#     cas_cvaas_client.apply_configlets('bgp_prefix_list')
#     cas_cvaas_client.apply_configlets('bgp')
#     cas_cvaas_client.apply_configlets('ops')
#
#
# def cvp_import(cas_cvaas_client):
#     """ Export configlets to CVaaS
#
#         Args:
#             cas_cvaas_client (obj): cvaas object
#     """
#
#     logging.info('Logging into CVP')
#     cas_cvaas_client.cvp_login()
#
#     logging.info('Importing standalone CVP configlets')
#     cas_cvaas_client.cvp_import()
#
#
# def import_definitions(definition_file):
#     """ Import YAML definitions file
#
#         Args:
#             defintion_file (str): Name of defintions file
#     """
#
#     logging.info(f'Opening {definition_file} for read')
#     try:
#         with open(definition_file, 'r') as input_yaml:
#             try:
#                 definitions_data = yaml.safe_load(input_yaml)
#                 logging.info(f'Inputed the following definitions: '
#                              f'{definitions_data}')
#                 input_data = {"definitions": definitions_data}
#                 return input_data
#             except yaml.YAMLError as e:
#                 logging.error(f'Error in YAML file. {e}')
#                 sys.exit(1)
#     except OSError as e:
#         logging.error(f'Defintions file: {definition_file} not '
#                       f'found. {e}')
#         sys.exit(1)


def main():
    """ main function
    """

    logging.info('Accept input from command-line')
    args = parse_cli()

    if args.definitions_file:
        logging.warning('Changing Definitions name to '
                        f'{args.definitions_file}')
        DEFINITIONS_FILE = args.definitions_file

    run_tests(DEFINITIONS_FILE)


if __name__ == "__main__":
    main()
