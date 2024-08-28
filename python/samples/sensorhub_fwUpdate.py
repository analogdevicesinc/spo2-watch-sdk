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
import os
import sys, getopt
from copy import deepcopy
from ctypes import *

from adi_spo2_watch import SDK
from adi_spo2_watch.core.enums.common_enums import CommonStatus

DEFAULT_PAGE_SIZE = 8192
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


def read_msbl_file(path):
    result = MSBL_FILE_INFO()
   # path = r"../../../sensorhub/build"
    files = os.listdir(path)
    total_size = 0
    file_msbl = [i for i in files if i.endswith('.msbl')]
    if len(file_msbl) == 0:
        print("no msbl file present in " + path)
        return
   # print("msbl being used: {}").format(file_msbl[0])
    file_msbl = [path + str('/') + file_msbl[0]]
    with open(file_msbl[0], 'rb') as f:
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
            else:
                print("Unknown State")
            i += step
            left_over -= step
            if left_over <= 16:
                step = left_over
            temp_page_part.clear()
            page_pkt_counter += 1

def myfunc(argv):
    arg_port = ""
    arg_directory = ""
    arg_help = "{0} -p <port> -d <directory>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hp:d:", ["help", "port=",
                                                         "directory="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-p", "--port"):
            arg_port = arg
        elif opt in ("-d", "--directory"):
            arg_directory = arg

    return arg_port, arg_directory


if __name__ == "__main__":
    portNum, msbl_path = myfunc(sys.argv)

    if(portNum == ""):
        portNum = input("Enter Serial port Num : ")

    if(msbl_path == ""):
        msbl_path = os.getcwd()

    sdk = SDK(portNum)
    sensorhub_application = sdk.get_sensorhub_application()
    sensorhub_application.enter_sh_boot_loader_mode(True)
    sensorhub_application.get_sh_page_size()
    msbl_info = read_msbl_file(msbl_path)
    sensorhub_application.set_sh_page_num(msbl_info.Numberofpages)
    sensorhub_application.set_sh_iv(msbl_info.nonce)
    sensorhub_application.set_sh_authorization(msbl_info.auth)
    sensorhub_application.sh_erase_flash()
    sensorhub_application.sh_init_download_page()
    start_download_page(sensorhub_application, msbl_info)
    sensorhub_application.sh_exit_bootloader()




