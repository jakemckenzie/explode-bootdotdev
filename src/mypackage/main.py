import os
import shutil
from typing import List

def copy_recursive_func(src: str, dst: str) -> None:

    if not os.path.exists(dst):
        os.mkdir(dst)
    
    items: List[str] = os.listdir(src)
    
    def copy_item(item: str) -> None:
        s_item: str = os.path.join(src, item)
        d_item: str = os.path.join(dst, item)
        if os.path.isdir(s_item):
            print(f"Copying directory: {s_item}")
            os.mkdir(d_item)

            copy_recursive_func(s_item, d_item)
        else:
            print(f"Copying file: {s_item}")
            shutil.copy(s_item, d_item)
    
    list(map(copy_item, items))

def main() -> None:
    src_dir = "static"
    dst_dir = "public"

    if os.path.exists(dst_dir):
        print(f"Deleting existing directory: {dst_dir}")
        shutil.rmtree(dst_dir)
    
    os.mkdir(dst_dir)

    copy_recursive_func(src_dir, dst_dir)
    print("Copy complete!")

if __name__ == "__main__":
    main()