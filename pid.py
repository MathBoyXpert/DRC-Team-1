#!/usr/bin/env python

def pid(Kp, Ki, Kd, setpoint, measurement):
    global time, integral, time_prev, e_prev

    offset = 320

    e = setpoint - measurement

    # PID calculations
    ## Note: We need to tune these Parameters during testing
    ## Start by tuning P first and then tuning I and D afterwards
    prop = Kp*e
    integral = integral + Ki*e*(time - time_prev)
    der = Kd*(e - e_prev)/(time - time_prev)

    MV = offset + prop + integral + der

    e_prev = e
    time_prev = time

    return MV
if __name__=="__main__":
    pid()