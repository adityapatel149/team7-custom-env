from highway_env.vehicle.kinematics import Vehicle
from highway_env.road.road import Road
import numpy as np
from highway_env.vehicle.objects import Obstacle, RoadObject
import highway_env.utils as utils   
from custom_env.vehicle.Pothole import Pothole 

class GhostVehicle(Vehicle):
    """
    A ghost vehicle near the target vehicle
    A Vehicle-like object without physical motion or control logic.

    """

    DEFAULT_INITIAL_DEGREE = [0, 180]
    """ Range for random initial position around target vehicle [degree] """
    MAX_SPEED = 200
    """ Maximum apparent speed of the ghost vehicle [m/s] """
    MIN_SPEED = -200
    """ Minimum apparent speed of the ghost vehicle [m/s] """


    def __init__(self, road, position, heading = 0, speed = 0, target_vehicle: Vehicle=None, degree = 90.0, distance = 10.0):
        super().__init__(road, position, heading, speed, predition_type = "zero_steering")
        
        # Vehicle around which ghost vehicle will appear
        self.target_vehicle = target_vehicle 
        # Position relative to target vehicle [degree] (0-> right, 90-> front, 180-> left)
        self.degree = degree 
        # distance from target vehicle [m]
        self.distance = distance 


        self.check_collisions = False # Do not check its own collisions
        self.collidable = False # Disable collision with other collidables
        self.solid = True # For Lidar Observation 
    
    # @classmethod    
    # def create_random(
    #     cls,
    #     road: Road,
    #     speed: float = None,
    #     lane_from: str | None = None,
    #     lane_to: str | None = None,
    #     lane_id: int | None = None,
    #     spacing: float = 1,
    # ) -> GhostVehicle:
    #     v= cls()
    #     return v

    def step(self, dt):
        """ 
        Update position to stay near the target vehicle
        """
        if self.target_vehicle:
            # Follow target_vehicle
            target_pos = self.target_vehicle.position
            self.position = target_pos + np.array([10.0, 5.0])
            self.heading = self.target_vehicle.heading

    # def act(self, action = None):
    #     # disable any driving behavior
    #     pass


    
    def _is_colliding(self, other, dt):
        # Fast spherical pre-check
        if (
            np.linalg.norm(other.position - self.position)
            > (self.diagonal + other.diagonal) / 2 + self.speed * dt
        ):
            return (
                False,
                False,
                np.zeros(
                    2,
                ),
            )
        # Accurate rectangular check
        
        results = utils.are_polygons_intersecting(
            self.polygon(), other.polygon(), self.velocity * dt, other.velocity * dt
        )
        results = list(results)
        results[-1] = np.zeros(2)    

        return results
    

    
    def handle_collisions(self, other: RoadObject, dt: float = 0) -> None:
        """
        Check for collision with another vehicle.

        :param other: the other vehicle or object
        :param dt: timestep to check for future collisions (at constant velocity)
        """
        if other is self or not (self.check_collisions or other.check_collisions):
            return
        if not (self.collidable and other.collidable):
            return
        intersecting, will_intersect, transition = self._is_colliding(other, dt)
        
        if isinstance(other, Pothole):
            print("Ghost Vehicle collided with Pothole")
            
            if will_intersect:
                if self.solid and other.solid:
                    if isinstance(other, Obstacle):
                        self.impact = None
                    elif isinstance(self, Obstacle):
                        other.impact = None
                    else:
                        # self.impact = transition / 2
                        # other.impact = -transition / 2
                        self.impact = None
                        other.impact = None
                        other.speed = 0.0
            if intersecting:
                if self.solid and other.solid:
                    self.crashed = False
                    other.crashed = False
                if not self.solid:
                    self.hit = False
                if not other.solid:
                    other.hit = False




