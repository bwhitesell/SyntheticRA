import transformers
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
        encoded_title: torch.Tensor = title.encoded_title(self._vocab)

        return encoded_title[:-1], encoded_title[1:]



class GPTRATitleDataset(Dataset):

    def __init__(
        self,
        ra_titles: List[RAPostTitle],
    ) -> None:

    self._ra_titles: List[RAPostTitle] = ra_titles
    self._tokenizer = transformers.AutoTokenizer.from_pretrained(
        'gpt2',
        pad_token='<pad>'
    )

    def __len__(self) -> int:
        return len(self._ra_titles)

    def __getitem__(self, idx: int):
        
        title: RAPostTitle = self.ra_titles[idx]

        gpt_encoded_title = self._tokenizer.encode_plus(
            title.cleaned_title_text,
            None,
            add_special_tokens=True,
            max_length=100,
            padding='max_length',
            trunctation=True,
        )
