import os

from datetime import datetime, timezone
from pathlib import Path
from shutil import copy as shutil_copy
from typing import List

SOURCES = [
    "/my/source/dir"
]

DESTINATION = "/my/destination/dir"


def get_target_path(destination, entry) -> str:
    stat = entry.stat()
    ts = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)

    return os.path.join(destination, ts.strftime("%Y"), ts.strftime("%m"), ts.strftime("%d"))


def main(paths: List[str], destination: str) -> None:
    path_to_existed = {}

    total = 0

    for i, path in enumerate(paths):
        files_count = 0
        dirs_count = 0

        for entry in os.scandir(path):
            if entry.is_dir():
                dirs_count += 1
            else:
                files_count += 1

        print(f"{datetime.now()} Processing {i + 1}/{len(paths)} directory '{path}' with {files_count} files and {dirs_count} dirs")

        total += files_count

        for j, entry in enumerate(os.scandir(path)):
            print(f"{j + 1}/{files_count + dirs_count}")

            if entry.is_dir():
                paths.append(entry.path)
                continue
            
            target = get_target_path(destination, entry)
            target_with_name = os.path.join(target, entry.name)

            if target not in path_to_existed:
                path_to_existed[target] = True
                Path(target).mkdir(parents=True, exist_ok=True)
            else:
                if os.path.isfile(target_with_name):
                    # already exists, skip
                    continue

            source = os.path.join(path, entry.name)

            shutil_copy(source, target_with_name)

    print(f"{datetime.now()} Processed {total} files")


if __name__ == '__main__':
    print(f"START {datetime.now()}")
    main(paths=SOURCES, destination=DESTINATION)
    print(f"END {datetime.now()}")
