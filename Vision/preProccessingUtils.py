import numpy as np
import tensorflow as tf
import keras
import cv2
import config
import os

def morphologicalOperationsOnMask(hsvMask):
    # bigger kernels remove/fill larger artifacts but distort shapes more
    kernel = np.ones((5, 5), np.uint8)
    # OPENING to remove background noise (stray pixels that have been masked in)
    cleaned_open = cv2.morphologyEx(hsvMask, cv2.MORPH_OPEN, kernel)
    # CLOSING to fill internal holes (glare/shadow patches, that didn get masked in)
    return cv2.morphologyEx(cleaned_open, cv2.MORPH_CLOSE, kernel)

# this is globally accessible 
# Preproccessing the frame before it is sent to be filtered, this returns a HSV Frame
def preprocessing(frame):
    
    # resize the frame to whatever is in config for faster processing
    resized_frame = cv2.resize(frame, (config.WIDTH, config.HEIGHT), interpolation=cv2.INTER_AREA)
    
    # applys a gaussian blur to smooth out the frame 
    blurred_frame = cv2.GaussianBlur(resized_frame, (5, 5), 0)
    
    # # applying CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # # Convert to Lab color space to apply CLAHE on the Lightness channel
    # lab = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2Lab)
    # l, a, b = cv2.split(lab)
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # cl = clahe.apply(l)

    # # Merge back and convert to BGR
    # limg = cv2.merge((cl, a, b))
    # enhanced_frame = cv2.cvtColor(limg, cv2.COLOR_Lab2BGR)
    
    # finally convertign to HSV for filtering
    curr_hsv_frame = cv2.cvtColor(blurred_frame, config.HSV_SPACE)
    
    return curr_hsv_frame