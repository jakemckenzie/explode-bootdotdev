#!/usr/bin/env python3
import os
import sys

basepath: str = sys.argv[1] if len(sys.argv) > 1 else "/"

# Set the project root (parent directory of src)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Insert the project root into sys.path so that Python finds the mypackage module
sys.path.insert(0, project_root)

# Corrected imports without the leading 'src.'
from mypackage.transforms.markdown_to_HTML import generate_pages_recursive
from mypackage.utils.move_files import move_files

def main() -> None:
    stc_dir     = os.path.join(project_root, "static")
    pub_dir     = os.path.join(project_root, "docs")
    cot_dir     = os.path.join(pub_dir, "content")
    stc_cnt_tmp = os.path.join(project_root, "static", "template.html")
    
    move_files(stc_dir, pub_dir)
    generate_pages_recursive(cot_dir, stc_cnt_tmp, pub_dir, basepath)

if __name__ == "__main__":
    main()
