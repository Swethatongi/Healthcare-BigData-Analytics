#!/usr/bin/env python3

import sys
import csv

reader = csv.reader(sys.stdin)

# Skip the header
next(reader, None)

for row in reader:
    if len(row) >= 3:
        disease = row[2].strip()

        if disease:
            print(f"{disease}\t1")
