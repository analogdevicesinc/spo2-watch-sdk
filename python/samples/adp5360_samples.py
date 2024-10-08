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
import datetime

from adi_spo2_watch import SDK


def battery_callback(data):
    print(data)


if __name__ == "__main__":
    sdk = SDK("COM4")
    application = sdk.get_adp5360_application()

    # battery stream
    application.set_callback(battery_callback, stream=application.STREAM_BATTERY)
    application.subscribe_stream(application.STREAM_BATTERY)
    application.enable_csv_logging("battery.csv")
    time.sleep(10)
    application.unsubscribe_stream()
    application.disable_csv_logging()

    # convert ticks to timestamp example
    packet = application.get_battery_info()
    print(packet)
    packet["payload"]["timestamp"] = sdk.convert_ticks_to_timestamp(packet["payload"]["timestamp"])
    print(packet)
    packet = application.read_register([0x3])
    print(packet)

    packet = application.set_battery_threshold(15, 10, 20, 3365, 3187, 3793)
    print(packet)

    packet = application.get_battery_threshold()
    print(packet)

    packet = application.write_device_configuration_block_from_file("dcb_cfg/ADP5360_SW_DCB.DCFG")
    print(packet)

    packet = application.read_device_configuration_block()
    print(packet)

    packet = application.delete_device_configuration_block()
    print(packet)

    packet = application.write_register([[0x3, 0x5]])
    print(packet)
    packet = application.read_register([0x3])
    print(packet)
