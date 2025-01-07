"""
copyright @ 2025
author: Dada Nanjesha
The provided code includes classes and functions for a robot simulator that involves robot movement,
obstacle avoidance, sensor functionality, and graphics rendering using Pygame.

"""

import pygame
import math
import numpy as np


def point_distance(p1, p2):
    """
    The function calculates the Euclidean distance between two points in a multi-dimensional space.

    :param p1: The `point_distance` function you provided calculates the Euclidean distance between two
        points `p1` and `p2` in n-dimensional space using NumPy
    :param p2: It seems like you have provided the code for calculating the distance between two points
        in a multi-dimensional space using NumPy. However, you have not provided the definition of `p2`.
        Could you please provide the definition of `p2` so that I can assist you further?
    :return: The function `point_distance` calculates the Euclidean distance between two points `p1` and
    `p2` in n-dimensional space and returns the distance as a scalar value.
    """
    p1 = np.array(p1)
    p2 = np.array(p2)
    return np.linalg.norm(p1 - p2)


# This class is named Robot and likely contains attributes and methods related to robots.
class Robot:
    def __init__(self, start_pos, width):
        """
        This function initializes attributes for a robot's position, heading, velocities, and speed
        limits.

        :param start_pos: The `start_pos` parameter seems to represent the starting position of an
            object or entity in a two-dimensional space. It is likely a tuple containing the x and y
            coordinates of the starting position
        :param width: The `width` parameter in the `__init__` method likely represents the width of
            something, such as a vehicle or an object. It is being assigned to the `self.w` attribute within
            the class instance. This width value could be used for calculations or to determine the size or
            dimensions of
        """
        self.m2p = 2779.52
        self.w = width
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.heading = 0

        self.vl = 0.01 * self.m2p
        self.vr = 0.01 * self.m2p

        self.max_speed = 0.02 * self.m2p
        self.min_speed = 0.01 * self.m2p

        self.min_obs_dist = 100
        self.count_down = 5  # seconds

    def avoid_obstacles(self, blank_point, dt):
        """
        This Python function helps a robot avoid obstacles by moving backwards if it is too close to the
        closest obstacle, otherwise it moves forwards.

        :param blank_point: The `blank_point` parameter seems to be a list of points that represent
            obstacles or potential obstacles in the environment. The code snippet provided is trying to find
            the closest obstacle to the current position of the object and take appropriate action based on
            the distance to that obstacle
        :param dt: The `dt` parameter in the `avoid_obstacles` method likely stands for "delta time" and
            is used to represent the time elapsed since the last update. It is commonly used in simulations
            and game development to ensure that movements and calculations are performed consistently
            regardless of the frame rate. By multiplying values
        """
        closest_obs = None
        dist = np.inf

        if len(blank_point) > 1:
            for point in blank_point:
                if dist > point_distance([self.x, self.y], point):
                    dist = point_distance([self.x, self.y], point)
                    closest_obs = (point, dist)

            if closest_obs[1] < self.min_obs_dist and self.count_down > 0:
                self.count_down -= dt
                self.move_backwards()
            else:
                self.count_down = 5
                self.move_forwards()

    def move_backwards(self):
        """
        The function `move_backwards` sets the robot's right wheel speed to the negative minimum speed
        and the left wheel speed to half of the negative minimum speed.
        """
        self.vr = -self.min_speed
        self.vl = -self.min_speed / 2

    def move_forwards(self):
        """
        The function `move_forwards` sets the left and right wheel speeds to the minimum speed for
        moving forwards.
        """
        self.vl = self.min_speed
        self.vr = self.min_speed

    def kinematics(self, dt):
        """
        The function updates the position and heading of a robot based on its velocities and wheel
        speeds over a given time interval.

        :param dt: The `dt` parameter in the `kinematics` function represents the time step or time
            interval over which the robot's kinematics are being updated. It is typically the small amount
            of time that elapses between each update of the robot's position and orientation based on its
            current velocities (`vl` and
        """
        self.x += (self.vl + self.vr) / 2 * math.cos(self.heading) * dt
        self.y -= (self.vl + self.vr) / 2 * math.sin(self.heading) * dt
        self.heading += (self.vr - self.vl) / self.w * dt

        if self.heading > 2 * math.pi or self.heading < -2 * math.pi:
            self.heading = 0

        self.vr = max(min(self.max_speed, self.vr), self.min_speed)
        self.vl = max(min(self.max_speed, self.vl), self.min_speed)


# This class likely contains methods and attributes related to graphics and visual elements.
class Graphics:

    def __init__(self, dimensions, robot_img_path, map_img_path):
        """
        The function initializes a pygame window for a robot simulator with specified dimensions and
        loads images for the robot and map.

        :param dimensions: The `dimensions` parameter in the `__init__` method is used to specify the
            height and width of the display window for the robot simulator. It is a tuple containing two
            values - the height and width of the display window in pixels
        :param robot_img_path: The `robot_img_path` parameter in the `__init__` method is a string that
            represents the file path to the image file of the robot that will be displayed in the
            simulation. This image will be loaded using pygame's `pygame.image.load()` function to create a
            surface object for the robot
        :param map_img_path: The `map_img_path` parameter in the `__init__` method is a string that
            represents the file path to the image file that will be loaded as the map background for the
            robot simulator. This image will be displayed on the pygame window where the robot will navigate
        """

        pygame.init()

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)

        self.robot_img = pygame.image.load(robot_img_path)
        self.map_img = pygame.image.load(map_img_path)

        self.height, self.width = dimensions

        pygame.display.set_caption("obstacles avoiding Robot Simulator")
        self.map = pygame.display.set_mode((self.width, self.height))
        self.map.blit(self.map_img, (0, 0))

    def draw_robot(self, x, y, heading):
        """
        This function draws a robot image on a map at a specified position and heading angle.

        :param x: The `x` parameter in the `draw_robot` function represents the x-coordinate of the
            position where the robot will be drawn on the screen or map. It specifies the horizontal
            position of the robot within the coordinate system
        :param y: The `y` parameter in the `draw_robot` function represents the y-coordinate of the
            position where the robot will be drawn on the screen. It determines the vertical position of the
            robot within the game or application window
        :param heading: The `heading` parameter in the `draw_robot` function represents the direction in
            which the robot is facing. It is typically an angle in radians that specifies the orientation of
            the robot. The function uses this heading to rotate the robot image before drawing it on the
            screen
        """
        rotated = pygame.transform.rotozoom(self.robot_img, math.degrees(heading), 1)
        rect = rotated.get_rect(center=(x, y))
        self.map.blit(rotated, rect)

    def draw_sensor_date(self, blank_point):
        """
        This function draws red circles representing sensor data points on a map using Pygame.

        :param blank_point: The `blank_point` parameter is a list of points where circles will be drawn
            on the map. Each point in the list represents the center of a circle to be drawn
        """
        for point in blank_point:
            pygame.draw.circle(self.map, self.red, point, 3, 0)


# This class likely represents an ultrasonic sensor and its functionality.
class Ultrasonic:

    def __init__(self, sensor_range, map):
        """
        The function initializes the sensor range and map attributes, as well as retrieves the width and
        height of the display surface using Pygame.

        :param sensor_range: The `sensor_range` parameter in the `__init__` method likely represents the
            range of a sensor in your code. This value could indicate how far the sensor can detect objects
            or obstacles in the environment. It is important for determining the functionality and behavior
            of the sensor within your program
        :param map: The `map` parameter in the `__init__` method likely refers to a map or grid that the
            object will interact with. It could be a representation of a game level, a maze, or any other
            environment where the object will navigate or interact with. The map could be a 2
        """
        self.sensor_range = sensor_range
        self.map = map
        self.map_width, self.map_height = pygame.display.get_surface().get_size()

    def sense_obstacles(self, x, y, heading):
        """
        This function calculates the positions of obstacles within the sensor range of a robot based on
        its current position and heading.

        :param x: The `x` parameter in the `sense_obstacles` function represents the x-coordinate of the
            current position of the robot in the map grid. It is used to calculate the starting point for
            the sensor range and to determine the x-coordinate of the potential obstacles detected by the
            sensor
        :param y: The `y` parameter in the `sense_obstacles` function represents the current
            y-coordinate of the robot's position in the environment. It is used to calculate the position of
            potential obstacles based on the robot's heading and sensor range
        :param heading: The `heading` parameter represents the current direction in which the agent is
            facing. It is used to calculate the start and finish angles for the sensor range in the
            `sense_obstacles` method. The sensor range is defined by `self.sensor_range[1]`, which is
            subtracted from the heading
        :return: The function `sense_obstacles` returns a list of coordinates representing the locations
            of obstacles detected by the sensor within the specified sensor range and heading.
        """
        obstacles = []
        x1, y1 = x, y
        start_angle = heading - self.sensor_range[1]
        finish_angle = heading + self.sensor_range[1]
        for angle in np.linspace(start_angle, finish_angle, 10, False):
            x2 = x1 + self.sensor_range[0] * math.cos(angle)
            y2 = y1 - self.sensor_range[0] * math.sin(angle)
            for i in range(0, 100):
                u = i / 100
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                if x < 0 or x < self.map_width or y < 0 or y < self.map_height:
                    color = self.map.get_at((x, y))
                    self.map.set_at((x, y), (0, 208, 255))
                    if color[0] == 0 and color[1] == 0 and color[2] == 0:
                        obstacles.append((x, y))
                        break
        return obstacles
