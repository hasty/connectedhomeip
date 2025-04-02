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

cluster = Clusters.WindowCovering

class WNCV_2_1(MatterBaseTest):

    def desc_WNCV_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_WNCV_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["WNCV.S"]

    def steps_WNCV_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read Type attribute"),
            TestStep("2", "Read PhysicalClosedLimitLift attribute"),
            TestStep("3", "Read PhysicalClosedLimitTilt attribute"),
            TestStep("4", "Read CurrentPositionLift attribute"),
            TestStep("5", "Read CurrentPositionTilt attribute"),
            TestStep("6", "Read NumberOfActuationsLift attribute"),
            TestStep("7", "Read NumberOfActuationsTilt attribute"),
            TestStep("8", "Read ConfigStatus attribute"),
            TestStep("9", "Read CurrentPositionLiftPercentage attribute"),
            TestStep("10", "Read CurrentPositionTiltPercentage attribute"),
            TestStep("11", "Read OperationalStatus attribute"),
            TestStep("12", "Read TargetPositionLiftPercent100ths attribute"),
            TestStep("13", "Read TargetPositionTiltPercent100ths attribute"),
            TestStep("14", "Read EndProductType attribute"),
            TestStep("15", "Read CurrentPositionLiftPercent100ths attribute"),
            TestStep("16", "Read CurrentPositionTiltPercent100ths attribute"),
            TestStep("17", "Read InstalledOpenLimitLift attribute"),
            TestStep("18", "Read InstalledClosedLimitLift attribute"),
            TestStep("19", "Read InstalledOpenLimitTilt attribute"),
            TestStep("20", "Read InstalledClosedLimitTilt attribute"),
            TestStep("21", "Read Mode attribute"),
            TestStep("22", "Read SafetyStatus attribute"),
        ]
        return steps

    InstalledClosedLimitLift = None
    InstalledClosedLimitTilt = None
    InstalledOpenLimitLift = None
    InstalledOpenLimitTilt = None

    @run_if_endpoint_matches(has_cluster(Clusters.WindowCovering))
    async def test_WNCV_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Type)
        matter_asserts.assert_valid_enum(val, "Type attribute must return a TypeEnum", cluster.Enums.TypeEnum)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PhysicalClosedLimitLift):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PhysicalClosedLimitLift)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'PhysicalClosedLimitLift')

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PhysicalClosedLimitTilt):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PhysicalClosedLimitTilt)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'PhysicalClosedLimitTilt')

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentPositionLift):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentPositionLift)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'CurrentPositionLift')
                asserts.assert_greater_equal(val, self.InstalledOpenLimitLift)
                asserts.assert_less_equal(val, self.InstalledClosedLimitLift)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentPositionTilt):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentPositionTilt)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'CurrentPositionTilt')
                asserts.assert_greater_equal(val, self.InstalledOpenLimitTilt)
                asserts.assert_less_equal(val, self.InstalledClosedLimitTilt)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfActuationsLift):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfActuationsLift)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'NumberOfActuationsLift')

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfActuationsTilt):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfActuationsTilt)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'NumberOfActuationsTilt')

        self.step("8")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ConfigStatus)
        matter_asserts.is_valid_int_value(val)
        # Check bitmap value less than or equal to (Operational | OnlineReserved | LiftMovementReversed | LiftPositionAware | TiltPositionAware | LiftEncoderControlled | TiltEncoderControlled)
        asserts.assert_less_equal(val, 127)

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentPositionLiftPercentage):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentPositionLiftPercentage)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'CurrentPositionLiftPercentage')

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentPositionTiltPercentage):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentPositionTiltPercentage)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'CurrentPositionTiltPercentage')

        self.step("11")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OperationalStatus)
        matter_asserts.is_valid_int_value(val)
        # Check bitmap value less than or equal to (Global | Lift | Tilt)
        asserts.assert_less_equal(val, 63)

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TargetPositionLiftPercent100ths):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TargetPositionLiftPercent100ths)
            if val is not NullValue:
                matter_asserts.assert_valid_uint16(val, 'TargetPositionLiftPercent100ths')

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TargetPositionTiltPercent100ths):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TargetPositionTiltPercent100ths)
            if val is not NullValue:
                matter_asserts.assert_valid_uint16(val, 'TargetPositionTiltPercent100ths')

        self.step("14")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EndProductType)
        matter_asserts.assert_valid_enum(val, "EndProductType attribute must return a EndProductTypeEnum", cluster.Enums.EndProductTypeEnum)

        self.step("15")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentPositionLiftPercent100ths):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentPositionLiftPercent100ths)
            if val is not NullValue:
                matter_asserts.assert_valid_uint16(val, 'CurrentPositionLiftPercent100ths')
                asserts.assert_less_equal(val, 10000)

        self.step("16")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentPositionTiltPercent100ths):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentPositionTiltPercent100ths)
            if val is not NullValue:
                matter_asserts.assert_valid_uint16(val, 'CurrentPositionTiltPercent100ths')
                asserts.assert_less_equal(val, 10000)

        self.step("17")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.InstalledOpenLimitLift):
            self.InstalledOpenLimitLift = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.InstalledOpenLimitLift)
            matter_asserts.assert_valid_uint16(self.InstalledOpenLimitLift, 'InstalledOpenLimitLift')
            asserts.assert_less_equal(self.InstalledOpenLimitLift, 65534)

        self.step("18")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.InstalledClosedLimitLift):
            self.InstalledClosedLimitLift = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.InstalledClosedLimitLift)
            matter_asserts.assert_valid_uint16(self.InstalledClosedLimitLift, 'InstalledClosedLimitLift')
            asserts.assert_less_equal(self.InstalledClosedLimitLift, 65534)

        self.step("19")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.InstalledOpenLimitTilt):
            self.InstalledOpenLimitTilt = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.InstalledOpenLimitTilt)
            matter_asserts.assert_valid_uint16(self.InstalledOpenLimitTilt, 'InstalledOpenLimitTilt')
            asserts.assert_less_equal(self.InstalledOpenLimitTilt, 65534)

        self.step("20")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.InstalledClosedLimitTilt):
            self.InstalledClosedLimitTilt = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.InstalledClosedLimitTilt)
            matter_asserts.assert_valid_uint16(self.InstalledClosedLimitTilt, 'InstalledClosedLimitTilt')
            asserts.assert_less_equal(self.InstalledClosedLimitTilt, 65534)

        self.step("21")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Mode)
        matter_asserts.is_valid_int_value(val)
        # Check bitmap value less than or equal to (MotorDirectionReversed | CalibrationMode | MaintenanceMode | LedFeedback)
        asserts.assert_less_equal(val, 15)

        self.step("22")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SafetyStatus):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SafetyStatus)
            if val is not None:
                matter_asserts.is_valid_int_value(val)
                # Check bitmap value less than or equal to (RemoteLockout | TamperDetection | FailedCommunication | PositionFailure | ThermalProtection | ObstacleDetected | Power | StopInput | MotorJammed | HardwareFailure | ManualOperation | Protection)
                asserts.assert_less_equal(val, 4095)

if __name__ == "__main__":
    default_matter_test_main()
