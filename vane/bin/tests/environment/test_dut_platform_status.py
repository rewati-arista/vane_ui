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
@pytest.mark.platform_status
@pytest.mark.environment
class EnvironmentTests():
    """ Environment Test Suite
    """

    def test_if_system_environment_temperature_are_in_spec_on_(self,
                                                               dut,
                                                               tests_definitions):
        """ Verify system temperature environmentals are functional within spec

            Args:
              dut (dict): Encapsulates dut details including name, connection
              tests_definitions (dict): Test parameters
        """

        test_case = inspect.currentframe().f_code.co_name
        test_parameters = tests_tools.get_parameters(tests_definitions,
                                                     TEST_SUITE,
                                                     test_case)

        show_cmd = test_parameters["show_cmd"]
        tests_tools.verify_show_cmd(show_cmd, dut)
        show_cmd_txt = dut["output"][show_cmd]['text']

        expected_output = test_parameters["expected_output"]
        dut_name = dut['name']

        logging.info(f'TEST is |{dut_name}| system termperature '
                     'environmentals functioning within spec')
        logging.info(f'GIVEN expected temperature state is {expected_output}')

        dut_ptr = dut["output"][show_cmd]["json"]
        system_status = dut_ptr["systemStatus"]
        power_supply_slots = dut_ptr["powerSupplySlots"]
        temp_sensors = dut_ptr["tempSensors"]

        actual_output = f"System Status: {system_status} \nPower Supply Slots: \
                        {power_supply_slots} \nTemperature Sensors: \
                        {temp_sensors}"
        logging.info(f'WHEN actual temperature state is {actual_output}')

        print(f"\nOn router |{dut_name}| system temperature is "
              f"|{system_status}|")

        assert system_status == 'temperatureOk'

        for powersupply in power_supply_slots:
            for temp_sensors in powersupply['tempSensors']:
                print("Power-supply temperature sensor "
                      f"|{temp_sensors['name']}| alert state is "
                      f"|{temp_sensors['inAlertState']}|")

                assert temp_sensors['inAlertState'] is False

        for temp_sensor in temp_sensors:
            print(f"Temperature sensor |{temp_sensor['name']}| alert state "
                  f"is |{temp_sensor['inAlertState']}|")

            assert temp_sensor['inAlertState'] is False

        logging.info('THEN test case result is |PASS|')
        logging.info(f'OUTPUT of |{show_cmd}| is :\n\n{show_cmd_txt}')
