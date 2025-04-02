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

cluster = Clusters.WaterHeaterManagement

class EWATERHTR_2_1(MatterBaseTest):

    def desc_EWATERHTR_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_EWATERHTR_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["EWATERHTR"]

    def steps_EWATERHTR_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read HeaterTypes attribute"),
            TestStep("2", "Read HeatDemand attribute"),
            TestStep("3", "Read TankVolume attribute"),
            TestStep("4", "Read EstimatedHeatRequired attribute"),
            TestStep("5", "Read TankPercentage attribute"),
            TestStep("6", "Read BoostState attribute"),
        ]
        return steps

    TargetPercentage = None

    @async_test_body
    async def test_EWATERHTR_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.HeaterTypes)
        matter_asserts.is_valid_int_value(val)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.HeatDemand)
        matter_asserts.is_valid_int_value(val)

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TankVolume):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TankVolume)
            matter_asserts.assert_valid_uint16(val, 'TankVolume')

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.EstimatedHeatRequired):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EstimatedHeatRequired)
            matter_asserts.assert_valid_int64(val, 'EstimatedHeatRequired')
            asserts.assert_greater_equal(val, 0)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TankPercentage):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TankPercentage)
            matter_asserts.assert_valid_uint8(val, 'TankPercentage')

        self.step("6")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BoostState)
        matter_asserts.assert_valid_enum(val, "BoostState attribute must return a BoostStateEnum", cluster.Enums.BoostStateEnum)

if __name__ == "__main__":
    default_matter_test_main()
