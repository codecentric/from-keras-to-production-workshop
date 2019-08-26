import cv2
import json

def preprocess_img():
    img = cv2.imread(input_img, cv2.IMREAD_COLOR)
    larger = cv2.resize(img, (100,100))
    gray = cv2.cvtColor(larger, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(preproc_img, gray)

def predict_img():
    img = cv2.imread(preproc_img, cv2.IMREAD_GRAYSCALE)
    circles = cv2.HoughCircles(
        img, cv2.HOUGH_GRADIENT, dp=2, minDist=15, param1=100, param2=70
    )
    label = "lemon" if circles is not None else "banana"
    with open(prediction, "w") as out:
        json.dump({"class": label}, out)

# TODO YOUR CODE COMES HERE