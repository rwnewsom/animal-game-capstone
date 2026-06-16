# UI/UX Improvements - Two-Step Move Selection and Visual Highlights

## Overview
The Animal Game interface has been enhanced with an intuitive two-step move selection system and visual board highlights, making the game more user-friendly and discoverable.

## Key Features Implementation

### 1. **Two-Step Move Selection**
Instead of entering both the source and destination in one line (e.g., `a1 a2`), players now:

**Step 1: Select a Piece**
```
==================================================
tangerine - Select piece to move (e.g., 'a1') or 'q' to quit: a2
```

**Step 2: See Valid Moves & Choose Destination**
```
Board with highlights displayed...

==================================================
tangerine - Move to (valid: a3, a4, b3) or 'c' to cancel: a3
==================================================
```

### 2. **Visual Board Highlights**

The board now displays:
- **Selected Piece**: Shown with brackets `[tCt]`
- **Valid Destinations**: 
  - Empty squares: ` . ` (dot notation)
  - Enemy pieces: `*aWa*` (asterisks for capture opportunities)
- **Normal Pieces**: Standard display (no brackets/asterisks)

Example board display after selecting `a2`:
```
Board for turn: 0    Status: UNFINISHED    Player: tangerine
      +-------+-------+-------+-------+-------+-------+-------+
      |   a   |   b   |   c   |   d   |   e   |   f   |   g   |
      +-------+-------+-------+-------+-------+-------+-------+
    1 |  tCt  |  tWt  |  tEt  |       |  tEt  |  tWt  |  tCt  |
      +-------+-------+-------+-------+-------+-------+-------+
    2 | [tEt] |  .    |       |       |       |       |       |
      +-------+-------+-------+-------+-------+-------+-------+
    3 |  .    |       |       |       |       |       |       |
      +-------+-------+-------+-------+-------+-------+-------+
    4 |       |  a&a  |       |       |       |       |       |
      +-------+-------+-------+-------+-------+-------+-------+
    5 |       |       |       |       |       |       |       |
      +-------+-------+-------+-------+-------+-------+-------+
    6 |       |       |       |       |       |       |       |
      +-------+-------+-------+-------+-------+-------+-------+
    7 |  aCa  |  aWa  |  aEa  |       |  aEa  |  aWa  |  aCa  |
      +-------+-------+-------+-------+-------+-------+-------+
```

### 3. **Enhanced Gameplay Experience**

**Input Validation During Piece Selection:**
- Only allows selecting pieces that belong to the current player
- Shows clear error if no piece exists at selected square
- Suggests valid square format (a1, b2, etc.)

**Dynamic Destination Display:**
- Shows list of all legal moves after piece selection
- Prevents invalid destination entries upfront
- Displays error message with reason if invalid move attempted

**Better Move Feedback:**
```
✓ Move accepted.
```
vs
```
✗ Illegal move. Reason: Move is blocked by another piece.
```

## New Methods Added

### `get_valid_destinations(start: str) -> List[str]`
Calculates and returns all valid destination squares for a piece at the given location.

- **Parameters**: `start` - algebraic notation (e.g., 'a1')
- **Returns**: List of valid destination squares in algebraic notation
- **Used by**: Display board highlights and destination suggestions

### Enhanced `_print_board()`
Now accepts optional parameters:
- `selected_square`: Algebraically notated square to highlight (e.g., 'a1')
- `valid_destinations`: List of valid destination squares to visualize

## Helper Functions

### `_prompt_piece_selection()`
Guides user through piece selection with validation:
- Checks if piece exists
- Verifies piece belongs to current player
- Reprompts on invalid input

### `_prompt_destination_selection()`
Guides user through destination selection with validation:
- Accepts only valid algebraic notation
- Verifies the move is legal
- Shows error reason if move is illegal
- Allows cancellation with 'c' command

## Workflow Improvements

**Before:**
```
tangerine move (e.g. 'a1 a2') or 'q' to quit: a1 a4
Illegal move. Reason: Move is too far for this piece.
tangerine move (e.g. 'a1 a2') or 'q' to quit: a1 a3
Move accepted.
```

**After:**
```
==================================================
tangerine - Select piece to move (e.g., 'a1') or 'q' to quit: a1

[board displays with a1 highlighted and valid destinations shown]

tangerine - Move to (valid: a2, a3, b2, b3) or 'c' to cancel: a4
Illegal move. Reason: Move is blocked by another piece.
tangerine - Move to (valid: a2, a3, b2, b3) or 'c' to cancel: a3
==================================================

✓ Move accepted.
```

## User Experience Benefits

1. **Discoverability**: Players see all valid moves before choosing
2. **Error Prevention**: Invalid moves are prevented earlier in the input process
3. **Clarity**: Clear visual distinction between different square types
4. **Accessibility**: Easier to understand game mechanics for new players
5. **Feedback**: Immediate visual confirmation of selected piece and destinations
6. **Convenience**: Can cancel piece selection and try another piece without retyping full moves

## Backward Compatibility

- `is_legal_move()` method retains same signature and behavior
- All existing unit tests pass without modification
- Game logic remains unchanged

