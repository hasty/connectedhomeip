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

cluster = Clusters.ApplicationLauncher

class APPLAUNCHER_2_1(MatterBaseTest):

    def desc_APPLAUNCHER_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_APPLAUNCHER_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["APPLAUNCHER.S"]

    def steps_APPLAUNCHER_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read CatalogList attribute"),
            TestStep("2", "Read CurrentApp attribute"),
        ]
        return steps

    @run_if_endpoint_matches(has_cluster(Clusters.ApplicationLauncher))
    async def test_APPLAUNCHER_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CatalogList):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CatalogList)
            matter_asserts.assert_list(val, "CatalogList attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "CatalogList attribute must contain int elements", int)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentApp):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentApp)
            if val is not NullValue and val is not None:
                asserts.assert_true(isinstance(val, cluster.Structs.ApplicationEPStruct), f"val must be of type ApplicationEPStruct")
                await self.test_checkApplicationEPStruct(endpoint=endpoint, cluster=cluster, struct=val)

    async def test_checkApplicationEPStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ApplicationLauncher = None, 
                                 struct: Clusters.ApplicationLauncher.Structs.ApplicationEPStruct = None):
        asserts.assert_true(isinstance(struct.application, cluster.Structs.ApplicationStruct), f"struct.application must be of type ApplicationStruct")
        await self.test_checkApplicationStruct(endpoint=endpoint, cluster=cluster, struct=struct.application)
        if struct.endpoint is not None:
            matter_asserts.assert_valid_uint16(struct.endpoint, 'Endpoint must be uint16')

    async def test_checkApplicationStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ApplicationLauncher = None, 
                                 struct: Clusters.ApplicationLauncher.Structs.ApplicationStruct = None):
        matter_asserts.assert_valid_uint16(struct.catalogVendorID, 'CatalogVendorID')
        matter_asserts.assert_is_string(struct.applicationID, "ApplicationID must be a string")

if __name__ == "__main__":
    default_matter_test_main()
