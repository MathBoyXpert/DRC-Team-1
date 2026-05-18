import cv2

# this is for changing the video input (0..*) with the number
VIDEO_INPUT = 0
# this is to indivcate the HSV space, to save on processing power utilise COLOR_BGR2HSV instead of COLOR_BGR2HSV_FULL
HSV_SPACE = cv2.COLOR_BGR2HSV_FULL

### NAMES OF OPEN CV WINDOWS ###

# Filter Names
OBSTACLE_HSV = "Obstacle HSV Filter"
TRACK_COMPLETION_HSV = "Track Completion HSV Filter"
TRACK_LINES_HSV = "Track Lines HSV Filter"
RIVAL_BOT_HSV = "Rival Bot HSV Filter"

# Names for the HSV Filter Track Bars
Trackbar_Names_Dict = {
    OBSTACLE_HSV: "Track Bar Window (Obstacle)",
    TRACK_COMPLETION_HSV: "Track Bar Window (Track Completion)",
    TRACK_LINES_HSV: "Track Bar Window (Track Lines)",
    RIVAL_BOT_HSV: "Track Bar Window (Rival Bot)"
}

# Names for the HSV Filter Masked Windows
Masked_Window_Names_Dict = {
    OBSTACLE_HSV: "Masked Obstacle Window",
    TRACK_COMPLETION_HSV: "Masked Track Completion Window",
    TRACK_LINES_HSV: "Masked Track Lines Window",
    RIVAL_BOT_HSV: "Masked Rival Bot Window"
}

# Names for the HSV Filter Files for storage for the filters
Hsv_Filter_File_Names_Dict = {
    OBSTACLE_HSV: "ObstacleHsvFilter.pkl",
    TRACK_COMPLETION_HSV: "TrackCompletionHsvFilter.pkl",
    TRACK_LINES_HSV: "TrackLinesHsvFilter.pkl",
    RIVAL_BOT_HSV: "RivalBotHsvFilter.pkl"
}

# Names for the HSV Filter Files for storage for the filters
Display_The_Frame = {
    OBSTACLE_HSV: False,
    TRACK_COMPLETION_HSV: False,
    TRACK_LINES_HSV: False,
    RIVAL_BOT_HSV: False
}
