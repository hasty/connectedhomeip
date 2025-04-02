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

cluster = Clusters.DeviceEnergyManagement

class DEM_2_1(MatterBaseTest):

    def desc_DEM_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_DEM_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["DEM"]

    def steps_DEM_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read ESAType attribute"),
            TestStep("2", "Read ESACanGenerate attribute"),
            TestStep("3", "Read ESAState attribute"),
            TestStep("4", "Read AbsMinPower attribute"),
            TestStep("5", "Read AbsMaxPower attribute"),
            TestStep("6", "Read PowerAdjustmentCapability attribute"),
            TestStep("7", "Read Forecast attribute"),
            TestStep("8", "Read OptOutState attribute"),
        ]

        return steps

    AbsMinPower = None
    MinDuration = None
    MinPower = None

    @async_test_body
    async def test_DEM_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ESAType)
        matter_asserts.assert_valid_enum(val, "ESAType attribute must return a Clusters.DeviceEnergyManagement.Enums.ESATypeEnum", Clusters.DeviceEnergyManagement.Enums.ESATypeEnum)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ESACanGenerate)
        matter_asserts.assert_valid_bool(val, 'ESACanGenerate')

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ESAState)
        matter_asserts.assert_valid_enum(val, "ESAState attribute must return a Clusters.DeviceEnergyManagement.Enums.ESAStateEnum", Clusters.DeviceEnergyManagement.Enums.ESAStateEnum)

        self.step("4")
        self.AbsMinPower = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AbsMinPower)
        matter_asserts.assert_valid_int64(self.AbsMinPower, 'AbsMinPower')

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AbsMaxPower)
        matter_asserts.assert_valid_int64(val, 'AbsMaxPower')
        asserts.assert_greater_equal(val, self.AbsMinPower)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PowerAdjustmentCapability):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PowerAdjustmentCapability)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, Clusters.DeviceEnergyManagement.Structs.PowerAdjustCapabilityStruct),
                                            f"val must be of type Clusters.DeviceEnergyManagement.Structs.PowerAdjustCapabilityStruct")
                await self.test_checkPowerAdjustCapabilityStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Forecast):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Forecast)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, Clusters.DeviceEnergyManagement.Structs.ForecastStruct),
                                            f"val must be of type Clusters.DeviceEnergyManagement.Structs.ForecastStruct")
                await self.test_checkForecastStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OptOutState):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OptOutState)
            matter_asserts.assert_valid_enum(val, "OptOutState attribute must return a Clusters.DeviceEnergyManagement.Enums.OptOutStateEnum", Clusters.DeviceEnergyManagement.Enums.OptOutStateEnum)


    async def test_checkCostStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.DeviceEnergyManagement = None, 
                                 struct: Clusters.DeviceEnergyManagement.Structs.CostStruct = None):
        matter_asserts.assert_valid_enum(struct.costType, "CostType attribute must return a Clusters.DeviceEnergyManagement.Enums.CostTypeEnum", Clusters.DeviceEnergyManagement.Enums.CostTypeEnum)
        matter_asserts.assert_valid_int32(struct.value, 'Value')
        matter_asserts.assert_valid_uint8(struct.decimalPoints, 'DecimalPoints')
        if struct.currency is not None:
            matter_asserts.assert_valid_uint16(struct.currency, 'Currency')
            asserts.assert_less_equal(struct.currency, 999)

    async def test_checkForecastStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.DeviceEnergyManagement = None, 
                                 struct: Clusters.DeviceEnergyManagement.Structs.ForecastStruct = None):
        matter_asserts.assert_valid_uint32(struct.forecastID, 'ForecastID')
        if struct.activeSlotNumber is not NullValue:
            matter_asserts.assert_valid_uint16(struct.activeSlotNumber, 'ActiveSlotNumber')
        matter_asserts.assert_valid_uint32(struct.startTime, 'StartTime')
        matter_asserts.assert_valid_uint32(struct.endTime, 'EndTime')
        if struct.earliestStartTime is not NullValue:
            matter_asserts.assert_valid_uint32(struct.earliestStartTime, 'EarliestStartTime')
        matter_asserts.assert_valid_uint32(struct.latestEndTime, 'LatestEndTime')
        matter_asserts.assert_valid_bool(struct.isPausable, 'IsPausable')
        matter_asserts.assert_list(struct.slots, "Slots attribute must return a list")
        matter_asserts.assert_list_element_type(struct.slots,  "Slots attribute must contain Clusters.DeviceEnergyManagement.Structs.SlotStruct elements", Clusters.DeviceEnergyManagement.Structs.SlotStruct)
        for item in struct.slots:
            await self.test_checkSlotStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(struct.slots), 10, "Slots must have at most 10 entries!")
        matter_asserts.assert_valid_enum(struct.forecastUpdateReason, "ForecastUpdateReason attribute must return a Clusters.DeviceEnergyManagement.Enums.ForecastUpdateReasonEnum", Clusters.DeviceEnergyManagement.Enums.ForecastUpdateReasonEnum)

    async def test_checkPowerAdjustCapabilityStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.DeviceEnergyManagement = None, 
                                 struct: Clusters.DeviceEnergyManagement.Structs.PowerAdjustCapabilityStruct = None):
        if struct.powerAdjustCapability is not NullValue:
            matter_asserts.assert_list(struct.powerAdjustCapability, "PowerAdjustCapability attribute must return a list")
            matter_asserts.assert_list_element_type(struct.powerAdjustCapability,  "PowerAdjustCapability attribute must contain Clusters.DeviceEnergyManagement.Structs.PowerAdjustStruct elements", Clusters.DeviceEnergyManagement.Structs.PowerAdjustStruct)
            for item in struct.powerAdjustCapability:
                await self.test_checkPowerAdjustStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_less_equal(len(struct.powerAdjustCapability), 8, "PowerAdjustCapability must have at most 8 entries!")
        matter_asserts.assert_valid_enum(struct.cause, "Cause attribute must return a Clusters.DeviceEnergyManagement.Enums.PowerAdjustReasonEnum", Clusters.DeviceEnergyManagement.Enums.PowerAdjustReasonEnum)

    async def test_checkPowerAdjustStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.DeviceEnergyManagement = None, 
                                 struct: Clusters.DeviceEnergyManagement.Structs.PowerAdjustStruct = None):
        matter_asserts.assert_valid_int64(struct.minPower, 'MinPower')
        matter_asserts.assert_valid_int64(struct.maxPower, 'MaxPower')
        asserts.assert_greater_equal(struct.maxPower, struct.MinPower)
        matter_asserts.assert_valid_uint32(struct.minDuration, 'MinDuration')
        matter_asserts.assert_valid_uint32(struct.maxDuration, 'MaxDuration')
        asserts.assert_greater_equal(struct.maxDuration, struct.MinDuration)

    async def test_checkSlotStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.DeviceEnergyManagement = None, 
                                 struct: Clusters.DeviceEnergyManagement.Structs.SlotStruct = None):
        matter_asserts.assert_valid_uint32(struct.minDuration, 'MinDuration')
        matter_asserts.assert_valid_uint32(struct.maxDuration, 'MaxDuration')
        matter_asserts.assert_valid_uint32(struct.defaultDuration, 'DefaultDuration')
        matter_asserts.assert_valid_uint32(struct.elapsedSlotTime, 'ElapsedSlotTime')
        matter_asserts.assert_valid_uint32(struct.remainingSlotTime, 'RemainingSlotTime')
        matter_asserts.assert_valid_bool(struct.slotIsPausable, 'SlotIsPausable')
        matter_asserts.assert_valid_uint32(struct.minPauseDuration, 'MinPauseDuration')
        matter_asserts.assert_valid_uint32(struct.maxPauseDuration, 'MaxPauseDuration')
        matter_asserts.assert_valid_uint16(struct.manufacturerEsaState, 'ManufacturerESAState')
        matter_asserts.assert_valid_int64(struct.nominalPower, 'NominalPower')
        matter_asserts.assert_valid_int64(struct.minPower, 'MinPower')
        matter_asserts.assert_valid_int64(struct.maxPower, 'MaxPower')
        matter_asserts.assert_valid_int64(struct.nominalEnergy, 'NominalEnergy')
        if struct.costs is not None:
            matter_asserts.assert_list(struct.costs, "Costs attribute must return a list")
            matter_asserts.assert_list_element_type(struct.costs,  "Costs attribute must contain Clusters.DeviceEnergyManagement.Structs.CostStruct elements", Clusters.DeviceEnergyManagement.Structs.CostStruct)
            for item in struct.costs:
                await self.test_checkCostStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_less_equal(len(struct.costs), 5, "Costs must have at most 5 entries!")
        matter_asserts.assert_valid_int64(struct.minPowerAdjustment, 'MinPowerAdjustment')
        matter_asserts.assert_valid_int64(struct.maxPowerAdjustment, 'MaxPowerAdjustment')
        matter_asserts.assert_valid_uint32(struct.minDurationAdjustment, 'MinDurationAdjustment')
        matter_asserts.assert_valid_uint32(struct.maxDurationAdjustment, 'MaxDurationAdjustment')


if __name__ == "__main__":
    default_matter_test_main()
