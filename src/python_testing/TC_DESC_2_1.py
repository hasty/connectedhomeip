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

cluster = Clusters.Descriptor

class DESC_2_1(MatterBaseTest):

    def desc_DESC_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_DESC_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["DESC"]

    def steps_DESC_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read DeviceTypeList attribute"),
            TestStep("2", "Read ServerList attribute"),
            TestStep("3", "Read ClientList attribute"),
            TestStep("4", "Read PartsList attribute"),
            TestStep("5", "Read TagList attribute"),
        ]

        return steps


    @async_test_body
    async def test_DESC_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DeviceTypeList)
        matter_asserts.assert_list(val, "DeviceTypeList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "DeviceTypeList attribute must contain Clusters.Descriptor.Structs.DeviceTypeStruct elements", Clusters.Descriptor.Structs.DeviceTypeStruct)
        for item in val:
            await self.test_checkDeviceTypeStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_greater_equal(len(val), 1, "DeviceTypeList must have at least 1 entries!")

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ServerList)
        matter_asserts.assert_list(val, "ServerList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "ServerList attribute must contain int elements", int)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ClientList)
        matter_asserts.assert_list(val, "ClientList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "ClientList attribute must contain int elements", int)

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PartsList)
        matter_asserts.assert_list(val, "PartsList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "PartsList attribute must contain int elements", int)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TagList):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TagList)
            matter_asserts.assert_list(val, "TagList attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "TagList attribute must contain Clusters.Descriptor.Structs.SemanticTagStruct elements", Clusters.Descriptor.Structs.SemanticTagStruct)
            for item in val:
                await self.test_checkSemanticTagStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_greater_equal(len(val), 1, "TagList must have at least 1 entries!")
            asserts.assert_less_equal(len(val), 6, "TagList must have at most 6 entries!")


    async def test_checkDeviceTypeStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Descriptor = None, 
                                 struct: Clusters.Descriptor.Structs.DeviceTypeStruct = None):
        matter_asserts.assert_valid_uint32(struct.deviceType, 'DeviceType must be uint32')
        matter_asserts.assert_valid_uint16(struct.revision, 'Revision')
        asserts.assert_greater_equal(struct.revision, 1)

    async def test_checkSemanticTagStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Descriptor = None, 
                                 struct: Clusters.Descriptor.Structs.SemanticTagStruct = None):
        if struct.mfgCode is not NullValue:
            matter_asserts.assert_valid_uint16(struct.mfgCode, 'MfgCode must be uint16')
        matter_asserts.assert_valid_uint8(struct.namespaceID, 'NamespaceID must be uint8')
        matter_asserts.assert_valid_uint8(struct.tag, 'Tag must be uint8')
        if struct.label is not NullValue and struct.label is not None:
            matter_asserts.assert_is_string(struct.label, "Label must be a string")
            asserts.assert_less_equal(len(struct.label), 64, "Label must have length at most 64!")


if __name__ == "__main__":
    default_matter_test_main()
