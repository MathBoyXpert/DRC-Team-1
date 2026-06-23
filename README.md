# DRC Team 1
This will be our github repo for our team DRC Team 1
t0ky0drIft2718
CREATEf4stAndcurI0us
source ml_env/bin/activate

sudo apt update && sudo apt install libatlas-base-dev libhdf5-dev python3-h5py -y && sudo pip3 install tensorflow --break
[sudo] password for fastandcurious: 
Hit:1 http://deb.debian.org/debian trixie InRelease
Hit:2 http://deb.debian.org/debian trixie-updates InRelease 
Hit:3 http://deb.debian.org/debian-security trixie-security InRelease             
Hit:4 http://archive.raspberrypi.com/debian trixie InRelease                      
250 packages can be upgraded. Run 'apt list --upgradable' to see them.
Package libatlas-base-dev is not available, but is referred to by another package.
This may mean that the package is missing, has been obsoleted, or
is only available from another source

# 1. Install the Python venv utility on your Pi
sudo apt install python3-venv -y

# 2. Create a virtual environment named 'ml_env' in your current directory
python3 -m venv ml_env

source ml_env/bin/activate

Traceback (most recent call last):
  File "/home/fast/DRC-Team-1/Control/ControlThread.py", line 144, in <module>
    robot.adjust_servo(135)
    ~~~~~~~~~~~~~~~~~~^^^^^
  File "/home/fast/DRC-Team-1/Control/ControlThread.py", line 83, in adjust_servo
    self.steering_servo.angle = angle
    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/fast/DRC-Team-1/ml_space/lib/python3.13/site-packages/adafruit_motor/servo.py", line 133, in angle
    self.fraction = new_angle / self.actuation_range
    ^^^^^^^^^^^^^
  File "/home/fast/DRC-Team-1/ml_space/lib/python3.13/site-packages/adafruit_motor/servo.py", line 69, in fraction
    self._pwm_out.duty_cycle = duty_cycle
    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/fast/DRC-Team-1/ml_space/lib/python3.13/site-packages/adafruit_pca9685.py", line 89, in duty_cycle
    raise ValueError(f"Out of range: value {value} not 0 <= value <= 65,535")
ValueError: Out of range: value 72129 not 0 <= value <= 65,535