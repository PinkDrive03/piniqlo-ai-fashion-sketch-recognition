import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.config import DEFAULT_CATEGORIES
from src.training import train_quickdraw_model


CACHE_DIR = BASE_DIR / "data" / "quickdraw"
MODEL_DIR = BASE_DIR / "models"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    artifacts = train_quickdraw_model(
        categories=DEFAULT_CATEGORIES,
        cache_dir=CACHE_DIR,
        model_dir=MODEL_DIR,
        samples_per_class=2000,
        val_per_class=400,
        epochs=6,
    )
    print("Hoàn tất huấn luyện model QuickDraw quần áo.")
    print(f"Lớp dữ liệu: {', '.join(artifacts.class_names)}")
    print(f"Số mẫu train: {artifacts.training_samples}")
    print(f"Số mẫu validation: {artifacts.validation_samples}")
    print(f"Độ chính xác validation tốt nhất: {artifacts.best_accuracy:.2%}")
