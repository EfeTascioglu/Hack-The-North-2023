import cv2
img = cv2.imread("Image.jpg")
detect = cv2.QRCodeDetector()
val, pts, st_code = detect.detectAndDecode(img)

print(val, pts, st_code)