import numpy as np
import cv2
import os

class TrackLinesFilter:

    def find_lane_pixels(self, frame, window_name):
        MIN_PIXELS = 10
        WINDOW_WIDTH = 45
	    # 1) Take a histogram of the bottom half of the image
        histogram = np.sum(frame[frame.shape[0]//2:,:], axis=0)

	    # 2) Find the peak of the left and right halves of the histogram
        midpoint = int(histogram.shape[0] / 2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint
        x_base = np.argmax(histogram[:])

	    # 3) Step through windows to track the line upward
        y = frame.shape[1]
        all_x = []
        all_y = []

        msk = frame.copy()

        while y > 0:
            ## Left Threshold

            # img = frame[y-40:y, leftx_base-50:leftx_base+50]
            # contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # for contour in contours:
            #     M = cv2.moments(contour)
            #     if M["m00"] != 0:
            #         cx = int(M["m10"]/M["m00"])
            #         cy = int(M["m01"]/M["m00"])
            #         lx.append(leftx_base - 50 + cx)
            #         ly.append(y - 40 + cy)
            #         leftx_base = leftx_base - 50 + cx
            
            # Right Threshold
            x_left = max(0, x_base - WINDOW_WIDTH)
            x_right = min(frame.shape[1], x_base + WINDOW_WIDTH)

            img = frame[y-40:y, x_left:x_right]

            if cv2.countNonZero(img) >= MIN_PIXELS:
                # contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                nonzero_y, nonzero_x = np.nonzero(img)
                # for contour in contours:
                #     M = cv2.moments(contour)
                #     if M["m00"] != 0:
                #         cx = int(M["m10"]/M["m00"])
                #         cy = int(M["m01"]/M["m00"])
                #         all_x.append(x_left + cx)
                #         all_y.append(y - 40 + cy)
                #         x_base = x_left + cx

                all_x.extend(nonzero_x + x_left)
                all_y.extend(nonzero_y + (y - 40))

                cx = int(np.mean(nonzero_x))
                x_base = x_left + cx

            # cv2.rectangle(msk, (leftx_base-50, y), (leftx_base + 50, y-40), (255,255,255), 2)
                cv2.rectangle(msk, (x_base - WINDOW_WIDTH, y), (x_base + WINDOW_WIDTH, y-40), (255,255,255), 2)

            y-=40
        
        # left_fit = None
        fit = None

        # if len(lx) >= 3:
        #     left_fit = np.polyfit(ly, lx, 2)
        
        if len(all_x) >= 3:
            fit = np.polyfit(all_y, all_x, 2)
            self.detect_polynomial(msk, fit, frame.shape[0])
        

        cv2.imshow(f"{window_name}", msk)

    def detect_polynomial(self, frame, fit, height):
        plot_y = np.linspace(0, height - 1, height)

        x = np.polyval(fit, plot_y)
        for i in range(len(plot_y) - 1):
            pt1 = (int(x[i]), int(plot_y[i]))
            pt2 = (int(x[i+1]), int(plot_y[i+1]))
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
    
    
    
            

            





  