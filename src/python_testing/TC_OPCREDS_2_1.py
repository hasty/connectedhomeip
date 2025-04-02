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

cluster = Clusters.OperationalCredentials

class OPCREDS_2_1(MatterBaseTest):

    def desc_OPCREDS_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_OPCREDS_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["OPCREDS"]

    def steps_OPCREDS_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read NOCs attribute"),
            TestStep("2", "Read Fabrics attribute"),
            TestStep("3", "Read SupportedFabrics attribute"),
            TestStep("4", "Read CommissionedFabrics attribute"),
            TestStep("5", "Read TrustedRootCertificates attribute"),
            TestStep("6", "Read CurrentFabricIndex attribute"),
        ]
        return steps

    SupportedFabrics = None

    @async_test_body
    async def test_OPCREDS_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NOCs)
        matter_asserts.assert_list(val, "NOCs attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "NOCs attribute must contain NOCStruct elements", cluster.Structs.NOCStruct)
        for item in val:
            await self.test_checkNOCStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(val), self.SupportedFabrics, "NOCs must have at most self.SupportedFabrics entries!")

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Fabrics)
        matter_asserts.assert_list(val, "Fabrics attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "Fabrics attribute must contain FabricDescriptorStruct elements", cluster.Structs.FabricDescriptorStruct)
        for item in val:
            await self.test_checkFabricDescriptorStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_less_equal(len(val), self.SupportedFabrics, "Fabrics must have at most self.SupportedFabrics entries!")

        self.step("3")
        self.SupportedFabrics = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportedFabrics)
        matter_asserts.assert_valid_uint8(self.SupportedFabrics, 'SupportedFabrics')
        asserts.assert_greater_equal(self.SupportedFabrics, 5)
        asserts.assert_less_equal(self.SupportedFabrics, 254)

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CommissionedFabrics)
        matter_asserts.assert_valid_uint8(val, 'CommissionedFabrics')
        asserts.assert_less_equal(val, self.SupportedFabrics)

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TrustedRootCertificates)
        matter_asserts.assert_list(val, "TrustedRootCertificates attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "TrustedRootCertificates attribute must contain bytes elements", bytes)
        asserts.assert_less_equal(len(val), self.SupportedFabrics, "TrustedRootCertificates must have at most self.SupportedFabrics entries!")
        for val in val:
            asserts.assert_less_equal(len(val), 400, "TrustedRootCertificates must have at most 400 entries!")

        self.step("6")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentFabricIndex)
        matter_asserts.assert_valid_uint8(val, 'CurrentFabricIndex')

    async def test_checkFabricDescriptorStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.OperationalCredentials = None, 
                                 struct: Clusters.OperationalCredentials.Structs.FabricDescriptorStruct = None):
        matter_asserts.assert_is_octstr(struct.rootPublicKey, "RootPublicKey must be an octstr")
        matter_asserts.assert_valid_uint16(struct.vendorID, 'VendorID must be uint16')
        matter_asserts.assert_valid_uint64(struct.fabricID, 'FabricID must be uint64')
        matter_asserts.assert_valid_uint64(struct.nodeID, 'NodeID must be uint64')
        matter_asserts.assert_is_string(struct.label, "Label must be a string")
        asserts.assert_less_equal(len(struct.label), 32, "Label must have length at most 32!")
        if struct.vidverificationStatement is not None:
            matter_asserts.assert_is_octstr(struct.vidVerificationStatement, "VIDVerificationStatement must be an octstr")

    async def test_checkNOCStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.OperationalCredentials = None, 
                                 struct: Clusters.OperationalCredentials.Structs.NOCStruct = None):
        matter_asserts.assert_is_octstr(struct.nOC, "NOC must be an octstr")
        asserts.assert_less_equal(len(struct.nOC), 400, "NOC must have length at most 400!")
        if struct.icac is not NullValue:
            matter_asserts.assert_is_octstr(struct.iCAC, "ICAC must be an octstr")
            asserts.assert_less_equal(len(struct.iCAC), 400, "ICAC must have length at most 400!")
        if struct.vvsc is not None:
            matter_asserts.assert_is_octstr(struct.vVSC, "VVSC must be an octstr")
            asserts.assert_less_equal(len(struct.vVSC), 400, "VVSC must have length at most 400!")

if __name__ == "__main__":
    default_matter_test_main()
