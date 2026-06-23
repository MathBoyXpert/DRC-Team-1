from gpiozero import OutputDevice
import time

# left motor
DRIVE_MOTOR_PWM1 = 13
DRIVE_MOTOR_DIR1 = 5

# right motor
DRIVE_MOTOR_PWM2 = 16
DRIVE_MOTOR_DIR2 = 6

motor1PWM = OutputDevice(DRIVE_MOTOR_PWM1, active_high=True, initial_value=False)
motor2PWM = OutputDevice(DRIVE_MOTOR_PWM2, active_high=True, initial_value=False)
motor1DIR = OutputDevice(DRIVE_MOTOR_DIR1, active_high=True, initial_value=False)
motor2DIR = OutputDevice(DRIVE_MOTOR_DIR2, active_high=True, initial_value=False)

motor2PWM.on()
motor2DIR.off()

time.sleep(5)

motor1PWM.close()
motor2PWM.close()
motor1DIR.close()
motor2DIR.close()