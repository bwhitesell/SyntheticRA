from dataclasses import dataclass
import re
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import GloVe
from torchtext.vocab import Vocab
import torch
from typing import List, Union

from synthetic_ra.data.constants import PAD_TOKEN


tokenizer = get_tokenizer('basic_english')


@dataclass(frozen=True)
class RAPostTitle:

    title_text: str
    fixed_encoded_len: int = 100

    def encoded_title(self, vocab: Union[Vocab, GloVe]) -> torch.Tensor:
        """
            Returns a fully encoded, clamped integer representation of the
            title given the passed vocab mapping.
        """

        full_encoded_title: List[int] = [
            vocab.stoi[x] for x in self.tokenized_title_text
        ]

        clamped_encoded_title: List[int] = (
            full_encoded_title[:(self.fixed_encoded_len - 1)]
        )

        clamped_encoded_title += (
            [vocab.stoi[PAD_TOKEN]] * (self.fixed_encoded_len - len(clamped_encoded_title))
        )

        return torch.tensor(clamped_encoded_title, dtype=torch.long)

    @property
    def cleaned_title_text(self) -> str:
        """ Title post text processing to clarify/simplify the content. """

        title: str = self.title_text.lower()
        # the informal RA syntax treats brackets and parens identically.
        title: str = title.replace('[', '(').replace(']', ')')
        # separate sequences of numerical tokens with spaces for tokenizer.
        title: str = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", title)
        return title

    @property
    def tokenized_title_text(self) -> List[str]:
        """ Apply a tokenizer to cleaned title text. """

        return tokenizer(self.cleaned_title_text)
