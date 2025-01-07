"""
copyright @ 2025
author: Dada Nanjesha
This is the main file that runs the simulation of a robot navigating through an environment using
The code snippet you provided is setting up a simulation environment for a robot using the Pygame
library in Python.

"""

import math

import pygame


from robot import Robot, Graphics, Ultrasonic


MAP_DIMES = (600, 1200)

gfx = Graphics(MAP_DIMES, "robot.png", "map3.png")

start = (200, 200)
robot = Robot(start, 0.01 * 2779.52)

sensor_range = 250, math.radians(40)
ultrasonic = Ultrasonic(sensor_range, gfx.map)

dt = 0
last_time = pygame.time.get_ticks()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = (pygame.time.get_ticks() - last_time) / 1000
    last_time = pygame.time.get_ticks()
    gfx.map.blit(gfx.map_img, (0, 0))

    robot.kinematics(dt)
    gfx.draw_robot(robot.x, robot.y, robot.heading)
    point_cloud = ultrasonic.sense_obstacles(robot.x, robot.y, robot.heading)
    robot.avoid_obstacles(point_cloud, dt)
    gfx.draw_sensor_date(point_cloud)

    pygame.display.update()
