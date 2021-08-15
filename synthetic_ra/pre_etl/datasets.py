import torch
from torch.utils.data import Dataset
from torchtext.vocab import GloVe
from torchtext.vocab import Vocab
from typing import List
from typing import Tuple
from typing import Union

from synthetic_ra.data.titles import RAPostTitle


class RATitleDataset(Dataset):

    def __init__(
        self,
        ra_titles: List[RAPostTitle],
        vocab: Union[Vocab, GloVe],
    ) -> None:

        self._ra_titles: List[RAPostTitle] = ra_titles
        self._vocab: Union[Vocab, GloVe] = vocab

    def __len__(self) -> int:
        return len(self._ra_titles)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor]:

        title: RAPostTitle = self._ra_titles[idx]
        encoded_title: torch.Tensor = title.encoded_title

        return encoded_title[:-1], encoded_title[1:]
