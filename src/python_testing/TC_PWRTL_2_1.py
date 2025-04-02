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

cluster = Clusters.PowerTopology

class PWRTL_2_1(MatterBaseTest):

    def desc_PWRTL_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_PWRTL_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["PWRTL.S"]

    def steps_PWRTL_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read AvailableEndpoints attribute"),
            TestStep("2", "Read ActiveEndpoints attribute"),
        ]
        return steps


    @run_if_endpoint_matches(has_cluster(Clusters.PowerTopology))
    async def test_PWRTL_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AvailableEndpoints):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AvailableEndpoints)
            matter_asserts.assert_list(val, "AvailableEndpoints attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "AvailableEndpoints attribute must contain int elements", int)
            asserts.assert_less_equal(len(val), 20, "AvailableEndpoints must have at most 20 entries!")

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveEndpoints):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveEndpoints)
            matter_asserts.assert_list(val, "ActiveEndpoints attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "ActiveEndpoints attribute must contain int elements", int)
            asserts.assert_less_equal(len(val), 20, "ActiveEndpoints must have at most 20 entries!")

if __name__ == "__main__":
    default_matter_test_main()
