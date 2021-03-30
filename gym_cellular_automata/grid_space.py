from operator import mul
from functools import reduce

import numpy as np
from gym.spaces import Space


class Grid(Space):
    r"""
    A Space for Cellular Automata Lattices.
    Arbitrary integers can be used as cell states.

    Example::

        >>> Grid(n=3, shape=(2, 2))
        >>> Grid(values=[-1, 0, 1], shape=(2,2))

    """

    def __init__(self, n=None, values=None, shape=None, probs=None, dtype=np.int32):

        assert shape is not None, "'shape' must be a non-empty tuple."
        assert n is not None or values is not None, "'n' or 'values' must be provided."

        super().__init__(shape, dtype)

        if values is not None:
            self._from_values = True

            self.values = np.unique(np.array(values, dtype=dtype))
            self.n = len(self.values)

        else:
            self._from_values = False

            assert n > 0, "'n' must be a positive integer."
            self.n = n

            self.values = np.arange(self.n, dtype=dtype)

        uniform = np.repeat(1.0, self.n) / self.n
        self.probs = uniform if probs is None else probs

        self.size = reduce(mul, self.shape)

    def sample(self):

        return np.random.choice(self.values, self.size, p=self.probs).reshape(
            self.shape
        )

    def contains(self, x):

        if isinstance(x, list):
            x = np.array(x, dtype=self.dtype)

        return set(np.unique(x)).issubset(set(self.values)) and self.shape == x.shape

    def __repr__(self):
        if self._from_values:

            return f"Grid(values={self.values}, shape={self.shape})"

        else:

            return f"Grid(n={self.n}, shape={self.shape})"

    def __eq__(self, other):
        return (
            isinstance(other, Grid)
            and (self.shape == other.shape)
            and np.all(self.values == other.values)
        )