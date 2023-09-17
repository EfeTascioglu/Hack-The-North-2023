import cv2
from pyzbar.pyzbar import decode

def extract_qr_code_from_image(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Thresholding the image (binary inverse)
    _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

    # Using the adaptive threshold to handle varying lighting conditions
    img_adaptive = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
    
    # Try decoding from the original, binary, and adaptive images
    for processed_img in [img, img_bin, img_adaptive]:
        decoded = decode(processed_img)
        if decoded:
            return decoded[0].data.decode('utf-8')

    return None