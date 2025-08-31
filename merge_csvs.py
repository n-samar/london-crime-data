import os
import csv

def merge_csv_files(root_dir, output_file):
    csv_files = []
    # Walk through directory recursively
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for f in filenames:
            if f.lower().endswith('.csv') and "metropolitan" in f:
                print(f)
                csv_files.append(os.path.join(dirpath, f))

    if not csv_files:
        print("No CSV files found.")
        return

    header_saved = False
    with open(output_file, 'w', newline='', encoding='utf-8') as out_csv:
        writer = None
        for file in csv_files:
            with open(file, 'r', newline='', encoding='utf-8') as in_csv:
                reader = csv.reader(in_csv)
                header = next(reader)  # read header
                if not header_saved:
                    writer = csv.writer(out_csv)
                    writer.writerow(header)
                    header_saved = True
                for row in reader:
                    writer.writerow(row)

    print(f"Merged {len(csv_files)} CSV files into {output_file}")

# Usage
merge_csv_files('/home/nikola/crime-data', 'merged_output.csv')
