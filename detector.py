from ultralytics import YOLO

class Detector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")  # stable working model

    def detect(self, frame):
        results = self.model(frame)[0]
        detections = []

        if results.boxes is None:
            return detections

        boxes = results.boxes.xyxy.cpu().numpy()
        classes = results.boxes.cls.cpu().numpy()

        for box, cls in zip(boxes, classes):
            x1, y1, x2, y2 = map(int, box)
            label = self.model.names[int(cls)]

            detections.append({
                "bbox": (x1, y1, x2, y2),
                "label": label
            })

        return detections