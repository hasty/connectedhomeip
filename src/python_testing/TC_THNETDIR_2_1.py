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

cluster = Clusters.ThreadNetworkDirectory

class THNETDIR_2_1(MatterBaseTest):

    def desc_THNETDIR_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_THNETDIR_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["THNETDIR"]

    def steps_THNETDIR_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read PreferredExtendedPanID attribute"),
            TestStep("2", "Read ThreadNetworks attribute"),
            TestStep("3", "Read ThreadNetworkTableSize attribute"),
        ]

        return steps

    ThreadNetworkTableSize = None

    @async_test_body
    async def test_THNETDIR_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PreferredExtendedPanID)
        if val is not NullValue:
            matter_asserts.assert_is_octstr(val, "PreferredExtendedPanID must be an octstr")

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ThreadNetworks)
        matter_asserts.assert_list(val, "ThreadNetworks attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "ThreadNetworks attribute must contain Clusters.ThreadNetworkDirectory.Structs.ThreadNetworkStruct elements", Clusters.ThreadNetworkDirectory.Structs.ThreadNetworkStruct)
        for item in val:
            await self.test_checkThreadNetworkStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(val), self.ThreadNetworkTableSize, "ThreadNetworks must have at most self.ThreadNetworkTableSize entries!")

        self.step("3")
        self.ThreadNetworkTableSize = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ThreadNetworkTableSize)
        matter_asserts.assert_valid_uint8(self.ThreadNetworkTableSize, 'ThreadNetworkTableSize')


    async def test_checkThreadNetworkStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ThreadNetworkDirectory = None, 
                                 struct: Clusters.ThreadNetworkDirectory.Structs.ThreadNetworkStruct = None):
        matter_asserts.assert_is_octstr(struct.extendedPanID, "ExtendedPanID must be an octstr")
        matter_asserts.assert_is_string(struct.networkName, "NetworkName must be a string")
        asserts.assert_greater_equal(len(struct.networkName), 1, "NetworkName must be at least 1 long!")
        asserts.assert_less_equal(len(struct.networkName), 16, "NetworkName must have length at most 16!")
        matter_asserts.assert_valid_uint16(struct.channel, 'Channel')
        matter_asserts.assert_valid_uint64(struct.activeTimestamp, 'ActiveTimestamp')


if __name__ == "__main__":
    default_matter_test_main()
