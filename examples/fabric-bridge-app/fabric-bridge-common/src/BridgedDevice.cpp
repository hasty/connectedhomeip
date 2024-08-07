/*
 *
 *    Copyright (c) 2024 Project CHIP Authors
 *    All rights reserved.
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

#include "BridgedDevice.h"

#include <cstdio>
#include <platform/CHIPDeviceLayer.h>

#include <string>

using namespace chip::app::Clusters::Actions;

BridgedDevice::BridgedDevice(chip::NodeId nodeId)
{
    mReachable  = false;
    mNodeId     = nodeId;
    mEndpointId = chip::kInvalidEndpointId;
}

bool BridgedDevice::IsReachable()
{
    return mReachable;
}

void BridgedDevice::SetReachable(bool reachable)
{
    mReachable = reachable;

    if (reachable)
    {
        ChipLogProgress(NotSpecified, "BridgedDevice[%s]: ONLINE", mName);
    }
    else
    {
        ChipLogProgress(NotSpecified, "BridgedDevice[%s]: OFFLINE", mName);
    }
}

void BridgedDevice::SetName(const char * name)
{
    ChipLogProgress(NotSpecified, "BridgedDevice[%s]: New Name=\"%s\"", mName, name);

    chip::Platform::CopyString(mName, name);
}
