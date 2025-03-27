

import os
import shutil
from typing import List


def move_files(src: str, dst: str) -> None:
    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.mkdir(dst)

    items: List[str] = os.listdir(src)

    def copy_item(item: str) -> None:
        s_item: str = os.path.join(src, item)
        d_item: str = os.path.join(dst, item)

        if os.path.abspath(s_item) == os.path.abspath(dst):
            return

        if os.path.isdir(s_item):
            move_files(s_item, d_item)
        else:
            shutil.copy(s_item, d_item)

    list(map(copy_item, items))