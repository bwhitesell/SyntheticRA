import random
import numpy as np
import torch
from torch.distributions import Categorical
from torch.nn.functional import softmax
from typing import List, Tuple

from synthetic_ra.modeling.layers import TFEncoder
from synthetic_ra.constants import DEVICE


class SmallEncoderDecoder(torch.nn.Module):

    def __init__(
        self,
        n_tokens: int,
        emb_size: int,
        n_heads: int,
        ff_size: int,
        n_layers: int,
        do: float = 0.1
    ) -> None:

        super(SmallEncoderDecoder, self).__init__()

        # define encoder
        self.tf_encoder = TFEncoder(
            n_tokens,
            emb_size,
            n_heads,
            ff_size,
            n_layers,
            do,
        ).to(DEVICE)

        # define decoder
        self.linear_decoder = torch.nn.Linear(emb_size, n_tokens).to(DEVICE)

    def forward(self, input) -> torch.Tensor:
        # encode input
        hidden_state = self.tf_encoder(input)
        # decode encoded reprs
        return self.linear_decoder(hidden_state)
