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

# 3. Activate the environment
source ml_env/bin/activate

# 4. Upgrade pip and install your packages cleanly inside the environment
pip install --upgrade pip
pip install h5py tensorflowpython3 -m venv ml_env

astandcurious@drc-pi:~/drcTest/DRC-Team-1 $ /home/fastandcurious/drcTest/DRC-Team-1/ml_env/bin/python /home/fastandcurious/drcTest/DRC-Team-1/Control/ControlThread.py
/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/devices.py:300: PinFactoryFallback: Falling back from lgpio: No module named 'lgpio'
  warnings.warn(
/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/devices.py:300: PinFactoryFallback: Falling back from rpigpio: No module named 'RPi'
  warnings.warn(
/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/devices.py:300: PinFactoryFallback: Falling back from pigpio: No module named 'pigpio'
  warnings.warn(
/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/devices.py:300: PinFactoryFallback: Falling back from native: unable to open /dev/gpiomem or /dev/mem; upgrade your kernel or run as root
  warnings.warn(
Traceback (most recent call last):
  File "/home/fastandcurious/drcTest/DRC-Team-1/Control/ControlThread.py", line 135, in <module>
    robot = AckermannRobot()
  File "/home/fastandcurious/drcTest/DRC-Team-1/Control/ControlThread.py", line 39, in __init__
    self.drive_motor1 = PhaseEnableMotor(config.DRIVE_MOTOR_DIR1, config.DRIVE_MOTOR_PWM1)
                        ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/devices.py", line 108, in __call__
    self = super().__call__(*args, **kwargs)
  File "/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/output_devices.py", line 1336, in __init__
    phase_device=DigitalOutputDevice(phase, pin_factory=pin_factory),
                 ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/devices.py", line 108, in __call__
    self = super().__call__(*args, **kwargs)
  File "/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/output_devices.py", line 192, in __init__
    super().__init__(pin, active_high=active_high,
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     initial_value=initial_value, pin_factory=pin_factory)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/output_devices.py", line 74, in __init__
    super().__init__(pin, pin_factory=pin_factory)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/mixins.py", line 75, in __init__
    super().__init__(*args, **kwargs)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/devices.py", line 544, in __init__
    super().__init__(pin_factory=pin_factory)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/devices.py", line 245, in __init__
    Device.ensure_pin_factory()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/devices.py", line 270, in ensure_pin_factory
    Device.pin_factory = Device._default_pin_factory()
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/fastandcurious/drcTest/DRC-Team-1/ml_env/lib/python3.13/site-packages/gpiozero/devices.py", line 302, in _default_pin_factory
    raise BadPinFactory('Unable to load any default pin factory!')
gpiozero.exc.BadPinFactory: Unable to load any default pin factory!

# 1. Install the required build tools
sudo apt update
sudo apt install --no-install-recommends -y python3-setuptools python3-full wget make gcc

# 2. Download the latest source package from the official repository
wget https://github.com/joan2937/pigpio/archive/refs/tags/v79.tar.gz

# 3. Extract the downloaded file
tar zxf v79.tar.gz

# 4. Move into the extracted directory and build it
cd pigpio-79
make

# Register the newly compiled libraries with the system
sudo ldconfig

# Set up the systemd service files so it runs in the background
sudo cp util/pigpiod.service /lib/systemd/system/
sudo systemctl daemon-reload

# Start the service right now and enable it to run on boot
sudo systemctl enable --now pigpiod

sudo systemctl status pigpiod



Step 1: Create a Symlink
Tell the system to map the actual installation location to the path systemd is searching for:

Bash
sudo ln -s /usr/local/bin/pigpiod /usr/bin/pigpiod
Step 2: Restart the Service
Clear the failed state, reload the systemd manager configuration, and kickstart the daemon:

Bash
sudo systemctl daemon-reload
sudo systemctl restart pigpiod
Step 3: Verify the Status
Bash
sudo systemctl status pigpiod


fastandcurious@drc-pi:~/pigpio-79 $ sudo ln -s /usr/local/bin/pigpiod /usr/bin/pigpiod
fastandcurious@drc-pi:~/pigpio-79 $ sudo systemctl daemon-reload
fastandcurious@drc-pi:~/pigpio-79 $ sudo systemctl restart pigpiod


Job for pigpiod.service failed because a timeout was exceeded.
See "systemctl status pigpiod.service" and "journalctl -xeu pigpiod.service" for details.
