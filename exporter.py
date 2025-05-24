import csv
import json

def export_data(data, filename, mode):
    if mode == "csv":
        if isinstance(data, list) and all(isinstance(d, dict) for d in data):
            keys = set(k for d in data for k in d.keys())
            with open(filename, "w", newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(keys))
                writer.writeheader()
                writer.writerows(data)
            print(f"Data exported to {filename}")
        else:
            print("Data format not suitable for CSV export.")
    elif mode == "json":
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Data exported to {filename}")
    else:
        print("Unsupported export format. Use 'csv' or 'json'.")