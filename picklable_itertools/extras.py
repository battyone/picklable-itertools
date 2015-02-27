"""Related things that aren't part of the standard library's `itertools`.

Currently home to picklable reimplementations of a few of the generators
from Matthew Rocklin's `toolz` package.
"""
import six
from .base import BaseItertool
from .iter_dispatch import _iter


class partition(BaseItertool):
    """Partition sequence into tuples of length n

    >>> list(partition(2, [1, 2, 3, 4]))
    [(1, 2), (3, 4)]

    If length of `seq` is not evenly divisible by `n`, the final
    tuple is dropped if `pad` is not specified, or filled to length
    `n` by `pad`:

    >>> list(partition(2, [1, 2, 3, 4, 5]))
    [(1, 2), (3, 4)]

    >>> list(partition(2, [1, 2, 3, 4, 5], pad=None))
    [(1, 2), (3, 4), (5, None)]

    See Also:
        partition_all
    """
    _NO_PAD = '__no_pad__'

    def __init__(self, n, seq, pad=_NO_PAD):
        self._n = n
        self._partition_all = partition_all(n, seq)
        self._pad = pad

    def __next__(self):
        items = next(self._partition_all)
        if len(items) < self._n:
            if self._pad != self._NO_PAD:
                items += (self._pad,) * (self._n - len(items))
            else:
                raise StopIteration
        return items


class partition_all(BaseItertool):
    """Partition all elements of sequence into tuples of length at most n

    The final tuple may be shorter to accommodate extra elements.

    >>> list(partition_all(2, [1, 2, 3, 4]))
    [(1, 2), (3, 4)]
    >>> list(partition_all(2, [1, 2, 3, 4, 5]))
    [(1, 2), (3, 4), (5,)]

    See Also:
        partition
    """
    def __init__(self, n, seq):
        self._n = n
        self._seq = _iter(seq)

    def __next__(self):
        items = []
        try:
            for i in six.moves.xrange(self._n):
                items.append(next(self._seq))
        except StopIteration:
            pass
        if len(items) == 0:
            raise StopIteration
        return tuple(items)