# ******************************************************************************
# Copyright (c) 2024 Analog Devices, Inc.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
#   * Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
# 
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
# 
#   * Neither the name of Analog Devices, Inc. nor the names of its contributors may
#     be used to endorse or promote products derived from this software without
#     specific prior written permission.
# 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# This software is subject to the above license but may also include
# additional software components that are identified in the NOTICE file,
# together with their associated licenses.
# ******************************************************************************

import time

from adi_spo2_watch import SDK

def callback_data(data):
    print(data)


if __name__ == "__main__":
    sdk = SDK("COM21")

    sensorhub_application = sdk.get_sensorhub_application()

    # Fetch sensorhub firmware version
    packet = sensorhub_application.get_sh_firmware_version()
    print(packet)

    # quickstart SensorHub Max86178 PPG
    sensorhub_application.set_operation_mode(sensorhub_application.SH_CONFIG_PPG_MODE)
    sensorhub_application.enable_csv_logging("sh_stream1.csv", stream=sensorhub_application.SH_MAX86178_STREAM1)
    sensorhub_application.enable_csv_logging("sh_stream2.csv", stream=sensorhub_application.SH_MAX86178_STREAM2)
    sensorhub_application.enable_csv_logging("sh_stream3.csv", stream=sensorhub_application.SH_MAX86178_STREAM3)
    sensorhub_application.set_callback(callback_data, stream=sensorhub_application.SH_MAX86178_STREAM1)
    sensorhub_application.set_callback(callback_data, stream=sensorhub_application.SH_MAX86178_STREAM2)
    sensorhub_application.set_callback(callback_data, stream=sensorhub_application.SH_MAX86178_STREAM3)
    sensorhub_application.subscribe_stream(sensorhub_application.SH_MAX86178_STREAM1)
    sensorhub_application.subscribe_stream(sensorhub_application.SH_MAX86178_STREAM2)
    sensorhub_application.subscribe_stream(sensorhub_application.SH_MAX86178_STREAM3)
    sensorhub_application.start_sensor()

    time.sleep(10)

    # quickstop SensorHub Max86178 PPG
    sensorhub_application.stop_sensor()
    sensorhub_application.unsubscribe_stream(sensorhub_application.SH_MAX86178_STREAM1)
    sensorhub_application.unsubscribe_stream(sensorhub_application.SH_MAX86178_STREAM2)
    sensorhub_application.unsubscribe_stream(sensorhub_application.SH_MAX86178_STREAM3)
    sensorhub_application.disable_csv_logging(stream=sensorhub_application.SH_MAX86178_STREAM1)
    sensorhub_application.disable_csv_logging(stream=sensorhub_application.SH_MAX86178_STREAM2)
    sensorhub_application.disable_csv_logging(stream=sensorhub_application.SH_MAX86178_STREAM3)

    # quickstart SensorHub MAX86178 ECG
    sensorhub_application.set_operation_mode(sensorhub_application.SH_CONFIG_ECG_MODE)
    sensorhub_application.enable_csv_logging("sh_ecg.csv", stream=sensorhub_application.SH_MAX86178_ECG_STREAM)
    sensorhub_application.set_callback(callback_data, stream=sensorhub_application.SH_MAX86178_ECG_STREAM)
    sensorhub_application.subscribe_stream(sensorhub_application.SH_MAX86178_ECG_STREAM)
    sensorhub_application.start_sensor()

    time.sleep(10)

    # quickstop SensorHub MAX86178 ECG
    sensorhub_application.stop_sensor()
    sensorhub_application.unsubscribe_stream(sensorhub_application.SH_MAX86178_ECG_STREAM)
    sensorhub_application.disable_csv_logging(stream=sensorhub_application.SH_MAX86178_ECG_STREAM)

    # quickstart SensorHub ADXL
    sensorhub_application.set_operation_mode(sensorhub_application.SH_CONFIG_ADXL_MODE)
    sensorhub_application.enable_csv_logging("sh_adxl.csv", stream=sensorhub_application.SH_ADXL_STREAM)
    sensorhub_application.set_callback(callback_data, stream=sensorhub_application.SH_ADXL_STREAM)
    sensorhub_application.subscribe_stream(sensorhub_application.SH_ADXL_STREAM)
    sensorhub_application.start_sensor()

    time.sleep(10)

    # quickstop SensorHub ADXL
    sensorhub_application.stop_sensor()
    sensorhub_application.unsubscribe_stream(sensorhub_application.SH_ADXL_STREAM)
    sensorhub_application.disable_csv_logging(stream=sensorhub_application.SH_ADXL_STREAM)

    # quickstart SensorHub HRM
    sensorhub_application.set_operation_mode(sensorhub_application.SH_CONFIG_ALGO_MODE)
    sensorhub_application.enable_csv_logging("sh_hrm.csv", stream=sensorhub_application.SH_HRM_STREAM)
    sensorhub_application.set_callback(callback_data, stream=sensorhub_application.SH_HRM_STREAM)
    sensorhub_application.subscribe_stream(sensorhub_application.SH_HRM_STREAM)
    sensorhub_application.start_sensor()

    time.sleep(10)

    # quickstop SensorHub HRM
    sensorhub_application.stop_sensor()
    sensorhub_application.unsubscribe_stream(sensorhub_application.SH_HRM_STREAM)
    sensorhub_application.disable_csv_logging(stream=sensorhub_application.SH_HRM_STREAM)

    # quickstart SensorHub SPO2
    sensorhub_application.set_operation_mode(sensorhub_application.SH_CONFIG_ALGO_MODE)
    sensorhub_application.enable_csv_logging("sh_spo2.csv", stream=sensorhub_application.SH_SPO2_STREAM)
    sensorhub_application.set_callback(callback_data, stream=sensorhub_application.SH_SPO2_STREAM)
    sensorhub_application.subscribe_stream(sensorhub_application.SH_SPO2_STREAM)
    sensorhub_application.start_sensor()

    time.sleep(10)

    # quickstop SensorHub SPO2
    sensorhub_application.stop_sensor()
    sensorhub_application.unsubscribe_stream(sensorhub_application.SH_SPO2_STREAM)
    sensorhub_application.disable_csv_logging(stream=sensorhub_application.SH_SPO2_STREAM)

    # quickstart SensorHub RR
    sensorhub_application.set_operation_mode(sensorhub_application.SH_CONFIG_ALGO_MODE)
    sensorhub_application.enable_csv_logging("sh_rr.csv", stream=sensorhub_application.SH_RR_STREAM)
    sensorhub_application.set_callback(callback_data, stream=sensorhub_application.SH_RR_STREAM)
    sensorhub_application.subscribe_stream(sensorhub_application.SH_RR_STREAM)
    sensorhub_application.start_sensor()

    time.sleep(10)

    # quickstop SensorHub RR
    sensorhub_application.stop_sensor()
    sensorhub_application.unsubscribe_stream(sensorhub_application.SH_RR_STREAM)
    sensorhub_application.disable_csv_logging(stream=sensorhub_application.SH_RR_STREAM)

    # Read register values
    packet = sensorhub_application.adxl367_read_register([0x20, 0x21, 0x22])
    print(packet)
    packet = sensorhub_application.max86178_read_register([0x30, 0x31, 0x32])
    print(packet)

    # Write register values
    packet = sensorhub_application.adxl367_write_register([[0x20, 0x01], [0x21, 0x02], [0x22, 0x03]])
    print(packet)
    packet = sensorhub_application.max86178_write_register([[0x30, 0x00], [0x31, 0x1A], [0x32, 0x23]])
    print(packet)

    # Load device configuration
    max86178_device_ids = sensorhub_application.get_supported_max86178_devices()
    packet = sensorhub_application.load_max86178_configuration(sensorhub_application.DEVICE_G_R_IR)
    print(packet)
    packet = sensorhub_application.load_max86178_configuration(sensorhub_application.DEVICE_ECG)
    print(packet)
    adxl367_device_ids = sensorhub_application.get_supported_adxl367_devices()
    packet = sensorhub_application.load_adxl367_configuration(sensorhub_application.DEVICE_367)
    print(packet)
    was_device_ids = sensorhub_application.get_supported_was_devices()
    packet = sensorhub_application.load_was_configuration(sensorhub_application.DEVICE_WAS)
    print(packet)

    # Read DCB
    packet = sensorhub_application.read_adxl367_device_configuration_block()
    print(packet)
    packet = sensorhub_application.read_max86178_device_configuration_block()
    print(packet)

    # Write DCB
    packet = sensorhub_application.write_adxl367_device_configuration_block([[0x20, 0x01], [0x21, 0x02], [0x22, 0x03]])
    print(packet)
    packet = sensorhub_application.write_max86178_device_configuration_block([[0x30, 0x00], [0x31, 0x1A], [0x32, 0x23]])
    print(packet)

    # Write DCB from file
    packet = sensorhub_application.write_adxl367_device_configuration_block_from_file("dcb_cfg/adxl367_dcb.dcfg")
    print(packet)
    packet = sensorhub_application.write_max86178_device_configuration_block_from_file("dcb_cfg/max86178_dcb.dcfg")
    print(packet)

    # Delete DCB
    packet = sensorhub_application.delete_adxl367_device_configuration_block()
    print(packet)
    packet = sensorhub_application.delete_max86178_device_configuration_block()
    print(packet)

    # ADXL367 self test
    adxl367_meas_range = sensorhub_application.get_supported_adxl367_meas_range()
    packet = sensorhub_application.adxl367_self_test(sensorhub_application.SH_ADXL367_MEAS_RANGE_8G)
    print(packet)

    #Decimaton Test for HR
    packet = sensorhub_application.set_algo_decimation(en_reg_decimation=False, en_spo2_decimation=False, en_hr_decimation=True, en_rr_decimation=False)
    packet = sensorhub_application.get_algo_decimation()
    print(packet)
    sensorhub_application.set_operation_mode(sensorhub_application.SH_CONFIG_ALGO_MODE)
    sensorhub_application.enable_csv_logging("sh_hrm_1Hz.csv", stream=sensorhub_application.SH_HRM_STREAM)
    sensorhub_application.set_callback(callback_data, stream=sensorhub_application.SH_HRM_STREAM)
    sensorhub_application.subscribe_stream(sensorhub_application.SH_HRM_STREAM)
    sensorhub_application.start_sensor()

    time.sleep(10)

    # quickstop SensorHub HRM
    sensorhub_application.stop_sensor()
    sensorhub_application.unsubscribe_stream(sensorhub_application.SH_HRM_STREAM)
    sensorhub_application.disable_csv_logging(stream=sensorhub_application.SH_HRM_STREAM)
    packet = sensorhub_application.set_algo_decimation(en_reg_decimation=False, en_spo2_decimation=False, en_hr_decimation=False, en_rr_decimation=False)
    packet = sensorhub_application.get_algo_decimation()
    print(packet)

