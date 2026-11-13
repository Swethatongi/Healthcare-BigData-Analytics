import matplotlib.pyplot as plt

datasets = []
counts = []

with open("../processed/dataset_split.txt", "r") as file:
    for line in file:
        dataset, count = line.strip().split("\t")
        datasets.append(dataset)
        counts.append(int(count))

plt.figure(figsize=(8, 5))

plt.bar(datasets, counts)

plt.title("Training and Testing Dataset Distribution")
plt.xlabel("Dataset Type")
plt.ylabel("Number of X-ray Images")

plt.tight_layout()

plt.savefig("../output/dataset_split.png")

plt.show()
