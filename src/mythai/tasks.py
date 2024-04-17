import argparse
import os
import pathlib
import time

import platformdirs
import requests
import yaml

CACHE_DURATION = 600  # 10 minutes in seconds
APPNAME = "mythai"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract task headers from a Taskfile."
    )
    parser.add_argument("-p", "--path", help="Path to the local Taskfile.yaml")
    return parser.parse_args()


def load_cached_taskfile():
    cache_dir = pathlib.Path(platformdirs.user_cache_dir(APPNAME))

    cache_file = cache_dir / "taskfile.yaml"

    if cache_file.exists():
        cache_age = time.time() - os.path.getmtime(cache_file)
        if cache_age < CACHE_DURATION:
            with open(cache_file, "r") as file:
                return yaml.safe_load(file)

    return None


def save_cached_taskfile(taskfile):
    cache_dir = platformdirs.user_cache_dir(APPNAME)
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "taskfile.yaml")

    with open(cache_file, "w") as file:
        yaml.dump(taskfile, file)


def fetch_taskfile():
    cached_taskfile = load_cached_taskfile()
    if cached_taskfile:
        return cached_taskfile

    url = (
        "https://raw.githubusercontent.com/taylormonacelli/ringgem/master/Taskfile.yaml"
    )
    response = requests.get(url)
    response.raise_for_status()
    taskfile = yaml.safe_load(response.text)

    save_cached_taskfile(taskfile)
    return taskfile


def main():
    taskfile = fetch_taskfile()

    task_headers = []
    for task_name, task_data in taskfile["tasks"].items():
        task_headers.append(task_name)

    return task_headers


if __name__ == "__main__":
    main()
