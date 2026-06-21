import pickle
import os
import glob
import numpy as np
import sys

# Add Vision to path so pickle can find the classes
sys.path.append(os.path.join(os.getcwd(), "Vision"))

pkl_files = glob.glob("*.pkl")

for pkl_file in pkl_files:
    print(f"--- {pkl_file} ---")
    try:
        with open(pkl_file, 'rb') as f:
            data = pickle.load(f)
            if hasattr(data, 'hsvValueMap'):
                print(f"hsvValueMap: {data.hsvValueMap}")
            else:
                # Some objects might not have hsvValueMap but have the attributes directly
                print(f"Attributes: { {k: v for k, v in data.__dict__.items() if not k.startswith('_')} }")
    except Exception as e:
        print(f"Error loading {pkl_file}: {e}")
