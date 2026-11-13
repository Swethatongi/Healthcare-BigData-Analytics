#!/usr/bin/env python3

import sys

current_disease = None
current_count = 0

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    disease, count = line.split("\t")

    count = int(count)

    if current_disease == disease:
        current_count += count
    else:
        if current_disease is not None:
            print(f"{current_disease}\t{current_count}")

        current_disease = disease
        current_count = count

if current_disease is not None:
    print(f"{current_disease}\t{current_count}")
