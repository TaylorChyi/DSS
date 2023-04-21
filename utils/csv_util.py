import csv
import os
from common.config import *

def save_to_csv(age, pregnant, allergy, weight, prescription):
        file_exists = os.path.isfile(PRESCRIPTIONS_RECORD_CSV)

        with open(PRESCRIPTIONS_RECORD_CSV, "a", newline="") as csvfile:
            fieldnames = ["age", "pregnant", "allergy", "weight", "prescription"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "age": age,
                "pregnant": pregnant,
                "allergy": allergy,
                "weight": weight,
                "prescription": prescription
            })
            
def read_csv_records():
    with open(PRESCRIPTIONS_RECORD_CSV, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            print(",\t".join(row))