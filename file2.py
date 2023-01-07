from __future__ import print_function

#Finding Carla Module
import glob
import os
import sys
import random
import time
import numpy as np
import cv2
try:
    sys.path.append(glob.glob(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla
actor_list = []
IM_WIDTH = 640
IM_HEIGHT = 480

def process_img(img):
    i = np.array(img.raw_data)
    i2 = i.reshape((IM_HEIGHT,IM_WIDTH,4))
    i3 = i2[:,:,:3] #drop the 4th channel "a" of rgba
    cv2.imshow("",i3)
    cv2.waitKey(1)
    return i3/255.0