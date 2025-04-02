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

cluster = Clusters.ThreadNetworkDiagnostics

class DGTHREAD_2_1(MatterBaseTest):

    def desc_DGTHREAD_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_DGTHREAD_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["DGTHREAD.S"]

    def steps_DGTHREAD_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read Channel attribute"),
            TestStep("2", "Read RoutingRole attribute"),
            TestStep("3", "Read NetworkName attribute"),
            TestStep("4", "Read PanId attribute"),
            TestStep("5", "Read ExtendedPanId attribute"),
            TestStep("6", "Read MeshLocalPrefix attribute"),
            TestStep("7", "Read OverrunCount attribute"),
            TestStep("8", "Read NeighborTable attribute"),
            TestStep("9", "Read RouteTable attribute"),
            TestStep("10", "Read PartitionId attribute"),
            TestStep("11", "Read Weighting attribute"),
            TestStep("12", "Read DataVersion attribute"),
            TestStep("13", "Read StableDataVersion attribute"),
            TestStep("14", "Read LeaderRouterId attribute"),
            TestStep("15", "Read DetachedRoleCount attribute"),
            TestStep("16", "Read ChildRoleCount attribute"),
            TestStep("17", "Read RouterRoleCount attribute"),
            TestStep("18", "Read LeaderRoleCount attribute"),
            TestStep("19", "Read AttachAttemptCount attribute"),
            TestStep("20", "Read PartitionIdChangeCount attribute"),
            TestStep("21", "Read BetterPartitionAttachAttemptCount attribute"),
            TestStep("22", "Read ParentChangeCount attribute"),
            TestStep("23", "Read TxTotalCount attribute"),
            TestStep("24", "Read TxUnicastCount attribute"),
            TestStep("25", "Read TxBroadcastCount attribute"),
            TestStep("26", "Read TxAckRequestedCount attribute"),
            TestStep("27", "Read TxAckedCount attribute"),
            TestStep("28", "Read TxNoAckRequestedCount attribute"),
            TestStep("29", "Read TxDataCount attribute"),
            TestStep("30", "Read TxDataPollCount attribute"),
            TestStep("31", "Read TxBeaconCount attribute"),
            TestStep("32", "Read TxBeaconRequestCount attribute"),
            TestStep("33", "Read TxOtherCount attribute"),
            TestStep("34", "Read TxRetryCount attribute"),
            TestStep("35", "Read TxDirectMaxRetryExpiryCount attribute"),
            TestStep("36", "Read TxIndirectMaxRetryExpiryCount attribute"),
            TestStep("37", "Read TxErrCcaCount attribute"),
            TestStep("38", "Read TxErrAbortCount attribute"),
            TestStep("39", "Read TxErrBusyChannelCount attribute"),
            TestStep("40", "Read RxTotalCount attribute"),
            TestStep("41", "Read RxUnicastCount attribute"),
            TestStep("42", "Read RxBroadcastCount attribute"),
            TestStep("43", "Read RxDataCount attribute"),
            TestStep("44", "Read RxDataPollCount attribute"),
            TestStep("45", "Read RxBeaconCount attribute"),
            TestStep("46", "Read RxBeaconRequestCount attribute"),
            TestStep("47", "Read RxOtherCount attribute"),
            TestStep("48", "Read RxAddressFilteredCount attribute"),
            TestStep("49", "Read RxDestAddrFilteredCount attribute"),
            TestStep("50", "Read RxDuplicatedCount attribute"),
            TestStep("51", "Read RxErrNoFrameCount attribute"),
            TestStep("52", "Read RxErrUnknownNeighborCount attribute"),
            TestStep("53", "Read RxErrInvalidSrcAddrCount attribute"),
            TestStep("54", "Read RxErrSecCount attribute"),
            TestStep("55", "Read RxErrFcsCount attribute"),
            TestStep("56", "Read RxErrOtherCount attribute"),
            TestStep("57", "Read ActiveTimestamp attribute"),
            TestStep("58", "Read PendingTimestamp attribute"),
            TestStep("59", "Read Delay attribute"),
            TestStep("60", "Read SecurityPolicy attribute"),
            TestStep("61", "Read ChannelPage0Mask attribute"),
            TestStep("62", "Read OperationalDatasetComponents attribute"),
            TestStep("63", "Read ActiveNetworkFaultsList attribute"),
            TestStep("64", "Read ExtAddress attribute"),
            TestStep("65", "Read Rloc16 attribute"),
        ]
        return steps


    @run_if_endpoint_matches(has_cluster(Clusters.ThreadNetworkDiagnostics))
    async def test_DGTHREAD_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Channel)
        if val is not NullValue:
            matter_asserts.assert_valid_uint16(val, 'Channel')

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RoutingRole)
        if val is not NullValue:
            matter_asserts.assert_valid_enum(val, "RoutingRole attribute must return a RoutingRoleEnum", cluster.Enums.RoutingRoleEnum)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NetworkName)
        if val is not NullValue:
            matter_asserts.assert_is_string(val, "NetworkName must be a string")
            asserts.assert_less_equal(len(val), 16, "NetworkName must have length at most 16!")

        self.step("4")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PanId)
        if val is not NullValue:
            matter_asserts.assert_valid_uint16(val, 'PanId')

        self.step("5")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ExtendedPanId)
        if val is not NullValue:
            matter_asserts.assert_valid_uint64(val, 'ExtendedPanId')

        self.step("6")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MeshLocalPrefix)
        if val is not NullValue:
            asserts.assert_true(isinstance(val, bytes), "MeshLocalPrefix must be of type bytes")
            matter_asserts.assert_int_in_range(len(val), 1, 17, "MeshLocalPrefix must have a length of between 1 and 17")

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OverrunCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OverrunCount)
            matter_asserts.assert_valid_uint64(val, 'OverrunCount')

        self.step("8")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NeighborTable)
        matter_asserts.assert_list(val, "NeighborTable attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "NeighborTable attribute must contain NeighborTableStruct elements", cluster.Structs.NeighborTableStruct)
        for item in val:
            await self.test_checkNeighborTableStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("9")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RouteTable)
        matter_asserts.assert_list(val, "RouteTable attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "RouteTable attribute must contain RouteTableStruct elements", cluster.Structs.RouteTableStruct)
        for item in val:
            await self.test_checkRouteTableStruct(endpoint=endpoint, cluster=cluster, struct=item)

        self.step("10")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PartitionId)
        if val is not NullValue:
            matter_asserts.assert_valid_uint32(val, 'PartitionId')

        self.step("11")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Weighting)
        if val is not NullValue:
            matter_asserts.assert_valid_uint16(val, 'Weighting')
            asserts.assert_less_equal(val, 255)

        self.step("12")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DataVersion)
        if val is not NullValue:
            matter_asserts.assert_valid_uint16(val, 'DataVersion')
            asserts.assert_less_equal(val, 255)

        self.step("13")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.StableDataVersion)
        if val is not NullValue:
            matter_asserts.assert_valid_uint16(val, 'StableDataVersion')
            asserts.assert_less_equal(val, 255)

        self.step("14")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LeaderRouterId)
        if val is not NullValue:
            matter_asserts.assert_valid_uint8(val, 'LeaderRouterId')
            asserts.assert_less_equal(val, 62)

        self.step("15")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DetachedRoleCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DetachedRoleCount)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'DetachedRoleCount')

        self.step("16")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ChildRoleCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ChildRoleCount)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ChildRoleCount')

        self.step("17")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RouterRoleCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RouterRoleCount)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'RouterRoleCount')

        self.step("18")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.LeaderRoleCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LeaderRoleCount)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'LeaderRoleCount')

        self.step("19")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AttachAttemptCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AttachAttemptCount)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'AttachAttemptCount')

        self.step("20")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PartitionIdChangeCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PartitionIdChangeCount)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'PartitionIdChangeCount')

        self.step("21")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.BetterPartitionAttachAttemptCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.BetterPartitionAttachAttemptCount)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'BetterPartitionAttachAttemptCount')

        self.step("22")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ParentChangeCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ParentChangeCount)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ParentChangeCount')

        self.step("23")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxTotalCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxTotalCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxTotalCount')

        self.step("24")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxUnicastCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxUnicastCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxUnicastCount')

        self.step("25")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxBroadcastCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxBroadcastCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxBroadcastCount')

        self.step("26")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxAckRequestedCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxAckRequestedCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxAckRequestedCount')

        self.step("27")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxAckedCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxAckedCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxAckedCount')

        self.step("28")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxNoAckRequestedCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxNoAckRequestedCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxNoAckRequestedCount')

        self.step("29")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxDataCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxDataCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxDataCount')

        self.step("30")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxDataPollCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxDataPollCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxDataPollCount')

        self.step("31")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxBeaconCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxBeaconCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxBeaconCount')

        self.step("32")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxBeaconRequestCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxBeaconRequestCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxBeaconRequestCount')

        self.step("33")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxOtherCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxOtherCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxOtherCount')

        self.step("34")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxRetryCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxRetryCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxRetryCount')

        self.step("35")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxDirectMaxRetryExpiryCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxDirectMaxRetryExpiryCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxDirectMaxRetryExpiryCount')

        self.step("36")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxIndirectMaxRetryExpiryCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxIndirectMaxRetryExpiryCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxIndirectMaxRetryExpiryCount')

        self.step("37")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxErrCcaCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxErrCcaCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxErrCcaCount')

        self.step("38")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxErrAbortCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxErrAbortCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxErrAbortCount')

        self.step("39")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.TxErrBusyChannelCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TxErrBusyChannelCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'TxErrBusyChannelCount')

        self.step("40")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxTotalCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxTotalCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxTotalCount')

        self.step("41")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxUnicastCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxUnicastCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxUnicastCount')

        self.step("42")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxBroadcastCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxBroadcastCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxBroadcastCount')

        self.step("43")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxDataCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxDataCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxDataCount')

        self.step("44")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxDataPollCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxDataPollCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxDataPollCount')

        self.step("45")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxBeaconCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxBeaconCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxBeaconCount')

        self.step("46")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxBeaconRequestCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxBeaconRequestCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxBeaconRequestCount')

        self.step("47")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxOtherCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxOtherCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxOtherCount')

        self.step("48")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxAddressFilteredCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxAddressFilteredCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxAddressFilteredCount')

        self.step("49")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxDestAddrFilteredCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxDestAddrFilteredCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxDestAddrFilteredCount')

        self.step("50")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxDuplicatedCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxDuplicatedCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxDuplicatedCount')

        self.step("51")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxErrNoFrameCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxErrNoFrameCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxErrNoFrameCount')

        self.step("52")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxErrUnknownNeighborCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxErrUnknownNeighborCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxErrUnknownNeighborCount')

        self.step("53")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxErrInvalidSrcAddrCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxErrInvalidSrcAddrCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxErrInvalidSrcAddrCount')

        self.step("54")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxErrSecCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxErrSecCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxErrSecCount')

        self.step("55")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxErrFcsCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxErrFcsCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxErrFcsCount')

        self.step("56")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RxErrOtherCount):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RxErrOtherCount)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'RxErrOtherCount')

        self.step("57")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ActiveTimestamp):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveTimestamp)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint64(val, 'ActiveTimestamp')

        self.step("58")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PendingTimestamp):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PendingTimestamp)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint64(val, 'PendingTimestamp')

        self.step("59")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Delay):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Delay)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint32(val, 'Delay')

        self.step("60")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SecurityPolicy)
        if val is not NullValue:
            asserts.assert_true(isinstance(val, cluster.Structs.SecurityPolicy), f"val must be of type SecurityPolicy")
            await self.test_checkSecurityPolicy(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("61")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ChannelPage0Mask)
        if val is not NullValue:
            matter_asserts.assert_is_octstr(val, "ChannelPage0Mask must be an octstr")

        self.step("62")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OperationalDatasetComponents)
        if val is not NullValue:
            asserts.assert_true(isinstance(val, cluster.Structs.OperationalDatasetComponents), f"val must be of type OperationalDatasetComponents")
            await self.test_checkOperationalDatasetComponents(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("63")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActiveNetworkFaultsList)
        matter_asserts.assert_list(val, "ActiveNetworkFaultsList attribute must return a list")
        matter_asserts.assert_list_element_type(val,  "ActiveNetworkFaultsList attribute must contain NetworkFaultEnum elements", cluster.Enums.NetworkFaultEnum)
        asserts.assert_less_equal(len(val), 4, "ActiveNetworkFaultsList must have at most 4 entries!")

        self.step("64")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ExtAddress)
        if val is not NullValue:
            matter_asserts.assert_valid_uint64(val, 'ExtAddress')

        self.step("65")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Rloc16)
        if val is not NullValue:
            matter_asserts.assert_valid_uint16(val, 'Rloc16')

    async def test_checkNeighborTableStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ThreadNetworkDiagnostics = None, 
                                 struct: Clusters.ThreadNetworkDiagnostics.Structs.NeighborTableStruct = None):
        matter_asserts.assert_valid_uint64(struct.extAddress, 'ExtAddress')
        matter_asserts.assert_valid_uint32(struct.age, 'Age')
        matter_asserts.assert_valid_uint16(struct.rloc16, 'Rloc16')
        matter_asserts.assert_valid_uint32(struct.linkFrameCounter, 'LinkFrameCounter')
        matter_asserts.assert_valid_uint32(struct.mleFrameCounter, 'MleFrameCounter')
        matter_asserts.assert_valid_uint8(struct.lQI, 'LQI')
        asserts.assert_greater_equal(struct.lQI, 0)
        asserts.assert_less_equal(struct.lQI, 255)
        if struct.averageRssi is not NullValue:
            matter_asserts.assert_valid_int8(struct.averageRssi, 'AverageRssi')
            asserts.assert_greater_equal(struct.averageRssi, -128)
            asserts.assert_less_equal(struct.averageRssi, 0)
        if struct.lastRssi is not NullValue:
            matter_asserts.assert_valid_int8(struct.lastRssi, 'LastRssi')
            asserts.assert_greater_equal(struct.lastRssi, -128)
            asserts.assert_less_equal(struct.lastRssi, 0)
        matter_asserts.assert_valid_uint8(struct.frameErrorRate, 'FrameErrorRate')
        asserts.assert_greater_equal(struct.frameErrorRate, 0)
        asserts.assert_less_equal(struct.frameErrorRate, 100)
        matter_asserts.assert_valid_uint8(struct.messageErrorRate, 'MessageErrorRate')
        asserts.assert_greater_equal(struct.messageErrorRate, 0)
        asserts.assert_less_equal(struct.messageErrorRate, 100)
        matter_asserts.assert_valid_bool(struct.rxOnWhenIdle, 'RxOnWhenIdle')
        matter_asserts.assert_valid_bool(struct.fullThreadDevice, 'FullThreadDevice')
        matter_asserts.assert_valid_bool(struct.fullNetworkData, 'FullNetworkData')
        matter_asserts.assert_valid_bool(struct.isChild, 'IsChild')

    async def test_checkOperationalDatasetComponents(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ThreadNetworkDiagnostics = None, 
                                 struct: Clusters.ThreadNetworkDiagnostics.Structs.OperationalDatasetComponents = None):
        matter_asserts.assert_valid_bool(struct.activeTimestampPresent, 'ActiveTimestampPresent')
        matter_asserts.assert_valid_bool(struct.pendingTimestampPresent, 'PendingTimestampPresent')
        matter_asserts.assert_valid_bool(struct.masterKeyPresent, 'MasterKeyPresent')
        matter_asserts.assert_valid_bool(struct.networkNamePresent, 'NetworkNamePresent')
        matter_asserts.assert_valid_bool(struct.extendedPanIdPresent, 'ExtendedPanIdPresent')
        matter_asserts.assert_valid_bool(struct.meshLocalPrefixPresent, 'MeshLocalPrefixPresent')
        matter_asserts.assert_valid_bool(struct.delayPresent, 'DelayPresent')
        matter_asserts.assert_valid_bool(struct.panIdPresent, 'PanIdPresent')
        matter_asserts.assert_valid_bool(struct.channelPresent, 'ChannelPresent')
        matter_asserts.assert_valid_bool(struct.pskcPresent, 'PskcPresent')
        matter_asserts.assert_valid_bool(struct.securityPolicyPresent, 'SecurityPolicyPresent')
        matter_asserts.assert_valid_bool(struct.channelMaskPresent, 'ChannelMaskPresent')

    async def test_checkRouteTableStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ThreadNetworkDiagnostics = None, 
                                 struct: Clusters.ThreadNetworkDiagnostics.Structs.RouteTableStruct = None):
        matter_asserts.assert_valid_uint64(struct.extAddress, 'ExtAddress')
        matter_asserts.assert_valid_uint16(struct.rloc16, 'Rloc16')
        matter_asserts.assert_valid_uint8(struct.routerId, 'RouterId')
        matter_asserts.assert_valid_uint8(struct.nextHop, 'NextHop')
        matter_asserts.assert_valid_uint8(struct.pathCost, 'PathCost')
        matter_asserts.assert_valid_uint8(struct.lqiIn, 'LQIIn')
        matter_asserts.assert_valid_uint8(struct.lqiOut, 'LQIOut')
        matter_asserts.assert_valid_uint8(struct.age, 'Age')
        matter_asserts.assert_valid_bool(struct.allocated, 'Allocated')
        matter_asserts.assert_valid_bool(struct.linkEstablished, 'LinkEstablished')

    async def test_checkSecurityPolicy(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.ThreadNetworkDiagnostics = None, 
                                 struct: Clusters.ThreadNetworkDiagnostics.Structs.SecurityPolicy = None):
        matter_asserts.assert_valid_uint16(struct.rotationTime, 'RotationTime')
        matter_asserts.assert_valid_uint16(struct.flags, 'Flags')

if __name__ == "__main__":
    default_matter_test_main()
