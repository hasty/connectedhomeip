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

cluster = Clusters.NetworkCommissioning

class CNET_2_1(MatterBaseTest):

    def desc_CNET_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_CNET_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["CNET"]

    def steps_CNET_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read MaxNetworks attribute"),
            TestStep("2", "Read Networks attribute"),
            TestStep("3", "Read ScanMaxTimeSeconds attribute"),
            TestStep("4", "Read ConnectMaxTimeSeconds attribute"),
            TestStep("5", "Read InterfaceEnabled attribute"),
            TestStep("6", "Read LastNetworkingStatus attribute"),
            TestStep("7", "Read LastNetworkID attribute"),
            TestStep("8", "Read LastConnectErrorValue attribute"),
            TestStep("9", "Read SupportedWiFiBands attribute"),
            TestStep("10", "Read SupportedThreadFeatures attribute"),
            TestStep("11", "Read ThreadVersion attribute"),
        ]

        return steps

    MaxNetworks = None

    @async_test_body
    async def test_CNET_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        self.MaxNetworks = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxNetworks)
        matter_asserts.assert_valid_uint8(self.MaxNetworks, 'MaxNetworks')
        asserts.assert_greater_equal(self.MaxNetworks, 1)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Networks)
        matter_asserts.assert_list(val, "Networks attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "Networks attribute must contain NetworkInfoStruct elements", cluster.Structs.NetworkInfoStruct)
        for item in val:
            await self.test_checkNetworkInfoStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(val), self.MaxNetworks, "Networks must have at most self.MaxNetworks entries!")

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ScanMaxTimeSeconds):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ScanMaxTimeSeconds)
            matter_asserts.assert_valid_uint8(val, 'ScanMaxTimeSeconds')

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ConnectMaxTimeSeconds):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ConnectMaxTimeSeconds)
            matter_asserts.assert_valid_uint8(val, 'ConnectMaxTimeSeconds')

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.InterfaceEnabled)
        matter_asserts.assert_valid_bool(val, 'InterfaceEnabled')

        self.step("6")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LastNetworkingStatus)
        if val is not NullValue:
            matter_asserts.assert_valid_enum(val, "LastNetworkingStatus attribute must return a NetworkCommissioningStatusEnum", cluster.Enums.NetworkCommissioningStatusEnum)

        self.step("7")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LastNetworkID)
        if val is not NullValue:
            matter_asserts.assert_is_octstr(val, "LastNetworkID must be an octstr")
            asserts.assert_greater_equal(len(val), 1, "LastNetworkID must be at least 1 long!")
            asserts.assert_less_equal(len(val), 32, "LastNetworkID must have length at most 32!")

        self.step("8")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LastConnectErrorValue)
        if val is not NullValue:
            matter_asserts.assert_valid_int32(val, 'LastConnectErrorValue')

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SupportedWiFiBands):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportedWiFiBands)
            matter_asserts.assert_list(val, "SupportedWiFiBands attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "SupportedWiFiBands attribute must contain WiFiBandEnum elements", cluster.Enums.WiFiBandEnum)
            asserts.assert_greater_equal(len(val), 1, "SupportedWiFiBands must have at least 1 entries!")

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SupportedThreadFeatures):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportedThreadFeatures)
            matter_asserts.is_valid_int_value(val)

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ThreadVersion):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ThreadVersion)
            matter_asserts.assert_valid_uint16(val, 'ThreadVersion')


    async def test_checkNetworkInfoStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.NetworkCommissioning = None, 
                                 struct: Clusters.NetworkCommissioning.Structs.NetworkInfoStruct = None):
        matter_asserts.assert_is_octstr(struct.networkID, "NetworkID must be an octstr")
        asserts.assert_greater_equal(len(struct.networkID), 1, "NetworkID must be at least 1 long!")
        asserts.assert_less_equal(len(struct.networkID), 32, "NetworkID must have length at most 32!")
        matter_asserts.assert_valid_bool(struct.connected, 'Connected')


if __name__ == "__main__":
    default_matter_test_main()
