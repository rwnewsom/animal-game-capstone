from typing import Optional

__all__ = ["Piece", "Chinchilla", "Wombat", "Emu", "Cuttlefish"]


class Piece:
    """
    base class to initialize a game piece with the following members:
    name: str - the type of piece
    direction: str [orthogonal or diagonal]
    distance: int - the number of spaces the piece can move
    locomotion: str - jumping or sliding
    captured: str - whether the piece has been captured
    color: str - amethyst or topaz
    """
    def __init__(self, name=None, direction=None, distance=None, locomotion=None, color=None):
        self._name = name
        self._direction = direction
        self._distance = distance
        self._locomotion = locomotion
        self._captured = False
        self._color = color # topaz or amethyst

    def get_name(self):
        return self._name
    def get_direction(self):
        return self._direction
    def get_distance(self):
        return self._distance
    def get_locomotion(self):
        return self._locomotion
    def get_is_captured(self):
        return self._captured

    def get_color(self):
        return self._color

    def __str__(self):
        return 'parent'

    def __repr__(self):
        return 'parent'


class Chinchilla(Piece):
    def __init__(self, color=None):
        super().__init__(
            name='chinchilla',
            direction='diagonal',
            distance=1,
            locomotion='sliding',
            color=color
        )

    def __str__(self):
        if self._color == 'amethyst':
            return 'aCa'
        else:
            return 'tCt'
    def __repr__(self):
        return self.__str__()


class Wombat(Piece):
    def __init__(self, color=None):
        super().__init__(
            name='wombat',
            direction='orthogonal',
            distance=4,
            locomotion='jumping',
            color=color
        )

    def __str__(self):
        if self._color == 'amethyst':
            return 'aWa'
        else:
            return 'tWt'
    def __repr__(self):
        return self.__str__()


class Emu(Piece):
    def __init__(self, color=None):
        super().__init__(
            name='emu',
            direction='orthogonal',
            distance=3,
            locomotion='sliding',
            color=color
        )

    def __str__(self):
        if self._color == 'amethyst':
            return 'aEa'
        else:
            return 'tEt'
    def __repr__(self):
        return self.__str__()


class Cuttlefish(Piece):
    def __init__(self, color=None):
        super().__init__(
            name='cuttlefish',
            direction='diagonal',
            distance=2,
            locomotion='jumping',
            color=color
        )

    def __str__(self):
        if self._color == 'amethyst':
            return 'a&a'
        else:
            return 't&t'
    def __repr__(self):
        return self.__str__()
