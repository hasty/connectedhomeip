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

cluster = Clusters.MicrowaveOvenControl

class MWOCTRL_2_1(MatterBaseTest):

    def desc_MWOCTRL_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_MWOCTRL_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["MWOCTRL.S"]

    def steps_MWOCTRL_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read CookTime attribute"),
            TestStep("2", "Read MaxCookTime attribute"),
            TestStep("3", "Read PowerSetting attribute"),
            TestStep("4", "Read MinPower attribute"),
            TestStep("5", "Read MaxPower attribute"),
            TestStep("6", "Read PowerStep attribute"),
            TestStep("7", "Read SupportedWatts attribute"),
            TestStep("8", "Read SelectedWattIndex attribute"),
            TestStep("9", "Read WattRating attribute"),
        ]
        return steps

    MaxCookTime = None
    MinPower = None

    @run_if_endpoint_matches(has_cluster(Clusters.MicrowaveOvenControl))
    async def test_MWOCTRL_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CookTime)
        matter_asserts.assert_valid_uint32(val, 'CookTime')
        asserts.assert_greater_equal(val, 1)
        asserts.assert_less_equal(val, self.MaxCookTime)

        self.step("2")
        self.MaxCookTime = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxCookTime)
        matter_asserts.assert_valid_uint32(self.MaxCookTime, 'MaxCookTime')
        asserts.assert_greater_equal(self.MaxCookTime, 1)
        asserts.assert_less_equal(self.MaxCookTime, 86400)

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PowerSetting):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PowerSetting)
            matter_asserts.assert_valid_uint8(val, 'PowerSetting')

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinPower):
            self.MinPower = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinPower)
            matter_asserts.assert_valid_uint8(self.MinPower, 'MinPower')
            asserts.assert_greater_equal(self.MinPower, 1)
            asserts.assert_less_equal(self.MinPower, 99)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxPower):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxPower)
            matter_asserts.assert_valid_uint8(val, 'MaxPower')
            asserts.assert_greater_equal(val, self.MinPower + 1)
            asserts.assert_less_equal(val, 100)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PowerStep):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PowerStep)
            matter_asserts.assert_valid_uint8(val, 'PowerStep')

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SupportedWatts):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportedWatts)
            matter_asserts.assert_list(val, "SupportedWatts attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "SupportedWatts attribute must contain int elements", int)
            asserts.assert_greater_equal(len(val), 1, "SupportedWatts must have at least 1 entries!")
            asserts.assert_less_equal(len(val), 10, "SupportedWatts must have at most 10 entries!")

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SelectedWattIndex):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SelectedWattIndex)
            matter_asserts.assert_valid_uint8(val, 'SelectedWattIndex')

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WattRating):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WattRating)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'WattRating')

if __name__ == "__main__":
    default_matter_test_main()
