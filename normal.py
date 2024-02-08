import cv2
cap = cv2.VideoCapture(0)
cap.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
# cap.set(3, 480)
# cap.set(4, 640)
while(True):
    _,image = cap.read()
    cv2.imshow("a",image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # change in git
