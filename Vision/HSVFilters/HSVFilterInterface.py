from abc import ABC, abstractmethod
import cv2
import pickle
import os
import config
from VisionInput import VisionInput
from .TrackLinesFilter import TrackLinesFilter
class HSVFilterInterface(ABC):



    def __init__(self):
        self.Retrieve_HSV_Filter() # initialises the hsv filter
        # this makes it so the masked hsv frame is displayed reguardless of config settings
        self.isFilterBeingEdited = False
        self.hsvMask = None
        self.c = None
        self.cx = None
        self.cy = None
        self.trackLines = TrackLinesFilter()

    @abstractmethod
    def debug_print_filters(self):
        pass

    @abstractmethod
    def Get_Min_Vals_Arr(self):
        pass

    @abstractmethod
    def Get_Max_Vals_Arr(self):
        pass

    @abstractmethod
    def Get_Filter_Name(self) -> str:
        pass

    def Get_Filter_File_Name(self):
        return config.Hsv_Filter_File_Names_Dict[self.Get_Filter_Name()]

    def Get_Filter_GUI_Name(self):
        return config.Trackbar_Names_Dict[self.Get_Filter_Name()]

    def Get_Filter_Frame_Name(self):
        return config.Masked_Window_Names_Dict[self.Get_Filter_Name()]

    # checks if I want the frame for the filter to be displayed (this can be changed in config)
    def Should_Filtered_Frame_Be_Displayed(self):
        return config.Display_The_Frame[self.Get_Filter_Name()]

    # this allows you to create and save a new filter
    def Apply_New_Filter(self):
        self.isFilterBeingEdited = True
        # saves a new HSV filter that is applied after it has been edited (the save hsv func also sets 'isFilterBeingEdited' to false)
        self.Save_HSV_Filter()
        # this then retrives the newly saved filter and applies it
        self.Retrieve_HSV_Filter()

    # this retrieves the most recently saved HSV filter
    def Retrieve_HSV_Filter(self):
        # retrieve the HSV filter to use
        if os.path.isfile(self.Get_Filter_File_Name()):
            print(f"Loaded {self.Get_Filter_File_Name()} HSV Filter")
            with open(self.Get_Filter_File_Name(), 'rb') as file:
                self.__dict__.update(pickle.load(file).__dict__)

        # for the case where there is no saved HSV filter
        else:
            self.isFilterBeingEdited = True
            # this makes it so that the initial filter is created and saved (the save hsv func also sets 'isFilterBeingEdited' to false)
            self.Save_HSV_Filter()
            # this recursively loads the newly saved filter
            self.Retrieve_HSV_Filter()
            print(f"Loaded New {self.Get_Filter_File_Name()} HSV Filter")

    # this opens the HSV GUI and allows the user to save a new HSV filter
    def Save_HSV_Filter(self):
        # creates the HSV editor GUI
        self.HSV_GUI_Adjustments()
        print("Press s to save the HSV Filter")

        # this creates another infinite loop that is used to preview the new HSV settings
        while True:
            # gets the current hsv values from the GUI sliders and then displays the Masked frame
            self.Update_HSV_Filter_From_GUI()
            # this automatically updates the masked frame and contours in accordance with the values in the GUI
            self.Filter_Main_Process(VisionInput().Get_Frame()[0], VisionInput().Get_Frame()[1])

            # this waits for an input "s" which will then save the new HSV filter in a file and then end the HSV editing process 
            if cv2.waitKey(1) & 0xFF == ord('s'):
                self.Update_HSV_Filter_From_GUI()
                cv2.destroyWindow(self.Get_Filter_GUI_Name())
                cv2.destroyWindow(self.Get_Filter_Frame_Name())

                # to signify that the hsv is no longer being edited, and to not save it in that state
                self.isFilterBeingEdited = False

                with open(self.Get_Filter_File_Name(), 'wb') as file:
                    pickle.dump(self, file)

                print(f"New {self.Get_Filter_File_Name()} Filter Saved")
                break

    # this creates and initialises the HSV Filter GUI to save the filter
    def HSV_GUI_Adjustments(self):
        # trackbar window constant is the name of the winodw, window normal allows it to be resized
        cv2.namedWindow(self.Get_Filter_GUI_Name(), cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.Get_Filter_GUI_Name(), 350, 700)

        # basic function for the trackbar call back, not needed, hence do nothing
        def doNothing(self):
            pass    

        # creating the trackbars to adjust HSV filtering
        for hsvAttribute in self.hsvList:
            cv2.createTrackbar(hsvAttribute, self.Get_Filter_GUI_Name(), 0, config.HSV_MAX_VAL, doNothing)
            # Setting initial trackbar positions based on past filters
            cv2.setTrackbarPos(hsvAttribute, self.Get_Filter_GUI_Name(), self.hsvValueMap[hsvAttribute])

    # this gets the current details of the filter form the GUI and returns it as a HSVFilter Obj
    def Update_HSV_Filter_From_GUI(self):
        # getting the trackbar values for the HSV filtering
        for hsvAttribute in self.hsvList:
            self.hsvValueMap[hsvAttribute] = cv2.getTrackbarPos(hsvAttribute, self.Get_Filter_GUI_Name())
    # this is the main order in which interal functions should run
    def Filter_Main_Process(self, frame, hsvFrame):
        # this finds the new masked frame
        self.Update_Masked_Frame(hsvFrame)
        # this calculates the new contour
        self.Find_Centroid()

        self.trackLines.find_lane_pixels(hsvFrame)
        # this displays the frame if allowed by the config
        self.Display_Masked_Frame(frame)

    # updates the current masked frame
    def Update_Masked_Frame(self, hsv_frame):
        # creates a mask for the HSV values
        self.hsvMask = cv2.inRange(hsv_frame, self.Get_Min_Vals_Arr(), self.Get_Max_Vals_Arr())

    # this calculates and finds a contour on the current masked frame
    def Find_Centroid(self):
        # CHAIN_APPROX_SIMPLE only keeps corner points instead of every single single pixel in a contour
        # cv2.RETR_EXTERNAL tells OpenCV to only look for and return the absolute outermost shapes
        contours, _ = cv2.findContours(self.hsvMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # if at least 1 contour was found
        if contours:
            # get the largest contour 
            self.c = max(contours, key=cv2.contourArea)
            # this calculates a bunch of stuff on the pixels of the contoured frame to allow for centroid calculations
            M = cv2.moments(self.c)

            # M["m00"] != 0 checks that there is at least 1 masked pixel
            if M["m00"] != 0:
                # this calculates the center of the masked pixels
                # sum of x coordinates for masked pixels over the the total number of masked pixels
                self.cx = int(M['m10'] / M['m00'])
                # sum of x coordinates for masked pixels over the the total number of masked pixels                
                self.cy = int(M['m01'] / M['m00'])
            # this ensures that if a centroid can not be calculated then there is no old contour that is still saved
            else:
                self.c = None
                self.cx = None
                self.cy = None
        else:
            self.c = None
            self.cx = None
            self.cy = None

    # displays the current masked frame
    def Display_Masked_Frame(self, frame): 
        # display the HSV masked frame if the current config allows
        if self.Should_Filtered_Frame_Be_Displayed() or self.isFilterBeingEdited:
            # this applys the mask on the current frame
            maskedframe = cv2.bitwise_and(frame, frame, mask=self.hsvMask)

            # Draw target centroid and the contour outline together if a contour exists
            if self.c is not None:
                cv2.circle(maskedframe, (self.cx, self.cy), 5, (255, 255, 255), -1)
                cv2.drawContours(maskedframe, [self.c], -1, (0, 255, 0), 1)

            cv2.imshow(self.Get_Filter_Frame_Name(), maskedframe)