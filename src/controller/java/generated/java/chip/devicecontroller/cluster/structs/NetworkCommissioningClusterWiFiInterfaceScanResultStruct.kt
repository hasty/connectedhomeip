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
package chip.devicecontroller.cluster.structs

import chip.devicecontroller.cluster.*
import java.util.Optional
import matter.tlv.ContextSpecificTag
import matter.tlv.Tag
import matter.tlv.TlvReader
import matter.tlv.TlvWriter

class NetworkCommissioningClusterWiFiInterfaceScanResultStruct(
  val security: Optional<UInt>,
  val ssid: Optional<ByteArray>,
  val bssid: Optional<ByteArray>,
  val channel: Optional<UInt>,
  val wiFiBand: Optional<UInt>,
  val rssi: Optional<Int>,
) {
  override fun toString(): String = buildString {
    append("NetworkCommissioningClusterWiFiInterfaceScanResultStruct {\n")
    append("\tsecurity : $security\n")
    append("\tssid : $ssid\n")
    append("\tbssid : $bssid\n")
    append("\tchannel : $channel\n")
    append("\twiFiBand : $wiFiBand\n")
    append("\trssi : $rssi\n")
    append("}\n")
  }

  fun toTlv(tlvTag: Tag, tlvWriter: TlvWriter) {
    tlvWriter.apply {
      startStructure(tlvTag)
      if (security.isPresent) {
        val optsecurity = security.get()
        put(ContextSpecificTag(TAG_SECURITY), optsecurity)
      }
      if (ssid.isPresent) {
        val optssid = ssid.get()
        put(ContextSpecificTag(TAG_SSID), optssid)
      }
      if (bssid.isPresent) {
        val optbssid = bssid.get()
        put(ContextSpecificTag(TAG_BSSID), optbssid)
      }
      if (channel.isPresent) {
        val optchannel = channel.get()
        put(ContextSpecificTag(TAG_CHANNEL), optchannel)
      }
      if (wiFiBand.isPresent) {
        val optwiFiBand = wiFiBand.get()
        put(ContextSpecificTag(TAG_WI_FI_BAND), optwiFiBand)
      }
      if (rssi.isPresent) {
        val optrssi = rssi.get()
        put(ContextSpecificTag(TAG_RSSI), optrssi)
      }
      endStructure()
    }
  }

  companion object {
    private const val TAG_SECURITY = 0
    private const val TAG_SSID = 1
    private const val TAG_BSSID = 2
    private const val TAG_CHANNEL = 3
    private const val TAG_WI_FI_BAND = 4
    private const val TAG_RSSI = 5

    fun fromTlv(
      tlvTag: Tag,
      tlvReader: TlvReader,
    ): NetworkCommissioningClusterWiFiInterfaceScanResultStruct {
      tlvReader.enterStructure(tlvTag)
      val security =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_SECURITY))) {
          Optional.of(tlvReader.getUInt(ContextSpecificTag(TAG_SECURITY)))
        } else {
          Optional.empty()
        }
      val ssid =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_SSID))) {
          Optional.of(tlvReader.getByteArray(ContextSpecificTag(TAG_SSID)))
        } else {
          Optional.empty()
        }
      val bssid =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_BSSID))) {
          Optional.of(tlvReader.getByteArray(ContextSpecificTag(TAG_BSSID)))
        } else {
          Optional.empty()
        }
      val channel =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_CHANNEL))) {
          Optional.of(tlvReader.getUInt(ContextSpecificTag(TAG_CHANNEL)))
        } else {
          Optional.empty()
        }
      val wiFiBand =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_WI_FI_BAND))) {
          Optional.of(tlvReader.getUInt(ContextSpecificTag(TAG_WI_FI_BAND)))
        } else {
          Optional.empty()
        }
      val rssi =
        if (tlvReader.isNextTag(ContextSpecificTag(TAG_RSSI))) {
          Optional.of(tlvReader.getInt(ContextSpecificTag(TAG_RSSI)))
        } else {
          Optional.empty()
        }

      tlvReader.exitContainer()

      return NetworkCommissioningClusterWiFiInterfaceScanResultStruct(
        security,
        ssid,
        bssid,
        channel,
        wiFiBand,
        rssi,
      )
    }
  }
}
