import cv2
import numpy as np
import os

def hide_data(video_path, data_bytes):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()

    if not ret:
        raise Exception("Can't read video frame.")

    binary_data = ''.join(format(byte, '08b') for byte in data_bytes)
    binary_data += '1111111111111110'
    data_index = 0

    for row in frame:
        for pixel in row:
            for n in range(3):  # BGR
                if data_index < len(binary_data):
                    pixel[n] = (pixel[n] & ~1) | int(binary_data[data_index])
                    data_index += 1

    out_path = os.path.join("output", os.path.basename(video_path))
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'XVID'), 24, (frame.shape[1], frame.shape[0]))
    out.write(frame)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    return out_path

def extract_data(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise Exception("Can't read frame.")

    binary_data = ""
    for row in frame:
        for pixel in row:
            for n in range(3):
                binary_data += str(pixel[n] & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    extracted = bytearray()

    for byte in all_bytes:
        if byte == '11111110':
            break
        extracted.append(int(byte, 2))

    return bytes(extracted)
