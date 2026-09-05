import unittest

import torch

from minigpt.config import Config
from minigpt.model import GPT


class TrainingTests(unittest.TestCase):
    def test_model_can_overfit_one_batch(self):
        """If it cannot memorise 4 sequences, the training wiring is broken."""
        cfg = Config(vocab_size=65, block_size=8, n_layer=2, n_head=2,
                     n_embd=32, dropout=0.0, device="cpu")
        torch.manual_seed(0)
        model = GPT(cfg)
        x = torch.randint(0, cfg.vocab_size, (4, 8))
        y = torch.randint(0, cfg.vocab_size, (4, 8))

        opt = torch.optim.AdamW(model.parameters(), lr=1e-2)
        first = model(x, y)[1].item()
        for _ in range(200):
            loss = model(x, y)[1]
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
        self.assertLess(loss.item(), first / 4)


if __name__ == "__main__":
    unittest.main()
