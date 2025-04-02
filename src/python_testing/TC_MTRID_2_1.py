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

cluster = Clusters.MeterIdentification

class MTRID_2_1(MatterBaseTest):

    def desc_MTRID_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_MTRID_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["MTRID"]

    def steps_MTRID_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read MeterType attribute"),
            TestStep("2", "Read PointOfDelivery attribute"),
            TestStep("3", "Read MeterSerialNumber attribute"),
            TestStep("4", "Read ProtocolVersion attribute"),
            TestStep("5", "Read PowerThreshold attribute"),
        ]

        return steps


    @async_test_body
    async def test_MTRID_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MeterType)
        if val is not NullValue:
            matter_asserts.assert_valid_enum(val, "MeterType attribute must return a Clusters.MeterIdentification.Enums.MeterTypeEnum", Clusters.MeterIdentification.Enums.MeterTypeEnum)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PointOfDelivery)
        if val is not NullValue:
            matter_asserts.assert_is_string(val, "PointOfDelivery must be a string")
            asserts.assert_less_equal(len(val), 64, "PointOfDelivery must have length at most 64!")

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MeterSerialNumber)
        if val is not NullValue:
            matter_asserts.assert_is_string(val, "MeterSerialNumber must be a string")
            asserts.assert_less_equal(len(val), 64, "MeterSerialNumber must have length at most 64!")

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ProtocolVersion):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ProtocolVersion)
            if val is not NullValue and val is not None:
                matter_asserts.assert_is_string(val, "ProtocolVersion must be a string")
                asserts.assert_less_equal(len(val), 64, "ProtocolVersion must have length at most 64!")

        self.step("5")
        if await self.feature_guard(endpoint=endpoint, cluster=cluster, feature_int=cluster.Bitmaps.Feature.kPowerThreshold):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PowerThreshold)
            if val is not NullValue:
                asserts.assert_true(isinstance(val, Globals.Structs.PowerThresholdStruct),
                                            f"val must be of type Globals.Structs.PowerThresholdStruct")
                await self.test_checkPowerThresholdStruct(endpoint=endpoint, cluster=cluster, struct=val)


    async def test_checkPowerThresholdStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.MeterIdentification = None, 
                                 struct: Globals.Structs.PowerThresholdStruct = None):
        if struct.powerThreshold is not None:
            matter_asserts.assert_valid_int64(struct.powerThreshold, 'PowerThreshold')
        if struct.apparentPowerThreshold is not None:
            matter_asserts.assert_valid_int64(struct.apparentPowerThreshold, 'ApparentPowerThreshold')
        if struct.powerThresholdSource is not NullValue:
            matter_asserts.assert_valid_enum(struct.powerThresholdSource, "PowerThresholdSource attribute must return a Globals.Enums.PowerThresholdSourceEnum", Globals.Enums.PowerThresholdSourceEnum)


if __name__ == "__main__":
    default_matter_test_main()
