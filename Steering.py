
import numpy as np
import math
import time

MAX_ANGLE = 40
MIN_ANGLE = -40

class Steering:

    def compute_steering_angle(control):
        if abs(control) < 10:
            return 0
        
        desired_angle_rad = math.atan2(control)
        desired_angle_deg = math.degrees(desired_angle_rad)

        steering_angle = -max(min(desired_angle_deg, MAX_ANGLE), MIN_ANGLE)
        return steering_angle