import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


img = cv2.imread('szachownica_kolor.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # blue
lower_blue = np.array([92,0,0])
upper_blue = np.array([124,256,256])

mask = cv2.inRange(hsv, lower_blue, upper_blue)

output = np.array([[]])
ret = False
    # Find the chess board corners
ret, corners = cv2.findChessboardCorners(gray, (7,7), output)
    # If found, add object points, image points (after refining them)
if ret == True:
    # (image, corners, winSize, zeroZone, criteria)
    x_substract = corners[01,[0]] - corners[00,[0]]
    y_substract = corners[07,[0]] - corners[00,[0]]
    cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
    # Przesuniecie punktow na srodek pol
    corners = np.subtract(corners, x_substract/2)
    corners = np.subtract(corners, y_substract/2)

    imgpoints.append(corners)
        # Draw and display the corners
    res = cv2.bitwise_and(img,img, mask= mask)
    cv2.drawChessboardCorners(res, (7,7), corners, ret)
    cv2.imshow('img',res)
    cv2.waitKey(0)
cv2.destroyAllWindows()