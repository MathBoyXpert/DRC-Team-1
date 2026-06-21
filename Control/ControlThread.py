import sys
from gpiozero import Servo, PhaseEnableMotor
from time import time, sleep
from sshkeyboard import listen_keyboard, stop_listening

sys.path.insert(1, "/home/fastandcurious/drcTest/DRC-Team-1/Vision/Utils/") # for the pi
sys.path.insert(1, "C:\Users\anshg\Downloads\University\DRC\DRC-Team-1 - Copy\Vision\Utils") # for local dev
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
        # Initialize hardware
        self.drive_motor1 = PhaseEnableMotor(config.DRIVE_MOTOR_DIR1, config.DRIVE_MOTOR_PWM1)
        self.drive_motor2 = PhaseEnableMotor(config.DRIVE_MOTOR_DIR2, config.DRIVE_MOTOR_PWM2)
        self.steering_servo = Servo(config.STEERING_SERVO_PIN)
        
        # Initialize PID for steering
        self.pid = PID()

    def set_steering(self, cx):
        """
        Adjust steering angle based on the centroid x-coordinate from vision.
        cx: Centroid X from track line filter.
        """
        if cx is None:
            # If no line is detected, keep steering at center or perform search
            self.steering_servo.value = config.STEERING_CENTER
            return

        # Calculate PID output
        correction = self.pid.update(cx)
        
        # Map correction to servo range [-1, 1]
        # PID output needs to be normalized or scaled based on expected error
        # Assuming cx is 0-640, error is up to 320.
        # Simple scaling: divide by half width to get a value roughly in [-1, 1]
        servo_value = config.STEERING_CENTER + (correction / (config.WIDTH / 2))
        
        # Constrain to servo limits
        servo_value = max(config.STEERING_MAX_LEFT, min(config.STEERING_MAX_RIGHT, servo_value))
        
        self.steering_servo.value = servo_value




    def adjust_servo(self, value):
        """
        Adjust the servo from the current position to a new position.
        value: value between -1 and 1.
        """
        self.steering_servo.value += value

    def drive(self, speed):
        """
        Drive forward or backward.
        speed: value between -1 and 1.
        """
        if speed > 0:
            self.drive_motor1.forward(speed)
            self.drive_motor2.forward(speed)
        elif speed < 0:
            self.drive_motor1.backward(abs(speed))
            self.drive_motor2.backward(abs(speed))
        else:
            self.drive_motor1.stop()
            self.drive_motor2.stop()

    def stop(self):
        self.drive_motor1.stop()
        self.drive_motor2.stop()
        self.steering_servo.value = config.STEERING_CENTER
    
    def manual_drive_mode(self):
        print("\n--- Manual Control Activated ---")
        print("Use W/S to drive, A/D to steer. Press 'Q' to quit.")
        
        def press(key):
            if key == 'w':
                self.drive(0.3)  # Adjust speed adjustments here
            elif key == 's':
                self.drive(-0.3)
            elif key == 'a':
                self.adjust_servo(-0.15)
            elif key == 'd':
                self.adjust_servo(0.15)
            elif key == 'q':
                print("\nExiting Manual Control...")
                stop_listening()

        def release(key):
            # When you lift your finger off driving keys, the robot cuts engine power
            if key in ['w', 's']:
                self.drive(0)

        # Starts the operational terminal keyboard listener
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
    while True:
            # checks for an exit input
            user_name = input("Enter dir: ")
            
            if user_name == 'w':
                robot.drive(0.1)
                sleep(1)
                robot.drive(0)

            if user_name == 's':
                robot.drive(-0.1)
                sleep(1)
                robot.drive(0)
                
            if user_name == 'a':
                robot.adjust_servo(-0.1)
                sleep(0.1)

            # this trains the AI
            if user_name == 'd':
                robot.adjust_servo(0.1)
                sleep(0.1)
                
            # kill the loop
            if user_name == 'q':
                break
