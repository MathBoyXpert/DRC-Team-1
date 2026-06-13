import cv2
import config
from HSVFilters.YellowTrackLinesHSVFilter import YellowTrackLinesHSVFilter
from HSVFilters.BlueTrackLinesHSVFilter import BlueTrackLinesHSVFilter
from HSVFilters.ObstacleHSVFilter import ObstacleHSVFilter
from HSVFilters.RivalBotHSVFilter import RivalBotHSVFilter
from HSVFilters.TrackCompletionHSVFilter import TrackCompletionHSVFilter
from HSVFilters.ArrowHSVFilter import ArrowHSVFilter
from HSVFilters.HSVFilterInterface import HSVFilterInterface
from VisionInput import VisionInput
from ArrowCNN import ArrowCNN
from typing import Dict
import numpy as np
import tensorflow as tf
import keras
import os
import preProccessingUtils
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

        # Initialize Arrow CNN
        self.arrowCNN = ArrowCNN()
        self.modelLoaded = False
        model_path = config.ARROW_CNN_PATH
        if os.path.exists(model_path):
            try:
                self.arrowCNN.load()
                self.modelLoaded = True
            except Exception as e:
                print(f"Error loading Arrow CNN: {e}")

        # tracks the last edited frame to ensure calculations arent performed on the same frame
        self.lastProcessedFrame = -1
    
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

    def mainLoop(self):
        # captures the video input frame by frame
        while True:
            # this displays the masked version of the current frame for each HSV Filter
            frame, currFrameNo = VisionInput().Get_Frame()
            # checks that the frame being retrieved isnt a frame that has already been calculated
            if self.lastProcessedFrame != currFrameNo:
                # updates the last processed frame to the frame now being processed
                self.lastProcessedFrame = currFrameNo
                framesToCombine = [] # this stores the frames output by various hsv filters, to combine into one processed output 
                
                # this is the hsv frame after it has been pre-processed
                hsvFrame = preProccessingUtils.preprocessing(frame)
                # this resizes and compresses teh frame
                frame = cv2.resize(frame, (config.WIDTH, config.HEIGHT), interpolation=cv2.INTER_AREA)
                
                for filter_name, filters in self.HSVManager.items():
                    # The update masked frame function will also display the masked frame of individual filters if needed, this is editable in the config
                    # This also allows us to determine if the combined frame with all processes done should be displayed
                    processed = filters.Filter_Main_Process(frame=frame, hsvFrame=hsvFrame)
                    
                    # this displays the processed output when combined with every frame 
                    if config.DISPLAY_PROCCESSED_OUTPUT:
                        framesToCombine.append(processed)
                    
                    # if this is the arrow filter, run CNN prediction
                    if filter_name == config.ARROW_HSV and self.modelLoaded:
                        # predicts the direction of the arrow
                        direction, conf = self.arrowCNN.predict(filters.hsvMask)
                        # if the CNN is confident and it's not 'None', then detect the arrow
                        # if direction != "None" and conf > config.CONFIDENCE_THRESHOLD: # Confidence threshold
                        cv2.putText(frame, f"Arrow: {direction} ({conf:.2f})", (10, 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                if config.DISPLAY_PROCCESSED_OUTPUT and framesToCombine:
                    combinedFrame = cv2.vconcat(framesToCombine)
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
