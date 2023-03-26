import numpy as np
import matplotlib.pyplot as plt
import cv2
# Read the image in BGR

carplate_img = cv2.imread('t20.jpg')

# Convert the image to RGB
carplate_img_rgb = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2RGB)

carplate_haar_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')


def carplate_detect(image):
    carplate_overlay = image.copy() 
    carplate_rects = carplate_haar_cascade.detectMultiScale(carplate_overlay,scaleFactor=1.1, minNeighbors=3)


    for x,y,w,h in carplate_rects: 
        # save image at location
        ROI = carplate_overlay[y:y+h, x:x+w]
        cv2.imwrite("static/img/extracted/x.png", ROI)
        cv2.rectangle(carplate_overlay, (x,y), (x+w,y+h), (255,255,0), 5) 
        
    return carplate_overlay

detected_carplate_img = carplate_detect(carplate_img_rgb)
# finalImg= cv2.cvtColor(detected_carplate_img, cv2.COLOR_BGR2RGB)
# cv2.imshow("testIt", finalImg)
# cv2.waitKey(0)



# gray_img = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2GRAY)

# # Convert the grayscale image to black and white
# bw_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)[1]

# # Display the original and converted images
# cv2.imshow('Original Image', carplate_img)
# cv2.imshow('Black and White Image', bw_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()