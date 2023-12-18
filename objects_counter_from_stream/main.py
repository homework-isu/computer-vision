import numpy as np
import zmq
import cv2


def get_diagonal(box):
    return np.sqrt((box[0][0] - box[2][0]) ** 2 + (box[0][1] - box[2][1]) ** 2)


def analyze_image(frame):
    circles = 0
    rects = 0
    frame_t = frame

    lab = cv2.cvtColor(frame_t, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    blured = cv2.medianBlur(b, 15)
    canny = cv2.Canny(blured, 30, 10)
    dilated = cv2.dilate(canny, None, iterations=1)

    contours_frame, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours_frame:
        if cv2.contourArea(contour) > 50:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.intp(box)

            (x, y), rad = cv2.minEnclosingCircle(contour)
            center = int(x), int(y)
            rad = int(rad)
            area_rect = cv2.contourArea(box)
            area_circle = 3.14 * rad * rad
            if area_circle < area_rect:
                cv2.circle(frame, center, rad, (0, 0, 255), 2)
                circles += 1
            else:
                rects += 1
                cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

    cv2.putText(frame, f"circles: {circles}, rects: {rects}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Main', dilated)
    cv2.imshow('Debug', frame)
    return circles, rects


def process_zmq(addr):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.connect(addr)

    while True:
        buffer = socket.recv()
        arr = np.frombuffer(buffer, np.uint8)
        frame = cv2.imdecode(arr, -1)
        analyze_image(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def process_img(path):
    img = cv2.imread(path)
    c, r = analyze_image(img)
    print(f"Circles count:\t{c}")
    print(f"Rects count:\t{r}")
    cv2.waitKey(0)


if __name__ == "__main__":
    cv2.namedWindow('Main')
    cv2.namedWindow('Debug')

    img_path = "imgs/img.jpg"
    zmq_addr = "tcp://192.168.0.105:6556"
    is_zmq = False

    if is_zmq:
        process_zmq(zmq_addr)
    else:
        process_img(img_path)
        