from __future__ import annotations


class Node:
    def __init__(self, frequency: int, data: str | None = None) -> None:
        self._right = None
        self._left = None
        self.data = data
        self.frequency = frequency

    def __gt__(self, other: Node):
        return self.frequency > other.frequency

    def __lt__(self, other: Node):
        return self.frequency < other.frequency

    def __eq__(self, other: Node):
        return self.frequency == other.frequency

    def __geq__(self, other: Node):
        return self.__gt__(other) or self.__eq__(other)

    def __leq__(self, other: Node):
        return self.__lt__(other) or self.__eq__(other)

    def __str__(self) -> str:
        return f"\n\t<Node :( Left:{self._left},\n\tRight:{self._right}>)"

    @property
    def get_left(self):
        return self._left

    @property
    def get_right(self):
        return self._right

    def set_left(self, node: Node | None):
        self._left = node

    def set_right(self, node: Node | None):
        self._right = node
