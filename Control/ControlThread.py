import sys
from gpiozero import PhaseEnableMotor
from time import time, sleep
from sshkeyboard import listen_keyboard, stop_listening
import busio
import numpy as np
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

sys.path.insert(1, "/home/fast/DRC-Team-1/Vision/Utils/") # for the pi
sys.path.insert(1, "C:/Users/anshg/Downloads/University/DRC/DRC-Team-1/Vision/Utils") # for local dev
import config

class PID:
    def __init__(self):
        self.kp = config.STEERING_KP
        self.ki = config.STEERING_KI
        self.kd = config.STEERING_KD
        self.setpoint = config.WIDTH // 2 # this tells the set point of the controller to be the cnetre of the image
        self.last_error = 0
        self.integral = 0
        self.last_time = time()

    def update(self, measurement):
        now = time()
        dt = now - self.last_time
        if dt <= 0:
            dt = 1e-3  # prevent division by zero

        error = self.setpoint - measurement
        self.integral += error * dt
        derivative = (error - self.last_error) / dt
        
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.last_error = error
        self.last_time = now
        return output

class AckermannRobot:
    def __init__(self):
        # set the motor pins
        self.drive_motor_left = PhaseEnableMotor(config.DRIVE_MOTOR_DIR1, config.DRIVE_MOTOR_PWM1)
        self.drive_motor_right = PhaseEnableMotor(config.DRIVE_MOTOR_DIR2, config.DRIVE_MOTOR_PWM2)
        
        i2c = busio.I2C(config.STEERING_SERVO_SCL_PIN, config.STEERING_SERVO_SDA_PIN)
        pca = PCA9685(i2c)
        pca.frequency = 50
        self.steering_servo = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500, actuation_range=270)


        # initialise PID for steering
        self.pid = PID()

    def set_steering(self, cx, curr_speed):
        """
        Adjust steering angle based on the centroid x-coordinate from vision.
        cx: Centroid X from track line filter (NOTE this must be 0-config.WDITH aka 0-640).
        """
        if cx is None:
            # if no line is detected keep steering at the center (aka straight)
            self.curr_angle = config.STEERING_CENTER
            self.steering_servo.angle = self.curr_angle
            return

        # Calculate PID output
        og_correction = self.pid.update(cx)
        print(f"The current PID correction pixel is: {og_correction}")

        correction = og_correction / (config.WIDTH / 2)
        
        servo_value = correction * config.STEERING_MAX_ANGLE 
        servo_value = config.STEERING_CENTER + servo_value
        # angle: [85-210]
        # Constrain to servo limits just incase
        servo_value = max(config.STEERING_MAX_RIGHT, min(config.STEERING_MAX_LEFT, servo_value))
        
        print(f"Current servo angle: {servo_value}")
        self.curr_angle = servo_value
        self.steering_servo.angle = self.curr_angle

        # activate differnetial steering if the turn is even sharper if unable to make the turn
        if og_correction < config.PID_CONSTANT_NEEDED_TO_MAX_RIGHT_STEERING_ANGLE:
            print("Right Correction Differential Activated!!")
            self.drive_motor_right.forward(config.BASE_SPEED)
            self.drive_motor_left.forward(config.BASE_SPEED)
        elif og_correction > config.PID_CONSTANT_NEEDED_TO_MAX_LEFT_STEERING_ANGLE:
            print("Left Correction Differential Activated!!")
            self.drive_motor_left.backward(config.BASE_SPEED)
            self.drive_motor_right.backward(config.BASE_SPEED)
        else:
            print("Differential Dectivated..")
            self.drive(config.BASE_SPEED)


    def adjust_servo(self, angle):
        """
        adjust the servo from the current position to a new position (through addition)
        value: value between 0 and 270
        """
        print(f"before: {self.steering_servo.angle} stuff to add: {angle}")
        self.curr_angle = max(config.STEERING_MAX_RIGHT, min(config.STEERING_MAX_LEFT, angle + self.steering_servo.angle))
        self.steering_servo.angle = self.curr_angle
        print(f"after: {self.steering_servo.angle}")


    def set_servo(self, angle):
        """
        Set the servo from the current position to a new position (through hard setting it)
        value: value between 0 and 270
        """

        self.curr_angle = max(config.STEERING_MAX_RIGHT, min(config.STEERING_MAX_LEFT, angle))
        self.steering_servo.angle = self.curr_angle

    def drive(self, speed):
        """
        drive forward or backward.
        speed: value between -1 and 1
        """
        if speed > 0:
            self.drive_motor_left.backward(abs(speed))
            self.drive_motor_right.forward(abs(speed))
        elif speed < 0:
            self.drive_motor_left.forward(abs(speed))
            self.drive_motor_right.backward(abs(speed))
        else:
            self.drive_motor_left.stop()
            self.drive_motor_right.stop()

    def stop(self):
        self.drive_motor_left.stop()
        self.drive_motor_right.stop()
        self.curr_angle = config.STEERING_CENTER
        self.steering_servo.angle = self.curr_angle
    
    def manual_drive_mode(self):
        print("\n--- Manual Control Activated ---")
        print("Use W/S to drive, A/D to steer, press Q to quit")
        self.pressed = False

        
        def press(key):
            if key == 'w':
                self.drive(0.3)
            
            elif key == 's':
                self.drive(-0.3)

            elif key == 'a':
                self.adjust_servo(-5)

            elif key == 'd':
                self.adjust_servo(5)
            
            elif key == 'q':
                print("\nExiting Manual Control...")
                stop_listening()

        def release(key):
            # when you lift your finger off the robot stops
            if key in ['w', 's']:
                self.drive(0)


        # starts the keyboard listener in the terminal
        listen_keyboard(on_press=press, on_release=release)
        self.stop()

def navigate_with_pid(cx, speed=0.5):
    """
    Main navigation function to be called from the vision loop.
    cx: Centroid X of the track line.
    """
    robot.set_steering(cx)
    robot.drive(speed)
    
if __name__ == "__main__":
    # Test drive
    robot = AckermannRobot()



    robot.manual_drive_mode()
    # for i in range(85, 210, 1):
    #     robot.adjust_servo(i)
    #     sleep(0.05)
    
    # robot.set_servo(config.STEERING_MAX_LEFT)
    # sleep(1)
    # robot.set_servo(config.STEERING_CENTER)
    # sleep(1)



    # robot.drive(0)
    # robot.drive_motor1.backward(0.2)
    # sleep(1)
    # robot.drive(0)
    # robot.drive_motor2.backward(0.2)
    # sleep(1)
    robot.drive(0)


