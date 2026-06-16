import unittest
import random
from AnimalGame import AnimalGame
from pieces import Chinchilla, Wombat, Emu
from ai import ai_choose_move


class TestAI(unittest.TestCase):
    def test_ai_greedy_capture(self):
        """AI should choose a capturing move when available."""
        game = AnimalGame()
        # clear board
        game._board = [[None for _ in range(len(game._columns))] for _ in range(len(game._rows))]
        # place AI piece (amethyst) at a3 and opponent at a1 so a3->a1 is a legal capture
        game._board[2][0] = Emu(color='amethyst')
        game._board[0][0] = Chinchilla(color='tangerine')
        # ensure it's amethyst's turn
        game._current_turn = 1

        start, end = ai_choose_move(game, 'amethyst')
        self.assertEqual((start, end), ('a3', 'a1'))

    def test_ai_max_distance_move(self):
        """When no captures are available, AI should move a piece the maximum legal distance."""
        game = AnimalGame()
        # clear board
        game._board = [[None for _ in range(len(game._columns))] for _ in range(len(game._rows))]
        # place a single amethyst wombat at a1 which can jump 4 squares to a5
        game._board[0][0] = Wombat(color='amethyst')
        # ensure it's amethyst's turn
        game._current_turn = 1

        # seed randomness to make behavior deterministic
        random.seed(0)
        start, end = ai_choose_move(game, 'amethyst')
        self.assertEqual((start, end), ('a1', 'a5'))


if __name__ == '__main__':
    unittest.main()

