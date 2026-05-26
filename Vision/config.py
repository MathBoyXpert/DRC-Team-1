import cv2

# this is for changing the video input (0..*) with the number
VIDEO_INPUT = 0

TARGET_FPS = 1/100

# this is to indivcate the HSV space, to save on processing power utilise COLOR_BGR2HSV instead of COLOR_BGR2HSV_FULL
HSV_SPACE = cv2.COLOR_BGR2HSV_FULL
# if the hsv space is COLOR_BGR2HSV_FULL the value of the constant must be 255 | if COLOR_BGR2HSV -> value = 179
HSV_MAX_VAL = 255



### NAMES OF OPEN CV WINDOWS ###
# Filter Names
OBSTACLE_HSV = "Obstacle HSV Filter"
TRACK_COMPLETION_HSV = "Track Completion HSV Filter"
YELLOW_TRACK_LINES_HSV = "Yellow Track Lines HSV Filter (Left)"
BLUE_TRACK_LINES_HSV = "Blue Track Lines HSV Filter"
RIVAL_BOT_HSV = "Rival Bot HSV Filter"

# Names for the HSV Filter Track Bars
Trackbar_Names_Dict = {
    OBSTACLE_HSV: "Track Bar Window (Obstacle)",
    TRACK_COMPLETION_HSV: "Track Bar Window (Track Completion)",
    YELLOW_TRACK_LINES_HSV: "Yellow Track Lines Track Bar Window (Left)",
    BLUE_TRACK_LINES_HSV: "Blue Track Lines Track Bar Window (Left)",
    RIVAL_BOT_HSV: "Track Bar Window (Rival Bot)"
}

# Names for the HSV Filter Masked Windows
Masked_Window_Names_Dict = {
    OBSTACLE_HSV: "Masked Obstacle Window",
    TRACK_COMPLETION_HSV: "Masked Track Completion Window",
    YELLOW_TRACK_LINES_HSV: "Masked Yellow Track Lines Window",
    BLUE_TRACK_LINES_HSV: "Masked Blue Track Lines Window",
    RIVAL_BOT_HSV: "Masked Rival Bot Window"
}

# Names for the HSV Filter Files for storage for the filters
Hsv_Filter_File_Names_Dict = {
    OBSTACLE_HSV: "ObstacleHsvFilter.pkl",
    TRACK_COMPLETION_HSV: "TrackCompletionHsvFilter.pkl",
    YELLOW_TRACK_LINES_HSV: "YellowTrackLinesHsvFilter.pkl",
    BLUE_TRACK_LINES_HSV: "BlueTrackLinesHsvFilter.pkl",
    RIVAL_BOT_HSV: "RivalBotHsvFilter.pkl"
}

# Names for the HSV Filter Files for storage for the filters
Display_The_Frame = {
    OBSTACLE_HSV: True,
    TRACK_COMPLETION_HSV: True,
    BLUE_TRACK_LINES_HSV: True,
    YELLOW_TRACK_LINES_HSV: True,
    RIVAL_BOT_HSV: True
}
