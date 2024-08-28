# SpO2 Watch Python SDK

The adi-spo2-watch provides an object-oriented interface for interacting with ADI's VSM Study Watch 4.5 platform (SpO2 Watch).

**Installation**

```python
pip install adi-spo2-watch
```
**Description**

A user application can use the SDK to receive complete packets of bytes over a physical interface (USB or BLE) and
decode it. The functionality is organized into applications, some of which own sensors, some own system-level
functionality (i.e. file system), and while others own algorithms. The hierarchy of objects within the SDK mirrors the
applications present on the device. Each application has its own object within the SDK hierarchy, which is used to
interact with that application. A brief guide on using the SDK and few examples have been added below.

**Firmware Setup**

https://github.com/analogdevicesinc/spo2-watch-sdk/blob/main/firmware/Firmware_update_guide.pdf

**Getting started with SDK**

Import the adi-spo2-watch module into your application code
```python
from adi_spo2_watch import SDK
```
Instantiate the SDK object by passing the com port number
```python
sdk = SDK('COM28')
```
The application objects can be instantiated from the sdk object. In order to instantiate an application object, we'll
have to pass a call-back function as an input argument which can be used to retrieve the data from the application
object. Define a callback function as displayed below.
```python
def callback_data(data):
    print(data)
```
Once the call-back function is defined, you can instantiate the application object as shown below.
```python
application = sdk.get_sensorhub_application()
application.set_callback(callback_data, stream=application.SH_ADXL_STREAM)
```
Each application object has various methods that can be called by referring to the application. Almost all method in 
an application returns result in a dict.


**Basic Example:**

```python
import time
from datetime import datetime
from adi_spo2_watch import SDK

# Callback function to receive adxl data
def callback_data(data):
    sequence_number = data["payload"]["sequence_number"]
    for stream_data in data["payload"]["stream_data"]:
        dt_object = datetime.fromtimestamp(stream_data['timestamp'] / 1000)  # convert timestamp from ms to sec.
        print(f"seq :{sequence_number} timestamp: {dt_object} x,y,z :: ({stream_data['x']}, "
                f"{stream_data['y']}, {stream_data['z']})")


if __name__ == "__main__":
    sdk = SDK("COM4")
    application = sdk.get_sensorhub_application()

    # Quickstart adxl stream
    application.set_callback(callback_data, stream=application.SH_ADXL_STREAM)
    application.enable_csv_logging("adxl.csv", stream=application.SH_ADXL_STREAM) # Logging adxl data to csv file
    application.subscribe_stream(stream=application.SH_ADXL_STREAM)
    application.set_operation_mode(application.SH_CONFIG_ADXL_MODE)
    application.start_sensor()
    time.sleep(10)
    application.stop_sensor()
    application.unsubscribe_stream(stream=application.SH_ADXL_STREAM)
    application.disable_csv_logging(stream=application.SH_ADXL_STREAM)
```

# Permission Issue in Ubuntu

1 - You can run your script with admin (sudo).

2 - If you don't want to run scripts as admin follows the steps below:

- add user to `tty` and `dialout` group

```
sudo usermod -aG tty <user>
sudo usermod -aG dialout <user>
```
- create a file at `/etc/udev/rules.d/` with name `10-adi-usb.rules`:
```
ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="0456", ATTRS{idProduct}=="2cfe", MODE="0666", GROUP="dialout"
```
- reboot

**All streams packet structure :**
https://analogdevicesinc.github.io/spo2-watch-sdk/python/_rst/adi_spo2_watch.core.packets.html#module-adi_spo2_watch.core.packets.stream_data_packets

**Documentation :**
https://analogdevicesinc.github.io/spo2-watch-sdk/python

**Examples :**
https://github.com/analogdevicesinc/spo2-watch-sdk/tree/main/python/samples

**License :**
https://github.com/analogdevicesinc/spo2-watch-sdk/blob/main/LICENSE

**Changelog**
https://github.com/analogdevicesinc/spo2-watch-sdk/blob/main/python/CHANGELOG.md

