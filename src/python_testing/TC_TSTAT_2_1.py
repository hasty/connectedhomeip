#
#    Copyright (c) 2025 Project CHIP Authors
#    All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# See https://github.com/project-chip/connectedhomeip/blob/master/docs/testing/python.md#defining-the-ci-test-arguments
# for details about the block below.
#
# === BEGIN CI TEST ARGUMENTS ===
# test-runner-runs:
#   run1:
#     app: ${ALL_CLUSTERS_APP}
#     app-args: >
#       --discriminator 1234
#       --KVS kvs1
#       --trace-to json:${TRACE_APP}.json
#       --enable-key 000102030405060708090a0b0c0d0e0f
#       --featureSet 0xa
#       --application evse
#     script-args: >
#       --storage-path admin_storage.json
#       --commissioning-method on-network
#       --discriminator 1234
#       --passcode 20202021
#       --hex-arg enableKey:000102030405060708090a0b0c0d0e0f
#       --endpoint 1
#       --trace-to json:${TRACE_TEST_JSON}.json
#       --trace-to perfetto:${TRACE_TEST_PERFETTO}.perfetto
#     factory-reset: true
#     quiet: true
# === END CI TEST ARGUMENTS ===

import copy
import logging
import random

import chip.clusters as Clusters
from chip import ChipDeviceCtrl  # Needed before chip.FabricAdmin
from chip.clusters import Globals
from chip.clusters.Types import NullValue
from chip.interaction_model import InteractionModelError, Status
from chip.testing import matter_asserts
from chip.testing.matter_testing import MatterBaseTest, TestStep, run_if_endpoint_matches, has_cluster, default_matter_test_main
from mobly import asserts

logger = logging.getLogger(__name__)

cluster = Clusters.Thermostat

class TSTAT_2_1(MatterBaseTest):

    def desc_TSTAT_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_TSTAT_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["TSTAT.S"]

    def steps_TSTAT_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read LocalTemperature attribute"),
            TestStep("2", "Read OutdoorTemperature attribute"),
            TestStep("3", "Read Occupancy attribute"),
            TestStep("4", "Read AbsMinHeatSetpointLimit attribute"),
            TestStep("5", "Read AbsMaxHeatSetpointLimit attribute"),
            TestStep("6", "Read AbsMinCoolSetpointLimit attribute"),
            TestStep("7", "Read AbsMaxCoolSetpointLimit attribute"),
            TestStep("8", "Read PICoolingDemand attribute"),
            TestStep("9", "Read PIHeatingDemand attribute"),
            TestStep("10", "Read LocalTemperatureCalibration attribute"),
            TestStep("11", "Read OccupiedCoolingSetpoint attribute"),
            TestStep("12", "Read OccupiedHeatingSetpoint attribute"),
            TestStep("13", "Read UnoccupiedCoolingSetpoint attribute"),
            TestStep("14", "Read UnoccupiedHeatingSetpoint attribute"),
            TestStep("15", "Read MinHeatSetpointLimit attribute"),
            TestStep("16", "Read MaxHeatSetpointLimit attribute"),
            TestStep("17", "Read MinCoolSetpointLimit attribute"),
            TestStep("18", "Read MaxCoolSetpointLimit attribute"),
            TestStep("19", "Read MinSetpointDeadBand attribute"),
            TestStep("20", "Read RemoteSensing attribute"),
            TestStep("21", "Read ControlSequenceOfOperation attribute"),
            TestStep("22", "Read SystemMode attribute"),
            TestStep("23", "Read ThermostatRunningMode attribute"),
            TestStep("24", "Read StartOfWeek attribute"),
            TestStep("25", "Read NumberOfWeeklyTransitions attribute"),
            TestStep("26", "Read NumberOfDailyTransitions attribute"),
            TestStep("27", "Read TemperatureSetpointHold attribute"),
            TestStep("28", "Read TemperatureSetpointHoldDuration attribute"),
            TestStep("29", "Read ThermostatProgrammingOperationMode attribute"),
            TestStep("30", "Read ThermostatRunningState attribute"),
            TestStep("31", "Read SetpointChangeSource attribute"),
            TestStep("32", "Read SetpointChangeAmount attribute"),
            TestStep("33", "Read SetpointChangeSourceTimestamp attribute"),
            TestStep("34", "Read OccupiedSetback attribute"),
            TestStep("35", "Read OccupiedSetbackMin attribute"),
            TestStep("36", "Read OccupiedSetbackMax attribute"),
            TestStep("37", "Read UnoccupiedSetback attribute"),
            TestStep("38", "Read UnoccupiedSetbackMin attribute"),
            TestStep("39", "Read UnoccupiedSetbackMax attribute"),
            TestStep("40", "Read EmergencyHeatDelta attribute"),
            TestStep("41", "Read ACType attribute"),
            TestStep("42", "Read ACCapacity attribute"),
            TestStep("43", "Read ACRefrigerantType attribute"),
            TestStep("44", "Read ACCompressorType attribute"),
            TestStep("45", "Read ACErrorCode attribute"),
            TestStep("46", "Read ACLouverPosition attribute"),
            TestStep("47", "Read ACCoilTemperature attribute"),
            TestStep("48", "Read ACCapacityFormat attribute"),
            TestStep("49", "Read PresetTypes attribute"),
            TestStep("50", "Read ScheduleTypes attribute"),
            TestStep("51", "Read NumberOfPresets attribute"),
            TestStep("52", "Read NumberOfSchedules attribute"),
            TestStep("53", "Read NumberOfScheduleTransitions attribute"),
            TestStep("54", "Read NumberOfScheduleTransitionPerDay attribute"),
            TestStep("55", "Read ActivePresetHandle attribute"),
            TestStep("56", "Read ActiveScheduleHandle attribute"),
            TestStep("57", "Read Presets attribute"),
            TestStep("58", "Read Schedules attribute"),
            TestStep("59", "Read SetpointHoldExpiryTimestamp attribute"),
        ]
        return steps

    NumberOfPresets = None
    NumberOfScheduleTransitions = None
    NumberOfSchedules = None
    OccupiedSetbackMax = None
    OccupiedSetbackMin = None
    UnoccupiedSetbackMax = None
    UnoccupiedSetbackMin = None

    @run_if_endpoint_matches(has_cluster(Clusters.Thermostat))
    async def test_TSTAT_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LocalTemperature)
        if val is not NullValue:
            matter_asserts.assert_valid_int16(val, 'LocalTemperature')

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OutdoorTemperature):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OutdoorTemperature)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int16(val, 'OutdoorTemperature')

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Occupancy):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Occupancy)
            matter_asserts.is_valid_int_value(val)
            # Check bitmap value less than or equal to (Occupied)
            asserts.assert_less_equal(val, 1)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AbsMinHeatSetpointLimit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AbsMinHeatSetpointLimit)
            if val is not None:
                matter_asserts.assert_valid_int16(val, 'AbsMinHeatSetpointLimit')

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AbsMaxHeatSetpointLimit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AbsMaxHeatSetpointLimit)
            if val is not None:
                matter_asserts.assert_valid_int16(val, 'AbsMaxHeatSetpointLimit')

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AbsMinCoolSetpointLimit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AbsMinCoolSetpointLimit)
            if val is not None:
                matter_asserts.assert_valid_int16(val, 'AbsMinCoolSetpointLimit')

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AbsMaxCoolSetpointLimit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AbsMaxCoolSetpointLimit)
            if val is not None:
                matter_asserts.assert_valid_int16(val, 'AbsMaxCoolSetpointLimit')

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PICoolingDemand):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PICoolingDemand)
            if val is not None:
                matter_asserts.assert_valid_uint8(val, 'PICoolingDemand')
                asserts.assert_greater_equal(val, 0)
                asserts.assert_less_equal(val, 100)

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PIHeatingDemand):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PIHeatingDemand)
            if val is not None:
                matter_asserts.assert_valid_uint8(val, 'PIHeatingDemand')
                asserts.assert_greater_equal(val, 0)
                asserts.assert_less_equal(val, 100)

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.LocalTemperatureCalibration):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LocalTemperatureCalibration)
            if val is not None:
                matter_asserts.assert_valid_int8(val, 'LocalTemperatureCalibration')

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OccupiedCoolingSetpoint):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OccupiedCoolingSetpoint)
            matter_asserts.assert_valid_int16(val, 'OccupiedCoolingSetpoint')

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OccupiedHeatingSetpoint):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OccupiedHeatingSetpoint)
            matter_asserts.assert_valid_int16(val, 'OccupiedHeatingSetpoint')

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.UnoccupiedCoolingSetpoint):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UnoccupiedCoolingSetpoint)
            matter_asserts.assert_valid_int16(val, 'UnoccupiedCoolingSetpoint')

        self.step("14")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.UnoccupiedHeatingSetpoint):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UnoccupiedHeatingSetpoint)
            matter_asserts.assert_valid_int16(val, 'UnoccupiedHeatingSetpoint')

        self.step("15")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinHeatSetpointLimit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinHeatSetpointLimit)
            if val is not None:
                matter_asserts.assert_valid_int16(val, 'MinHeatSetpointLimit')

        self.step("16")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxHeatSetpointLimit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxHeatSetpointLimit)
            if val is not None:
                matter_asserts.assert_valid_int16(val, 'MaxHeatSetpointLimit')

        self.step("17")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinCoolSetpointLimit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinCoolSetpointLimit)
            if val is not None:
                matter_asserts.assert_valid_int16(val, 'MinCoolSetpointLimit')

        self.step("18")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxCoolSetpointLimit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxCoolSetpointLimit)
            if val is not None:
                matter_asserts.assert_valid_int16(val, 'MaxCoolSetpointLimit')

        self.step("19")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinSetpointDeadBand):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinSetpointDeadBand)
            matter_asserts.assert_valid_int8(val, 'MinSetpointDeadBand')
            asserts.assert_greater_equal(val, 0)
            asserts.assert_less_equal(val, 127)

        self.step("20")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RemoteSensing):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RemoteSensing)
            if val is not None:
                matter_asserts.is_valid_int_value(val)
                # Check bitmap value less than or equal to (LocalTemperature | OutdoorTemperature | Occupancy)
                asserts.assert_less_equal(val, 7)

        self.step("21")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ControlSequenceOfOperation)
        matter_asserts.assert_valid_enum(val, "ControlSequenceOfOperation attribute must return a ControlSequenceOfOperationEnum", cluster.Enums.ControlSequenceOfOperationEnum)

        self.step("22")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SystemMode)
        matter_asserts.assert_valid_enum(val, "SystemMode attribute must return a SystemModeEnum", cluster.Enums.SystemModeEnum)

        self.step("23")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ThermostatRunningMode):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ThermostatRunningMode)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "ThermostatRunningMode attribute must return a ThermostatRunningModeEnum", cluster.Enums.ThermostatRunningModeEnum)

        self.step("24")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.StartOfWeek):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.StartOfWeek)
            matter_asserts.assert_valid_enum(val, "StartOfWeek attribute must return a StartOfWeekEnum", cluster.Enums.StartOfWeekEnum)

        self.step("25")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfWeeklyTransitions):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfWeeklyTransitions)
            matter_asserts.assert_valid_uint8(val, 'NumberOfWeeklyTransitions')

        self.step("26")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfDailyTransitions):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfDailyTransitions)
            matter_asserts.assert_valid_uint8(val, 'NumberOfDailyTransitions')

        self.step("27")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TemperatureSetpointHold):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TemperatureSetpointHold)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "TemperatureSetpointHold attribute must return a TemperatureSetpointHoldEnum", cluster.Enums.TemperatureSetpointHoldEnum)

        self.step("28")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TemperatureSetpointHoldDuration):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TemperatureSetpointHoldDuration)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'TemperatureSetpointHoldDuration')
                asserts.assert_less_equal(val, 1440)

        self.step("29")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ThermostatProgrammingOperationMode):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ThermostatProgrammingOperationMode)
            if val is not None:
                matter_asserts.is_valid_int_value(val)
                # Check bitmap value less than or equal to (ScheduleActive | AutoRecovery | Economy)
                asserts.assert_less_equal(val, 7)

        self.step("30")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ThermostatRunningState):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ThermostatRunningState)
            if val is not None:
                matter_asserts.is_valid_int_value(val)
                # Check bitmap value less than or equal to (Heat | Cool | Fan | HeatStage2 | CoolStage2 | FanStage2 | FanStage3)
                asserts.assert_less_equal(val, 127)

        self.step("31")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SetpointChangeSource):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SetpointChangeSource)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "SetpointChangeSource attribute must return a SetpointChangeSourceEnum", cluster.Enums.SetpointChangeSourceEnum)

        self.step("32")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SetpointChangeAmount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SetpointChangeAmount)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int16(val, 'SetpointChangeAmount')

        self.step("33")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SetpointChangeSourceTimestamp):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SetpointChangeSourceTimestamp)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'SetpointChangeSourceTimestamp')

        self.step("34")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OccupiedSetback):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OccupiedSetback)
            if val is not NullValue:
                matter_asserts.assert_valid_uint8(val, 'OccupiedSetback')
                asserts.assert_greater_equal(val, self.OccupiedSetbackMin)
                asserts.assert_less_equal(val, self.OccupiedSetbackMax)

        self.step("35")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OccupiedSetbackMin):
            self.OccupiedSetbackMin = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OccupiedSetbackMin)
            if self.OccupiedSetbackMin is not NullValue:
                matter_asserts.assert_valid_uint8(self.OccupiedSetbackMin, 'OccupiedSetbackMin')
                asserts.assert_less_equal(self.OccupiedSetbackMin, self.OccupiedSetbackMax)

        self.step("36")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OccupiedSetbackMax):
            self.OccupiedSetbackMax = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OccupiedSetbackMax)
            if self.OccupiedSetbackMax is not NullValue:
                matter_asserts.assert_valid_uint8(self.OccupiedSetbackMax, 'OccupiedSetbackMax')
                asserts.assert_greater_equal(self.OccupiedSetbackMax, self.OccupiedSetbackMin)
                asserts.assert_less_equal(self.OccupiedSetbackMax, 254)

        self.step("37")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.UnoccupiedSetback):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UnoccupiedSetback)
            if val is not NullValue:
                matter_asserts.assert_valid_uint8(val, 'UnoccupiedSetback')
                asserts.assert_greater_equal(val, self.UnoccupiedSetbackMin)
                asserts.assert_less_equal(val, self.UnoccupiedSetbackMax)

        self.step("38")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.UnoccupiedSetbackMin):
            self.UnoccupiedSetbackMin = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UnoccupiedSetbackMin)
            if self.UnoccupiedSetbackMin is not NullValue:
                matter_asserts.assert_valid_uint8(self.UnoccupiedSetbackMin, 'UnoccupiedSetbackMin')
                asserts.assert_less_equal(self.UnoccupiedSetbackMin, self.UnoccupiedSetbackMax)

        self.step("39")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.UnoccupiedSetbackMax):
            self.UnoccupiedSetbackMax = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UnoccupiedSetbackMax)
            if self.UnoccupiedSetbackMax is not NullValue:
                matter_asserts.assert_valid_uint8(self.UnoccupiedSetbackMax, 'UnoccupiedSetbackMax')
                asserts.assert_greater_equal(self.UnoccupiedSetbackMax, self.UnoccupiedSetbackMin)
                asserts.assert_less_equal(self.UnoccupiedSetbackMax, 254)

        self.step("40")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.EmergencyHeatDelta):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EmergencyHeatDelta)
            if val is not None:
                matter_asserts.assert_valid_uint8(val, 'EmergencyHeatDelta')

        self.step("41")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ACType):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ACType)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "ACType attribute must return a ACTypeEnum", cluster.Enums.ACTypeEnum)

        self.step("42")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ACCapacity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ACCapacity)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ACCapacity')

        self.step("43")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ACRefrigerantType):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ACRefrigerantType)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "ACRefrigerantType attribute must return a ACRefrigerantTypeEnum", cluster.Enums.ACRefrigerantTypeEnum)

        self.step("44")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ACCompressorType):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ACCompressorType)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "ACCompressorType attribute must return a ACCompressorTypeEnum", cluster.Enums.ACCompressorTypeEnum)

        self.step("45")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ACErrorCode):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ACErrorCode)
            if val is not None:
                matter_asserts.is_valid_int_value(val)
                # Check bitmap value less than or equal to (CompressorFail | RoomSensorFail | OutdoorSensorFail | CoilSensorFail | FanFail)
                asserts.assert_less_equal(val, 31)

        self.step("46")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ACLouverPosition):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ACLouverPosition)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "ACLouverPosition attribute must return a ACLouverPositionEnum", cluster.Enums.ACLouverPositionEnum)

        self.step("47")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ACCoilTemperature):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ACCoilTemperature)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int16(val, 'ACCoilTemperature')

        self.step("48")

        self.step("49")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PresetTypes):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PresetTypes)
            matter_asserts.assert_list(val, "PresetTypes attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "PresetTypes attribute must contain PresetTypeStruct elements", cluster.Structs.PresetTypeStruct)
            for item in val:
                await self.test_checkPresetTypeStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("50")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ScheduleTypes):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ScheduleTypes)
            matter_asserts.assert_list(val, "ScheduleTypes attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "ScheduleTypes attribute must contain ScheduleTypeStruct elements", cluster.Structs.ScheduleTypeStruct)
            for item in val:
                await self.test_checkScheduleTypeStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("51")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfPresets):
            self.NumberOfPresets = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfPresets)
            matter_asserts.assert_valid_uint8(self.NumberOfPresets, 'NumberOfPresets')

        self.step("52")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfSchedules):
            self.NumberOfSchedules = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfSchedules)
            matter_asserts.assert_valid_uint8(self.NumberOfSchedules, 'NumberOfSchedules')

        self.step("53")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfScheduleTransitions):
            self.NumberOfScheduleTransitions = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfScheduleTransitions)
            matter_asserts.assert_valid_uint8(self.NumberOfScheduleTransitions, 'NumberOfScheduleTransitions')

        self.step("54")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfScheduleTransitionPerDay):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfScheduleTransitionPerDay)
            if val is not NullValue:
                matter_asserts.assert_valid_uint8(val, 'NumberOfScheduleTransitionPerDay')

        self.step("55")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActivePresetHandle):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActivePresetHandle)
            if val is not NullValue:
                matter_asserts.assert_is_octstr(val, "ActivePresetHandle must be an octstr")
                asserts.assert_less_equal(len(val), 16, "ActivePresetHandle must have length at most 16!")

        self.step("56")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveScheduleHandle):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveScheduleHandle)
            if val is not NullValue:
                matter_asserts.assert_is_octstr(val, "ActiveScheduleHandle must be an octstr")
                asserts.assert_less_equal(len(val), 16, "ActiveScheduleHandle must have length at most 16!")

        self.step("57")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Presets):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Presets)
            matter_asserts.assert_list(val, "Presets attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "Presets attribute must contain PresetStruct elements", cluster.Structs.PresetStruct)
            for item in val:
                await self.test_checkPresetStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_less_equal(len(val), self.NumberOfPresets, "Presets must have at most self.NumberOfPresets entries!")

        self.step("58")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Schedules):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Schedules)
            matter_asserts.assert_list(val, "Schedules attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "Schedules attribute must contain ScheduleStruct elements", cluster.Structs.ScheduleStruct)
            for item in val:
                await self.test_checkScheduleStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("59")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SetpointHoldExpiryTimestamp):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SetpointHoldExpiryTimestamp)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'SetpointHoldExpiryTimestamp')

    async def test_checkPresetStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Thermostat = None, 
                                 struct: Clusters.Thermostat.Structs.PresetStruct = None):
        if struct.presetHandle is not NullValue:
            matter_asserts.assert_is_octstr(struct.presetHandle, "PresetHandle must be an octstr")
            asserts.assert_less_equal(len(struct.presetHandle), 16, "PresetHandle must have length at most 16!")
        matter_asserts.assert_valid_enum(struct.presetScenario, "PresetScenario attribute must return a PresetScenarioEnum", cluster.Enums.PresetScenarioEnum)
        if struct.name is not NullValue and struct.name is not None:
            matter_asserts.assert_is_string(struct.name, "Name must be a string")
            asserts.assert_less_equal(len(struct.name), 64, "Name must have length at most 64!")
        matter_asserts.assert_valid_int16(struct.coolingSetpoint, 'CoolingSetpoint')
        matter_asserts.assert_valid_int16(struct.heatingSetpoint, 'HeatingSetpoint')
        if struct.builtIn is not NullValue:
            matter_asserts.assert_valid_bool(struct.builtIn, 'BuiltIn')

    async def test_checkPresetTypeStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Thermostat = None, 
                                 struct: Clusters.Thermostat.Structs.PresetTypeStruct = None):
        matter_asserts.assert_valid_enum(struct.presetScenario, "PresetScenario attribute must return a PresetScenarioEnum", cluster.Enums.PresetScenarioEnum)
        matter_asserts.assert_valid_uint8(struct.numberOfPresets, 'NumberOfPresets')
        matter_asserts.is_valid_int_value(struct.presetTypeFeatures)
        # Check bitmap value less than or equal to (Automatic | SupportsNames)
        asserts.assert_less_equal(struct.presetTypeFeatures, 3)

    async def test_checkScheduleStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Thermostat = None, 
                                 struct: Clusters.Thermostat.Structs.ScheduleStruct = None):
        if struct.scheduleHandle is not NullValue:
            matter_asserts.assert_is_octstr(struct.scheduleHandle, "ScheduleHandle must be an octstr")
            asserts.assert_less_equal(len(struct.scheduleHandle), 16, "ScheduleHandle must have length at most 16!")
        matter_asserts.assert_valid_enum(struct.systemMode, "SystemMode attribute must return a SystemModeEnum", cluster.Enums.SystemModeEnum)
        if struct.name is not None:
            matter_asserts.assert_is_string(struct.name, "Name must be a string")
            asserts.assert_less_equal(len(struct.name), 64, "Name must have length at most 64!")
        if struct.presetHandle is not None:
            matter_asserts.assert_is_octstr(struct.presetHandle, "PresetHandle must be an octstr")
            asserts.assert_less_equal(len(struct.presetHandle), 16, "PresetHandle must have length at most 16!")
        matter_asserts.assert_list(struct.transitions, "Transitions attribute must return a list")
        matter_asserts.assert_list_element_type(struct.transitions,  "Transitions attribute must contain ScheduleTransitionStruct elements", cluster.Structs.ScheduleTransitionStruct)
        for item in struct.transitions:
            await self.test_checkScheduleTransitionStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_greater_equal(len(struct.transitions), 1, "Transitions must have at least 1 entries!")
        asserts.assert_less_equal(len(struct.transitions), self.NumberOfScheduleTransitions, "Transitions must have at most self.NumberOfScheduleTransitions entries!")
        if struct.builtIn is not NullValue:
            matter_asserts.assert_valid_bool(struct.builtIn, 'BuiltIn')

    async def test_checkScheduleTransitionStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Thermostat = None, 
                                 struct: Clusters.Thermostat.Structs.ScheduleTransitionStruct = None):
        matter_asserts.is_valid_int_value(struct.dayOfWeek)
        # Check bitmap value less than or equal to (Sunday | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Away)
        asserts.assert_less_equal(struct.dayOfWeek, 255)
        matter_asserts.assert_valid_uint16(struct.transitionTime, 'TransitionTime')
        asserts.assert_less_equal(struct.transitionTime, 1439)
        if struct.presetHandle is not None:
            matter_asserts.assert_is_octstr(struct.presetHandle, "PresetHandle must be an octstr")
            asserts.assert_less_equal(len(struct.presetHandle), 16, "PresetHandle must have length at most 16!")
        if struct.systemMode is not None:
            matter_asserts.assert_valid_enum(struct.systemMode, "SystemMode attribute must return a SystemModeEnum", cluster.Enums.SystemModeEnum)
        if struct.coolingSetpoint is not None:
            matter_asserts.assert_valid_int16(struct.coolingSetpoint, 'CoolingSetpoint')
        if struct.heatingSetpoint is not None:
            matter_asserts.assert_valid_int16(struct.heatingSetpoint, 'HeatingSetpoint')

    async def test_checkScheduleTypeStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Thermostat = None, 
                                 struct: Clusters.Thermostat.Structs.ScheduleTypeStruct = None):
        matter_asserts.assert_valid_enum(struct.systemMode, "SystemMode attribute must return a SystemModeEnum", cluster.Enums.SystemModeEnum)
        matter_asserts.assert_valid_uint8(struct.numberOfSchedules, 'NumberOfSchedules')
        asserts.assert_less_equal(struct.numberOfSchedules, self.NumberOfSchedules)
        matter_asserts.is_valid_int_value(struct.scheduleTypeFeatures)
        # Check bitmap value less than or equal to (SupportsPresets | SupportsSetpoints | SupportsNames | SupportsOff)
        asserts.assert_less_equal(struct.scheduleTypeFeatures, 15)

if __name__ == "__main__":
    default_matter_test_main()
