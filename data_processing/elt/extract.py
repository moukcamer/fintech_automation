import csv

def extract_csv(file):
    return list(csv.DictReader(file.read().decode("utf-8").splitlines()))
