import os
import subprocess
from typing import Literal

from git import Reference, Repo
from utils import Progress

# constants
BASE_DIR = "./data"
GIT_DIR = os.path.join(BASE_DIR, "repositories")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")


class GitRepo:
    def __init__(self, url: str):
        self.name = os.path.basename(url)
        self.path = os.path.abspath(os.path.join(GIT_DIR, self.name))
        if os.path.exists(os.path.join(self.path, ".git")):
            self.repo = Repo(self.path)
        else:
            self.repo = Repo.clone_from(
                url,
                self.path,
                progress=Progress(),
            )

    def checkout(self, reference: Reference):
        self.repo.git.checkout(reference)

    def iter_commits(self, *args, **kwargs):
        for commit in self.repo.iter_commits(*args, **kwargs):
            yield commit


class ResticRepo:
    def __init__(self, name: str):
        self.path = os.path.join(BACKUP_DIR, "restic", name)
        self._cmd_prefix = [
            "restic",
            "--repo",
            self.path,
            "--insecure-no-password",
            "--quiet",
        ]
        if not os.path.exists(self.path):
            subprocess.run([*self._cmd_prefix, "init"])
        else:
            subprocess.run([*self._cmd_prefix, "check"])

    def backup(self, source: str, tag: str = None):
        subprocess.run(
            [
                *self._cmd_prefix,
                "backup",
                "--tag",
                tag,
                "--exclude",
                ".git",
                source,
            ]
        )

    def restore(self, tag: str, target: str):
        subprocess.run(
            [
                *self._cmd_prefix,
                "restore",
                "--target",
                target,
                "--tag",
                tag,
                "latest",
            ]
        )

    def size(self, mode: Literal["raw-data", "restore-size"] = "raw-data") -> str:
        result = subprocess.run(
            [
                *self._cmd_prefix,
                "stats",
                "--mode",
                mode,
            ],
            capture_output=True,
            text=True,
        )
        lines = result.stdout.splitlines()
        for line in lines:
            if "Total Size" in line:
                return line.split(":")[1].strip()

        raise AttributeError("Size not found in restic stats output")
