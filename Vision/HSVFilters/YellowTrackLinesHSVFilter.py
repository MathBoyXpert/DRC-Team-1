import numpy as np
import Utils.config as config
import cv2
from .HSVFilterInterface import HSVFilterInterface
from .TrackLinesFilter import TrackLinesFilter
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
        self.trackline = TrackLinesFilter()
        self.fit = None
        self.x_base = None

    # This creates an array of the minimum HSV values for the yellow mask
    def Get_Min_Vals_Arr(self):
        return np.array([self.hsvValueMap["yellow_hMin"], self.hsvValueMap["yellow_sMin"], self.hsvValueMap["yellow_vMin"]])

    # This creates an array of the maximum HSV values for the yellow mask
    def Get_Max_Vals_Arr(self):
        return np.array([self.hsvValueMap["yellow_hMax"], self.hsvValueMap["yellow_sMax"], self.hsvValueMap["yellow_vMax"]])

    def Filter_Main_Process(self, frame, hsvFrame):
        result, contour_status = super().Filter_Main_Process(frame, hsvFrame)
        bounded_mask_y = np.zeros_like(self.hsvMask)

        if contour_status:
            bounded_mask_y[self.y:self.y+self.h, self.x:self.x+self.w] = self.hsvMask[self.y:self.y+self.h, self.x:self.x+self.w]
    
        msk, fit, x_base = self.trackline.find_lane_pixels(bounded_mask_y, "Left Sliding window (yellow)")
        if msk is not None and fit is not None:
            self.fit = fit
            self.x_base = x_base
        return result, contour_status
    
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