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

cluster = Clusters.PressureMeasurement

class PRS_2_1(MatterBaseTest):

    def desc_PRS_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_PRS_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["PRS"]

    def steps_PRS_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read MeasuredValue attribute"),
            TestStep("2", "Read MinMeasuredValue attribute"),
            TestStep("3", "Read MaxMeasuredValue attribute"),
            TestStep("4", "Read Tolerance attribute"),
            TestStep("5", "Read ScaledValue attribute"),
            TestStep("6", "Read MinScaledValue attribute"),
            TestStep("7", "Read MaxScaledValue attribute"),
            TestStep("8", "Read ScaledTolerance attribute"),
            TestStep("9", "Read Scale attribute"),
        ]
        return steps

    MaxMeasuredValue = None
    MaxScaledValue = None
    MinMeasuredValue = None
    MinScaledValue = None

    @async_test_body
    async def test_PRS_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MeasuredValue)
        if val is not NullValue:
            matter_asserts.assert_valid_int16(val, 'MeasuredValue')
            asserts.assert_greater_equal(val, self.MinMeasuredValue)
            asserts.assert_less_equal(val, self.MaxMeasuredValue)

        self.step("2")
        self.MinMeasuredValue = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinMeasuredValue)
        if self.MinMeasuredValue is not NullValue:
            matter_asserts.assert_valid_int16(self.MinMeasuredValue, 'MinMeasuredValue')
            asserts.assert_less_equal(self.MinMeasuredValue, 32766)

        self.step("3")
        self.MaxMeasuredValue = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxMeasuredValue)
        if self.MaxMeasuredValue is not NullValue:
            matter_asserts.assert_valid_int16(self.MaxMeasuredValue, 'MaxMeasuredValue')
            asserts.assert_greater_equal(self.MaxMeasuredValue, self.MinMeasuredValue + 1)
            asserts.assert_less_equal(self.MaxMeasuredValue, 32767)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Tolerance):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Tolerance)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Tolerance')
                asserts.assert_less_equal(val, 2048)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ScaledValue):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ScaledValue)
            if val is not NullValue:
                matter_asserts.assert_valid_int16(val, 'ScaledValue')
                asserts.assert_greater_equal(val, self.MinScaledValue)
                asserts.assert_less_equal(val, self.MaxScaledValue)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinScaledValue):
            self.MinScaledValue = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinScaledValue)
            if self.MinScaledValue is not NullValue:
                matter_asserts.assert_valid_int16(self.MinScaledValue, 'MinScaledValue')
                asserts.assert_less_equal(self.MinScaledValue, 32766)

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxScaledValue):
            self.MaxScaledValue = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxScaledValue)
            if self.MaxScaledValue is not NullValue:
                matter_asserts.assert_valid_int16(self.MaxScaledValue, 'MaxScaledValue')
                asserts.assert_greater_equal(self.MaxScaledValue, self.MinScaledValue + 1)
                asserts.assert_less_equal(self.MaxScaledValue, 32767)

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ScaledTolerance):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ScaledTolerance)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ScaledTolerance')
                asserts.assert_less_equal(val, 2048)

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Scale):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Scale)
            matter_asserts.assert_valid_int8(val, 'Scale')
            asserts.assert_greater_equal(val, -127)

if __name__ == "__main__":
    default_matter_test_main()
