import numpy as np
import cv2
from sampler_class import Sampler
from state_representation.state_repr import Repr
from state_representation.math import Math
import copy
import time
import scipy.misc

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
    #img = cv2.imread(img)

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
        image = Repr.create_representation(str_state_table)
        image_cv = (np.array(image))[:, :, ::-1].copy()
        cv2.imshow('representation', image_cv)
        cv2.drawChessboardCorners(img, (8,8),result, ret)
        cv2.imshow('img',img)

        return str_state_table

def map_indexes(x, y):
    if(x == 0):
        if(y == 1):
            return 0
        if(y == 3):
            return 1
        if(y == 5):
            return 2
        if(y == 7):
            return 3
    if(x == 1):
        if(y == 0):
            return 4
        if(y == 2):
            return 5
        if(y == 4):
            return 6
        if(y == 6):
            return 7
    if(x == 2):
        if(y == 1):
            return 8
        if(y == 3):
            return 9
        if(y == 5):
            return 10
        if(y == 7):
            return 11
    if(x == 3):
        if(y == 0):
            return 12
        if(y == 2):
            return 13
        if(y == 4):
            return 14
        if(y == 6):
            return 15
    if(x == 4):
        if(y == 1):
            return 16
        if(y == 3):
            return 17
        if(y == 5):
            return 18
        if(y == 7):
            return 19
    if(x == 5):
        if(y == 0):
            return 20
        if(y == 2):
            return 21
        if(y == 4):
            return 22
        if(y == 6):
            return 23
    if(x == 6):
        if(y == 1):
            return 24
        if(y == 3):
            return 25
        if(y == 5):
            return 26
        if(y == 7):
            return 27
    if(x == 7):
        if(y == 0):
            return 28
        if(y == 2):
            return 29
        if(y == 4):
            return 30
        if(y == 6):
            return 31

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

    try:
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
                k = 0
            x = null_tile[0]
            y = null_tile[1]
            index_null = map_indexes(x,y)
            map_new[index_null][1] = 0
            print("zmieniam", map_new[active_tile[0] * 4 + null_tile[1]][0], 'z', map_new[active_tile[0] * 4 + null_tile[1]][1], 'na ',map_current[null_tile[0] * 4 + null_tile[1] + k][1])
            x = active_tile[0]
            y = active_tile[1]
            index_active = map_indexes(x,y)
            #map_new[index][1] = map_current
            map_new[index_active][1] = map_current[index_null][1]
            map_current = copy.deepcopy(map_new)
        elif len(difference) == 1:
            null_tile = difference[0]
            x = null_tile[0]
            y = null_tile[1]
            index_null = map_indexes(x,y)
            map_new[index_null][1] = 0
            map_current = copy.deepcopy(map_new)
        elif len(difference) == 0:
            return

    except Exception as e:
        print('Inaccesible state! Return to the last acceptable')
        return
                #ONLY if test in logic will prove that it was valid move
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
output = np.array([[]])
cap = cv2.VideoCapture(0)
# pierwszy odczyt z kamery
ret, img = cap.read()
# zapisanie pierwszego odczytu z kamery do obrazu
# ustawienie poczatkowe reprezentacji planszy
if ret:
    normal = cv2.cvtColor(img, cv2.COLORMAP_BONE)
    #scipy.misc.imsave('old.jpg', normal)
    #cv2.imwrite('old2.jpg', normal)
    map_curr = starting_map()
    map_new = starting_map()
    #path1 = scipy.misc.imread('old.jpg')
    path1 = cv2.imread('old2.jpg')
    path2 = cv2.imread('old2.jpg')

while(True):
    cv2.waitKey(4000)
    ret, img = cap.read()

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,7), output)
        # If found, add object points, image points (after refining them)
    if ret == True:

        time.sleep(0.5)
        normal = cv2.cvtColor(img, cv2.COLORMAP_BONE)
        #scipy.misc.imsave('new.jpg', normal)
        cv2.imwrite('new.jpg',normal)
        #path2 = scipy.misc.imread('new.jpg')
        path2 = cv2.imread('new.jpg')
        maps = check_move(path1, path2, map_curr, map_new)                              #Dziwne przypisanie bo nie zwojowalem wewnatrz funkcji zmiany zawartosci listy podanej jako parametr
        #path2 = scipy.misc.imread('new.jpg')
        if maps is not None:
            path1 = path2
            cv2.imwrite('new.jpg',normal)
            map_curr = maps[0]
            map_new = maps[1]
        print(map_curr)

        cv2.waitKey(delay=100)
cap.relase()
cv2.destroyAllWindows()