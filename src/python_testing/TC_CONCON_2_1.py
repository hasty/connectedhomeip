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

cluster = Clusters.ContentControl

class CONCON_2_1(MatterBaseTest):

    def desc_CONCON_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_CONCON_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["CONCON.S"]

    def steps_CONCON_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read Enabled attribute"),
            TestStep("2", "Read OnDemandRatings attribute"),
            TestStep("3", "Read OnDemandRatingThreshold attribute"),
            TestStep("4", "Read ScheduledContentRatings attribute"),
            TestStep("5", "Read ScheduledContentRatingThreshold attribute"),
            TestStep("6", "Read ScreenDailyTime attribute"),
            TestStep("7", "Read RemainingScreenTime attribute"),
            TestStep("8", "Read BlockUnrated attribute"),
            TestStep("9", "Read BlockChannelList attribute"),
            TestStep("10", "Read BlockApplicationList attribute"),
            TestStep("11", "Read BlockContentTimeWindow attribute"),
        ]
        return steps


    @async_test_body
    async def test_CONCON_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Enabled)
        matter_asserts.assert_valid_bool(val, 'Enabled')

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OnDemandRatings):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OnDemandRatings)
            matter_asserts.assert_list(val, "OnDemandRatings attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "OnDemandRatings attribute must contain RatingNameStruct elements", cluster.Structs.RatingNameStruct)
            for item in val:
                await self.test_checkRatingNameStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OnDemandRatingThreshold):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OnDemandRatingThreshold)
            matter_asserts.assert_is_string(val, "OnDemandRatingThreshold must be a string")
            asserts.assert_less_equal(len(val), 8, "OnDemandRatingThreshold must have length at most 8!")

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ScheduledContentRatings):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ScheduledContentRatings)
            matter_asserts.assert_list(val, "ScheduledContentRatings attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "ScheduledContentRatings attribute must contain RatingNameStruct elements", cluster.Structs.RatingNameStruct)
            for item in val:
                await self.test_checkRatingNameStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ScheduledContentRatingThreshold):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ScheduledContentRatingThreshold)
            matter_asserts.assert_is_string(val, "ScheduledContentRatingThreshold must be a string")
            asserts.assert_less_equal(len(val), 8, "ScheduledContentRatingThreshold must have length at most 8!")

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ScreenDailyTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ScreenDailyTime)
            matter_asserts.assert_valid_uint32(val, 'ScreenDailyTime')
            asserts.assert_less_equal(val, 86400)

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RemainingScreenTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RemainingScreenTime)
            matter_asserts.assert_valid_uint32(val, 'RemainingScreenTime')
            asserts.assert_less_equal(val, 86400)

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BlockUnrated):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BlockUnrated)
            matter_asserts.assert_valid_bool(val, 'BlockUnrated')

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BlockChannelList):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BlockChannelList)
            matter_asserts.assert_list(val, "BlockChannelList attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "BlockChannelList attribute must contain BlockChannelStruct elements", cluster.Structs.BlockChannelStruct)
            for item in val:
                await self.test_checkBlockChannelStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BlockApplicationList):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BlockApplicationList)
            matter_asserts.assert_list(val, "BlockApplicationList attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "BlockApplicationList attribute must contain AppInfoStruct elements", cluster.Structs.AppInfoStruct)
            for item in val:
                await self.test_checkAppInfoStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BlockContentTimeWindow):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BlockContentTimeWindow)
            matter_asserts.assert_list(val, "BlockContentTimeWindow attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "BlockContentTimeWindow attribute must contain TimeWindowStruct elements", cluster.Structs.TimeWindowStruct)
            for item in val:
                await self.test_checkTimeWindowStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_less_equal(len(val), 7, "BlockContentTimeWindow must have at most 7 entries!")

    async def test_checkAppInfoStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ContentControl = None, 
                                 struct: Clusters.ContentControl.Structs.AppInfoStruct = None):
        matter_asserts.assert_valid_uint16(struct.catalogVendorID, 'CatalogVendorID')
        matter_asserts.assert_is_string(struct.applicationID, "ApplicationID must be a string")

    async def test_checkBlockChannelStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ContentControl = None, 
                                 struct: Clusters.ContentControl.Structs.BlockChannelStruct = None):
        if struct.blockChannelIndex is not NullValue:
            matter_asserts.assert_valid_uint16(struct.blockChannelIndex, 'BlockChannelIndex')
        matter_asserts.assert_valid_uint16(struct.majorNumber, 'MajorNumber')
        matter_asserts.assert_valid_uint16(struct.minorNumber, 'MinorNumber')
        if struct.identifier is not None:
            matter_asserts.assert_is_string(struct.identifier, "Identifier must be a string")

    async def test_checkRatingNameStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ContentControl = None, 
                                 struct: Clusters.ContentControl.Structs.RatingNameStruct = None):
        matter_asserts.assert_is_string(struct.ratingName, "RatingName must be a string")
        asserts.assert_less_equal(len(struct.ratingName), 8, "RatingName must have length at most 8!")
        if struct.ratingNameDesc is not None:
            matter_asserts.assert_is_string(struct.ratingNameDesc, "RatingNameDesc must be a string")
            asserts.assert_less_equal(len(struct.ratingNameDesc), 64, "RatingNameDesc must have length at most 64!")

    async def test_checkTimePeriodStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ContentControl = None, 
                                 struct: Clusters.ContentControl.Structs.TimePeriodStruct = None):
        matter_asserts.assert_valid_uint8(struct.startHour, 'StartHour')
        asserts.assert_greater_equal(struct.startHour, 0)
        asserts.assert_less_equal(struct.startHour, 23)
        matter_asserts.assert_valid_uint8(struct.startMinute, 'StartMinute')
        asserts.assert_greater_equal(struct.startMinute, 0)
        asserts.assert_less_equal(struct.startMinute, 59)
        matter_asserts.assert_valid_uint8(struct.endHour, 'EndHour')
        asserts.assert_greater_equal(struct.endHour, 0)
        asserts.assert_less_equal(struct.endHour, 23)
        matter_asserts.assert_valid_uint8(struct.endMinute, 'EndMinute')
        asserts.assert_greater_equal(struct.endMinute, 0)
        asserts.assert_less_equal(struct.endMinute, 59)

    async def test_checkTimeWindowStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ContentControl = None, 
                                 struct: Clusters.ContentControl.Structs.TimeWindowStruct = None):
        if struct.timeWindowIndex is not NullValue:
            matter_asserts.assert_valid_uint16(struct.timeWindowIndex, 'TimeWindowIndex')
        matter_asserts.is_valid_int_value(struct.dayOfWeek)
        matter_asserts.assert_list(struct.timePeriod, "TimePeriod attribute must return a list")
        matter_asserts.assert_list_element_type(struct.timePeriod,  "TimePeriod attribute must contain TimePeriodStruct elements", cluster.Structs.TimePeriodStruct)
        for item in struct.timePeriod:
            await self.test_checkTimePeriodStruct(endpoint=endpoint, cluster=cluster, struct=item)

if __name__ == "__main__":
    default_matter_test_main()
