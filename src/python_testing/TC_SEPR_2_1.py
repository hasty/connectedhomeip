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

cluster = Clusters.CommodityPrice

class SEPR_2_1(MatterBaseTest):

    def desc_SEPR_2_1(self) -> str:
        """Returns a description of this test"""
        return "Attributes with Server as DUT"

    def pics_SEPR_2_1(self) -> list[str]:
        """This function returns a list of PICS for this test case that must be True for the test to be run"""
        return ["SEPR"]

    def steps_SEPR_2_1(self) -> list[TestStep]:
        steps = [
            TestStep("1", "Read TariffUnit attribute"),
            TestStep("2", "Read Currency attribute"),
            TestStep("3", "Read CurrentPrice attribute"),
            TestStep("4", "Read PriceForecast attribute"),
        ]

        return steps


    @async_test_body
    async def test_SEPR_2_1(self):
        endpoint = self.get_endpoint()
        attributes = cluster.Attributes

        self.step("1")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.TariffUnit)
        matter_asserts.assert_valid_enum(val, "TariffUnit attribute must return a Globals.Enums.TariffUnitEnum", Globals.Enums.TariffUnitEnum)

        self.step("2")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.Currency)
        if val is not NullValue:
            asserts.assert_true(isinstance(val, Globals.Structs.CurrencyStruct),
                                        f"val must be of type Globals.Structs.CurrencyStruct")
            await self.test_checkCurrencyStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("3")
        val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.CurrentPrice)
        if val is not NullValue:
            asserts.assert_true(isinstance(val, Clusters.CommodityPrice.Structs.CommodityPriceStruct),
                                        f"val must be of type Clusters.CommodityPrice.Structs.CommodityPriceStruct")
            await self.test_checkCommodityPriceStruct(endpoint=endpoint, cluster=cluster, struct=val)

        self.step("4")
        if await self.attribute_guard(endpoint=endpoint, attribute=attributes.PriceForecast):
            val = await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=cluster.Attributes.PriceForecast)
            matter_asserts.assert_list(val, "PriceForecast attribute must return a list")
            matter_asserts.assert_list_element_type(val,  "PriceForecast attribute must contain Clusters.CommodityPrice.Structs.CommodityPriceStruct elements", Clusters.CommodityPrice.Structs.CommodityPriceStruct)
            for item in val:
                await self.test_checkCommodityPriceStruct(endpoint=endpoint, cluster=cluster, struct=item)


    async def test_checkCommodityPriceComponentStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.CommodityPrice = None, 
                                 struct: Clusters.CommodityPrice.Structs.CommodityPriceComponentStruct = None):
        matter_asserts.assert_valid_int64(struct.price, 'Price')
        matter_asserts.assert_valid_enum(struct.source, "Source attribute must return a Globals.Enums.TariffPriceTypeEnum", Globals.Enums.TariffPriceTypeEnum)
        if struct.description is not None:
            matter_asserts.assert_is_string(struct.description, "Description must be a string")
            asserts.assert_less_equal(len(struct.description), 32, "Description must have length at most 32!")
        if struct.tariffComponentId is not None:
            matter_asserts.assert_valid_uint32(struct.tariffComponentID, 'TariffComponentID')

    async def test_checkCommodityPriceStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.CommodityPrice = None, 
                                 struct: Clusters.CommodityPrice.Structs.CommodityPriceStruct = None):
        matter_asserts.assert_valid_uint32(struct.periodStart, 'PeriodStart')
        if struct.periodEnd is not NullValue:
            matter_asserts.assert_valid_uint32(struct.periodEnd, 'PeriodEnd')
        asserts.assert_true(isinstance(struct.price, Globals.Structs.PriceStruct),
                                    f"struct.price must be of type Globals.Structs.PriceStruct")
        await self.test_checkPriceStruct(endpoint=endpoint, cluster=cluster, struct=struct.price)
        if struct.description is not None:
            matter_asserts.assert_is_string(struct.description, "Description must be a string")
            asserts.assert_less_equal(len(struct.description), 32, "Description must have length at most 32!")
        if struct.components is not None:
            matter_asserts.assert_list(struct.components, "Components attribute must return a list")
            matter_asserts.assert_list_element_type(struct.components,  "Components attribute must contain Clusters.CommodityPrice.Structs.CommodityPriceComponentStruct elements", Clusters.CommodityPrice.Structs.CommodityPriceComponentStruct)
            for item in struct.components:
                await self.test_checkCommodityPriceComponentStruct(endpoint=endpoint, cluster=cluster, struct=item)
            asserts.assert_less_equal(len(struct.components), 10, "Components must have at most 10 entries!")

    async def test_checkCurrencyStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.CommodityPrice = None, 
                                 struct: Globals.Structs.CurrencyStruct = None):
        matter_asserts.assert_valid_uint16(struct.currency, 'Currency')
        asserts.assert_less_equal(struct.currency, 999)
        matter_asserts.assert_valid_uint8(struct.decimalPoints, 'DecimalPoints')

    async def test_checkPriceStruct(self, 
                                 endpoint: int = None, 
                                 cluster: Clusters.CommodityPrice = None, 
                                 struct: Globals.Structs.PriceStruct = None):
        matter_asserts.assert_valid_int64(struct.amount, 'Amount')
        asserts.assert_true(isinstance(struct.currency, Globals.Structs.CurrencyStruct),
                                    f"struct.currency must be of type Globals.Structs.CurrencyStruct")
        await self.test_checkCurrencyStruct(endpoint=endpoint, cluster=cluster, struct=struct.currency)


if __name__ == "__main__":
    default_matter_test_main()
