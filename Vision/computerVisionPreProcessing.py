import cv2
import Utils.config as config
from HSVFilters.YellowTrackLinesHSVFilter import YellowTrackLinesHSVFilter
from HSVFilters.BlueTrackLinesHSVFilter import BlueTrackLinesHSVFilter
from HSVFilters.ObstacleHSVFilter import ObstacleHSVFilter
from HSVFilters.RivalBotHSVFilter import RivalBotHSVFilter
from HSVFilters.TrackCompletionHSVFilter import TrackCompletionHSVFilter
from HSVFilters.ArrowHSVFilter import ArrowHSVFilter
from HSVFilters.HSVFilterInterface import HSVFilterInterface
from VisionInput import VisionInput
from typing import Dict
import numpy as np
import os
import Utils.preProccessingUtils as preProccessingUtils
import time

class vision:
    def __init__(self):
        # the manager allows for editing of the hsv filters
        # loads the filters into memory, so it doesn't have to be retrieved constantly
        self.HSVManager: Dict[str, HSVFilterInterface] = {config.YELLOW_TRACK_LINES_HSV:    YellowTrackLinesHSVFilter(),
                                                          config.BLUE_TRACK_LINES_HSV:      BlueTrackLinesHSVFilter(),
                                                          config.OBSTACLE_HSV:              ObstacleHSVFilter(),
                                                          config.TRACK_COMPLETION_HSV:      TrackCompletionHSVFilter(),
                                                          config.RIVAL_BOT_HSV:             RivalBotHSVFilter(),
                                                          config.ARROW_HSV:                 ArrowHSVFilter()}
        
        # this determines if the cnn method of arrow matching should be used
        self.modelLoaded = False    
        if config.ARROW_DETECTION_METHOD == config.CNN_METHOD:
            from CNNLogic.ArrowCNN import ArrowCNN
            import tensorflow as tf
            import keras
            # Initialize Arrow CNN
            self.arrowCNN = ArrowCNN()
            model_path = config.ARROW_CNN_PATH
            if os.path.exists(model_path):
                try:
                    self.arrowCNN.load()
                    self.modelLoaded = True
                except Exception as e:
                    print(f"Error loading Arrow CNN: {e}")
                    
        if config.ARROW_DETECTION_METHOD == config.TEMPLATE_MATCHING_METHOD:
            self.left_template = cv2.imread(config.LEFT_TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
            self.right_template = cv2.imread(config.RIGHT_TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)

        # tracks the last edited frame to ensure calculations arent performed on the same frame
        self.lastProcessedFrame = -1

        # Variables for CNN optimization
        self.inference_counter = 0
        self.last_direction = "None"
        self.last_conf = 0.0
    
    # captures the current arrow mask and saves it for training data.
    def capture_arrow(self, label):
        arrow_filter = self.HSVManager[config.ARROW_HSV]
        if arrow_filter.c is not None:
            # Get the ROI from the hsvMask
            x, y, w, h = arrow_filter.x, arrow_filter.y, arrow_filter.w, arrow_filter.h
            roi = arrow_filter.hsvMask[y:y+h, x:x+w]
            
            # Create directory if it doesn't exist
            save_dir = os.path.join(config.CAPTURED_IMAGES_DIR, label)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir, exist_ok=True)
            
            # Save with timestamp to avoid name collisions
            timestamp = int(time.time() * 1000)
            file_path = os.path.join(save_dir, f"capture_{timestamp}.png")
            cv2.imwrite(file_path, roi)
            print(f"Captured {label} arrow to {file_path}")
        else:
            print("No arrow detected in mask to capture!")
            
    def analyse_arrow(self, contour_status, frame):
        arrow_filter = self.HSVManager[config.ARROW_HSV]
        
        # this runs template matching
        if config.ARROW_DETECTION_METHOD == config.TEMPLATE_MATCHING_METHOD and contour_status:
            # gets the location of the bounding box of the arrow
            x, y, w, h = arrow_filter.x, arrow_filter.y, arrow_filter.w, arrow_filter.h
            detected_arrow = arrow_filter.hsvMask[y:y+h, x:x+w]
            resized_arrow = cv2.resize(detected_arrow, config.TEMPLATE_SIZE)
            
            # Perform Template Matching
            # TM_CCOEFF_NORMED returns a score between -1.0 and 1.0 (1.0 is a perfect match)
            res_left = cv2.matchTemplate(resized_arrow, self.left_template, cv2.TM_CCOEFF_NORMED)
            res_right = cv2.matchTemplate(resized_arrow, self.right_template, cv2.TM_CCOEFF_NORMED)
            
            # minMaxLoc returns the highest score and where it was found
            _, max_val_left, _, _ = cv2.minMaxLoc(res_left)
            _, max_val_right, _, _ = cv2.minMaxLoc(res_right)
            
            # get the max confidence of the arrow
            confidence = max(max_val_left, max_val_right)
            
            # If the match is terrible (e.g., less than 40% confidence), it's probably a shoe or a shadow
            if confidence < 0.4:
                cv2.putText(frame, f"Arrow: None ({confidence:.2f})", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  
            elif max_val_left > max_val_right:
                cv2.putText(frame, f"Arrow: Left ({max_val_left:.2f})", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, f"Arrow: Right ({max_val_right:.2f})", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
        # run CNN prediction
        if self.modelLoaded and config.ARROW_DETECTION_METHOD == config.CNN_METHOD:
            # only use the CNN if a contour is detected
            if contour_status:
                # Throttle inference to run every nth frame
                if self.inference_counter % config.CNN_INFERENCE == 0:
                    # gets the location of the bounding box of the arrow
                    x, y, w, h = arrow_filter.x, arrow_filter.y, arrow_filter.w, arrow_filter.h
                    detected_arrow = arrow_filter.hsvMask[y:y+h, x:x+w]
                    # predicts the direction of the arrow
                    self.last_direction, self.last_conf = self.arrowCNN.predict(detected_arrow)
                
                # if the CNN is confident and it's not 'None', then detect the arrow
                # if direction != "None" and conf > config.CONFIDENCE_THRESHOLD: # Confidence threshold
                cv2.putText(frame, f"Arrow: {self.last_direction} ({self.last_conf:.2f})", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                # Reset when no contour is detected
                self.last_direction = "None"
                self.last_conf = 0.0
        
        # returning the frame with the text for arrow detection added
        return frame

    def mainLoop(self):
        # captures the video input frame by frame
        while True:
            # this displays the masked version of the current frame for each HSV Filter
            frame, currFrameNo = VisionInput().Get_Frame()
            # checks that the frame being retrieved isnt a frame that has already been calculated
            if self.lastProcessedFrame != currFrameNo:
                # updates the last processed frame to the frame now being processed
                self.lastProcessedFrame = currFrameNo
                self.inference_counter += 1 # Increment for CNN throttling
                frames_to_combine = [] # this stores the frames output by various hsv filters, to combine into one processed output 
                
                # this is the hsv frame after it has been pre-processed
                frame, hsvFrame = preProccessingUtils.preprocessing(frame)
                
                for filter_name, filters in self.HSVManager.items():
                    # The update masked frame function will also display the masked frame of individual filters if needed, this is editable in the config
                    # This also allows us to determine if the combined frame with all processes done should be displayed
                    processed, contour_status = filters.Filter_Main_Process(frame=frame, hsvFrame=hsvFrame)
                    
                    # this displays the processed output when combined with every frame 
                    if config.DISPLAY_PROCCESSED_OUTPUT:
                        frames_to_combine.append(processed)
                    
                    if filter_name == config.ARROW_HSV:
                        frame = self.analyse_arrow(contour_status, frame)
                
                if config.DISPLAY_PROCCESSED_OUTPUT and frames_to_combine:
                    combinedFrame = cv2.vconcat(frames_to_combine)
                    cv2.imshow('Processed Video Feed', combinedFrame)
                    
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
            
            # this toggles the display for displaying a processed frame
            if key == ord('d'):
                config.DISPLAY_PROCCESSED_OUTPUT = not config.DISPLAY_PROCCESSED_OUTPUT

            # this trains the AI
            if key == ord('t'):
                config.DISPLAY_PROCCESSED_OUTPUT = not config.DISPLAY_PROCCESSED_OUTPUT

            # Capture keybinds
            if key == ord('1'):
                self.capture_arrow("Left")
            elif key == ord('2'):
                self.capture_arrow("Right")
            elif key == ord('3'):
                self.capture_arrow("None")

        # frees anything stored in memory
        cv2.destroyAllWindows()
