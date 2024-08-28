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

import math
import time

from adi_spo2_watch import SDK


def callback_data(data):
    for value in data["payload"]["stream_data"]:
        eda_real = value["real"]
        eda_imaginary = value["imaginary"]
        if eda_real == 0:
            eda_real = 1
        impedance_img = eda_imaginary * 1000.0
        impedance_real = eda_real * 1000.0
        real_and_img = float(impedance_real * impedance_real + impedance_img * impedance_img)
        impedance_module = math.sqrt(real_and_img)
        impedance_phase = math.atan2(impedance_img, impedance_real)
        print(value["timestamp"], data["payload"]["sequence_number"], impedance_module, impedance_phase)


if __name__ == "__main__":
    sdk = SDK("COM4")
    application = sdk.get_eda_application()
    application.set_callback(callback_data)

    # quickstart EDA stream
    application.write_library_configuration([[0x0, 0x4], [0x02, 0x02]])
    application.start_sensor()
    application.enable_csv_logging("eda.csv")
    application.subscribe_stream()
    time.sleep(10)
    application.unsubscribe_stream()
    application.disable_csv_logging()
    application.stop_sensor()

    # changing ODR 8Hz
    application.write_library_configuration([[0x0, 0x8], [0x02, 0x02]])

    # changing ODR greater than 16
    application.write_library_configuration([[0x0, 0x30], [0x02, 0x01]])

    # get decimation factor
    packet = application.get_decimation_factor()
    print(packet)

    # get sensor status
    packet = application.get_sensor_status()
    print(packet)

    # write dcb
    packet = application.write_device_configuration_block_from_file("dcb_cfg/eda_dcb.lcfg", application.EDA_LCFG_BLOCK)
    print(packet)

    # read dcb
    packet = application.read_device_configuration_block(application.EDA_LCFG_BLOCK)
    print(packet)

    packet = application.delete_device_configuration_block(application.EDA_LCFG_BLOCK)
    print(packet)

    packet = application.set_baseline_impedance(25000.5, 25000.5, 25000.5, 25000.5, 19900)
    print(packet)

    packet = application.get_baseline_impedance()
    print(packet)
