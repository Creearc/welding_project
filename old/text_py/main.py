from pytesseract import Output
import pytesseract
import cv2
import sys
import rotator

def recognition(img):
  rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  rgb = cv2.resize(rgb, (W, H))
  
  results = pytesseract.image_to_data(rgb, output_type=Output.DICT, lang="rus")  

  for i in range(len(results["text"])):
    x = results["left"][i]
    y = results["top"][i]
    w = results["width"][i]
    h = results["height"][i]

    text = results["text"][i]
    conf = int(float(results["conf"][i]))

    if conf > 50:
      if False:
        print("Confidence: {}".format(conf))
        print("Text: {}".format(text))
        print("")
        return text

if __name__ == '__main__':
  try:
    r = rotator.Rotator()
    cap = cv2.VideoCapture(0)
    while True:
      ret, img = cap.read()
       if not ret:
         continue
      text = recognition(img,)
      r.rotate(30)
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
