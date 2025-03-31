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

cluster = Clusters.JointFabricDatastore

class JFDS_2_1(MatterBaseTest):

    def desc_JFDS_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_JFDS_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["JFDS"]

    def steps_JFDS_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read AnchorRootCA attribute"),
            TestStep("2", "Read AnchorNodeID attribute"),
            TestStep("3", "Read AnchorVendorID attribute"),
            TestStep("4", "Read FriendlyName attribute"),
            TestStep("5", "Read GroupKeySetList attribute"),
            TestStep("6", "Read GroupList attribute"),
            TestStep("7", "Read NodeList attribute"),
            TestStep("8", "Read AdminList attribute"),
            TestStep("9", "Read StatusEntry attribute"),
        ]

        return steps


    @async_test_body
    async def test_JFDS_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AnchorRootCA)
        matter_asserts.assert_is_octstr(val, "AnchorRootCA must be an octstr")

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AnchorNodeID)
        matter_asserts.assert_valid_uint64(val, 'AnchorNodeID must be uint64')

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AnchorVendorID)
        matter_asserts.assert_valid_uint16(val, 'AnchorVendorID must be uint16')

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.FriendlyName)
        matter_asserts.assert_is_string(val, "FriendlyName must be a string")
        asserts.assert_less_equal(len(val), 32, "FriendlyName must have length at most 32!")

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.GroupKeySetList)
        matter_asserts.assert_list(val, "GroupKeySetList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "GroupKeySetList attribute must contain Clusters.GroupKeyManagement.Structs.GroupKeySetStruct elements", Clusters.GroupKeyManagement.Structs.GroupKeySetStruct)
        for item in val:
            await self.test_checkGroupKeySetStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("6")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.GroupList)
        matter_asserts.assert_list(val, "GroupList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "GroupList attribute must contain Clusters.JointFabricDatastore.Structs.DatastoreGroupInformationEntryStruct elements", Clusters.JointFabricDatastore.Structs.DatastoreGroupInformationEntryStruct)
        for item in val:
            await self.test_checkDatastoreGroupInformationEntryStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("7")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NodeList)
        matter_asserts.assert_list(val, "NodeList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "NodeList attribute must contain Clusters.JointFabricDatastore.Structs.DatastoreNodeInformationEntryStruct elements", Clusters.JointFabricDatastore.Structs.DatastoreNodeInformationEntryStruct)
        for item in val:
            await self.test_checkDatastoreNodeInformationEntryStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("8")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AdminList)
        matter_asserts.assert_list(val, "AdminList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "AdminList attribute must contain Clusters.JointFabricDatastore.Structs.DatastoreAdministratorInformationEntryStruct elements", Clusters.JointFabricDatastore.Structs.DatastoreAdministratorInformationEntryStruct)
        for item in val:
            await self.test_checkDatastoreAdministratorInformationEntryStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("9")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.StatusEntry)
        asserts.assert_true(isinstance(val, Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct),
                                    f"val must be of type Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct")
        await self.test_checkDatastoreStatusEntryStruct(endpoint=endpoint, cluster=cluster, struct=val)


    async def test_checkAccessControlEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.AccessControl.Structs.AccessControlEntryStruct = None):
        matter_asserts.assert_valid_enum(struct.privilege, "Privilege attribute must return a Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum", Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum)
        matter_asserts.assert_valid_enum(struct.authMode, "AuthMode attribute must return a Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum", Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum)
        if struct.subjects is not NullValue:
            matter_asserts.assert_list(struct.subjects, "Subjects attribute must return a list")
            matter_asserts.assert_list_element_type(struct.subjects,  "Subjects attribute must contain int elements", int)
            asserts.assert_less_equal(len(struct.subjects), self.SubjectsPerAccessControlEntry, "Subjects must have at most self.SubjectsPerAccessControlEntry entries!")
        if struct.targets is not NullValue:
            matter_asserts.assert_list(struct.targets, "Targets attribute must return a list")
            matter_asserts.assert_list_element_type(struct.targets,  "Targets attribute must contain Clusters.AccessControl.Structs.AccessControlTargetStruct elements", Clusters.AccessControl.Structs.AccessControlTargetStruct)
            for item in struct.targets:
                await self.test_checkAccessControlTargetStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_less_equal(len(struct.targets), self.TargetsPerAccessControlEntry, "Targets must have at most self.TargetsPerAccessControlEntry entries!")

    async def test_checkAccessControlTargetStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.AccessControl.Structs.AccessControlTargetStruct = None):
        if struct.cluster is not NullValue:
            matter_asserts.assert_valid_uint32(struct.cluster, 'Cluster must be uint32')
        if struct.endpoint is not NullValue:
            matter_asserts.assert_valid_uint16(struct.endpoint, 'Endpoint must be uint16')
        if struct.deviceType is not NullValue:
            matter_asserts.assert_valid_uint32(struct.deviceType, 'DeviceType must be uint32')

    async def test_checkDatastoreACLEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.JointFabricDatastore.Structs.DatastoreACLEntryStruct = None):
        matter_asserts.assert_valid_uint16(struct.listID, 'ListID')
        asserts.assert_true(isinstance(struct.aclEntry, Clusters.AccessControl.Structs.AccessControlEntryStruct),
                                    f"struct.aclEntry must be of type Clusters.AccessControl.Structs.AccessControlEntryStruct")
        await self.test_checkAccessControlEntryStruct(endpoint=endpoint, cluster=cluster, struct=struct.aclEntry)
        asserts.assert_true(isinstance(struct.statusEntry, Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct),
                                    f"struct.statusEntry must be of type Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct")
        await self.test_checkDatastoreStatusEntryStruct(endpoint=endpoint, cluster=cluster, struct=struct.statusEntry)

    async def test_checkDatastoreAdministratorInformationEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.JointFabricDatastore.Structs.DatastoreAdministratorInformationEntryStruct = None):
        matter_asserts.assert_valid_uint64(struct.nodeID, 'NodeID must be uint64')
        matter_asserts.assert_is_string(struct.friendlyName, "FriendlyName must be a string")
        asserts.assert_less_equal(len(struct.friendlyName), 32, "FriendlyName must have length at most 32!")
        matter_asserts.assert_valid_uint16(struct.vendorID, 'VendorID must be uint16')
        matter_asserts.assert_is_octstr(struct.iCAC, "ICAC must be an octstr")
        asserts.assert_less_equal(len(struct.iCAC), 400, "ICAC must have length at most 400!")

    async def test_checkDatastoreBindingEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.JointFabricDatastore.Structs.DatastoreBindingEntryStruct = None):
        matter_asserts.assert_valid_uint16(struct.listID, 'ListID')
        asserts.assert_true(isinstance(struct.binding, Clusters.Binding.Structs.TargetStruct),
                                    f"struct.binding must be of type Clusters.Binding.Structs.TargetStruct")
        await self.test_checkTargetStruct(endpoint=endpoint, cluster=cluster, struct=struct.binding)
        asserts.assert_true(isinstance(struct.statusEntry, Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct),
                                    f"struct.statusEntry must be of type Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct")
        await self.test_checkDatastoreStatusEntryStruct(endpoint=endpoint, cluster=cluster, struct=struct.statusEntry)

    async def test_checkDatastoreEndpointEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.JointFabricDatastore.Structs.DatastoreEndpointEntryStruct = None):
        matter_asserts.assert_valid_uint16(struct.endpointID, 'EndpointID must be uint16')
        matter_asserts.assert_valid_uint64(struct.nodeID, 'NodeID must be uint64')
        matter_asserts.assert_is_string(struct.friendlyName, "FriendlyName must be a string")
        asserts.assert_less_equal(len(struct.friendlyName), 32, "FriendlyName must have length at most 32!")
        asserts.assert_true(isinstance(struct.statusEntry, Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct),
                                    f"struct.statusEntry must be of type Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct")
        await self.test_checkDatastoreStatusEntryStruct(endpoint=endpoint, cluster=cluster, struct=struct.statusEntry)
        matter_asserts.assert_list(struct.groupIdList, "GroupIDList attribute must return a list")
        matter_asserts.assert_list_element_type(struct.groupIdList,  "GroupIDList attribute must contain Clusters.JointFabricDatastore.Structs.DatastoreGroupIDEntryStruct elements", Clusters.JointFabricDatastore.Structs.DatastoreGroupIDEntryStruct)
        for item in struct.groupIdList:
            await self.test_checkDatastoreGroupIDEntryStruct(endpoint=endpoint, cluster=cluster, struct=item)
        matter_asserts.assert_list(struct.bindingList, "BindingList attribute must return a list")
        matter_asserts.assert_list_element_type(struct.bindingList,  "BindingList attribute must contain Clusters.JointFabricDatastore.Structs.DatastoreBindingEntryStruct elements", Clusters.JointFabricDatastore.Structs.DatastoreBindingEntryStruct)
        for item in struct.bindingList:
            await self.test_checkDatastoreBindingEntryStruct(endpoint=endpoint, cluster=cluster, struct=item)

    async def test_checkDatastoreGroupIDEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.JointFabricDatastore.Structs.DatastoreGroupIDEntryStruct = None):
        matter_asserts.assert_valid_uint16(struct.groupID, 'GroupID must be uint16')
        asserts.assert_true(isinstance(struct.statusEntry, Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct),
                                    f"struct.statusEntry must be of type Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct")
        await self.test_checkDatastoreStatusEntryStruct(endpoint=endpoint, cluster=cluster, struct=struct.statusEntry)

    async def test_checkDatastoreGroupInformationEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.JointFabricDatastore.Structs.DatastoreGroupInformationEntryStruct = None):
        matter_asserts.assert_valid_uint64(struct.groupID, 'GroupID')
        matter_asserts.assert_is_string(struct.friendlyName, "FriendlyName must be a string")
        asserts.assert_less_equal(len(struct.friendlyName), 32, "FriendlyName must have length at most 32!")
        matter_asserts.assert_valid_uint16(struct.groupKeySetID, 'GroupKeySetID')
        asserts.assert_greater_equal(struct.groupKeySetID, 1)
        asserts.assert_less_equal(struct.groupKeySetID, 65535)
        matter_asserts.assert_valid_uint16(struct.groupCAT, 'GroupCAT')
        asserts.assert_greater_equal(struct.groupCAT, 1)
        asserts.assert_less_equal(struct.groupCAT, 65535)
        matter_asserts.assert_valid_uint16(struct.groupCatVersion, 'GroupCATVersion')
        asserts.assert_greater_equal(struct.groupCatVersion, 1)
        asserts.assert_less_equal(struct.groupCatVersion, 65535)
        matter_asserts.assert_valid_enum(struct.groupPermission, "GroupPermission attribute must return a Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum", Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum)

    async def test_checkDatastoreNodeInformationEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.JointFabricDatastore.Structs.DatastoreNodeInformationEntryStruct = None):
        matter_asserts.assert_valid_uint64(struct.nodeID, 'NodeID must be uint64')
        matter_asserts.assert_is_string(struct.friendlyName, "FriendlyName must be a string")
        asserts.assert_less_equal(len(struct.friendlyName), 32, "FriendlyName must have length at most 32!")
        asserts.assert_true(isinstance(struct.commissioningStatusEntry, Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct),
                                    f"struct.commissioningStatusEntry must be of type Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct")
        await self.test_checkDatastoreStatusEntryStruct(endpoint=endpoint, cluster=cluster, struct=struct.commissioningStatusEntry)
        matter_asserts.assert_list(struct.nodeKeySetList, "NodeKeySetList attribute must return a list")
        matter_asserts.assert_list_element_type(struct.nodeKeySetList,  "NodeKeySetList attribute must contain Clusters.JointFabricDatastore.Structs.DatastoreNodeKeyEntryStruct elements", Clusters.JointFabricDatastore.Structs.DatastoreNodeKeyEntryStruct)
        for item in struct.nodeKeySetList:
            await self.test_checkDatastoreNodeKeyEntryStruct(endpoint=endpoint, cluster=cluster, struct=item)
        matter_asserts.assert_list(struct.aclList, "ACLList attribute must return a list")
        matter_asserts.assert_list_element_type(struct.aclList,  "ACLList attribute must contain Clusters.JointFabricDatastore.Structs.DatastoreACLEntryStruct elements", Clusters.JointFabricDatastore.Structs.DatastoreACLEntryStruct)
        for item in struct.aclList:
            await self.test_checkDatastoreACLEntryStruct(endpoint=endpoint, cluster=cluster, struct=item)
        matter_asserts.assert_list(struct.endpointList, "EndpointList attribute must return a list")
        matter_asserts.assert_list_element_type(struct.endpointList,  "EndpointList attribute must contain Clusters.JointFabricDatastore.Structs.DatastoreEndpointEntryStruct elements", Clusters.JointFabricDatastore.Structs.DatastoreEndpointEntryStruct)
        for item in struct.endpointList:
            await self.test_checkDatastoreEndpointEntryStruct(endpoint=endpoint, cluster=cluster, struct=item)

    async def test_checkDatastoreNodeKeyEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.JointFabricDatastore.Structs.DatastoreNodeKeyEntryStruct = None):
        matter_asserts.assert_valid_uint16(struct.groupKeySetID, 'GroupKeySetID')
        asserts.assert_true(isinstance(struct.statusEntry, Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct),
                                    f"struct.statusEntry must be of type Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct")
        await self.test_checkDatastoreStatusEntryStruct(endpoint=endpoint, cluster=cluster, struct=struct.statusEntry)

    async def test_checkDatastoreStatusEntryStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.JointFabricDatastore.Structs.DatastoreStatusEntryStruct = None):
        matter_asserts.assert_valid_enum(struct.state, "State attribute must return a Clusters.JointFabricDatastore.Enums.DatastoreStateEnum", Clusters.JointFabricDatastore.Enums.DatastoreStateEnum)
        matter_asserts.assert_valid_uint32(struct.updateTimestamp, 'UpdateTimestamp')
        matter_asserts.assert_valid_uint8(struct.failureCode, 'FailureCode must be uint8')

    async def test_checkGroupKeySetStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.GroupKeyManagement.Structs.GroupKeySetStruct = None):
        matter_asserts.assert_valid_uint16(struct.groupKeySetID, 'GroupKeySetID')
        matter_asserts.assert_valid_enum(struct.groupKeySecurityPolicy, "GroupKeySecurityPolicy attribute must return a Clusters.GroupKeyManagement.Enums.GroupKeySecurityPolicyEnum", Clusters.GroupKeyManagement.Enums.GroupKeySecurityPolicyEnum)
        if struct.epochKey0 is not NullValue:
            matter_asserts.assert_is_octstr(struct.epochKey0, "EpochKey0 must be an octstr")
        if struct.epochStartTime0 is not NullValue:
            matter_asserts.assert_valid_uint64(struct.epochStartTime0, 'EpochStartTime0')
        if struct.epochKey1 is not NullValue:
            matter_asserts.assert_is_octstr(struct.epochKey1, "EpochKey1 must be an octstr")
        if struct.epochStartTime1 is not NullValue:
            matter_asserts.assert_valid_uint64(struct.epochStartTime1, 'EpochStartTime1')
        if struct.epochKey2 is not NullValue:
            matter_asserts.assert_is_octstr(struct.epochKey2, "EpochKey2 must be an octstr")
        if struct.epochStartTime2 is not NullValue:
            matter_asserts.assert_valid_uint64(struct.epochStartTime2, 'EpochStartTime2')
        matter_asserts.assert_valid_enum(struct.groupKeyMulticastPolicy, "GroupKeyMulticastPolicy attribute must return a Clusters.GroupKeyManagement.Enums.GroupKeyMulticastPolicyEnum", Clusters.GroupKeyManagement.Enums.GroupKeyMulticastPolicyEnum)

    async def test_checkTargetStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.JointFabricDatastore = None, 
                                 struct: Clusters.Binding.Structs.TargetStruct = None):
        matter_asserts.assert_valid_uint64(struct.node, 'Node must be uint64')
        matter_asserts.assert_valid_uint16(struct.group, 'Group must be uint16')
        asserts.assert_greater_equal(struct.group, 1)
        matter_asserts.assert_valid_uint16(struct.endpoint, 'Endpoint must be uint16')
        if struct.cluster is not None:
            matter_asserts.assert_valid_uint32(struct.cluster, 'Cluster must be uint32')


if __name__ == "__main__":
    default_matter_test_main()
