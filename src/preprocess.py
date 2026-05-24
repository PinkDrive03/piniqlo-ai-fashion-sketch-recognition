from __future__ import annotations

import base64
import io

import numpy as np
from PIL import Image, ImageOps


def decode_data_url(data_url: str) -> Image.Image:
    if "," not in data_url:
        raise ValueError("Định dạng ảnh không hợp lệ.")

    _, encoded = data_url.split(",", 1)
    binary = base64.b64decode(encoded)
    return Image.open(io.BytesIO(binary)).convert("L")


def preprocess_canvas_image(image: Image.Image, output_size: int = 28) -> np.ndarray:
    # Convert the white canvas with a colored stroke into a QuickDraw-like bitmap.
    grayscale = image.convert("L")
    inverted = ImageOps.invert(grayscale)
    array = np.array(inverted, dtype=np.uint8)
    array[array < 20] = 0

    non_zero = np.argwhere(array > 0)
    if non_zero.size == 0:
        return np.zeros((1, output_size, output_size), dtype=np.float32)

    top, left = non_zero.min(axis=0)
    bottom, right = non_zero.max(axis=0) + 1
    cropped = Image.fromarray(array[top:bottom, left:right])

    target_inner = output_size - 8
    width, height = cropped.size
    scale = target_inner / max(width, height)
    resized = cropped.resize(
        (max(1, round(width * scale)), max(1, round(height * scale))),
        Image.Resampling.LANCZOS,
    )

    canvas = Image.new("L", (output_size, output_size), color=0)
    paste_x = (output_size - resized.width) // 2
    paste_y = (output_size - resized.height) // 2
    canvas.paste(resized, (paste_x, paste_y))

    normalized = np.array(canvas, dtype=np.float32) / 255.0
    return normalized[None, :, :]
