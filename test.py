from itertools import islice
import os

from tqdm import tqdm
from benchmarking.repositories import GitRepo, ResticRepo, KopiaRepo

# initialize the Git repository and backup repositories
git = GitRepo("https://github.com/git/git")
restic = ResticRepo(git.name, overwrite=True)
kopia = KopiaRepo(git.name, overwrite=True)

git.checkout("master")
commits = list(git.iter_commits())
commits.reverse()

print("Iterating through commits...")
for commit in tqdm(commits[:5], desc="Backing up data"):

    # checkout the commit
    git.checkout(commit)

    # backup using restic
    restic.backup(git.path, commit.hexsha)

    # backup using kopia
    with kopia:
        kopia.backup(git.path, commit.hexsha)

git.checkout("master")

print("Iterating through commits...")
for commit in tqdm(commits[:5], desc="Restoring data"):
    restic.restore(commit.hexsha, f"./data/restores/restic/{git.name}")
    with kopia:
        kopia.restore(commit.hexsha, f"./data/restores/kopia/{git.name}")
