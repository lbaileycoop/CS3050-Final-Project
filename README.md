# CS3050-Final-Project

## Scrabble Board Game
For our final project, we've implemented Scrabble using pyarcade. It is singleplayer and keeps a scoreboard of the player vs the computer. 

### The rules of the game are as follows:
- First turn must play at least 2 letters, one of which is on the center tiles
- All subsequent turns can play any amount of tiles
- All tiles played must be in only 1 row or column of the board
- All tiles played must be orthogonally adjacent to another tile (tiles played on the same turn count)
- All words created or added to on a turn must be valid (i.e. if a tile is placed and is adjacent to tiles on both the x and y axes, both axes must form a valid word

__Bonus squares__:
- Letter multipliers are calculated before word multipliers 
- Center tile is a double word score
- Covering multiple word multipliers in one word applies both 
- Word score is doubled and then doubled again
- If multiple words are created, word score multipliers only apply to the word they are covered by
- Multipliers can contribute to multiple words if the tile covering them is a part of both words
- Play an S on a double word to create both AXES and PLAYS, both word scores are doubled
- Once a multiplier square is first played on it returns to normal 
- If you play SCORE and get a double word on it, adding an S to make SCORES would not get that multiplier
- If a player plays 7 tiles, the player scores a “bingo”, which yields an additional +50 points. These points are added on after tile multipliers
- When the draw bag is empty, players can opt to end the game for themselves. When this occurs, the following must happen:
- When all players opt to end the game, or all tiles are played, the game ends
- Any remaining tiles in any player’s hand total score is subtracted from their score. If any other players have used all of their letters, the remaining total score is added to these player’s scores.

### Table of contents:
- main.py
- modules: a folder of all python files needed to run the scrabble game:
     - init.py : facilitates our imports
     - ai_logic.py: creates and handles the AI object
     - board.py: creates the board and needed functions
     - condfig.py: creates and handles various config values
     - drawbag.py: creates the shuffled letter drawbag 
     - game_manager.py: creates the game_manager object to handle game status and flow
     - player.py: creates the player object to represent the user
     - rack.py: creates the letter rack object
     - scrabble_ui.py: draws all necessary visuals of the objects created and handles functionality of buttons and mouse clicks
     - start_screen.py: creates a welcome screen for the user to begin the game
     - tile.py: creates and handles all letter tiles in the game
     - utils.py: handles other functions needed for various modules
