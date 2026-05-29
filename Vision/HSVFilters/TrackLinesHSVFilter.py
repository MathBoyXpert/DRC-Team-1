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
        # Let the window size by 9. We can change this if required.

    def window_shift(histogram, x_base):
        """
        This function aims to determine if the windows can follow the line provided.
        """
        N = 9

        window_size = histogram.shape[0] // N

        for i in range(N):
            # Setting up the rectangle
            y_hi = histogram.shape[0] - (i * window_size)
            y_lo = histogram.shape[0] - ((i+1) * window_size)

            x_left = x_base - window_size
            x_right = x_base + window_size

            





  