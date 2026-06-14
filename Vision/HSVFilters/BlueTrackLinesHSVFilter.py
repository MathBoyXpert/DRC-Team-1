import numpy as np
import Utils.config as config
import cv2
from .HSVFilterInterface import HSVFilterInterface
from .TrackLinesFilter import TrackLinesFilter
from VisionInput import VisionInput

class BlueTrackLinesHSVFilter(HSVFilterInterface):
    # HSV filter constructor
    def __init__(self):
        # stores blue hsv values
        self.hsvValueMap = {}

        self.hsvList = ["blue_hMin", "blue_sMin", "blue_vMin", 
                        "blue_hMax", "blue_sMax", "blue_vMax"]

        # populating the HSV values
        for hsvAttribute in self.hsvList:
            self.hsvValueMap[hsvAttribute] = 0;

        super().__init__()
        self.trackline = TrackLinesFilter()

    # This creates an array of the minimum HSV values for the blue mask
    def Get_Min_Vals_Arr(self):
        return np.array([self.hsvValueMap["blue_hMin"], self.hsvValueMap["blue_sMin"], self.hsvValueMap["blue_vMin"]])

    # This creates an array of the maximum HSV values for the blue mask
    def Get_Max_Vals_Arr(self):
        return np.array([self.hsvValueMap["blue_hMax"], self.hsvValueMap["blue_sMax"], self.hsvValueMap["blue_vMax"]])

    def Filter_Main_Process(self, frame, hsvFrame):
        result, contour_status = super().Filter_Main_Process(frame, hsvFrame)
        bounded_mask_b = np.zeros_like(self.hsvMask)
        if contour_status:
            bounded_mask_b[self.y:self.y+self.h, self.x:self.x+self.w] = self.hsvMask[self.y:self.y+self.h, self.x:self.x + self.w]
        
        msk = self.trackline.find_lane_pixels(bounded_mask_b, "Right Sliding window (blue)")
        return result, contour_status

    # prints all current HSV values for debugging and displaying
    def debug_print_filters(self):
        """Prints all current HSV filter values in a readable format."""
        print("-" * 30)
        print("DEBUG: Current HSV Filters")
        print("-" * 30)

        # Blue Tape Filter (Right Boundary)
        print(f"[Blue FILTER (Right Boundary)]")
        print(f"  Min: H={self.blue_hMin}, S={self.blue_sMin}, V={self.blue_vMin}")
        print(f"  Max: H={self.blue_hMax}, S={self.blue_sMax}, V={self.blue_vMax}")
        print("-" * 30)

        self.trackLines.find_lane_pixels(self.hsvMask)

    def Get_Filter_Name(self):
        return config.BLUE_TRACK_LINES_HSV