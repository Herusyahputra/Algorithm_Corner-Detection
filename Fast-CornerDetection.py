import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:

    _,frame = cap.read()
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray_frame, 100, 0.1, 20)

    if corners is not None:
        corner = np.int0(corners)
        for corner in corners:
            set = corner.ravel()
            x,y = set
            cv2.circle(frame, (x,y), 5, (0,0,255), -1)
    cv2.imshow("frame containing corners", frame)
    k = cv2.waitKey(1)
    if k ==27:
        break

cap.release()
cv2.destroyAllWindows()