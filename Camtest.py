import cv2

# Initialize the camera (0 is usually the default built-in/USB camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Camera feed active. Press 'q' to quit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly ret is True
    if not ret:
        print("Error: Can't receive frame. Exiting ...")
        break

    # Display the resulting frame in a window named 'Camera Test'
    cv2.imshow('Camera Test', frame)

    # Wait 1 ms for key press. If 'q' is pressed, break the loop
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture and close windows
cap.release()
cv2.destroyAllWindows()