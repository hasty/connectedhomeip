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

cluster = Clusters.Messages

class MESS_2_1(MatterBaseTest):

    def desc_MESS_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_MESS_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["MESS.S"]

    def steps_MESS_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read Messages attribute"),
            TestStep("2", "Read ActiveMessageIDs attribute"),
        ]
        return steps


    @run_if_endpoint_matches(has_cluster(Clusters.Messages))
    async def test_MESS_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Messages)
        matter_asserts.assert_list(val, "Messages attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "Messages attribute must contain MessageStruct elements", cluster.Structs.MessageStruct)
        for item in val:
            await self.test_checkMessageStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(val), 8, "Messages must have at most 8 entries!")

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveMessageIDs)
        matter_asserts.assert_list(val, "ActiveMessageIDs attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "ActiveMessageIDs attribute must contain bytes elements", bytes)
        asserts.assert_less_equal(len(val), 8, "ActiveMessageIDs must have at most 8 entries!")

    async def test_checkMessageResponseOptionStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Messages = None, 
                                 struct: Clusters.Messages.Structs.MessageResponseOptionStruct = None):
        matter_asserts.assert_valid_uint32(struct.messageResponseID, 'MessageResponseID')
        asserts.assert_greater_equal(struct.messageResponseID, 1)
        matter_asserts.assert_is_string(struct.label, "Label must be a string")
        asserts.assert_less_equal(len(struct.label), 32, "Label must have length at most 32!")

    async def test_checkMessageStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Messages = None, 
                                 struct: Clusters.Messages.Structs.MessageStruct = None):
        asserts.assert_true(isinstance(struct.messageID, bytes), "MessageID must be of type bytes")
        asserts.assert_equal(len(struct.messageID), 16, "MessageID must have a length of 16")
        matter_asserts.assert_valid_enum(struct.priority, "Priority attribute must return a MessagePriorityEnum", cluster.Enums.MessagePriorityEnum)
        matter_asserts.is_valid_int_value(struct.messageControl)
        if struct.startTime is not NullValue:
            matter_asserts.assert_valid_uint32(struct.startTime, 'StartTime')
        if struct.duration is not NullValue:
            matter_asserts.assert_valid_uint64(struct.duration, 'Duration')
        matter_asserts.assert_is_string(struct.messageText, "MessageText must be a string")
        asserts.assert_less_equal(len(struct.messageText), 256, "MessageText must have length at most 256!")
        matter_asserts.assert_list(struct.responses, "Responses attribute must return a list")
        matter_asserts.assert_list_element_type(struct.responses,  "Responses attribute must contain MessageResponseOptionStruct elements", cluster.Structs.MessageResponseOptionStruct)
        for item in struct.responses:
            await self.test_checkMessageResponseOptionStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(struct.responses), 4, "Responses must have at most 4 entries!")

if __name__ == "__main__":
    default_matter_test_main()
