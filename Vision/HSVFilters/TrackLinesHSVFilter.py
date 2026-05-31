import numpy as np
import cv2
import os

class TrackLinesHSVFilter:
    def find_lane_pixels(binary_warped):
	    # 1) Take a histogram of the bottom half of the image
        histogram = np.sum(binary_warped[binary_warped.shape[0]//2:,:], axis=0)

	    # 2) Find the peak of the left and right halves of the histogram
        midpoint = int(histogram.shape[0] // 2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint

	    # 3) Step through windows to track the line upward
        new_leftx_base = TrackLinesHSVFilter.window_shift(histogram, leftx_base)
        new_rightx_base = TrackLinesHSVFilter.window_shift(histogram, rightx_base)

        return new_leftx_base, new_rightx_base

    def window_shift(histogram, x_base):
        """
        This function aims to determine if the windows can follow the line provided.
        """
        # Divide the image up into 9 "windows". We can change this if necessary. 
        N = 9

        min_pixels = 0

        window_size = histogram.shape[0] // N

        for i in range(N):
            # Setting up the rectangle
            y_hi = histogram.shape[0] - (i * window_size)
            y_lo = histogram.shape[0] - ((i+1) * window_size)

            x_left = x_base - window_size
            x_right = x_base + window_size

            non_zero_x, non_zero_y = np.nonzero(histogram)

            good_indices = ((non_zero_y >= y_lo) & (non_zero_y < y_hi) &
                            (non_zero_x >= x_left) & (non_zero_x < x_right))
            
            lane_pixels_x = non_zero_x[good_indices]
            lane_pixels_y = non_zero_y[good_indices]

            ## If there are enough lane pixels detected, change the base
            if len(lane_pixels_x) > min_pixels and len(lane_pixels_y) > min_pixels:
                x_base = np.mean(lane_pixels_x)

        return x_base
    
    
    
            

            





  