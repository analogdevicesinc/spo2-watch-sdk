# ******************************************************************************
# Copyright (c) 2023 Analog Devices, Inc.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
# - Modified versions of the software must be conspicuously marked as such.
# - This software is licensed solely and exclusively for use with
#  processors/products manufactured by or for Analog Devices, Inc.
# - This software may not be combined or merged with other code in any manner
#  that would cause the software to become subject to terms and conditions
#  which differ from those listed here.
# - Neither the name of Analog Devices, Inc. nor the names of its contributors
#  may be used to endorse or promote products derived from this software
#  without specific prior written permission.
# - The use of this software may or may not infringe the patent rights of one
#  or more patent holders.  This license does not release you from the
#  requirement that you obtain separate licenses from these patent holders to
#  use this software.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES, INC. AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# NONINFRINGEMENT, TITLE, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ANALOG DEVICES, INC. OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, DAMAGES ARISING OUT OF
# CLAIMS OF INTELLECTUAL PROPERTY RIGHTS INFRINGEMENT; PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ******************************************************************************
import os
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
import sys
import time
from copy import deepcopy
from ctypes import *

from adi_spo2_watch import SDK
from adi_spo2_watch.core.enums.common_enums import CommonStatus
from adi_spo2_watch.core.enums.sensorhub_enums import SHMode

DEFAULT_PAGE_SIZE = 8192
POST_HW_RESET_WAIT_SEC = 43

class MsblHeader(Structure):
	_fields_ = [('magic', 4 * c_char),
				('formatVersion', c_uint),
				('target', 16 * c_char),
				('enc_type', 16 * c_char),
				('nonce', 11 * c_ubyte),
				('resv0', c_ubyte),
				('auth', 16 * c_ubyte),
				('numPages', c_ushort),
				('pageSize', c_ushort),
				('crcSize', c_ubyte),
				('resv1', 3 * c_ubyte)]

class Page(Structure):
	_fields_ = [('data', (8192 + 16) * c_ubyte)]

class CRC32(Structure):
	_fields_ = [('val', c_uint)]

class MSBL_FILE_INFO:
    Numberofpages = 0
    nonce = []
    auth = []
    page = {}


def initialize(com_port):
    global sdk
    sdk = SDK(com_port)


def read_msbl_file(msbl_file):
    result = MSBL_FILE_INFO()
    total_size = 0
    with open(msbl_file, 'rb') as f:
        header = MsblHeader()
        if f.readinto(header) == sizeof(header):
            result.Numberofpages = header.numPages
            result.nonce = header.nonce
            result.auth = header.auth
        else:
            print("Header of the file doesnt match size !!!")

        i = 0
        tmp_page = Page()
        total_size = total_size + sizeof(header)
        while f.readinto(tmp_page) == sizeof(tmp_page):
            result.page[i] = deepcopy(tmp_page.data)
            total_size = total_size + sizeof(tmp_page)
            i = i + 1
        crc32 = CRC32()
        f.seek(-4, 2)
        f.readinto(crc32)
        total_size = total_size + sizeof(crc32)
        f.close()
    return result


def start_download_page(app,file_info : MSBL_FILE_INFO):
    num_pages = file_info.Numberofpages
    # print("{} pages needs to be downloaded").format(num_pages)
    for page_num in range(0, num_pages):
        left_over = DEFAULT_PAGE_SIZE + 16
        step = 128
        page_bin = file_info.page[page_num]
        page_pkt_counter = 0
        i = 0
        temp_page_part = []
        while i < (DEFAULT_PAGE_SIZE + 16):
            j = 0
            while j < step:
                page_part = page_bin[i + j: i + j + 1]
                temp_page_part.append(page_part[0])
                j += 1
            result = app.sh_start_download_page(page_pkt_counter, page_num, step, temp_page_part)
            if result["payload"]["status"] == CommonStatus.DOWNLOAD_IN_PROGRESS:
                pass
            elif result["payload"]["status"] == CommonStatus.DOWNLOAD_COMPLETE:
                print("Download complete for page ", page_num + 1)
            elif result["payload"]["status"] == CommonStatus.DOWNLOAD_CHECKSUM_ERROR:
                print("Checksum Error")
                raise ValueError("Checksum Error")
            else:
                print("Unknown State")
                raise ValueError("Watch is in unknown State")
            i += step
            left_over -= step
            if left_over <= 16:
                step = left_over
            temp_page_part.clear()
            page_pkt_counter += 1

def reset(com_port):
    pm = sdk.get_pm_application()
    pm.system_reset()
    time.sleep(5)


if __name__ == "__main__":
    com_port = sys.argv[1]
    msbl_file = sys.argv[2]
    initialize(com_port)
    sensorhub_application = sdk.get_sensorhub_application()
    pm_application = sdk.get_pm_application()
    for i in range(3):
        try:
            time.sleep(10)
            pkt = sensorhub_application.get_operation_mode()
            if (pkt["payload"]["status"] == CommonStatus.OK):
                if pkt["payload"]["mode"] == SHMode.SENSORHUB_APPLICATION_MODE:
                    print("Sensorhub in Application Mode")
                    pkt = sensorhub_application.enter_sh_boot_loader_mode(True)
                    if (pkt["payload"]["status"] == CommonStatus.OK):
                        if (pkt["payload"]["mode"] == True):
                            print("Sensorhub in Bootloader mode")
                        else:
                            print("Sensorhub not in mode.It is in {}".format(pkt["payload"]["mode"]))
                            
                    else:
                        raise ValueError("Error:\tenter_sh_boot_loader_mode(): {}. It is in {}".format(pkt["payload"]["status"],pkt["payload"]["mode"]))                   
                    
                elif pkt["payload"]["mode"] == SHMode.SENSORHUB_BOOTLOADER_MODE:
                    print("Sensorhub in Bootloader Mode")
                
                else:
                    raise ValueError("SH is in Unknown Mode")   
            else:
                raise ValueError("Error:\t get_operation_mode()".format(pkt["payload"]["status"]))
            
            pkt = sensorhub_application.get_sh_page_size()
            if (pkt["payload"]["status"] == CommonStatus.OK):
                print("Successful:\tget_sh_page_size(): Page size info:{}".format(pkt["payload"]["page_size"]))
                
                msbl_info = read_msbl_file(msbl_file)
                
                pkt = sensorhub_application.set_sh_page_num(msbl_info.Numberofpages)
                if (pkt["payload"]["status"] == CommonStatus.OK):
                    print("Successful:\tset_sh_page_num()")
                else:    
                    raise ValueError("Error:\tset_sh_page_num():{}".format(pkt["payload"]["status"]))
                    
                    
                pkt = sensorhub_application.set_sh_iv(msbl_info.nonce)
                if (pkt["payload"]["status"] == CommonStatus.OK):
                    print("Successful:\tset_sh_iv()")
                else:
                    raise ValueError("Error:\tset_sh_iv(): Out of bootloader mode:{}".format(pkt["payload"]["status"]))
                    
                pkt = sensorhub_application.set_sh_authorization(msbl_info.auth)
                if (pkt["payload"]["status"] == CommonStatus.OK):
                    print("Successful:\tset_sh_authorization()")
                else:    
                    raise ValueError("Error:\tset_sh_authorization(). Out of bootloader mode: {}".format(pkt["payload"]["status"]))
                    
                pkt = sensorhub_application.sh_erase_flash()
                if (pkt["payload"]["status"] == CommonStatus.OK):
                    print("Successful:\tsh_erase_flash()")
                else:    
                    raise ValueError("Error:\tsh_erase_flash(): Out of bootloader mode: {}".format(pkt["payload"]["status"]))
                
                pkt = sensorhub_application.sh_init_download_page()
                if (pkt["payload"]["status"] == CommonStatus.OK):
                    print("Successful:\tsh_init_download_page()")
                else:
                    raise ValueError("Error:\tsh_init_download_page():{}".format(pkt["payload"]["status"]))
                    
                start_download_page(sensorhub_application, msbl_info)
                    
                pkt = sensorhub_application.sh_exit_bootloader()
                if (pkt["payload"]["status"] == CommonStatus.OK):
                    print("Successful:\tsh_exit_bootloader()")
                else:
                    raise ValueError("Error:\tsh_exit_bootloader:{}".format(pkt["payload"]["status"]))
                              
            else:
                raise ValueError("Error:\tget_sh_page_size(): Out of bootloader mode:{}".format(pkt["payload"]["status"]))

               
            print("Performing system reset...")
            pm_application.system_hardware_reset()
            time.sleep(POST_HW_RESET_WAIT_SEC)  # Wait for POST_HW_RESET_WAIT_SEC seconds after a hardware reset
            break
            
        except ValueError as e:
            time.sleep(30)
            print("Iteration Count = {} | Error Msg = {}".format(i, e))
            
    else:
        raise Exception("Unable to Load SH FW")

