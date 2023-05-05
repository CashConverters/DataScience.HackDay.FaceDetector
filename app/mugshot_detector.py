# SPDX-License-Identifier: MIT
import os
os.environ['ORT_LOGGING_LEVEL'] = 'ERROR'   

import cv2
import onnxruntime as ort
import argparse
import numpy as np
from app.dependencies.box_utils import predict

face_detector_onnx = "./app/version-RFB-320.onnx"

face_detector = ort.InferenceSession(face_detector_onnx)

# scale current rectangle to box
def scale(box):
    width = box[2] - box[0]
    height = box[3] - box[1]
    maximum = max(width, height)
    dx = int((maximum - width)/2)
    dy = int((maximum - height)/2)

    bboxes = [box[0] - dx, box[1] - dy, box[2] + dx, box[3] + dy]
    return bboxes


# get box size
def box_size(x1, y1, x2, y2):
    return (x2 - x1) * (y2 - y1)

# crop image
def cropImage(image, box):
    num = image[box[1]:box[3], box[0]:box[2]]
    return num

# face detection method
def faceDetector(orig_image, threshold = 0.7):
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (320, 240))
    image_mean = np.array([127, 127, 127])
    image = (image - image_mean) / 128
    image = np.transpose(image, [2, 0, 1])
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.float32)

    input_name = face_detector.get_inputs()[0].name
    confidences, boxes = face_detector.run(None, {input_name: image})
    boxes, labels, probs = predict(orig_image.shape[1], orig_image.shape[0], confidences, boxes, threshold)
    return boxes, labels, probs

def is_mugshot(image):
    resp = {}
    orig_image = cv2.imread(image)
    height, width, channels = orig_image.shape

    boxes, labels, probs = faceDetector(orig_image)

    if len(boxes) == 0 or len(boxes) > 1:
        resp["mugshot"] = False
    else:
        image_size = height * width
        for i in range(boxes.shape[0]):
            box = scale(boxes[i, :])
            size = box_size(box[0], box[1], box[2], box[3])
            scale_factor = size / image_size
            
            resp["scale_factor"] = scale_factor * 100

            if scale_factor * 100 < 10:
                resp["mugshot"] = False
            else:
                resp["mugshot"] = True

    return resp
