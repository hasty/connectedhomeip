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

cluster = Clusters.LaundryWasherControls

class WASHERCTRL_2_1(MatterBaseTest):

    def desc_WASHERCTRL_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_WASHERCTRL_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["WASHERCTRL"]

    def steps_WASHERCTRL_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read SpinSpeeds attribute"),
            TestStep("2", "Read SpinSpeedCurrent attribute"),
            TestStep("3", "Read NumberOfRinses attribute"),
            TestStep("4", "Read SupportedRinses attribute"),
        ]
        return steps


    @async_test_body
    async def test_WASHERCTRL_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SpinSpeeds):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SpinSpeeds)
            matter_asserts.assert_list(val, "SpinSpeeds attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "SpinSpeeds attribute must contain str elements", str)
            asserts.assert_less_equal(len(val), 16, "SpinSpeeds must have at most 16 entries!")
            for val in val:
                asserts.assert_less_equal(len(val), 64, "SpinSpeeds must have at most 64 entries!")

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SpinSpeedCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SpinSpeedCurrent)
            if val is not NullValue:
                matter_asserts.assert_valid_uint8(val, 'SpinSpeedCurrent')
                asserts.assert_less_equal(val, 15)

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfRinses):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfRinses)
            matter_asserts.assert_valid_enum(val, "NumberOfRinses attribute must return a NumberOfRinsesEnum", cluster.Enums.NumberOfRinsesEnum)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SupportedRinses):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportedRinses)
            matter_asserts.assert_list(val, "SupportedRinses attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "SupportedRinses attribute must contain NumberOfRinsesEnum elements", cluster.Enums.NumberOfRinsesEnum)
            asserts.assert_less_equal(len(val), 4, "SupportedRinses must have at most 4 entries!")

if __name__ == "__main__":
    default_matter_test_main()
