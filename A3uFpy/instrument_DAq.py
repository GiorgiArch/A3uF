from cv2 import VideoCapture
from cv2 import namedWindow
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyWindow
from cv2 import imwrite
from cv2 import CAP_MSMF
import os
import numpy as np

class Microscope():
    def __init__(self):
        self.version = "0.1.1"
        self.video_hardware = None
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
        except Exception as e:
            return str(e)

    def test_cam(self):
        try:
            if self.video_hardware is not None:
                for i in range(3):
                    cam_read = self.video_hardware.read()
            else:
                return "No video hardware selected"

            namedWindow("Microscope Test")
            imshow("Microscope Test",cam_read[1])
            waitKey(0)
            destroyWindow("Microscope Test")
        except Exception as e:
            return str(e)
