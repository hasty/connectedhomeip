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

cluster = Clusters.ClosureControl

class CLCTRL_2_1(MatterBaseTest):

    def desc_CLCTRL_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_CLCTRL_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["CLCTRL"]

    def steps_CLCTRL_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read CountdownTime attribute"),
            TestStep("2", "Read MainState attribute"),
            TestStep("3", "Read CurrentErrorList attribute"),
            TestStep("4", "Read OverallState attribute"),
            TestStep("5", "Read OverallTarget attribute"),
        ]

        return steps


    @async_test_body
    async def test_CLCTRL_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CountdownTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CountdownTime)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'CountdownTime')
                asserts.assert_less_equal(val, 259200)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MainState)
        matter_asserts.assert_valid_enum(val, "MainState attribute must return a Clusters.ClosureControl.Enums.MainStateEnum", Clusters.ClosureControl.Enums.MainStateEnum)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentErrorList)
        matter_asserts.assert_list(val, "CurrentErrorList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "CurrentErrorList attribute must contain Clusters.ClosureControl.Enums.ClosureErrorEnum elements", Clusters.ClosureControl.Enums.ClosureErrorEnum)

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OverallState)
        if val is not NullValue:
            asserts.assert_true(isinstance(val, Clusters.ClosureControl.Structs.OverallStateStruct),
                                        f"val must be of type Clusters.ClosureControl.Structs.OverallStateStruct")
            await self.test_checkOverallStateStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OverallTarget)
        if val is not NullValue:
            asserts.assert_true(isinstance(val, Clusters.ClosureControl.Structs.OverallTargetStruct),
                                        f"val must be of type Clusters.ClosureControl.Structs.OverallTargetStruct")
            await self.test_checkOverallTargetStruct(endpoint=endpoint, cluster=cluster, struct=val)


    async def test_checkOverallStateStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ClosureControl = None, 
                                 struct: Clusters.ClosureControl.Structs.OverallStateStruct = None):
        if struct.positioning is not NullValue:
            matter_asserts.assert_valid_enum(struct.positioning, "Positioning attribute must return a Clusters.ClosureControl.Enums.PositioningEnum", Clusters.ClosureControl.Enums.PositioningEnum)
        if struct.latching is not NullValue:
            matter_asserts.assert_valid_enum(struct.latching, "Latching attribute must return a Clusters.ClosureControl.Enums.LatchingEnum", Clusters.ClosureControl.Enums.LatchingEnum)
        if struct.speed is not NullValue:
            matter_asserts.assert_valid_enum(struct.speed, "Speed attribute must return a Globals.Enums.ThreeLevelAutoEnum", Globals.Enums.ThreeLevelAutoEnum)

    async def test_checkOverallTargetStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ClosureControl = None, 
                                 struct: Clusters.ClosureControl.Structs.OverallTargetStruct = None):
        matter_asserts.assert_valid_enum(struct.position, "Position attribute must return a Clusters.ClosureControl.Enums.TargetPositionEnum", Clusters.ClosureControl.Enums.TargetPositionEnum)
        matter_asserts.assert_valid_enum(struct.latch, "Latch attribute must return a Clusters.ClosureControl.Enums.TargetLatchEnum", Clusters.ClosureControl.Enums.TargetLatchEnum)
        matter_asserts.assert_valid_enum(struct.speed, "Speed attribute must return a Globals.Enums.ThreeLevelAutoEnum", Globals.Enums.ThreeLevelAutoEnum)


if __name__ == "__main__":
    default_matter_test_main()
