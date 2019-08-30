import fire


def preprocess(inpath, outpath, x, y):
    import cv2
    img = cv2.imread(inpath, cv2.IMREAD_COLOR)
    larger = cv2.resize(img, (x, y))
    gray = cv2.cvtColor(larger, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(outpath, gray)

    
def classify(inpath, outpath):
    import cv2
    import json
    img = cv2.imread(inpath, cv2.IMREAD_GRAYSCALE)
    circles = cv2.HoughCircles(img, 
                               cv2.HOUGH_GRADIENT,
                               dp=2, 
                               minDist=15, 
                               param1=100, 
                               param2=70)
    label = "lemon" if circles is not None else "banana"
    with open(outpath, "w") as out:
        json.dump({"class": label}, out)
    

if __name__ == '__main__':
  fire.Fire()