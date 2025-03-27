#!/usr/bin/env python3
import os

from src.mypackage.transforms.markdown_to_HTML import generate_page
from src.mypackage.utils.move_files import move_files

src_dir_current = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
overall_root = os.path.abspath(os.path.join(src_dir_current, ".."))

import sys
sys.path.insert(0, os.path.join(overall_root, "src"))

def generate_pages_recursive(content_dir: str, template_path: str, dest_dir: str) -> None:
    for entry in os.listdir(content_dir):
        entry_path = os.path.join(content_dir, entry)

        if os.path.isdir(entry_path):
            new_dest_dir = os.path.join(dest_dir, entry)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(entry_path, template_path, new_dest_dir)

        elif os.path.isfile(entry_path) and entry.lower().endswith(".md"):

            base_name = os.path.splitext(entry)[0]
            dest_file_path = os.path.join(dest_dir, base_name + ".html")
            generate_page(entry_path, template_path, dest_file_path)

def main() -> None:
    stc_dir         = os.path.join(overall_root, "static")
    pub_dir         = os.path.join(overall_root, "public")
    cot_dir         = os.path.join(overall_root, "content")
    stc_cnt_tmp     = os.path.join(overall_root, "static", "template.html")

    
    move_files(stc_dir, pub_dir)

    generate_pages_recursive(cot_dir, stc_cnt_tmp, pub_dir)

if __name__ == "__main__":
    main()

