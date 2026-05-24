from computerVisionPreProcessing import vision
from VisionInput import VisionInput
import time

# this simply initialise the vision input
# THIS DOES NOT NEED TO BE USED, instead vision input should be called statically with only one instance in a singleton approach
visionInput = VisionInput()
visionInput.Start_Vision_IO()
time.sleep(2)

preprocessing = vision()

preprocessing.mainLoop()

visionInput.End_Vision_IO()