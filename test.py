from itertools import islice

from tqdm import tqdm
from benchmarking.repositories import GitRepo, ResticRepo

# initialize the Git repository and backup repositories
git = GitRepo("https://github.com/git/git")
restic = ResticRepo(git.name, overwrite=True)

print("Iterating through commits...")
commits = reversed(list(git.iter_commits()))
for commit in tqdm(islice(commits, 10), total=10):

    # checkout the commit
    git.checkout(commit)

    # backup using restic
    restic.backup(
        source=git.path,
        tag=commit.hexsha,
    )

git.checkout("master")
