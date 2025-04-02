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

cluster = Clusters.GeneralCommissioning

class CGEN_2_1(MatterBaseTest):

    def desc_CGEN_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_CGEN_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["CGEN.S"]

    def steps_CGEN_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read Breadcrumb attribute"),
            TestStep("2", "Read BasicCommissioningInfo attribute"),
            TestStep("3", "Read RegulatoryConfig attribute"),
            TestStep("4", "Read LocationCapability attribute"),
            TestStep("5", "Read SupportsConcurrentConnection attribute"),
            TestStep("6", "Read TCAcceptedVersion attribute"),
            TestStep("7", "Read TCMinRequiredVersion attribute"),
            TestStep("8", "Read TCAcknowledgements attribute"),
            TestStep("9", "Read TCAcknowledgementsRequired attribute"),
            TestStep("10", "Read TCUpdateDeadline attribute"),
        ]
        return steps

    @run_if_endpoint_matches(has_cluster(Clusters.GeneralCommissioning))
    async def test_CGEN_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Breadcrumb)
        matter_asserts.assert_valid_uint64(val, 'Breadcrumb')

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BasicCommissioningInfo)
        asserts.assert_true(isinstance(val, cluster.Structs.BasicCommissioningInfo), f"val must be of type BasicCommissioningInfo")
        await self.test_checkBasicCommissioningInfo(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RegulatoryConfig)
        matter_asserts.assert_valid_enum(val, "RegulatoryConfig attribute must return a RegulatoryLocationTypeEnum", cluster.Enums.RegulatoryLocationTypeEnum)

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LocationCapability)
        matter_asserts.assert_valid_enum(val, "LocationCapability attribute must return a RegulatoryLocationTypeEnum", cluster.Enums.RegulatoryLocationTypeEnum)

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportsConcurrentConnection)
        matter_asserts.assert_valid_bool(val, 'SupportsConcurrentConnection')

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TCAcceptedVersion):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TCAcceptedVersion)
            matter_asserts.assert_valid_uint16(val, 'TCAcceptedVersion')

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TCMinRequiredVersion):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TCMinRequiredVersion)
            matter_asserts.assert_valid_uint16(val, 'TCMinRequiredVersion')

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TCAcknowledgements):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TCAcknowledgements)
            matter_asserts.assert_valid_uint16(val, 'TCAcknowledgements must be uint16')

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TCAcknowledgementsRequired):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TCAcknowledgementsRequired)
            matter_asserts.assert_valid_bool(val, 'TCAcknowledgementsRequired')

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TCUpdateDeadline):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TCUpdateDeadline)
            if val is not NullValue:
                matter_asserts.assert_valid_uint32(val, 'TCUpdateDeadline')

    async def test_checkBasicCommissioningInfo(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.GeneralCommissioning = None, 
                                 struct: Clusters.GeneralCommissioning.Structs.BasicCommissioningInfo = None):
        matter_asserts.assert_valid_uint16(struct.failSafeExpiryLengthSeconds, 'FailSafeExpiryLengthSeconds')
        matter_asserts.assert_valid_uint16(struct.maxCumulativeFailsafeSeconds, 'MaxCumulativeFailsafeSeconds')

if __name__ == "__main__":
    default_matter_test_main()
