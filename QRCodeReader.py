import cv2

def QR_read(image = "image.png"):
    """
    This function reads the QR code from the image and returns the decoded value, the points of the QR code and the status code.
    We assume there will only be one QR code in the image.
    
    :param image: The image from which the QR code is to be read.
    :return: The decoded value, the points of the QR code and the status code.
    """
        
    img = cv2.imread(image)
    detect = cv2.QRCodeDetector()
    val, pts, st_code = detect.detectAndDecode(img)

    # print(val, pts, st_code)
    return val, pts, st_code

if __name__ == "__main__":
    QR_read()