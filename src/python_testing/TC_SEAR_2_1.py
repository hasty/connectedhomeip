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

cluster = Clusters.ServiceArea

class SEAR_2_1(MatterBaseTest):

    def desc_SEAR_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_SEAR_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["SEAR"]

    def steps_SEAR_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read SupportedAreas attribute"),
            TestStep("2", "Read SupportedMaps attribute"),
            TestStep("3", "Read SelectedAreas attribute"),
            TestStep("4", "Read CurrentArea attribute"),
            TestStep("5", "Read EstimatedEndTime attribute"),
            TestStep("6", "Read Progress attribute"),
        ]

        return steps


    @async_test_body
    async def test_SEAR_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportedAreas)
        matter_asserts.assert_list(val, "SupportedAreas attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "SupportedAreas attribute must contain Clusters.ServiceArea.Structs.AreaStruct elements", Clusters.ServiceArea.Structs.AreaStruct)
        for item in val:
            await self.test_checkAreaStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(val), 255, "SupportedAreas must have at most 255 entries!")

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SupportedMaps):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportedMaps)
            matter_asserts.assert_list(val, "SupportedMaps attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "SupportedMaps attribute must contain Clusters.ServiceArea.Structs.MapStruct elements", Clusters.ServiceArea.Structs.MapStruct)
            for item in val:
                await self.test_checkMapStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_less_equal(len(val), 255, "SupportedMaps must have at most 255 entries!")

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SelectedAreas)
        matter_asserts.assert_list(val, "SelectedAreas attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "SelectedAreas attribute must contain int elements", int)

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentArea)
        if val is not NullValue and val is not None:
            matter_asserts.assert_valid_uint32(val, 'CurrentArea')

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.EstimatedEndTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EstimatedEndTime)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'EstimatedEndTime')

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Progress):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Progress)
            matter_asserts.assert_list(val, "Progress attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "Progress attribute must contain Clusters.ServiceArea.Structs.ProgressStruct elements", Clusters.ServiceArea.Structs.ProgressStruct)
            for item in val:
                await self.test_checkProgressStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_less_equal(len(val), 255, "Progress must have at most 255 entries!")


    async def test_checkAreaInfoStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ServiceArea = None, 
                                 struct: Clusters.ServiceArea.Structs.AreaInfoStruct = None):
        if struct.locationInfo is not NullValue:
            asserts.assert_true(isinstance(struct.locationInfo, Globals.Structs.LocationDescriptorStruct),
                                        f"struct.locationInfo must be of type Globals.Structs.LocationDescriptorStruct")
            await self.test_checkLocationDescriptorStruct(endpoint=endpoint, cluster=cluster, struct=struct.locationInfo)
        if struct.landmarkInfo is not NullValue:
            asserts.assert_true(isinstance(struct.landmarkInfo, Clusters.ServiceArea.Structs.LandmarkInfoStruct),
                                        f"struct.landmarkInfo must be of type Clusters.ServiceArea.Structs.LandmarkInfoStruct")
            await self.test_checkLandmarkInfoStruct(endpoint=endpoint, cluster=cluster, struct=struct.landmarkInfo)

    async def test_checkAreaStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ServiceArea = None, 
                                 struct: Clusters.ServiceArea.Structs.AreaStruct = None):
        matter_asserts.assert_valid_uint32(struct.areaID, 'AreaID')
        if struct.mapId is not NullValue:
            matter_asserts.assert_valid_uint32(struct.mapID, 'MapID')
        asserts.assert_true(isinstance(struct.areaInfo, Clusters.ServiceArea.Structs.AreaInfoStruct),
                                    f"struct.areaInfo must be of type Clusters.ServiceArea.Structs.AreaInfoStruct")
        await self.test_checkAreaInfoStruct(endpoint=endpoint, cluster=cluster, struct=struct.areaInfo)

    async def test_checkLandmarkInfoStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ServiceArea = None, 
                                 struct: Clusters.ServiceArea.Structs.LandmarkInfoStruct = None):
        matter_asserts.assert_valid_uint8(struct.landmarkTag, 'LandmarkTag must be uint8')
        if struct.relativePositionTag is not NullValue:
            matter_asserts.assert_valid_uint8(struct.relativePositionTag, 'RelativePositionTag must be uint8')

    async def test_checkLocationDescriptorStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ServiceArea = None, 
                                 struct: Globals.Structs.LocationDescriptorStruct = None):
        matter_asserts.assert_is_string(struct.locationName, "LocationName must be a string")
        asserts.assert_less_equal(len(struct.locationName), 128, "LocationName must have length at most 128!")
        if struct.floorNumber is not NullValue:
            matter_asserts.assert_valid_int16(struct.floorNumber, 'FloorNumber')
        if struct.areaType is not NullValue:
            matter_asserts.assert_valid_uint8(struct.areaType, 'AreaType must be uint8')

    async def test_checkMapStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ServiceArea = None, 
                                 struct: Clusters.ServiceArea.Structs.MapStruct = None):
        matter_asserts.assert_valid_uint32(struct.mapID, 'MapID')
        matter_asserts.assert_is_string(struct.name, "Name must be a string")
        asserts.assert_less_equal(len(struct.name), 64, "Name must have length at most 64!")

    async def test_checkProgressStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ServiceArea = None, 
                                 struct: Clusters.ServiceArea.Structs.ProgressStruct = None):
        matter_asserts.assert_valid_uint32(struct.areaID, 'AreaID')
        matter_asserts.assert_valid_enum(struct.status, "Status attribute must return a Clusters.ServiceArea.Enums.OperationalStatusEnum", Clusters.ServiceArea.Enums.OperationalStatusEnum)
        if struct.totalOperationalTime is not NullValue and struct.totalOperationalTime is not None:
            matter_asserts.assert_valid_uint32(struct.totalOperationalTime, 'TotalOperationalTime')
        if struct.initialTimeEstimate is not NullValue and struct.initialTimeEstimate is not None:
            matter_asserts.assert_valid_uint32(struct.initialTimeEstimate, 'InitialTimeEstimate')


if __name__ == "__main__":
    default_matter_test_main()
