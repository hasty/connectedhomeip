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

cluster = Clusters.TimeFormatLocalization

class LTIME_2_1(MatterBaseTest):

    def desc_LTIME_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_LTIME_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["LTIME.S"]

    def steps_LTIME_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read HourFormat attribute"),
            TestStep("2", "Read ActiveCalendarType attribute"),
            TestStep("3", "Read SupportedCalendarTypes attribute"),
        ]
        return steps


    @run_if_endpoint_matches(has_cluster(Clusters.TimeFormatLocalization))
    async def test_LTIME_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.HourFormat)
        matter_asserts.assert_valid_enum(val, "HourFormat attribute must return a HourFormatEnum", cluster.Enums.HourFormatEnum)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveCalendarType):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveCalendarType)
            matter_asserts.assert_valid_enum(val, "ActiveCalendarType attribute must return a CalendarTypeEnum", cluster.Enums.CalendarTypeEnum)

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SupportedCalendarTypes):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportedCalendarTypes)
            matter_asserts.assert_list(val, "SupportedCalendarTypes attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "SupportedCalendarTypes attribute must contain CalendarTypeEnum elements", cluster.Enums.CalendarTypeEnum)

if __name__ == "__main__":
    default_matter_test_main()
