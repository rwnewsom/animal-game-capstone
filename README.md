# portfolio-project

Write a class named **AnimalGame** for playing an animal-themed abstract board game, described below.

One side's pieces are colored tangerine and the other side's pieces are colored amethyst (you don't need to display any colors, but having names for the two sides will help us talk about them) You will need to keep track of which player's turn it is. The tangerine player moves first.

The game takes place on a 7x7 grid. Locations on the board will be specified using "algebraic notation", with columns labeled a-g and rows labeled 1-7.

**Piece movements**: The table below gives the names and movements for each piece (like the colors of the two sides, the names of the pieces don't affect the game and are just to make talking about them easier).
* The _distance_ is the number of squares a piece can move in its given direction. 
* The _direction_ a piece moves is either orthogonal or diagonal (orthogonal just means vertical or horizontal). However, any diagonal moving piece can also move 1 square orthogonally **instead** of its normal move and any orthogonal moving piece can also move 1 square diagonally **instead** of its normal move. It technically doesn't matter if a piece with distance 1 is orthogonal or diagonal.
* The _locomotion_ is either sliding or jumping. A sliding piece can move any (nonzero) number of squares up to its distance, but is blocked if a piece is in the way. A jumping piece must move its full number of squares in a straight (orthogonal or diagonal) line, but it cannot be blocked. It technically doesn't matter if a piece with distance 1 is sliding or jumping.
* If a piece moves to a square that contains an enemy piece, it captures that piece by replacing it on the square and removing the captured piece from the board.

| Name | Direction | Distance | Locomotion |
|---|---|---|---|
|chinchilla | diagonal | 1 | sliding |
| wombat | orthogonal | 4 | jumping |
| emu | orthogonal | 3 | sliding |
| cuttlefish | diagonal | 2 | jumping |

**Starting position**: The tangerine player's pieces start in row 1 and the amethyst player's pieces start in row 7. The order of pieces in the row (for both players) is as follows:

| chinchilla | wombat | emu | cuttlefish |  emu | wombat | chinchilla |
|---|---|---|---|---|---|---|

 The pieces are placed in the order given, with the first piece in the row placed in column 1, the second piece in column 2, etc.

If a player's cuttlefish is captured, the game ends, and that player loses.

You must write a class for each piece type that contains the logic for how that piece can legally move. You must write a Piece class that all the classes for the different piece types inherit from. The data members and methods of these classes are up to you.

Your AnimalGame class must include the following:
* An **init method** that initializes any data members
* A method called **get_game_state** that just returns 'UNFINISHED', 'TANGERINE_WON', 'AMETHYST_WON'. 
* A method called **make_move** that takes two parameters - strings that represent the square moved from and the square moved to.  For example, make_move('b2', 'b4').  If the square being moved from does not contain a piece belonging to the player whose turn it is, or if the piece cannot legally move to the **indicated target square**, or if the game has already been won, then it should **just return False**.  Otherwise, it should make the indicated move, update whose turn it is, and return True.

You're not required to have a function that prints the board, but you will probably find it very useful for testing purposes.

Feel free to add whatever other classes, methods, or data members you want.  All data members of a class must be private.  Every class must have an init method that initializes all of the data members for that class.

Here's a very simple example of how the class could be used:
```
game = AnimalGame()
move_result = game.make_move('c2', 'c4')
state = game.get_game_state()
```

The file must be named: **AnimalGame.py**

