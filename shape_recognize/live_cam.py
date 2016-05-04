import numpy as np
import cv2
import scipy.misc

#capturing frame from external camera
cap = cv2.VideoCapture(0)
#capturing frame from built-in camera
#cap = cv2.VideoCapture(1)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        normal = cv2.cvtColor(frame, cv2.COLORMAP_BONE)
        scipy.misc.imsave('outfile.jpg', normal)

    img = scipy.misc.imread('outfile.jpg')

    cv2.imshow('okno',img)
    cv2.waitKey(10)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()