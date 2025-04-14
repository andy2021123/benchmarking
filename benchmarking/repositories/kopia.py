import os
import shutil
import subprocess
from typing import Literal

from .backup import BackupRepo
from ._constants import BACKUP_DIR


class KopiaRepo(BackupRepo):
    def __init__(self, name: str, overwrite: bool = False):
        self.path = os.path.abspath(os.path.join(BACKUP_DIR, "kopia", name))
        self._cmd_prefix = ["kopia", "--no-progress"]
        if overwrite and os.path.exists(self.path):
            shutil.rmtree(self.path)
        if overwrite or not os.path.exists(os.path.join(self.path, "config.json")):
            # Initialize repository with default settings (encryption and compression)
            subprocess.run(
                [
                    *self._cmd_prefix,
                    "repository",
                    "create",
                    "filesystem",
                    "--path",
                    self.path,
                    "--password",
                    "default",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            with self:
                subprocess.run(
                    [
                        *self._cmd_prefix,
                        "policy",
                        "set",
                        "--global",
                        "--add-ignore",
                        ".git",
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

    def __enter__(self):
        # Connect to the repository
        subprocess.run(
            [
                *self._cmd_prefix,
                "repository",
                "connect",
                "filesystem",
                "--path",
                self.path,
                "--password",
                "default",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Disconnect from repository
        subprocess.run(
            [
                *self._cmd_prefix,
                "repository",
                "disconnect",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def backup(self, source: str, tag: str):
        subprocess.run(
            [*self._cmd_prefix, "snapshot", "create", "--tags", f"git:{tag}", source],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def restore(self, tag: str, target: str):
        # First find the snapshot with the given tag
        result = subprocess.run(
            [*self._cmd_prefix, "snapshot", "list", "--tags", f"git:{tag}"],
            capture_output=True,
            text=True,
        )
        # Assuming the first snapshot with the matching tag is wanted
        # A more robust implementation would parse the JSON response properly
        snapshot_id = result.stdout.strip().split(" ")[5]

        subprocess.run(
            [*self._cmd_prefix, "snapshot", "restore", snapshot_id, target],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def size(self, mode: Literal["raw-data", "restore-size"] = "raw-data") -> str:
        # Kopia doesn't have the same modes as restic,
        # but we can get repository size stats
        result = subprocess.run(
            [*self._cmd_prefix, "content", "stats"],
            capture_output=True,
            text=True,
        )

        lines = result.stdout.splitlines()
        for line in lines:
            if mode == "raw-data" and "Original Size" in line:
                return line.split(":")[1].strip()
            elif mode == "restore-size" and "Total Size" in line:
                return line.split(":")[1].strip()

        raise AttributeError("Size not found in kopia stats output")

    def snapshots(self):
        subprocess.run([*self._cmd_prefix, "snapshot", "list"])
