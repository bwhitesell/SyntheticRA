import math
import torch
from torch.nn import TransformerEncoder, TransformerEncoderLayer


class PositionalEncoding(torch.nn.Module):
    """
        An  additive operation that injects positional information into an
        existing embedding space.
    """

    def __init__(self, emb_len: int, dropout: float = 0.1, max_len: int = 5000):
        super(PositionalEncoding, self).__init__()

        self.dropout = torch.nn.Dropout(p=dropout)

        # initalize positional embeddings with zero weights and full shape.
        positional_embeddings: torch.Tensor = torch.zeros(
            max_len,
            emb_len,
        )

        position: torch.Tensor = torch.arange(
            0,
            max_len,
            dtype=torch.float
        ).unsqueeze(1)

        div_scale: torch.tensor = torch.exp(
            torch.arange(0, emb_len, 2).float() * (-math.log(10000.0) / emb_len)
        )

        # map the weights to their proper positional embedding
        positional_embeddings[:, 0::2] = torch.sin(position * div_scale)
        positional_embeddings[:, 1::2] = torch.cos(position * div_scale)
        positional_embeddings = positional_embeddings.unsqueeze(0).transpose(
            0,
            1,
        )
        self.register_buffer('positional_embeddings', positional_embeddings)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.positional_embeddings[:x.size(0), :]
        return self.dropout(x)


class TFEncoder(torch.nn.Module):
    """
        A complete transformer-based encoding network to contextually embed
        sequence data.
    """

    def __init__(
        self,
        n_tokens: int,
        emb_size: int,
        n_heads: int,
        ff_size: int,
        n_layers: int,
        do: float = 0.1
    ) -> None:

        super(TFEncoder, self).__init__()

        self.n_tokens = n_tokens
        self.emb_size = emb_size
        self.n_heads = n_heads
        self.ff_size = ff_size
        self.n_layers = n_layers
        self.do = do

        self.seq_embeddings = torch.nn.Embedding(self.n_tokens, self.emb_size)
        self.pos_encoder = PositionalEncoding(self.emb_size, self.do)
        self.transformer_encoder = TransformerEncoder(
            self.encoder_layers,
            self.n_layers
        )

    def forward(self, x):
        mask = self._generate_square_subsequent_mask(x.shape[0], x.device)

        x = self.seq_embeddings(x) * math.sqrt(self.emb_size)
        x = self.pos_encoder(x)
        output = self.transformer_encoder(x, mask)
        return output

    @property
    def encoder_layers(self) -> TransformerEncoderLayer:
        return TransformerEncoderLayer(
            self.emb_size,
            self.n_heads,
            self.ff_size,
            self.do
        )

    def _generate_square_subsequent_mask(self, sz, device) -> torch.Tensor:
        """ Generates a mask to disable lookahead contextualization. """

        mask: torch.Tensor = (
            torch.triu(torch.ones(sz, sz, device=device)) == 1
        ).transpose(0, 1)
        mask: torch.Tensor = mask.float().masked_fill(
            mask == 0, float('-inf')
        ).masked_fill(
            mask == 1, float(0.0)
        )

        return mask
