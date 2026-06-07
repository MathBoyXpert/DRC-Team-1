import numpy as np
import cv2
import os

class TrackLinesFilter:
    def find_lane_pixels(self, frame):
	    # 1) Take a histogram of the bottom half of the image
        histogram = np.sum(frame[frame.shape[0]//2:,:], axis=0)

	    # 2) Find the peak of the left and right halves of the histogram
        midpoint = int(histogram.shape[0] / 2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint

	    # 3) Step through windows to track the line upward
        # new_leftx_base = self.window_shift(histogram, leftx_base)
        # new_rightx_base = self.window_shift(histogram, rightx_base)
        y = 472
        lx = []
        ly = []
        rx = []
        ry = []

        msk = frame.copy()

        while y > 0:
            ## Left Threshold

            img = frame[y-40:y, leftx_base-50:leftx_base+50]
            contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                    lx.append(leftx_base - 50 + cx)
                    ly.append(y - 40 + cy)
                    leftx_base = leftx_base - 50 + cx
            
            # Right Threshold
            img = frame[y-40:y, rightx_base-50:rightx_base+50]
            contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                    rx.append(rightx_base - 50 + cx)
                    ry.append(y - 40 + cy)
                    rightx_base = rightx_base - 50 + cx

            cv2.rectangle(msk, (leftx_base-50, y), (leftx_base + 50, y-40), (255,255,255), 2)
            cv2.rectangle(msk, (rightx_base-50, y), (rightx_base + 50, y-40), (255,255,255), 2)
            y-=40
        
        left_fit = None
        right_fit = None

        if len(lx) >= 3:
            left_fit = np.polyfit(ly, lx, 2)
        
        if len(ry) >= 3:
            right_fit = np.polyfit(ry, rx, 2)
        
        self.detect_polynomial(msk, left_fit, right_fit, frame.shape[0])
        

        cv2.imshow("Sliding Windows", msk)

    def detect_polynomial(self, frame, left, right, height):
        plot_y = np.linspace(0, height - 1, height)

        if left is not None:
            left_x = np.polyval(left, plot_y)
            for i in range(len(plot_y) - 1):
                pt1 = (int(left_x[i]), int(plot_y[i]))
                pt2 = (int(left_x[i+1]), int(plot_y[i+1]))
                if 0 <= pt1[0] < frame.shape[1] and 0 <= pt2[0] < frame.shape[1]:
                    cv2.line(frame, pt1, pt2, (255, 255, 0), 2)

        if right is not None:
            right_x = np.polyval(right, plot_y)
            for i in range(len(plot_y) - 1):
                pt1 = (int(right_x[i]), int(plot_y[i]))
                pt2 = (int(right_x[i+1]), int(plot_y[i+1]))
                if 0 <= pt1[0] < frame.shape[1] and 0 <= pt2[0] < frame.shape[1]:
                    cv2.line(frame, pt1, pt2, (255, 255, 0), 2)
    ## Ignore this function
    # def window_shift(self, histogram, x_base):
    #     """
    #     This function aims to determine if the windows can follow the line provided. 
    #     It should be trending upwards. 
    #     """
    #     # Divide the image up into 9 "windows". We can change this if necessary. 
    #     N = 12

    #     min_pixels = 0

    #     window_size = histogram.shape[0] // N
    #     y = 472

    #     for i in range(N):
    #         # Setting up the rectangle
    #         y_hi = histogram.shape[0] - (i * window_size)
    #         y_lo = histogram.shape[0] - ((i+1) * window_size)

    #         x_left = x_base - window_size
    #         x_right = x_base + window_size

    #         non_zero_x, non_zero_y = np.nonzero(histogram)

    #         good_indices = ((non_zero_y >= y_lo) & (non_zero_y < y_hi) &
    #                         (non_zero_x >= x_left) & (non_zero_x < x_right))
            
    #         lane_pixels_x = non_zero_x[good_indices]
    #         lane_pixels_y = non_zero_y[good_indices]

    #         ## If there are enough lane pixels detected, change the base
    #         if len(lane_pixels_x) > min_pixels and len(lane_pixels_y) > min_pixels:
    #             x_base = np.mean(lane_pixels_x)

    #     return x_base
    
    
    
            

            





  