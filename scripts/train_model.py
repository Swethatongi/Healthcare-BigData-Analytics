import joblib
import csv
import numpy as np

from pathlib import Path
from PIL import Image

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Dataset paths
BASE = Path.home() / "Healthcare_BigData/dataset/extracted/Coronahack-Chest-XRay-Dataset/Coronahack-Chest-XRay-Dataset"

CSV_FILE = Path.home() / "Healthcare_BigData/dataset/extracted/Chest_xray_Corona_Metadata.csv"

# HOG feature extraction
def extract_hog(image_path):

    image = Image.open(image_path).convert("L")
    image = image.resize((64, 64))

    pixels = np.asarray(image, dtype=np.float32)

    gy, gx = np.gradient(pixels)

    magnitude = np.sqrt(gx**2 + gy**2)

    orientation = np.degrees(np.arctan2(gy, gx)) % 180

    features = []

    # Divide image into 8x8 cells
    for y in range(0, 64, 8):
        for x in range(0, 64, 8):

            cell_mag = magnitude[y:y+8, x:x+8]
            cell_ang = orientation[y:y+8, x:x+8]

            bins = np.floor(cell_ang / 20).astype(int)
            bins = np.clip(bins, 0, 8)

            histogram = np.bincount(
                bins.ravel(),
                weights=cell_mag.ravel(),
                minlength=9
            )

            histogram = histogram / (
                np.linalg.norm(histogram) + 1e-6
            )

            features.extend(histogram)

    return np.array(features, dtype=np.float32)


# Read metadata
train_features = []
train_labels = []

test_features = []
test_labels = []

with open(CSV_FILE, newline="") as file:

    reader = csv.DictReader(file)

    for index, row in enumerate(reader, start=1):

        split = row["Dataset_type"].strip().lower()
        filename = row["X_ray_image_name"].strip()
        label = row["Label"].strip().lower()

        image_path = BASE / split / filename

        if not image_path.is_file():
            continue

        if label == "normal":
            target = 0
        elif label == "pnemonia":
            target = 1
        else:
            continue

        features = extract_hog(image_path)

        if split == "train":
            train_features.append(features)
            train_labels.append(target)

        elif split == "test":
            test_features.append(features)
            test_labels.append(target)

        if index % 500 == 0:
            print("Processed metadata rows:", index)


# Convert features into NumPy arrays
X_train = np.array(train_features)
y_train = np.array(train_labels)

X_test = np.array(test_features)
y_test = np.array(test_labels)

print("\nTraining data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)

# Train Logistic Regression
print("\nTraining Logistic Regression model...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Evaluate model
print("\nMODEL EVALUATION")

print("Accuracy:", accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=["Normal", "Pneumonia"]
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nModel training and evaluation completed!")
joblib.dump(model, "../output/healthcare_model.pkl")
print("Model saved successfully!")
