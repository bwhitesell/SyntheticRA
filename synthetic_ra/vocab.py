from collections import Counter
import torch
from typing import List
from torchtext.vocab import GloVe
from torchtext.vocab import Vocab

from synthetic_ra.data.constants import START_TOKEN
from synthetic_ra.data.constants import END_TOKEN
from synthetic_ra.data.constants import PAD_TOKEN
from synthetic_ra.data.titles import RAPostTitle


GLOVE_EMB_SIZE: int = 200


def load_glove_vocab(
    extra_tokens: List[str] = [START_TOKEN, END_TOKEN, PAD_TOKEN],
) -> GloVe:

    glove_vocab: GloVe = GloVe(name='6B', dim=GLOVE_EMB_SIZE)

    # add our extra tokens in.
    for token in extra_tokens:
        with torch.no_grad():
            glove_vocab.stoi[token] = len(glove_vocab.itos)
            glove_vocab.itos.append(token)
            glove_vocab.vectors: torch.Tensor = torch.cat(
                (
                    glove_vocab.vectors,
                    torch.nn.Embedding(1, GLOVE_EMB_SIZE).weight,
                ),
                axis=0,
            )

    return glove_vocab
