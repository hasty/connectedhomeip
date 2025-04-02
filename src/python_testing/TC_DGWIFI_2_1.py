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

cluster = Clusters.WiFiNetworkDiagnostics

class DGWIFI_2_1(MatterBaseTest):

    def desc_DGWIFI_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_DGWIFI_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["DGWIFI.S"]

    def steps_DGWIFI_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read BSSID attribute"),
            TestStep("2", "Read SecurityType attribute"),
            TestStep("3", "Read WiFiVersion attribute"),
            TestStep("4", "Read ChannelNumber attribute"),
            TestStep("5", "Read RSSI attribute"),
            TestStep("6", "Read BeaconLostCount attribute"),
            TestStep("7", "Read BeaconRxCount attribute"),
            TestStep("8", "Read PacketMulticastRxCount attribute"),
            TestStep("9", "Read PacketMulticastTxCount attribute"),
            TestStep("10", "Read PacketUnicastRxCount attribute"),
            TestStep("11", "Read PacketUnicastTxCount attribute"),
            TestStep("12", "Read CurrentMaxRate attribute"),
            TestStep("13", "Read OverrunCount attribute"),
        ]
        return steps

    @run_if_endpoint_matches(has_cluster(Clusters.WiFiNetworkDiagnostics))
    async def test_DGWIFI_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BSSID)
        if val is not NullValue:
            matter_asserts.assert_is_octstr(val, "BSSID must be an octstr")

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SecurityType)
        if val is not NullValue:
            matter_asserts.assert_valid_enum(val, "SecurityType attribute must return a SecurityTypeEnum", cluster.Enums.SecurityTypeEnum)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WiFiVersion)
        if val is not NullValue:
            matter_asserts.assert_valid_enum(val, "WiFiVersion attribute must return a WiFiVersionEnum", cluster.Enums.WiFiVersionEnum)

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ChannelNumber)
        if val is not NullValue:
            matter_asserts.assert_valid_uint16(val, 'ChannelNumber')

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RSSI)
        if val is not NullValue:
            matter_asserts.assert_valid_int8(val, 'RSSI')
            asserts.assert_greater_equal(val, -120)
            asserts.assert_less_equal(val, 0)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BeaconLostCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BeaconLostCount)
            if val is not NullValue:
                matter_asserts.assert_valid_uint32(val, 'BeaconLostCount')

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BeaconRxCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BeaconRxCount)
            if val is not NullValue:
                matter_asserts.assert_valid_uint32(val, 'BeaconRxCount')

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PacketMulticastRxCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PacketMulticastRxCount)
            if val is not NullValue:
                matter_asserts.assert_valid_uint32(val, 'PacketMulticastRxCount')

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PacketMulticastTxCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PacketMulticastTxCount)
            if val is not NullValue:
                matter_asserts.assert_valid_uint32(val, 'PacketMulticastTxCount')

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PacketUnicastRxCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PacketUnicastRxCount)
            if val is not NullValue:
                matter_asserts.assert_valid_uint32(val, 'PacketUnicastRxCount')

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PacketUnicastTxCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PacketUnicastTxCount)
            if val is not NullValue:
                matter_asserts.assert_valid_uint32(val, 'PacketUnicastTxCount')

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentMaxRate):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentMaxRate)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint64(val, 'CurrentMaxRate')

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OverrunCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OverrunCount)
            if val is not NullValue:
                matter_asserts.assert_valid_uint64(val, 'OverrunCount')

if __name__ == "__main__":
    default_matter_test_main()
