import cv2
import config
from HSVFilters.YellowTrackLinesHSVFilter import YellowTrackLinesHSVFilter
from HSVFilters.BlueTrackLinesHSVFilter import BlueTrackLinesHSVFilter
from HSVFilters.ObstacleHSVFilter import ObstacleHSVFilter
from HSVFilters.RivalBotHSVFilter import RivalBotHSVFilter
from HSVFilters.TrackCompletionHSVFilter import TrackCompletionHSVFilter
from HSVFilters.HSVFilterInterface import HSVFilterInterface
from VisionInput import VisionInput
from typing import Dict

class vision:
    # constants

    # variables
    
    
    def __init__(self):
        # the manager allows for editing of the hsv filters
        # loads the filters into memory, so it doesn't have to be retrieved constantly
        self.HSVManager: Dict[str, HSVFilterInterface] = {config.YELLOW_TRACK_LINES_HSV:    YellowTrackLinesHSVFilter(),
                                                          config.BLUE_TRACK_LINES_HSV:      BlueTrackLinesHSVFilter(),
                                                          config.OBSTACLE_HSV:              ObstacleHSVFilter(),
                                                          config.TRACK_COMPLETION_HSV:      TrackCompletionHSVFilter(),
                                                          config.RIVAL_BOT_HSV:             RivalBotHSVFilter()}
        
        # tracks the last edited frame to ensure calculations arent performed on the same frame
        self.lastProcessedFrame = -1
        

    def mainLoop(self):
        # captures the video input frame by frame
        while True:
            # this displays the masked version of the current frame for each HSV Filter
            frame, currFrameNo = VisionInput().Get_Frame()
            # checks that the frame being retrieved isnt a frame that has already been calculated
            if self.lastProcessedFrame != currFrameNo:
                # updates the last processed frame to the frame now being processed
                self.lastProcessedFrame = currFrameNo
                for filters in self.HSVManager.values():
                    # The update masked frame function will also display the masked frame if needed, this is editable in the config
                    filters.Filter_Main_Process()

                # display the curr frame
                cv2.imshow('Live Video Feed', frame)

            #############################
            ### LIVE DEBUGGING INPUTS ###
            #############################

            # grabs the key pressed
            key = cv2.waitKey(1) & 0xFF

            # checks for an exit input
            if key == ord('q'):
                break

            # checks for an input to change the hsv filter
            if key == ord('h'):
                # destroys the current masked frame and for the HSVManager to display it within itself 
                for filters in self.HSVManager.values():
                    if config.Display_The_Frame[filters.Get_Filter_Name()]:
                        cv2.destroyWindow(filters.Get_Filter_Frame_Name())
                    # this applies the new HSV filter after we edit it and save it 
                    filters.Apply_New_Filter()
                
        # frees anything stored in memory
        cv2.destroyAllWindows()


# # Find geometric contours (shapes) in the binary mask.
#     # '1' refers to cv2.RETR_EXTERNAL (retrieves only the outermost contours).
#     # cv2.CHAIN_APPROX_NONE stores all contour boundary points without compression.
#     contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    
#     # Check if at least one contour was found in the frame.
#     if len(contours) > 0:
        
#         # Isolate the largest contour found based on physical area (helps filter out noise).
#         c = max(contours, key=cv2.contourArea)
        
#         # Calculate the spatial moments of the largest contour.
#         # Moments capture geometric properties like area, centroid, and orientation.
#         M = cv2.moments(c)
        
#         # Prevent a division-by-zero error. 'm00' represents the total area of the contour.
#         if M["m00"] != 0:
            
#             # Calculate the X-coordinate of the centroid (center of mass).
#             # 'm10' is the first-order spatial moment for X.
#             cx = int(M['m10'] / M['m00'])
            
#             # Calculate the Y-coordinate of the centroid.
#             # 'm01' is the first-order spatial moment for Y.
#             cy = int(M['m01'] / M['m00'])
            
#             # Print the calculated center coordinates to the console terminal for debugging.
#             print("CX : " + str(cx) + " CY : " + str(cy))
            
#             # --- Steering Control Logic Based on Centroid X-Position ---
#             # If the target centroid shifts too far to the right, command a left turn.
#             if cx >= 120:
#                 print("Turn Left")
                
#             # If the centroid stays safely in the center channel, maintain course.
#             if cx < 120 and cx > 40:
#                 print("On Track!")
                
#             # If the target centroid shifts too far to the left, command a right turn.
#             if cx <= 40:
#                 print("Turn Right")
#             # -----------------------------------------------------------
            
#             # Draw a small, solid white circle at the centroid coordinates (cx, cy).
#             # Radius = 5 pixels, Color = (255, 255, 255) [White], Thickness = -1 [Filled].
#             cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
            
#     # Draw the outline of the largest detected contour 'c' back onto the original frame.
#     # Contour Index = -1 (draws the specific passed contour), Color = (0, 255, 0) [Green], Thickness = 1.
#     cv2.drawContours(frame, c, -1, (0, 255, 0), 1)