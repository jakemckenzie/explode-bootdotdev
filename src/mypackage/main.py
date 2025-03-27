#!/usr/bin/env python3
import os

from src.mypackage.transforms.markdown_to_HTML import generate_page
from src.mypackage.utils.move_files import move_files

src_dir_current = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
overall_root = os.path.abspath(os.path.join(src_dir_current, ".."))

import sys
sys.path.insert(0, os.path.join(overall_root, "src"))

def main() -> None:
    stc_dir         = os.path.join(overall_root, "static")
    pub_dir         = os.path.join(overall_root, "public")
    stc_cnt_tmp     = os.path.join(overall_root, "static", "template.html")
    stc_ctn_ind     = os.path.join(overall_root, "static", "content", "index.md")
    pub_ctn_ind     = os.path.join(pub_dir, "index.html")
    
    move_files(stc_dir, pub_dir)

    generate_page(
        stc_ctn_ind,
        stc_cnt_tmp,
        pub_ctn_ind
    )

if __name__ == "__main__":
    main()

