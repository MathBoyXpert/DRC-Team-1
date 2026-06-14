from HSVFilters.BlueTrackLinesHSVFilter import BlueTrackLinesHSVFilter
from HSVFilters.YellowTrackLinesHSVFilter import YellowTrackLinesHSVFilter

import numpy as np


class PathEstimation:
    CAR_CENTRE = 320 ## This is frame size (640) / 2 = 320

    ## Takes in the yellow and blue filters when initialising the class
    def __init__(self, yellow_filter: YellowTrackLinesHSVFilter, blue_filter: BlueTrackLinesHSVFilter):
        self.yellow_filter = yellow_filter
        self.blue_filter = blue_filter

    def calculate_curvature(self):
        y_eval = 480
        ## This grabs the polynomial coefficients that were obtained from the fit
        left_fit = self.yellow_filter.fit
        right_fit = self.blue_filter.fit
        if left_fit is None or right_fit is None:
            return None
        
        ## Calculates the theoretical curvature of the left and right curves
        left_curvature = ((1 + (2* left_fit[0]*y_eval+ left_fit[1])**2)**1.5) / np.abs(2*left_fit[0])
        right_curvature = ((1 + (2 *right_fit[0]*y_eval + right_fit[1])**2)**1.5) / np.abs(2*right_fit[0])

        ## Returns the curve
        return (left_curvature + right_curvature) / 2
    
    def calculate_centreline(self):
        left_base = self.yellow_filter.x_base
        right_base = self.blue_filter.x_base
        if left_base is None or right_base is None:
            return None
        
        return (left_base + right_base) / 2
        
    def calculate_steering_angle(self):
        ## Find the curvature of the track based on the left and right lines
        curvature = self.calculate_curvature()
        ## Find the offset from the centreline
        lane_offset = (self.CAR_CENTRE - self.calculate_centreline())
        return np.arctan(lane_offset / curvature) * 180/ np.pi