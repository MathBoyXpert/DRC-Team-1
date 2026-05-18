from abc import ABC, abstractmethod
import cv2
import pickle
import os
import config
from VisionInput import VisionInput

class HSVFilterInterface(ABC):

    # this makes it so the masked hsv frame is displayed reguardless of config settings
    isFilterBeingEdited = False

    def __init__(self):
        self.Retrieve_HSV_Filter() # initialises the hsv filter

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
            self.Display_Masked_Frame()
            
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
            cv2.createTrackbar(hsvAttribute, self.Get_Filter_GUI_Name(), 0, 255, doNothing)
            # Setting initial trackbar positions based on past filters
            cv2.setTrackbarPos(hsvAttribute, self.Get_Filter_GUI_Name(), self.hsvValueMap[hsvAttribute])
            
        

    # this gets the current details of the filter form the GUI and returns it as a HSVFilter Obj
    def Update_HSV_Filter_From_GUI(self):
        # getting the trackbar values for the HSV filtering
        for hsvAttribute in self.hsvList:
            self.hsvValueMap[hsvAttribute] = cv2.getTrackbarPos(hsvAttribute, self.Get_Filter_GUI_Name())
            
    # displays the current masked frame
    def Display_Masked_Frame(self):
        # gets the latest frame
        frame = VisionInput().Get_Frame()

        # converts the current frame into HSV and then creates a mask for the HSV values
        hsvFrame = cv2.cvtColor(frame, config.HSV_SPACE)
        hsvMask = cv2.inRange(hsvFrame, self.Get_Min_Vals_Arr(), self.Get_Max_Vals_Arr())

        # this applys the mask on the current frame and saves the masked frame
        maskedframe = cv2.bitwise_and(frame, frame, mask=hsvMask)
        
        # display the HSV masked frame if the current config allows
        if self.Should_Filtered_Frame_Be_Displayed() or self.isFilterBeingEdited:
            cv2.imshow(self.Get_Filter_Frame_Name(), maskedframe)