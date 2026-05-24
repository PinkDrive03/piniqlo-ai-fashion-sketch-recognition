from __future__ import annotations


CATEGORY_LABELS = {
    "t-shirt": "Áo thun",
    "pants": "Quần dài",
    "jacket": "Áo khoác",
    "shorts": "Quần short",
    "sweater": "Áo len",
    "shoe": "Giày",
    "sock": "Tất",
    "underwear": "Đồ lót",
    "hat": "Mũ",
    "backpack": "Ba lô",
}

DEFAULT_CATEGORIES = list(CATEGORY_LABELS.keys())


def get_category_label(category_key: str) -> str:
    return CATEGORY_LABELS.get(category_key, category_key.replace("-", " ").title())


def build_class_items(category_keys: list[str]) -> list[dict[str, str]]:
    return [{"key": key, "label": get_category_label(key)} for key in category_keys]
