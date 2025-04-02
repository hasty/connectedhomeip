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

cluster = Clusters.ColorControl

class CC_2_1(MatterBaseTest):

    def desc_CC_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_CC_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["CC.S"]

    def steps_CC_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read CurrentHue attribute"),
            TestStep("2", "Read CurrentSaturation attribute"),
            TestStep("3", "Read RemainingTime attribute"),
            TestStep("4", "Read CurrentX attribute"),
            TestStep("5", "Read CurrentY attribute"),
            TestStep("6", "Read DriftCompensation attribute"),
            TestStep("7", "Read CompensationText attribute"),
            TestStep("8", "Read ColorTemperatureMireds attribute"),
            TestStep("9", "Read ColorMode attribute"),
            TestStep("10", "Read Options attribute"),
            TestStep("11", "Read NumberOfPrimaries attribute"),
            TestStep("12", "Read Primary1X attribute"),
            TestStep("13", "Read Primary1Y attribute"),
            TestStep("14", "Read Primary1Intensity attribute"),
            TestStep("15", "Read Primary2X attribute"),
            TestStep("16", "Read Primary2Y attribute"),
            TestStep("17", "Read Primary2Intensity attribute"),
            TestStep("18", "Read Primary3X attribute"),
            TestStep("19", "Read Primary3Y attribute"),
            TestStep("20", "Read Primary3Intensity attribute"),
            TestStep("21", "Read Primary4X attribute"),
            TestStep("22", "Read Primary4Y attribute"),
            TestStep("23", "Read Primary4Intensity attribute"),
            TestStep("24", "Read Primary5X attribute"),
            TestStep("25", "Read Primary5Y attribute"),
            TestStep("26", "Read Primary5Intensity attribute"),
            TestStep("27", "Read Primary6X attribute"),
            TestStep("28", "Read Primary6Y attribute"),
            TestStep("29", "Read Primary6Intensity attribute"),
            TestStep("30", "Read WhitePointX attribute"),
            TestStep("31", "Read WhitePointY attribute"),
            TestStep("32", "Read ColorPointRX attribute"),
            TestStep("33", "Read ColorPointRY attribute"),
            TestStep("34", "Read ColorPointRIntensity attribute"),
            TestStep("35", "Read ColorPointGX attribute"),
            TestStep("36", "Read ColorPointGY attribute"),
            TestStep("37", "Read ColorPointGIntensity attribute"),
            TestStep("38", "Read ColorPointBX attribute"),
            TestStep("39", "Read ColorPointBY attribute"),
            TestStep("40", "Read ColorPointBIntensity attribute"),
            TestStep("41", "Read EnhancedCurrentHue attribute"),
            TestStep("42", "Read EnhancedColorMode attribute"),
            TestStep("43", "Read ColorLoopActive attribute"),
            TestStep("44", "Read ColorLoopDirection attribute"),
            TestStep("45", "Read ColorLoopTime attribute"),
            TestStep("46", "Read ColorLoopStartEnhancedHue attribute"),
            TestStep("47", "Read ColorLoopStoredEnhancedHue attribute"),
            TestStep("48", "Read ColorCapabilities attribute"),
            TestStep("49", "Read ColorTempPhysicalMinMireds attribute"),
            TestStep("50", "Read ColorTempPhysicalMaxMireds attribute"),
            TestStep("51", "Read CoupleColorTempToLevelMinMireds attribute"),
            TestStep("52", "Read StartUpColorTemperatureMireds attribute"),
        ]
        return steps

    ColorTempPhysicalMinMireds = None
    ColorTemperatureMireds = None

    @run_if_endpoint_matches(has_cluster(Clusters.ColorControl))
    async def test_CC_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentHue):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentHue)
            matter_asserts.assert_valid_uint8(val, 'CurrentHue')
            asserts.assert_less_equal(val, 254)

        self.step("2")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentSaturation):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentSaturation)
            matter_asserts.assert_valid_uint8(val, 'CurrentSaturation')
            asserts.assert_less_equal(val, 254)

        self.step("3")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.RemainingTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.RemainingTime)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'RemainingTime')
                asserts.assert_less_equal(val, 65534)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentX):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentX)
            matter_asserts.assert_valid_uint16(val, 'CurrentX')
            asserts.assert_less_equal(val, 65279)

        self.step("5")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CurrentY):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentY)
            matter_asserts.assert_valid_uint16(val, 'CurrentY')
            asserts.assert_less_equal(val, 65279)

        self.step("6")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.DriftCompensation):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.DriftCompensation)
            if val is not None:
                matter_asserts.assert_valid_enum(val, "DriftCompensation attribute must return a DriftCompensationEnum", cluster.Enums.DriftCompensationEnum)

        self.step("7")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CompensationText):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CompensationText)
            if val is not None:
                matter_asserts.assert_is_string(val, "CompensationText must be a string")
                asserts.assert_less_equal(len(val), 254, "CompensationText must have length at most 254!")

        self.step("8")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorTemperatureMireds):
            self.ColorTemperatureMireds = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorTemperatureMireds)
            matter_asserts.assert_valid_uint16(self.ColorTemperatureMireds, 'ColorTemperatureMireds')
            asserts.assert_less_equal(self.ColorTemperatureMireds, 65279)

        self.step("9")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorMode)
        matter_asserts.assert_valid_enum(val, "ColorMode attribute must return a ColorModeEnum", cluster.Enums.ColorModeEnum)

        self.step("10")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Options)
        matter_asserts.is_valid_int_value(val)

        self.step("11")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.NumberOfPrimaries)
        if val is not NullValue:
            matter_asserts.assert_valid_uint8(val, 'NumberOfPrimaries')
            asserts.assert_less_equal(val, 6)

        self.step("12")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary1X):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary1X)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary1X')
                asserts.assert_less_equal(val, 65279)

        self.step("13")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary1Y):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary1Y)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary1Y')
                asserts.assert_less_equal(val, 65279)

        self.step("14")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary1Intensity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary1Intensity)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'Primary1Intensity')

        self.step("15")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary2X):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary2X)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary2X')
                asserts.assert_less_equal(val, 65279)

        self.step("16")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary2Y):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary2Y)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary2Y')
                asserts.assert_less_equal(val, 65279)

        self.step("17")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary2Intensity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary2Intensity)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'Primary2Intensity')

        self.step("18")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary3X):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary3X)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary3X')
                asserts.assert_less_equal(val, 65279)

        self.step("19")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary3Y):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary3Y)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary3Y')
                asserts.assert_less_equal(val, 65279)

        self.step("20")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary3Intensity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary3Intensity)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'Primary3Intensity')

        self.step("21")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary4X):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary4X)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary4X')
                asserts.assert_less_equal(val, 65279)

        self.step("22")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary4Y):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary4Y)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary4Y')
                asserts.assert_less_equal(val, 65279)

        self.step("23")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary4Intensity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary4Intensity)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'Primary4Intensity')

        self.step("24")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary5X):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary5X)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary5X')
                asserts.assert_less_equal(val, 65279)

        self.step("25")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary5Y):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary5Y)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary5Y')
                asserts.assert_less_equal(val, 65279)

        self.step("26")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary5Intensity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary5Intensity)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'Primary5Intensity')

        self.step("27")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary6X):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary6X)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary6X')
                asserts.assert_less_equal(val, 65279)

        self.step("28")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary6Y):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary6Y)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'Primary6Y')
                asserts.assert_less_equal(val, 65279)

        self.step("29")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.Primary6Intensity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Primary6Intensity)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'Primary6Intensity')

        self.step("30")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WhitePointX):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WhitePointX)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'WhitePointX')
                asserts.assert_less_equal(val, 65279)

        self.step("31")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.WhitePointY):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.WhitePointY)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'WhitePointY')
                asserts.assert_less_equal(val, 65279)

        self.step("32")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorPointRX):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorPointRX)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ColorPointRX')
                asserts.assert_less_equal(val, 65279)

        self.step("33")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorPointRY):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorPointRY)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ColorPointRY')
                asserts.assert_less_equal(val, 65279)

        self.step("34")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorPointRIntensity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorPointRIntensity)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'ColorPointRIntensity')

        self.step("35")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorPointGX):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorPointGX)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ColorPointGX')
                asserts.assert_less_equal(val, 65279)

        self.step("36")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorPointGY):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorPointGY)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ColorPointGY')
                asserts.assert_less_equal(val, 65279)

        self.step("37")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorPointGIntensity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorPointGIntensity)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'ColorPointGIntensity')

        self.step("38")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorPointBX):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorPointBX)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ColorPointBX')
                asserts.assert_less_equal(val, 65279)

        self.step("39")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorPointBY):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorPointBY)
            if val is not None:
                matter_asserts.assert_valid_uint16(val, 'ColorPointBY')
                asserts.assert_less_equal(val, 65279)

        self.step("40")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorPointBIntensity):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorPointBIntensity)
            if val is not NullValue and val is not None:
                matter_asserts.assert_valid_uint8(val, 'ColorPointBIntensity')

        self.step("41")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.EnhancedCurrentHue):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EnhancedCurrentHue)
            matter_asserts.assert_valid_uint16(val, 'EnhancedCurrentHue')

        self.step("42")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.EnhancedColorMode)
        matter_asserts.assert_valid_enum(val, "EnhancedColorMode attribute must return a EnhancedColorModeEnum", cluster.Enums.EnhancedColorModeEnum)

        self.step("43")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorLoopActive):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorLoopActive)
            matter_asserts.assert_valid_uint8(val, 'ColorLoopActive')
            asserts.assert_less_equal(val, 1)

        self.step("44")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorLoopDirection):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorLoopDirection)
            matter_asserts.assert_valid_enum(val, "ColorLoopDirection attribute must return a ColorLoopDirectionEnum", cluster.Enums.ColorLoopDirectionEnum)

        self.step("45")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorLoopTime):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorLoopTime)
            matter_asserts.assert_valid_uint16(val, 'ColorLoopTime')

        self.step("46")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorLoopStartEnhancedHue):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorLoopStartEnhancedHue)
            matter_asserts.assert_valid_uint16(val, 'ColorLoopStartEnhancedHue')

        self.step("47")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorLoopStoredEnhancedHue):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorLoopStoredEnhancedHue)
            matter_asserts.assert_valid_uint16(val, 'ColorLoopStoredEnhancedHue')

        self.step("48")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorCapabilities)
        matter_asserts.is_valid_int_value(val)
        asserts.assert_less_equal(val, 31)

        self.step("49")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorTempPhysicalMinMireds):
            self.ColorTempPhysicalMinMireds = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorTempPhysicalMinMireds)
            matter_asserts.assert_valid_uint16(self.ColorTempPhysicalMinMireds, 'ColorTempPhysicalMinMireds')
            asserts.assert_greater_equal(self.ColorTempPhysicalMinMireds, 1)
            asserts.assert_less_equal(self.ColorTempPhysicalMinMireds, 65279)

        self.step("50")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.ColorTempPhysicalMaxMireds):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.ColorTempPhysicalMaxMireds)
            matter_asserts.assert_valid_uint16(val, 'ColorTempPhysicalMaxMireds')
            asserts.assert_less_equal(val, 65279)

        self.step("51")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.CoupleColorTempToLevelMinMireds):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CoupleColorTempToLevelMinMireds)
            matter_asserts.assert_valid_uint16(val, 'CoupleColorTempToLevelMinMireds')
            asserts.assert_greater_equal(val, self.ColorTempPhysicalMinMireds)
            asserts.assert_less_equal(val, self.ColorTemperatureMireds)

        self.step("52")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.StartUpColorTemperatureMireds):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.StartUpColorTemperatureMireds)
            if val is not NullValue:
                matter_asserts.assert_valid_uint16(val, 'StartUpColorTemperatureMireds')
                asserts.assert_greater_equal(val, 1)
                asserts.assert_less_equal(val, 65279)

if __name__ == "__main__":
    default_matter_test_main()
