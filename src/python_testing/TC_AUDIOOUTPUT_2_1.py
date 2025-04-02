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

cluster = Clusters.AudioOutput

class AUDIOOUTPUT_2_1(MatterBaseTest):

    def desc_AUDIOOUTPUT_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_AUDIOOUTPUT_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["AUDIOOUTPUT"]

    def steps_AUDIOOUTPUT_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read OutputList attribute"),
            TestStep("2", "Read CurrentOutput attribute"),
        ]
        return steps


    @async_test_body
    async def test_AUDIOOUTPUT_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OutputList)
        matter_asserts.assert_list(val, "OutputList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "OutputList attribute must contain OutputInfoStruct elements", cluster.Structs.OutputInfoStruct)
        for item in val:
            await self.test_checkOutputInfoStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentOutput)
        matter_asserts.assert_valid_uint8(val, 'CurrentOutput')

    async def test_checkOutputInfoStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.AudioOutput = None, 
                                 struct: Clusters.AudioOutput.Structs.OutputInfoStruct = None):
        matter_asserts.assert_valid_uint8(struct.index, 'Index')
        matter_asserts.assert_valid_enum(struct.outputType, "OutputType attribute must return a OutputTypeEnum", cluster.Enums.OutputTypeEnum)
        matter_asserts.assert_is_string(struct.name, "Name must be a string")

if __name__ == "__main__":
    default_matter_test_main()
