#!/usr/bin/env python3

import sys
import csv

reader = csv.reader(sys.stdin)

# Skip header
next(reader, None)

for row in reader:
    if len(row) >= 6:

        specific_category = row[4].strip()
        broad_category = row[5].strip()

        if broad_category:
            print(f"Broad:{broad_category}\t1")

        if specific_category:
            print(f"Specific:{specific_category}\t1")
