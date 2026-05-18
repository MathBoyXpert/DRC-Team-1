import numpy as np
import config
import cv2
from .HSVFilterInterface import HSVFilterInterface
from VisionInput import VisionInput

class RivalBotHSVFilter(HSVFilterInterface):
    # HSV filter constructor
    def __init__(self):
        # stores red hsv values
        self.hsvValueMap = {}

        self.hsvList = ["red_hMin", "red_sMin", "red_vMin", 
                        "red_hMax", "red_sMax", "red_vMax"]
        
        # populating the HSV values
        for hsvAttribute in self.hsvList:
            self.hsvValueMap[hsvAttribute] = 0;

        super().__init__()

    # This creates an array of the minimum HSV values for the red mask
    def Get_Min_Vals_Arr(self):
        return np.array([self.hsvValueMap["red_hMin"], self.hsvValueMap["red_sMin"], self.hsvValueMap["red_vMin"]])
    
    # This creates an array of the maximum HSV values for the red mask
    def Get_Max_Vals_Arr(self):
        return np.array([self.hsvValueMap["red_hMax"], self.hsvValueMap["red_sMax"], self.hsvValueMap["red_vMax"]])

    # prints all current HSV values for debugging and displaying
    def debug_print_filters(self):
        """Prints all current HSV filter values in a readable format."""
        print("-" * 30)
        print("DEBUG: Current Rival Bot (Red) HSV Filters")
        print("-" * 30)
        
        # Red Bot Filter
        print(f"[Red FILTER]")
        print(f"  Min: H={self.red_hMin}, S={self.red_sMin}, V={self.red_vMin}")
        print(f"  Max: H={self.red_hMax}, S={self.red_sMax}, V={self.red_vMax}")

    def Get_Filter_Name(self):
        return config.RIVAL_BOT_HSV