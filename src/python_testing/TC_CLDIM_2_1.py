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

cluster = Clusters.ClosureDimension

class CLDIM_2_1(MatterBaseTest):

    def desc_CLDIM_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_CLDIM_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["CLDIM"]

    def steps_CLDIM_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read Current attribute"),
            TestStep("2", "Read Target attribute"),
            TestStep("3", "Read Resolution attribute"),
            TestStep("4", "Read StepValue attribute"),
            TestStep("5", "Read Unit attribute"),
            TestStep("6", "Read UnitRange attribute"),
            TestStep("7", "Read LimitRange attribute"),
            TestStep("8", "Read TranslationDirection attribute"),
            TestStep("9", "Read RotationAxis attribute"),
            TestStep("10", "Read Overflow attribute"),
            TestStep("11", "Read ModulationType attribute"),
        ]

        return steps

    Min = None
    Min = None

    @async_test_body
    async def test_CLDIM_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Current)
        if val is not NullValue:
            asserts.assert_true(isinstance(val, Clusters.ClosureDimension.Structs.CurrentStruct),
                                        f"val must be of type Clusters.ClosureDimension.Structs.CurrentStruct")
            await self.test_checkCurrentStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Target)
        if val is not NullValue:
            asserts.assert_true(isinstance(val, Clusters.ClosureDimension.Structs.TargetStruct),
                                        f"val must be of type Clusters.ClosureDimension.Structs.TargetStruct")
            await self.test_checkTargetStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("3")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kPositioning):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Resolution)
            matter_asserts.assert_valid_uint16(val, 'Resolution')
            asserts.assert_greater_equal(val, 0.01)

        self.step("4")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kPositioning):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.StepValue)
            matter_asserts.assert_valid_uint16(val, 'StepValue')

        self.step("5")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kUnit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Unit)
            matter_asserts.assert_valid_enum(val, "Unit attribute must return a Clusters.ClosureDimension.Enums.ClosureUnitEnum", Clusters.ClosureDimension.Enums.ClosureUnitEnum)

        self.step("6")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kUnit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UnitRange)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, Clusters.ClosureDimension.Structs.UnitRangeStruct),
                                            f"val must be of type Clusters.ClosureDimension.Structs.UnitRangeStruct")
                await self.test_checkUnitRangeStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("7")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kLimitation):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LimitRange)
            asserts.assert_true(isinstance(val, Clusters.ClosureDimension.Structs.RangePercent100thsStruct),
                                        f"val must be of type Clusters.ClosureDimension.Structs.RangePercent100thsStruct")
            await self.test_checkRangePercent100thsStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("8")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kTranslation):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TranslationDirection)
            matter_asserts.assert_valid_enum(val, "TranslationDirection attribute must return a Clusters.ClosureDimension.Enums.TranslationDirectionEnum", Clusters.ClosureDimension.Enums.TranslationDirectionEnum)

        self.step("9")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kRotation):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RotationAxis)
            matter_asserts.assert_valid_enum(val, "RotationAxis attribute must return a Clusters.ClosureDimension.Enums.RotationAxisEnum", Clusters.ClosureDimension.Enums.RotationAxisEnum)

        self.step("10")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kRotation) and await self.attribute_guard(endpoint=endpoint, attribute=attributes.Overflow) and await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kMotionLatching):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Overflow)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "Overflow attribute must return a Clusters.ClosureDimension.Enums.OverflowEnum", Clusters.ClosureDimension.Enums.OverflowEnum)

        self.step("11")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kModulation):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ModulationType)
            matter_asserts.assert_valid_enum(val, "ModulationType attribute must return a Clusters.ClosureDimension.Enums.ModulationTypeEnum", Clusters.ClosureDimension.Enums.ModulationTypeEnum)


    async def test_checkCurrentStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ClosureDimension = None, 
                                 struct: Clusters.ClosureDimension.Structs.CurrentStruct = None):
        matter_asserts.assert_valid_uint16(struct.position, 'Position')
        matter_asserts.assert_valid_enum(struct.latching, "Latching attribute must return a Clusters.ClosureDimension.Enums.LatchingEnum", Clusters.ClosureDimension.Enums.LatchingEnum)
        matter_asserts.assert_valid_enum(struct.speed, "Speed attribute must return a Globals.Enums.ThreeLevelAutoEnum", Globals.Enums.ThreeLevelAutoEnum)

    async def test_checkRangePercent100thsStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ClosureDimension = None, 
                                 struct: Clusters.ClosureDimension.Structs.RangePercent100thsStruct = None):
        matter_asserts.assert_valid_uint16(struct.min, 'Min')
        matter_asserts.assert_valid_uint16(struct.max, 'Max')
        asserts.assert_greater_equal(struct.max, self.Min)
        asserts.assert_less_equal(struct.max, 100)

    async def test_checkTargetStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ClosureDimension = None, 
                                 struct: Clusters.ClosureDimension.Structs.TargetStruct = None):
        matter_asserts.assert_valid_uint16(struct.position, 'Position')
        matter_asserts.assert_valid_enum(struct.latch, "Latch attribute must return a Clusters.ClosureDimension.Enums.TargetLatchEnum", Clusters.ClosureDimension.Enums.TargetLatchEnum)
        matter_asserts.assert_valid_enum(struct.speed, "Speed attribute must return a Globals.Enums.ThreeLevelAutoEnum", Globals.Enums.ThreeLevelAutoEnum)

    async def test_checkUnitRangeStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ClosureDimension = None, 
                                 struct: Clusters.ClosureDimension.Structs.UnitRangeStruct = None):
        matter_asserts.assert_valid_int16(struct.min, 'Min')
        matter_asserts.assert_valid_int16(struct.max, 'Max')
        asserts.assert_greater_equal(struct.max, self.Min)
        asserts.assert_less_equal(struct.max, 32767)


if __name__ == "__main__":
    default_matter_test_main()
