import cv2

# this is for changing the video input (0..*) with the number
VIDEO_INPUT = 0

# this determines the arrow detection method
CNN_METHOD = "CNN"
TEMPLATE_MATCHING_METHOD = "Template Matching"
ARROW_DETECTION_METHOD = CNN_METHOD

# this tells the program if everything should that is procesed (e.g contours etc) should be displayed tgt
# this is editable at runtime by pressing 'D'
DISPLAY_PROCCESSED_OUTPUT = True
TARGET_FPS = 1/100
# run the cnn every nth frame based on the CNN_INFERENCE variable value
CNN_INFERENCE = 3

### PRE-PROCESSING VARIABLES ##
# this dictates the various intensities of the preproccessing, can be: (5,5) or (7,7)
GAUSSIAN_BLUR_STRENGTH = (5,5)
# this determines how big the gaps that a morphological operation will fill in, can be: (5,5) or (3,3)
MORPHOLOGICAL_OPERATIONS_KERNEL_SIZE = (5, 5)
# this dictates the size of a resized frame
WIDTH = 640
HEIGHT = 480

# this is to indivcate the HSV space, to save on processing power utilise COLOR_BGR2HSV instead of COLOR_BGR2HSV_FULL
HSV_SPACE = cv2.COLOR_BGR2HSV_FULL
# if the hsv space is COLOR_BGR2HSV_FULL the value of the constant must be 255 | if COLOR_BGR2HSV -> value = 179
HSV_MAX_VAL = 255

### TEMPLATE MATCHING VARIABLES ###
TEMPLATE_SIZE = (171, 240)
RIGHT_TEMPLATE_PATH = "Vision/ArrowData/BaseArrows/Right.png"
LEFT_TEMPLATE_PATH = "Vision/ArrowData/BaseArrows/Left.png"

### AI CNN VARIABLES ###
# Name of the Arrow CNN
ARROW_CNN_PATH = "ArrowCNN.keras"
# this is the confidence threshold for the ai to determine an arrow direction
CONFIDENCE_THRESHOLD = 0.8
# this is the input shape of the AI
INPUT_SHAPE = (64, 64, 1)
# data for the ai to train and refer to
BASE_ARROWS_DIR = "Vision/ArrowData/BaseArrows"
CAPTURED_IMAGES_DIR = "Vision/ArrowData/CapturedImages"
TRAINING_DATA_IMAGES_DIR = "Vision/ArrowData/TrainingData"


### NAMES OF OPEN CV WINDOWS ###
# Filter Names
OBSTACLE_HSV = "Obstacle HSV Filter"
TRACK_COMPLETION_HSV = "Track Completion HSV Filter"
YELLOW_TRACK_LINES_HSV = "Yellow Track Lines HSV Filter (Left)"
BLUE_TRACK_LINES_HSV = "Blue Track Lines HSV Filter"
RIVAL_BOT_HSV = "Rival Bot HSV Filter"
ARROW_HSV = "Arrow HSV Filter"

# Names for the HSV Filter Track Bars
Trackbar_Names_Dict = {
    OBSTACLE_HSV: "Track Bar Window (Obstacle)",
    TRACK_COMPLETION_HSV: "Track Bar Window (Track Completion)",
    YELLOW_TRACK_LINES_HSV: "Yellow Track Lines Track Bar Window (Left)",
    BLUE_TRACK_LINES_HSV: "Blue Track Lines Track Bar Window (Left)",
    RIVAL_BOT_HSV: "Track Bar Window (Rival Bot)",
    ARROW_HSV: "Track Bar Window (Arrow)"
}

# Names for the HSV Filter Masked Windows
Masked_Window_Names_Dict = {
    OBSTACLE_HSV: "Masked Obstacle Window",
    TRACK_COMPLETION_HSV: "Masked Track Completion Window",
    YELLOW_TRACK_LINES_HSV: "Masked Yellow Track Lines Window",
    BLUE_TRACK_LINES_HSV: "Masked Blue Track Lines Window",
    RIVAL_BOT_HSV: "Masked Rival Bot Window",
    ARROW_HSV: "Masked Arrow Window"
}

# Names for the HSV Filter Files for storage for the filters
Hsv_Filter_File_Names_Dict = {
    OBSTACLE_HSV: "HSVStorage/ObstacleHsvFilter.pkl",
    TRACK_COMPLETION_HSV: "HSVStorage/TrackCompletionHsvFilter.pkl",
    YELLOW_TRACK_LINES_HSV: "HSVStorage/YellowTrackLinesHsvFilter.pkl",
    BLUE_TRACK_LINES_HSV: "HSVStorage/BlueTrackLinesHsvFilter.pkl",
    RIVAL_BOT_HSV: "HSVStorage/RivalBotHsvFilter.pkl",
    ARROW_HSV: "HSVStorage/ArrowHsvFilter.pkl"
}

# Names for the HSV Filter Files for storage for the filters
Display_The_Frame = {
    OBSTACLE_HSV: True,
    TRACK_COMPLETION_HSV: True,
    BLUE_TRACK_LINES_HSV: True,
    YELLOW_TRACK_LINES_HSV: True,
    RIVAL_BOT_HSV: True,
    ARROW_HSV: True
}

# Names for the HSV Filter Files for storage for the filters
Display_Bounding_Box = {
    OBSTACLE_HSV: True,
    TRACK_COMPLETION_HSV: True,
    BLUE_TRACK_LINES_HSV: False,
    YELLOW_TRACK_LINES_HSV: False,
    RIVAL_BOT_HSV: True,
    ARROW_HSV: True
}

Minimum_Contour_Size = {
    OBSTACLE_HSV: 500,
    TRACK_COMPLETION_HSV: 500,
    BLUE_TRACK_LINES_HSV: 500,
    YELLOW_TRACK_LINES_HSV: 500,
    RIVAL_BOT_HSV: 500,
    ARROW_HSV: 500
}
