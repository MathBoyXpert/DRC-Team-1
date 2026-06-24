import cv2
import numpy as np

# Number of inner intersections for length & width
GRID_SIZE = (6,9)
# Size of each chessboard square from birds-eye view in pixels
OUTPUT_SQUARE_SIZE = 100
STARTING_POINT = np.float32([1000,1000])
BOARD_FILE_PATH = "chessboard.jpg"

chessboardCaptured = False

cap = cv2.VideoCapture(0)

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

if chessboardCaptured:
    chessboardImg = cv2.imread(BOARD_FILE_PATH)
    if chessboardImg is None:
        raise FileNotFoundError(f"Could not load image from {BOARD_FILE_PATH}")
    ret, corners = cv2.findChessboardCorners(chessboardImg, GRID_SIZE, None)
    if ret:
        annotatedImg = cv2.drawChessboardCorners(chessboardImg, GRID_SIZE, corners, ret)
        cv2.imshow("Corners found", annotatedImg)
        corner = corners.reshape(-1, 2)
        tl = corners[0]
        tr = corners[GRID_SIZE[0] - 1]
        bl = corners[-GRID_SIZE[0]]
        br = corners[-1]
        src_pts = np.float32([tl, tr, br, bl])

        tl1 = STARTING_POINT
        tr1 = STARTING_POINT + np.float32([0, GRID_SIZE[0]*OUTPUT_SQUARE_SIZE])
        br1 = STARTING_POINT + np.float32([GRID_SIZE[1]*OUTPUT_SQUARE_SIZE, GRID_SIZE[0]*OUTPUT_SQUARE_SIZE])
        bl1 = STARTING_POINT + np.float32([GRID_SIZE[1]*OUTPUT_SQUARE_SIZE, 0])

        dst_pts = np.float32([br1, bl1, tl1, tr1])
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        cornerPts = np.float32([[0,0], [1920, 0], [1920, 1080], [0, 1080]])
        cornerPtsReshaped = np.reshape(cornerPts, (-1, 1, 2))
        dstCornerPts = cv2.perspectiveTransform(cornerPtsReshaped, M)
        dstCornerPts = dstCornerPts.reshape(-1, 2)
        dstCornerX = dstCornerPts[:,0]
        dstCornerY = dstCornerPts[:,1]
        boundingBox = (int(max(dstCornerX) - min(dstCornerX)), int(max(dstCornerY) - min(dstCornerY)))
    while True:
        r, frame = cap.read()
        if r:
            print(boundingBox)
            warpedImg = cv2.warpPerspective(frame, M, boundingBox)
            # warpedImg = cv2.rotate(warpedImg, cv2.ROTATE_90_CLOCKWISE)
            cv2.imshow("Perspective Warp", cv2.resize(warpedImg, None, fx=0.25, fy=0.25))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break



cv2.destroyAllWindows()
