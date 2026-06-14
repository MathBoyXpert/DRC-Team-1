import pid
from gpiozero import AngularServo

SERVO_MIN = -135
SERVO_MAX = 135

MIN_STEERING_ANGLE = -75
MAX_STEERING_ANGLE = 75
SERVO_PIN = 9 #GONNA GUESS 9 FOR NOW
class SteeringController:
    radius = 46 # radius of the servo arm in mm
    
    def __init__(self):
        self.servo = AngularServo(SERVO_PIN, min_angle = MIN_STEERING_ANGLE, max_angle=MAX_STEERING_ANGLE)


    def steer_servo(self, target_angle):
        # target angle is in degrees
        """
        Gonna type this out because im gonna go insane from the math

        - SO, we are assuming the target angle will be in radians, because I think 
        the PID will do better more accurate math if its in radians

        - With that, we have to convert this into degrees, actually we dont because the 
        AngularServo class being used takes a value from -1 to +1, meaning we have to 
        get it as a fraction and offset it by -1 so it is within that range

        - MG996R servo has a range of 270 degrees iirc, but we only want to use 180
        but the problem is IDK which side of the servo is the min and max

        - so the fraction is over 270
        - the centre position of the servo is at either 90 (for min)or 180 (max) 
        
        so formula should be:

        (target_angle + 90 degrees) / 270 for min

        (270 - (180 - target_angle) / 270 for max

        but what if the PID expects a larger turning angle than the bounds of the servo?
        - We make it take the min of the pid angle and the max angle, 
        and the max of the min angle the resulting angle, 

        -90 < x < 90
        angle = min(x, 90)  -> less than 90
        max(angle, -90) -> more than -90

        OH MY FUCKING GOD ITS THE FUCKING TURNING ANGLE OF THE ACKERMANN NOT THE SERVO KMS

        So now we need to do a cos (JOKES ITS A SINE) transformation?
             /| <- Theta is in that corner
          r / |
           /__|
            d
        so that means... sin(theta) = d/r
            where
                r = radius of servo horn
                d = distance moved 
                theta = arcsin(d/r)
        therefore bruh i need the length of the side legs of the ackermann
             look at the bloody triangle again im not bothered making another
             but the turning angle is determined by d 
             therefore it should be the same right? fuck it ill trust its the same for now and debug later
        """
        servo_angle = max(MIN_STEERING_ANGLE, min(MAX_STEERING_ANGLE, target_angle))
        
        # Going to assume min 
        servo_value = ((servo_angle - 90) / (SERVO_MAX - SERVO_MIN)) - 1.0

        # Just to check if my math is wrong
        servo_value = max(SERVO_MIN, min(SERVO_MAX, servo_value))

        self.servo.value = servo_value

        return servo_angle
