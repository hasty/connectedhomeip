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

cluster = Clusters.DeviceEnergyManagementMode

class DEMM_2_1(MatterBaseTest):

    def desc_DEMM_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_DEMM_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["DEMM.S"]

    def steps_DEMM_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read SupportedModes attribute"),
            TestStep("2", "Read CurrentMode attribute"),
        ]
        return steps


    @run_if_endpoint_matches(has_cluster(Clusters.DeviceEnergyManagementMode))
    async def test_DEMM_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportedModes)
        matter_asserts.assert_list(val, "SupportedModes attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "SupportedModes attribute must contain ModeOptionStruct elements", Clusters.ModeBase.Structs.ModeOptionStruct)
        for item in val:
            await self.test_checkModeOptionStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_greater_equal(len(val), 2, "SupportedModes must have at least 2 entries!")
        asserts.assert_less_equal(len(val), 255, "SupportedModes must have at most 255 entries!")

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentMode)
        matter_asserts.assert_valid_uint8(val, 'CurrentMode')

    async def test_checkModeOptionStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.DeviceEnergyManagementMode = None, 
                                 struct: Clusters.ModeBase.Structs.ModeOptionStruct = None):
        matter_asserts.assert_is_string(struct.label, "Label must be a string")
        asserts.assert_less_equal(len(struct.label), 64, "Label must have length at most 64!")
        matter_asserts.assert_valid_uint8(struct.mode, 'Mode')
        matter_asserts.assert_list(struct.modeTags, "ModeTags attribute must return a list")
        matter_asserts.assert_list_element_type(struct.modeTags,  "ModeTags attribute must contain ModeTagStruct elements", Clusters.ModeBase.Structs.ModeTagStruct)
        for item in struct.modeTags:
            await self.test_checkModeTagStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(struct.modeTags), 8, "ModeTags must have at most 8 entries!")

    async def test_checkModeTagStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.DeviceEnergyManagementMode = None, 
                                 struct: Clusters.ModeBase.Structs.ModeTagStruct = None):
        if struct.mfgCode is not None:
            matter_asserts.assert_valid_uint16(struct.mfgCode, 'MfgCode must be uint16')
        matter_asserts.assert_valid_uint16(struct.value, 'Value must be uint16')

if __name__ == "__main__":
    default_matter_test_main()
