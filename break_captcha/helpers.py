import imutils
import cv2
import requests


def resize_to_fit(image, width, height):
    (h, w) = image.shape[:2]
    if w > h:
        image = imutils.resize(image, width=width)
    else:
        image = imutils.resize(image, height=height)

    padW = int((width - image.shape[1]) / 2.0)
    padH = int((height - image.shape[0]) / 2.0)

    image = cv2.copyMakeBorder(image, padH, padH, padW, padW,
                               cv2.BORDER_REPLICATE)

    image = cv2.resize(image, (width, height))
    return image


def clear_image_to_replace(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(gray, (13, 13), 0)
    thresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(path, gray)


def save_image(content, path_save):
    file = open(path_save, "wb")
    file.write(content)
    file.close()