from __future__ import print_function
#Imports transferred over from other files.
import glob
import os
import sys
import random
import time
import numpy as np
import cv2
import math
try:
    sys.path.append(glob.glob(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

#The image rendering dimensions (set arbitrarily).
IM_WIDTH = 640
IM_HEIGHT = 480
SHOW_PREVIEW = False
SECONDS_PER_EPISODE = 10

#The class responsible for setting up a basic car environment, that can read sensory data and take an arbitrary action upon it (a step function).
class CarEnv:
    #initialize environment variables
    SHOW_CAM = SHOW_PREVIEW
    STEER = 1.0
    im_width = IM_WIDTH
    im_height = IM_HEIGHT
    front_camera = None

    #constructor to construct a basic environment object
    def __init__(self):
        #connection details by carla
        self.client = carla.Client("localhost",2000)
        self.client.set_timeout(4.0)
        self.world = self.client.get_world()
        self.blueprint_library = self.world.get_blueprint_library()

        #arbitrary car model for testing
        self.model_3 = self.blueprint_library.filter("model3")[0]
    
    #equivalent of a destructor
    def reset(self):
        #reset historical values of collisions and respawn vehicle
        self.collision_hist = []
        self.actor_list = []
        self.transform = random.choice(self.world.get_map().get_spawn_points())
        self.vehicle = self.world.spawn_actor(self.model_3, self.transform)
        self.actor_list.append(self.vehicle)

        #reset sensors
        self.rgb_cam = self.blueprint_library.find('sensor.camera.rgb')
        self.rgb.set_attribute("image_size_x", f"{self.im_width}")
        self.rgb.set_attribute("image_size_y", f"{self.im_height}")

        #arbitrary field of view
        self.rgb.set_attribute("fov", f"110")
        
        #arbitray relative position of sensor to car, position stored in transform
        transform = carla.Transform(carla.Location(x=2.5, y=0.7))
        self.sensor = self.world.spawn_actor(self.rbg_cam, transform, attach_to=self.vehicle)
        self.actor_list.append(self.sensor)
        self.sensor.listen(lambda data: self.process_img(data))

        self.vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=0.0))
        #sleep so that it doesnt quit right away
        time.sleep(4)

        colsensor = self.blueprint_library("sensor.camera.collision")
        self.colsensor = self.world.spawn_actor(colsensor,transform,attach_to=self.vehicle)
        self.actor_list.append(self.cols)
        self.sensor.listen(lambda event: self.collision_data(event))

        while self.front_camera is None:
            time.sleep(0.01)
        self.episode_start = time.time()
        self.vehicle.apply_control(carla.vehicleControl(throttle=0.0,brake=0.0))

        return self.front_camera
    def collision_data(self, event):
        self.collision_hist.append(event)
    
    def process_img(self,img):
        i = np.array(img.raw_data)
        i2 = i.reshape((self.im_height,self.im_width,4))
        i3 = i2[:,:,:3] #drop the 4th channel "a" of rgba
        if self.SHOW_CAM:
            cv2.imshow("",i3)
            cv2.waitKey(1)
        self.front_camera = i3
    def step(self, action): 
        if action == 0:
            self.vehicle.apply_control(carla.vehicleControl(throttle=1.0,steer=-1*self.STEER))
        elif action == 1:
            self.vehicle.apply_control(carla.vehicleControl(throttle=1.0,steer=0*self.STEER))
        elif action == 2:
            self.vehicle.apply_control(carla.vehicleControl(throttle=1.0,steer=1*self.STEER))
        v = self.vehicle.get_velocity()
        #vector to scalar
        kmh = int(3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2))
        #arbitrary rewards, can be adjusted later
        if len(self.collision_hist) != 0:
            done = True
            reward = -200
        elif kmh < 50:
            done = False
            reward = -1
        else:
            done = False
            reward = 1
        if self.episode_start + SECONDS_PER_EPISODE < time.time():
            done = True
        return self.front_camera, reward, done, None
