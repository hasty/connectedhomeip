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

cluster = Clusters.EnergyEVSE

class EEVSE_2_1(MatterBaseTest):

    def desc_EEVSE_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_EEVSE_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["EEVSE.S"]

    def steps_EEVSE_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read State attribute"),
            TestStep("2", "Read SupplyState attribute"),
            TestStep("3", "Read FaultState attribute"),
            TestStep("4", "Read ChargingEnabledUntil attribute"),
            TestStep("5", "Read DischargingEnabledUntil attribute"),
            TestStep("6", "Read CircuitCapacity attribute"),
            TestStep("7", "Read MinimumChargeCurrent attribute"),
            TestStep("8", "Read MaximumChargeCurrent attribute"),
            TestStep("9", "Read MaximumDischargeCurrent attribute"),
            TestStep("10", "Read UserMaximumChargeCurrent attribute"),
            TestStep("11", "Read RandomizationDelayWindow attribute"),
            TestStep("12", "Read NextChargeStartTime attribute"),
            TestStep("13", "Read NextChargeTargetTime attribute"),
            TestStep("14", "Read NextChargeRequiredEnergy attribute"),
            TestStep("15", "Read NextChargeTargetSoC attribute"),
            TestStep("16", "Read ApproximateEVEfficiency attribute"),
            TestStep("17", "Read StateOfCharge attribute"),
            TestStep("18", "Read BatteryCapacity attribute"),
            TestStep("19", "Read VehicleID attribute"),
            TestStep("20", "Read SessionID attribute"),
            TestStep("21", "Read SessionDuration attribute"),
            TestStep("22", "Read SessionEnergyCharged attribute"),
            TestStep("23", "Read SessionEnergyDischarged attribute"),
        ]
        return steps


    @run_if_endpoint_matches(has_cluster(Clusters.EnergyEVSE))
    async def test_EEVSE_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.State)
        if val is not NullValue:
            matter_asserts.assert_valid_enum(val, "State attribute must return a StateEnum", cluster.Enums.StateEnum)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupplyState)
        matter_asserts.assert_valid_enum(val, "SupplyState attribute must return a SupplyStateEnum", cluster.Enums.SupplyStateEnum)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.FaultState)
        matter_asserts.assert_valid_enum(val, "FaultState attribute must return a FaultStateEnum", cluster.Enums.FaultStateEnum)

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ChargingEnabledUntil)
        if val is not NullValue:
            matter_asserts.assert_valid_uint32(val, 'ChargingEnabledUntil')

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DischargingEnabledUntil):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DischargingEnabledUntil)
            if val is not NullValue:
                matter_asserts.assert_valid_uint32(val, 'DischargingEnabledUntil')

        self.step("6")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CircuitCapacity)
        matter_asserts.assert_valid_int64(val, 'CircuitCapacity')
        asserts.assert_greater_equal(val, 0)

        self.step("7")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinimumChargeCurrent)
        matter_asserts.assert_valid_int64(val, 'MinimumChargeCurrent')
        asserts.assert_greater_equal(val, 0)

        self.step("8")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaximumChargeCurrent)
        matter_asserts.assert_valid_int64(val, 'MaximumChargeCurrent')
        asserts.assert_greater_equal(val, 0)

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaximumDischargeCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaximumDischargeCurrent)
            matter_asserts.assert_valid_int64(val, 'MaximumDischargeCurrent')
            asserts.assert_greater_equal(val, 0)

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.UserMaximumChargeCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UserMaximumChargeCurrent)
            if val is not None:
                matter_asserts.assert_valid_int64(val, 'UserMaximumChargeCurrent')

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RandomizationDelayWindow):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RandomizationDelayWindow)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RandomizationDelayWindow')
                asserts.assert_less_equal(val, 86400)

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NextChargeStartTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NextChargeStartTime)
            if val is not NullValue:
                matter_asserts.assert_valid_uint32(val, 'NextChargeStartTime')

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NextChargeTargetTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NextChargeTargetTime)
            if val is not NullValue:
                matter_asserts.assert_valid_uint32(val, 'NextChargeTargetTime')

        self.step("14")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NextChargeRequiredEnergy):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NextChargeRequiredEnergy)
            if val is not NullValue:
                matter_asserts.assert_valid_int64(val, 'NextChargeRequiredEnergy')
                asserts.assert_greater_equal(val, 0)

        self.step("15")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NextChargeTargetSoC):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NextChargeTargetSoC)
            if val is not NullValue:
                matter_asserts.assert_valid_uint8(val, 'NextChargeTargetSoC')

        self.step("16")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ApproximateEVEfficiency):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ApproximateEVEfficiency)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'ApproximateEVEfficiency')

        self.step("17")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.StateOfCharge):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.StateOfCharge)
            if val is not NullValue:
                matter_asserts.assert_valid_uint8(val, 'StateOfCharge')

        self.step("18")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatteryCapacity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatteryCapacity)
            if val is not NullValue:
                matter_asserts.assert_valid_int64(val, 'BatteryCapacity')
                asserts.assert_greater_equal(val, 0)

        self.step("19")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.VehicleID):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.VehicleID)
            if val is not NullValue:
                matter_asserts.assert_is_string(val, "VehicleID must be a string")
                asserts.assert_less_equal(len(val), 32, "VehicleID must have length at most 32!")

        self.step("20")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SessionID)
        if val is not NullValue:
            matter_asserts.assert_valid_uint32(val, 'SessionID')

        self.step("21")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SessionDuration)
        if val is not NullValue:
            matter_asserts.assert_valid_uint32(val, 'SessionDuration')

        self.step("22")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SessionEnergyCharged)
        if val is not NullValue:
            matter_asserts.assert_valid_int64(val, 'SessionEnergyCharged')
            asserts.assert_greater_equal(val, 0)

        self.step("23")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SessionEnergyDischarged):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SessionEnergyDischarged)
            if val is not NullValue:
                matter_asserts.assert_valid_int64(val, 'SessionEnergyDischarged')
                asserts.assert_greater_equal(val, 0)

if __name__ == "__main__":
    default_matter_test_main()
