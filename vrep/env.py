# Import Libraries:
import vrep
import sys
import time
import numpy as np
import math
import matplotlib.pyplot as plt


class RlBot(object):
    def __init__(self):
        # just in case, close all opened connections
        vrep.simxFinish(-1)

        self.client_id = vrep.simxStart(
            '127.0.0.1', 19997, True, True, 5000, 5)

        if self.client_id != -1:  # check if client connection successful
            print('Connected to remote API server')
        else:
            print('Connection not successful')
            sys.exit('Could not connect')

        # Restart the simulation
        vrep.simxStopSimulation(self.client_id, vrep.simx_opmode_blocking)
        vrep.simxStartSimulation(self.client_id, vrep.simx_opmode_blocking)

        # Get handles
        self.get_handles()

    def get_handles(self):
        # retrieve motor  handles
        _, self.left_motor_handle = vrep.simxGetObjectHandle(
            self.client_id, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_blocking)
        _, self.right_motor_handle = vrep.simxGetObjectHandle(
            self.client_id, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_blocking)

        # empty list for handles
        self.proxy_sensors = []

        # for loop to retrieve proxy sensor arrays and initiate sensors
        for i in range(16):
            _, sensor_handle = vrep.simxGetObjectHandle(
                self.client_id, 'ultrasonic_sensor#' + str(i),
                vrep.simx_opmode_blocking)
            # Append to the list of sensors
            self.proxy_sensors.append(sensor_handle)

        # empty list for handles
        self.light_sensors = []

        # for loop to retrieve light sensor arrays and initiate sensors
        for i in range(8):
            _, sensor_handle = vrep.simxGetObjectHandle(
                self.client_id, 'light_sensor#' + str(i),
                vrep.simx_opmode_blocking)
            # Append to the list of sensors
            self.light_sensors.append(sensor_handle)

    def distroy(self):
        vrep.simxStopSimulation(self.client_id, vrep.simx_opmode_blocking)

    def reset(self):
        # Restart the simulation
        vrep.simxStopSimulation(self.client_id, vrep.simx_opmode_blocking)
        vrep.simxStartSimulation(self.client_id, vrep.simx_opmode_blocking)

    def step(self, action):
        # Activate the motors
        vrep.simxSetJointTargetVelocity(
            self.client_id, self.left_motor_handle, action[0], vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(
            self.client_id, self.right_motor_handle, action[1], vrep.simx_opmode_blocking)

        # Get observations
        observations = {}
        observations['proxy_sensor'] = []
        observations['light_sensor'] = []

        # Fetch the vals of proxy sensors
        for sensor in self.proxy_sensors:
            _, _, detectedPoint, _, _ = vrep.simxReadProximitySensor(
                self.client_id, sensor, vrep.simx_opmode_blocking)
            # Append to list of values
            observations['proxy_sensor'].append(
                np.linalg.norm(detectedPoint))

        # Fetch the vals of light sensors
        for sensor in self.light_sensors:
            # Fetch the initial value in the suggested mode
            _, _, image = vrep.simxGetVisionSensorImage(
                self.client_id, sensor, 1, vrep.simx_opmode_blocking)
            # Append to the list of values
            observations['light_sensor'].append(image)

        # vrep gives a positive value for the black strip and negative for the
        # floor so convert it into 0 and 1

        observations['light_sensor'] = np.asarray(
            observations['light_sensor'])
        observations['light_sensor'] = observations['light_sensor'].reshape(-1)
        mask = observations['light_sensor'] > 0
        observations['light_sensor'][:] = 0
        observations['light_sensor'][mask] = 1

        # Assign reward
        reward = {}

        # For light sensors

        # If any of the center 2 sensors is 1 give high reward
        if np.sum(observations['light_sensor'][[3, 4]]) > 0:
            reward['light_sensor'] = 3
        # If any of second, third, sixth or seventh is 1
        elif np.sum(observations['light_sensor'][[1, 2, 5, 6]]) > 0:
            reward['light_sensor'] = 1
        # If first or last are high
        elif np.sum(observations['light_sensor'][[0, 7]]) > 0:
            reward['light_sensor'] = 0
        # Bot is completly out of line
        else:
            reward['light_sensor'] = -2

        # For proximity sensors
        reward['proxy_sensor'] = 0

        # Should be rewarded for quick movement
        r = action[0] + action[1]
        # But no more than 2
        if r > 2:
            r = 2

        reward['light_sensor'], reward['proxy_sensor'], reward['combined'] += r

        return observations, reward
