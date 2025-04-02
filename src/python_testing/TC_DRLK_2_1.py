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

cluster = Clusters.DoorLock

class DRLK_2_1(MatterBaseTest):

    def desc_DRLK_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_DRLK_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["DRLK.S"]

    def steps_DRLK_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read LockState attribute"),
            TestStep("2", "Read LockType attribute"),
            TestStep("3", "Read ActuatorEnabled attribute"),
            TestStep("4", "Read DoorState attribute"),
            TestStep("5", "Read DoorOpenEvents attribute"),
            TestStep("6", "Read DoorClosedEvents attribute"),
            TestStep("7", "Read OpenPeriod attribute"),
            TestStep("8", "Read NumberOfTotalUsersSupported attribute"),
            TestStep("9", "Read NumberOfPINUsersSupported attribute"),
            TestStep("10", "Read NumberOfRFIDUsersSupported attribute"),
            TestStep("11", "Read NumberOfWeekDaySchedulesSupportedPerUser attribute"),
            TestStep("12", "Read NumberOfYearDaySchedulesSupportedPerUser attribute"),
            TestStep("13", "Read NumberOfHolidaySchedulesSupported attribute"),
            TestStep("14", "Read MaxPINCodeLength attribute"),
            TestStep("15", "Read MinPINCodeLength attribute"),
            TestStep("16", "Read MaxRFIDCodeLength attribute"),
            TestStep("17", "Read MinRFIDCodeLength attribute"),
            TestStep("18", "Read CredentialRulesSupport attribute"),
            TestStep("19", "Read NumberOfCredentialsSupportedPerUser attribute"),
            TestStep("20", "Read Language attribute"),
            TestStep("21", "Read LEDSettings attribute"),
            TestStep("22", "Read AutoRelockTime attribute"),
            TestStep("23", "Read SoundVolume attribute"),
            TestStep("24", "Read OperatingMode attribute"),
            TestStep("25", "Read SupportedOperatingModes attribute"),
            TestStep("26", "Read DefaultConfigurationRegister attribute"),
            TestStep("27", "Read EnableLocalProgramming attribute"),
            TestStep("28", "Read EnableOneTouchLocking attribute"),
            TestStep("29", "Read EnableInsideStatusLED attribute"),
            TestStep("30", "Read EnablePrivacyModeButton attribute"),
            TestStep("31", "Read LocalProgrammingFeatures attribute"),
            TestStep("32", "Read WrongCodeEntryLimit attribute"),
            TestStep("33", "Read UserCodeTemporaryDisableTime attribute"),
            TestStep("34", "Read SendPINOverTheAir attribute"),
            TestStep("35", "Read RequirePINforRemoteOperation attribute"),
            TestStep("36", "Read ExpiringUserTimeout attribute"),
            TestStep("37", "Read AliroReaderVerificationKey attribute"),
            TestStep("38", "Read AliroReaderGroupIdentifier attribute"),
            TestStep("39", "Read AliroReaderGroupSubIdentifier attribute"),
            TestStep("40", "Read AliroExpeditedTransactionSupportedProtocolVersions attribute"),
            TestStep("41", "Read AliroGroupResolvingKey attribute"),
            TestStep("42", "Read AliroSupportedBLEUWBProtocolVersions attribute"),
            TestStep("43", "Read AliroBLEAdvertisingVersion attribute"),
            TestStep("44", "Read NumberOfAliroCredentialIssuerKeysSupported attribute"),
            TestStep("45", "Read NumberOfAliroEndpointKeysSupported attribute"),
        ]
        return steps

    @run_if_endpoint_matches(has_cluster(Clusters.DoorLock))
    async def test_DRLK_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LockState)
        if val is not NullValue:
            matter_asserts.assert_valid_enum(val, "LockState attribute must return a LockStateEnum", cluster.Enums.LockStateEnum)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LockType)
        matter_asserts.assert_valid_enum(val, "LockType attribute must return a LockTypeEnum", cluster.Enums.LockTypeEnum)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ActuatorEnabled)
        matter_asserts.assert_valid_bool(val, 'ActuatorEnabled')

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DoorState):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DoorState)
            if val is not NullValue:
                matter_asserts.assert_valid_enum(val, "DoorState attribute must return a DoorStateEnum", cluster.Enums.DoorStateEnum)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DoorOpenEvents):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DoorOpenEvents)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'DoorOpenEvents')

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DoorClosedEvents):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DoorClosedEvents)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'DoorClosedEvents')

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.OpenPeriod):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OpenPeriod)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'OpenPeriod')

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfTotalUsersSupported):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfTotalUsersSupported)
            matter_asserts.assert_valid_uint16(val, 'NumberOfTotalUsersSupported')

        self.step("9")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfPINUsersSupported):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfPINUsersSupported)
            matter_asserts.assert_valid_uint16(val, 'NumberOfPINUsersSupported')

        self.step("10")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfRFIDUsersSupported):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfRFIDUsersSupported)
            matter_asserts.assert_valid_uint16(val, 'NumberOfRFIDUsersSupported')

        self.step("11")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfWeekDaySchedulesSupportedPerUser):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfWeekDaySchedulesSupportedPerUser)
            matter_asserts.assert_valid_uint8(val, 'NumberOfWeekDaySchedulesSupportedPerUser')
            asserts.assert_less_equal(val, 253)

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfYearDaySchedulesSupportedPerUser):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfYearDaySchedulesSupportedPerUser)
            matter_asserts.assert_valid_uint8(val, 'NumberOfYearDaySchedulesSupportedPerUser')
            asserts.assert_less_equal(val, 253)

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfHolidaySchedulesSupported):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfHolidaySchedulesSupported)
            matter_asserts.assert_valid_uint8(val, 'NumberOfHolidaySchedulesSupported')
            asserts.assert_less_equal(val, 253)

        self.step("14")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxPINCodeLength):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxPINCodeLength)
            matter_asserts.assert_valid_uint8(val, 'MaxPINCodeLength')

        self.step("15")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinPINCodeLength):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinPINCodeLength)
            matter_asserts.assert_valid_uint8(val, 'MinPINCodeLength')

        self.step("16")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MaxRFIDCodeLength):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MaxRFIDCodeLength)
            matter_asserts.assert_valid_uint8(val, 'MaxRFIDCodeLength')

        self.step("17")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.MinRFIDCodeLength):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.MinRFIDCodeLength)
            matter_asserts.assert_valid_uint8(val, 'MinRFIDCodeLength')

        self.step("18")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CredentialRulesSupport):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CredentialRulesSupport)
            matter_asserts.is_valid_int_value(val)
            # Check bitmap value less than or equal to (Single | Dual | Tri)
            asserts.assert_less_equal(val, 7)

        self.step("19")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfCredentialsSupportedPerUser):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfCredentialsSupportedPerUser)
            matter_asserts.assert_valid_uint8(val, 'NumberOfCredentialsSupportedPerUser')

        self.step("20")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Language):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Language)
            if val is not None:
                matter_asserts.assert_is_string(val, "Language must be a string")
                asserts.assert_less_equal(len(val), 3, "Language must have length at most 3!")

        self.step("21")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.LEDSettings):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LEDSettings)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "LEDSettings attribute must return a LEDSettingEnum", cluster.Enums.LEDSettingEnum)

        self.step("22")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AutoRelockTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AutoRelockTime)
            if val is not None:
                matter_asserts.assert_valid_uint32(val, 'AutoRelockTime')

        self.step("23")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SoundVolume):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SoundVolume)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "SoundVolume attribute must return a SoundVolumeEnum", cluster.Enums.SoundVolumeEnum)

        self.step("24")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.OperatingMode)
        matter_asserts.assert_valid_enum(val, "OperatingMode attribute must return a OperatingModeEnum", cluster.Enums.OperatingModeEnum)

        self.step("25")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SupportedOperatingModes)
        matter_asserts.is_valid_int_value(val)
        # Check bitmap value less than or equal to (Normal | Vacation | Privacy | NoRemoteLockUnlock | Passage)
        asserts.assert_less_equal(val, 31)

        self.step("26")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DefaultConfigurationRegister):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DefaultConfigurationRegister)
            if val is not None:
                matter_asserts.is_valid_int_value(val)
                # Check bitmap value less than or equal to (LocalProgramming | KeypadInterface | RemoteInterface | SoundVolume | AutoRelockTime | LEDSettings)
                asserts.assert_less_equal(val, 231)

        self.step("27")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.EnableLocalProgramming):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EnableLocalProgramming)
            if val is not None:
                matter_asserts.assert_valid_bool(val, 'EnableLocalProgramming')

        self.step("28")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.EnableOneTouchLocking):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EnableOneTouchLocking)
            if val is not None:
                matter_asserts.assert_valid_bool(val, 'EnableOneTouchLocking')

        self.step("29")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.EnableInsideStatusLED):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EnableInsideStatusLED)
            if val is not None:
                matter_asserts.assert_valid_bool(val, 'EnableInsideStatusLED')

        self.step("30")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.EnablePrivacyModeButton):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EnablePrivacyModeButton)
            if val is not None:
                matter_asserts.assert_valid_bool(val, 'EnablePrivacyModeButton')

        self.step("31")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.LocalProgrammingFeatures):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.LocalProgrammingFeatures)
            if val is not None:
                matter_asserts.is_valid_int_value(val)
                # Check bitmap value less than or equal to (AddUsersCredentialsSchedules | ModifyUsersCredentialsSchedules | ClearUsersCredentialsSchedules | AdjustSettings)
                asserts.assert_less_equal(val, 15)

        self.step("32")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WrongCodeEntryLimit):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WrongCodeEntryLimit)
            matter_asserts.assert_valid_uint8(val, 'WrongCodeEntryLimit')
            asserts.assert_greater_equal(val, 1)
            asserts.assert_less_equal(val, 255)

        self.step("33")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.UserCodeTemporaryDisableTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.UserCodeTemporaryDisableTime)
            matter_asserts.assert_valid_uint8(val, 'UserCodeTemporaryDisableTime')
            asserts.assert_greater_equal(val, 1)
            asserts.assert_less_equal(val, 255)

        self.step("34")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.SendPINOverTheAir):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.SendPINOverTheAir)
            if val is not None:
                matter_asserts.assert_valid_bool(val, 'SendPINOverTheAir')

        self.step("35")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RequirePINforRemoteOperation):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RequirePINforRemoteOperation)
            matter_asserts.assert_valid_bool(val, 'RequirePINforRemoteOperation')

        self.step("36")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ExpiringUserTimeout):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ExpiringUserTimeout)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ExpiringUserTimeout')
                asserts.assert_greater_equal(val, 1)
                asserts.assert_less_equal(val, 2880)

        self.step("37")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AliroReaderVerificationKey):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AliroReaderVerificationKey)
            if val is not NullValue:
                matter_asserts.assert_is_octstr(val, "AliroReaderVerificationKey must be an octstr")

        self.step("38")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AliroReaderGroupIdentifier):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AliroReaderGroupIdentifier)
            if val is not NullValue:
                matter_asserts.assert_is_octstr(val, "AliroReaderGroupIdentifier must be an octstr")

        self.step("39")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AliroReaderGroupSubIdentifier):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AliroReaderGroupSubIdentifier)
            matter_asserts.assert_is_octstr(val, "AliroReaderGroupSubIdentifier must be an octstr")

        self.step("40")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AliroExpeditedTransactionSupportedProtocolVersions):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AliroExpeditedTransactionSupportedProtocolVersions)
            matter_asserts.assert_list(val, "AliroExpeditedTransactionSupportedProtocolVersions attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "AliroExpeditedTransactionSupportedProtocolVersions attribute must contain bytes elements", bytes)
            asserts.assert_less_equal(len(val), 16, "AliroExpeditedTransactionSupportedProtocolVersions must have at most 16 entries!")

        self.step("41")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AliroGroupResolvingKey):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AliroGroupResolvingKey)
            if val is not NullValue:
                matter_asserts.assert_is_octstr(val, "AliroGroupResolvingKey must be an octstr")

        self.step("42")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AliroSupportedBLEUWBProtocolVersions):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AliroSupportedBLEUWBProtocolVersions)
            matter_asserts.assert_list(val, "AliroSupportedBLEUWBProtocolVersions attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "AliroSupportedBLEUWBProtocolVersions attribute must contain bytes elements", bytes)
            asserts.assert_less_equal(len(val), 16, "AliroSupportedBLEUWBProtocolVersions must have at most 16 entries!")

        self.step("43")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.AliroBLEAdvertisingVersion):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.AliroBLEAdvertisingVersion)
            matter_asserts.assert_valid_uint8(val, 'AliroBLEAdvertisingVersion')

        self.step("44")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfAliroCredentialIssuerKeysSupported):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfAliroCredentialIssuerKeysSupported)
            matter_asserts.assert_valid_uint16(val, 'NumberOfAliroCredentialIssuerKeysSupported')

        self.step("45")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.NumberOfAliroEndpointKeysSupported):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfAliroEndpointKeysSupported)
            matter_asserts.assert_valid_uint16(val, 'NumberOfAliroEndpointKeysSupported')

if __name__ == "__main__":
    default_matter_test_main()
