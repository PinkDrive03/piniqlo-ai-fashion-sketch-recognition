from __future__ import annotations

import copy
import json
import random
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from src.model import QuickDrawClothingCNN


QUICKDRAW_BASE_URL = "https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap"


@dataclass
class TrainingArtifacts:
    class_names: list[str]
    training_samples: int
    validation_samples: int
    best_accuracy: float


def download_category(category: str, cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    file_path = cache_dir / f"{category}.npy"
    if file_path.exists():
        return file_path

    encoded = urllib.parse.quote(category)
    url = f"{QUICKDRAW_BASE_URL}/{encoded}.npy"
    urllib.request.urlretrieve(url, file_path)
    return file_path


def load_quickdraw_arrays(
    categories: list[str],
    cache_dir: Path,
    samples_per_class: int,
    val_per_class: int,
    seed: int,
) -> tuple[TensorDataset, TensorDataset]:
    random.seed(seed)
    arrays: list[np.ndarray] = []
    labels: list[np.ndarray] = []
    val_arrays: list[np.ndarray] = []
    val_labels: list[np.ndarray] = []

    for label_index, category in enumerate(categories):
        file_path = download_category(category, cache_dir)
        data = np.load(file_path)
        required = samples_per_class + val_per_class
        if data.shape[0] < required:
            raise ValueError(
                f"Category '{category}' chỉ có {data.shape[0]} mẫu, nhỏ hơn {required}."
            )

        indices = np.random.default_rng(seed + label_index).choice(
            data.shape[0],
            size=required,
            replace=False,
        )
        selected = data[indices].reshape(required, 1, 28, 28).astype(np.float32) / 255.0
        train_part = selected[:samples_per_class]
        val_part = selected[samples_per_class:]

        arrays.append(train_part)
        labels.append(np.full(samples_per_class, label_index))
        val_arrays.append(val_part)
        val_labels.append(np.full(val_per_class, label_index))

    x_train = torch.tensor(np.concatenate(arrays), dtype=torch.float32)
    y_train = torch.tensor(np.concatenate(labels), dtype=torch.long)
    x_val = torch.tensor(np.concatenate(val_arrays), dtype=torch.float32)
    y_val = torch.tensor(np.concatenate(val_labels), dtype=torch.long)

    train_dataset = TensorDataset(x_train, y_train)
    val_dataset = TensorDataset(x_val, y_val)
    return train_dataset, val_dataset


def evaluate_model(model: QuickDrawClothingCNN, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    correct = 0
    total = 0

    with torch.inference_mode():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            logits = model(images)
            predictions = logits.argmax(dim=1)
            correct += (predictions == labels).sum().item()
            total += labels.size(0)

    return correct / max(total, 1)


def train_quickdraw_model(
    categories: list[str],
    cache_dir: Path,
    model_dir: Path,
    samples_per_class: int = 2500,
    val_per_class: int = 500,
    epochs: int = 6,
    batch_size: int = 128,
    learning_rate: float = 1e-3,
    seed: int = 42,
) -> TrainingArtifacts:
    model_dir.mkdir(parents=True, exist_ok=True)
    train_dataset, val_dataset = load_quickdraw_arrays(
        categories=categories,
        cache_dir=cache_dir,
        samples_per_class=samples_per_class,
        val_per_class=val_per_class,
        seed=seed,
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = QuickDrawClothingCNN(num_classes=len(categories)).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()
    best_accuracy = 0.0
    best_state = None

    for _ in range(epochs):
        model.train()
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            logits = model(images)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

        accuracy = evaluate_model(model, val_loader, device)
        if accuracy >= best_accuracy:
            best_accuracy = accuracy
            best_state = copy.deepcopy(model.state_dict())

    if not best_state:
        raise RuntimeError("Huấn luyện không tạo được checkpoint.")

    torch.save(best_state, model_dir / "quickdraw_clothing_cnn.pt")
    (model_dir / "labels.json").write_text(
        json.dumps(categories, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return TrainingArtifacts(
        class_names=categories,
        training_samples=len(train_dataset),
        validation_samples=len(val_dataset),
        best_accuracy=best_accuracy,
    )
