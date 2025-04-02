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

cluster = Clusters.HEPAFilterMonitoring

class HEPAFREMON_2_1(MatterBaseTest):

    def desc_HEPAFREMON_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_HEPAFREMON_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["HEPAFREMON.S"]

    def steps_HEPAFREMON_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read Condition attribute"),
            TestStep("2", "Read DegradationDirection attribute"),
            TestStep("3", "Read ChangeIndication attribute"),
            TestStep("4", "Read InPlaceIndicator attribute"),
            TestStep("5", "Read LastChangedTime attribute"),
            TestStep("6", "Read ReplacementProductList attribute"),
        ]
        return steps


    @async_test_body
    async def test_HEPAFREMON_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Condition):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Condition)
            matter_asserts.assert_valid_uint8(val, 'Condition')

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DegradationDirection):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DegradationDirection)
            matter_asserts.assert_valid_enum(val, "DegradationDirection attribute must return a DegradationDirectionEnum", cluster.Enums.DegradationDirectionEnum)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ChangeIndication)
        matter_asserts.assert_valid_enum(val, "ChangeIndication attribute must return a ChangeIndicationEnum", cluster.Enums.ChangeIndicationEnum)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.InPlaceIndicator):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.InPlaceIndicator)
            if val is not None:
                matter_asserts.assert_valid_bool(val, 'InPlaceIndicator')

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.LastChangedTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LastChangedTime)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'LastChangedTime')

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ReplacementProductList):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ReplacementProductList)
            matter_asserts.assert_list(val, "ReplacementProductList attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "ReplacementProductList attribute must contain ReplacementProductStruct elements", cluster.Structs.ReplacementProductStruct)
            for item in val:
                await self.test_checkReplacementProductStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_less_equal(len(val), 5, "ReplacementProductList must have at most 5 entries!")

    async def test_checkReplacementProductStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.HEPAFilterMonitoring = None, 
                                 struct: Clusters.HEPAFilterMonitoring.Structs.ReplacementProductStruct = None):
        matter_asserts.assert_valid_enum(struct.productIdentifierType, "ProductIdentifierType attribute must return a ProductIdentifierTypeEnum", cluster.Enums.ProductIdentifierTypeEnum)
        matter_asserts.assert_is_string(struct.productIdentifierValue, "ProductIdentifierValue must be a string")
        asserts.assert_less_equal(len(struct.productIdentifierValue), 20, "ProductIdentifierValue must have length at most 20!")

if __name__ == "__main__":
    default_matter_test_main()
