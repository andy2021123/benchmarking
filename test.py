from itertools import islice
from repository import GitRepo, ResticRepo

git = GitRepo("https://github.com/git/git")
restic = ResticRepo(git.name)

commits = reversed(list(git.iter_commits()))
for commit in islice(commits, 100):
    print(f"Backing up commit '{commit.hexsha}'")
    git.checkout(commit)
    restic.backup(
        source=git.path,
        tag=commit.hexsha,
    )

print(" restore size:", restic.size("restore-size"))
print("raw data size:", restic.size("raw-data"))
