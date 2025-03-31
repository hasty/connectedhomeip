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

cluster = Clusters.RVCOperationalState

class RVCOPSTATE_2_1(MatterBaseTest):

    def desc_RVCOPSTATE_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_RVCOPSTATE_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["RVCOPSTATE"]

    def steps_RVCOPSTATE_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read PhaseList attribute"),
            TestStep("2", "Read CurrentPhase attribute"),
            TestStep("3", "Read CountdownTime attribute"),
            TestStep("4", "Read OperationalStateList attribute"),
            TestStep("5", "Read OperationalState attribute"),
            TestStep("6", "Read OperationalError attribute"),
        ]

        return steps


    @async_test_body
    async def test_RVCOPSTATE_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PhaseList)
        if val is not NullValue:
            matter_asserts.assert_list(val, "PhaseList attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "PhaseList attribute must contain str elements", str)
            asserts.assert_less_equal(len(val), 32, "PhaseList must have at most 32 entries!")
            for val in val:
                asserts.assert_less_equal(len(val), 64, "PhaseList must have at most 64 entries!")

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentPhase)
        if val is not NullValue:
            matter_asserts.assert_valid_uint8(val, 'CurrentPhase')

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CountdownTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CountdownTime)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'CountdownTime')
                asserts.assert_less_equal(val, 259200)

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OperationalStateList)
        matter_asserts.assert_list(val, "OperationalStateList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "OperationalStateList attribute must contain Clusters.OperationalState.Structs.OperationalStateStruct elements", Clusters.OperationalState.Structs.OperationalStateStruct)
        for item in val:
            await self.test_checkOperationalStateStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OperationalState)
        matter_asserts.assert_valid_enum(val, "OperationalState attribute must return a Clusters.RVCOperationalState.Enums.OperationalStateEnum", Clusters.RVCOperationalState.Enums.OperationalStateEnum)

        self.step("6")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OperationalError)
        asserts.assert_true(isinstance(val, Clusters.OperationalState.Structs.ErrorStateStruct),
                                    f"val must be of type Clusters.OperationalState.Structs.ErrorStateStruct")
        await self.test_checkErrorStateStruct(endpoint=endpoint, cluster=cluster, struct=val)


    async def test_checkErrorStateStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.RVCOperationalState = None, 
                                 struct: Clusters.OperationalState.Structs.ErrorStateStruct = None):
        matter_asserts.assert_valid_enum(struct.errorStateID, "ErrorStateID attribute must return a Clusters.OperationalState.Enums.ErrorStateEnum", Clusters.OperationalState.Enums.ErrorStateEnum)
        matter_asserts.assert_is_string(struct.errorStateLabel, "ErrorStateLabel must be a string")
        asserts.assert_less_equal(len(struct.errorStateLabel), 64, "ErrorStateLabel must have length at most 64!")
        if struct.errorStateDetails is not None:
            matter_asserts.assert_is_string(struct.errorStateDetails, "ErrorStateDetails must be a string")
            asserts.assert_less_equal(len(struct.errorStateDetails), 64, "ErrorStateDetails must have length at most 64!")

    async def test_checkOperationalStateStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.RVCOperationalState = None, 
                                 struct: Clusters.OperationalState.Structs.OperationalStateStruct = None):
        matter_asserts.assert_valid_enum(struct.operationalStateID, "OperationalStateID attribute must return a Clusters.OperationalState.Enums.OperationalStateEnum", Clusters.OperationalState.Enums.OperationalStateEnum)
        matter_asserts.assert_is_string(struct.operationalStateLabel, "OperationalStateLabel must be a string")
        asserts.assert_less_equal(len(struct.operationalStateLabel), 64, "OperationalStateLabel must have length at most 64!")


if __name__ == "__main__":
    default_matter_test_main()
