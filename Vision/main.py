from computerVisionPreProcessing import vision
from VisionInput import VisionInput

# this simply initialise the vision input
# THIS DOES NOT NEED TO BE USED, instead vision input should be called statically with only one instance in a singleton approach
visionInput = VisionInput()

preprocessing = vision()

preprocessing.mainLoop()