from cv2 import VideoCapture
from cv2 import namedWindow, resizeWindow
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyWindow
from cv2 import imwrite
from cv2 import CAP_MSMF, WINDOW_NORMAL
import cv2
import os, glob
import numpy as np

import time
import serial # install pyserial
from serial import Serial
import re
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import subprocess

class Microscope():
    def __init__(self):
        self.version = "0.1.1"
        self.video_hardware = None
        self.initialized = False
        self.calibration = None
        return

    def list_cams(self):
        index = 0
        self.cam_numbers = []
        self.resaolution = []
        self.cam_strings = []
        while True:
            cap = VideoCapture(index)
            cam_read = cap.read()
            if not cam_read[0]:
                break
            else:
                for i in range(20):
                    # print(cam_read[0])
                    r = np.array(cam_read[1]).shape
                    self.resaolution.append(r)
                    # namedWindow("cam-test")
                    # imshow("cam-test",cam_read[1])
                    # waitKey(0)
                    # destroyWindow("cam-test")
                    self.cam_numbers.append(index)
            cap.release()
            index += 1
            self.cam_strings.append(
                ("Cam %d"%index) + " Resolution: %d x %d" % (r[0],r[1])
            )

        return self.cam_strings

    def select_cam(self, index):
        try:
            self.video_hardware = VideoCapture(index)
            self.initialized = True
        except Exception as e:
            return str(e)

    def simple_video_stream(self):
        """
        Thread function for streaming unmodified frames
        """

    def start_simple(self):
        '''
        Start simple_video_stream
        '''
        return

    def start_simple(self):
        '''
        Stop simple_video_stream
        '''
        return

    def test_cam(self):
        """
        Test and calibrate the camera.
        """
        try:
            if self.video_hardware is not None:
                for i in range(3):
                    cam_read = self.video_hardware.read()
            else:
                return "No video hardware selected"
        except Exception as e:
            self.initialized = False
            return str(e)
        # vid = cv2.VideoCapture(0) self.video_hardware
        namedWindow("Microscope Calibration", WINDOW_NORMAL)
        resizeWindow("Microscope Calibration", 1280*2, 720*2 )
        def back(*args):
            pass
        cv2.createButton("Back",back,None,cv2.QT_PUSH_BUTTON,1)
        while(True):

            # Capture the video frame
            # by frame
            ret, frame = self.video_hardware.read()

            # Display the resulting frame
            imshow("Microscope Calibration", frame)

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if waitKey(1) & 0xFF == ord('q'):
                break

        # After the loop release the cap object
        # self.video_hardware.release()
        # Destroy all the windows
        destroyWindow("Microscope Calibration")



    def get_frame(self):
        '''
        get a frame from the camera
        '''
        try:
            if self.video_hardware is not None:
                for i in range(3):
                    cam_read = self.video_hardware.read()
            self.initialized = True
        except Exception as e:
            self.initialized = False
            return False
        return cam_read[0]

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
            ports = glob.glob('/dev/tty*')
            for p in ports:
                try:
                    port_name = p
                    scale_name = self.read_serial(p)
                    if scale_name:
                        self.scales_list.append(scale_name)
                        self.ports_list.append(port_name)
                except Exception as e:
                    pass
        if len(self.scales_list )==0:
            return "OS is blocking access to the port or no device connected"

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
