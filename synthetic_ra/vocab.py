from collections import Counter
from pathlib import Path
import torch
from torchtext.vocab import GloVe
from torchtext.vocab import Vocab
from typing import List
from typing import Union

from synthetic_ra.data.constants import START_TOKEN
from synthetic_ra.data.constants import END_TOKEN
from synthetic_ra.data.constants import PAD_TOKEN
from synthetic_ra.data.titles import RAPostTitle


GLOVE_EMB_SIZE: int = 200


def xavier_init(tensor):
    torch.nn.init.xavier_uniform_(tensor.unsqueeze(0))
    return tensor.squeeze(0)


def build_vocab_w_glove_init_from_post_titles(
    titles: List[RAPostTitle],
    extra_tokens: List[str] = [START_TOKEN, END_TOKEN, PAD_TOKEN],
) -> GloVe:
    """
        Builds a vocabulary object from the provided post titles.
        Also provides an embedding initalization tensor for the token ids
        from GloVe.
    """

    counter: Counter = Counter()
    counter.update(extra_tokens)

    for title in titles:
        counter.update(title.tokenized_title_text)

    vocab: Vocab = Vocab(counter)

    glove_vecs: torch.Tensor = torch.zeros(len(vocab), GLOVE_EMB_SIZE)
    glove_vocab: GloVe = GloVe(
        name='6B',
        dim=GLOVE_EMB_SIZE,
        unk_init=xavier_init
    )

    for word in vocab.itos:
        glove_vecs[vocab.stoi[word]] = glove_vocab[word]

    return vocab, glove_vecs
