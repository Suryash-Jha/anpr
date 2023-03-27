from django.shortcuts import render
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import time

# Create your views here.


def appendToTxt(currTime):
    f = open("static/txt/checked.txt", "a")
    f.write(str(currTime)+'\n')
    f.close()


def extractAndSaveNumberPlate(currTime):
    # Read the image in BGR
    fileName = f'static/img/recvd/recvd_{currTime}.jpg'
    carplate_img = cv2.imread(filename=fileName)

    # Convert the image to RGB
    carplate_img_rgb = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2RGB)

    carplate_haar_cascade = cv2.CascadeClassifier(
        'haarcascade_russian_plate_number.xml')

    def carplate_detect(image):
        carplate_overlay = image.copy()
        # image resizing
        resize_test_NP = cv2.resize(
            carplate_overlay, None, fx=2, fy=2,
            interpolation=cv2.INTER_CUBIC)

        # converting image to grayscale
        grayscale_resize_test_NP = cv2.cvtColor(
            resize_test_NP, cv2.COLOR_BGR2GRAY)

        # denoising the image
        gaussian_blur_NP = cv2.GaussianBlur(
            grayscale_resize_test_NP, (5, 5), 0)

        fileNameX = f'static/img/clear/clear_{currTime}.jpg'
        cv2.imwrite(fileNameX, gaussian_blur_NP)

        # cv2.imshow("testIt", gaussian_blur_NP)
        # cv2.waitKey(0)

        # temproary fix
        # carplate_rects = carplate_haar_cascade.detectMultiScale(
        # gaussian_blur_NP, scaleFactor=1.01, minNeighbors=5)

        carplate_rects = carplate_haar_cascade.detectMultiScale(
            carplate_overlay, scaleFactor=1.1, minNeighbors=3)
        # print(carplate_rects)
        for x, y, w, h in carplate_rects:
            # save image at location
            print(x, y, w, h)
            ROI = carplate_overlay[y:y+h, x:x+w]
            fileName = f'static/img/extracted/extracted_{currTime}.png'
            cv2.imwrite(fileName, ROI)
            # cv2.rectangle(carplate_overlay, (x, y),
            #   (x+w, y+h), (255, 255, 0), 5)
            appendToTxt(currTime)

        return carplate_overlay
    detected_carplate_img = carplate_detect(carplate_img_rgb)


def home(request):
    try:

        # get epoch time in milliseconds
        currTime = int(round(time.time() * 1000))
        # print(currTime)
        print(request.POST)
        if request.method == "POST":
            # print(request.FILES)
            data = request.FILES['mainImg']
            fileName = f'static/img/recvd/recvd_{currTime}.jpg'
            with open(fileName, 'wb') as f:
                image = Image.open(data)
                image.save(f, format='JPEG')

        # to repair django
        # extractAndSaveNumberPlate(1679927492294)
        print(currTime)
        extractAndSaveNumberPlate(currTime)
        return render(request, "plateDetection/indexr.html")
    except Exception as e:
        print(e)
        return render(request, "plateDetection/indexr.html")


def tempResult(request):
    # fileName = f'static/img/extracted/extracted_{currTime}.png'
    return render(request, "plateDetection/ocrNow.html")
