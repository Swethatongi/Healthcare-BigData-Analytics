import matplotlib.pyplot as plt

# Read MapReduce output
diseases = []
counts = []

with open("../processed/disease_count.txt", "r") as file:
    for line in file:
        disease, count = line.strip().split("\t")
        diseases.append(disease)
        counts.append(int(count))

# Create bar chart
plt.figure(figsize=(8, 5))

plt.bar(diseases, counts)

plt.title("Healthcare Disease Distribution")
plt.xlabel("Disease Category")
plt.ylabel("Number of X-ray Images")

plt.tight_layout()

# Save chart
plt.savefig("../output/disease_distribution.png")

plt.show()
