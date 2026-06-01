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
    def __init__(self):
        # the manager allows for editing of the hsv filters
        # loads the filters into memory, so it doesn't have to be retrieved constantly
        self.HSVManager: Dict[str, HSVFilterInterface] = {config.YELLOW_TRACK_LINES_HSV:    YellowTrackLinesHSVFilter(),
                                                          config.BLUE_TRACK_LINES_HSV:      BlueTrackLinesHSVFilter(),
                                                          config.OBSTACLE_HSV:              ObstacleHSVFilter(),
                                                          config.TRACK_COMPLETION_HSV:      TrackCompletionHSVFilter(),
                                                          config.RIVAL_BOT_HSV:             RivalBotHSVFilter()
                                                          }

        # tracks the last edited frame to ensure calculations arent performed on the same frame
        self.lastProcessedFrame = -1


    def mainLoop(self):
        # captures the video input frame by frame
        while True:
            # this displays the masked version of the current frame for each HSV Filter
            frame, hsvFrame, currFrameNo = VisionInput().Get_Frame()
            # checks that the frame being retrieved isnt a frame that has already been calculated
            if self.lastProcessedFrame != currFrameNo:
                # updates the last processed frame to the frame now being processed
                self.lastProcessedFrame = currFrameNo
                for filters in self.HSVManager.values():
                    # The update masked frame function will also display the masked frame if needed, this is editable in the config
                    filters.Filter_Main_Process(frame=frame, hsvFrame=hsvFrame)

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