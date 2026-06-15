from gpiozero import Servo, PhaseEnableMotor
from time import time, sleep
from Vision.Utils import config

class PID:
    def __init__(self, kp, ki, kd, setpoint=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
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
        # The setpoint is the center of the image (WIDTH / 2)
        self.pid = PID(config.STEERING_KP, config.STEERING_KI, config.STEERING_KD, 
                       setpoint=config.WIDTH // 2)

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
        self.drive_motor.stop()
        self.steering_servo.value = config.STEERING_CENTER

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
