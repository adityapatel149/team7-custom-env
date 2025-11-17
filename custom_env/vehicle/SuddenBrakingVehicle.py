from highway_env.vehicle.behavior import IDMVehicle
import numpy as np

#Custom class for Sudden Braking Vehicle
class SuddenBrakingVehicle(IDMVehicle):
    COMFORT_ACC_MAX = 45
    COMFORT_ACC_MIN = -150

    def act(self, action= None):
        if np.random.rand() < 0.01:
            self.color = (255,0, 0)
            self.target_speed = -200 #Sudden stop
        if self.speed < 5:
            self.target_speed = 45 #Normal behavior
            self.color = (0,0,255)
           
        super().act(action)