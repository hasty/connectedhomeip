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

cluster = Clusters.TimeSynchronization

class TIMESYNC_2_1(MatterBaseTest):

    def desc_TIMESYNC_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_TIMESYNC_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["TIMESYNC"]

    def steps_TIMESYNC_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read UTCTime attribute"),
            TestStep("2", "Read Granularity attribute"),
            TestStep("3", "Read TimeSource attribute"),
            TestStep("4", "Read TrustedTimeSource attribute"),
            TestStep("5", "Read DefaultNTP attribute"),
            TestStep("6", "Read TimeZone attribute"),
            TestStep("7", "Read DSTOffset attribute"),
            TestStep("8", "Read LocalTime attribute"),
            TestStep("9", "Read TimeZoneDatabase attribute"),
            TestStep("10", "Read NTPServerAvailable attribute"),
            TestStep("11", "Read TimeZoneListMaxSize attribute"),
            TestStep("12", "Read DSTOffsetListMaxSize attribute"),
            TestStep("13", "Read SupportsDNSResolve attribute"),
        ]

        return steps


    @async_test_body
    async def test_TIMESYNC_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UTCTime)
        if val is not NullValue:
            matter_asserts.assert_valid_uint64(val, 'UTCTime')

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Granularity)
        matter_asserts.assert_valid_enum(val, "Granularity attribute must return a Clusters.TimeSynchronization.Enums.GranularityEnum", Clusters.TimeSynchronization.Enums.GranularityEnum)

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TimeSource):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TimeSource)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "TimeSource attribute must return a Clusters.TimeSynchronization.Enums.TimeSourceEnum", Clusters.TimeSynchronization.Enums.TimeSourceEnum)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TrustedTimeSource):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TrustedTimeSource)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, Clusters.TimeSynchronization.Structs.TrustedTimeSourceStruct),
                                            f"val must be of type Clusters.TimeSynchronization.Structs.TrustedTimeSourceStruct")
                await self.test_checkTrustedTimeSourceStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DefaultNTP):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DefaultNTP)
            if val is not NullValue:
                matter_asserts.assert_is_string(val, "DefaultNTP must be a string")
                asserts.assert_less_equal(len(val), 128, "DefaultNTP must have length at most 128!")

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TimeZone):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TimeZone)
            matter_asserts.assert_list(val, "TimeZone attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "TimeZone attribute must contain Clusters.TimeSynchronization.Structs.TimeZoneStruct elements", Clusters.TimeSynchronization.Structs.TimeZoneStruct)
            for item in val:
                await self.test_checkTimeZoneStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_greater_equal(len(val), 1, "TimeZone must have at least 1 entries!")
            asserts.assert_less_equal(len(val), 2, "TimeZone must have at most 2 entries!")

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DSTOffset):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DSTOffset)
            matter_asserts.assert_list(val, "DSTOffset attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "DSTOffset attribute must contain Clusters.TimeSynchronization.Structs.DSTOffsetStruct elements", Clusters.TimeSynchronization.Structs.DSTOffsetStruct)
            for item in val:
                await self.test_checkDSTOffsetStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.LocalTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LocalTime)
            if val is not NullValue:
                matter_asserts.assert_valid_uint64(val, 'LocalTime')

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TimeZoneDatabase):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TimeZoneDatabase)
            matter_asserts.assert_valid_enum(val, "TimeZoneDatabase attribute must return a Clusters.TimeSynchronization.Enums.TimeZoneDatabaseEnum", Clusters.TimeSynchronization.Enums.TimeZoneDatabaseEnum)

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NTPServerAvailable):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NTPServerAvailable)
            matter_asserts.assert_valid_bool(val, 'NTPServerAvailable')

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TimeZoneListMaxSize):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TimeZoneListMaxSize)
            matter_asserts.assert_valid_uint8(val, 'TimeZoneListMaxSize')
            asserts.assert_greater_equal(val, 1)
            asserts.assert_less_equal(val, 2)

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DSTOffsetListMaxSize):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DSTOffsetListMaxSize)
            matter_asserts.assert_valid_uint8(val, 'DSTOffsetListMaxSize')
            asserts.assert_greater_equal(val, 1)

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SupportsDNSResolve):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportsDNSResolve)
            matter_asserts.assert_valid_bool(val, 'SupportsDNSResolve')


    async def test_checkDSTOffsetStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.TimeSynchronization = None, 
                                 struct: Clusters.TimeSynchronization.Structs.DSTOffsetStruct = None):
        matter_asserts.assert_valid_int32(struct.offset, 'Offset')
        matter_asserts.assert_valid_uint64(struct.validStarting, 'ValidStarting')
        if struct.validUntil is not NullValue:
            matter_asserts.assert_valid_uint64(struct.validUntil, 'ValidUntil')

    async def test_checkTimeZoneStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.TimeSynchronization = None, 
                                 struct: Clusters.TimeSynchronization.Structs.TimeZoneStruct = None):
        matter_asserts.assert_valid_int32(struct.offset, 'Offset')
        asserts.assert_greater_equal(struct.offset, -43200)
        asserts.assert_less_equal(struct.offset, 50400)
        matter_asserts.assert_valid_uint64(struct.validAt, 'ValidAt')
        if struct.name is not None:
            matter_asserts.assert_is_string(struct.name, "Name must be a string")
            asserts.assert_greater_equal(len(struct.name), 0, "Name must be at least 0 long!")
            asserts.assert_less_equal(len(struct.name), 64, "Name must have length at most 64!")

    async def test_checkTrustedTimeSourceStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.TimeSynchronization = None, 
                                 struct: Clusters.TimeSynchronization.Structs.TrustedTimeSourceStruct = None):
        matter_asserts.assert_valid_uint8(struct.fabricIndex, 'FabricIndex must be uint8')
        matter_asserts.assert_valid_uint64(struct.nodeID, 'NodeID must be uint64')
        matter_asserts.assert_valid_uint16(struct.endpoint, 'Endpoint must be uint16')


if __name__ == "__main__":
    default_matter_test_main()
