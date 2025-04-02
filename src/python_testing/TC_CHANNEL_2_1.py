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

cluster = Clusters.Channel

class CHANNEL_2_1(MatterBaseTest):

    def desc_CHANNEL_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_CHANNEL_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["CHANNEL"]

    def steps_CHANNEL_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read ChannelList attribute"),
            TestStep("2", "Read Lineup attribute"),
            TestStep("3", "Read CurrentChannel attribute"),
        ]
        return steps


    @async_test_body
    async def test_CHANNEL_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ChannelList):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ChannelList)
            matter_asserts.assert_list(val, "ChannelList attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "ChannelList attribute must contain ChannelInfoStruct elements", cluster.Structs.ChannelInfoStruct)
            for item in val:
                await self.test_checkChannelInfoStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Lineup):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Lineup)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, cluster.Structs.LineupInfoStruct), f"val must be of type LineupInfoStruct")
                await self.test_checkLineupInfoStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentChannel):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentChannel)
            if val is not NullValue and val is not None:
                asserts.assert_true(isinstance(val, cluster.Structs.ChannelInfoStruct), f"val must be of type ChannelInfoStruct")
                await self.test_checkChannelInfoStruct(endpoint=endpoint, cluster=cluster, struct=val)

    async def test_checkChannelInfoStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Channel = None, 
                                 struct: Clusters.Channel.Structs.ChannelInfoStruct = None):
        matter_asserts.assert_valid_uint16(struct.majorNumber, 'MajorNumber')
        matter_asserts.assert_valid_uint16(struct.minorNumber, 'MinorNumber')
        if struct.name is not None:
            matter_asserts.assert_is_string(struct.name, "Name must be a string")
        if struct.callSign is not None:
            matter_asserts.assert_is_string(struct.callSign, "CallSign must be a string")
        if struct.affiliateCallSign is not None:
            matter_asserts.assert_is_string(struct.affiliateCallSign, "AffiliateCallSign must be a string")
        if struct.identifier is not None:
            matter_asserts.assert_is_string(struct.identifier, "Identifier must be a string")
        if struct.type is not None:
            matter_asserts.assert_valid_enum(struct.type, "Type attribute must return a ChannelTypeEnum", cluster.Enums.ChannelTypeEnum)

    async def test_checkLineupInfoStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.Channel = None, 
                                 struct: Clusters.Channel.Structs.LineupInfoStruct = None):
        matter_asserts.assert_is_string(struct.operatorName, "OperatorName must be a string")
        if struct.lineupName is not None:
            matter_asserts.assert_is_string(struct.lineupName, "LineupName must be a string")
        if struct.postalCode is not None:
            matter_asserts.assert_is_string(struct.postalCode, "PostalCode must be a string")
        matter_asserts.assert_valid_enum(struct.lineupInfoType, "LineupInfoType attribute must return a LineupInfoTypeEnum", cluster.Enums.LineupInfoTypeEnum)

if __name__ == "__main__":
    default_matter_test_main()
