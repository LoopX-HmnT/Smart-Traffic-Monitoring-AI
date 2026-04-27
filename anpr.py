import easyocr

class ANPR:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)

    def extract_text(self, frame, bbox):
        x1, y1, x2, y2 = bbox
        crop = frame[y1:y2, x1:x2]

        results = self.reader.readtext(crop)

        if not results:
            return ""

        return results[0][1]