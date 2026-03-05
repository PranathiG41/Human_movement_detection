import cv2
import time

def motionDetection():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not accessible")
        return

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    last_detect_time = 0
    DISPLAY_TIME = 1 # seconds
    frame_count = 0

    ret, frame = cap.read()

    while ret:
        frame_count += 1
        human_found = False

        #  Run HOG only every 5 frames (FAST)
        if frame_count % 5 == 0:
            try:
                humans, _ = hog.detectMultiScale(
                    frame,
                    winStride=(4, 4),      # more sensitive
                    padding=(16, 16),      # captures head/neck
                    scale=1.05             # detects small movements
                )

                if len(humans) > 0:
                    human_found = True
                    last_detect_time = time.time()

                    for (x, y, w, h) in humans:
                        cv2.rectangle(
                            frame, (x, y), (x+w, y+h), (0, 255, 0), 2
                        )

            except cv2.error:
                pass

        # 🕒 Keep message for 2 seconds
        if time.time() - last_detect_time <= DISPLAY_TIME:
            cv2.putText(
                frame,
                "STATUS: HUMAN MOVEMENT DETECTED",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        cv2.imshow("Human Movement Detection", frame)

        ret, frame = cap.read()

        if cv2.waitKey(25) == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    motionDetection()
