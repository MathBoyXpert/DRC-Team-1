import numpy as np

class HSVFilter:
    # HSV filter constructor
    def __init__(
            self,
            blue_hMin, blue_sMin, blue_vMin,
            blue_hMax, blue_sMax, blue_vMax,
            yellow_hMin, yellow_sMin, yellow_vMin,
            yellow_hMax, yellow_sMax, yellow_vMax
    ):
        # setting blue hsv values
        self.blue_hMin = blue_hMin
        self.blue_sMin = blue_sMin
        self.blue_vMin = blue_vMin
        self.blue_hMax = blue_hMax
        self.blue_sMax = blue_sMax
        self.blue_vMax = blue_vMax

        # setting yellow hsv values
        self.yellow_hMin = yellow_hMin
        self.yellow_sMin = yellow_sMin
        self.yellow_vMin = yellow_vMin
        self.yellow_hMax = yellow_hMax
        self.yellow_sMax = yellow_sMax
        self.yellow_vMax = yellow_vMax

    # This creates an array of the minimum HSV values for the blue mask
    def Get_Blue_Min_Vals_Arr(self):
        return np.array([self.blue_hMin, self.blue_sMin, self.blue_vMin])
    
    # This creates an array of the maximum HSV values for the blue mask
    def Get_Blue_Max_Vals_Arr(self):
        return np.array([self.blue_hMax, self.blue_sMax, self.blue_vMax])
    
    # This creates an array of the minimum HSV values for the yellow mask
    def Get_Yellow_Min_Vals_Arr(self):
        return np.array([self.yellow_hMin, self.yellow_sMin, self.yellow_vMin])

    # This creates an array of the maximum HSV values for the yellow mask
    def Get_Yellow_Max_Vals_Arr(self):
        return np.array([self.yellow_hMax, self.yellow_sMax, self.yellow_vMax])
    