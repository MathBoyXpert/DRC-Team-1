
class HSVFilter:
    def __init__(
            self,
            blue_hMin=None, blue_sMin=None, blue_vMin=None,
            blue_hMax=None, blue_sMax=None, blue_vMax=None,
            yellow_hMin=None, yellow_sMin=None, yellow_vMin=None,
            yellow_hMax=None, yellow_sMax=None, yellow_vMax=None
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