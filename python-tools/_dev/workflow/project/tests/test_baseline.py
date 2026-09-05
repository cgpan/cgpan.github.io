import math
import unittest

import numpy as np

from minigpt.baseline import CountBigram


class BaselineTests(unittest.TestCase):
    def test_untrained_model_is_uniform(self):
        model = CountBigram(vocab_size=5)
        self.assertAlmostEqual(model.nll([0, 1, 2, 3]), math.log(5), places=6)

    def test_rows_are_probability_distributions(self):
        model = CountBigram(vocab_size=4).fit([0, 1, 1, 2, 3, 0])
        np.testing.assert_allclose(model.probs.sum(axis=1), 1.0)

    def test_fitting_lowers_the_loss(self):
        ids = [0, 1] * 50
        model = CountBigram(vocab_size=2)
        before = model.nll(ids)
        after = model.fit(ids).nll(ids)
        self.assertLess(after, before)


if __name__ == "__main__":
    unittest.main()
