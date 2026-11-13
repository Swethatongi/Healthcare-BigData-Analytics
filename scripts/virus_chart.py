import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

categories = []
counts = []

with open("../processed/virus_categories.txt", "r") as file:
    for line in file:
        category, count = line.strip().split("\t")
        categories.append(category)
        counts.append(int(count))

plt.figure(figsize=(11, 6))

plt.bar(categories, counts)

plt.title("Virus and Bacterial Category Distribution")
plt.xlabel("Category")
plt.ylabel("Number of X-ray Images")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig("../output/virus_distribution.png")

print("Virus category chart saved successfully!")
