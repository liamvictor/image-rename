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
        
        dimension_suffix = f"-{x}-{y}"

        if stem.lower().endswith(dimension_suffix):
            image["new_name"] = name
        else:
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
    dir_name = Path(args.directory).name
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    csv_report_path = output_dir / f"report-{dir_name}.csv"
    html_report_path = output_dir / f"report-{dir_name}.html"

    generate_csv_report(image_files, csv_report_path)
    generate_html_report(image_files, html_report_path, args.rename)

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


def generate_csv_report(image_files, report_path):
    """Generate a CSV report of the image files"""
    with open(report_path, "w") as f:
        f.write("path,name,x,y,new_name\n")
        for image in image_files:
            f.write(
                f"{image['path']},{image['name']},{image['x']},{image['y']},{image['new_name']}\n"
            )
    print(f"Generated {report_path}")


def generate_html_report(image_files, report_path, rename_active):
    """Generate an HTML report of the image files"""
    with open(report_path, "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container-fluid">
    <h1 class="mt-4">Image Report</h1>
""")
        f.write("<table class='table table-striped table-bordered'>\n")
        f.write("<thead class='thead-dark'><tr><th>Path</th><th>Name</th><th>X</th><th>Y</th><th>New Name</th><th>Image</th></tr></thead>\n")
        f.write("<tbody>\n")
        for image in image_files:
            path_only = image['path'].parent
            new_name_cell = image['new_name'] if image['name'] != image['new_name'] else ""
            
            if rename_active and image['name'] != image['new_name']:
                source_path = image['path'].parent / image['new_name']
            else:
                source_path = image['path']
            
            relative_image_path = os.path.relpath(source_path, report_path.parent)

            f.write(
                f"<tr><td>{path_only}</td><td>{image['name']}</td><td>{image['x']}</td><td>{image['y']}</td><td>{new_name_cell}</td>"
            )
            f.write(f"<td><img src='{relative_image_path}' width='100' class='img-fluid'></td></tr>\n")
        f.write("</tbody></table>\n")

        f.write("<h2 class='mt-4'>Rename Commands</h2>\n")
        f.write("<textarea class='form-control' rows='10' readonly>\n")
        for image in image_files:
            if image['name'] == image['new_name']:
                continue
            f.write(f"mv '{image['path']}' '{image['path'].parent / image['new_name']}'\n")
        f.write("</textarea>\n")
        f.write("</div></body></html>\n")

    print(f"Generated {report_path}")




if __name__ == "__main__":
    main()
