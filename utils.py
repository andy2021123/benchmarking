from typing import Union
from git.util import RemoteProgress
from tqdm import tqdm


class Progress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.tqdm = tqdm(total=1, desc="Cloning")

    def update(
        self,
        op_code: int,
        cur_count: Union[str, float],
        max_count: Union[str, float, None] = None,
        message: str = "",
    ):
        if op_code == self.COUNTING:
            self.tqdm.desc = "Counting objects"
        elif op_code == self.COMPRESSING:
            self.tqdm.desc = "Compressing objects"
        elif op_code == self.WRITING:
            self.tqdm.desc = "Writing objects"
        elif op_code == self.RECEIVING:
            self.tqdm.desc = "Receiving objects"
        elif op_code == self.RESOLVING:
            self.tqdm.desc = "Resolving deltas"
        elif op_code == self.FINDING_SOURCES:
            self.tqdm.desc = "Finding sources"
        elif op_code == self.CHECKING_OUT:
            self.tqdm.desc = "Checking out files"

        if op_code == 1:
            self.tqdm.leave = False
            self.tqdm.close()
        else:
            self.tqdm.total = max_count
            self.tqdm.n = cur_count
            self.tqdm.refresh()
