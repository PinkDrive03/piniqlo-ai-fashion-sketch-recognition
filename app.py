from pathlib import Path

from flask import Flask, jsonify, render_template, request

from src.config import DEFAULT_CATEGORIES, build_class_items
from src.inference import QuickDrawClothingClassifier


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

app = Flask(__name__)
classifier = QuickDrawClothingClassifier(model_dir=MODEL_DIR)


@app.get("/")
def index():
    class_items = classifier.class_items or build_class_items(DEFAULT_CATEGORIES)
    return render_template(
        "index.html",
        class_items=class_items,
        model_ready=classifier.is_ready,
    )


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    image_data = payload.get("image")

    if not image_data:
        return jsonify({"error": "Thiếu dữ liệu ảnh vẽ."}), 400

    if not classifier.is_ready:
        return (
            jsonify(
                {
                    "error": (
                        "Model chưa sẵn sàng. Hãy chạy scripts/train_quickdraw.py "
                        "để tải dữ liệu QuickDraw và huấn luyện model."
                    )
                }
            ),
            503,
        )

    result = classifier.predict(image_data)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
