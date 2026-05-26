import config
import cv2
import threading
import time
class VisionInput:
    _instance = None
    _video_capture = None
    _curr_frame = None
    _curr_hsv_frame = None
    _ingestion = True
    _frame_no = 0


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
    def Frame_Ingestion(self):
        print("Starting Frame Ingestion....")
        while self._ingestion:
            # target fps
            time.sleep(config.TARGET_FPS)
            good, frame = self._video_capture.read()
            # checks for a bad video read
            if not good:
                print("Error: Can't receive frame. Exiting...")
                raise VisionError("The vision object could not produce a good frame")

            # updates the frame
            self._curr_frame = frame;
            self._curr_hsv_frame = cv2.cvtColor(frame, config.HSV_SPACE)
            self._frame_no += 1

        print("Ending Frame Ingestion....")
        self._video_capture.release()

    # returns the most recently ingested frame
    def Get_Frame(self):
        return self._curr_frame, self._frame_no

    # returns the most recently ingested frame
    def Get_HSV_Frame(self):
        return self._curr_hsv_frame

    # starts the vision ingestion thread
    def Start_Vision_IO(self): 
        self._ingestion = True
        visionIOTHread = threading.Thread(target=self.Frame_Ingestion)
        visionIOTHread.start()

    # Should end the Vision Ingestion Thread
    def End_Vision_IO(self): 
        self._ingestion = False

class VisionError(Exception):
    pass