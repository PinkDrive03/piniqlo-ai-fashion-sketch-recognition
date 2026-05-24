from __future__ import annotations

import json
from pathlib import Path

import torch

from src.config import build_class_items, get_category_label
from src.model import QuickDrawClothingCNN
from src.preprocess import decode_data_url, preprocess_canvas_image


class QuickDrawClothingClassifier:
    def __init__(self, model_dir: Path) -> None:
        self.model_dir = model_dir
        self.model_path = model_dir / "quickdraw_clothing_cnn.pt"
        self.labels_path = model_dir / "labels.json"
        self.device = torch.device("cpu")
        self.class_names: list[str] = []
        self.class_items: list[dict[str, str]] = []
        self.model: QuickDrawClothingCNN | None = None
        self.is_ready = False
        self._load()

    def _load(self) -> None:
        if not self.model_path.exists() or not self.labels_path.exists():
            return

        self.class_names = json.loads(self.labels_path.read_text(encoding="utf-8"))
        self.class_items = build_class_items(self.class_names)
        self.model = QuickDrawClothingCNN(num_classes=len(self.class_names))
        state_dict = torch.load(self.model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.to(self.device)
        self.model.eval()
        self.is_ready = True

    def predict(self, image_data: str) -> dict:
        if not self.model:
            raise RuntimeError("Model chưa được nạp.")

        image = decode_data_url(image_data)
        tensor = torch.tensor(
            preprocess_canvas_image(image),
            dtype=torch.float32,
            device=self.device,
        ).unsqueeze(0)

        with torch.inference_mode():
            logits = self.model(tensor)
            probabilities = torch.softmax(logits, dim=1)[0].cpu().tolist()

        ranked = sorted(
            zip(self.class_names, probabilities),
            key=lambda item: item[1],
            reverse=True,
        )
        top_label, top_score = ranked[0]

        return {
            "key": top_label,
            "label": get_category_label(top_label),
            "confidence": round(top_score * 100, 2),
            "probabilities": [
                {
                    "key": label,
                    "label": get_category_label(label),
                    "score": round(score * 100, 2),
                }
                for label, score in ranked
            ],
        }
