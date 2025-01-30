# PipeWipe - Metadata Cleaning Tool

&nbsp;

PipeWipe allows to **display, remove, or securely overwrite metadata** from various file types. This helps improve privacy and security by ensuring sensitive metadata is removed from documents, images, videos, and other files.

- Program usage details:
```sh
python pipewipe.py --info
```
- Basic help:
```sh
python pipewipe.py -h
```
&nbsp;

## 🗂️ Supported File Types

| File Type                  | Metadata Removal Method              |
|----------------------------|-------------------------------------|
| **Images** (`.jpg`, `.png`, `.tiff`) | Strips EXIF metadata |
| **Audio** (`.mp3`, `.flac`, `.mp4`, `.m4a`) | Clears ID3 or FLAC metadata |
| **PDF** (`.pdf`)           | Removes embedded metadata |
| **Videos** (`.mp4`, `.mkv`, `.avi`, `.mov`) | Uses `ffmpeg` to strip metadata |
| **Word Docs** (`.docx`)    | Clears core properties |
| **Excel Docs** (`.xlsx`)   | Clears workbook properties |
| **Markdown** (`.md`)       | Strips metadata sections |

&nbsp;

## Main Features

### Default (no argument)
- Creates a **new file** in the `no_meta` folder without metadata.

### `--display`
- Shows existing metadata from a specified file or folder.

### `--secure`
- Creates a **new file** in the `no_meta` folder.
- Overwrites metadata **3 times by default** (or a custom number with argument `--ow-times`).

### `--owrite`
- Modifies the **original file** instead of creating a new one.
- Overwrites metadata **3 times by default** (or a custom number with argument `--ow-times`).

&nbsp;

## 🛠️ How to Use It

### **1️⃣ Display Metadata**
```sh
python pipewipe.py path/to/file --display
```

### **2️⃣ Remove Metadata (Default)**
```sh
python pipewipe.py path/to/file
```
- Creates a **new file** in `no_meta` without metadata.

### **3️⃣ Securely Overwrite Metadata (`--secure`)**
```sh
python pipewipe.py path/to/file --secure
```
- Creates a **new file** in `no_meta` with metadata overwritten **3 times**.

### **4️⃣ Set Custom Overwrites (`--ow-times`)**
```sh
python pipewipe.py path/to/file --secure --ow-times 5
```
- Creates a **new file** in `no_meta` with metadata overwritten **5 times**.

### **5️⃣ Overwrite Metadata in the Original File (`--owrite`)**
```sh
python pipewipe.py path/to/file --owrite
```
- Directly modifies the **original file** (overwriting **3 times by default**).

### **6️⃣ Overwrite Original File with Custom Overwrites**
```sh
python pipewipe.py path/to/file --owrite --ow-times 7
```
- Modifies the **original file**, overwriting metadata **7 times**.


## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).  
Feel free to **use, modify, and share** it.

