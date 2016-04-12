import numpy as np
import cv2
from matplotlib import pyplot as plt


#capturing frame from external camera
cap = cv2.VideoCapture(0)
#capturing frame from built-in camera
#cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    normal = cv2.cvtColor(frame, cv2.COLORMAP_BONE)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('frame',normal)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()