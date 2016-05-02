import numpy as np
import cv2
from sampler_class import Sampler
from state_representation.state_repr import Repr
from state_representation.math import Math
import time

# function needed to change 7x7 matrix to 8x8 and calculate missing points

def insert_value(ndarray, value_x, value_y):
    result = ndarray
    result.resize((64,2))
    acumulator = result[6]
    for x in range(1,(result.size/2)-7):
        if(x % 8 == 0):
            for y in range((result.size/2)-1,x-1,-1):
                result[y] = result[y-1]
            result[(x-1)] = result[(x-1)-1] + value_x
            x += 1
    for x in range(56,64):
        result[x] = result[x-8] + value_y
    return result

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


img = cv2.imread('../pictures/artificial_light/position4.jpg')

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
    # calculate lenght between two adjecent points
    x_substract = corners[01,[0]] - corners[00,[0]]
    y_substract = corners[07,[0]] - corners[00,[0]]

    result = np.copy(corners)
    result.resize((64,2))

    insert_value(result, x_substract, y_substract)
    result.resize((64,1,2))
    # cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
    # Przesuniecie punktow na srodek pol
    result = np.subtract(result, x_substract/2)
    result = np.subtract(result, y_substract/2)

    #************************************************** to change orientation if necessary
    result = Math.alter_chessboard_middles(img, result)
    #***************************************************

    imgpoints.append(result)
    # Draw and display the corners

    #****************************************************
    #M.Werda test
    #analyze points in lattice
    #create representation in RGB
    #RGB to BGR and PIL to cv
    img = cv2.multiply(img, np.array([1.1]))
    img = cv2.medianBlur(img, 7)
    table = Sampler.check_colors(img, result)
    image = Repr.create_representation(table)
    image_cv = (np.array(image))[:, :, ::-1].copy()
    cv2.imshow('representation', image_cv)
    cv2.imshow('contrast', img)
    #****************************************************

    res = cv2.bitwise_and(img,img, mask= mask)
    cv2.drawChessboardCorners(res, (8,8),result, ret)
    cv2.imshow('img',res)
    cv2.imshow('mask',mask)
    cv2.waitKey(0)
cv2.destroyAllWindows()


