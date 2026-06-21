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
sudo make install

# 5. Reload system configs and enable the daemon globally
sudo ldconfig
sudo systemctl daemon-reload
sudo systemctl enable --now pigpiod

fastandcurious@drc-pi:~ $ tar zxf v79.tar.gz
fastandcurious@drc-pi:~ $ cd pigpio-79
fastandcurious@drc-pi:~/pigpio-79 $ make
gcc -O3 -Wall -pthread -fpic -c -o pigpio.o pigpio.c
gcc -O3 -Wall -pthread -fpic -c -o command.o command.c
gcc -shared -pthread -Wl,-soname,libpigpio.so.1 -o libpigpio.so.1 pigpio.o command.o
ln -fs libpigpio.so.1 libpigpio.so
strip --strip-unneeded libpigpio.so
size     libpigpio.so
   text	   data	    bss	    dec	    hex	filename
 303208	  10656	 611656	 925520	  e1f50	libpigpio.so
gcc -O3 -Wall -pthread -fpic -c -o pigpiod_if.o pigpiod_if.c
gcc -shared -pthread -Wl,-soname,libpigpiod_if.so.1 -o libpigpiod_if.so.1 pigpiod_if.o command.o
ln -fs libpigpiod_if.so.1 libpigpiod_if.so
strip --strip-unneeded libpigpiod_if.so
size     libpigpiod_if.so
   text	   data	    bss	    dec	    hex	filename
  63287	   8696	  49304	 121287	  1d9c7	libpigpiod_if.so
gcc -O3 -Wall -pthread -fpic -c -o pigpiod_if2.o pigpiod_if2.c
gcc -shared -pthread -Wl,-soname,libpigpiod_if2.so.1 -o libpigpiod_if2.so.1 pigpiod_if2.o command.o
ln -fs libpigpiod_if2.so.1 libpigpiod_if2.so
strip --strip-unneeded libpigpiod_if2.so
size     libpigpiod_if2.so
   text	   data	    bss	    dec	    hex	filename
  87677	   8704	   2936	  99317	  183f5	libpigpiod_if2.so
gcc -O3 -Wall -pthread   -c -o x_pigpio.o x_pigpio.c
gcc -o x_pigpio x_pigpio.o -L. -lpigpio -pthread -lrt
gcc -O3 -Wall -pthread   -c -o x_pigpiod_if.o x_pigpiod_if.c
gcc -o x_pigpiod_if x_pigpiod_if.o -L. -lpigpiod_if -pthread -lrt
gcc -O3 -Wall -pthread   -c -o x_pigpiod_if2.o x_pigpiod_if2.c
gcc -o x_pigpiod_if2 x_pigpiod_if2.o -L. -lpigpiod_if2 -pthread -lrt
gcc -O3 -Wall -pthread   -c -o pig2vcd.o pig2vcd.c
gcc -o pig2vcd pig2vcd.o
strip pig2vcd
gcc -O3 -Wall -pthread   -c -o pigpiod.o pigpiod.c
gcc -o pigpiod pigpiod.o -L. -lpigpio -pthread -lrt
strip pigpiod
gcc -O3 -Wall -pthread   -c -o pigs.o pigs.c
gcc -o pigs pigs.o command.o
strip pigs
fastandcurious@drc-pi:~/pigpio-79 $ sudo make install
install -m 0755 -d                             /opt/pigpio/cgi
install -m 0755 -d                             /usr/local/include
install -m 0644 pigpio.h                       /usr/local/include
install -m 0644 pigpiod_if.h                   /usr/local/include
install -m 0644 pigpiod_if2.h                  /usr/local/include
install -m 0755 -d                             /usr/local/lib
install -m 0755 libpigpio.so.1      /usr/local/lib
install -m 0755 libpigpiod_if.so.1  /usr/local/lib
install -m 0755 libpigpiod_if2.so.1 /usr/local/lib
cd /usr/local/lib && ln -fs libpigpio.so.1      libpigpio.so
cd /usr/local/lib && ln -fs libpigpiod_if.so.1  libpigpiod_if.so
cd /usr/local/lib && ln -fs libpigpiod_if2.so.1 libpigpiod_if2.so
install -m 0755 -d                             /usr/local/bin
install -m 0755 pig2vcd                        /usr/local/bin
install -m 0755 pigpiod                        /usr/local/bin
install -m 0755 pigs                           /usr/local/bin
if which python2; then python2 setup.py install ; fi
if which python3; then python3 setup.py install ; fi
/usr/local/bin/python3
Traceback (most recent call last):
  File "/home/fastandcurious/pigpio-79/setup.py", line 3, in <module>
    from distutils.core import setup
ModuleNotFoundError: No module named 'distutils'
make: *** [Makefile:107: install] Error 1
