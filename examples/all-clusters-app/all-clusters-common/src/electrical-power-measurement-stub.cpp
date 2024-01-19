/*
 *
 *    Copyright (c) 2023 Project CHIP Authors
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

#include <app/clusters/electrical-power-measurement-server/electrical-power-measurement-server.h>

using namespace chip;
using namespace chip::app::Clusters;
using namespace chip::app::Clusters::ElectricalPowerMeasurement;
using namespace chip::app::Clusters::ElectricalPowerMeasurement::Structs;

namespace chip {
namespace app {
namespace Clusters {
namespace ElectricalPowerMeasurement {

class ElectricalPowerMeasurementDelegate : public Delegate
{
public:

	PowerModeEnum GetPowerMode() override;                                                                        
	uint8_t GetNumberOfMeasurementTypes() override;                                                               
	DataModel::List<const Structs::MeasurementAccuracyStruct::Type> GetAccuracy() override;                       
	DataModel::List<const Structs::MeasurementRangeStruct::Type> GetRanges() override;                            
	DataModel::Nullable<int64_t> GetVoltage() override;                                                           
	DataModel::Nullable<int64_t> GetActiveCurrent() override;                                                     
	DataModel::Nullable<int64_t> GetReactiveCurrent() override;                                                   
	DataModel::Nullable<int64_t> GetApparentCurrent() override;                                                   
	DataModel::Nullable<int64_t> GetActivePower() override;                                                       
	DataModel::Nullable<int64_t> GetReactivePower() override;                                                     
	DataModel::Nullable<int64_t> GetApparentPower() override;                                                     
	DataModel::Nullable<int64_t> GetRMSVoltage() override;                                                        
	DataModel::Nullable<int64_t> GetRMSCurrent() override;                                                        
	DataModel::Nullable<int64_t> GetRMSPower() override;                                                          
	DataModel::Nullable<int64_t> GetFrequency() override;                                                         
	DataModel::Nullable<DataModel::List<Structs::HarmonicMeasurementStruct::Type>> GetHarmonicCurrents() override;
	DataModel::Nullable<DataModel::List<Structs::HarmonicMeasurementStruct::Type>> GetHarmonicPhases() override;  
	DataModel::Nullable<int64_t> GetPowerFactor() override;                                                       
	DataModel::Nullable<int64_t> GetNeutralCurrent() override;                                                    

    ~ElectricalPowerMeasurementDelegate() = default;
};


PowerModeEnum ElectricalPowerMeasurementDelegate::GetPowerMode() {
	return PowerModeEnum::kAc;
}                    

uint8_t ElectricalPowerMeasurementDelegate::GetNumberOfMeasurementTypes() {
	return 1;
}    

DataModel::List<const Structs::MeasurementAccuracyStruct::Type> ElectricalPowerMeasurementDelegate::GetAccuracy() {

	Structs::MeasurementAccuracyRangeStruct::Type activeCurrentAccuracyRanges[] = {
		{
			.rangeMin = 500,
			.rangeMax = 1000
		}
	};
	 Structs::MeasurementAccuracyStruct::Type accuracies[] = {
		{
			.measurementType = MeasurementTypeEnum::kActiveCurrent,
			.measured = true,
			.minMeasuredValue = -10000000,
			.maxMeasuredValue = 10000000,
			.accuracyRanges = DataModel::List<const Structs::MeasurementAccuracyRangeStruct::Type>(
				activeCurrentAccuracyRanges
			)
		}
	 };

	return DataModel::List<const Structs::MeasurementAccuracyStruct::Type>(accuracies);
}       

DataModel::List<const Structs::MeasurementRangeStruct::Type> ElectricalPowerMeasurementDelegate::GetRanges() {
	return DataModel::List<const Structs::MeasurementRangeStruct::Type>();
}     

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetVoltage() {
	return {};
}   

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetActiveCurrent() {
	return {};
}   

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetReactiveCurrent() {
	return {};
}    

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetApparentCurrent() {
	return {};
}    

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetActivePower() {
	return DataModel::Nullable<int64_t>(10000);
}    

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetReactivePower() {
	return {};
}   

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetApparentPower() {
	return {};
}  

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetRMSVoltage() {
	return {};
} 

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetRMSCurrent() {
	return {};
}    

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetRMSPower() {
	return {};
}   

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetFrequency() {
	return {};
}  

DataModel::Nullable<DataModel::List<Structs::HarmonicMeasurementStruct::Type>> ElectricalPowerMeasurementDelegate::GetHarmonicCurrents() {
	return {};
}

DataModel::Nullable<DataModel::List<Structs::HarmonicMeasurementStruct::Type>> ElectricalPowerMeasurementDelegate::GetHarmonicPhases() {
	return {};
}  

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetPowerFactor() {
	return {};
}        

DataModel::Nullable<int64_t> ElectricalPowerMeasurementDelegate::GetNeutralCurrent() {
	return {};
}   

} // namespace ElectricalPowerMeasurement
} // namespace Clusters
} // namespace app
} // namespace chip

static std::unique_ptr<ElectricalPowerMeasurement::Delegate> gDelegate;
static std::unique_ptr<ElectricalPowerMeasurement::Instance> gInstance;

void emberAfEnergyPowerMeasurementClusterInitCallback(chip::EndpointId endpointId)
{
    VerifyOrDie(endpointId == 1); // this cluster is only enabled for endpoint 1.
    VerifyOrDie(!gInstance);

    gDelegate = std::make_unique<ElectricalPowerMeasurementDelegate>();
    if (gDelegate)
    {
        gInstance = std::make_unique<Instance>(
            endpointId, *gDelegate,
            BitMask<Feature, uint32_t>(Feature::kAlternatingCurrent),
            BitMask<OptionalAttributes, uint32_t>());

        gInstance->Init(); 
    }
}
