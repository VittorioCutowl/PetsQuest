#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

ICON_DIRS = [
    Path("assets/ui/abilities"),
    Path("assets/inventory/weapons"),
    Path("assets/inventory/potions"),
    Path("assets/inventory/equipment"),
    Path("assets/generated_ui/class_icons"),
]

MAX_CENTER_OFFSET = 5


def iter_icons():
    for folder in ICON_DIRS:
        for path in sorted(folder.glob("*.png")):
            if path.name.startswith("_sheet"):
                continue
            yield path


def audit(path):
    image = Image.open(path).convert("RGBA")
    width, height = image.size
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return [path, width, height, "empty", "", "", ""]

    x0, y0, x1, y1 = bbox
    center_x = (x0 + x1) / 2
    center_y = (y0 + y1) / 2
    dx = center_x - width / 2
    dy = center_y - height / 2
    is_square = width == height
    is_centered = abs(dx) <= MAX_CENTER_OFFSET and abs(dy) <= MAX_CENTER_OFFSET
    status = "ok" if is_square and is_centered else "check"
    return [path, width, height, status, round(dx, 1), round(dy, 1), f"{x1 - x0}x{y1 - y0}"]


def main():
    rows = [audit(path) for path in iter_icons()]
    checks = [row for row in rows if row[3] != "ok"]
    print(f"checked={len(rows)} check={len(checks)}")
    for path, width, height, status, dx, dy, bbox in checks:
        print(f"{status}\t{width}x{height}\tdx={dx}\tdy={dy}\tbbox={bbox}\t{path}")


if __name__ == "__main__":
    main()
