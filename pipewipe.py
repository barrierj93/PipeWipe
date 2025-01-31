import os
import shutil
import argparse
import subprocess
from tqdm import tqdm
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.id3 import ID3
from PyPDF2 import PdfReader, PdfWriter
from docx import Document
import openpyxl

def display_metadata(file_path):
    ext = file_path.lower().split('.')[-1]
    metadata = None
    if ext in ['jpg', 'jpeg', 'png', 'tiff']:
        metadata = Image.open(file_path).info
    elif ext in ['mp3', 'flac', 'mp4', 'm4a']:
        if ext == 'mp3':
            metadata = MP3(file_path).tags
        elif ext == 'flac':
            metadata = FLAC(file_path).tags
        elif ext in ['mp4', 'm4a']:
            metadata = MP4(file_path).tags
    elif ext == 'pdf':
        metadata = PdfReader(file_path).metadata
    elif ext in ['mp4', 'mkv', 'avi', 'mov']:
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format_tags", "-of", "json", file_path], capture_output=True, text=True)
        metadata = result.stdout
    elif ext == 'docx':
        metadata = Document(file_path).core_properties.__dict__
    elif ext == 'xlsx':
        metadata = openpyxl.load_workbook(file_path).properties.__dict__
    elif ext == 'md':
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        metadata = [line for line in lines if line.startswith("---")]
    
    print("\n\n")
    if metadata:
        print("File Metadata:")
        for key, value in metadata.items() if isinstance(metadata, dict) else enumerate(metadata):
            print(f"  - {key}: {value}")
    else:
        print("No metadata found.")
def secure_remove_metadata(file_path, output_path, overwrite_times=3):
    for _ in range(overwrite_times):
        remove_metadata(file_path, output_path)
    print(f"Metadata securely overwritten {overwrite_times} times for {file_path} -> {output_path}")

def overwrite_metadata(file_path, overwrite_times=3):
    for _ in range(overwrite_times):
        remove_metadata(file_path, file_path)
    print(f"Metadata securely overwritten {overwrite_times} times for {file_path} (original file modified)")

def remove_metadata(file_path, output_path):
    ext = file_path.lower().split('.')[-1]
    if ext in ['jpg', 'jpeg', 'png', 'tiff']:
        image = Image.open(file_path)
        data = list(image.getdata())
        image_clean = Image.new(image.mode, image.size)
        image_clean.putdata(data)
        image_clean.save(output_path)
    elif ext in ['mp3', 'flac', 'mp4', 'm4a']:
        audio = None
        if ext == 'mp3':
            audio = MP3(file_path)
        elif ext == 'flac':
            audio = FLAC(file_path)
        elif ext in ['mp4', 'm4a']:
            audio = MP4(file_path)
        audio.delete()
        audio.save()
        shutil.copy(file_path, output_path)
    elif ext == 'pdf':
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.add_metadata({})
            with open(output_path, "wb") as out_file:
                writer.write(out_file)
    elif ext in ['mp4', 'mkv', 'avi', 'mov']:
        subprocess.run(["ffmpeg", "-i", file_path, "-map_metadata", "-1", "-c:v", "copy", "-c:a", "copy", output_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif ext == 'docx':
        doc = Document(file_path)
        doc.core_properties.__dict__.clear()
        doc.save(output_path)
    elif ext == 'xlsx':
        wb = openpyxl.load_workbook(file_path)
        wb.properties = None
        wb.save(output_path)
    elif ext == 'md':
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        cleaned_lines = [line for line in lines if not line.startswith("---")]
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
    else:
        shutil.copy(file_path, output_path)
    print(f"Metadata removed from {file_path} -> {output_path}")
def process_files(input_path, output_folder, display, secure, overwrite_times, overwrite_original):
    files = [os.path.join(root, file) for root, _, files in os.walk(input_path) for file in files] if os.path.isdir(input_path) else [input_path]
    with tqdm(total=len(files), desc="Processing files", unit="file", dynamic_ncols=True, leave=True, bar_format="Processing files: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}") as pbar:
        for file_path in files:
            output_path = os.path.join(output_folder, os.path.basename(file_path))
            if display:
                display_metadata(file_path)
            elif secure:
                secure_remove_metadata(file_path, output_path, overwrite_times)
            elif overwrite_original:
                overwrite_metadata(file_path, overwrite_times)
            else:
                remove_metadata(file_path, output_path)
            pbar.update(1)
def main():
    parser = argparse.ArgumentParser(description="Remove or display metadata from files.")
    parser.add_argument("input", nargs="?", help="Input file path or directory")
    parser.add_argument("--display", action="store_true", help="Display metadata instead of removing it")
    parser.add_argument("--secure", action="store_true", help="Securely overwrite metadata multiple times (creates new file in no_meta folder)")
    parser.add_argument("--ow-times", type=int, default=3, help="Number of times to overwrite metadata (default: 3)")
    parser.add_argument("--owrite", action="store_true", help="Overwrite metadata on the original file (3 times by default)")
    parser.add_argument("--info", action="store_true", help="Show program usage information")
    args = parser.parse_args()

    # If --info is provided, show usage details and exit
    if args.info:
        print("""
        Metadata Cleaner Tool
        ---------------------
        Usage:
        - Display metadata: python pipewipe.py <file_or_folder> --display
        - Remove metadata (default): python pipewipe.py <file_or_folder>
        - Secure overwrite (creates new file): python pipewipe.py <file_or_folder> --secure
        - Set overwrite iterations: python pipewipe.py <file_or_folder> --secure --ow-times N
        - Overwrite original file: python pipewipe.py <file_or_folder> --owrite
        - Overwrite original file with custom iterations: python pipewipe.py <file_or_folder> --owrite --ow-times N

        Supported File Types:
        ---------------------
        | Category   | Extensions                  |
        |------------|-----------------------------|
        | Images     | jpg, png, tiff              |
        | Audio      | mp3, flac, mp4, m4a         |
        | PDF        | pdf                         |
        | Video      | mp4, mkv, avi, mov          |
        | Documents  | docx, xlsx, md              |
        """)
        return


    # Ensure input is provided unless --info was used
    if not args.input:
        parser.print_help()
        return

    output_folder = os.path.join(os.getcwd(), "no_meta")
    os.makedirs(output_folder, exist_ok=True)

    process_files(args.input, output_folder, args.display, args.secure, args.ow_times, args.owrite)

if __name__ == "__main__":
    main()
