#!/usr/bin/env python3
"""Copy the latest generated image into a normalized PetsQuest asset."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from PIL import Image


GENERATED_DIR = Path("/Users/vittoriocutolo/.codex/generated_images/019f054d-7798-7fe2-a4ae-db63e26fca19")
REMOVE_KEY = Path("/Users/vittoriocutolo/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py")


def latest_generated_png() -> Path:
    files = sorted(GENERATED_DIR.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise SystemExit(f"No generated PNGs found in {GENERATED_DIR}")
    return files[0]


def cover_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def contain_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    image.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(image, ((target_w - image.width) // 2, (target_h - image.height) // 2))
    return canvas


def split_grid(image: Image.Image, out_dir: Path, names: list[str], columns: int, rows: int, size: tuple[int, int]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    cell_w = image.width / columns
    cell_h = image.height / rows
    for index, name in enumerate(names):
        row = index // columns
        col = index % columns
        cell = image.crop((
            round(col * cell_w),
            round(row * cell_h),
            round((col + 1) * cell_w),
            round((row + 1) * cell_h),
        ))
        bbox = cell.getchannel("A").getbbox()
        canvas = Image.new("RGBA", size, (0, 0, 0, 0))
        if bbox:
            sprite = cell.crop(bbox)
            sprite = contain_resize(sprite, size)
            canvas.alpha_composite(sprite)
        out = out_dir / f"{name}.png"
        canvas.save(out)
        print(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Output file for a single normalized image.")
    parser.add_argument("--size", required=True, help="Target size, e.g. 820x400.")
    parser.add_argument("--mode", choices=["cover", "contain", "alpha-sheet"], default="cover")
    parser.add_argument("--split-dir", type=Path)
    parser.add_argument("--names", help="Comma-separated output names for alpha-sheet mode.")
    parser.add_argument("--columns", type=int, default=1)
    parser.add_argument("--rows", type=int, default=1)
    args = parser.parse_args()

    width, height = map(int, args.size.lower().split("x"))
    source = latest_generated_png()

    if args.mode == "alpha-sheet":
        if not args.split_dir or not args.names:
            raise SystemExit("--split-dir and --names are required for alpha-sheet mode")
        tmp_chroma = args.split_dir / "_sheet_chromakey.png"
        tmp_alpha = args.split_dir / "_sheet_alpha.png"
        args.split_dir.mkdir(parents=True, exist_ok=True)
        tmp_chroma.write_bytes(source.read_bytes())
        subprocess.run([
            "python3", str(REMOVE_KEY),
            "--input", str(tmp_chroma),
            "--out", str(tmp_alpha),
            "--auto-key", "border",
            "--soft-matte",
            "--transparent-threshold", "12",
            "--opaque-threshold", "220",
            "--despill",
            "--force",
        ], check=True)
        image = Image.open(tmp_alpha).convert("RGBA")
        split_grid(image, args.split_dir, args.names.split(","), args.columns, args.rows, (width, height))
        print(tmp_chroma)
        print(tmp_alpha)
        return

    if not args.out:
        raise SystemExit("--out is required unless --mode alpha-sheet")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(source).convert("RGBA")
    if args.mode == "cover":
        image = cover_resize(image, (width, height))
    else:
        image = contain_resize(image, (width, height))
    image.save(args.out)
    print(args.out)
    print(f"size={width}x{height}")


if __name__ == "__main__":
    main()
