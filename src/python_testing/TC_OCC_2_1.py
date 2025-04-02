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

cluster = Clusters.OccupancySensing

class OCC_2_1(MatterBaseTest):

    def desc_OCC_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_OCC_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["OCC"]

    def steps_OCC_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read Occupancy attribute"),
            TestStep("2", "Read OccupancySensorType attribute"),
            TestStep("3", "Read OccupancySensorTypeBitmap attribute"),
            TestStep("4", "Read HoldTime attribute"),
            TestStep("5", "Read HoldTimeLimits attribute"),
            TestStep("6", "Read PIROccupiedToUnoccupiedDelay attribute"),
            TestStep("7", "Read PIRUnoccupiedToOccupiedDelay attribute"),
            TestStep("8", "Read PIRUnoccupiedToOccupiedThreshold attribute"),
            TestStep("9", "Read UltrasonicOccupiedToUnoccupiedDelay attribute"),
            TestStep("10", "Read UltrasonicUnoccupiedToOccupiedDelay attribute"),
            TestStep("11", "Read UltrasonicUnoccupiedToOccupiedThreshold attribute"),
            TestStep("12", "Read PhysicalContactOccupiedToUnoccupiedDelay attribute"),
            TestStep("13", "Read PhysicalContactUnoccupiedToOccupiedDelay attribute"),
            TestStep("14", "Read PhysicalContactUnoccupiedToOccupiedThreshold attribute"),
        ]

        return steps

    HoldTimeLimits = None
    HoldTimeMax = None
    HoldTimeMin = None

    @async_test_body
    async def test_OCC_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Occupancy)
        matter_asserts.is_valid_int_value(val)
        asserts.assert_greater_equal(val, 0)
        asserts.assert_less_equal(val, 1)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OccupancySensorType)
        if val is not None:
            matter_asserts.assert_valid_enum(val, "OccupancySensorType attribute must return a OccupancySensorTypeEnum", cluster.Enums.OccupancySensorTypeEnum)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OccupancySensorTypeBitmap)
        if val is not None:
            matter_asserts.is_valid_int_value(val)
            asserts.assert_greater_equal(val, 0)
            asserts.assert_less_equal(val, 7)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.HoldTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.HoldTime)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'HoldTime')
                asserts.assert_greater_equal(val, self.HoldTimeLimits)
                asserts.assert_less_equal(val, self.HoldTimeLimits)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.HoldTimeLimits):
            self.HoldTimeLimits = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.HoldTimeLimits)
            asserts.assert_true(isinstance(self.HoldTimeLimits, cluster.Structs.HoldTimeLimitsStruct), f"self.HoldTimeLimits must be of type HoldTimeLimitsStruct")
            await self.test_checkHoldTimeLimitsStruct(endpoint=endpoint, cluster=cluster, struct=self.HoldTimeLimits)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PIROccupiedToUnoccupiedDelay):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PIROccupiedToUnoccupiedDelay)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'PIROccupiedToUnoccupiedDelay')

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PIRUnoccupiedToOccupiedDelay):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PIRUnoccupiedToOccupiedDelay)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'PIRUnoccupiedToOccupiedDelay')

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PIRUnoccupiedToOccupiedThreshold):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PIRUnoccupiedToOccupiedThreshold)
            if val is not None:
                matter_asserts.assert_valid_uint8(val, 'PIRUnoccupiedToOccupiedThreshold')
                asserts.assert_greater_equal(val, 1)
                asserts.assert_less_equal(val, 254)

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.UltrasonicOccupiedToUnoccupiedDelay):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UltrasonicOccupiedToUnoccupiedDelay)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'UltrasonicOccupiedToUnoccupiedDelay')

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.UltrasonicUnoccupiedToOccupiedDelay):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UltrasonicUnoccupiedToOccupiedDelay)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'UltrasonicUnoccupiedToOccupiedDelay')

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.UltrasonicUnoccupiedToOccupiedThreshold):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UltrasonicUnoccupiedToOccupiedThreshold)
            if val is not None:
                matter_asserts.assert_valid_uint8(val, 'UltrasonicUnoccupiedToOccupiedThreshold')
                asserts.assert_greater_equal(val, 1)
                asserts.assert_less_equal(val, 254)

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PhysicalContactOccupiedToUnoccupiedDelay):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PhysicalContactOccupiedToUnoccupiedDelay)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'PhysicalContactOccupiedToUnoccupiedDelay')

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PhysicalContactUnoccupiedToOccupiedDelay):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PhysicalContactUnoccupiedToOccupiedDelay)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'PhysicalContactUnoccupiedToOccupiedDelay')

        self.step("14")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PhysicalContactUnoccupiedToOccupiedThreshold):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PhysicalContactUnoccupiedToOccupiedThreshold)
            if val is not None:
                matter_asserts.assert_valid_uint8(val, 'PhysicalContactUnoccupiedToOccupiedThreshold')
                asserts.assert_greater_equal(val, 1)
                asserts.assert_less_equal(val, 254)


    async def test_checkHoldTimeLimitsStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.OccupancySensing = None, 
                                 struct: Clusters.OccupancySensing.Structs.HoldTimeLimitsStruct = None):
        matter_asserts.assert_valid_uint16(struct.holdTimeMin, 'HoldTimeMin')
        asserts.assert_greater_equal(struct.holdTimeMin, 1)
        matter_asserts.assert_valid_uint16(struct.holdTimeMax, 'HoldTimeMax')
        asserts.assert_greater_equal(struct.holdTimeMax, struct.HoldTimeMin)
        asserts.assert_greater_equal(struct.holdTimeMax, 10)
        matter_asserts.assert_valid_uint16(struct.holdTimeDefault, 'HoldTimeDefault')
        asserts.assert_greater_equal(struct.holdTimeDefault, struct.HoldTimeMin)
        asserts.assert_less_equal(struct.holdTimeDefault, struct.HoldTimeMax)


if __name__ == "__main__":
    default_matter_test_main()
