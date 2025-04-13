import os
import shutil
import subprocess
from typing import Literal

from .backup import BackupRepo

from ._constants import BACKUP_DIR


class ResticRepo(BackupRepo):
    def __init__(self, name: str, overwrite: bool = False):
        self.path = os.path.abspath(os.path.join(BACKUP_DIR, "restic", name))
        self._cmd_prefix = [
            "restic",
            "--repo",
            self.path,
            "--insecure-no-password",
            "--quiet",
        ]
        if overwrite:
            shutil.rmtree(self.path)
        if not os.path.exists(self.path):
            subprocess.run([*self._cmd_prefix, "init"])
        else:
            subprocess.run([*self._cmd_prefix, "check"])

    def backup(self, source: str, tag: str):
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

    def snapshots(self):
        subprocess.run([*self._cmd_prefix, "snapshots"])
