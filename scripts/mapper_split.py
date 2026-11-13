#!/usr/bin/env python3

import sys
import csv

reader = csv.reader(sys.stdin)

# Skip CSV header
next(reader, None)

for row in reader:
    if len(row) >= 4:
        dataset_type = row[3].strip()

        if dataset_type:
            print(f"{dataset_type}\t1")
