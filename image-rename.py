#!/usr/bin/env python3

import argparse
import os
from datetime import datetime
from pathlib import Path

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Find images and rename them")
    parser.add_argument(
        "-d",
        "--directory",
        dest="directory",
        help="The directory to search for images",
        required=True,
    )
    parser.add_argument(
        "-r",
        "--rename",
        dest="rename",
        action="store_true",
        help="Rename the files",
    )
    args = parser.parse_args()

    image_files = []
    image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]

    for root, _, files in os.walk(args.directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_path = Path(root) / file
                try:
                    from PIL import Image

                    with Image.open(image_path) as img:
                        width, height = img.size
                        image_files.append(
                            {
                                "path": image_path,
                                "name": file,
                                "x": width,
                                "y": height,
                            }
                        )
                except ImportError:
                    print("Pillow is not installed. Please install it with 'pip install Pillow'")
                    return
                except Exception as e:
                    print(f"Could not process {image_path}: {e}")
    
    for image in image_files:
        path = image["path"]
        name = image["name"]
        x = image["x"]
        y = image["y"]

        stem = Path(name).stem
        ext = Path(name).suffix

        new_stem = f"{stem}-{x}-{y}".lower().replace("_", "-")
        new_name = f"{new_stem}{ext}"
        
        image["new_name"] = new_name

    print(f"Found {len(image_files)} images.")
    for image in image_files:
        print(f"  - {image['path']} -> {image['new_name']}")



if __name__ == "__main__":
    main()
