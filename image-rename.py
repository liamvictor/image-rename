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

    print(f"Searching for images in {args.directory}")


if __name__ == "__main__":
    main()
