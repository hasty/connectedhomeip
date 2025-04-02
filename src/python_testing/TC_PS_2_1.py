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

cluster = Clusters.PowerSource

class PS_2_1(MatterBaseTest):

    def desc_PS_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_PS_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["PS.S"]

    def steps_PS_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read Status attribute"),
            TestStep("2", "Read Order attribute"),
            TestStep("3", "Read Description attribute"),
            TestStep("4", "Read WiredAssessedInputVoltage attribute"),
            TestStep("5", "Read WiredAssessedInputFrequency attribute"),
            TestStep("6", "Read WiredCurrentType attribute"),
            TestStep("7", "Read WiredAssessedCurrent attribute"),
            TestStep("8", "Read WiredNominalVoltage attribute"),
            TestStep("9", "Read WiredMaximumCurrent attribute"),
            TestStep("10", "Read WiredPresent attribute"),
            TestStep("11", "Read ActiveWiredFaults attribute"),
            TestStep("12", "Read BatVoltage attribute"),
            TestStep("13", "Read BatPercentRemaining attribute"),
            TestStep("14", "Read BatTimeRemaining attribute"),
            TestStep("15", "Read BatChargeLevel attribute"),
            TestStep("16", "Read BatReplacementNeeded attribute"),
            TestStep("17", "Read BatReplaceability attribute"),
            TestStep("18", "Read BatPresent attribute"),
            TestStep("19", "Read ActiveBatFaults attribute"),
            TestStep("20", "Read BatReplacementDescription attribute"),
            TestStep("21", "Read BatCommonDesignation attribute"),
            TestStep("22", "Read BatANSIDesignation attribute"),
            TestStep("23", "Read BatIECDesignation attribute"),
            TestStep("24", "Read BatApprovedChemistry attribute"),
            TestStep("25", "Read BatCapacity attribute"),
            TestStep("26", "Read BatQuantity attribute"),
            TestStep("27", "Read BatChargeState attribute"),
            TestStep("28", "Read BatTimeToFullCharge attribute"),
            TestStep("29", "Read BatFunctionalWhileCharging attribute"),
            TestStep("30", "Read BatChargingCurrent attribute"),
            TestStep("31", "Read ActiveBatChargeFaults attribute"),
            TestStep("32", "Read EndpointList attribute"),
        ]
        return steps


    @async_test_body
    async def test_PS_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Status)
        matter_asserts.assert_valid_enum(val, "Status attribute must return a PowerSourceStatusEnum", cluster.Enums.PowerSourceStatusEnum)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Order)
        matter_asserts.assert_valid_uint8(val, 'Order')

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Description)
        matter_asserts.assert_is_string(val, "Description must be a string")
        asserts.assert_less_equal(len(val), 60, "Description must have length at most 60!")

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WiredAssessedInputVoltage):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WiredAssessedInputVoltage)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'WiredAssessedInputVoltage')

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WiredAssessedInputFrequency):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WiredAssessedInputFrequency)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint16(val, 'WiredAssessedInputFrequency')

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WiredCurrentType):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WiredCurrentType)
            matter_asserts.assert_valid_enum(val, "WiredCurrentType attribute must return a WiredCurrentTypeEnum", cluster.Enums.WiredCurrentTypeEnum)

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WiredAssessedCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WiredAssessedCurrent)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'WiredAssessedCurrent')

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WiredNominalVoltage):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WiredNominalVoltage)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'WiredNominalVoltage')

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WiredMaximumCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WiredMaximumCurrent)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'WiredMaximumCurrent')

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WiredPresent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WiredPresent)
            if val is not None:
                matter_asserts.assert_valid_bool(val, 'WiredPresent')

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveWiredFaults):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveWiredFaults)
            if val is not None:
                matter_asserts.assert_list(val, "ActiveWiredFaults attribute must return a list")
                matter_asserts.assert_list_element_type(val,  "ActiveWiredFaults attribute must contain WiredFaultEnum elements", cluster.Enums.WiredFaultEnum)
                asserts.assert_less_equal(len(val), 8, "ActiveWiredFaults must have at most 8 entries!")

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatVoltage):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatVoltage)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'BatVoltage')

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatPercentRemaining):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatPercentRemaining)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'BatPercentRemaining')
                asserts.assert_less_equal(val, 200)

        self.step("14")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatTimeRemaining):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatTimeRemaining)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'BatTimeRemaining')

        self.step("15")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatChargeLevel):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatChargeLevel)
            matter_asserts.assert_valid_enum(val, "BatChargeLevel attribute must return a BatChargeLevelEnum", cluster.Enums.BatChargeLevelEnum)

        self.step("16")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatReplacementNeeded):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatReplacementNeeded)
            matter_asserts.assert_valid_bool(val, 'BatReplacementNeeded')

        self.step("17")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatReplaceability):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatReplaceability)
            matter_asserts.assert_valid_enum(val, "BatReplaceability attribute must return a BatReplaceabilityEnum", cluster.Enums.BatReplaceabilityEnum)

        self.step("18")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatPresent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatPresent)
            if val is not None:
                matter_asserts.assert_valid_bool(val, 'BatPresent')

        self.step("19")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveBatFaults):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveBatFaults)
            if val is not None:
                matter_asserts.assert_list(val, "ActiveBatFaults attribute must return a list")
                matter_asserts.assert_list_element_type(val,  "ActiveBatFaults attribute must contain BatFaultEnum elements", cluster.Enums.BatFaultEnum)
                asserts.assert_less_equal(len(val), 8, "ActiveBatFaults must have at most 8 entries!")

        self.step("20")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatReplacementDescription):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatReplacementDescription)
            matter_asserts.assert_is_string(val, "BatReplacementDescription must be a string")
            asserts.assert_less_equal(len(val), 60, "BatReplacementDescription must have length at most 60!")

        self.step("21")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatCommonDesignation):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatCommonDesignation)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "BatCommonDesignation attribute must return a BatCommonDesignationEnum", cluster.Enums.BatCommonDesignationEnum)

        self.step("22")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatANSIDesignation):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatANSIDesignation)
            if val is not None:
                matter_asserts.assert_is_string(val, "BatANSIDesignation must be a string")
                asserts.assert_less_equal(len(val), 20, "BatANSIDesignation must have length at most 20!")

        self.step("23")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatIECDesignation):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatIECDesignation)
            if val is not None:
                matter_asserts.assert_is_string(val, "BatIECDesignation must be a string")
                asserts.assert_less_equal(len(val), 20, "BatIECDesignation must have length at most 20!")

        self.step("24")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatApprovedChemistry):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatApprovedChemistry)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "BatApprovedChemistry attribute must return a BatApprovedChemistryEnum", cluster.Enums.BatApprovedChemistryEnum)

        self.step("25")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatCapacity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatCapacity)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'BatCapacity')

        self.step("26")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatQuantity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatQuantity)
            matter_asserts.assert_valid_uint8(val, 'BatQuantity')

        self.step("27")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatChargeState):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatChargeState)
            matter_asserts.assert_valid_enum(val, "BatChargeState attribute must return a BatChargeStateEnum", cluster.Enums.BatChargeStateEnum)

        self.step("28")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatTimeToFullCharge):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatTimeToFullCharge)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'BatTimeToFullCharge')

        self.step("29")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatFunctionalWhileCharging):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatFunctionalWhileCharging)
            matter_asserts.assert_valid_bool(val, 'BatFunctionalWhileCharging')

        self.step("30")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BatChargingCurrent):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BatChargingCurrent)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'BatChargingCurrent')

        self.step("31")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveBatChargeFaults):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveBatChargeFaults)
            if val is not None:
                matter_asserts.assert_list(val, "ActiveBatChargeFaults attribute must return a list")
                matter_asserts.assert_list_element_type(val,  "ActiveBatChargeFaults attribute must contain BatChargeFaultEnum elements", cluster.Enums.BatChargeFaultEnum)
                asserts.assert_less_equal(len(val), 16, "ActiveBatChargeFaults must have at most 16 entries!")

        self.step("32")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EndpointList)
        matter_asserts.assert_list(val, "EndpointList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "EndpointList attribute must contain int elements", int)

if __name__ == "__main__":
    default_matter_test_main()
