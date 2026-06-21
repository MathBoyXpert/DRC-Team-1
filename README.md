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

fastandcurious@drc-pi:~/drcTest/DRC-Team-1 $ openssl version
OpenSSL 3.5.6 7 Apr 2026 (Library: OpenSSL 3.5.6 7 Apr 2026)
fastandcurious@drc-pi:~/drcTest/DRC-Team-1 $ python3 -c "import ssl; print(ssl.OPENSSL_VERSION)"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import ssl; print(ssl.OPENSSL_VERSION)
    ^^^^^^^^^^
  File "/usr/local/lib/python3.13/ssl.py", line 100, in <module>
    import _ssl             # if we can't import it, let the error propagate
    ^^^^^^^^^^^
ModuleNotFoundError: No module named '_ssl'

Option 2: Recompile Python 3.13 from source (If you absolutely need 3.13)
If you compiled Python 3.13 yourself because your robotics project explicitly requires features unique to 3.13, you need to fix the dependency chain and re-run the compilation:

Install the missing development headers:

Bash
sudo apt update
sudo apt install libssl-dev build-essential zlib1g-dev libffi-dev -y
Head back to your original Python source code folder (where you downloaded and extracted Python 3.13, usually something like ~/Python-3.13.x/):

Bash
cd ~/Python-3.13.x  # Adjust this to your actual source path
Reconfigure and recompile:
Running ./configure now will successfully detect the libssl-dev headers you just installed and configure the SSL module automatically.

Bash
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
Once completed, your custom Python 3.13 will possess full cryptographic capabilities, allowing you to create your virtual environment normally.