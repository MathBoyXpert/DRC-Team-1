import cv2
import config
from HSVFilters.TrackLinesHSVFilter import TrackLinesHSVFilter
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
        self.HSVManager: Dict[str, HSVFilterInterface] = {config.TRACK_LINES_HSV: TrackLinesHSVFilter(),
                                                        config.OBSTACLE_HSV: ObstacleHSVFilter(),
                                                        config.TRACK_COMPLETION_HSV: TrackCompletionHSVFilter(),
                                                        config.RIVAL_BOT_HSV: RivalBotHSVFilter()}

    def mainLoop(self):
        # captures the video input frame by frame
        while True:
            # gets the current frame
            frame = VisionInput().Get_Frame()            

            # this displays the masked version of the current frame for each HSV Filter
            frame = VisionInput().Get_Frame()
            hsvFrame = VisionInput().Get_HSV_Frame()
            for filters in self.HSVManager.values():
                filters.Display_Masked_Frame(frame=frame, hsv_frame=hsvFrame)

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
