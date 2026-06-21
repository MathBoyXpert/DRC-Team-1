import sys
from gpiozero import Servo, PhaseEnableMotor, AngularServo
from time import time, sleep
from sshkeyboard import listen_keyboard, stop_listening

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
        # set the hardware by linking them with the pins
        self.drive_motor1 = PhaseEnableMotor(config.DRIVE_MOTOR_DIR1, config.DRIVE_MOTOR_PWM1)
        self.drive_motor2 = PhaseEnableMotor(config.DRIVE_MOTOR_DIR2, config.DRIVE_MOTOR_PWM2)
        self.steering_servo = AngularServo(config.STEERING_SERVO_PIN, min_angle=0, max_angle=270, min_pulse_width=0.0004, max_pulse_width=0.0028)
        
        # initialise PID for steering
        self.pid = PID()

    def set_steering(self, cx):
        """
        Adjust steering angle based on the centroid x-coordinate from vision.
        cx: Centroid X from track line filter.
        """
        if cx is None:
            # if no line is detected keep steering at the center (aka straight)
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

    def adjust_servo(self, angle):
        """
        adjust the servo from the current position to a new position
        value: value between 0 and 270
        """
        self.steering_servo.angle = angle

    def drive(self, speed):
        """
        drive forward or backward.
        speed: value between -1 and 1
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
        print("Use W/S to drive, A/D to steer, press Q to quit")
        
        def press(key):
            if key == 'w':
                self.drive(0.3)
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
    # robot.manual_drive_mode()
    for i in range(65, 157):
        robot.adjust_servo(i)
        sleep(1)
    sleep(1)
    robot.adjust_servo(135)
    sleep(1)
    sleep(1)



    # robot.drive(0)
    # robot.drive_motor1.forward(0.2)
    # sleep(1)
    # robot.drive(0)
    # robot.drive_motor2.forward(0.2)
    # sleep(1)
    # robot.drive(0)


