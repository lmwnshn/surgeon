import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

# curl "https://api.github.com/repos/postgres/postgres/tags" > pg_tags.json

def main():
    PG_PATH = Path("/mnt/nvme1n1/wanshenl/git/postgres/")
    WORKDIR_PATH = os.getcwd()

    with open("pg_tags.json", "r") as f:
        raw_tags = json.load(f)

    # GitHub tags are incomplete.
    raw_tags.append({
        "name": "PG95-1_01",
        "commit": {
            "sha": "d31084e9d1118b25fd16580d9d8c2924b5740dff",
        }
    })
    
    tags = []
    for tag in raw_tags:
        tag_name = tag["name"]
        tag_commit_sha = tag["commit"]["sha"]
        os.chdir(PG_PATH)
        proc = subprocess.run(["git", "show", "--no-patch", r"--format=%ci", tag_commit_sha], capture_output=True)
        os.chdir(WORKDIR_PATH)
        tag_date = proc.stdout.decode().strip()
        tag_date = datetime.strptime(tag_date, "%Y-%m-%d %H:%M:%S %z")
        tags.append((tag_name, tag_commit_sha, tag_date))
    tags.sort(key=lambda x: x[2])

    for i in range(len(tags) - 1):
        tag_name, tag_commit_sha, tag_date = tags[i]
        next_tag_name, next_tag_commit_sha, next_tag_date = tags[i + 1]
        
        os.chdir(PG_PATH)
        proc = subprocess.run(["git", "log", f"{tag_commit_sha}..{next_tag_commit_sha}"], capture_output=True)
        os.chdir(WORKDIR_PATH)
        commit_log = proc.stdout.decode().strip()
        tag_date_str = datetime.strftime(tag_date, "%Y-%m-%d")
        next_tag_date_str = datetime.strftime(next_tag_date, "%Y-%m-%d")
        folder = Path("commits")
        folder.mkdir(exist_ok=True)
        with open(folder / f"{next_tag_date_str}_{next_tag_name}_commits.txt", "w") as f:
            print(
                f"This is a list of commits from tag '{tag_name}' to tag '{next_tag_name}', "
                f"ranging from {tag_date_str} to {next_tag_date_str}.\n",
                file=f
            )
            print(commit_log, file=f)

if __name__ == "__main__":
    main()