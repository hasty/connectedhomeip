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

cluster = Clusters.PumpConfigurationAndControl

class PCC_2_1(MatterBaseTest):

    def desc_PCC_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_PCC_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["PCC"]

    def steps_PCC_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read MaxPressure attribute"),
            TestStep("2", "Read MaxSpeed attribute"),
            TestStep("3", "Read MaxFlow attribute"),
            TestStep("4", "Read MinConstPressure attribute"),
            TestStep("5", "Read MaxConstPressure attribute"),
            TestStep("6", "Read MinCompPressure attribute"),
            TestStep("7", "Read MaxCompPressure attribute"),
            TestStep("8", "Read MinConstSpeed attribute"),
            TestStep("9", "Read MaxConstSpeed attribute"),
            TestStep("10", "Read MinConstFlow attribute"),
            TestStep("11", "Read MaxConstFlow attribute"),
            TestStep("12", "Read MinConstTemp attribute"),
            TestStep("13", "Read MaxConstTemp attribute"),
            TestStep("14", "Read PumpStatus attribute"),
            TestStep("15", "Read EffectiveOperationMode attribute"),
            TestStep("16", "Read EffectiveControlMode attribute"),
            TestStep("17", "Read Capacity attribute"),
            TestStep("18", "Read Speed attribute"),
            TestStep("19", "Read LifetimeRunningHours attribute"),
            TestStep("20", "Read Power attribute"),
            TestStep("21", "Read LifetimeEnergyConsumed attribute"),
            TestStep("22", "Read OperationMode attribute"),
            TestStep("23", "Read ControlMode attribute"),
        ]

        return steps


    @async_test_body
    async def test_PCC_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxPressure)
        if val is not NullValue:
            matter_asserts.assert_valid_int16(val, 'MaxPressure')

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxSpeed)
        if val is not NullValue:
            matter_asserts.assert_valid_uint16(val, 'MaxSpeed')

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxFlow)
        if val is not NullValue:
            matter_asserts.assert_valid_uint16(val, 'MaxFlow')

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinConstPressure):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinConstPressure)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int16(val, 'MinConstPressure')

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxConstPressure):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxConstPressure)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int16(val, 'MaxConstPressure')

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinCompPressure):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinCompPressure)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int16(val, 'MinCompPressure')

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxCompPressure):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxCompPressure)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int16(val, 'MaxCompPressure')

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinConstSpeed):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinConstSpeed)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'MinConstSpeed')

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxConstSpeed):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxConstSpeed)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'MaxConstSpeed')

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinConstFlow):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinConstFlow)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'MinConstFlow')

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxConstFlow):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxConstFlow)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'MaxConstFlow')

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinConstTemp):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinConstTemp)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int16(val, 'MinConstTemp')
                asserts.assert_greater_equal(val, -27315)

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxConstTemp):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxConstTemp)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_int16(val, 'MaxConstTemp')
                asserts.assert_greater_equal(val, -27315)

        self.step("14")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PumpStatus):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PumpStatus)
            if val is not None:
                matter_asserts.is_valid_int_value(val)

        self.step("15")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EffectiveOperationMode)
        matter_asserts.assert_valid_enum(val, "EffectiveOperationMode attribute must return a OperationModeEnum", cluster.Enums.OperationModeEnum)

        self.step("16")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EffectiveControlMode)
        matter_asserts.assert_valid_enum(val, "EffectiveControlMode attribute must return a ControlModeEnum", cluster.Enums.ControlModeEnum)

        self.step("17")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Capacity)
        if val is not NullValue:
            matter_asserts.assert_valid_int16(val, 'Capacity')

        self.step("18")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Speed):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Speed)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'Speed')

        self.step("19")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.LifetimeRunningHours):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LifetimeRunningHours)
            if val is not NullValue and val is not None:
                asserts.assert_true(matter_asserts.is_valid_uint_value(value, bit_count=24), 'LifetimeRunningHoursmust be a valid uint24 integer')

        self.step("20")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Power):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Power)
            if val is not NullValue and val is not None:
                asserts.assert_true(matter_asserts.is_valid_uint_value(value, bit_count=24), 'Powermust be a valid uint24 integer')

        self.step("21")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.LifetimeEnergyConsumed):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LifetimeEnergyConsumed)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'LifetimeEnergyConsumed')

        self.step("22")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OperationMode)
        matter_asserts.assert_valid_enum(val, "OperationMode attribute must return a OperationModeEnum", cluster.Enums.OperationModeEnum)

        self.step("23")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ControlMode):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ControlMode)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "ControlMode attribute must return a ControlModeEnum", cluster.Enums.ControlModeEnum)



if __name__ == "__main__":
    default_matter_test_main()
