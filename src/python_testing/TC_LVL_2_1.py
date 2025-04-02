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

cluster = Clusters.LevelControl

class LVL_2_1(MatterBaseTest):

    def desc_LVL_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_LVL_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["LVL.S"]

    def steps_LVL_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read CurrentLevel attribute"),
            TestStep("2", "Read RemainingTime attribute"),
            TestStep("3", "Read MinLevel attribute"),
            TestStep("4", "Read MinLevel attribute"),
            TestStep("5", "Read MaxLevel attribute"),
            TestStep("6", "Read CurrentFrequency attribute"),
            TestStep("7", "Read MinFrequency attribute"),
            TestStep("8", "Read MaxFrequency attribute"),
            TestStep("9", "Read OnOffTransitionTime attribute"),
            TestStep("10", "Read OnLevel attribute"),
            TestStep("11", "Read OnTransitionTime attribute"),
            TestStep("12", "Read OffTransitionTime attribute"),
            TestStep("13", "Read DefaultMoveRate attribute"),
            TestStep("14", "Read Options attribute"),
            TestStep("15", "Read StartUpCurrentLevel attribute"),
        ]
        return steps

    MaxFrequency = None
    MaxLevel = None
    MinFrequency = None
    MinLevel = None

    @run_if_endpoint_matches(has_cluster(Clusters.LevelControl))
    async def test_LVL_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentLevel)
        if val is not NullValue:
            matter_asserts.assert_valid_uint8(val, 'CurrentLevel')
            asserts.assert_greater_equal(val, self.MinLevel)
            asserts.assert_less_equal(val, self.MaxLevel)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RemainingTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RemainingTime)
            matter_asserts.assert_valid_uint16(val, 'RemainingTime')

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinLevel):
            self.MinLevel = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinLevel)
            if self.MinLevel is not None:
                matter_asserts.assert_valid_uint8(self.MinLevel, 'MinLevel')
                asserts.assert_greater_equal(self.MinLevel, 1)
                asserts.assert_less_equal(self.MinLevel, 254)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinLevel):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinLevel)
            if val is not None:
                matter_asserts.assert_valid_uint8(val, 'MinLevel')
                asserts.assert_less_equal(val, 254)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxLevel):
            self.MaxLevel = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxLevel)
            if self.MaxLevel is not None:
                matter_asserts.assert_valid_uint8(self.MaxLevel, 'MaxLevel')
                asserts.assert_greater_equal(self.MaxLevel, self.MinLevel)
                asserts.assert_less_equal(self.MaxLevel, 254)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentFrequency):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentFrequency)
            matter_asserts.assert_valid_uint16(val, 'CurrentFrequency')
            asserts.assert_greater_equal(val, self.MinFrequency)
            asserts.assert_less_equal(val, self.MaxFrequency)

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinFrequency):
            self.MinFrequency = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinFrequency)
            matter_asserts.assert_valid_uint16(self.MinFrequency, 'MinFrequency')

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxFrequency):
            self.MaxFrequency = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxFrequency)
            matter_asserts.assert_valid_uint16(self.MaxFrequency, 'MaxFrequency')
            asserts.assert_greater_equal(self.MaxFrequency, self.MinFrequency)

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OnOffTransitionTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OnOffTransitionTime)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'OnOffTransitionTime')

        self.step("10")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OnLevel)
        if val is not NullValue:
            matter_asserts.assert_valid_uint8(val, 'OnLevel')
            asserts.assert_greater_equal(val, self.MinLevel)
            asserts.assert_less_equal(val, self.MaxLevel)

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OnTransitionTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OnTransitionTime)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'OnTransitionTime')

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OffTransitionTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OffTransitionTime)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'OffTransitionTime')

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DefaultMoveRate):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DefaultMoveRate)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'DefaultMoveRate')
                asserts.assert_greater_equal(val, 1)

        self.step("14")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Options)
        matter_asserts.is_valid_int_value(val)

        self.step("15")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.StartUpCurrentLevel):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.StartUpCurrentLevel)
            if val is not NullValue:
                matter_asserts.assert_valid_uint8(val, 'StartUpCurrentLevel')

if __name__ == "__main__":
    default_matter_test_main()
