import numpy as np
import random
import cv2
import math
import re
from pyax12.connection import Connection
import time
import pywin32_system32
import pyttsx3


# GLOBAL VARIABLE FOR MASKS
GREEN_LOWER_1 = np.array([40, 70, 70], np.uint8)  # green
GREEN_UPPER_1 = np.array([80, 200, 200], np.uint8)  # green

GREEN_LOWER = np.array([40, 30, 30], np.uint8)  # green
GREEN_UPPER = np.array([70, 255, 255], np.uint8)  # green

RED_LOWER = np.array([0, 70, 50], np.uint8)
RED_UPPER = np.array([10, 255, 255], np.uint8)

RED_LOWER_1 = np.array([170, 70, 50], np.uint8)
RED_UPPER_1 = np.array([180, 255, 255], np.uint8)

# BLUE_LOWER = np.array([100, 150, 0], np.uint8) #100
# BLUE_UPPER = np.array([150, 255, 255], np.uint8) #150

MINIMUM_CONTOUR_AREA = 1200
MAXIMUMM_CONTOUR_AREA = 5000
CONTOUR_LIMIT = 20
TOLERANCE = 15

MISSIONARY = "green"
CANNIBAL = "red"

# HARD CODED POSITIONS
POSITION = {
    "L1": [85, 450],
    "L2": [97, 360],
    "L3": [130, 255],
    "L4": [210, 165],
    "L5": [360, 110],
    "L6": [515, 85],
    "R1": [930, 515],
    "R2": [950, 415],
    "R3": [926, 340],
    "R4": [900, 255],
    "R5": [840, 170],
    "R6": [720, 110],
}

SERVO_SPEED = 100

POSSIBLE_POSITIONS = ["L1", "L2", "L3", "L4", "L5", "L6", "R1", "R2", "R3", "R4", "R5", "R6"]

SERVO_SETTING = {"R1": {1: -95.7,
                        2: 48.5,
                        3: 57.6,
                        4: 67.3},
                 "L1": {1: 91.9,
                        2: 50.6,
                        3: 51.2,
                        4: 73.2},
                 "L2": {1: 72.6,
                        2: 51.2,
                        3: 50.9,
                        4: 73.2},
                 "R2": {1: -78.2,
                        2: 48.5,
                        3: 57,
                        4: 67},
                 "L3": {1: 53.5,
                        2: 51.2,
                        3: 50.9,
                        4: 69.8},
                 "R3": {1: -62.6,
                        2: 48.8,
                        3: 56.7,
                        4: 66.7},
                 "L4": {1: 38.6,
                        2: 51.5,
                        3: 50,
                        4: 68.8},
                 "R4": {1: -47.1,
                        2: 51.5,
                        3: 53.5,
                        4: 66.1},
                 "L5": {1: 20.4,
                        2: 51.8,
                        3: 50,
                        4: 68.8},
                 "R5": {1: -31.9,
                        2: 51.5,
                        3: 53.2,
                        4: 66.1},
                 "R6": {1: -16.3,
                        2: 51.5,
                        3: 51.5,
                        4: 66.4},
                 "L6": {1: 4.8,
                        2: 52.1,
                        3: 48.2,
                        4: 68.5}
                 }

