import numpy as np
import Utils.config as config
import cv2
from .HSVFilterInterface import HSVFilterInterface
from VisionInput import VisionInput

class TrackCompletionHSVFilter(HSVFilterInterface):
    # HSV filter constructor
    def __init__(self):
        # stores green hsv values
        self.hsvValueMap = {}

        self.hsvList = ["green_hMin", "green_sMin", "green_vMin", 
                        "green_hMax", "green_sMax", "green_vMax"]

        # populating the HSV values
        for hsvAttribute in self.hsvList:
            self.hsvValueMap[hsvAttribute] = 0;

        super().__init__()

    # This creates an array of the minimum HSV values for the green mask
    def Get_Min_Vals_Arr(self):
        return np.array([self.hsvValueMap["green_hMin"], self.hsvValueMap["green_sMin"], self.hsvValueMap["green_vMin"]])

    # This creates an array of the maximum HSV values for the green mask
    def Get_Max_Vals_Arr(self):
        return np.array([self.hsvValueMap["green_hMax"], self.hsvValueMap["green_sMax"], self.hsvValueMap["green_vMax"]])

    # prints all current HSV values for debugging and displaying
    def debug_print_filters(self):
        """Prints all current HSV filter values in a readable format."""
        print("-" * 30)
        print("DEBUG: Current Track Completion (Green) HSV Filters")
        print("-" * 30)

        # green Bot Filter
        print(f"[Green FILTER]")
        print(f"  Min: H={self.green_hMin}, S={self.green_sMin}, V={self.green_vMin}")
        print(f"  Max: H={self.green_hMax}, S={self.green_sMax}, V={self.green_vMax}")

    def Get_Filter_Name(self):
        return config.TRACK_COMPLETION_HSV