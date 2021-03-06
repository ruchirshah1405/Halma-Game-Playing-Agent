## Introduction 
In this project, we will play the game of Halma, an adversarial game with some similarities to
checkers. The game uses a 16x16 checkered gameboard. Each player starts with 19 game pieces
clustered in diagonally opposite corners of the board. To win the game, a player needs to
transfer all of their pieces from their starting corner to the opposite corner, into the positions
that were initially occupied by the opponent. Note that this original rule of the game is subject
to spoiling, as a player may choose to not move some pieces at all, thereby preventing the
opponent from occupying those locations. Note that the spoiling player cannot win either
(because some pieces remain in their original corner and thus cannot be used to occupy all
positions in the opposite corner). Here, to prevent spoiling, we modify the goal of the game to
be to occupy all of the opponent’s starting positions which the opponent is not still occupying.
## Play sequence:
We first describe the typical play for humans. We will then describe some minor modifications
for how we will play this game with artificial agents.
- Create the initial board setup according to the above description.
- Players randomly determine who will move first.
- Pieces can move in eight possible directions (orthogonally and diagonally).
- Each player's turn consists of moving a single piece of one's own color in one of the
following plays:
    - One move to an empty square:
      - Move the piece to an empty square that is adjacent to the piece’s original
position (with 8-adjacency).
      - This move ends the play for this player’s turn.
    - One or more jumps over adjacent pieces:
        - An adjacent piece of any color can be jumped if there is an empty square
on the directly opposite side of that piece.
        - Place the piece in the empty square on the opposite side of the jumped
piece.
        -The piece that was jumped over is unaffected and remains on the board.
        - After any jump, one may make further jumps using the same piece, or end
the play for this turn.
        - In a sequence of jumps, a piece may jump several times over the same
other piece.
- Once a piece has reached the opposing camp, a play cannot result in that piece leaving
the camp.
- If the current play results in having every square of the opposing camp that is not already
occupied by the opponent to be occupied by one's own pieces, the acting player wins.
Otherwise, play proceeds to the other player.