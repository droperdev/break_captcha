import os
import cv2

path_origin = 'images/'
path_origin_destination = 'images_process/'
with os.scandir(path_origin) as ficheros:
    for fichero in ficheros:
        image = cv2.imread(path_origin+fichero.name)
        gray = cv2.cvtColor(image, cv2.IMREAD_GRAYSCALE)
        blur = cv2.GaussianBlur(gray, (13, 13), 0)
        thresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY)[1]
        gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(path_origin_destination+fichero.name, gray)
        print("[INFO] Imagen {} procesada correctamente".format(fichero.name))
