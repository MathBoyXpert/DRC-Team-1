from HSVFilters.BlueTrackLinesHSVFilter import BlueTrackLinesHSVFilter
from HSVFilters.YellowTrackLinesHSVFilter import YellowTrackLinesHSVFilter

import numpy as np
import Utils.config as config

class PathEstimation:
    CAR_CENTRE = config.WIDTH ## This is frame size (640) / 2 = 320

    ## Takes in the yellow and blue filters when initialising the class
    def __init__(self, yellow_filter: YellowTrackLinesHSVFilter, blue_filter: BlueTrackLinesHSVFilter):
        self.yellow_filter = yellow_filter
        self.blue_filter = blue_filter

    def calculate_curvature(self):
        y_eval = 480
        ## This grabs the polynomial coefficients that were obtained from the fit
        left_fit = self.yellow_filter.fit
        right_fit = self.blue_filter.fit

        left_curvature = None
        right_curvature = None

        ## Calculates the theoretical curvature of the left and right curves
        if left_fit is not None:
            left_curvature = ((1 + (2* left_fit[0]*y_eval+ left_fit[1])**2)**1.5) / np.abs(2*left_fit[0])

        if right_fit is not None:
            right_curvature = ((1 + (2 *right_fit[0]*y_eval + right_fit[1])**2)**1.5) / np.abs(2*right_fit[0])

        ## Edge cases: When either onr of the lanes are not in view, return the other lane.
        if left_curvature is not None and right_curvature is not None:
            return (left_curvature + right_curvature) / 2
        elif left_curvature is not None:
            return left_curvature
        elif right_curvature is not None:
            return right_curvature
        else:
            return None
        
        ## Calculates the theoretical curvature of the left and right curves
        # left_curvature = ((1 + (2* left_fit[0]*y_eval+ left_fit[1])**2)**1.5) / np.abs(2*left_fit[0])
        # right_curvature = ((1 + (2 *right_fit[0]*y_eval + right_fit[1])**2)**1.5) / np.abs(2*right_fit[0])

        ## Edge Case: U-turn lane. You cannot see one of the lanes
    
        ## Returns the curve this ill give you the coefficients of the poolynomail which then can be accessed by using polyfit.
    
    def calculate_centreline(self):

        ### This gets the x_base that was from the histogram calculations
        left_base = self.yellow_filter.x_base
        right_base = self.blue_filter.x_base
        if left_base is None and right_base is None:
            return None
        
        ## Edge case: U-turn
       
        ## This retuns the centreline. 
        return (left_base + right_base) / 2
        
    def calculate_steering_angle(self):
        ## Find the curvature of the track based on the left and right lines
        curvature = self.calculate_curvature()
        ## Find the offset from the centreline
        lane_offset = (self.CAR_CENTRE - self.calculate_centreline())
        return np.arctan(lane_offset / curvature) * 180/ np.pi
    
    ## Note: Refer to this Youtube Video to see where I got the implementations fopr all of these from.
    ## https://www.youtube.com/watch?v=Birvs5MYOLY&list=PLCiTDJays9rWQkp_IuHOd15JXHyVaYQKE&index=5