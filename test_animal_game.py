import unittest
from AnimalGame import AnimalGame, UnknownValueException
from pieces import Chinchilla, Wombat, Emu, Cuttlefish


class TestPieces(unittest.TestCase):
    """contains unit tests for game pieces"""
    def test_chinchilla(self):
        """chinchilla should initialize with appropriate values"""
        piece = Chinchilla()
        self.assertEqual(piece.get_name(), 'chinchilla')
        self.assertEqual(piece.get_direction(), 'diagonal')
        self.assertEqual(piece.get_distance(), 1)
        self.assertEqual(piece.get_is_captured(), False)
        self.assertEqual(piece.get_locomotion(), 'sliding')

    def test_wombat(self):
        """wombat should initialize with appropriate values"""
        piece = Wombat()
        self.assertEqual(piece.get_name(), 'wombat')
        self.assertEqual(piece.get_direction(), 'orthogonal')
        self.assertEqual(piece.get_distance(), 4)
        self.assertEqual(piece.get_is_captured(), False)
        self.assertEqual(piece.get_locomotion(), 'jumping')

    def test_emu(self):
        """emu should initialize with appropriate values"""
        piece = Emu()
        self.assertEqual(piece.get_name(), 'emu')
        self.assertEqual(piece.get_direction(), 'orthogonal')
        self.assertEqual(piece.get_distance(), 3)
        self.assertEqual(piece.get_is_captured(), False)
        self.assertEqual(piece.get_locomotion(), 'sliding')

    def test_cuttlefish(self):
        """cuttlefish should initialize with appropriate values"""
        piece = Cuttlefish()
        self.assertEqual(piece.get_name(), 'cuttlefish')
        self.assertEqual(piece.get_direction(), 'diagonal')
        self.assertEqual(piece.get_distance(), 2)
        self.assertEqual(piece.get_is_captured(), False)
        self.assertEqual(piece.get_locomotion(), 'jumping')


class TestAnimalGame(unittest.TestCase):
    def test_init_game(self):
        """
        game should be initialized correctly
        """
        game = AnimalGame()
        self.assertIsInstance(game, AnimalGame)

    def test_get_current_player(self):
        """first player should be topaz"""
        game = AnimalGame()
        current_player = game._get_current_player()
        self.assertEqual(current_player, 'topaz')

    def test_get_current_turn(self):
        """game should initialize at turn 0"""
        game = AnimalGame()
        self.assertEqual(game._get_current_turn(), 0)

    def test_get_game_state(self):
        """initial game state should be unfinished"""
        game = AnimalGame()
        self.assertEqual(game.get_game_state(), 'UNFINISHED')


    def test_setup_game(self):
        """
        tests to verify that pieces are in order
        """
        game = AnimalGame()
        # creature on first row, first column should be a Chinchilla
        initial_topaz_piece = game._board[0][0]
        self.assertIsInstance(initial_topaz_piece, Chinchilla)
        # and type should match current player
        current_player = game._get_current_player()
        self.assertEqual(initial_topaz_piece.get_color(), current_player)

        # creature on last row, first column should also be a Chinchilla
        initial_amethyst_piece = game._board[6][0]
        self.assertIsInstance(initial_amethyst_piece, Chinchilla)
        # however color should match that of opposing player
        self.assertEqual(initial_amethyst_piece.get_color(), 'amethyst')

    def test_map_column_to_index(self):
        """test helper function that converts char to its array index"""
        game = AnimalGame()
        result = [game._map_column_to_index(i) for i in game._columns]
        self.assertEqual(result, [0,1,2,3,4,5,6])

    def test_calculate_distance(self):
        game = AnimalGame()
        result = game._calculate_distance(2, 2, 1, 1)
        self.assertEqual(result, (1, 1))


    def test_validate_move_invalid(self):
        """ series of tests to determine if invalid moves are flagged """
        game = AnimalGame()
        # should not be able to choose if no piece exists
        result = game.make_move('a3', 'b2')
        self.assertFalse(result)

        # should not be able to move opponent's piece
        result = game.make_move('a7', 'a6')
        self.assertFalse(result)

        # should not be able to move on top of own piece
        result = game.make_move('a1', 'b1')
        self.assertFalse(result)



    def test_validate_move_in_bounds(self):
        """should not be able to move off the board - column"""
        game = AnimalGame()
        result = game.make_move('a1', 'h1')
        self.assertFalse(result)


    def test_make_valid_move(self):
        """
        series of tests for valid moves and side effects
        HACK: I acknowledge this is more of an integration test, if I can break out more helper functions
        from make_move I'll likewise break out asserts into tests
        Also, logic to detect if a sliding move has been blocked has not yet been implemented, so that case is missing
        """
        game = AnimalGame()
        # should be allowed to move a distance of one - orthogonal when piece movement is diagonal
        result = game.make_move('d1', 'd2')
        self.assertTrue(result)

        # should increment turn and change current player
        result = game._get_current_turn()
        self.assertEqual(result, 1)

        # should be next players turn
        current_player = game._get_current_player()
        assert current_player == 'amethyst'

        # should not allow a diagonal piece to move greater than 1 unit diagonally

        result = game.make_move('a7', 'a5')
        self.assertFalse(result)

        # should allow diagonal move
        result = game.make_move('d7', 'b5')
        self.assertTrue(result)
        game._print_board()

        # next player makes diagonal move
        result = game.make_move('d2', 'b4')
        self.assertTrue(result)
        game._print_board()

        # now handle capture logic!!
        result = game.make_move('b5', 'b4')
        self.assertTrue(result)
        game_state = game.get_game_state()
        self.assertEqual(game_state, 'AMETHYST_WON')
        game._print_board()

        # should not be able to move further this game
        result = game.make_move('f7', 'f5')
        self.assertFalse(result)
        game._print_board()

    def test_jumping_piece_must_use_full_distance(self):
        """
        a jumping piece must use all available distance
        """
        game = AnimalGame()
        bad_jump = game.make_move('f1', 'f3')
        # may not jump unless full distance
        self.assertFalse(bad_jump)
        # may jump full distance
        good_jump = game.make_move('f1', 'f5')
        game._print_board()
        self.assertTrue(good_jump)

    def test_unknown_value_on_board(self):
        """
        error should be raised if a value is on the board other than '.' or a Piece object
        """
        game = AnimalGame()
        # None is now used for empty squares; use a distinct invalid value to trigger the exception
        game._board[0][0] = "INVALID"
        with self.assertRaises(UnknownValueException):
            game.make_move('a1', 'a2')

    def test_is_move_blocked(self):
        """
        test that a sliding animal cannot make a move if any other piece it between its starting and ending location:
        """
        game = AnimalGame()
        # set cuttlefish in front of emu
        game._print_board()
        first_legal_move = game.make_move('a1', 'a2')
        self.assertTrue(first_legal_move)
        game._print_board()
        # make opposing move to increment turn

        second_legal_move = game.make_move('a7', 'a6')
        self.assertTrue(second_legal_move)
        game._print_board()
        # try tp move emu past wombat
        result = game.make_move('c1', 'a1')
        game._print_board()
        self.assertFalse(result)

    def test_is_counter_move(self):
        """test if a piece is making a move not IAW piece direction"""
        game = AnimalGame()
        piece = Cuttlefish()
        is_orthogonal = True
        result = game._is_counter_move(piece, is_orthogonal)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
