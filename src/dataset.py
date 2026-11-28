from pathlib import Path


class CornellDataset:

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

        if not self.root_dir.is_dir():
            raise FileNotFoundError(self.root_dir)

        self.samples = []
        self.missing_annotations = []

        self._load_samples()

    def _load_samples(self):
        image_paths = sorted(
            self.root_dir.rglob("*r.png")
        )

        for image_path in image_paths:
            image_id = image_path.stem[:-1]

            annotation_path = image_path.with_name(
                f"{image_id}cpos.txt"
            )

            if not annotation_path.is_file():
                self.missing_annotations.append(image_path)
                continue

            self.samples.append({
                "image_id": image_id,
                "image_path": image_path,
                "annotation_path": annotation_path
            })

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        return self.samples[index]
    