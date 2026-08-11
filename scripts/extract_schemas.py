import os
import csv
import json

data_dir = r"E:\repo\lh_nautical_analise\data"
schemas = {}

for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                headers = next(reader)
                schemas[filename.replace('.csv', '')] = headers
            except StopIteration:
                schemas[filename.replace('.csv', '')] = []

print(json.dumps(schemas, indent=2))
