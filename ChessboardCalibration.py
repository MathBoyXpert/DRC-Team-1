import cv2
import numpy as np

# Number of inner intersections for (columns, rows)
GRID_SIZE = (6, 9)
# Size of each chessboard square from birds-eye view in pixels
OUTPUT_SQUARE_SIZE = 100
BOARD_FILE_PATH = "chessboard.jpg"

chessboardCaptured = False
cap = cv2.VideoCapture(0)

# 1. Capture the Setup Frame
while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame, exiting...")
        break
    cv2.imshow("Video Feed", frame)

    keyPressed = cv2.waitKey(1) & 0xFF
    if keyPressed == ord("q"):
        break
    elif keyPressed == ord("c"):
        print("Chessboard image has been saved")
        cv2.imwrite(BOARD_FILE_PATH, frame)
        chessboardCaptured = True
        break

# 2. Process Calibration and Matrix Generation
if chessboardCaptured:
    chessboardImg = cv2.imread(BOARD_FILE_PATH)
    if chessboardImg is None:
        raise FileNotFoundError(f"Could not load image from {BOARD_FILE_PATH}")
        
    ret, corners = cv2.findChessboardCorners(chessboardImg, GRID_SIZE, None)
    if ret:
        # Flatten corners to shape (-1, 2) to fix indexing issues
        corner = corners.reshape(-1, 2)
        
        # Correctly grab the four outer-most intersections of the grid
        tl = corner[0]
        tr = corner[GRID_SIZE[0] - 1]
        bl = corner[-GRID_SIZE[0]]
        br = corner[-1]
        src_pts = np.float32([tl, tr, br, bl])

        # Define destination points relative to (0,0) to keep the warp perfectly in bounds
        # Width scales with columns (GRID_SIZE[0]), Height scales with rows (GRID_SIZE[1])
        board_width = (GRID_SIZE[0] - 1) * OUTPUT_SQUARE_SIZE
        board_height = (GRID_SIZE[1] - 1) * OUTPUT_SQUARE_SIZE

        tl1 = np.float32([0, 0])
        tr1 = np.float32([board_width, 0])
        br1 = np.float32([board_width, board_height])
        bl1 = np.float32([0, board_height])
        dst_pts = np.float32([tl1, tr1, br1, bl1])

        # Generate transformation matrix
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        
        # Calculate exactly how big the output canvas needs to be
        img_h, img_w, _ = chessboardImg.shape
        cornerPts = np.float32([[0, 0], [img_w, 0], [img_w, img_h], [0, img_h]])
        cornerPtsReshaped = np.reshape(cornerPts, (-1, 1, 2))
        
        dstCornerPts = cv2.perspectiveTransform(cornerPtsReshaped, M).reshape(-1, 2)
        dstCornerX = dstCornerPts[:, 0]
        dstCornerY = dstCornerPts[:, 1]
        
        # Canvas bounding box dimension
        boundingBox = (int(max(dstCornerX) - min(dstCornerX)), int(max(dstCornerY) - min(dstCornerY)))

        # 3. Stream Live Warped Video Feed
        while True:
            r, frame = cap.read()
            if r:
                warpedImg = cv2.warpPerspective(frame, M, boundingBox)
                cv2.imshow("Perspective Warp", warpedImg)
                
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

cap.release()
cv2.destroyAllWindows()