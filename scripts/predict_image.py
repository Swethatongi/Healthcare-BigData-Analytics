import joblib
import numpy as np

from pathlib import Path
from PIL import Image

# Load the trained model
model_path = Path.home() / "Healthcare_BigData/output/healthcare_model.pkl"
model = joblib.load(model_path)

# Select a test image
image_path = (
    Path.home()
    / "Healthcare_BigData/dataset/extracted/Coronahack-Chest-XRay-Dataset/Coronahack-Chest-XRay-Dataset/test/IM-0001-0001.jpeg"
)

# Extract HOG features (same method used during training)
def extract_hog(image_path):

    image = Image.open(image_path).convert("L")
    image = image.resize((64, 64))

    pixels = np.asarray(image, dtype=np.float32)

    gy, gx = np.gradient(pixels)

    magnitude = np.sqrt(gx**2 + gy**2)

    orientation = np.degrees(np.arctan2(gy, gx)) % 180

    features = []

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


# Extract features and predict
features = extract_hog(image_path)

features = features.reshape(1, -1)

prediction = model.predict(features)

if prediction[0] == 0:
    print("Prediction: NORMAL")
else:
    print("Prediction: PNEUMONIA")

print("Image:", image_path.name)
print("Prediction completed successfully!")
