# Author: Robert Newsom
# GitHub username: rwnewsom
# Date: 5/31/2025
# Description: Portfolio project: create an animal game.


# Unit tests moved to test_animal_game.py
from typing import List, Optional, Tuple, Type
from pieces import Piece, Chinchilla, Wombat, Emu, Cuttlefish
from ai import ai_choose_move


class UnknownValueException(Exception):
    """should not encounter this exception however useful for debugging if it occurs"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


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
        self._columns: List[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self._rows: List[int] = [1, 2, 3, 4, 5, 6, 7]
        # initialize board (use None for empty squares rather than '.')
        self._board: List[List[Optional[Piece]]] = [[None for _ in range(len(self._columns))] for _ in range(len(self._rows))]
        # pieces are placed in this order...
        self._animal_order: List[Type[Piece]] = [Chinchilla, Wombat, Emu, Cuttlefish, Emu, Wombat, Chinchilla]
        # ... on the first and last row
        self._starting_rows: List[int] = [0, 6]
        self._setup_game()
        # store the last error message for a failed move
        self._last_error: Optional[str] = None

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

    def _get_current_player(self) -> str:
        return self._turn_order[self._current_turn % 2]

    def _get_current_turn(self) -> int:
        return self._current_turn

    def _print_board(self, selected_square: Optional[str] = None, valid_destinations: Optional[List[str]] = None):
        """Display the current board in a compact ASCII grid with optional highlights.

        Uses fixed-width cells so headers, separators and rows align exactly.
        :param selected_square: algebraic notation of selected piece (e.g., 'a1')
        :param valid_destinations: list of algebraic notations for valid move destinations
        """
        print(f'Board for turn: {self._current_turn}    Status: {self._game_state}    Player: {self._get_current_player()}')
        cols = self._columns
        label_w = 3  # width reserved for the row labels (e.g. ' 1')
        cell_w = 5   # inner content width for each cell
        cell_total = cell_w + 2  # includes one space padding on each side

        # Parse selected square if provided
        selected_row_idx, selected_col_idx = None, None
        if selected_square:
            try:
                selected_col_idx = self._map_column_to_index(selected_square[0])
                selected_row_idx = int(selected_square[1]) - 1
            except (IndexError, ValueError):
                pass

        # Convert valid destinations to coordinate indices
        valid_coords = set()
        if valid_destinations:
            for dest in valid_destinations:
                try:
                    col_idx = self._map_column_to_index(dest[0])
                    row_idx = int(dest[1]) - 1
                    valid_coords.add((row_idx, col_idx))
                except (IndexError, ValueError):
                    pass

        # separator line (top and between rows)
        sep = ' ' * (label_w + 1) + '+' + '+'.join(['-' * cell_total for _ in cols]) + '+'

        # header with column letters centered in each cell_total
        header = ' ' * (label_w + 1) + '|' + '|'.join([f'{c:^{cell_total}}' for c in cols]) + '|'

        print(sep)
        print(header)
        print(sep)

        for r_idx, row in enumerate(self._board):
            row_label = f'{r_idx+1:>{label_w}}'
            cells = []
            for c_idx, cell in enumerate(row):
                # Determine cell content and highlight
                if r_idx == selected_row_idx and c_idx == selected_col_idx:
                    # Selected piece - highlight with brackets
                    if isinstance(cell, Piece):
                        content = f'[{str(cell)}]'
                    else:
                        content = '[  ]'
                elif (r_idx, c_idx) in valid_coords:
                    # Valid destination - show with dots
                    if isinstance(cell, Piece):
                        content = f'*{str(cell)}*'
                    else:
                        content = ' . '
                else:
                    # Normal cell
                    if isinstance(cell, Piece):
                        content = f'{str(cell)}'
                    else:
                        content = ''
                cells.append(f'{content:^{cell_total}}')
            row_str = f'{row_label} |' + '|'.join(cells) + '|'
            print(row_str)
            print(sep)

    def get_game_state(self):
        """ retrieve the current state of the game, which is initially 'UNFINISHED',
        however may become either 'TANGERINE_WON' OR 'AMETHYST_WON' """
        return self._game_state

    def _map_column_to_index(self, column: str) -> int:
        """helper function that converts char to its array index
        column: char - the column (a..g) to be mapped
        """
        return self._columns.index(column)

    def _validate_move_in_bounds(self, start_column: str, start_row: int, end_column: str, end_row: int) -> bool:
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

    def _calculate_distance(self, start_row: int, start_column: int, end_row: int, end_column: int) -> Tuple[int, int]:
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

    def _is_counter_move(self, piece: Piece, is_orthogonal: bool) -> bool:
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

    def _is_move_blocked(self, start_row: int, start_column: int, end_row: int, end_column: int) -> bool:
        """
        determine how many positions the piece will move
        :param start_column: int - starting column for piece
        :param start_row: int - starting row for piece
        :param end_column: int - ending column for piece
        :param end_row: int - ending row for piece
        :returns: bool true is movement is blocked
        """
        # Only orthogonal moves can be blocked; diagonal moves are considered jumping
        row_distance, column_distance = self._calculate_distance(start_row, start_column, end_row, end_column)
        if row_distance != 0 and column_distance != 0:
            return False
        if row_distance == 0 and column_distance == 0:
            return False

        # Step from the destination back toward the start, but do NOT consider the destination square itself
        cur_row, cur_col = end_row, end_column
        # compute the step to move one square toward the start
        step_row = 0
        if start_row < end_row:
            step_row = -1
        elif start_row > end_row:
            step_row = 1
        step_col = 0
        if start_column < end_column:
            step_col = -1
        elif start_column > end_column:
            step_col = 1

        # move one step first to skip the destination square
        cur_row += step_row
        cur_col += step_col

        while True:
            # if we've reached the start location, no blockers were found
            if cur_row == start_row and cur_col == start_column:
                return False
            # guard against out-of-bounds just in case
            if not (0 <= cur_row < len(self._rows) and 0 <= cur_col < len(self._columns)):
                return False
            location = self._board[cur_row][cur_col]
            if isinstance(location, Piece):
                return True
            cur_row += step_row
            cur_col += step_col

    def make_move(self, start, end):
        """
        :param start: str- algebraic notation of starting position, e.g. 'a1' for column a row 1
        :param end: str-  algebraic notation of ending position, e.g. 'a2' for column a row 2
        :return: bool: false if game has been won or move illegal, else true
        """
        # cannot continue to play if game is in finished state
        is_game_active = self.get_game_state() == 'UNFINISHED'
        if not is_game_active:
            self._last_error = 'Game is already finished.'
            return False

        start_column, start_row = start[0], start[1]
        end_column, end_row = end[0], end[1]

        is_in_bounds = self._validate_move_in_bounds(start_column, start_row, end_column, end_row)
        if not is_in_bounds:
            self._last_error = 'Move is out of bounds.'
            return False

        start_row_index = int(start_row) - 1 # cast to int and adjust for zero based indexing

        start_column_index = self._map_column_to_index(start_column)
        selected_piece = self._board[start_row_index][start_column_index]

        # a piece must exist at the selected location
        if selected_piece is None:
            self._last_error = 'No piece at the starting square.'
            return False

        elif not isinstance(selected_piece, Piece):
            # somehow an inappropriate value has been recorded on the board, perhaps a piece from a monopoly game?
            message = f'unknown piece on board: {selected_piece}'
            raise UnknownValueException(message)

        # Help static analyzers: by this point selected_piece is guaranteed to be a Piece
        assert isinstance(selected_piece, Piece)

        selected_piece_color = selected_piece.get_color()
        current_player = self._get_current_player()
        # piece must have same color as current player
        if selected_piece_color != current_player:
            self._last_error = 'You must move your own piece.'
            return False

        else:
            end_row_index = int(end_row) - 1
            end_column_index = self._map_column_to_index(end_column)

            row_dist, col_dist = self._calculate_distance(
                start_row_index, start_column_index, end_row_index, end_column_index
            )
            if max(abs(row_dist), abs(col_dist)) > selected_piece.get_distance():
                self._last_error = 'Move is too far for this piece.'
                return False
            row_distance, column_distance = abs(row_dist), abs(col_dist)
            if row_distance == 0 and column_distance == 0:
                self._last_error = 'Must move to a different square (cannot pass).'
                return False # not allowed to pass, that could stall game indefinitely

            is_orthogonal = row_distance == 0 or column_distance == 0

            if max(row_distance, column_distance) > 0:
                if selected_piece.get_locomotion() == 'sliding':
                    # fixme adjust so not checking destination
                    is_blocked = self._is_move_blocked(start_row_index, start_column_index, end_row_index,
                                                       end_column_index)
                    if is_blocked:
                        self._last_error = 'Move is blocked by another piece.'
                        return False
                else:
                    # jumpers must use all movement UNLESS dist is 1 and counter to normal direction
                    if max(row_distance, column_distance) == 1:
                        if not self._is_counter_move(selected_piece, is_orthogonal):
                            self._last_error = 'Jumping piece may only move 1 square as a counter-move.'
                            return False
                    else:
                        if max(row_distance, column_distance) != selected_piece.get_distance():
                            self._last_error = 'Jumping piece must use full movement distance.'
                            return False

                if is_orthogonal:
                    if selected_piece.get_direction() == 'diagonal':
                        if max(row_distance, column_distance) != 1:
                            self._last_error = 'Diagonal piece can only move 1 square orthogonally as counter-move.'
                            return False
                else:
                    if row_distance != column_distance:
                        self._last_error = 'Diagonal moves must change row and column by the same amount.'
                        return False # diag must move one square each dir
                    if selected_piece.get_direction() == 'orthogonal':
                        if max(row_distance, column_distance) != 1:
                            self._last_error = 'Orthogonal-only piece can only move 1 square diagonally as counter-move.'
                            return False

            destination_value = self._board[end_row_index][end_column_index]

            if isinstance(destination_value, Piece):
                destination_piece_color = destination_value.get_color()
                # cannot move on top of own piece
                if destination_piece_color == current_player:
                    self._last_error = 'Destination occupied by your own piece.'
                    return False
                self._board[end_row_index][end_column_index] = selected_piece
                self._board[start_row_index][start_column_index] = None
                if destination_value.get_name() == 'cuttlefish':
                    if destination_value.get_color() == 'amethyst':
                        self._game_state = 'TANGERINE_WON'
                    else:
                        self._game_state = 'AMETHYST_WON'
                    return True # do not increment turn
                else:
                    self._current_turn += 1
                    return True

            elif destination_value is None: # legal move, update origin and destination values
                self._board[end_row_index][end_column_index] = selected_piece
                self._board[start_row_index][start_column_index] = None
                # increment turn and return True
                self._current_turn += 1
                self._last_error = None
                return True
            else:
                message = f'unknown piece on board: {destination_value}'
                raise UnknownValueException(message)

    def get_last_error(self) -> Optional[str]:
        """Return the last error message set by make_move when it returns False."""
        return self._last_error

    def get_valid_destinations(self, start: str) -> List[str]:
        """Get all valid destination squares for a piece at the given position.

        :param start: algebraic notation of starting position (e.g., 'a1')
        :return: list of valid destination squares in algebraic notation
        """
        valid_moves = []

        # Validate starting position
        if not start or len(start) < 2:
            return valid_moves

        start_column, start_row = start[0], start[1]

        # Check if move is in bounds
        if not self._validate_move_in_bounds(start_column, start_row, start_column, start_row):
            return valid_moves

        start_row_index = int(start_row) - 1
        start_column_index = self._map_column_to_index(start_column)
        selected_piece = self._board[start_row_index][start_column_index]

        # No piece at starting location
        if selected_piece is None or not isinstance(selected_piece, Piece):
            return valid_moves

        # Try all possible destinations on the board
        for end_row in self._rows:
            for end_col in self._columns:
                end_notation = f'{end_col}{end_row}'
                # Check if this move would be legal
                is_legal, _, _ = self.is_legal_move(start, end_notation, player=selected_piece.get_color())
                if is_legal:
                    valid_moves.append(end_notation)

        return valid_moves

    def is_legal_move(self, start: str, end: str, player: Optional[str] = None) -> Tuple[bool, bool, Optional[str]]:
        """Check whether a move would be legal without mutating game state.

        Returns (is_legal, is_capture, error_message). If is_legal is True, error_message is None.
        If player is provided, it is enforced as the moving player; otherwise current player is used.
        """
        # mirror validation logic from make_move but do not change any state
        is_game_active = self.get_game_state() == 'UNFINISHED'
        if not is_game_active:
            return False, False, 'Game is already finished.'

        if not start or not end or len(start) < 2 or len(end) < 2:
            return False, False, 'Invalid algebraic notation.'

        start_column, start_row = start[0], start[1]
        end_column, end_row = end[0], end[1]

        is_in_bounds = self._validate_move_in_bounds(start_column, start_row, end_column, end_row)
        if not is_in_bounds:
            return False, False, 'Move is out of bounds.'

        start_row_index = int(start_row) - 1
        start_column_index = self._map_column_to_index(start_column)
        selected_piece = self._board[start_row_index][start_column_index]

        if selected_piece is None:
            return False, False, 'No piece at the starting square.'
        if not isinstance(selected_piece, Piece):
            return False, False, f'unknown piece on board: {selected_piece}'

        current_player = player if player is not None else self._get_current_player()
        if selected_piece.get_color() != current_player:
            return False, False, 'You must move your own piece.'

        end_row_index = int(end_row) - 1
        end_column_index = self._map_column_to_index(end_column)

        row_dist, col_dist = self._calculate_distance(
            start_row_index, start_column_index, end_row_index, end_column_index
        )
        if max(abs(row_dist), abs(col_dist)) > selected_piece.get_distance():
            return False, False, 'Move is too far for this piece.'
        row_distance, column_distance = abs(row_dist), abs(col_dist)
        if row_distance == 0 and column_distance == 0:
            return False, False, 'Must move to a different square (cannot pass).'

        is_orthogonal = row_distance == 0 or column_distance == 0

        if max(row_distance, column_distance) > 0:
            if selected_piece.get_locomotion() == 'sliding':
                is_blocked = self._is_move_blocked(start_row_index, start_column_index, end_row_index,
                                                   end_column_index)
                if is_blocked:
                    return False, False, 'Move is blocked by another piece.'
            else:
                if max(row_distance, column_distance) == 1:
                    if not self._is_counter_move(selected_piece, is_orthogonal):
                        return False, False, 'Jumping piece may only move 1 square as a counter-move.'
                else:
                    if max(row_distance, column_distance) != selected_piece.get_distance():
                        return False, False, 'Jumping piece must use full movement distance.'

            if is_orthogonal:
                if selected_piece.get_direction() == 'diagonal':
                    if max(row_distance, column_distance) != 1:
                        return False, False, 'Diagonal piece can only move 1 square orthogonally as counter-move.'
            else:
                if row_distance != column_distance:
                    return False, False, 'Diagonal moves must change row and column by the same amount.'
                if selected_piece.get_direction() == 'orthogonal':
                    if max(row_distance, column_distance) != 1:
                        return False, False, 'Orthogonal-only piece can only move 1 square diagonally as counter-move.'

        destination_value = self._board[end_row_index][end_column_index]
        if isinstance(destination_value, Piece):
            destination_piece_color = destination_value.get_color()
            if destination_piece_color == current_player:
                return False, False, 'Destination occupied by your own piece.'
            # capture
            return True, True, None
        elif destination_value is None:
            return True, False, None
        else:
            return False, False, f'unknown piece on board: {destination_value}'

    def show_board(self):
        """Show the board using the improved ASCII grid output used by _print_board."""
        # Delegate to the formatted debug printer so CLI uses the same UI.
        self._print_board()


def _prompt_piece_selection(game: 'AnimalGame', player: str, prompt_text: str) -> Optional[str]:
    """Helper to get piece selection from player. Returns algebraic notation or None if quit."""
    while True:
        raw = input(prompt_text).strip()
        if raw.lower() in ('q', 'quit', 'exit'):
            return None
        if len(raw) < 2:
            print("Invalid input. Enter piece location as: 'a1' or 'q' to quit.")
            continue
        piece_notation = raw[:2]

        # Validate the notation format
        if piece_notation[0] not in game._columns or piece_notation[1] not in [str(r) for r in game._rows]:
            print(f"Invalid square: '{piece_notation}'. Enter move as: 'a1' or 'q' to quit.")
            continue

        # Check if piece exists and belongs to player
        start_col_idx = game._map_column_to_index(piece_notation[0])
        start_row_idx = int(piece_notation[1]) - 1
        piece = game._board[start_row_idx][start_col_idx]

        if piece is None:
            print(f"No piece at {piece_notation}. Select a piece to move.")
            continue

        if piece.get_color() != player:
            print(f"That piece belongs to the opponent. Select one of your own pieces.")
            continue

        return piece_notation


def _prompt_destination_selection(game: 'AnimalGame', start: str, prompt_text: str) -> Optional[str]:
    """Helper to get destination from player. Returns algebraic notation or None if cancel."""
    while True:
        raw = input(prompt_text).strip()
        if raw.lower() in ('c', 'cancel'):
            return None
        if len(raw) < 2:
            print("Invalid input. Enter destination as: 'a3' or 'c' to cancel.")
            continue
        dest_notation = raw[:2]

        # Validate the notation format
        if dest_notation[0] not in game._columns or dest_notation[1] not in [str(r) for r in game._rows]:
            print(f"Invalid square: '{dest_notation}'. Enter move as: 'a3' or 'c' to cancel.")
            continue

        # Check if move is legal
        is_legal, is_capture, error = game.is_legal_move(start, dest_notation)
        if not is_legal:
            print(f"Illegal move. Reason: {error}")
            continue

        return dest_notation


def _prompt_move_input(prompt_text: str) -> tuple:
    """Helper to get start/end from a player's input. Reprompts on malformed input. Returns (start, end) or (None, None) if quit."""
    while True:
        raw = input(prompt_text).strip()
        if raw.lower() in ('q', 'quit', 'exit'):
            return (None, None)
        parts = raw.split()
        if len(parts) != 2:
            print("Invalid input. Enter move as: 'a1 b2' or 'q' to quit.")
            continue
        return (parts[0], parts[1])


if __name__ == '__main__':
    game = AnimalGame()
    try:
        while game.get_game_state() == 'UNFINISHED':
            game.show_board()
            current = game._get_current_player()
            # human plays tangerine; AI plays amethyst
            if current == 'amethyst':
                start, end = ai_choose_move(game, 'amethyst')
                if start is None:
                    print('AI has no legal moves. Exiting.')
                    break
                print(f"AI ({current}) plays: {start} {end}")
            else:
                # Two-step move selection for human player
                print("\n" + "="*50)
                start = _prompt_piece_selection(
                    game,
                    current,
                    f"{current} - Select piece to move (e.g., 'a1') or 'q' to quit: "
                )
                if start is None:
                    print('Exiting game.')
                    break

                # Show valid destinations
                valid_destinations = game.get_valid_destinations(start)
                if not valid_destinations:
                    print(f"No legal moves available for piece at {start}. Try another piece.")
                    print("="*50 + "\n")
                    continue

                # Display board with selected piece and valid destinations highlighted
                game._print_board(selected_square=start, valid_destinations=valid_destinations)

                # Get destination
                dest_list = ", ".join(sorted(valid_destinations))
                end = _prompt_destination_selection(
                    game,
                    start,
                    f"{current} - Move to (valid: {dest_list}) or 'c' to cancel: "
                )
                if end is None:
                    print("Move cancelled. Try again.")
                    print("="*50 + "\n")
                    continue
                print("="*50 + "\n")

            try:
                moved = game.make_move(start, end)
            except UnknownValueException as e:
                print(f'Error: {e}')
                continue
            if moved:
                print('✓ Move accepted.')
            else:
                print(f"✗ Illegal move. Reason: {game.get_last_error()}")
        # final state
        print('\nFinal board:')
        game.show_board()
        state = game.get_game_state()
        if state == 'TANGERINE_WON':
             print('Tangerine has won!')
        elif state == 'AMETHYST_WON':
            print('Amethyst has won!')
        else:
            print('Game ended.')
    except (KeyboardInterrupt, EOFError):
        print('\nInterrupted. Exiting.')

# Unit tests moved to test_animal_game.py
