import os
from abc import ABC, abstractmethod
from typing import Literal

from ._constants import BACKUP_DIR


class BackupRepo(ABC):
    """
    Abstract class for backup repositories.
    """

    @abstractmethod
    def __init__(self, name: str, overwrite: bool = False): ...

    @abstractmethod
    def backup(self, source: str, tag: str): ...

    @abstractmethod
    def restore(self, tag: str, target: str): ...

    @abstractmethod
    def size(self, mode: Literal["raw-data", "restore-size"] = "raw-data") -> str: ...

    @abstractmethod
    def snapshots(self) -> list[str]: ...
