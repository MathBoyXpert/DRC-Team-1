import cv2
import config
from HSVManager import HSVManager

class vision:
    # constants
    
    def __init__(self):
        self.vision = cv2.VideoCapture(config.VIDEO_INPUT)

        # intially retreieve the HSV filter
        # the manager allows for editing of the hsv filter
        # savedHsvFilter loads the filter into memory, so it doesnt have to be retrieved constantly
        self.PersonalHSVManager = HSVManager(self.vision)

    def mainLoop(self):
        # this is the comp vision obj

        # see if it opened properly
        if not self.vision.isOpened():
            print("Error: Could not open video device")
            exit()

        # captures the video input frame by frame
        while True:
            # good is a boolean that lets you see if the frame is read well, frame is the current frame
            good, frame = self.vision.read()

            # bad video read
            if not good:
                print("Error: Can't receive frame. Exiting...")
                break

            # this displayes the masked version of the current frame for line detection
            self.PersonalHSVManager.Display_Track_Lines_Masked_Frame()

            # display the curr frame
            cv2.imshow('Live Video Feed', frame)

            #############################
            ### LIVE DEDUGGING INPUTS ###
            #############################

            # grabs the key pressed
            key = cv2.waitKey(1) & 0xFF

            # checks for an exit input
            if key == ord('q'):
                break

            # checks for an input to change the hsv filter
            if key == ord('h'):
                # destorys the current maked frame and for the HSVManager to display it within itself 
                cv2.destroyWindow(config.MASKED_FRAME_TRACK_LINES)
                # this applys the new HSV filter after we edit it and save it 
                self.PersonalHSVManager.Apply_New_Filter()
                
        # frees anything stored in memory
        self.vision.release()
        cv2.destroyAllWindows()
