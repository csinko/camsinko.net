#!/usr/bin/env python3

import re
import shutil
import subprocess
import sys

from pathlib import Path

# Regular expression to find pasted images in the markdown file
IMG_PATTERN = re.compile(r"!\[\[Pasted image (\d+)\.png\]\]")

# The source directory where the images are stored.
SRC_DIR = Path(
    "/Users/csinko/Library/Mobile Documents/iCloud~md~obsidian/Documents/Master/"
)

# The target directory where the images will be moved.
TARGET_DIR = Path(__file__).parent.parent / "static"


def preview_image(image_path: Path):
    """Function to preview an image using MacOS preview."""
    subprocess.run(["open", image_path])


def rename_and_move_image(old_path, new_name, target_dir) -> str:
    """Rename and move the image to the target directory."""
    new_path = target_dir / f"{new_name}.png"
    shutil.move(old_path, new_path)
    print(f"Moved {old_path.name} to {new_path}")
    return new_path.name  # Return the new file name


def update_markdown_file(markdown_file, old_reference, new_reference):
    """Update the markdown file to replace the old image reference with the new one."""
    with open(markdown_file, "r") as file:
        content = file.read()

    # Replace the old reference with the new one
    updated_content = content.replace(old_reference, new_reference)

    # Write the updated content back to the file
    with open(markdown_file, "w") as file:
        file.write(updated_content)


def process_images(markdown_file: Path, source_dir: Path, target_dir: Path):
    """Main function to process all images in the markdown file."""
    content = markdown_file.read_text()

    # Find all pasted images
    images = IMG_PATTERN.findall(content)

    if not images:
        print("No pasted images found in the markdown file.")
        return

    for image_id in images:
        image_filename = f"Pasted image {image_id}.png"
        image_path = source_dir / image_filename

        if not image_path.exists():
            print("Image {image_filename} does not exist in {source_dir}.")
            continue

        # Preview the image
        preview_image(image_path)

        # Ask the user for a new name
        new_name = input(f"Enter new name for {image_filename} (without extension): ")

        # Rename and move the image
        new_image_filename = rename_and_move_image(image_path, new_name, target_dir)

        # Update the markdown file
        old_reference = f"![[{image_filename}]]"
        new_reference = f"![{new_name}](/{new_image_filename})"

        update_markdown_file(markdown_file, old_reference, new_reference)


if __name__ == "__main__":
    # Check that correct number of args given.
    if len(sys.argv) != 2:
        print("Usage: ./cp-images.py <markdown_file>")

    markdown_file = Path(sys.argv[1])

    process_images(markdown_file, SRC_DIR, TARGET_DIR)
