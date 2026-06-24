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

            GRID_SIZE = (6,9)
            OUTPUT_SQUARE_SIZE = 100

            tl = [222, 387]
            bl = [70, 472]
            tr = [400, 380]
            br = [538, 472]

            cv2.circle(frame, tl, 5, (0,0, 255), -1)
            cv2.circle(frame, bl, 5, (0,0, 255), -1)
            cv2.circle(frame, tr, 5, (0,0, 255), -1)
            cv2.circle(frame, br, 5, (0,0, 255), -1)

            pts1 = np.array([tl, bl, tr, br], dtype=np.float32)
            pts2 = np.array([[0, 0], [0, config.HEIGHT], [config.WIDTH, 0], [config.WIDTH, config.HEIGHT]], dtype=np.float32)

            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            transformed_frame = cv2.warpPerspective(frame, matrix, (config.WIDTH, config.HEIGHT))
            # print(f'Frame type: {type(frame)}')
            # cv2.imshow("Transformed frame", transformed_frame)
            # time.sleep(3)
            # cv2.destroyAllWindows()
            
            self._curr_frame = transformed_frame;
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

    def perspective_Transform_slider():
        window_name = "Adjust corners"
        cv2.namedWindow(window_name)

        pass

class VisionError(Exception):
    pass