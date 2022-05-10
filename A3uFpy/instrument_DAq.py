import time
import serial # install pyserial
from serial import Serial
import re
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import os
import subprocess

class Scale():
    '''
    Acquire data from the scale XXX.
    '''
    def __init__(self):
        self.initialized = False
        self.scales_list = []
        self.ports_list = []
        self.serial_port = None

    def read_serial(self, port):
        ser = Serial(
            port=port,
            baudrate=2400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS,
            xonxoff=False,
            timeout = 0.1
        )

        # print(ser.isOpen())
        ser.write(("PSN\r\n").encode('utf-8'))
        # print('msg sent')
        time.sleep(0.1)
        result = (ser.read(300)).decode()
        # print('result')
        if len(result)>1:
            return "OHAUS " + ''.join(c for c in result if c.isdigit())
        else:
            return None

    def list_available_scales(self):
        '''
        Scan all the ports on unix and windows and report which is connected to a scale.
        '''
        self.scales_list = []
        self.ports_list = []
        if os.name == 'nt':
            # BUILD WINDOWS COMMAND TO LIST ALL SERIAL TO USB ADAPTERS
            cmd_args = []
            cmd_args.append("wmic")
            cmd_args.append("path")
            cmd_args.append("CIM_LogicalDevice")
            cmd_args.append("get")
            cmd_args.append("/value")
            # print(cmd_args)
            win32_string = subprocess.run(cmd_args, stdout=subprocess.PIPE, shell=True)
            all_devices_raw = str(win32_string.stdout)
            all_devices = all_devices_raw.split("Availability=")
            for d in all_devices:
                if  d.find("Description=USB Serial Port")!=-1:
                    a = d.find("COM")
                    port_name = d[a:a+4]
                    scale_name = self.read_serial(port_name)
                    if scale_name:
                        self.scales_list.append(scale_name)
                        self.ports_list.append(port_name)
        else:
            print("OS not recognized")

        return self.scales_list

    def read(self):
        if self.initialized:
            self.serial_port.write(("IP\r\n").encode('utf-8'))
            time.sleep(0.1)
            recv_string = (self.serial_port.read(3000)).decode()
            # print(recv_string)
            for x in recv_string.split("\n"):
                if x.find("mg")!=-1:
                    result = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", x)[0]
            result =  float(result)
        else:
            result = None

        return result

    def initialize(self, scale_name):
        '''
        Initialize the serial connection to the scale
        '''
        port = self.ports_list[self.scales_list.index(scale_name)]
        self.serial_port = Serial(
            port=port,
            baudrate=2400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS,
            xonxoff=False,
            timeout = 0.5
        )
        self.initialized = True



class Microscope():
    '''
    Acquire data from the microscope. The hardware is identified as a webcam.
    '''
    def __init__(self):
        self.serial_address = ""
        self.initialized = False

    def initialize(self):
        '''
        Initialize the serial connection to the Microscope
        '''
        if ping_scale:
            self.initialized = True
        else:
            self.initialized = False
        return self.initialized
