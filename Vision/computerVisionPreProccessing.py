import cv2
import config as config
from HSVfilters import HSVFilter

class vision:
    # constants
    TRACKBAR_WINDOW = "Track Bar Window"

    def mainLoop(self):
        # this is the comp vision obj
        vision = cv2.VideoCapture(config.VIDEO_INPUT)

        # see if it opened properly
        if not vision.isOpened():
            print("Error: Could not open video device")
            exit()

        # captures the video input frame by frame
        while True:
            # good is a boolean that lets you see if the frame is read well, frame is the current frame
            good, frame = vision.read()

            # bad video read
            if not good:
                print("Error: Can't receive frame. Exiting...")
                break

            # gets the frame in a hsv colour space
            hsv_frame = cv2.cvtColor(frame, config.HSV_SPACE)

            # display the curr frame
            cv2.imshow('Live Video Feed', frame)

            # checks for an exit input
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # frees anything stored in memory
        vision.release()
        cv2.destroyAllWindows()

    def HSV_GUI_Adjustments(self):
        # trackbar window constant is the name of the winodw, window normal allows it to be resized
        cv2.namedWindow(self.TRACKBAR_WINDOW, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)
        
        def doNothing(self):
            pass    

        cv2.createTrackbar("blue_hMin", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("blue_sMin", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("blue_vMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("blue_hMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("blue_sMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("blue_vMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)

        cv2.createTrackbar("yellow_hMin", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("yellow_sMin", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("yellow_vMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("yellow_hMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("yellow_sMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("yellow_vMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)

    def Get_HSV_Filter_From_GUI(self):
        hsvfilter = HSVFilter()
        hsvfilter.blue_hMin = cv2.getTrackbarPos("blue_hMin", self.TRACKBAR_WINDOW)
        hsvfilter.blue_sMin = cv2.getTrackbarPos("blue_sMin", self.TRACKBAR_WINDOW)
        hsvfilter.blue_vMin = cv2.getTrackbarPos("blue_vMin", self.TRACKBAR_WINDOW)
        hsvfilter.blue_hMax = cv2.getTrackbarPos("blue_hMax", self.TRACKBAR_WINDOW)
        hsvfilter.blue_sMax = cv2.getTrackbarPos("blue_sMax", self.TRACKBAR_WINDOW)
        hsvfilter.blue_vMax = cv2.getTrackbarPos("blue_vMax", self.TRACKBAR_WINDOW)

        hsvfilter.yellow_hMin = cv2.getTrackbarPos("yellow_hMin", self.TRACKBAR_WINDOW)
        hsvfilter.yellow_sMin = cv2.getTrackbarPos("yellow_sMin", self.TRACKBAR_WINDOW)
        hsvfilter.yellow_vMin = cv2.getTrackbarPos("yellow_vMin", self.TRACKBAR_WINDOW)
        hsvfilter.yellow_hMax = cv2.getTrackbarPos("yellow_hMax", self.TRACKBAR_WINDOW)
        hsvfilter.yellow_sMax = cv2.getTrackbarPos("yellow_sMax", self.TRACKBAR_WINDOW)
        hsvfilter.yellow_vMax = cv2.getTrackbarPos("yellow_vMax", self.TRACKBAR_WINDOW)

        return hsvfilter

if __name__ =="__main__":
    x = vision()
    x.mainLoop()