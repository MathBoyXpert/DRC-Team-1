import numpy as np
import Utils.config as config
import cv2
from .HSVFilterInterface import HSVFilterInterface
from VisionInput import VisionInput

class ObstacleHSVFilter(HSVFilterInterface):
    # HSV filter constructor
    def __init__(self):
        # stores purple hsv values
        self.hsvValueMap = {}

        self.hsvList = ["purple_hMin", "purple_sMin", "purple_vMin", 
                        "purple_hMax", "purple_sMax", "purple_vMax"]

        # populating the HSV values
        for hsvAttribute in self.hsvList:
            self.hsvValueMap[hsvAttribute] = 0;

        super().__init__()

    # This creates an array of the minimum HSV values for the purple mask
    def Get_Min_Vals_Arr(self):
        return np.array([self.hsvValueMap["purple_hMin"], self.hsvValueMap["purple_sMin"], self.hsvValueMap["purple_vMin"]])

    # This creates an array of the maximum HSV values for the purple mask
    def Get_Max_Vals_Arr(self):
        return np.array([self.hsvValueMap["purple_hMax"], self.hsvValueMap["purple_sMax"], self.hsvValueMap["purple_vMax"]])

    # prints all current HSV values for debugging and displaying
    def debug_print_filters(self):
        """Prints all current HSV filter values in a readable format."""
        print("-" * 30)
        print("DEBUG: Current Obstacle (Purple) HSV Filters")
        print("-" * 30)

        # purple Bot Filter
        print(f"[Purple FILTER]")
        print(f"  Min: H={self.purple_hMin}, S={self.purple_sMin}, V={self.purple_vMin}")
        print(f"  Max: H={self.purple_hMax}, S={self.purple_sMax}, V={self.purple_vMax}")

    def Get_Filter_Name(self):
        return config.OBSTACLE_HSV