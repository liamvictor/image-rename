# Image Rename

A Python script to find image files in a directory, get their dimensions, and generate HTML and CSV reports. It can also optionally rename the files to include their dimensions.

## First-time setup and execution

These instructions are for running the script in a Python virtual environment for the first time.

### 1. Create the virtual environment

If you don't have a virtual environment set up yet, create one in the project directory.

```bash
python3 -m venv .venv
```

### 2. Activate the virtual environment

Before you can install dependencies or run the script, you need to activate the virtual environment.

On macOS and Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

With the virtual environment active, install the necessary Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Run the script

Now you can run the script. You need to provide the path to the directory containing your images using the `-d` or `--directory` argument.

To generate the reports without renaming the files:

```bash
python3 image-rename.py -d /path/to/your/images
```

To generate the reports AND rename the files, add the `-r` or `--rename` flag:

```bash
python3 image-rename.py -d /path/to/your/images -r
```

The reports (`report.csv` and `report.html`) will be created in the `image-rename` project directory.
