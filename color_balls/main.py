import cv2
import numpy as np


def find_color_ball(color, color_to_show, color_map):
    mask = cv2.inRange(hsv, color_map[0], color_map[1])
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center  = None
    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if radius < 30:
            return np.zeros_like(frame), None
        M = cv2.moments(contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        cv2.circle(frame, (int(x), int(y)), int(radius), color_to_show[color], 2)

        cv2.circle(frame, center, 5, (0, 0, 255), -1)

    result = frame.copy()
    result[mask == 255] = colors_to_show[color]
    result[mask != 255] = (0, 0, 0)
    return result, center


capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_EXPOSURE, -1)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

cv2.namedWindow("Camera")
cv2.namedWindow("Debug")

colors = ["yellow", "green", "red", "blue"]

colors_map = {
    "yellow": [(20, 150, 150), (25, 220, 220)],
    "green": [(61, 100, 100), (70, 180, 170)],
    "red": [(1, 150, 150), (10, 210, 180)],
    "blue": [(89, 100, 100), (109, 255, 255)],
}

colors_to_show = {
    "yellow": (22, 180, 200),
    "green": (0, 255, 0),
    "red":  (0, 0, 255),
    "blue":  (255, 0, 0),
}


capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_EXPOSURE, -1)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

picked_colors = ["red", "blue", "yellow", "green"]
centers_map = {}

while capture.isOpened():
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)
    # cv2.putText(frame, color, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (11, 11), 0)


    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    results = []
    for color in picked_colors:
        mask, center = find_color_ball(color, colors_to_show, colors_map[color])
        centers_map[color] = center
        results += [mask]



    ok = True
    for center in centers_map.values():
        if center is None:
            ok = False
            break
    flag = False
    if ok:
        if centers_map[picked_colors[0]][0] < centers_map[picked_colors[2]][0] and \
            centers_map[picked_colors[1]][0] < centers_map[picked_colors[3]][0] and \
            centers_map[picked_colors[0]][1] < centers_map[picked_colors[1]][1] and \
            centers_map[picked_colors[2]][1] < centers_map[picked_colors[3]][1]:
                flag = True


    if (len(results) > 0):
        final_result = results[0]
        for result in results[1:]:
            final_result = cv2.addWeighted(final_result, 0.5, result, 0.5, 0)

    if flag:
        cv2.putText(frame, "Victory", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Debug", final_result)
    cv2.imshow("Camera", frame)


capture.release()
cv2.destroyAllWindows()
