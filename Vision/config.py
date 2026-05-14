import cv2

# this is for changing the video input (0..*) with the number
VIDEO_INPUT = 0
# this is to indivcate the HSV space, to save on processing power utilise COLOR_BGR2HSV instead of COLOR_BGR2HSV_FULL
HSV_SPACE = cv2.COLOR_BGR2HSV_FULL

### NAMES OF OPEN CV WINDOWS ###
TRACKBAR_WINDOW_TRACK_LINES = "Track Bar Window"
MASKED_FRAME_TRACK_LINES = "Masked Track Lines Window"
TRACK_LINES_HSV_FILTER_FILE = "TrackLinesHsvFilter.pkl"
