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
    sdk = SDK("COM4")
    application = sdk.get_ecg_application()
    application.set_callback(callback_data)

    # quickstart ECG stream
    application.write_library_configuration([[0x0, 1000]])
    application.write_library_configuration([[0x3, 0]])
    application.start_sensor()
    application.enable_csv_logging("ecg.csv")
    application.subscribe_stream()
    time.sleep(20)
    application.unsubscribe_stream()
    application.disable_csv_logging()
    application.stop_sensor()

    # get decimation factor
    packet = application.get_decimation_factor()
    print(packet)

    # set decimation factor
    packet = application.set_decimation_factor(1)
    print(packet)

    # get sensor status
    packet = application.get_sensor_status()
    print(packet)

    # read dcb
    packet = application.read_device_configuration_block()
    print(packet)

    # write dcb
    packet = application.write_device_configuration_block_from_file("dcb_cfg/ecg_dcb.lcfg")
    print(packet)

    # delete dcb
    packet = application.delete_device_configuration_block()
    print(packet)

    # read lcfg
    packet = application.read_library_configuration([0x0, 0x1])
    print(packet)

    # write dcb to lcfg
    packet = application.write_dcb_to_lcfg()
    print(packet)

    # write lcfg
    packet = application.write_library_configuration([[0x0, 1], [0x1, 2]])
    print(packet)

    # get version
    packet = application.get_version()
    print(packet)

    # algo version
    packet = application.get_algo_version()
    print(packet)
