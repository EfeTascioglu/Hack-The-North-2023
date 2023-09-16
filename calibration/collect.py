import cv2
import cv2 as cv

cap = cv.VideoCapture(2)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

counter = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', frame)  # gray)
    key = cv.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('a'):
        cv.imwrite(f"img{counter}.jpg", frame)
        counter += 1

# Size: 8x6, 0.021444

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
