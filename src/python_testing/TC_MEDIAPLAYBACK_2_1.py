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

cluster = Clusters.MediaPlayback

class MEDIAPLAYBACK_2_1(MatterBaseTest):

    def desc_MEDIAPLAYBACK_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_MEDIAPLAYBACK_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["MEDIAPLAYBACK"]

    def steps_MEDIAPLAYBACK_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read CurrentState attribute"),
            TestStep("2", "Read StartTime attribute"),
            TestStep("3", "Read Duration attribute"),
            TestStep("4", "Read SampledPosition attribute"),
            TestStep("5", "Read PlaybackSpeed attribute"),
            TestStep("6", "Read SeekRangeEnd attribute"),
            TestStep("7", "Read SeekRangeStart attribute"),
            TestStep("8", "Read ActiveAudioTrack attribute"),
            TestStep("9", "Read AvailableAudioTracks attribute"),
            TestStep("10", "Read ActiveTextTrack attribute"),
            TestStep("11", "Read AvailableTextTracks attribute"),
        ]

        return steps


    @async_test_body
    async def test_MEDIAPLAYBACK_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentState)
        matter_asserts.assert_valid_enum(val, "CurrentState attribute must return a Clusters.MediaPlayback.Enums.PlaybackStateEnum", Clusters.MediaPlayback.Enums.PlaybackStateEnum)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.StartTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.StartTime)
            if val is not NullValue:
                matter_asserts.assert_valid_uint64(val, 'StartTime')

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Duration):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Duration)
            if val is not NullValue:
                matter_asserts.assert_valid_uint64(val, 'Duration')

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SampledPosition):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SampledPosition)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, Clusters.MediaPlayback.Structs.PlaybackPositionStruct),
                                            f"val must be of type Clusters.MediaPlayback.Structs.PlaybackPositionStruct")
                await self.test_checkPlaybackPositionStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PlaybackSpeed):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PlaybackSpeed)
            asserts.assert_true(isinstance(val, float), f"val must be a float")

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SeekRangeEnd):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SeekRangeEnd)
            if val is not NullValue:
                matter_asserts.assert_valid_uint64(val, 'SeekRangeEnd')

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SeekRangeStart):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SeekRangeStart)
            if val is not NullValue:
                matter_asserts.assert_valid_uint64(val, 'SeekRangeStart')

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveAudioTrack):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveAudioTrack)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, Clusters.MediaPlayback.Structs.TrackStruct),
                                            f"val must be of type Clusters.MediaPlayback.Structs.TrackStruct")
                await self.test_checkTrackStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AvailableAudioTracks):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AvailableAudioTracks)
            if val is not NullValue:
                matter_asserts.assert_list(val, "AvailableAudioTracks attribute must return a list")
                matter_asserts.assert_list_element_type(val,  "AvailableAudioTracks attribute must contain Clusters.MediaPlayback.Structs.TrackStruct elements", Clusters.MediaPlayback.Structs.TrackStruct)
                for item in val:
                    await self.test_checkTrackStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveTextTrack):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveTextTrack)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, Clusters.MediaPlayback.Structs.TrackStruct),
                                            f"val must be of type Clusters.MediaPlayback.Structs.TrackStruct")
                await self.test_checkTrackStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AvailableTextTracks):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AvailableTextTracks)
            if val is not NullValue:
                matter_asserts.assert_list(val, "AvailableTextTracks attribute must return a list")
                matter_asserts.assert_list_element_type(val,  "AvailableTextTracks attribute must contain Clusters.MediaPlayback.Structs.TrackStruct elements", Clusters.MediaPlayback.Structs.TrackStruct)
                for item in val:
                    await self.test_checkTrackStruct(endpoint=endpoint, cluster=cluster, struct=item)


    async def test_checkPlaybackPositionStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.MediaPlayback = None, 
                                 struct: Clusters.MediaPlayback.Structs.PlaybackPositionStruct = None):
        matter_asserts.assert_valid_uint64(struct.updatedAt, 'UpdatedAt')
        if struct.position is not NullValue:
            matter_asserts.assert_valid_uint64(struct.position, 'Position')

    async def test_checkTrackAttributesStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.MediaPlayback = None, 
                                 struct: Clusters.MediaPlayback.Structs.TrackAttributesStruct = None):
        matter_asserts.assert_is_string(struct.languageCode, "LanguageCode must be a string")
        asserts.assert_less_equal(len(struct.languageCode), 32, "LanguageCode must have length at most 32!")
        if struct.characteristics is not NullValue and struct.characteristics is not None:
            matter_asserts.assert_list(struct.characteristics, "Characteristics attribute must return a list")
            matter_asserts.assert_list_element_type(struct.characteristics,  "Characteristics attribute must contain Clusters.MediaPlayback.Enums.CharacteristicEnum elements", Clusters.MediaPlayback.Enums.CharacteristicEnum)
        if struct.displayName is not NullValue and struct.displayName is not None:
            matter_asserts.assert_is_string(struct.displayName, "DisplayName must be a string")
            asserts.assert_less_equal(len(struct.displayName), 256, "DisplayName must have length at most 256!")

    async def test_checkTrackStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.MediaPlayback = None, 
                                 struct: Clusters.MediaPlayback.Structs.TrackStruct = None):
        matter_asserts.assert_is_string(struct.iD, "ID must be a string")
        asserts.assert_less_equal(len(struct.iD), 32, "ID must have length at most 32!")
        asserts.assert_true(isinstance(struct.trackAttributes, Clusters.MediaPlayback.Structs.TrackAttributesStruct),
                                    f"struct.trackAttributes must be of type Clusters.MediaPlayback.Structs.TrackAttributesStruct")
        await self.test_checkTrackAttributesStruct(endpoint=endpoint, cluster=cluster, struct=struct.trackAttributes)


if __name__ == "__main__":
    default_matter_test_main()
