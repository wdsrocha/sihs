"""
import pyzbar.pyzbar as pyzbar
import numpy as np
# import cv2
import time
import requests
import json
from flask import jsonify

# get the webcam:
# cap = cv2.VideoCapture(0)

# cap.set(3, 352)
# cap.set(4, 288)
# 160.0 x 120.0
# 176.0 x 144.0
# 320.0 x 240.0
# 352.0 x 288.0
# 640.0 x 480.0
# 1024.0 x 768.0
# 1280.0 x 1024.0
time.sleep(2)
cnt = 0


def decode(im, to_request = False):
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)

    if to_request and len(decodedObjects):
        url_api = "http://127.0.0.1:5000/confirm"

        try:
            payload = dict(eval(decodedObjects[0].data.decode("utf-8")))
        except Exception as e:
            print(e)
            return decodedObjects

        r = requests.post(url=url_api, json=payload)
        print(r.json())

    return decodedObjects


# font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    frame_url = "http://192.168.100.118:8080/photo.jpg"
    response = requests.get(url, stream=True)
with open('img.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
    # Capture frame-by-frame
    # ret, frame = cap.read()
    # Our operations on the frame come here
    # im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    decodedObjects = decode(im, (cnt == 0))
     
    cnt = (cnt + 1) % 60


    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv2.convexHull(
                np.array([point for point in points], dtype=np.float32)
            )
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        # Number of points in the convex hull
        n = len(hull)
        # Draw the convext hull
        for j in range(0, n):
            cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        # print(x, y)

        # print(' iii Type : {}\n'.format(decodedObject.type))
        # print('iii Data : {}\n'.format(decodedObject.data))

        # ip = ''

        # url_api = ip+':5000/confirm'

        # payload = {'QR CODE': decodedObject.data}

        # requests.post(url=url_api, data=payload)

        barCode = str(decodedObject.data)
        cv2.putText(frame, barCode, (x, y), font, 1, (0, 255, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord("q"):
        break
    elif key & 0xFF == ord("s"):  # wait for 's' key to save
        cv2.imwrite("Capture.png", frame)

# When everything done, release the capture


"""
import pyzbar.pyzbar as pyzbar
import numpy as np
import shutil
import time
import requests
import json
from flask import jsonify
import cv2

ip = input("IP: ")
port = input("Port: ")

cnt = 0

def decode(im, to_request = False):
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)

    if to_request and len(decodedObjects):
        url_api = f"http://{ip}:{port}/confirm"

        try:
            payload = dict(eval(decodedObjects[0].data.decode("utf-8")))
        except Exception as e:
            print(e)
            return decodedObjects

        r = requests.post(url=url_api, json=payload)
        print(r.json())

    return decodedObjects


while True:
    frame_url = "http://100.65.225.189:8080/photo.jpg"
    response = requests.get(frame_url, stream=True).raw

    im = np.asarray(bytearray(response.read()), dtype="uint8")
    im = cv2.imdecode(im, cv2.IMREAD_COLOR)

    cv2.imshow('Image', im)
    cv2.waitKey(1)

    decoded_objects = decodedObjects = decode(im, (cnt == 0))
    print(decoded_objects)
     
    cnt = (cnt + 1) % 60


cv2.destroyAllWindows()

