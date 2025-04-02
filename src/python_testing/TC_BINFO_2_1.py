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

cluster = Clusters.BasicInformation

class BINFO_2_1(MatterBaseTest):

    def desc_BINFO_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_BINFO_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["BINFO.S"]

    def steps_BINFO_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read DataModelRevision attribute"),
            TestStep("2", "Read VendorName attribute"),
            TestStep("3", "Read VendorID attribute"),
            TestStep("4", "Read ProductName attribute"),
            TestStep("5", "Read ProductID attribute"),
            TestStep("6", "Read NodeLabel attribute"),
            TestStep("7", "Read Location attribute"),
            TestStep("8", "Read HardwareVersion attribute"),
            TestStep("9", "Read HardwareVersionString attribute"),
            TestStep("10", "Read SoftwareVersion attribute"),
            TestStep("11", "Read SoftwareVersionString attribute"),
            TestStep("12", "Read ManufacturingDate attribute"),
            TestStep("13", "Read PartNumber attribute"),
            TestStep("14", "Read ProductURL attribute"),
            TestStep("15", "Read ProductLabel attribute"),
            TestStep("16", "Read SerialNumber attribute"),
            TestStep("17", "Read LocalConfigDisabled attribute"),
            TestStep("18", "Read Reachable attribute"),
            TestStep("19", "Read UniqueID attribute"),
            TestStep("20", "Read CapabilityMinima attribute"),
            TestStep("21", "Read ProductAppearance attribute"),
            TestStep("22", "Read SpecificationVersion attribute"),
            TestStep("23", "Read MaxPathsPerInvoke attribute"),
            TestStep("24", "Read ConfigurationVersion attribute"),
        ]
        return steps

    @run_if_endpoint_matches(has_cluster(Clusters.BasicInformation))
    async def test_BINFO_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DataModelRevision)
        matter_asserts.assert_valid_uint16(val, 'DataModelRevision')

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.VendorName)
        matter_asserts.assert_is_string(val, "VendorName must be a string")
        asserts.assert_less_equal(len(val), 32, "VendorName must have length at most 32!")

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.VendorID)
        matter_asserts.assert_valid_uint16(val, 'VendorID must be uint16')

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ProductName)
        matter_asserts.assert_is_string(val, "ProductName must be a string")
        asserts.assert_less_equal(len(val), 32, "ProductName must have length at most 32!")

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ProductID)
        matter_asserts.assert_valid_uint16(val, 'ProductID')

        self.step("6")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NodeLabel)
        matter_asserts.assert_is_string(val, "NodeLabel must be a string")
        asserts.assert_less_equal(len(val), 32, "NodeLabel must have length at most 32!")

        self.step("7")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Location)
        matter_asserts.assert_is_string(val, "Location must be a string")

        self.step("8")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.HardwareVersion)
        matter_asserts.assert_valid_uint16(val, 'HardwareVersion')

        self.step("9")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.HardwareVersionString)
        matter_asserts.assert_is_string(val, "HardwareVersionString must be a string")
        asserts.assert_greater_equal(len(val), 1, "HardwareVersionString must be at least 1 long!")
        asserts.assert_less_equal(len(val), 64, "HardwareVersionString must have length at most 64!")

        self.step("10")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SoftwareVersion)
        matter_asserts.assert_valid_uint32(val, 'SoftwareVersion')

        self.step("11")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SoftwareVersionString)
        matter_asserts.assert_is_string(val, "SoftwareVersionString must be a string")
        asserts.assert_greater_equal(len(val), 1, "SoftwareVersionString must be at least 1 long!")
        asserts.assert_less_equal(len(val), 64, "SoftwareVersionString must have length at most 64!")

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ManufacturingDate):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ManufacturingDate)
            if val is not None:
                matter_asserts.assert_is_string(val, "ManufacturingDate must be a string")
                asserts.assert_greater_equal(len(val), 8, "ManufacturingDate must be at least 8 long!")
                asserts.assert_less_equal(len(val), 16, "ManufacturingDate must have length at most 16!")

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PartNumber):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PartNumber)
            if val is not None:
                matter_asserts.assert_is_string(val, "PartNumber must be a string")
                asserts.assert_less_equal(len(val), 32, "PartNumber must have length at most 32!")

        self.step("14")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ProductURL):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ProductURL)
            if val is not None:
                matter_asserts.assert_is_string(val, "ProductURL must be a string")
                asserts.assert_less_equal(len(val), 256, "ProductURL must have length at most 256!")

        self.step("15")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ProductLabel):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ProductLabel)
            if val is not None:
                matter_asserts.assert_is_string(val, "ProductLabel must be a string")
                asserts.assert_less_equal(len(val), 64, "ProductLabel must have length at most 64!")

        self.step("16")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SerialNumber):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SerialNumber)
            if val is not None:
                matter_asserts.assert_is_string(val, "SerialNumber must be a string")
                asserts.assert_less_equal(len(val), 32, "SerialNumber must have length at most 32!")

        self.step("17")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.LocalConfigDisabled):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LocalConfigDisabled)
            if val is not None:
                matter_asserts.assert_valid_bool(val, 'LocalConfigDisabled')

        self.step("18")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Reachable):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Reachable)
            if val is not None:
                matter_asserts.assert_valid_bool(val, 'Reachable')

        self.step("19")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UniqueID)
        matter_asserts.assert_is_string(val, "UniqueID must be a string")
        asserts.assert_less_equal(len(val), 32, "UniqueID must have length at most 32!")

        self.step("20")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CapabilityMinima)
        asserts.assert_true(isinstance(val, cluster.Structs.CapabilityMinimaStruct), f"val must be of type CapabilityMinimaStruct")
        await self.test_checkCapabilityMinimaStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("21")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ProductAppearance):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ProductAppearance)
            if val is not None:
                asserts.assert_true(isinstance(val, cluster.Structs.ProductAppearanceStruct), f"val must be of type ProductAppearanceStruct")
                await self.test_checkProductAppearanceStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("22")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SpecificationVersion)
        matter_asserts.assert_valid_uint32(val, 'SpecificationVersion')

        self.step("23")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxPathsPerInvoke)
        matter_asserts.assert_valid_uint16(val, 'MaxPathsPerInvoke')
        asserts.assert_greater_equal(val, 1)

        self.step("24")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ConfigurationVersion)
        matter_asserts.assert_valid_uint32(val, 'ConfigurationVersion')
        asserts.assert_greater_equal(val, 1)

    async def test_checkCapabilityMinimaStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.BasicInformation = None, 
                                 struct: Clusters.BasicInformation.Structs.CapabilityMinimaStruct = None):
        matter_asserts.assert_valid_uint16(struct.caseSessionsPerFabric, 'CaseSessionsPerFabric')
        asserts.assert_greater_equal(struct.caseSessionsPerFabric, 3)
        matter_asserts.assert_valid_uint16(struct.subscriptionsPerFabric, 'SubscriptionsPerFabric')
        asserts.assert_greater_equal(struct.subscriptionsPerFabric, 3)

    async def test_checkProductAppearanceStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.BasicInformation = None, 
                                 struct: Clusters.BasicInformation.Structs.ProductAppearanceStruct = None):
        matter_asserts.assert_valid_enum(struct.finish, "Finish attribute must return a ProductFinishEnum", cluster.Enums.ProductFinishEnum)
        if struct.primaryColor is not NullValue:
            matter_asserts.assert_valid_enum(struct.primaryColor, "PrimaryColor attribute must return a ColorEnum", cluster.Enums.ColorEnum)

if __name__ == "__main__":
    default_matter_test_main()
