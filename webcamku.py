import cv2

cam = cv2.VideoCapture(0)

while True:
    
    retV, frame = cam. read()
    cv2.imshow('webcamku', frame)
    if cv2.waitKey()& 0XFF == ord ('c'):
        break

cv2.release()
cv2.destrouAllWindows()

