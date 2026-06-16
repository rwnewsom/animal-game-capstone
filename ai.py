import random
from typing import Tuple
from pieces import Piece


def ai_choose_move(game: 'object', ai_color: str) -> Tuple[object, object]:
    """Choose a move for the AI.

    Strategy:
    - Greedy capture: if any move captures an opponent piece, play the first such move.
    - Otherwise: pick a random piece (shuffled order) and move it the maximum legal distance available.
    Returns (start, end) or (None, None) if no legal moves.
    """
    size_r = len(game._rows)
    size_c = len(game._columns)
    # 1) find captures
    for r in range(size_r):
        for c in range(size_c):
            piece = game._board[r][c]
            if not isinstance(piece, Piece) or piece.get_color() != ai_color:
                continue
            start = f"{game._columns[c]}{r+1}"
            for er in range(size_r):
                for ec in range(size_c):
                    dest = game._board[er][ec]
                    if isinstance(dest, Piece) and dest.get_color() != ai_color:
                        end = f"{game._columns[ec]}{er+1}"
                        # use non-mutating probe
                        legal, is_capture, _ = game.is_legal_move(start, end, player=ai_color)
                        if legal and is_capture:
                            return (start, end)

    # 2) random piece, maximize distance
    starts = [(r, c) for r in range(size_r) for c in range(size_c)
              if isinstance(game._board[r][c], Piece) and game._board[r][c].get_color() == ai_color]
    random.shuffle(starts)
    for (r, c) in starts:
        start = f"{game._columns[c]}{r+1}"
        legal_moves = []
        for er in range(size_r):
            for ec in range(size_c):
                end = f"{game._columns[ec]}{er+1}"
                legal, is_capture, _ = game.is_legal_move(start, end, player=ai_color)
                if legal:
                    dist = max(abs(r - er), abs(c - ec))
                    legal_moves.append((dist, start, end, is_capture))
        if legal_moves:
            maxd = max(m[0] for m in legal_moves)
            # prefer capture among max-distance moves if any
            candidates = [m for m in legal_moves if m[0] == maxd]
            captures = [m for m in candidates if m[3]]
            choice_pool = captures if captures else candidates
            choice = random.choice(choice_pool)
            return (choice[1], choice[2])

    # 3) fallback: any legal move
    for r in range(size_r):
        for c in range(size_c):
            piece = game._board[r][c]
            if not isinstance(piece, Piece) or piece.get_color() != ai_color:
                continue
            start = f"{game._columns[c]}{r+1}"
            for er in range(size_r):
                for ec in range(size_c):
                    end = f"{game._columns[ec]}{er+1}"
                    legal, _, _ = game.is_legal_move(start, end, player=ai_color)
                    if legal:
                        return (start, end)
    return (None, None)
