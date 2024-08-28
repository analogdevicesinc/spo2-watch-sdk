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
import argparse
import shutil
import subprocess
import sys
import time

from adi_spo2_watch import SDK

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("com_port", help="The COM port of SpO2 Watch. Example: COM6")

    com_port = parser.parse_args().com_port

    assert shutil.which("nrfutil") is not None, "nrfutil not found in PATH!"
    
    print("Updating NRF firmware...")
    sdk = SDK(com_port)
    pm_app = sdk.get_pm_application()
    pm_app.enter_boot_loader_mode()
    sdk.disconnect()
    subprocess.run(["nrfutil", "dfu", "usb-serial", "-pkg", "Binaries\\ADI_project.zip", "-p", com_port])

    print("\nWaiting for device to reboot...")
    time.sleep(15)

    print("\nUpdating Sensorhub firmware...")
    subprocess.run([sys.executable, "Utils\\sensorhub_fw_update.py", com_port, "Binaries\\MAX32670_WHRM_AEC_SCD_WSPO2_devel.msbl"])

    print("\nFirmware update complete!")
