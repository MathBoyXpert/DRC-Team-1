#!/usr/bin/env python

class PID:
    time = 0
    integral = 0
    time_prev = -1e-6
    e_prev = 0
    Ki = 0
    Kd = 0
    Kp = 0
    setpoint = 0

    def __init__(self):
        self.setpoint = 0

    ## The selfpoint changes during turns
    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    ## 
    def pid(Kp, Ki, Kd, setpoint, measurement):
        global time, integral, time_prev, e_prev

        ### The error is the current point and the where you want to go
        e = setpoint - measurement

        # PID calculations
        ## Note: We need to tune these Parameters during testing
        ## Start by tuning P first and then tuning I and D afterwards
        prop = Kp * e
        integral = integral + Ki*e*(time - time_prev)
        der = Kd*(e - e_prev)/(time - time_prev)

        # calculate manipulated variable - MV 
        manipulated_var = prop + integral + der

        e_prev = e
        time_prev = time

        return manipulated_var
    

if __name__=="__main__":
    x = PID()
    print(x.pid(0.1, 0.1, 0.1, 0.3))