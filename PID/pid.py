import numpy as np
import time

class PID:    

    def __init__(self, kp, ki, kd):

        # Changable Coefficients - Should be set by config then be changeable
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)

        # Initialising Vars of New Controller
        self.target = 0         # What the controller wants the end to be at
        self.integral = 0       # Integral for the small error correction - I
        self.prev_error = 0     # Previous error - D 
        self.prev_time = time.time()


    def set_desired(self, target):
        self.target = target

    def compute(self, curr, dt):    
        # curr is the current angle the drc is facing
        # dt is delta time, so the difference in time between this cycle and prev 
        now = time.time()
        dt = now - self.prev_time
        if dt <= 0: 
            dt = 1e-6 # so as to not divide by 0, also should be positive
        """
         Going to make the angle calculations in radians, as it seems like its 
         the more viable option for calculation
        """

        curr_rad = np.deg2rad(curr)
        error = self.target - curr_rad

        # P calculations
        P = self.kp * error

        # I calculations
        self.integral += error * dt
        I = self.ki * self.integral

        # D calculations 
        derivative = (error - self.prev_error) / dt
        D = self.kd * derivative

        output = P + I + D
        self.prev_error = error
        
        output = np.rad2deg(output) # so it outputs the target angle in deg? hopefully this works
        return output




    

