import math

class SimpleTracker:
    def __init__(self):
        self.next_id = 0
        self.objects = {}  # id → center

    def get_center(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1+x2)//2, (y1+y2)//2)

    def distance(self, p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def update(self, detections):
        tracked = []

        for d in detections:
            center = self.get_center(d["bbox"])

            matched_id = None

            for obj_id, prev_center in self.objects.items():
                if self.distance(center, prev_center) < 50:
                    matched_id = obj_id
                    break

            if matched_id is None:
                matched_id = self.next_id
                self.next_id += 1

            self.objects[matched_id] = center

            tracked.append({
                "id": matched_id,
                "bbox": d["bbox"],
                "label": d["label"]
            })

        return tracked