import numpy as np
import cv2
from matplotlib import pyplot as plt

# capturing frame from external camera
cap = cv2.VideoCapture(0)
# capturing frame from built-in camera
# cap = cv2.VideoCapture(1)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # frame = cv2.cvtColor(frame, cv2.COLORMAP_AUTUMN)
    frame = cv2.Canny(frame, 280, 350)
    normal = cv2.cvtColor(frame, cv2.COLOR_BAYER_GB2BGR)
    # laplacian = cv2.Laplacian(frame,cv2.CV_64F)

    # Display the resulting frame
    #cv2.imshow('frame',laplacian)
    #cv2.imshow('frame', normal)
    #cv2.imshow('frame')
    # zapis do pliku
    cv2.imwrite('img_CV2_90.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    frame = cv2.imread('img_CV2_90.jpg')
    cv2.imshow('frame', normal)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
