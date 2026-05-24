import numpy as np
import config
import cv2
from .HSVFilterInterface import HSVFilterInterface
from VisionInput import VisionInput

class TrackLinesHSVFilter(HSVFilterInterface):
    # HSV filter constructor
    def __init__(self):
        # stores yellow hsv values
        self.hsvValueMap = {}

        self.hsvList = ["yellow_hMin", "yellow_sMin", "yellow_vMin", 
                        "yellow_hMax", "yellow_sMax", "yellow_vMax",
                        "blue_hMin", "blue_sMin", "blue_vMin",
                        "blue_hMax", "blue_sMax", "blue_vMax"]
        
        # populating the HSV values
        for hsvAttribute in self.hsvList:
            self.hsvValueMap[hsvAttribute] = 0;

        super().__init__()
    
    # the track lines HSV should display its own frame
    def Get_Min_Vals_Arr(self):
        return super().Get_Min_Vals_Arr()
    
    # the track lines HSV should display its own frame
    def Get_Max_Vals_Arr(self):
        return super().Get_Max_Vals_Arr()

    # This creates an array of the minimum HSV values for the yellow mask
    def Get_Yellow_Min_Vals_Arr(self):
        return np.array([self.hsvValueMap["yellow_hMin"], self.hsvValueMap["yellow_sMin"], self.hsvValueMap["yellow_vMin"]])
    
    # This creates an array of the maximum HSV values for the yellow mask
    def Get_Yellow_Max_Vals_Arr(self):
        return np.array([self.hsvValueMap["yellow_hMax"], self.hsvValueMap["yellow_sMax"], self.hsvValueMap["yellow_vMax"]])

    # This creates an array of the minimum HSV values for the blue mask
    def Get_Blue_Min_Vals_Arr(self):
        return np.array([self.hsvValueMap["blue_hMin"], self.hsvValueMap["blue_sMin"], self.hsvValueMap["blue_vMin"]])
    
    # This creates an array of the maximum HSV values for the blue mask
    def Get_Blue_Max_Vals_Arr(self):
        return np.array([self.hsvValueMap["blue_hMax"], self.hsvValueMap["blue_sMax"], self.hsvValueMap["blue_vMax"]])
    
    # displays the current masked frame
    def Display_Masked_Frame(self, frame, hsv_frame):        
        # mask for Blue and Yellow values
        blueHsvMask = cv2.inRange(hsv_frame, self.Get_Blue_Min_Vals_Arr(), self.Get_Blue_Max_Vals_Arr())
        yellowHsvMask = cv2.inRange(hsv_frame, self.Get_Yellow_Min_Vals_Arr(), self.Get_Yellow_Max_Vals_Arr())

        # this combines the yellow and blue masks
        linesHsvMask = cv2.bitwise_or(blueHsvMask, yellowHsvMask)

        # this applys the mask on the current frame and saves the masked frame
        maskedframe = cv2.bitwise_and(frame, frame, mask=linesHsvMask)

        # display the HSV masked frame
        # display the HSV masked frame if the current config allows
        if self.Should_Filtered_Frame_Be_Displayed() or self.isFilterBeingEdited:
            cv2.imshow(self.Get_Filter_Frame_Name(), maskedframe)

    # prints all current HSV values for debugging and displaying
    def debug_print_filters(self):
        """Prints all current HSV filter values in a readable format."""
        print("-" * 30)
        print("DEBUG: Current HSV Filters")
        print("-" * 30)
        
        # Blue Tape Filter (Right Boundary)
        print(f"[BLUE FILTER (Right Boundary)]")
        print(f"  Min: H={self.blue_hMin}, S={self.blue_sMin}, V={self.blue_vMin}")
        print(f"  Max: H={self.blue_hMax}, S={self.blue_sMax}, V={self.blue_vMax}")
        
        print("") # Spacer

        # Yellow Tape Filter (Left Boundary)
        print(f"[YELLOW FILTER (Left Boundary)]")
        print(f"  Min: H={self.yellow_hMin}, S={self.yellow_sMin}, V={self.yellow_vMin}")
        print(f"  Max: H={self.yellow_hMax}, S={self.yellow_sMax}, V={self.yellow_vMax}")
        print("-" * 30)

    def Get_Filter_Name(self):
        return config.TRACK_LINES_HSV