import cv2


def get_thresh(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    return thresh


def is_similar_template(img, frame):
    img_thresh = get_thresh(img)
    frame_thresh = get_thresh(frame)

    val = cv2.matchTemplate(frame_thresh, img_thresh, cv2.TM_CCOEFF_NORMED)
    return val > 0.9



def process_video(video, image, save_same=False):
    image_in_video_count = 0
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

    while video.isOpened():
        flag, frame = video.read()
        current_frame = video.get(cv2.CAP_PROP_POS_FRAMES)

        if flag:
            frame = cv2.resize(frame, (image.shape[1], image.shape[0]))
            cv2.imshow('Video Frame', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if is_similar_template(image, frame):
                image_in_video_count += 1
                if save_same:
                    cv2.imwrite(f"files/same_frames/{image_in_video_count}.png", frame)
                if image_in_video_count % 10 == 0:
                    print("Image found", image_in_video_count)

        if current_frame >= total_frames:
            break
    return image_in_video_count


if __name__ == "__main__":
    img = cv2.imread('files/my_img.png')
    video = cv2.VideoCapture("files/output.avi")

    count = process_video(video, img)
    print(f"Number of images: {count}")