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

cluster = Clusters.EcosystemInformation

class ECOINFO_2_1(MatterBaseTest):

    def desc_ECOINFO_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_ECOINFO_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["ECOINFO.S"]

    def steps_ECOINFO_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read DeviceDirectory attribute"),
            TestStep("2", "Read LocationDirectory attribute"),
        ]
        return steps


    @run_if_endpoint_matches(has_cluster(Clusters.EcosystemInformation))
    async def test_ECOINFO_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DeviceDirectory)
        matter_asserts.assert_list(val, "DeviceDirectory attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "DeviceDirectory attribute must contain EcosystemDeviceStruct elements", cluster.Structs.EcosystemDeviceStruct)
        for item in val:
            await self.test_checkEcosystemDeviceStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LocationDirectory)
        matter_asserts.assert_list(val, "LocationDirectory attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "LocationDirectory attribute must contain EcosystemLocationStruct elements", cluster.Structs.EcosystemLocationStruct)
        for item in val:
            await self.test_checkEcosystemLocationStruct(endpoint=endpoint, cluster=cluster, struct=item)

    async def test_checkDeviceTypeStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.EcosystemInformation = None, 
                                 struct: Clusters.Descriptor.Structs.DeviceTypeStruct = None):
        matter_asserts.assert_valid_uint32(struct.deviceType, 'DeviceType must be uint32')
        matter_asserts.assert_valid_uint16(struct.revision, 'Revision')
        asserts.assert_greater_equal(struct.revision, 1)

    async def test_checkEcosystemDeviceStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.EcosystemInformation = None, 
                                 struct: Clusters.EcosystemInformation.Structs.EcosystemDeviceStruct = None):
        if struct.deviceName is not None:
            matter_asserts.assert_is_string(struct.deviceName, "DeviceName must be a string")
            asserts.assert_less_equal(len(struct.deviceName), 64, "DeviceName must have length at most 64!")
        matter_asserts.assert_valid_uint64(struct.deviceNameLastEdit, 'DeviceNameLastEdit')
        if struct.bridgedEndpoint is not None:
            matter_asserts.assert_valid_uint16(struct.bridgedEndpoint, 'BridgedEndpoint must be uint16')
        if struct.originalEndpoint is not None:
            matter_asserts.assert_valid_uint16(struct.originalEndpoint, 'OriginalEndpoint must be uint16')
        matter_asserts.assert_list(struct.deviceTypes, "DeviceTypes attribute must return a list")
        matter_asserts.assert_list_element_type(struct.deviceTypes,  "DeviceTypes attribute must contain DeviceTypeStruct elements", Clusters.Descriptor.Structs.DeviceTypeStruct)
        for item in struct.deviceTypes:
            await self.test_checkDeviceTypeStruct(endpoint=endpoint, cluster=cluster, struct=item)
        matter_asserts.assert_list(struct.uniqueLocationIDs, "UniqueLocationIDs attribute must return a list")
        matter_asserts.assert_list_element_type(struct.uniqueLocationIDs,  "UniqueLocationIDs attribute must contain str elements", str)
        asserts.assert_less_equal(len(struct.uniqueLocationIDs), 64, "UniqueLocationIDs must have at most 64 entries!")
        for  in :
            asserts.assert_less_equal(len(struct.uniqueLocationIDs), 64, "UniqueLocationIDs must have at most 64 entries!")
        matter_asserts.assert_valid_uint64(struct.uniqueLocationIDsLastEdit, 'UniqueLocationIDsLastEdit')

    async def test_checkEcosystemLocationStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.EcosystemInformation = None, 
                                 struct: Clusters.EcosystemInformation.Structs.EcosystemLocationStruct = None):
        matter_asserts.assert_is_string(struct.uniqueLocationID, "UniqueLocationID must be a string")
        asserts.assert_less_equal(len(struct.uniqueLocationID), 64, "UniqueLocationID must have length at most 64!")
        asserts.assert_true(isinstance(struct.locationDescriptor, Globals.Structs.LocationDescriptorStruct), f"struct.locationDescriptor must be of type LocationDescriptorStruct")
        await self.test_checkLocationDescriptorStruct(endpoint=endpoint, cluster=cluster, struct=struct.locationDescriptor)
        matter_asserts.assert_valid_uint64(struct.locationDescriptorLastEdit, 'LocationDescriptorLastEdit')

    async def test_checkLocationDescriptorStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.EcosystemInformation = None, 
                                 struct: Globals.Structs.LocationDescriptorStruct = None):
        matter_asserts.assert_is_string(struct.locationName, "LocationName must be a string")
        asserts.assert_less_equal(len(struct.locationName), 128, "LocationName must have length at most 128!")
        if struct.floorNumber is not NullValue:
            matter_asserts.assert_valid_int16(struct.floorNumber, 'FloorNumber')
        if struct.areaType is not NullValue:
            matter_asserts.assert_valid_uint8(struct.areaType, 'AreaType must be uint8')

if __name__ == "__main__":
    default_matter_test_main()
