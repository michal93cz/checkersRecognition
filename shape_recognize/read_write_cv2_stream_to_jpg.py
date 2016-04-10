import numpy as np
import cv2
from matplotlib import pyplot as plt

# capturing frame from external camera
cap = cv2.VideoCapture(0)
# capturing frame from built-in camera
# cap = cv2.VideoCapture(1)

while (True):
    # Capture frame-by-frame
    frame = cap.read()

    normal = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # zapis do pliku
    cv2.imwrite('img_CV2_90.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    frame = cv2.imread('img_CV2_90.jpg')
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
