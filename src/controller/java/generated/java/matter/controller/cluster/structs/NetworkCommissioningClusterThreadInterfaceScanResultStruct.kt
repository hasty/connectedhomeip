/*
 *
 *    Copyright (c) 2023 Project CHIP Authors
 *
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *
 *        http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing, software
 *    distributed under the License is distributed on an "AS IS" BASIS,
 *    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *    See the License for the specific language governing permissions and
 *    limitations under the License.
 */
package matter.controller.cluster.structs

import java.util.Optional
import matter.controller.cluster.*
import matter.tlv.ContextSpecificTag
import matter.tlv.Tag
import matter.tlv.TlvReader
import matter.tlv.TlvWriter

class NetworkCommissioningClusterThreadInterfaceScanResultStruct(
  val panId: Optional<UShort>,
  val extendedPanId: Optional<ULong>,
  val networkName: Optional<String>,
  val channel: Optional<UShort>,
  val version: Optional<UByte>,
  val extendedAddress: Optional<ByteArray>,
  val rssi: Optional<Byte>,
  val lqi: Optional<UByte>,
) {
  override fun toString(): String = buildString {
    append("NetworkCommissioningClusterThreadInterfaceScanResultStruct {\n")
    append("\tpanId : $panId\n")
    append("\textendedPanId : $extendedPanId\n")
    append("\tnetworkName : $networkName\n")
    append("\tchannel : $channel\n")
    append("\tversion : $version\n")
    append("\textendedAddress : $extendedAddress\n")
    append("\trssi : $rssi\n")
    append("\tlqi : $lqi\n")
    append("}\n")
  }

  fun toTlv(tlvTag: Tag, tlvWriter: TlvWriter) {
    tlvWriter.apply {
      startStructure(tlvTag)
      if (panId.isPresent) {
        val optpanId = panId.get()
        put(ContextSpecificTag(TAG_PAN_ID), optpanId)
      }
      if (extendedPanId.isPresent) {
        val optextendedPanId = extendedPanId.get()
        put(ContextSpecificTag(TAG_EXTENDED_PAN_ID), optextendedPanId)
      }
      if (networkName.isPresent) {
        val optnetworkName = networkName.get()
        put(ContextSpecificTag(TAG_NETWORK_NAME), optnetworkName)
      }
      if (channel.isPresent) {
        val optchannel = channel.get()
        put(ContextSpecificTag(TAG_CHANNEL), optchannel)
      }
      if (version.isPresent) {
        val optversion = version.get()
        put(ContextSpecificTag(TAG_VERSION), optversion)
      }
      if (extendedAddress.isPresent) {
        val optextendedAddress = extendedAddress.get()
        put(ContextSpecificTag(TAG_EXTENDED_ADDRESS), optextendedAddress)
      }
      if (rssi.isPresent) {
        val optrssi = rssi.get()
        put(ContextSpecificTag(TAG_RSSI), optrssi)
      }
      if (lqi.isPresent) {
        val optlqi = lqi.get()
        put(ContextSpecificTag(TAG_LQI), optlqi)
      }
      endStructure()
    }
  }

  companion object {
    private const val TAG_PAN_ID = 0
    private const val TAG_EXTENDED_PAN_ID = 1
    private const val TAG_NETWORK_NAME = 2
    private const val TAG_CHANNEL = 3
    private const val TAG_VERSION = 4
    private const val TAG_EXTENDED_ADDRESS = 5
    private const val TAG_RSSI = 6
    private const val TAG_LQI = 7

    fun fromTlv(
      tlvTag: Tag,
      tlvReader: TlvReader,
    ): NetworkCommissioningClusterThreadInterfaceScanResultStruct {
      tlvReader.enterStructure(tlvTag)
      val panId =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_PAN_ID))) {
          Optional.of(tlvReader.getUShort(ContextSpecificTag(TAG_PAN_ID)))
        } else {
          Optional.empty()
        }
      val extendedPanId =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_EXTENDED_PAN_ID))) {
          Optional.of(tlvReader.getULong(ContextSpecificTag(TAG_EXTENDED_PAN_ID)))
        } else {
          Optional.empty()
        }
      val networkName =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_NETWORK_NAME))) {
          Optional.of(tlvReader.getString(ContextSpecificTag(TAG_NETWORK_NAME)))
        } else {
          Optional.empty()
        }
      val channel =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_CHANNEL))) {
          Optional.of(tlvReader.getUShort(ContextSpecificTag(TAG_CHANNEL)))
        } else {
          Optional.empty()
        }
      val version =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_VERSION))) {
          Optional.of(tlvReader.getUByte(ContextSpecificTag(TAG_VERSION)))
        } else {
          Optional.empty()
        }
      val extendedAddress =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_EXTENDED_ADDRESS))) {
          Optional.of(tlvReader.getByteArray(ContextSpecificTag(TAG_EXTENDED_ADDRESS)))
        } else {
          Optional.empty()
        }
      val rssi =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_RSSI))) {
          Optional.of(tlvReader.getByte(ContextSpecificTag(TAG_RSSI)))
        } else {
          Optional.empty()
        }
      val lqi =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_LQI))) {
          Optional.of(tlvReader.getUByte(ContextSpecificTag(TAG_LQI)))
        } else {
          Optional.empty()
        }

      tlvReader.exitContainer()

      return NetworkCommissioningClusterThreadInterfaceScanResultStruct(
        panId,
        extendedPanId,
        networkName,
        channel,
        version,
        extendedAddress,
        rssi,
        lqi,
      )
    }
  }
}
