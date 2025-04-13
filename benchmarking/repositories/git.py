import os

from git import Reference, Repo
from ..utils import Progress
from ._constants import GIT_DIR


class GitRepo:
    def __init__(self, url: str):
        self.name = os.path.basename(url)
        self.path = os.path.join(GIT_DIR, self.name)
        if os.path.exists(os.path.join(self.path, ".git")):
            self.repo = Repo(self.path)
        else:
            print("Cloning git repository...")
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
