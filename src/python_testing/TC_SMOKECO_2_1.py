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

cluster = Clusters.SmokeCOAlarm

class SMOKECO_2_1(MatterBaseTest):

    def desc_SMOKECO_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_SMOKECO_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["SMOKECO.S"]

    def steps_SMOKECO_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read ExpressedState attribute"),
            TestStep("2", "Read SmokeState attribute"),
            TestStep("3", "Read COState attribute"),
            TestStep("4", "Read BatteryAlert attribute"),
            TestStep("5", "Read DeviceMuted attribute"),
            TestStep("6", "Read TestInProgress attribute"),
            TestStep("7", "Read HardwareFaultAlert attribute"),
            TestStep("8", "Read EndOfServiceAlert attribute"),
            TestStep("9", "Read InterconnectSmokeAlarm attribute"),
            TestStep("10", "Read InterconnectCOAlarm attribute"),
            TestStep("11", "Read ContaminationState attribute"),
            TestStep("12", "Read SmokeSensitivityLevel attribute"),
            TestStep("13", "Read ExpiryDate attribute"),
        ]
        return steps


    @run_if_endpoint_matches(has_cluster(Clusters.SmokeCOAlarm))
    async def test_SMOKECO_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ExpressedState)
        matter_asserts.assert_valid_enum(val, "ExpressedState attribute must return a ExpressedStateEnum", cluster.Enums.ExpressedStateEnum)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SmokeState):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SmokeState)
            matter_asserts.assert_valid_enum(val, "SmokeState attribute must return a AlarmStateEnum", cluster.Enums.AlarmStateEnum)

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.COState):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.COState)
            matter_asserts.assert_valid_enum(val, "COState attribute must return a AlarmStateEnum", cluster.Enums.AlarmStateEnum)

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatteryAlert)
        matter_asserts.assert_valid_enum(val, "BatteryAlert attribute must return a AlarmStateEnum", cluster.Enums.AlarmStateEnum)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DeviceMuted):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DeviceMuted)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "DeviceMuted attribute must return a MuteStateEnum", cluster.Enums.MuteStateEnum)

        self.step("6")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TestInProgress)
        matter_asserts.assert_valid_bool(val, 'TestInProgress')

        self.step("7")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.HardwareFaultAlert)
        matter_asserts.assert_valid_bool(val, 'HardwareFaultAlert')

        self.step("8")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EndOfServiceAlert)
        matter_asserts.assert_valid_enum(val, "EndOfServiceAlert attribute must return a EndOfServiceEnum", cluster.Enums.EndOfServiceEnum)

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.InterconnectSmokeAlarm):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.InterconnectSmokeAlarm)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "InterconnectSmokeAlarm attribute must return a AlarmStateEnum", cluster.Enums.AlarmStateEnum)

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.InterconnectCOAlarm):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.InterconnectCOAlarm)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "InterconnectCOAlarm attribute must return a AlarmStateEnum", cluster.Enums.AlarmStateEnum)

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ContaminationState):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ContaminationState)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "ContaminationState attribute must return a ContaminationStateEnum", cluster.Enums.ContaminationStateEnum)

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SmokeSensitivityLevel):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SmokeSensitivityLevel)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "SmokeSensitivityLevel attribute must return a SensitivityEnum", cluster.Enums.SensitivityEnum)

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ExpiryDate):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ExpiryDate)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'ExpiryDate')

if __name__ == "__main__":
    default_matter_test_main()
