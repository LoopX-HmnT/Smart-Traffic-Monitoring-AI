class ViolationDetector:
    def check(self, label):
        if label == "person":
            return "No Helmet"
        return None