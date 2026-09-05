import math
import unittest

import torch

from minigpt.config import Config
from minigpt.model import GPT


def tiny():
    return Config(vocab_size=65, block_size=8, n_layer=2,
                  n_head=2, n_embd=32, dropout=0.0, device="cpu")


class ModelTests(unittest.TestCase):
    def test_output_shape(self):
        cfg = tiny()
        logits, _ = GPT(cfg)(torch.randint(0, cfg.vocab_size, (4, 8)))
        self.assertEqual(tuple(logits.shape), (4, 8, cfg.vocab_size))

    def test_loss_at_init_is_uniform(self):
        cfg = tiny()
        torch.manual_seed(0)
        x = torch.randint(0, cfg.vocab_size, (16, 8))
        y = torch.randint(0, cfg.vocab_size, (16, 8))
        _, loss = GPT(cfg)(x, y)
        self.assertAlmostEqual(loss.item(), math.log(cfg.vocab_size), delta=0.15)

    def test_attention_is_causal(self):
        cfg = tiny()
        torch.manual_seed(0)
        model = GPT(cfg).eval()
        a = torch.randint(0, cfg.vocab_size, (1, 8))
        b = a.clone()
        b[0, -1] = (b[0, -1] + 1) % cfg.vocab_size          # edit the future only
        with torch.no_grad():
            self.assertTrue(torch.equal(model(a)[0][:, :-1], model(b)[0][:, :-1]))

    def test_generate_respects_block_size(self):
        cfg = tiny()
        model = GPT(cfg).eval()
        out = model.generate(torch.zeros((1, 1), dtype=torch.long), 30)
        self.assertEqual(tuple(out.shape), (1, 31))


if __name__ == "__main__":
    unittest.main()
