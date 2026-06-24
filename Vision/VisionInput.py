import Utils.config as config
import cv2
import threading
import time
import numpy as np
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
            import Utils.config as config
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

            # Perspective Transform
            tl = [222, 387]
            bl = [70, 472]
            tr = [400, 380]
            br = [538, 472]
            # Assume these are the 4 corner points of the object you selected in your 1080p image
            # [Top-Left, Top-Right, Bottom-Right, Bottom-Left]
            src_pts = np.float32([tl, tr, br, bl])

            (tl, tr, br, bl) = src_pts

            # 1. Calculate the maximum width
            # Distance between Bottom-Right & Bottom-Left, and Top-Right & Top-Left
            width_bottom = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            width_top = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            max_width = max(int(width_bottom), int(width_top))

            # 2. Calculate the maximum height
            # Distance between Top-Right & Bottom-Right, and Top-Left & Bottom-Left
            height_right = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            height_left = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            max_height = max(int(height_right), int(height_left))

            # 3. Use these maximums for your destination points
            dst_pts = np.float32([
                [0, 0],
                [max_width - 1, 0],
                [max_width - 1, max_height - 1],
                [0, max_height - 1]
            ])

            # 4. Pass them directly to the warp function
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped_image = cv2.warpPerspective(frame, M, (max_width, max_height))
            
            self._curr_frame = warped_image;
            self._frame_no += 1

        print("Ending Frame Ingestion....")
        self._video_capture.release()

    # returns the most recently ingested frames
    def Get_Frame(self):
        return self._curr_frame, self._frame_no

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