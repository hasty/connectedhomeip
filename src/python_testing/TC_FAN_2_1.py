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

cluster = Clusters.FanControl

class FAN_2_1(MatterBaseTest):

    def desc_FAN_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_FAN_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["FAN"]

    def steps_FAN_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read FanMode attribute"),
            TestStep("2", "Read FanModeSequence attribute"),
            TestStep("3", "Read FanModeSequence attribute"),
            TestStep("4", "Read PercentSetting attribute"),
            TestStep("5", "Read PercentCurrent attribute"),
            TestStep("6", "Read SpeedMax attribute"),
            TestStep("7", "Read SpeedSetting attribute"),
            TestStep("8", "Read SpeedCurrent attribute"),
            TestStep("9", "Read RockSupport attribute"),
            TestStep("10", "Read RockSetting attribute"),
            TestStep("11", "Read WindSupport attribute"),
            TestStep("12", "Read WindSetting attribute"),
            TestStep("13", "Read AirflowDirection attribute"),
        ]
        return steps

    SpeedMax = None

    @async_test_body
    async def test_FAN_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.FanMode)
        matter_asserts.assert_valid_enum(val, "FanMode attribute must return a FanModeEnum", cluster.Enums.FanModeEnum)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.FanModeSequence):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.FanModeSequence)
            matter_asserts.assert_valid_enum(val, "FanModeSequence attribute must return a FanModeSequenceEnum", cluster.Enums.FanModeSequenceEnum)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.FanModeSequence)
        matter_asserts.assert_valid_enum(val, "FanModeSequence attribute must return a FanModeSequenceEnum", cluster.Enums.FanModeSequenceEnum)

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PercentSetting)
        if val is not NullValue:
            matter_asserts.assert_valid_uint8(val, 'PercentSetting')
            asserts.assert_less_equal(val, 100)

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PercentCurrent)
        matter_asserts.assert_valid_uint8(val, 'PercentCurrent')
        asserts.assert_less_equal(val, 100)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SpeedMax):
            self.SpeedMax = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SpeedMax)
            matter_asserts.assert_valid_uint8(self.SpeedMax, 'SpeedMax')
            asserts.assert_greater_equal(self.SpeedMax, 1)
            asserts.assert_less_equal(self.SpeedMax, 100)

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SpeedSetting):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SpeedSetting)
            if val is not NullValue:
                matter_asserts.assert_valid_uint8(val, 'SpeedSetting')
                asserts.assert_less_equal(val, self.SpeedMax)

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SpeedCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SpeedCurrent)
            matter_asserts.assert_valid_uint8(val, 'SpeedCurrent')
            asserts.assert_less_equal(val, self.SpeedMax)

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RockSupport):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RockSupport)
            matter_asserts.is_valid_int_value(val)

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RockSetting):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RockSetting)
            matter_asserts.is_valid_int_value(val)

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WindSupport):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WindSupport)
            matter_asserts.is_valid_int_value(val)

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WindSetting):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WindSetting)
            matter_asserts.is_valid_int_value(val)

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AirflowDirection):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AirflowDirection)
            matter_asserts.assert_valid_enum(val, "AirflowDirection attribute must return a AirflowDirectionEnum", cluster.Enums.AirflowDirectionEnum)

if __name__ == "__main__":
    default_matter_test_main()
