import os
import shutil
import json
import logging
import argparse

with open("rules.json", encoding="utf-8") as f:
    rules = json.load(f)

logging.basicConfig(
    filename="sort.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    encoding="utf-8"
)

parser = argparse.ArgumentParser(description="Сортировщик файлов")
parser.add_argument("--src", required=True, help="откуда брать файлы")
parser.add_argument("--dst", required=True, help="куда складывать")
args = parser.parse_args()

download_folder = args.src
storage_folder = args.dst
items = os.listdir(download_folder)

for item in items:
    full_path = os.path.join(download_folder, item)

    if not os.path.isfile(full_path):
        continue

    ext = "." + item.split(".")[-1].lower()
    item_folder = rules.get(ext, "Other")

    dest_folder = os.path.join(storage_folder, item_folder)
    os.makedirs(dest_folder, exist_ok=True)

    dest_path = os.path.join(dest_folder, item)

    if os.path.exists(dest_path):
        name, ext_part = os.path.splitext(item)
        dest_path = os.path.join(dest_folder, name + "_new" + ext_part)

    shutil.move(full_path, dest_path)
    logging.info(f"{full_path} -> {dest_path}")