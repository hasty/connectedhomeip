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

cluster = Clusters.ApplicationBasic

class APBSC_2_1(MatterBaseTest):

    def desc_APBSC_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_APBSC_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["APBSC.S"]

    def steps_APBSC_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read VendorName attribute"),
            TestStep("2", "Read VendorID attribute"),
            TestStep("3", "Read ApplicationName attribute"),
            TestStep("4", "Read ProductID attribute"),
            TestStep("5", "Read Application attribute"),
            TestStep("6", "Read Status attribute"),
            TestStep("7", "Read ApplicationVersion attribute"),
            TestStep("8", "Read AllowedVendorList attribute"),
        ]
        return steps


    @run_if_endpoint_matches(has_cluster(Clusters.ApplicationBasic))
    async def test_APBSC_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.VendorName):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.VendorName)
            if val is not None:
                matter_asserts.assert_is_string(val, "VendorName must be a string")
                asserts.assert_less_equal(len(val), 32, "VendorName must have length at most 32!")

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.VendorID):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.VendorID)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'VendorID must be uint16')

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ApplicationName)
        matter_asserts.assert_is_string(val, "ApplicationName must be a string")

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ProductID):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ProductID)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ProductID')

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Application)
        asserts.assert_true(isinstance(val, cluster.Structs.ApplicationStruct), f"val must be of type ApplicationStruct")
        await self.test_checkApplicationStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("6")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Status)
        matter_asserts.assert_valid_enum(val, "Status attribute must return a ApplicationStatusEnum", cluster.Enums.ApplicationStatusEnum)

        self.step("7")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ApplicationVersion)
        matter_asserts.assert_is_string(val, "ApplicationVersion must be a string")
        asserts.assert_less_equal(len(val), 32, "ApplicationVersion must have length at most 32!")

        self.step("8")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AllowedVendorList)
        matter_asserts.assert_list(val, "AllowedVendorList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "AllowedVendorList attribute must contain int elements", int)

    async def test_checkApplicationStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ApplicationBasic = None, 
                                 struct: Clusters.ApplicationBasic.Structs.ApplicationStruct = None):
        matter_asserts.assert_valid_uint16(struct.catalogVendorID, 'CatalogVendorID')
        matter_asserts.assert_is_string(struct.applicationID, "ApplicationID must be a string")

if __name__ == "__main__":
    default_matter_test_main()
