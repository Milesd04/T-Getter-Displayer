import csv

def load_stops(file_path):
    stops = {}
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stops[row['stop_id']] = row['stop_name']
    return stops
