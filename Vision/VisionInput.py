import config
import cv2
class VisionInput:
    _instance = None
    _video_capture = None
    

    # this new function ensures the instance of Vision that is created is a singleton instance
    # this works by accessing class level attributes through cls where "_instance" is defined this is now unattached from any spesific instance
    # and shared by all instances of this class, the _instance var is then checked to see if it exists 
    # if it does then just return that instance (the one containing the video capture obj)
    # if it doesnt then create that instance
    # as such to use this class as a singleton obj you must always initalise it and then use th ecorresponding methods
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VisionInput, cls).__new__(cls)
            # Initialize camera here to be a singleton
            import config
            import cv2
            print("Vision Object created - THIS SHOULD NEVER APPEAR TWICE IN DEBUGGING OUTPUTS")
            cls._video_capture = cv2.VideoCapture(config.VIDEO_INPUT)
        return cls._instance

    # allows someone calling this object to get the same vision object
    def Get_Vision(self):
        if not self._video_capture.isOpened():
            print("Error: Could not open video device")
            raise VisionError("The vision object is not opened")

        return self._video_capture
    
    # returns the most recently produced frame
    def Get_Frame(self):
        good, frame = self._video_capture.read()
        # checks for a bad video read
        if not good:
            print("Error: Can't receive frame. Exiting...")
            raise VisionError("The vision object could not produce a good frame")
        
        # returns the frame
        return frame

    
class VisionError(Exception):
    pass