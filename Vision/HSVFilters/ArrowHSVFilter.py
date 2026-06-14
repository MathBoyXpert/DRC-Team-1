import numpy as np
import Utils.config as config
from .HSVFilterInterface import HSVFilterInterface

class ArrowHSVFilter(HSVFilterInterface):
    def __init__(self):
        self.hsvValueMap = {}
        self.hsvList = ["arrow_hMin", "arrow_sMin", "arrow_vMin", 
                        "arrow_hMax", "arrow_sMax", "arrow_vMax"]

        # Initializing with default values (can be adjusted via GUI)
        for hsvAttribute in self.hsvList:
            self.hsvValueMap[hsvAttribute] = 0

        super().__init__()

    def Get_Min_Vals_Arr(self):
        return np.array([self.hsvValueMap["arrow_hMin"], 
                        self.hsvValueMap["arrow_sMin"], 
                        self.hsvValueMap["arrow_vMin"]])

    def Get_Max_Vals_Arr(self):
        return np.array([self.hsvValueMap["arrow_hMax"], 
                        self.hsvValueMap["arrow_sMax"], 
                        self.hsvValueMap["arrow_vMax"]])

    def debug_print_filters(self):
        print("-" * 30)
        print("DEBUG: Current Arrow HSV Filters")
        print("-" * 30)
        print(f"  Min: H={self.hsvValueMap['arrow_hMin']}, S={self.hsvValueMap['arrow_sMin']}, V={self.hsvValueMap['arrow_vMin']}")
        print(f"  Max: H={self.hsvValueMap['arrow_hMax']}, S={self.hsvValueMap['arrow_sMax']}, V={self.hsvValueMap['arrow_vMax']}")

    def Get_Filter_Name(self):
        return config.ARROW_HSV
