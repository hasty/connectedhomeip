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

cluster = Clusters.EnergyPreference

class EPREF_2_1(MatterBaseTest):

    def desc_EPREF_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_EPREF_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["EPREF"]

    def steps_EPREF_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read EnergyBalances attribute"),
            TestStep("2", "Read CurrentEnergyBalance attribute"),
            TestStep("3", "Read EnergyPriorities attribute"),
            TestStep("4", "Read LowPowerModeSensitivities attribute"),
            TestStep("5", "Read CurrentLowPowerModeSensitivity attribute"),
        ]

        return steps


    @async_test_body
    async def test_EPREF_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.EnergyBalances):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EnergyBalances)
            matter_asserts.assert_list(val, "EnergyBalances attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "EnergyBalances attribute must contain BalanceStruct elements", cluster.Structs.BalanceStruct)
            for item in val:
                await self.test_checkBalanceStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_greater_equal(len(val), 2, "EnergyBalances must have at least 2 entries!")
            asserts.assert_less_equal(len(val), 10, "EnergyBalances must have at most 10 entries!")

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentEnergyBalance):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentEnergyBalance)
            matter_asserts.assert_valid_uint8(val, 'CurrentEnergyBalance')

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.EnergyPriorities):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EnergyPriorities)
            matter_asserts.assert_list(val, "EnergyPriorities attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "EnergyPriorities attribute must contain EnergyPriorityEnum elements", cluster.Enums.EnergyPriorityEnum)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.LowPowerModeSensitivities):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LowPowerModeSensitivities)
            matter_asserts.assert_list(val, "LowPowerModeSensitivities attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "LowPowerModeSensitivities attribute must contain BalanceStruct elements", cluster.Structs.BalanceStruct)
            for item in val:
                await self.test_checkBalanceStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_greater_equal(len(val), 2, "LowPowerModeSensitivities must have at least 2 entries!")
            asserts.assert_less_equal(len(val), 10, "LowPowerModeSensitivities must have at most 10 entries!")

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentLowPowerModeSensitivity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentLowPowerModeSensitivity)
            matter_asserts.assert_valid_uint8(val, 'CurrentLowPowerModeSensitivity')


    async def test_checkBalanceStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.EnergyPreference = None, 
                                 struct: Clusters.EnergyPreference.Structs.BalanceStruct = None):
        matter_asserts.assert_valid_uint8(struct.step, 'Step')
        if struct.label is not None:
            matter_asserts.assert_is_string(struct.label, "Label must be a string")
            asserts.assert_less_equal(len(struct.label), 64, "Label must have length at most 64!")


if __name__ == "__main__":
    default_matter_test_main()
