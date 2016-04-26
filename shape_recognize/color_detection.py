import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of colors
    # blue
    lower_blue = np.array([92,0,0])
    upper_blue = np.array([124,256,256])
    # red
    lower_red = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
    upper_red = cv2.inRange(hsv, np.array([160, 100, 100]), np.array([179, 255, 255]))
    # black
    black = cv2.inRange(hsv, np.array([0,0,0]), np.array([180,255,30]))
    # fiolet
    lower_violet = np.array([153,0,78])
    upper_violet = np.array([255,204,229])
    # green
    # lower_green = np.array([34,139,34])
    # upper_green = np.array([152,251,230])
    lower_green = np.array([40,70,70])
    upper_green = np.array([80,200,200])
    # masks
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # mask = black
    mask = cv2.inRange(hsv, lower_green, upper_green )
    # mask = cv2.addWeighted(lower_red,1.0,upper_red,1.0,0.0)
    # mask = cv2.inRange(hsv,lower_violet, upper_violet)
    # zakres brany z http://www.rapidtables.com/web/color/RGB_Color.html
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()