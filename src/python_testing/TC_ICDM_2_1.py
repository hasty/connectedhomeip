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

cluster = Clusters.ICDManagement

class ICDM_2_1(MatterBaseTest):

    def desc_ICDM_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_ICDM_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["ICDM"]

    def steps_ICDM_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read IdleModeDuration attribute"),
            TestStep("2", "Read ActiveModeDuration attribute"),
            TestStep("3", "Read ActiveModeThreshold attribute"),
            TestStep("4", "Read RegisteredClients attribute"),
            TestStep("5", "Read ICDCounter attribute"),
            TestStep("6", "Read ClientsSupportedPerFabric attribute"),
            TestStep("7", "Read UserActiveModeTriggerHint attribute"),
            TestStep("8", "Read UserActiveModeTriggerInstruction attribute"),
            TestStep("9", "Read OperatingMode attribute"),
            TestStep("10", "Read MaximumCheckInBackoff attribute"),
        ]

        return steps

    IdleModeDuration = None

    @async_test_body
    async def test_ICDM_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        self.IdleModeDuration = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.IdleModeDuration)
        matter_asserts.assert_valid_uint32(self.IdleModeDuration, 'IdleModeDuration')
        asserts.assert_greater_equal(self.IdleModeDuration, 1)
        asserts.assert_less_equal(self.IdleModeDuration, 64800)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveModeDuration)
        matter_asserts.assert_valid_uint32(val, 'ActiveModeDuration')

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveModeThreshold)
        matter_asserts.assert_valid_uint16(val, 'ActiveModeThreshold')

        self.step("4")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kCheckInProtocolSupport):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RegisteredClients)
            matter_asserts.assert_list(val, "RegisteredClients attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "RegisteredClients attribute must contain Clusters.ICDManagement.Structs.MonitoringRegistrationStruct elements", Clusters.ICDManagement.Structs.MonitoringRegistrationStruct)
            for item in val:
                await self.test_checkMonitoringRegistrationStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("5")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kCheckInProtocolSupport):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ICDCounter)
            matter_asserts.assert_valid_uint32(val, 'ICDCounter')

        self.step("6")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kCheckInProtocolSupport):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ClientsSupportedPerFabric)
            matter_asserts.assert_valid_uint16(val, 'ClientsSupportedPerFabric')
            asserts.assert_greater_equal(val, 1)

        self.step("7")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kUserActiveModeTrigger):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UserActiveModeTriggerHint)
            matter_asserts.is_valid_int_value(val)

        self.step("8")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UserActiveModeTriggerInstruction)
        if val is not None:
            matter_asserts.assert_is_string(val, "UserActiveModeTriggerInstruction must be a string")
            asserts.assert_less_equal(len(val), 128, "UserActiveModeTriggerInstruction must have length at most 128!")

        self.step("9")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kLongIdleTimeSupport):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OperatingMode)
            matter_asserts.assert_valid_enum(val, "OperatingMode attribute must return a Clusters.ICDManagement.Enums.OperatingModeEnum", Clusters.ICDManagement.Enums.OperatingModeEnum)

        self.step("10")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kCheckInProtocolSupport):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaximumCheckInBackoff)
            matter_asserts.assert_valid_uint32(val, 'MaximumCheckInBackoff')
            asserts.assert_greater_equal(val, self.IdleModeDuration)
            asserts.assert_less_equal(val, 64800)


    async def test_checkMonitoringRegistrationStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ICDManagement = None, 
                                 struct: Clusters.ICDManagement.Structs.MonitoringRegistrationStruct = None):
        matter_asserts.assert_valid_uint64(struct.checkInNodeID, 'CheckInNodeID must be uint64')
        matter_asserts.assert_valid_uint64(struct.monitoredSubject, 'MonitoredSubject must be uint64')
        matter_asserts.assert_valid_enum(struct.clientType, "ClientType attribute must return a Clusters.ICDManagement.Enums.ClientTypeEnum", Clusters.ICDManagement.Enums.ClientTypeEnum)


if __name__ == "__main__":
    default_matter_test_main()
