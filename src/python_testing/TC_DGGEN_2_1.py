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

cluster = Clusters.GeneralDiagnostics

class DGGEN_2_1(MatterBaseTest):

    def desc_DGGEN_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_DGGEN_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["DGGEN.S"]

    def steps_DGGEN_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read NetworkInterfaces attribute"),
            TestStep("2", "Read RebootCount attribute"),
            TestStep("3", "Read UpTime attribute"),
            TestStep("4", "Read TotalOperationalHours attribute"),
            TestStep("5", "Read BootReason attribute"),
            TestStep("6", "Read ActiveHardwareFaults attribute"),
            TestStep("7", "Read ActiveRadioFaults attribute"),
            TestStep("8", "Read ActiveNetworkFaults attribute"),
            TestStep("9", "Read TestEventTriggersEnabled attribute"),
        ]
        return steps


    @run_if_endpoint_matches(has_cluster(Clusters.GeneralDiagnostics))
    async def test_DGGEN_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NetworkInterfaces)
        matter_asserts.assert_list(val, "NetworkInterfaces attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "NetworkInterfaces attribute must contain NetworkInterface elements", cluster.Structs.NetworkInterface)
        for item in val:
            await self.test_checkNetworkInterface(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(val), 8, "NetworkInterfaces must have at most 8 entries!")

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RebootCount)
        matter_asserts.assert_valid_uint16(val, 'RebootCount')

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UpTime)
        matter_asserts.assert_valid_uint64(val, 'UpTime')

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TotalOperationalHours):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TotalOperationalHours)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TotalOperationalHours')

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BootReason):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BootReason)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "BootReason attribute must return a BootReasonEnum", cluster.Enums.BootReasonEnum)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveHardwareFaults):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveHardwareFaults)
            if val is not None:
                matter_asserts.assert_list(val, "ActiveHardwareFaults attribute must return a list")
                matter_asserts.assert_list_element_type(val,  "ActiveHardwareFaults attribute must contain HardwareFaultEnum elements", cluster.Enums.HardwareFaultEnum)
                asserts.assert_less_equal(len(val), 11, "ActiveHardwareFaults must have at most 11 entries!")

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveRadioFaults):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveRadioFaults)
            if val is not None:
                matter_asserts.assert_list(val, "ActiveRadioFaults attribute must return a list")
                matter_asserts.assert_list_element_type(val,  "ActiveRadioFaults attribute must contain RadioFaultEnum elements", cluster.Enums.RadioFaultEnum)
                asserts.assert_less_equal(len(val), 7, "ActiveRadioFaults must have at most 7 entries!")

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveNetworkFaults):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveNetworkFaults)
            if val is not None:
                matter_asserts.assert_list(val, "ActiveNetworkFaults attribute must return a list")
                matter_asserts.assert_list_element_type(val,  "ActiveNetworkFaults attribute must contain NetworkFaultEnum elements", cluster.Enums.NetworkFaultEnum)
                asserts.assert_less_equal(len(val), 4, "ActiveNetworkFaults must have at most 4 entries!")

        self.step("9")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TestEventTriggersEnabled)
        matter_asserts.assert_valid_bool(val, 'TestEventTriggersEnabled')

    async def test_checkNetworkInterface(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.GeneralDiagnostics = None, 
                                 struct: Clusters.GeneralDiagnostics.Structs.NetworkInterface = None):
        matter_asserts.assert_is_string(struct.name, "Name must be a string")
        asserts.assert_less_equal(len(struct.name), 32, "Name must have length at most 32!")
        matter_asserts.assert_valid_bool(struct.isOperational, 'IsOperational')
        if struct.offPremiseServicesReachableIpv4 is not NullValue:
            matter_asserts.assert_valid_bool(struct.offPremiseServicesReachableIPv4, 'OffPremiseServicesReachableIPv4')
        if struct.offPremiseServicesReachableIpv6 is not NullValue:
            matter_asserts.assert_valid_bool(struct.offPremiseServicesReachableIPv6, 'OffPremiseServicesReachableIPv6')
        asserts.assert_true(isinstance(struct.hardwareAddress, bytes), "HardwareAddress must be of type bytes")
        asserts.assert_true(len(struct.hardwareAddress) in [6,8]), "HardwareAddress must have a length of 6 or 8 bytes")
        HardwareAddress must have a length of 6")
        matter_asserts.assert_list(struct.iPv4Addresses, "IPv4Addresses attribute must return a list")
        matter_asserts.assert_list_element_type(struct.iPv4Addresses,  "IPv4Addresses attribute must contain bytes elements", bytes)
        asserts.assert_less_equal(len(struct.iPv4Addresses), 4, "IPv4Addresses must have at most 4 entries!")
        matter_asserts.assert_list(struct.iPv6Addresses, "IPv6Addresses attribute must return a list")
        matter_asserts.assert_list_element_type(struct.iPv6Addresses,  "IPv6Addresses attribute must contain bytes elements", bytes)
        asserts.assert_less_equal(len(struct.iPv6Addresses), 8, "IPv6Addresses must have at most 8 entries!")
        matter_asserts.assert_valid_enum(struct.type, "Type attribute must return a InterfaceTypeEnum", cluster.Enums.InterfaceTypeEnum)

if __name__ == "__main__":
    default_matter_test_main()
