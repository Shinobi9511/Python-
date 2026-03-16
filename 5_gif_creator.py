
import os
import glob
from PIL import Image


def load_images(folder: str, extensions=("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.webp")) -> list:
    """Load and sort images from a folder."""
    paths = []
    for ext in extensions:
        paths.extend(glob.glob(os.path.join(folder, ext)))
    paths.sort()
    return paths


def resize_image(img: Image.Image, max_size: int) -> Image.Image:
    """Resize image maintaining aspect ratio."""
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    return img


def create_gif(image_paths: list, output_path: str, duration: int, loop: int, max_size: int):
    """Create animated GIF from image paths."""
    frames = []
    for path in image_paths:
        try:
            img = Image.open(path).convert("RGBA")
            if max_size:
                img = resize_image(img, max_size)
            # Convert to palette for smaller GIF
            img = img.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=256)
            frames.append(img)
            print(f"  ✅ Loaded: {os.path.basename(path)}")
        except Exception as e:
            print(f"  ❌ Skipped {os.path.basename(path)}: {e}")

    if len(frames) < 2:
        print("\n  ⚠️  Need at least 2 valid images to create a GIF.")
        return

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=loop,
        optimize=True,
    )
    size_kb = os.path.getsize(output_path) / 1024
    print(f"\n  🎉 GIF created: {os.path.abspath(output_path)}")
    print(f"  📦 File size : {size_kb:.1f} KB")
    print(f"  🖼️  Frames   : {len(frames)}")
    print(f"  ⏱️  Duration : {duration}ms per frame")


def main():
    print("=" * 45)
    print("          GIF CREATOR")
    print("=" * 45)

    folder = input("\n  Folder containing images: ").strip()
    if not os.path.isdir(folder):
        print("  ❌ Folder not found.")
        return

    image_paths = load_images(folder)
    if not image_paths:
        print(f"  ❌ No supported images found in '{folder}'.")
        return

    print(f"\n  Found {len(image_paths)} image(s):\n")
    for p in image_paths:
        print(f"    - {os.path.basename(p)}")

    output = input("\n  Output GIF filename [default: output.gif]: ").strip()
    if not output:
        output = "output.gif"
    if not output.endswith(".gif"):
        output += ".gif"

    try:
        duration = int(input("  Frame duration in ms [default: 500]: ").strip() or 500)
    except ValueError:
        duration = 500

    try:
        loop = int(input("  Loop count (0 = infinite) [default: 0]: ").strip() or 0)
    except ValueError:
        loop = 0

    try:
        max_size = int(input("  Max frame size in px (0 = no resize) [default: 500]: ").strip() or 500)
    except ValueError:
        max_size = 500

    print(f"\n  ⚙️  Creating GIF...\n")
    create_gif(image_paths, output, duration, loop, max_size if max_size > 0 else None)


if __name__ == "__main__":
    main()
