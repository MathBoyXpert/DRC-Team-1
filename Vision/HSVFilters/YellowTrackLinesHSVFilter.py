import numpy as np
import config
import cv2
from .HSVFilterInterface import HSVFilterInterface
from VisionInput import VisionInput

class YellowTrackLinesHSVFilter(HSVFilterInterface):
    # HSV filter constructor
    def __init__(self):
        # stores yellow hsv values
        self.hsvValueMap = {}

        self.hsvList = ["yellow_hMin", "yellow_sMin", "yellow_vMin", 
                        "yellow_hMax", "yellow_sMax", "yellow_vMax"]
        
        # populating the HSV values
        for hsvAttribute in self.hsvList:
            self.hsvValueMap[hsvAttribute] = 0;

        super().__init__()

    # This creates an array of the minimum HSV values for the yellow mask
    def Get_Min_Vals_Arr(self):
        return np.array([self.hsvValueMap["yellow_hMin"], self.hsvValueMap["yellow_sMin"], self.hsvValueMap["yellow_vMin"]])
    
    # This creates an array of the maximum HSV values for the yellow mask
    def Get_Max_Vals_Arr(self):
        return np.array([self.hsvValueMap["yellow_hMax"], self.hsvValueMap["yellow_sMax"], self.hsvValueMap["yellow_vMax"]])

    # prints all current HSV values for debugging and displaying
    def debug_print_filters(self):
        """Prints all current HSV filter values in a readable format."""
        print("-" * 30)
        print("DEBUG: Current HSV Filters")
        print("-" * 30)

        # Yellow Tape Filter (Left Boundary)
        print(f"[YELLOW FILTER (Left Boundary)]")
        print(f"  Min: H={self.yellow_hMin}, S={self.yellow_sMin}, V={self.yellow_vMin}")
        print(f"  Max: H={self.yellow_hMax}, S={self.yellow_sMax}, V={self.yellow_vMax}")
        print("-" * 30)

    def Get_Filter_Name(self):
        return config.YELLOW_TRACK_LINES_HSV