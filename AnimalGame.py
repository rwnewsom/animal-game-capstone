# Author: Robert Newsom
# GitHub username: rwnewsom
# Date: 5/31/2025
# Description: Portfolio project: create an animal game.


# Unit tests moved to test_animal_game.py


class UnknownValueException(Exception):
    """should not encounter this exception however useful for debugging if it occurs"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Piece:
    """
    base class to initialize a game piece with the following members:
    name: str - the type of piece
    direction: str [orthogonal or diagonal]
    distance: int - the number of spaces the piece can move
    locomotion: str - jumping or sliding
    captured: str - whether the piece has been captured
    color: str - amethyst or tangerine
    """
    def __init__(self, name=None, direction=None, distance=None, locomotion=None, color=None):
        self._name = name
        self._direction = direction
        self._distance = distance
        self._locomotion = locomotion
        self._captured = False
        self._color = color # tangerine or amethyst

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

    # override so that the object is represented as a single character when game board is printed
    # add -t or -a to disambiguate the game board as to which player controls which piece
    def __str__(self):
        return 'parent'

    def __repr__(self):
        return 'parent'


class Chinchilla(Piece):
    """
    The Chinchilla subclass, color varies by owning player
    remaining values initialized per readme
    """
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
        if self._color == 'amethyst':
            return 'aCa'
        else:
            return 'tCt'

class Wombat(Piece):
    """
    The Wombat subclass, color varies by owning player
    remaining values initialized per readme
    """
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
        if self._color == 'amethyst':
            return 'aWa'
        else:
            return 'tWt'

class Emu(Piece):
    """
    The Emu subclass, color varies by owning player
    remaining values initialized per readme
    """
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
        if self._color == 'amethyst':
            return 'aEa'
        else:
            return 'tEt'

class Cuttlefish(Piece):
    """
    The Cuttlefish subclass, color varies by owning player
    remaining values initialized per readme
    """
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
        if self._color == 'amethyst':
            return 'a&a'
        else:
            return 't&t'


class AnimalGame:
    """
    The animal game initializes a 7 x 7 game board,
    sets the starting game state and turn,
    and places starting pieces for each player.
    potential states are 'UNFINISHED', 'TANGERINE_WON', 'AMETHYST_WON'

    the two players are designated tangerine & amethyst, pieces are initialized with the respective color
    """
    def __init__(self):
        self._current_turn = 0
        self._game_state = 'UNFINISHED'
        self._turn_order = ['tangerine', 'amethyst']
        self._columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self._rows = [1, 2, 3, 4, 5, 6, 7]
        # initialize board
        self._board = [['.' for _ in range(len(self._columns))] for _ in range(len(self._rows))]
        # pieces are placed in this order...
        self._animal_order = [Chinchilla, Wombat, Emu, Cuttlefish, Emu, Wombat, Chinchilla]
        # ... on the first and last row
        self._starting_rows = [0, 6]
        self._setup_game()

    def _setup_game(self):
        """
        initializes the board for both players, instantiating pieces with appropriate colors
        """
        for i in range(len(self._animal_order)):
            for j in self._starting_rows:
                animal = self._animal_order[i]
                color = self._turn_order[0] if j == 0 else self._turn_order[1]
                animal = animal(color=color)
                self._board[j][i] = animal

    def _get_current_player(self):
        return self._turn_order[self._current_turn % 2]

    def _get_current_turn(self):
        return self._current_turn

    def _print_board(self):
        """
        display the current board through a series of print statements
        """
        print(f'Board for turn: {self._current_turn}')
        print(f'Game Status: {self._game_state}')
        print(f'Current Player: {self._get_current_player()}')
        print('|-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|')
        print('|   a    b    c    d    e    f    g')
        print('|-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|')
        for i, row in enumerate(self._board):
            print(f'{i+1}|{row}|')
        print('|-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|')

    def get_game_state(self):
        """ retrieve the current state of the game, which is initially 'UNFINISHED',
        however may become either 'TANGERINE_WON' OR 'AMETHYST_WON' """
        return self._game_state

    def _map_column_to_index(self, column):
        """helper function that converts char to its array index
        column: char - the column (a..g) to be mapped
        """
        return self._columns.index(column)

    def _validate_move_in_bounds(self, start_column, start_row, end_column, end_row):
        """
        Check if either starting or ending coordinates are not within bounds of the game board
        :param start_column: char - starting column for piece
        :param start_row: int - starting row for piece
        :param end_column: char - ending column for piece
        :param end_row: int - ending row for piece
        :return: bool
        """
        if start_column not in self._columns or end_column not in self._columns:
            return False
        elif int(start_row) not in self._rows or int(end_row) not in self._rows:
            return False
        else:
            return True

    def _calculate_distance(self, start_row, start_column, end_row, end_column):
        """
        determine how many positions the piece will move
        :param start_column: int - starting column for piece
        :param start_row: int - starting row for piece
        :param end_column: int - ending column for piece
        :param end_row: int - ending row for piece
        :returns: tuple (row_distance: int, column_distance: int)
        """
        row_distance = start_row - end_row
        column_distance = start_column - end_column
        return row_distance, column_distance

    def _is_counter_move(self, piece, is_orthogonal):
        """

        :param piece: Piece object
        :param is_orthogonal: bool - True if desired move is Orthogonal
        :return: bool True if piece is moving alternate to normal direction
        """
        if piece.get_direction() == 'orthogonal':
            if is_orthogonal:
                return False
            return True
        else:
            if is_orthogonal:
                return True
            return False

    def _is_move_blocked(self, start_row, start_column, end_row, end_column):
        """
        determine how many positions the piece will move
        :param start_column: int - starting column for piece
        :param start_row: int - starting row for piece
        :param end_column: int - ending column for piece
        :param end_row: int - ending row for piece
        :returns: bool true is movement is blocked
        """
        row_distance, column_distance = self._calculate_distance(start_row, start_column, end_row, end_column)
        if row_distance != 0 and column_distance != 0:
            return True # only orthogonal moves can be blocked, diag animals jump or only have dist of 1
        if row_distance == 0 and column_distance == 0:
            return False # made it back to start
        location = self._board[end_row][end_column]
        if isinstance(location, Piece):
            return True
        else:
            # move closer to start
            if row_distance > 0:
                end_row += 1
            elif row_distance < 0:
                end_row -= 1
            if column_distance > 0:
                end_column += 1
            elif column_distance < 0:
                end_column -= 1
            return self._is_move_blocked(start_row, start_column, end_row, end_column)

    def make_move(self, start, end):
        """
        :param start: str- algebraic notation of starting position, e.g. 'a1' for column a row 1
        :param end: str-  algebraic notation of ending position, e.g. 'a2' for column a row 2
        :return: bool: false if game has been won or move illegal, else true
        """
        # cannot continue to play if game is in finished state
        is_game_active = self.get_game_state() == 'UNFINISHED'
        if not is_game_active:
            return False

        start_column, start_row = start[0], start[1]
        end_column, end_row = end[0], end[1]

        is_in_bounds = self._validate_move_in_bounds(start_column, start_row, end_column, end_row)
        if not is_in_bounds:
            return False

        start_row_index = int(start_row) - 1 # cast to int and adjust for zero based indexing

        start_column_index = self._map_column_to_index(start_column)
        selected_piece = self._board[start_row_index][start_column_index]

        # a piece must exist at the selected location
        if selected_piece == '.':
            return False

        elif not isinstance(selected_piece, Piece):
            # somehow an inappropriate value has been recorded on the board, perhaps a piece from a monopoly game?
            message = f'unknown piece on board: {selected_piece}'
            raise UnknownValueException(message)

        selected_piece_color = selected_piece.get_color()
        current_player = self._get_current_player()
        # piece must have same color as current player
        if selected_piece_color != current_player:
            return False

        else:
            end_row_index = int(end_row) - 1
            end_column_index = self._map_column_to_index(end_column)

            row_dist, col_dist = self._calculate_distance(
                start_row_index, start_column_index, end_row_index, end_column_index
            )
            if max(abs(row_dist), abs(col_dist)) > selected_piece.get_distance():
                return False
            row_distance, column_distance = abs(row_dist), abs(col_dist)
            if row_distance == 0 and column_distance == 0:
                return False # not allowed to pass, that could stall game indefinitely

            is_orthogonal = row_distance == 0 or column_distance == 0

            if max(row_distance, column_distance) > 0:
                if selected_piece.get_locomotion() == 'sliding':
                    # fixme adjust so not checking destination
                    is_blocked = self._is_move_blocked(start_row_index, start_column_index, end_row_index,
                                                       end_column_index)
                    if is_blocked:
                        return False
                else:
                    # jumpers must use all movement UNLESS dist is 1 and counter to normal direction
                    if max(row_distance, column_distance) == 1:
                        if not self._is_counter_move(selected_piece, is_orthogonal):
                            return False
                    else:
                        if max(row_distance, column_distance) != selected_piece.get_distance():
                            return False

                if is_orthogonal:
                    if selected_piece.get_direction() == 'diagonal':
                        if max(row_distance, column_distance) != 1:
                            return False
                else:
                    if row_distance != column_distance:
                        return False # diag must move one square each dir
                    if selected_piece.get_direction() == 'orthogonal':
                        if max(row_distance, column_distance) != 1:
                            return False

            destination_value = self._board[end_row_index][end_column_index]

            if isinstance(destination_value, Piece):
                destination_piece_color = destination_value.get_color()
                # cannot move on top of own piece
                if destination_piece_color == current_player:
                    return False
                self._board[end_row_index][end_column_index] = selected_piece
                self._board[start_row_index][start_column_index] = '.'
                if destination_value.get_name() == 'cuttlefish':
                    if destination_value.get_color() == 'amethyst':
                        self._game_state = 'TANGERINE_WON'
                    else:
                        self._game_state = 'AMETHYST_WON'
                    return True # do not increment turn
                else:
                    self._current_turn += 1
                    return True

            elif destination_value == '.': # legal move, update origin and destination values
                self._board[end_row_index][end_column_index] = selected_piece
                self._board[start_row_index][start_column_index] = '.'
                # increment turn and return True
                self._current_turn += 1
                return True
            else:
                message = f'unknown piece on board: {destination_value}'
                raise UnknownValueException(message)
