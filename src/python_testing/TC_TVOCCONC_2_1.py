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

cluster = Clusters.TotalVolatileOrganicCompoundsConcentrationMeasurement

class TVOCCONC_2_1(MatterBaseTest):

    def desc_TVOCCONC_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_TVOCCONC_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["TVOCCONC"]

    def steps_TVOCCONC_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read MeasuredValue attribute"),
            TestStep("2", "Read MinMeasuredValue attribute"),
            TestStep("3", "Read MaxMeasuredValue attribute"),
            TestStep("4", "Read PeakMeasuredValue attribute"),
            TestStep("5", "Read PeakMeasuredValueWindow attribute"),
            TestStep("6", "Read AverageMeasuredValue attribute"),
            TestStep("7", "Read AverageMeasuredValueWindow attribute"),
            TestStep("8", "Read Uncertainty attribute"),
            TestStep("9", "Read MeasurementUnit attribute"),
            TestStep("10", "Read MeasurementMedium attribute"),
            TestStep("11", "Read LevelValue attribute"),
        ]
        return steps

    MaxMeasuredValue = None
    MinMeasuredValue = None

    @async_test_body
    async def test_TVOCCONC_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MeasuredValue):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MeasuredValue)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, float), f"val must be a float")
                asserts.assert_greater_equal(val, self.MinMeasuredValue)
                asserts.assert_less_equal(val, self.MaxMeasuredValue)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinMeasuredValue):
            self.MinMeasuredValue = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinMeasuredValue)
            if self.MinMeasuredValue is not NullValue:
                asserts.assert_true(isinstance(self.MinMeasuredValue, float), f"self.MinMeasuredValue must be a float")

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxMeasuredValue):
            self.MaxMeasuredValue = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxMeasuredValue)
            if self.MaxMeasuredValue is not NullValue:
                asserts.assert_true(isinstance(self.MaxMeasuredValue, float), f"self.MaxMeasuredValue must be a float")
                asserts.assert_greater_equal(self.MaxMeasuredValue, self.MinMeasuredValue)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PeakMeasuredValue):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PeakMeasuredValue)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, float), f"val must be a float")
                asserts.assert_greater_equal(val, self.MinMeasuredValue)
                asserts.assert_less_equal(val, self.MaxMeasuredValue)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PeakMeasuredValueWindow):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PeakMeasuredValueWindow)
            matter_asserts.assert_valid_uint32(val, 'PeakMeasuredValueWindow')
            asserts.assert_less_equal(val, 604800)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AverageMeasuredValue):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AverageMeasuredValue)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, float), f"val must be a float")
                asserts.assert_greater_equal(val, self.MinMeasuredValue)
                asserts.assert_less_equal(val, self.MaxMeasuredValue)

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AverageMeasuredValueWindow):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AverageMeasuredValueWindow)
            matter_asserts.assert_valid_uint32(val, 'AverageMeasuredValueWindow')
            asserts.assert_less_equal(val, 604800)

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Uncertainty):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Uncertainty)
            if val is not None:
                asserts.assert_true(isinstance(val, float), f"val must be a float")

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MeasurementUnit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MeasurementUnit)
            matter_asserts.assert_valid_enum(val, "MeasurementUnit attribute must return a MeasurementUnitEnum", Clusters.CarbonMonoxideConcentrationMeasurement.Enums.MeasurementUnitEnum)

        self.step("10")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MeasurementMedium)
        matter_asserts.assert_valid_enum(val, "MeasurementMedium attribute must return a MeasurementMediumEnum", Clusters.CarbonMonoxideConcentrationMeasurement.Enums.MeasurementMediumEnum)

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.LevelValue):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LevelValue)
            matter_asserts.assert_valid_enum(val, "LevelValue attribute must return a LevelValueEnum", Clusters.CarbonMonoxideConcentrationMeasurement.Enums.LevelValueEnum)

if __name__ == "__main__":
    default_matter_test_main()
