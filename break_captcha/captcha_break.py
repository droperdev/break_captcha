from break_captcha.helpers import resize_to_fit
from keras.models import load_model
from imutils import paths
import numpy as np
import imutils
import cv2
import pickle


MODEL_FILENAME = "./models/captcha_model.hdf5"
MODEL_LABELS_FILENAME = "./models/model_labels.dat"


with open(MODEL_LABELS_FILENAME, "rb") as f:
    lb = pickle.load(f)


def get_predict(path):
    model = load_model(MODEL_FILENAME)

    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = cv2.copyMakeBorder(image, 8, 8, 8, 8, cv2.BORDER_REPLICATE)

    thresh = cv2.threshold(
        image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    contours = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = contours[1] if imutils.is_cv3() else contours[0]

    letter_image_regions = []

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if w / h > 1.25:
            half_width = int(w / 2)
            
            letter_image_regions.append((x, y, half_width, h))
            letter_image_regions.append((x + half_width, y, half_width, h))
        else:
            letter_image_regions.append((x, y, w, h))

    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])

    predictions = []

    for letter_bounding_box in letter_image_regions:
        x, y, w, h = letter_bounding_box

        letter_image = image[y - 2:y + h + 2, x - 2:x + w + 2]

        letter_image = resize_to_fit(letter_image, 20, 20)

        letter_image = np.expand_dims(letter_image, axis=2)
        letter_image = np.expand_dims(letter_image, axis=0)

        prediction = model.predict(letter_image)

        letter = lb.inverse_transform(prediction)[0]
        predictions.append(letter)

    captcha_text = "".join(predictions)
    return captcha_text
