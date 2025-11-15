from highway_env.envs import HighwayEnv
from highway_env.envs.common.action import DiscreteMetaAction
from highway_env.envs.highway_env import Observation
import numpy as np

from highway_env import utils, vehicle
from highway_env.envs.common.abstract import AbstractEnv
# from highway_env.envs import HighwayEnv
from highway_env.road.road import Road, RoadNetwork
from highway_env.vehicle.kinematics import Vehicle
from highway_env.vehicle.controller import ControlledVehicle

from custom_env.vehicle import GhostVehicle


Observation = np.ndarray


class MyEnv(HighwayEnv): 
# class MyEnv(AbstractEnv): # When defining custom functions
    """
    Team 7 custom environment derived from highway-env.
    Currently uses LIDAR observation type and default highway-env behaviour.

    Copied Highway_Env code as is.
    
    """

    @classmethod
    def default_config(cls) -> dict:
        config = super().default_config()
        config.update({
                "observation": {
                    "type": "LidarObservation",
                     "cells": 16
                },
                "action":{
                    "type" : "DiscreteMetaAction",
                },
                "lanes_count": 8,
                "vehicles_count": 50,
                "controlled_vehicles": 1,
                "initial_lane_id": None,
                "duration": 40, #[s]
                "ego_spacing": 2,
                "vehicles_density": 1,
                "collision_reward": -1, # The reward received when colliding with a vehicle.
                "right_lane_reward": 0.1, # The reward received when driving on the right-most lanes, linearly mapped to
                # zero for other lanes.
                "lane_change_reward": 0, # The reward received at each lane change action.
                "high_speed_reward": 0.4, # The reward received when driving at full speed, linearly mapped to zero for
                # lower speeds according to config["reward_speed_range"].
                "speed_limit": 30,
                "reward_speed_range": [20,30],
                "normalize_reward": True,
                "offroad_terminal": False,
            }
        )
        return config

    def _reset(self) -> None:
        self._make_road()
        self._make_vehicles()

    def _make_road(self) -> None:
        """Create a road composed of striaght adjacent lines"""
        self.road = Road(
            network = RoadNetwork.straight_road_network(
                lanes = self.config["lanes_count"], 
                speed_limit = self.config["speed_limit"]
            ),
            np_random = self.np_random,
            record_history = self.config["show_trajectories"],
        )
        
    def _make_vehicles(self) -> None:
        """Create some new rnadom vehicles of a given type, and add them on the road"""
        other_vehicles_type = utils.class_from_path(
            self.config["other_vehicles_type"]
        )
        other_per_controlled = utils.near_split(
            self.config["vehicles_count"], 
            num_bins=self.config["controlled_vehicles"]
        )

        self.controlled_vehicles = []
        for others in other_per_controlled:
            

            # Create controlled Vehicle
            vehicle = Vehicle.create_random(
                self.road,
                speed=25.0,
                lane_id=self.config["initial_lane_id"],
                spacing=self.config["ego_spacing"],
            )
            vehicle = self.action_type.vehicle_class(
                self.road, vehicle.position, vehicle.heading, vehicle.speed    
            )
            self.controlled_vehicles.append(vehicle)
            self.road.vehicles.append(vehicle)
            ghost_vehicle = GhostVehicle(self.road, vehicle.position, target_vehicle = vehicle) # Will use this method to create ghost vehicle
            self.road.vehicles.append(ghost_vehicle) 

            for _ in range(others):
                vehicle = other_vehicles_type.create_random(
                        self.road, spacing=1 / self.config["vehicles_density"]
                )
                vehicle.randomize_behavior()
                self.road.vehicles.append(vehicle)

    def _reward(self, action):
        """Use default reward for now."""
        return super()._reward(action)


    def _is_terminal(self):
        """Use default termination condition."""
        return super()._is_terminal() 
            