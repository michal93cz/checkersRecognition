import numpy as np
import cv2
from sampler_class import Sampler
from state_representation.state_repr import Repr
from state_representation.math import Math
import copy
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

def first_state_matrix():
    matrix = []
    for i in range(1, 33):
        matrix.append([i, i])
    return matrix

def get_image_state(img):
    img = cv2.imread(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # blue
    lower_blue = np.array([92, 0, 0])
    upper_blue = np.array([124, 256, 256])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    output = np.array([[]])
    ret = False
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 7), output)
    # If found, add object points, image points (after refining them)
    if ret == True:
        # calculate lenght between two adjecent points
        x_substract = corners[01, [0]] - corners[00, [0]]
        y_substract = corners[07, [0]] - corners[00, [0]]

        result = np.copy(corners)
        result.resize((64, 2))

        insert_value(result, x_substract, y_substract)
        result.resize((64, 1, 2))
        # cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        # Przesuniecie punktow na srodek pol
        result = np.subtract(result, x_substract / 2)
        result = np.subtract(result, y_substract / 2)

        # **************************************************
        result = Math.alter_chessboard_middles(img, result)
        # ***************************************************

        imgpoints.append(result)
        img = cv2.multiply(img, np.array([1.1]))
        img = cv2.medianBlur(img, 7) #to change orientation if necessary
        str_state_table = Sampler.check_colors(img, result)
        return str_state_table

def check_move(path1, path2, map_current, map_new):
    state1 = get_image_state(path1)
    state2 = get_image_state(path2)

    difference = []
    null_tile = None
    active_tile = None
    for i in range(0, len(state1)):
        for j in range(0, len(state1[0])):
            if state1[i][j] != state2[i][j]:
                difference.append([i, j, state1[i][j], state2[i][j]])

    k = None
    if len(difference) > 2:                                                                                             #if difference is more than 2 then the change is not valid
        print("State change not possible, number of tiles that do not match: " + len(null_tile))
    elif len(difference) == 2:
        if difference[0][3] == 'white':
            null_tile = difference[0]
            active_tile = difference[1]
            k = -1
        else:
            null_tile = difference[1]
            active_tile = difference[0]
            k = 1

        map_new[null_tile[0] * 4 + null_tile[1]][1] = 0
        print("zmieniam", map_new[active_tile[0] * 4 + null_tile[1]][0], 'z', map_new[active_tile[0] * 4 + null_tile[1]][1], 'na ',map_current[null_tile[0] * 4 + null_tile[1] + k][1])
        map_new[active_tile[0] * 4 + null_tile[1]][1] = map_current[null_tile[0] * 4 + null_tile[1] + k][1]
        map_current = copy.deepcopy(map_new)            #ONLY if test in logic will prove that it was valid move
        return[map_current, map_new]

        # temp = map_current[null_tile[0] * 4 + null_tile[1] + 1][1]
        # map_new[active_tile[0] * 4 + active_tile[1] + 1] = temp
        # map_new[null_tile[0] * 4 + null_tile[1] + 1] =

        # get_nth_element_of_map(null_tile * 4 + null_tile[1] + 1, map_current)[1] = temp
        # get_nth_element_of_map(difference[1][0] * 4 + difference[1][1] + 1, map_current)[1] =

def starting_map():
    array = []
    for i in range(33, 45):
        array.append([i, i + 44])
    for i in range(45, 53):
        array.append([i, 0])
    for i in range(53, 65):
        array.append([i, i + 12])
    return array

def get_nth_element_of_map(i, array):
    return array[i + 32][1]


map_curr = []
map_new = []

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


Sampler.debug = 0
img = cv2.imread('../pictures/move_test/position8_1.jpg')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # blue
lower_blue = np.array([92,0,0])
upper_blue = np.array([124,256,256])
mask = cv2.inRange(hsv, lower_blue, upper_blue)

map_curr = starting_map()
map_new = starting_map()

path1 = '../pictures/move_test/position1.jpg'
path2 = '../pictures/move_test/position2.jpg'
print(map_curr)

maps = check_move(path1, path2, map_curr, map_new)                              #Dziwne przypisanie bo nie zwojowalem wewnatrz funkcji zmiany zawartosci listy podanej jako parametr
map_curr = maps[0]
map_new = maps[1]

print(map_curr)
path1 = '../pictures/move_test/position2.jpg'
path2 = '../pictures/move_test/position3.jpg'
maps = check_move(path1, path2, map_curr, map_new)                             
map_curr = maps[0]
map_new = maps[1]

print(map_curr)

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
    str_state_table = Sampler.check_colors(img, result)
    #print(Sampler.strarr_to_intarr(str_state_table))
    image = Repr.create_representation(str_state_table)
    image_cv = (np.array(image))[:, :, ::-1].copy()
    cv2.imshow('representation', image_cv)
    cv2.imshow('contrast', img)

    #print(str_state_table)
    #****************************************************

    res = cv2.bitwise_and(img,img, mask= mask)
    cv2.drawChessboardCorners(res, (8,8),result, ret)
    cv2.imshow('img',res)
    cv2.imshow('mask',mask)
    cv2.waitKey(0)
cv2.destroyAllWindows()


