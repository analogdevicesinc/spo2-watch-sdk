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



if __name__ == "__main__":
    # SDK setup
    sdk = SDK("COM4")
    sh_application = sdk.get_sensorhub_application()
    fs_application = sdk.get_fs_application()
    
    # get supported streams
    packet = fs_application.get_supported_streams()
    print(packet)

    # START LOGGING
    fs_application.subscribe_stream(fs_application.SH_ADXL_STREAM)
    fs_application.start_logging()
    sh_application.set_operation_mode(sh_application.SH_CONFIG_ADXL_MODE)
    sh_application.start_sensor()
    print(fs_application.get_status()["payload"]["status"])

    print("logging...")
    
    # get stream status
    packet = fs_application.get_stream_status(fs_application.SH_ADXL_STREAM)
    print(packet)
    
    time.sleep(20)

    # STOP LOGGING
    sh_application.stop_sensor()
    fs_application.unsubscribe_stream(fs_application.SH_ADXL_STREAM)
    fs_application.stop_logging()
    print(fs_application.get_status()["payload"]["status"])

    # List all the files available to download.
    files = fs_application.ls()
    for x in files:
        print(x["payload"]["filename"])

    # Download data from the watch and save it to a file.
    fs_application.download_file(files[-1]["payload"]["filename"], download_to_file=True, display_progress=True)

    # Convert downloaded file into CSVs
    sdk.convert_log_to_csv(files[-1]["payload"]["filename"])
    
    # get volume info
    packet = fs_application.volume_info()
    print(packet)

    # get file count
    packet = fs_application.get_file_count()
    print(packet)
