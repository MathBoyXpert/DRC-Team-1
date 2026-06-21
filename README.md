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
(ml_space) fast@raspberrypi:~/DRC-Team-1 $ pip install rpi-lgpio
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting rpi-lgpio
  Using cached https://www.piwheels.org/simple/rpi-lgpio/rpi_lgpio-0.6-py3-none-any.whl.metadata (2.5 kB)
Collecting lgpio>=0.1.0.1 (from rpi-lgpio)
  Using cached lgpio-0.2.2.0.tar.gz (90 kB)
  Preparing metadata (setup.py) ... done
Using cached https://www.piwheels.org/simple/rpi-lgpio/rpi_lgpio-0.6-py3-none-any.whl (11 kB)
Building wheels for collected packages: lgpio
  DEPRECATION: Building 'lgpio' using the legacy setup.py bdist_wheel mechanism, which will be removed in a future version. pip 25.3 will enforce this behaviour change. A possible replacement is to use the standardized build interface by setting the `--use-pep517` option, (possibly combined with `--no-build-isolation`), or adding a `pyproject.toml` file to the source tree of 'lgpio'. Discussion can be found at https://github.com/pypa/pip/issues/6334
  Building wheel for lgpio (setup.py) ... error
  error: subprocess-exited-with-error
  
  × python setup.py bdist_wheel did not run successfully.
  │ exit code: 1
  ╰─> [8 lines of output]
      running bdist_wheel
      running build
      running build_py
      running build_ext
      building '_lgpio' extension
      swigging lgpio.i to lgpio_wrap.c
      swig -python -o lgpio_wrap.c lgpio.i
      error: command 'swig' failed: No such file or directory
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for lgpio
  Running setup.py clean for lgpio
Failed to build lgpio
ERROR: Failed to build installable wheels for some pyproject.toml based projects (lgpio)
