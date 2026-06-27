#!/usr/bin/env python3
"""Process the latest generated PetsQuest sprite sheet into frame PNGs."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from PIL import Image


GENERATED_DIR = Path("/Users/vittoriocutolo/.codex/generated_images/019f054d-7798-7fe2-a4ae-db63e26fca19")
REMOVE_KEY = Path("/Users/vittoriocutolo/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py")
TARGET_SIZE = (362, 724)


def latest_generated_png() -> Path:
    files = sorted(GENERATED_DIR.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise SystemExit(f"No generated PNGs found in {GENERATED_DIR}")
    return files[0]


def make_left_frames(src_dir: Path, stem: str, out_dir: Path, out_stem: str, sheet_path: Path) -> None:
    frames = sorted(src_dir.glob(f"{stem}_*.png"))
    if not frames:
        raise SystemExit(f"No frames found in {src_dir} matching {stem}_*.png")
    out_dir.mkdir(parents=True, exist_ok=True)
    flipped = []
    for idx, frame in enumerate(frames, start=1):
        image = Image.open(frame).convert("RGBA")
        out = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        out_path = out_dir / f"{out_stem}_{idx:02d}.png"
        out.save(out_path)
        flipped.append(out)
        print(out_path)

    width, height = flipped[0].size
    sheet = Image.new("RGBA", (width * len(flipped), height), (0, 0, 0, 0))
    for idx, image in enumerate(flipped):
        if image.size != (width, height):
            raise SystemExit(f"Frame size mismatch: {image.size} != {(width, height)}")
        sheet.alpha_composite(image, (idx * width, 0))
    sheet.save(sheet_path)
    print(sheet_path)


def split_center_frames(sheet_path: Path, out_dir: Path, stem: str, frames: int) -> None:
    image = Image.open(sheet_path).convert("RGBA")
    out_dir.mkdir(parents=True, exist_ok=True)
    target_w, target_h = TARGET_SIZE

    for idx in range(frames):
        left = round(idx * image.width / frames)
        right = round((idx + 1) * image.width / frames)
        cell = image.crop((left, 0, right, image.height))
        bbox = cell.getchannel("A").getbbox()
        canvas = Image.new("RGBA", TARGET_SIZE, (0, 0, 0, 0))
        if bbox:
            sprite = cell.crop(bbox)
            if sprite.width > target_w or sprite.height > target_h:
                scale = min(target_w / sprite.width, target_h / sprite.height)
                sprite = sprite.resize((round(sprite.width * scale), round(sprite.height * scale)), Image.Resampling.LANCZOS)
            x = (target_w - sprite.width) // 2
            y = (target_h - sprite.height) // 2
            canvas.alpha_composite(sprite, (x, y))
        out = out_dir / f"{stem}_{idx + 1:02d}.png"
        canvas.save(out)
        print(out)

    print(f"frame_size={target_w}x{target_h}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--character", required=True, help="Character folder, e.g. main_character")
    parser.add_argument("--animation", required=True, help="Animation name, e.g. attack")
    parser.add_argument("--stem", required=True, help="Filename stem, e.g. main_character_attack")
    parser.add_argument("--frames", type=int, default=6)
    args = parser.parse_args()

    source = latest_generated_png()
    root = Path("assets/sprites") / args.character
    anim_dir = root / args.animation
    left_anim = f"{args.animation}_left"
    left_dir = root / left_anim
    anim_dir.mkdir(parents=True, exist_ok=True)

    chroma = root / f"{args.stem}_sheet_chromakey.png"
    sheet = root / f"{args.stem}_sheet.png"
    chroma.write_bytes(source.read_bytes())
    print(chroma)

    subprocess.run(
        [
            "python3",
            str(REMOVE_KEY),
            "--input",
            str(chroma),
            "--out",
            str(sheet),
            "--auto-key",
            "border",
            "--soft-matte",
            "--transparent-threshold",
            "12",
            "--opaque-threshold",
            "220",
            "--despill",
            "--force",
        ],
        check=True,
    )

    split_center_frames(sheet, anim_dir, args.stem, args.frames)

    left_stem = f"{args.stem}_left"
    make_left_frames(anim_dir, args.stem, left_dir, left_stem, root / f"{left_stem}_sheet.png")


if __name__ == "__main__":
    main()
