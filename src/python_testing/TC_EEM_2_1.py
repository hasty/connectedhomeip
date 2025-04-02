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

cluster = Clusters.ElectricalEnergyMeasurement

class EEM_2_1(MatterBaseTest):

    def desc_EEM_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_EEM_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["EEM.S"]

    def steps_EEM_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read Accuracy attribute"),
            TestStep("2", "Read CumulativeEnergyImported attribute"),
            TestStep("3", "Read CumulativeEnergyExported attribute"),
            TestStep("4", "Read PeriodicEnergyImported attribute"),
            TestStep("5", "Read PeriodicEnergyExported attribute"),
            TestStep("6", "Read CumulativeEnergyReset attribute"),
        ]
        return steps

    StartSystime = None
    StartTimestamp = None

    @run_if_endpoint_matches(has_cluster(Clusters.ElectricalEnergyMeasurement))
    async def test_EEM_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Accuracy)
        asserts.assert_true(isinstance(val, Globals.Structs.MeasurementAccuracyStruct), f"val must be of type MeasurementAccuracyStruct")
        await self.test_checkMeasurementAccuracyStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CumulativeEnergyImported):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CumulativeEnergyImported)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, cluster.Structs.EnergyMeasurementStruct), f"val must be of type EnergyMeasurementStruct")
                await self.test_checkEnergyMeasurementStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CumulativeEnergyExported):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CumulativeEnergyExported)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, cluster.Structs.EnergyMeasurementStruct), f"val must be of type EnergyMeasurementStruct")
                await self.test_checkEnergyMeasurementStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PeriodicEnergyImported):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PeriodicEnergyImported)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, cluster.Structs.EnergyMeasurementStruct), f"val must be of type EnergyMeasurementStruct")
                await self.test_checkEnergyMeasurementStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PeriodicEnergyExported):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PeriodicEnergyExported)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, cluster.Structs.EnergyMeasurementStruct), f"val must be of type EnergyMeasurementStruct")
                await self.test_checkEnergyMeasurementStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CumulativeEnergyReset):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CumulativeEnergyReset)
            if val is not NullValue and val is not None:
                asserts.assert_true(isinstance(val, cluster.Structs.CumulativeEnergyResetStruct), f"val must be of type CumulativeEnergyResetStruct")
                await self.test_checkCumulativeEnergyResetStruct(endpoint=endpoint, cluster=cluster, struct=val)

    async def test_checkCumulativeEnergyResetStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ElectricalEnergyMeasurement = None, 
                                 struct: Clusters.ElectricalEnergyMeasurement.Structs.CumulativeEnergyResetStruct = None):
        if struct.importedResetTimestamp is not NullValue and struct.importedResetTimestamp is not None:
            matter_asserts.assert_valid_uint32(struct.importedResetTimestamp, 'ImportedResetTimestamp')
        if struct.exportedResetTimestamp is not NullValue and struct.exportedResetTimestamp is not None:
            matter_asserts.assert_valid_uint32(struct.exportedResetTimestamp, 'ExportedResetTimestamp')
        if struct.importedResetSystime is not NullValue and struct.importedResetSystime is not None:
            matter_asserts.assert_valid_uint64(struct.importedResetSystime, 'ImportedResetSystime')
        if struct.exportedResetSystime is not NullValue and struct.exportedResetSystime is not None:
            matter_asserts.assert_valid_uint64(struct.exportedResetSystime, 'ExportedResetSystime')

    async def test_checkEnergyMeasurementStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ElectricalEnergyMeasurement = None, 
                                 struct: Clusters.ElectricalEnergyMeasurement.Structs.EnergyMeasurementStruct = None):
        matter_asserts.assert_valid_int64(struct.energy, 'Energy')
        asserts.assert_greater_equal(struct.energy, 0)
        asserts.assert_less_equal(struct.energy, 2e62)
        if struct.startTimestamp is not None:
            matter_asserts.assert_valid_uint32(struct.startTimestamp, 'StartTimestamp')
        if struct.endTimestamp is not None:
            matter_asserts.assert_valid_uint32(struct.endTimestamp, 'EndTimestamp')
            asserts.assert_greater_equal(struct.endTimestamp, struct.StartTimestamp + 1)
        if struct.startSystime is not None:
            matter_asserts.assert_valid_uint64(struct.startSystime, 'StartSystime')
        if struct.endSystime is not None:
            matter_asserts.assert_valid_uint64(struct.endSystime, 'EndSystime')
            asserts.assert_greater_equal(struct.endSystime, struct.StartSystime + 1)
        matter_asserts.assert_valid_int64(struct.apparentEnergy, 'ApparentEnergy')
        asserts.assert_greater_equal(struct.apparentEnergy, 0)
        asserts.assert_less_equal(struct.apparentEnergy, 2e62)
        matter_asserts.assert_valid_int64(struct.reactiveEnergy, 'ReactiveEnergy')
        asserts.assert_greater_equal(struct.reactiveEnergy, 0)
        asserts.assert_less_equal(struct.reactiveEnergy, 2e62)

    async def test_checkMeasurementAccuracyRangeStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ElectricalEnergyMeasurement = None, 
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
                                 cluster: Clusters.ElectricalEnergyMeasurement = None, 
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

if __name__ == "__main__":
    default_matter_test_main()
