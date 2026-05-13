import cv2
import config
import pickle
import os
from HSVfilters import HSVFilter
class HSVManager:

    TRACKBAR_WINDOW = "Track Window"

    def __init__(self, vision):
        self.vision = vision

    # this allows you to create and save a new filter
    def Apply_New_Filter(self) -> HSVFilter:
        self.Save_HSV_Filter()
        self.Retrieve_HSV_Filter()
    
    # this retrieves the most recently saved HSV filter
    def Retrieve_HSV_Filter(self) -> HSVFilter:
        # retrieve the HSV filter to use
        loadedHsvFilter = None;
        if os.path.isfile("savedHsvFilter.pkl"):
            print("loaded")
            with open('savedHsvFilter.pkl', 'rb') as file:
                self.savedHsvFilter = pickle.load(file)
        else:
            # this makes it so that the initial filter is created
            self.Save_HSV_Filter()
            # and now it is loaded
            self.savedHsvFilter = self.Retrieve_HSV_Filter()


    def Display_Masked_Frame(self):
        # gets the frame in a hsv colour space
        good, frame = self.vision.read()

        # bad video read
        if not good:
            print("Error: Can't receive frame. Exiting...")

        hsvFrame = cv2.cvtColor(frame, config.HSV_SPACE)
        blueHsvMask = cv2.inRange(hsvFrame, self.savedHsvFilter.Get_Blue_Min_Vals_Arr(), self.savedHsvFilter.Get_Blue_Max_Vals_Arr())
        yellowHsvMask = cv2.inRange(hsvFrame, self.savedHsvFilter.Get_Yellow_Min_Vals_Arr(), self.savedHsvFilter.Get_Yellow_Max_Vals_Arr())

        linesHsvMask = cv2.bitwise_or(blueHsvMask, yellowHsvMask)

        maskedframe = cv2.bitwise_and(frame, frame, mask=linesHsvMask)

        # display the HSV masked frame
        cv2.imshow("Masked Frame", maskedframe)

    # this opens the HSV GUI and allows the user to save a new HSV filter
    def Save_HSV_Filter(self, hsvFilter=None):
        if hsvFilter is None:
            self.HSV_GUI_Adjustments()
            print("Press s to save the HSV Filter")
            
            while True:  
                self.savedHsvFilter = self.Get_HSV_Filter_From_GUI()
                self.Display_Masked_Frame()          
                
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    self.savedHsvFilter = self.Get_HSV_Filter_From_GUI()
                    cv2.destroyWindow(self.TRACKBAR_WINDOW)

                    with open('savedHsvFilter.pkl', 'wb') as file:
                        pickle.dump(self.savedHsvFilter, file)
                    break

    # this creates and initialises the HSV Filter GUI to save the filter
    def HSV_GUI_Adjustments(self):
        # trackbar window constant is the name of the winodw, window normal allows it to be resized
        cv2.namedWindow(self.TRACKBAR_WINDOW, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)
        
        # basic function for the trackbar call back, not needed, hence do nothing
        def doNothing(self):
            pass    

        # creating the trackbars for the Blue HSV filtering
        cv2.createTrackbar("blue_hMin", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("blue_sMin", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("blue_vMin", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("blue_hMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("blue_sMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("blue_vMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)

        # creating the trackbars for the Yellow HSV filtering
        cv2.createTrackbar("yellow_hMin", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("yellow_sMin", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("yellow_vMin", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("yellow_hMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("yellow_sMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)
        cv2.createTrackbar("yellow_vMax", self.TRACKBAR_WINDOW, 0, 255, doNothing)

    # this gets the current details of the filter form the GUI and returns it as a HSVFilter Obj
    def Get_HSV_Filter_From_GUI(self) -> HSVFilter:
        hsvfilter = HSVFilter()

        # getting the trackbar values for the Blue HSV filtering
        hsvfilter.blue_hMin = cv2.getTrackbarPos("blue_hMin", self.TRACKBAR_WINDOW)
        hsvfilter.blue_sMin = cv2.getTrackbarPos("blue_sMin", self.TRACKBAR_WINDOW)
        hsvfilter.blue_vMin = cv2.getTrackbarPos("blue_vMin", self.TRACKBAR_WINDOW)
        hsvfilter.blue_hMax = cv2.getTrackbarPos("blue_hMax", self.TRACKBAR_WINDOW)
        hsvfilter.blue_sMax = cv2.getTrackbarPos("blue_sMax", self.TRACKBAR_WINDOW)
        hsvfilter.blue_vMax = cv2.getTrackbarPos("blue_vMax", self.TRACKBAR_WINDOW)

        # getting the trackbar values for the Yellow HSV filtering
        hsvfilter.yellow_hMin = cv2.getTrackbarPos("yellow_hMin", self.TRACKBAR_WINDOW)
        hsvfilter.yellow_sMin = cv2.getTrackbarPos("yellow_sMin", self.TRACKBAR_WINDOW)
        hsvfilter.yellow_vMin = cv2.getTrackbarPos("yellow_vMin", self.TRACKBAR_WINDOW)
        hsvfilter.yellow_hMax = cv2.getTrackbarPos("yellow_hMax", self.TRACKBAR_WINDOW)
        hsvfilter.yellow_sMax = cv2.getTrackbarPos("yellow_sMax", self.TRACKBAR_WINDOW)
        hsvfilter.yellow_vMax = cv2.getTrackbarPos("yellow_vMax", self.TRACKBAR_WINDOW)


        return hsvfilter