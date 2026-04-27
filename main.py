import cv2
import os
import time
import winsound
from detector import Detector
from anpr import ANPR
from logger import Logger
from tracker import SimpleTracker

# 📍 Location
LAT = 30.3398
LON = 76.3869

detector = Detector()
anpr = ANPR()
logger = Logger()
tracker = SimpleTracker()

os.makedirs("outputs/images", exist_ok=True)

cap = cv2.VideoCapture(0)

last_log_time = {}
last_alert_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detector.detect(frame)

    tracked_objects = tracker.update(detections)

    for obj in tracked_objects:
        x1, y1, x2, y2 = obj["bbox"]
        label = obj["label"]
        track_id = obj["id"]

        color = (0, 255, 0)

        if label == "person":
            color = (0, 0, 255)

            current_time = time.time()

            # 🔊 Alert
            if current_time - last_alert_time > 2:
                winsound.PlaySound("fahhhhh.wav", winsound.SND_ASYNC)
                last_alert_time = current_time

            # 🧾 Log once per ID
            if track_id not in last_log_time or (current_time - last_log_time[track_id] > 1):

                # 📸 Cropped image
                crop = frame[y1:y2, x1:x2]

                cv2.putText(crop, "NO HELMET", (5, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

                filename = f"outputs/images/violation_{track_id}.jpg"
                cv2.imwrite(filename, crop)

                logger.log("No Helmet", track_id, filename, LAT, LON)

                last_log_time[track_id] = current_time

            cv2.putText(frame, "NO HELMET",
                        (x1, y1 - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        cv2.putText(frame, f"ID:{track_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("SMART TRAFFIC SYSTEM", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()