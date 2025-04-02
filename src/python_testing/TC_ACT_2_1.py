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

cluster = Clusters.Actions

class ACT_2_1(MatterBaseTest):

    def desc_ACT_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_ACT_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["ACT.S"]

    def steps_ACT_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read ActionList attribute"),
            TestStep("2", "Read EndpointLists attribute"),
            TestStep("3", "Read SetupURL attribute"),
        ]
        return steps

    @run_if_endpoint_matches(has_cluster(Clusters.Actions))
    async def test_ACT_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActionList)
        matter_asserts.assert_list(val, "ActionList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "ActionList attribute must contain ActionStruct elements", cluster.Structs.ActionStruct)
        for item in val:
            await self.test_checkActionStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(val), 256, "ActionList must have at most 256 entries!")

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EndpointLists)
        matter_asserts.assert_list(val, "EndpointLists attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "EndpointLists attribute must contain EndpointListStruct elements", cluster.Structs.EndpointListStruct)
        for item in val:
            await self.test_checkEndpointListStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(val), 256, "EndpointLists must have at most 256 entries!")

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SetupURL):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SetupURL)
            if val is not None:
                matter_asserts.assert_is_string(val, "SetupURL must be a string")
                asserts.assert_less_equal(len(val), 512, "SetupURL must have length at most 512!")

    async def test_checkActionStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Actions = None, 
                                 struct: Clusters.Actions.Structs.ActionStruct = None):
        matter_asserts.assert_valid_uint16(struct.actionID, 'ActionID')
        matter_asserts.assert_is_string(struct.name, "Name must be a string")
        asserts.assert_less_equal(len(struct.name), 128, "Name must have length at most 128!")
        matter_asserts.assert_valid_enum(struct.type, "Type attribute must return a ActionTypeEnum", cluster.Enums.ActionTypeEnum)
        matter_asserts.assert_valid_uint16(struct.endpointListID, 'EndpointListID')
        matter_asserts.is_valid_int_value(struct.supportedCommands)
        asserts.assert_greater_equal(struct.supportedCommands, 0)
        asserts.assert_less_equal(struct.supportedCommands, 4095)
        # Check bitmap value less than or equal to (InstantAction | InstantActionWithTransition | StartAction | StartActionWithDuration | StopAction | PauseAction | PauseActionWithDuration | ResumeAction | EnableAction | EnableActionWithDuration | DisableAction | DisableActionWithDuration)
        asserts.assert_less_equal(struct.supportedCommands, 4095)
        matter_asserts.assert_valid_enum(struct.state, "State attribute must return a ActionStateEnum", cluster.Enums.ActionStateEnum)

    async def test_checkEndpointListStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Actions = None, 
                                 struct: Clusters.Actions.Structs.EndpointListStruct = None):
        matter_asserts.assert_valid_uint16(struct.endpointListID, 'EndpointListID')
        matter_asserts.assert_is_string(struct.name, "Name must be a string")
        asserts.assert_less_equal(len(struct.name), 128, "Name must have length at most 128!")
        matter_asserts.assert_valid_enum(struct.type, "Type attribute must return a EndpointListTypeEnum", cluster.Enums.EndpointListTypeEnum)
        matter_asserts.assert_list(struct.endpoints, "Endpoints attribute must return a list")
        matter_asserts.assert_list_element_type(struct.endpoints,  "Endpoints attribute must contain int elements", int)
        asserts.assert_less_equal(len(struct.endpoints), 256, "Endpoints must have at most 256 entries!")

if __name__ == "__main__":
    default_matter_test_main()
