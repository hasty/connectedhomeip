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

cluster = Clusters.AccessControl

class ACL_2_1(MatterBaseTest):

    def desc_ACL_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_ACL_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["ACL.S"]

    def steps_ACL_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read ACL attribute"),
            TestStep("2", "Read Extension attribute"),
            TestStep("3", "Read SubjectsPerAccessControlEntry attribute"),
            TestStep("4", "Read TargetsPerAccessControlEntry attribute"),
            TestStep("5", "Read AccessControlEntriesPerFabric attribute"),
            TestStep("6", "Read CommissioningARL attribute"),
            TestStep("7", "Read ARL attribute"),
        ]
        return steps

    SubjectsPerAccessControlEntry = None
    TargetsPerAccessControlEntry = None

    @run_if_endpoint_matches(has_cluster(Clusters.AccessControl))
    async def test_ACL_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ACL)
        matter_asserts.assert_list(val, "ACL attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "ACL attribute must contain AccessControlEntryStruct elements", cluster.Structs.AccessControlEntryStruct)
        for item in val:
            await self.test_checkAccessControlEntryStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Extension):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Extension)
            matter_asserts.assert_list(val, "Extension attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "Extension attribute must contain AccessControlExtensionStruct elements", cluster.Structs.AccessControlExtensionStruct)
            for item in val:
                await self.test_checkAccessControlExtensionStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("3")
        self.SubjectsPerAccessControlEntry = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SubjectsPerAccessControlEntry)
        matter_asserts.assert_valid_uint16(self.SubjectsPerAccessControlEntry, 'SubjectsPerAccessControlEntry')
        asserts.assert_greater_equal(self.SubjectsPerAccessControlEntry, 4)

        self.step("4")
        self.TargetsPerAccessControlEntry = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TargetsPerAccessControlEntry)
        matter_asserts.assert_valid_uint16(self.TargetsPerAccessControlEntry, 'TargetsPerAccessControlEntry')
        asserts.assert_greater_equal(self.TargetsPerAccessControlEntry, 3)

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AccessControlEntriesPerFabric)
        matter_asserts.assert_valid_uint16(val, 'AccessControlEntriesPerFabric')
        asserts.assert_greater_equal(val, 4)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CommissioningARL):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CommissioningARL)
            matter_asserts.assert_list(val, "CommissioningARL attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "CommissioningARL attribute must contain CommissioningAccessRestrictionEntryStruct elements", cluster.Structs.CommissioningAccessRestrictionEntryStruct)
            for item in val:
                await self.test_checkCommissioningAccessRestrictionEntryStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ARL):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ARL)
            matter_asserts.assert_list(val, "ARL attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "ARL attribute must contain AccessRestrictionEntryStruct elements", cluster.Structs.AccessRestrictionEntryStruct)
            for item in val:
                await self.test_checkAccessRestrictionEntryStruct(endpoint=endpoint, cluster=cluster, struct=item)

    async def test_checkAccessControlEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.AccessControl = None, 
                                 struct: Clusters.AccessControl.Structs.AccessControlEntryStruct = None):
        matter_asserts.assert_valid_enum(struct.privilege, "Privilege attribute must return a AccessControlEntryPrivilegeEnum", cluster.Enums.AccessControlEntryPrivilegeEnum)
        matter_asserts.assert_valid_enum(struct.authMode, "AuthMode attribute must return a AccessControlEntryAuthModeEnum", cluster.Enums.AccessControlEntryAuthModeEnum)
        if struct.subjects is not NullValue:
            matter_asserts.assert_list(struct.subjects, "Subjects attribute must return a list")
            matter_asserts.assert_list_element_type(struct.subjects,  "Subjects attribute must contain int elements", int)
            asserts.assert_less_equal(len(struct.subjects), self.SubjectsPerAccessControlEntry, "Subjects must have at most self.SubjectsPerAccessControlEntry entries!")
        if struct.targets is not NullValue:
            matter_asserts.assert_list(struct.targets, "Targets attribute must return a list")
            matter_asserts.assert_list_element_type(struct.targets,  "Targets attribute must contain AccessControlTargetStruct elements", cluster.Structs.AccessControlTargetStruct)
            for item in struct.targets:
                await self.test_checkAccessControlTargetStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_less_equal(len(struct.targets), self.TargetsPerAccessControlEntry, "Targets must have at most self.TargetsPerAccessControlEntry entries!")

    async def test_checkAccessControlExtensionStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.AccessControl = None, 
                                 struct: Clusters.AccessControl.Structs.AccessControlExtensionStruct = None):
        matter_asserts.assert_is_octstr(struct.data, "Data must be an octstr")
        asserts.assert_less_equal(len(struct.data), 128, "Data must have length at most 128!")

    async def test_checkAccessControlTargetStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.AccessControl = None, 
                                 struct: Clusters.AccessControl.Structs.AccessControlTargetStruct = None):
        if struct.cluster is not NullValue:
            matter_asserts.assert_valid_uint32(struct.cluster, 'Cluster must be uint32')
        if struct.endpoint is not NullValue:
            matter_asserts.assert_valid_uint16(struct.endpoint, 'Endpoint must be uint16')
        if struct.deviceType is not NullValue:
            matter_asserts.assert_valid_uint32(struct.deviceType, 'DeviceType must be uint32')

    async def test_checkAccessRestrictionEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.AccessControl = None, 
                                 struct: Clusters.AccessControl.Structs.AccessRestrictionEntryStruct = None):
        matter_asserts.assert_valid_uint16(struct.endpoint, 'Endpoint must be uint16')
        matter_asserts.assert_valid_uint32(struct.cluster, 'Cluster must be uint32')
        matter_asserts.assert_list(struct.restrictions, "Restrictions attribute must return a list")
        matter_asserts.assert_list_element_type(struct.restrictions,  "Restrictions attribute must contain AccessRestrictionStruct elements", cluster.Structs.AccessRestrictionStruct)
        for item in struct.restrictions:
            await self.test_checkAccessRestrictionStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_greater_equal(len(struct.restrictions), 1, "Restrictions must have at least 1 entries!")

    async def test_checkAccessRestrictionStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.AccessControl = None, 
                                 struct: Clusters.AccessControl.Structs.AccessRestrictionStruct = None):
        matter_asserts.assert_valid_enum(struct.type, "Type attribute must return a AccessRestrictionTypeEnum", cluster.Enums.AccessRestrictionTypeEnum)
        if struct.id is not NullValue:
            matter_asserts.assert_valid_uint32(struct.iD, 'ID')

    async def test_checkCommissioningAccessRestrictionEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.AccessControl = None, 
                                 struct: Clusters.AccessControl.Structs.CommissioningAccessRestrictionEntryStruct = None):
        matter_asserts.assert_valid_uint16(struct.endpoint, 'Endpoint must be uint16')
        matter_asserts.assert_valid_uint32(struct.cluster, 'Cluster must be uint32')
        matter_asserts.assert_list(struct.restrictions, "Restrictions attribute must return a list")
        matter_asserts.assert_list_element_type(struct.restrictions,  "Restrictions attribute must contain AccessRestrictionStruct elements", cluster.Structs.AccessRestrictionStruct)
        for item in struct.restrictions:
            await self.test_checkAccessRestrictionStruct(endpoint=endpoint, cluster=cluster, struct=item)
        asserts.assert_greater_equal(len(struct.restrictions), 1, "Restrictions must have at least 1 entries!")

if __name__ == "__main__":
    default_matter_test_main()
