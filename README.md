# DRC Team 1
This will be our github repo for our team DRC Team 1
t0ky0drIft2718
CREATEf4stAndcurI0us

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

fastandcurious@drc-pi:~/drcTest/DRC-Team-1 $ python3 -m venv ml_env
fastandcurious@drc-pi:~/drcTest/DRC-Team-1 $ ^[[200~pip install --upgrade pip
bash: $'\E[200~pip': command not found
fastandcurious@drc-pi:~/drcTest/DRC-Team-1 $ pip install --upgrade pip
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    For more information visit http://rptl.io/venv

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
