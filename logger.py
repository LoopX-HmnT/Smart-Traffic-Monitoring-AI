import csv
import os
from datetime import datetime

class Logger:
    def __init__(self):
        os.makedirs("outputs", exist_ok=True)
        self.file = "outputs/logs.csv"

        # create file with header if not exists
        if not os.path.exists(self.file):
            with open(self.file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Time", "Violation", "TrackID", "Plate", "Lat", "Lon"])

    def log(self, violation, track_id, plate="", lat=0.0, lon=0.0):
        with open(self.file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                violation,
                track_id,
                plate,
                lat,
                lon
            ])