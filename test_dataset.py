from src.dataset import CornellDataset


dataset = CornellDataset("data/cornell")

print(f"Valid image-annotation pairs: {len(dataset)}")

print(
    f"Missing annotations: "
    f"{len(dataset.missing_annotations)}"
)

print("\nFirst five samples:")

for i in range(min(5, len(dataset))):
    sample = dataset[i]

    print(f"\nSample {i + 1}")
    print(f"Image ID: {sample['image_id']}")
    print(f"Image: {sample['image_path']}")
    print(f"Annotation: {sample['annotation_path']}")

print("\nImages missing annotations:")

for path in dataset.missing_annotations:
    print(path)
    