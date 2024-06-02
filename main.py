import os

from datetime import datetime, timezone
from pathlib import Path
from shutil import copy as shutil_copy
from typing import List

SOURCES = [
    "/my/source/dir"
]

DESTINATION = "sorted"


def get_target_path(destination, entry) -> str:
    stat = entry.stat()
    ts = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
    return os.path.join(destination, ts.strftime("%Y"), ts.strftime("%m"), ts.strftime("%d"))


def printdt(content: str) -> None:
    print(f"{datetime.now()}: {content}")


def main(paths: List[str], destination: str) -> None:
    path_to_existed = {}
    path_to_failed = {}

    total = 0

    for i, path in enumerate(paths):
        files_count = 0
        dirs_count = 0

        for entry in os.scandir(path):
            if entry.is_dir():
                dirs_count += 1
            else:
                files_count += 1

        printdt(f"Processing {i + 1}/{len(paths)} dir '{path}' with {files_count} files and {dirs_count} dirs")

        total += files_count

        for j, entry in enumerate(os.scandir(path)):
            printdt(f"{j + 1}/{files_count + dirs_count}")

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

            try:
                shutil_copy(source, target_with_name)
            except OSError as e:
                if target not in path_to_failed:
                    path_to_failed[target] = []
                path_to_failed[target].append((source, e))
                try:
                    # clean up failed file
                    os.remove(target_with_name)
                except FileNotFoundError:
                    pass

    printdt(f"Processed {total} files")
    if len(path_to_failed) > 0:
        print("Some files have been failed to copy")
        for path, failed in path_to_failed.items():
            print(f"Failed copy to path {path}:")
            for f in failed:
                print(f[0], f[1])


if __name__ == '__main__':
    printdt("START")
    main(paths=SOURCES, destination=DESTINATION)
    printdt("END")
