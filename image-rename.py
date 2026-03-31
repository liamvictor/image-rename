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

    # Handle filename clashes
    new_filenames = {}
    for image in image_files:
        new_name = image["new_name"]
        if new_name in new_filenames:
            new_filenames[new_name] += 1
            version = new_filenames[new_name]
            stem = Path(new_name).stem
            ext = Path(new_name).suffix
            image["new_name"] = f"{stem}-v{version}{ext}"
        else:
            new_filenames[image["new_name"]] = 1

    print(f"Found {len(image_files)} images.")

    # Generate reports
    generate_csv_report(image_files)
    generate_html_report(image_files)

    if args.rename:
        print("Renaming files...")
        for image in image_files:
            new_path = image["path"].parent / image["new_name"]
            try:
                image["path"].rename(new_path)
                print(f"  - Renamed {image['path']} to {new_path}")
            except OSError as e:
                print(f"Could not rename {image['path']}: {e}")
    else:
        for image in image_files:
            print(f"  - {image['path']} -> {image['new_name']}")


def generate_csv_report(image_files):
    """Generate a CSV report of the image files"""
    with open("report.csv", "w") as f:
        f.write("path,name,x,y,new_name\n")
        for image in image_files:
            f.write(
                f"{image['path']},{image['name']},{image['x']},{image['y']},{image['new_name']}\n"
            )
    print("Generated report.csv")


def generate_html_report(image_files):
    """Generate an HTML report of the image files"""
    with open("report.html", "w") as f:
        f.write("<html><body>\n")
        f.write("<h1>Image Report</h1>\n")
        f.write("<table border='1'>\n")
        f.write("<tr><th>Path</th><th>Name</th><th>X</th><th>Y</th><th>New Name</th><th>Image</th></tr>\n")
        for image in image_files:
            f.write(
                f"<tr><td>{image['path']}</td><td>{image['name']}</td><td>{image['x']}</td><td>{image['y']}</td><td>{image['new_name']}</td>"
            )
            f.write(f"<td><img src='{image['path']}' width='100'></td></tr>\n")
        f.write("</table>\n")

        f.write("<h2>Rename Commands</h2>\n")
        f.write("<textarea rows='10' cols='100'>\n")
        for image in image_files:
            f.write(f"mv '{image['path']}' '{image['path'].parent / image['new_name']}'\n")
        f.write("</textarea>\n")

        f.write("</body></html>\n")
    print("Generated report.html")




if __name__ == "__main__":
    main()
