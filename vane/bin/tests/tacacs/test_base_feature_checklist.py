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

""" Tests to validate base feature status."""

import inspect
import logging
import pytest
import tests_tools


TEST_SUITE = __file__
LOG_FILE = {"parameters": {"show_log": "show_output.log"}}


@pytest.mark.nrfu
@pytest.mark.base_feature
@pytest.mark.tacacs
class TacacsTests():
    """ AAA TACACS Test Suite
    """

    def test_if_tacacs_is_sending_messages_on_(self, dut, tests_definitions):
        """ Verify tacacs messages are sending correctly

            Args:
              dut (dict): Encapsulates dut details including name, connection
              tests_definitions (dict): Test parameters
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        tacacs_servers = tests_tools.verify_tacacs(dut)

        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is |{dut_name}| sending messages to TACACS server')

        if tacacs_servers:
            dut_ptr = dut["output"][show_cmd]['json']
            eos_messages_sent_1 = dut_ptr['tacacsServers'][0]['messagesSent']
            logging.info(f'GIVEN {eos_messages_sent_1} TACACS messages sent '
                         'at time 1')

            show_output, _ = tests_tools.return_show_cmd(show_cmd,
                                                         dut,
                                                         test_case,
                                                         LOG_FILE)
            show_ptr = show_output[0]['result']
            eos_messages_sent_2 = show_ptr['tacacsServers'][0]['messagesSent']
            logging.info(f'WHEN {eos_messages_sent_2} TACACS messages sent '
                         'at time 2')

            actual_output = f"TACACS Sent Message Time 1: \
                            {eos_messages_sent_1} \nTACACS Sent Message \
                            Time 2: {eos_messages_sent_2}"

            if eos_messages_sent_1 < eos_messages_sent_2:
                print(f"\nOn router |{dut_name}| TACACS messages2 sent: "
                      f"|{eos_messages_sent_2}| increments from TACACS "
                      f"messages1 sent: |{eos_messages_sent_1}|")
                logging.info('THEN test case result is |True|')
            else:
                print(f"\nOn router |{dut_name}| TACACS messages2 sent: "
                      f"|{eos_messages_sent_2}| doesn't increments from "
                      f"TACACS messages1 sent: |{eos_messages_sent_1}|")
                logging.info('THEN test case result is |False|')

            logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

            assert eos_messages_sent_1 < eos_messages_sent_2
        else:
            print(f"\nOn router |{dut_name}| does not have TACACS servers "
                  "configured")

    def test_if_tacacs_is_receiving_messages_on_(self,
                                                      dut,
                                                      tests_definitions):
        """ Verify tacacs messages are received correctly

            Args:
              dut (dict): Encapsulates dut details including name, connection
              tests_definitions (dict): Test parameters
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        tacacs_servers = tests_tools.verify_tacacs(dut)

        show_cmd_txt = dut["output"][show_cmd]['text']

        logging.info(f'TEST is |{dut_name}| receiving messages to TACACS '
                     'server')

        if tacacs_servers:
            dut_ptr = dut["output"][show_cmd]['json']['tacacsServers']
            eos_messages_received_1 = dut_ptr[0]['messagesReceived']
            logging.info(f'GIVEN {eos_messages_received_1} TACACS messages '
                         'recieved at time 1')

            show_output, _ = tests_tools.return_show_cmd(show_cmd,
                                                         dut,
                                                         test_case,
                                                         LOG_FILE)
            show_ptr = show_output[0]['result']['tacacsServers']

            eos_messages_received_2 = show_ptr[0]['messagesReceived']
            logging.info(f'WHEN {eos_messages_received_2} TACACS messages '
                         'sent at time 2')

            actual_output = f"TACACS Sent Message Time 1: \
                            {eos_messages_received_1} \nTACACS Sent Message \
                            Time 2: {eos_messages_received_2}"

            if eos_messages_received_1 < eos_messages_received_2:
                print(f"\nOn router |{dut['name']}| TACACS messages2 "
                      f"received: |{eos_messages_received_2}| increments "
                      "from TACACS messages1 received: "
                      f"|{eos_messages_received_1}|")
                logging.info('THEN test case result is |True|')
            else:
                print(f"\nOn router |{dut['name']}| TACACS messages2 "
                      f"received: |{eos_messages_received_2}| doesn't "
                      "increments from ACACS messages1 received: "
                      f"|{eos_messages_received_1}|")
                logging.info('THEN test case result is |False|')

            logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')

            assert eos_messages_received_1 < eos_messages_received_2
        else:
            print(f"\nOn router |{dut_name}| does not have TACACS servers "
                  "configured")
