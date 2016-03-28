import numpy as np
import cv2

#capturing frame from external camera
cap = cv2.VideoCapture(1)
#capturing frame from built-in camera
#cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    normal = cv2.cvtColor(frame, cv2.COLORMAP_BONE)

    # Display the resulting frame
    cv2.imshow('frame',normal)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()