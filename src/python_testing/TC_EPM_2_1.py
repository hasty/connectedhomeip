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
# test-runner-runs: run1
# test-runner-run/run1/app: ${ALL_CLUSTERS_APP}
# test-runner-run/run1/factoryreset: True
# test-runner-run/run1/quiet: True
# test-runner-run/run1/app-args: --discriminator 1234 --KVS kvs1 --trace-to json:${TRACE_APP}.json
# test-runner-run/run1/script-args: --storage-path admin_storage.json --commissioning-method on-network --discriminator 1234 --passcode 20202021 --endpoint 1 --trace-to json:${TRACE_TEST_JSON}.json --trace-to perfetto:${TRACE_TEST_PERFETTO}.perfetto
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
from chip.testing.matter_testing import MatterBaseTest, TestStep, async_test_body, default_matter_test_main
from mobly import asserts

logger = logging.getLogger(__name__)

cluster = Clusters.ElectricalPowerMeasurement

class EPM_2_1(MatterBaseTest):

    def desc_EPM_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_EPM_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["EPM"]

    def steps_EPM_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read PowerMode attribute"),
            TestStep("2", "Read NumberOfMeasurementTypes attribute"),
            TestStep("3", "Read Accuracy attribute"),
            TestStep("4", "Read Ranges attribute"),
            TestStep("5", "Read Voltage attribute"),
            TestStep("6", "Read ActiveCurrent attribute"),
            TestStep("7", "Read ReactiveCurrent attribute"),
            TestStep("8", "Read ApparentCurrent attribute"),
            TestStep("9", "Read ActivePower attribute"),
            TestStep("10", "Read ReactivePower attribute"),
            TestStep("11", "Read ApparentPower attribute"),
            TestStep("12", "Read RMSVoltage attribute"),
            TestStep("13", "Read RMSCurrent attribute"),
            TestStep("14", "Read RMSPower attribute"),
            TestStep("15", "Read Frequency attribute"),
            TestStep("16", "Read HarmonicCurrents attribute"),
            TestStep("17", "Read HarmonicPhases attribute"),
            TestStep("18", "Read PowerFactor attribute"),
            TestStep("19", "Read NeutralCurrent attribute"),
        ]
        return steps

    MinSystime = None
    MinTimestamp = None
    NumberOfMeasurementTypes = None
    StartSystime = None
    StartTimestamp = None

    @async_test_body
    async def test_EPM_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PowerMode)
        matter_asserts.assert_valid_enum(val, "PowerMode attribute must return a PowerModeEnum", cluster.Enums.PowerModeEnum)

        self.step("2")
        self.NumberOfMeasurementTypes = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfMeasurementTypes)
        matter_asserts.assert_valid_uint8(self.NumberOfMeasurementTypes, 'NumberOfMeasurementTypes')
        asserts.assert_greater_equal(self.NumberOfMeasurementTypes, 1)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Accuracy)
        matter_asserts.assert_list(val, "Accuracy attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "Accuracy attribute must contain MeasurementAccuracyStruct elements", Globals.Structs.MeasurementAccuracyStruct)
        for item in val:
            await self.test_checkMeasurementAccuracyStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_greater_equal(len(val), 1, "Accuracy must have at least 1 entries!")
        asserts.assert_less_equal(len(val), self.NumberOfMeasurementTypes, "Accuracy must have at most self.NumberOfMeasurementTypes entries!")

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Ranges):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Ranges)
            if val is not None:
                matter_asserts.assert_list(val, "Ranges attribute must return a list")
                matter_asserts.assert_list_element_type(val,  "Ranges attribute must contain MeasurementRangeStruct elements", cluster.Structs.MeasurementRangeStruct)
                for item in val:
                    await self.test_checkMeasurementRangeStruct(endpoint=endpoint, cluster=cluster, struct=item)
                asserts.assert_greater_equal(len(val), 0, "Ranges must have at least 0 entries!")
                asserts.assert_less_equal(len(val), self.NumberOfMeasurementTypes, "Ranges must have at most self.NumberOfMeasurementTypes entries!")

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Voltage):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Voltage)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'Voltage')
                asserts.assert_greater_equal(val, -2e62)
                asserts.assert_less_equal(val, 2e62)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveCurrent)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'ActiveCurrent')
                asserts.assert_greater_equal(val, -2e62)
                asserts.assert_less_equal(val, 2e62)

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ReactiveCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ReactiveCurrent)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'ReactiveCurrent')
                asserts.assert_greater_equal(val, -2e62)
                asserts.assert_less_equal(val, 2e62)

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ApparentCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ApparentCurrent)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'ApparentCurrent')
                asserts.assert_greater_equal(val, -2e62)
                asserts.assert_less_equal(val, 2e62)

        self.step("9")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActivePower)
        if val is not NullValue:
            matter_asserts.assert_valid_int64(val, 'ActivePower')
            asserts.assert_greater_equal(val, -2e62)
            asserts.assert_less_equal(val, 2e62)

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ReactivePower):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ReactivePower)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'ReactivePower')
                asserts.assert_greater_equal(val, -2e62)
                asserts.assert_less_equal(val, 2e62)

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ApparentPower):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ApparentPower)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'ApparentPower')
                asserts.assert_greater_equal(val, -2e62)
                asserts.assert_less_equal(val, 2e62)

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RMSVoltage):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RMSVoltage)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'RMSVoltage')
                asserts.assert_greater_equal(val, -2e62)
                asserts.assert_less_equal(val, 2e62)

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RMSCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RMSCurrent)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'RMSCurrent')
                asserts.assert_greater_equal(val, -2e62)
                asserts.assert_less_equal(val, 2e62)

        self.step("14")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RMSPower):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RMSPower)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'RMSPower')
                asserts.assert_greater_equal(val, -2e62)
                asserts.assert_less_equal(val, 2e62)

        self.step("15")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Frequency):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Frequency)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'Frequency')
                asserts.assert_greater_equal(val, 0)
                asserts.assert_less_equal(val, 1000000)

        self.step("16")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.HarmonicCurrents):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.HarmonicCurrents)
            if val is not NullValue:
                matter_asserts.assert_list(val, "HarmonicCurrents attribute must return a list")
                matter_asserts.assert_list_element_type(val,  "HarmonicCurrents attribute must contain HarmonicMeasurementStruct elements", cluster.Structs.HarmonicMeasurementStruct)
                for item in val:
                    await self.test_checkHarmonicMeasurementStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("17")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.HarmonicPhases):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.HarmonicPhases)
            if val is not NullValue:
                matter_asserts.assert_list(val, "HarmonicPhases attribute must return a list")
                matter_asserts.assert_list_element_type(val,  "HarmonicPhases attribute must contain HarmonicMeasurementStruct elements", cluster.Structs.HarmonicMeasurementStruct)
                for item in val:
                    await self.test_checkHarmonicMeasurementStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("18")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PowerFactor):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PowerFactor)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'PowerFactor')
                asserts.assert_greater_equal(val, -10000)
                asserts.assert_less_equal(val, 10000)

        self.step("19")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NeutralCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NeutralCurrent)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int64(val, 'NeutralCurrent')
                asserts.assert_greater_equal(val, -2e62)
                asserts.assert_less_equal(val, 2e62)

    async def test_checkHarmonicMeasurementStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ElectricalPowerMeasurement = None, 
                                 struct: Clusters.ElectricalPowerMeasurement.Structs.HarmonicMeasurementStruct = None):
        matter_asserts.assert_valid_uint8(struct.order, 'Order')
        asserts.assert_greater_equal(struct.order, 1)
        if struct.measurement is not NullValue:
            matter_asserts.assert_valid_int64(struct.measurement, 'Measurement')
            asserts.assert_greater_equal(struct.measurement, -2e62)
            asserts.assert_less_equal(struct.measurement, 2e62)

    async def test_checkMeasurementAccuracyRangeStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ElectricalPowerMeasurement = None, 
                                 struct: Globals.Structs.MeasurementAccuracyRangeStruct = None):
        matter_asserts.assert_valid_int64(struct.rangeMin, 'RangeMin')
        asserts.assert_greater_equal(struct.rangeMin, -2e62)
        asserts.assert_less_equal(struct.rangeMin, 2e62)
        matter_asserts.assert_valid_int64(struct.rangeMax, 'RangeMax')
        asserts.assert_greater_equal(struct.rangeMax, -2e62)
        asserts.assert_less_equal(struct.rangeMax, 2e62)
        if struct.percentMax is not None:
            matter_asserts.assert_valid_uint16(struct.percentMax, 'PercentMax')
        if struct.percentMin is not None:
            matter_asserts.assert_valid_uint16(struct.percentMin, 'PercentMin')
            asserts.assert_less_equal(struct.percentMin, struct.PercentTypical)
        if struct.percentTypical is not None:
            matter_asserts.assert_valid_uint16(struct.percentTypical, 'PercentTypical')
            asserts.assert_greater_equal(struct.percentTypical, struct.PercentMin)
            asserts.assert_less_equal(struct.percentTypical, struct.PercentMax)
        if struct.fixedMax is not None:
            matter_asserts.assert_valid_uint64(struct.fixedMax, 'FixedMax')
            asserts.assert_less_equal(struct.fixedMax, 2e62 - 1)
        if struct.fixedMin is not None:
            matter_asserts.assert_valid_uint64(struct.fixedMin, 'FixedMin')
            asserts.assert_less_equal(struct.fixedMin, struct.FixedMax)
        if struct.fixedTypical is not None:
            matter_asserts.assert_valid_uint64(struct.fixedTypical, 'FixedTypical')
            asserts.assert_greater_equal(struct.fixedTypical, struct.FixedMin)
            asserts.assert_less_equal(struct.fixedTypical, struct.FixedMax)

    async def test_checkMeasurementAccuracyStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ElectricalPowerMeasurement = None, 
                                 struct: Globals.Structs.MeasurementAccuracyStruct = None):
        matter_asserts.assert_valid_enum(struct.measurementType, "MeasurementType attribute must return a MeasurementTypeEnum", Globals.Enums.MeasurementTypeEnum)
        matter_asserts.assert_valid_bool(struct.measured, 'Measured')
        matter_asserts.assert_valid_int64(struct.minMeasuredValue, 'MinMeasuredValue')
        asserts.assert_greater_equal(struct.minMeasuredValue, -2e62)
        asserts.assert_less_equal(struct.minMeasuredValue, 2e62)
        matter_asserts.assert_valid_int64(struct.maxMeasuredValue, 'MaxMeasuredValue')
        asserts.assert_greater_equal(struct.maxMeasuredValue, -2e62)
        asserts.assert_less_equal(struct.maxMeasuredValue, 2e62)
        matter_asserts.assert_list(struct.accuracyRanges, "AccuracyRanges attribute must return a list")
        matter_asserts.assert_list_element_type(struct.accuracyRanges,  "AccuracyRanges attribute must contain MeasurementAccuracyRangeStruct elements", Globals.Structs.MeasurementAccuracyRangeStruct)
        for item in struct.accuracyRanges:
            await self.test_checkMeasurementAccuracyRangeStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_greater_equal(len(struct.accuracyRanges), 1, "AccuracyRanges must have at least 1 entries!")

    async def test_checkMeasurementRangeStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ElectricalPowerMeasurement = None, 
                                 struct: Clusters.ElectricalPowerMeasurement.Structs.MeasurementRangeStruct = None):
        matter_asserts.assert_valid_enum(struct.measurementType, "MeasurementType attribute must return a MeasurementTypeEnum", Globals.Enums.MeasurementTypeEnum)
        matter_asserts.assert_valid_int64(struct.min, 'Min')
        asserts.assert_greater_equal(struct.min, -2e62)
        asserts.assert_less_equal(struct.min, 2e62)
        matter_asserts.assert_valid_int64(struct.max, 'Max')
        asserts.assert_greater_equal(struct.max, -2e62)
        asserts.assert_less_equal(struct.max, 2e62)
        matter_asserts.assert_valid_uint32(struct.startTimestamp, 'StartTimestamp')
        if struct.endTimestamp is not None:
            matter_asserts.assert_valid_uint32(struct.endTimestamp, 'EndTimestamp')
            asserts.assert_greater_equal(struct.endTimestamp, struct.StartTimestamp + 1)
        matter_asserts.assert_valid_uint32(struct.minTimestamp, 'MinTimestamp')
        matter_asserts.assert_valid_uint32(struct.maxTimestamp, 'MaxTimestamp')
        asserts.assert_greater_equal(struct.maxTimestamp, struct.MinTimestamp + 1)
        matter_asserts.assert_valid_uint64(struct.startSystime, 'StartSystime')
        if struct.endSystime is not None:
            matter_asserts.assert_valid_uint64(struct.endSystime, 'EndSystime')
            asserts.assert_greater_equal(struct.endSystime, struct.StartSystime + 1)
        matter_asserts.assert_valid_uint64(struct.minSystime, 'MinSystime')
        matter_asserts.assert_valid_uint64(struct.maxSystime, 'MaxSystime')
        asserts.assert_greater_equal(struct.maxSystime, struct.MinSystime + 1)

if __name__ == "__main__":
    default_matter_test_main()
