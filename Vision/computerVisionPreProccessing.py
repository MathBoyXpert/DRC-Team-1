import cv2
import config
from HSVfilters import HSVFilter
from HSVManager import HSVManager

class vision:
    # constants
    TRACKBAR_WINDOW = "Track Bar Window"
    
    def __init__(self):
        self.vision = cv2.VideoCapture(config.VIDEO_INPUT)

        # intially retreieve the HSV filter
        # the manager allows for editing of the hsv filter
        # savedHsvFilter loads the filter into memory, so it doesnt have to be retrieved constantly
        self.PersonalHSVManager = HSVManager(self.vision)
        self.PersonalHSVManager.Retrieve_HSV_Filter() # initialises the hsv filter in the manager



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

            self.PersonalHSVManager.Display_Masked_Frame()

            # display the curr frame
            cv2.imshow('Live Video Feed', frame)


            #############################
            ### LIVE BEDUGGING INPUTS ###
            #############################

            # checks for an exit input
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # checks for an input to change the hsv filter
            if cv2.waitKey(1) & 0xFF == ord('h'):
                cv2.destroyWindow("Masked Frame")
                self.PersonalHSVManager.Apply_New_Filter()
                

        # frees anything stored in memory
        self.vision.release()
        cv2.destroyAllWindows()
