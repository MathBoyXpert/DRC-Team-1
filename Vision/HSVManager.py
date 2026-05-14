import cv2
import config
import pickle
import os
from HSVfilters import HSVFilter
class HSVManager:

    # HSV manager constructor
    def __init__(self, vision):
        self.vision = vision
        self.savedTrackLinesHsvFilter = HSVFilter();
        self.Retrieve_HSV_Filter() # initialises the hsv filter in the manager

    # this allows you to create and save a new filter
    def Apply_New_Filter(self) -> HSVFilter:
        self.Save_HSV_Filter()
        self.Retrieve_HSV_Filter()
    
    # this retrieves the most recently saved HSV filter
    def Retrieve_HSV_Filter(self) -> HSVFilter:
        # retrieve the HSV filter to use
        loadedHsvFilter = None;
        if os.path.isfile(config.TRACK_LINES_HSV_FILTER_FILE):
            print("Loaded Track Lines HSV Filter")
            with open(config.TRACK_LINES_HSV_FILTER_FILE, 'rb') as file:
                self.savedTrackLinesHsvFilter = pickle.load(file)
        else:
            # this makes it so that the initial filter is created
            self.Save_HSV_Filter()
            # and now it is loaded
            self.Retrieve_HSV_Filter()
            print("Loaded New Track Lines HSV Filter")

    # displays the current masked frame
    def Display_Track_Lines_Masked_Frame(self):
        # gets the frame in a hsv colour space
        good, frame = self.vision.read()

        # bad video read
        if not good:
            print("Error: Can't receive frame. Exiting...")

        # converts the current frame into HSV and then creates a mask for Blue and Yello values


        hsvFrame = cv2.cvtColor(frame, config.HSV_SPACE)
        blueHsvMask = cv2.inRange(hsvFrame, self.savedTrackLinesHsvFilter.Get_Blue_Min_Vals_Arr(), self.savedTrackLinesHsvFilter.Get_Blue_Max_Vals_Arr())
        yellowHsvMask = cv2.inRange(hsvFrame, self.savedTrackLinesHsvFilter.Get_Yellow_Min_Vals_Arr(), self.savedTrackLinesHsvFilter.Get_Yellow_Max_Vals_Arr())

        # this combines the yellow and blue masks
        linesHsvMask = cv2.bitwise_or(blueHsvMask, yellowHsvMask)

        # this applys the mask on the current frame and saves tha masked frame 
        maskedframe = cv2.bitwise_and(frame, frame, mask=linesHsvMask)

        # display the HSV masked frame
        cv2.imshow(config.MASKED_FRAME_TRACK_LINES, maskedframe)

    # this opens the HSV GUI and allows the user to save a new HSV filter
    def Save_HSV_Filter(self, hsvFilter=None):
        if hsvFilter is None:
            # creates the HSV editor GUI
            self.HSV_GUI_Adjustments()
            print("Press s to save the HSV Filter")
            
            # this creates another infinite loop that is used to preview the new HSV settings
            while True:
                # gets teh current hsv values from the GUI sliders and then displays the Masked frame
                self.savedTrackLinesHsvFilter = self.Get_HSV_Filter_From_GUI()
                self.Display_Track_Lines_Masked_Frame()          
                
                # this waits for an input "s" which will then save the new HSV filter in a file and then end the HSV editing process 
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    self.savedTrackLinesHsvFilter = self.Get_HSV_Filter_From_GUI()
                    cv2.destroyWindow(config.TRACKBAR_WINDOW_TRACK_LINES)

                    with open(config.TRACK_LINES_HSV_FILTER_FILE, 'wb') as file:
                        pickle.dump(self.savedTrackLinesHsvFilter, file)

                    print("New Filter Saved")
                    break
                

    # this creates and initialises the HSV Filter GUI to save the filter
    def HSV_GUI_Adjustments(self):
        # trackbar window constant is the name of the winodw, window normal allows it to be resized
        cv2.namedWindow(config.TRACKBAR_WINDOW_TRACK_LINES, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(config.TRACKBAR_WINDOW_TRACK_LINES, 350, 700)
        
        # basic function for the trackbar call back, not needed, hence do nothing
        def doNothing(self):
            pass    

        # creating the trackbars for the Blue HSV filtering
        cv2.createTrackbar("blue_hMin", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)
        cv2.createTrackbar("blue_sMin", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)
        cv2.createTrackbar("blue_vMin", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)
        cv2.createTrackbar("blue_hMax", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)
        cv2.createTrackbar("blue_sMax", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)
        cv2.createTrackbar("blue_vMax", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)

        # creating the trackbars for the Yellow HSV filtering
        cv2.createTrackbar("yellow_hMin", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)
        cv2.createTrackbar("yellow_sMin", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)
        cv2.createTrackbar("yellow_vMin", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)
        cv2.createTrackbar("yellow_hMax", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)
        cv2.createTrackbar("yellow_sMax", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)
        cv2.createTrackbar("yellow_vMax", config.TRACKBAR_WINDOW_TRACK_LINES, 0, 255, doNothing)

        # Setting initial trackbar positions
        # set trackbar positition for blue sliders
        cv2.setTrackbarPos("blue_hMin", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.blue_hMin)
        cv2.setTrackbarPos("blue_sMin", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.blue_sMin)
        cv2.setTrackbarPos("blue_vMin", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.blue_vMin)
        cv2.setTrackbarPos("blue_hMax", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.blue_hMax)
        cv2.setTrackbarPos("blue_sMax", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.blue_sMax)
        cv2.setTrackbarPos("blue_vMax", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.blue_vMax)
        
        # set trackbar positition for yellow sliders
        cv2.setTrackbarPos("yellow_hMin", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.yellow_hMin)
        cv2.setTrackbarPos("yellow_sMin", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.yellow_sMin)
        cv2.setTrackbarPos("yellow_vMin", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.yellow_vMin)
        cv2.setTrackbarPos("yellow_hMax", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.yellow_hMax)
        cv2.setTrackbarPos("yellow_sMax", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.yellow_sMax)
        cv2.setTrackbarPos("yellow_vMax", config.TRACKBAR_WINDOW_TRACK_LINES, self.savedTrackLinesHsvFilter.yellow_vMax)


    # this gets the current details of the filter form the GUI and returns it as a HSVFilter Obj
    def Get_HSV_Filter_From_GUI(self) -> HSVFilter:
        hsvfilter = HSVFilter()

        # getting the trackbar values for the Blue HSV filtering
        hsvfilter.blue_hMin = cv2.getTrackbarPos("blue_hMin", config.TRACKBAR_WINDOW_TRACK_LINES)
        hsvfilter.blue_sMin = cv2.getTrackbarPos("blue_sMin", config.TRACKBAR_WINDOW_TRACK_LINES)
        hsvfilter.blue_vMin = cv2.getTrackbarPos("blue_vMin", config.TRACKBAR_WINDOW_TRACK_LINES)
        hsvfilter.blue_hMax = cv2.getTrackbarPos("blue_hMax", config.TRACKBAR_WINDOW_TRACK_LINES)
        hsvfilter.blue_sMax = cv2.getTrackbarPos("blue_sMax", config.TRACKBAR_WINDOW_TRACK_LINES)
        hsvfilter.blue_vMax = cv2.getTrackbarPos("blue_vMax", config.TRACKBAR_WINDOW_TRACK_LINES)

        # getting the trackbar values for the Yellow HSV filtering
        hsvfilter.yellow_hMin = cv2.getTrackbarPos("yellow_hMin", config.TRACKBAR_WINDOW_TRACK_LINES)
        hsvfilter.yellow_sMin = cv2.getTrackbarPos("yellow_sMin", config.TRACKBAR_WINDOW_TRACK_LINES)
        hsvfilter.yellow_vMin = cv2.getTrackbarPos("yellow_vMin", config.TRACKBAR_WINDOW_TRACK_LINES)
        hsvfilter.yellow_hMax = cv2.getTrackbarPos("yellow_hMax", config.TRACKBAR_WINDOW_TRACK_LINES)
        hsvfilter.yellow_sMax = cv2.getTrackbarPos("yellow_sMax", config.TRACKBAR_WINDOW_TRACK_LINES)
        hsvfilter.yellow_vMax = cv2.getTrackbarPos("yellow_vMax", config.TRACKBAR_WINDOW_TRACK_LINES)

        return hsvfilter