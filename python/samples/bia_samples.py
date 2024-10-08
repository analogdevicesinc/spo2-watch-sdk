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


def callback_data_bia(data):
    for value in data["payload"]["stream_data"]:
        bcm_real = value["real"]
        bcm_imaginary = value["imaginary"]
        if bcm_real == 0:
            bcm_real = 1
        if bcm_imaginary == 0:
            bcm_imaginary = 1
        impedance_img = bcm_imaginary / 1000
        impedance_real = bcm_real / 1000
        real_and_img = float(impedance_real * impedance_real + impedance_img * impedance_img)
        impedance_magnitude = math.sqrt(real_and_img)
        impedance_phase = math.atan2(impedance_img, impedance_real)
        print("BIA ", value["timestamp"], data["payload"]["sequence_number"], impedance_magnitude, impedance_phase)


def callback_data_bcm(data):
    print("BCM ", data["payload"]["timestamp"], data["payload"]["ffm_estimated"], data["payload"]["bmi"],
          data["payload"]["fat_percent"], data["payload"]["sequence_num"])


if __name__ == "__main__":
    sdk = SDK("COM6", mac_address="D5-67-F1-CA-05-C5")
    application = sdk.get_bia_application()
    application.set_callback(callback_data_bia, stream=application.STREAM_BIA)
    application.set_callback(callback_data_bcm, stream=application.STREAM_BCM)

    # quick start bia
    application.write_library_configuration([[0x6, 0x1]])
    application.start_sensor()
    application.subscribe_stream(stream=application.STREAM_BIA)
    application.subscribe_stream(stream=application.STREAM_BCM)
    application.enable_csv_logging("bia.csv", stream=application.STREAM_BIA)
    application.enable_csv_logging("bcm.csv", stream=application.STREAM_BCM)
    time.sleep(50)
    application.unsubscribe_stream(stream=application.STREAM_BIA)
    application.unsubscribe_stream(stream=application.STREAM_BCM)
    application.disable_csv_logging(stream=application.STREAM_BIA)
    application.disable_csv_logging(stream=application.STREAM_BCM)
    application.stop_sensor()

    # get sensor status
    packet = application.get_sensor_status()
    print(packet)

    # write lcfg
    packet = application.write_library_configuration([[0x0B, 0xBDE631F9]])
    print(packet)

    # read lcfg
    packet = application.read_library_configuration([0x0B])
    print(packet)

    # link to use above conversion of float to hexadecimal is found in link:
    # https://babbage.cs.qc.cuny.edu/IEEE-754.old/Decimal.html
    # please find the information about IEEE 754 Single Precision floating format
    # https://en.wikipedia.org/wiki/IEEE_754
    # IEEE conversion is valid from indices 0x0A to 0x11
    # code below shows how to convert hex to decimal
    import struct

    result = list(struct.pack("f", 5.0))
    result1 = struct.unpack("L", bytes(result))[0]
    print('0x%02X' % result1)

    packet = application.write_device_configuration_block_from_file("dcb_cfg/bia_dcb.lcfg", application.BIA_LCFG_BLOCK)
    print(packet)

    packet = application.read_device_configuration_block(application.BIA_LCFG_BLOCK)
    print(packet)

    packet = application.delete_device_configuration_block(application.BIA_LCFG_BLOCK)
    print(packet)
