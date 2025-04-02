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

cluster = Clusters.EthernetNetworkDiagnostics

class DGETH_2_1(MatterBaseTest):

    def desc_DGETH_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_DGETH_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["DGETH.S"]

    def steps_DGETH_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read PHYRate attribute"),
            TestStep("2", "Read FullDuplex attribute"),
            TestStep("3", "Read PacketRxCount attribute"),
            TestStep("4", "Read PacketTxCount attribute"),
            TestStep("5", "Read TxErrCount attribute"),
            TestStep("6", "Read CollisionCount attribute"),
            TestStep("7", "Read OverrunCount attribute"),
            TestStep("8", "Read CarrierDetect attribute"),
            TestStep("9", "Read TimeSinceReset attribute"),
        ]
        return steps


    @run_if_endpoint_matches(has_cluster(Clusters.EthernetNetworkDiagnostics))
    async def test_DGETH_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PHYRate):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PHYRate)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_enum(val, "PHYRate attribute must return a PHYRateEnum", cluster.Enums.PHYRateEnum)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.FullDuplex):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.FullDuplex)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_bool(val, 'FullDuplex')

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PacketRxCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PacketRxCount)
            matter_asserts.assert_valid_uint64(val, 'PacketRxCount')

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PacketTxCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PacketTxCount)
            matter_asserts.assert_valid_uint64(val, 'PacketTxCount')

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxErrCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxErrCount)
            matter_asserts.assert_valid_uint64(val, 'TxErrCount')

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CollisionCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CollisionCount)
            matter_asserts.assert_valid_uint64(val, 'CollisionCount')

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OverrunCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OverrunCount)
            matter_asserts.assert_valid_uint64(val, 'OverrunCount')

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CarrierDetect):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CarrierDetect)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_bool(val, 'CarrierDetect')

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TimeSinceReset):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TimeSinceReset)
            if val is not None:
                matter_asserts.assert_valid_uint64(val, 'TimeSinceReset')

if __name__ == "__main__":
    default_matter_test_main()
