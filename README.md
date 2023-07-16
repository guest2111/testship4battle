![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)
---

Hello visitor,

let me shortly explain to you the creation and structure of this program.

---

# Table of Content
---
 * [Preliminary Considerations](#preliminary-considerations)
   * [First Idea of Responsive Game Play](#first-idea-of-responsive-game-play)
   * [Game Execution Logic](#game-execution-logic)
   * [Needed Methods](#needed-methods)
 * [Appearance](#appearance)
 * [Rules](#rules)
 * [Features](#features)
 * [Possible Features in Future](#possible-features-in-future)
 * [Testing](#testing)
   * [Device Tests](#device-tests)
   * [Validator Test](#validator-test)
   * [Systematical Tests](#systematical-tests)
 * [Deployment](#deployment)
 * [Bugs](#bugs)
   * [Solved Bugs](#solved-bugs)
   * [Open Bugs](#open-bugs)
 * [Credits](#credits)
   * [Code Ideas](#code-ideas)
 * [Final Words](#final-words)
---
# Preliminary considerations
Before starting with the actual code, I tried my first idea of how to interact with the game with the folowing proof of concept. After that I have started with some basic considerations of which classes and methods might be necessary. Just after that I tried to deploy the test code on a public website. I failed on every alternative to Heroku since I noticed to late, that the python interactive terminal is not a standard feature of Heroku or others but was build with the additional html- and javascript files. Over web search I could not find any solution and advice - probably because it is a rare usecase.

## First Idea of Responsive Game Play
The first idea as a possible interaction with the game was to catch any keyboard input and call for the desired method. The printing of input I have disabled to fully concentrate on the map. Thus it was "seemingly" possible to navigate by the keyboards arrow keys over the map and target the wanted position.

Such example can be seen in the [test.py file](/test.py).

It would have been possible to fully individually decide, which inputs are shown to the user and which not. But after deployment to Heroku I noticed, that it is not possible to use the module `pynput` and `subprocess` as intented.

So I decided to give the command for targeted field in one input as `<row><column>` for example `b3`. Additional functionality can be reached by entering `/` as first sign of input. This allows to keep the printing and dialogs while running the game as short as possible and have the position of the map mostly positioned on the same area on the screen. (Read about the feature [`/automatic`](#feature-automatic))

For an easier accesible map some "decorators" are added around the core map. The exact position can be then described by a letter for the row and number for the column.

The core field would be:

```
   . . .
   . . . 
   . . .
```

And the field additionally with decorators:
```
   a b c    
 1 . . . 1  
 2 . . . 2  
 3 . . . 3  
   a b c
   ```

## Game Execution Logic
First the user will be asked a couple of questions, which are automatically answered if the user does not give an answer on first question. They are determining the user's name, the size of map and the skill of the opposing computer.

According to the chosen answers an object containing the rules is created, then one map for the player and one map for the opponent.

When the game starts a while loop opens until one map answers "Game over". While the game is running a player has its turn until a bad guess. If he had no luck opening a position of a ship, the oppenent can do his turn.

## Needed methods
Before the start of coding I made considerations in the separate file [considerations.txt'](/considerations.txt). It seemed usuful to have following classes and methods:

- class Field:
    - field data, 2D-matrix, containing ship positions
    - history data, 2D-matrix, containing opened positions

- class Turn with methods:
    - asking positions
    - discover positions

- class Opponent AI:
    1. Simple: random choice
    2. Advanced: chosing position next to hit
    3. Hard: using diagonal pattern
    - AddOn: start guessing at borders if ship deployment is done by player manually, since that would be good strategy

While programming the set up has been changed. The Field class has remained and is providing the data containing structures to the new class `BattleMap`, which is now the main class containing most interaction methods. It is meant, that a request towards the map is implemented in the `BattleMap` class.

The game loop, the AI strategies and the dialogs with the user, while game is running, are kept in the `Game` class. Most part is dedicated to the routines, which give some strategy to the AI as targeting a hit ship which is not sunk yet. But other methads are even more imported since they provide the interaction with the user `ask_position`. The afore mentioned main while loop is implemented in the `start_game` method. It is finished if one of the "turn" methods are giving permission to continue.

# Appearance
Game start:  
![game start](/docu/maps_game_start.png)

Appearance of map while battle is going (players map left and opponents maps right):  
![players map](/docu/players_map.png)
![opponents map](/docu/opponents_map.png)

Example of big map:  
![big map](/docu/map_biggest.png)

# Rules
On this Battleship game it is possible to shoot again on same turn right after a successful hit. Ships have different lengths. When a ship is sunk, all directly adjancted fields are opened since it is not allowed to position ships so close to each other, that they can touch each other. 

# Features
- It is possible to change the size of map by choosing the amount of rows and columns indepentently before the game starts.
- One can choose the difficulty of computer.
- This options are chosen by default, if the player does not give his name on first question. If wrong input is given a default value is chosen as well. The user get's notified.
- A user can <a id="feature-automatic"></a> choose to open a random field by entering `/automatic` (or just `/` since there are anyway not much special commands) and continue doing so by just pushing repeatedly the Enter key.
- Anytime a user can quit the game and open both maps by entering `/quit` instead of a position or the confirmation of auto mode.
- The computer can choose randomly, or next to a hit and even considering the direction of the ship if it is visible (but not if it is just single hit) or choosing on a diagonal pattern favouring positions in the middle of the field if choosen so.

# Possible Features in Future
- Listing the sunk, hit and total amount of ships per length next to the map.  
This would allow to have fast overview of the progress. Especialy on big fields it would help.

- Asking for preferred visualisation signs.

- Positioning the ship manually before start if wanted.

- Add another strategy to the computer oponent, which considers the actual opened positions due to sunk ships in combination with the diagonal pattern. E.g. if in the case all ships of length 2 and 3 are sunk, one could guess `f2` and directly `f6` and skipping the `f4` which would come in a simple diagonal pattern as well. Targeting crossings of unopened positions whould be more beneficial than targeting only lines (in the case all souroundings is already open). This is more likely to find a ship since there are more combinations to position the ship there. Such strategy would be very difficult to implement.


# Testing
## Device Tests
The game runs on:  

    - Firefox 115.0.1 (64-bit) as snap on  
    Linux Kubuntu 5.19.0-46-generic #47~22.04.1-Ubuntu x86_64 GNU/Linux

    - Chromium Version 91.0.4472.164 (Developer Build) stable (64-bit) on  
    Linux OrangeOS  5.10.110-rockchip-rk3588 #1.1.4 aarch64 GNU/Linux

The game does not rund:

    - Firefox 115.0.2 on  
    Windows 11 Home, 12th Gen Intel(R) Core(TM) i5-1235U, x64-based processor

## Validator Test
Both code files [run.py](/run.py) and [classes/game.py](/classes/game.py) have been tested with the *pep8 CodeInstitute* validator. All issues have been resolved.

## Systematical Tests

| Test name | Decription | Behaviour | Result |
| --------- | ---------- | --------- | ------ |
| Enter name | Entering a name on first question | - "Hello {name}" <br />- Asking for size of map | passed |
| Enter no name | Entering empty string on first question | - start game with 7x7 map | passed |
| Enter various sizes | 5, 9, 14, 19, 21, 26, [5,13], [19, 7], [12,25] | - map created and ships deployed <br /> - no error | passed |
| Enter wrong size | strings as 'd', 'df' | - anser "Your input could not be processed" <br /> - "A size of 7x7 will be set" <br /> - Question about difficulty | passed |
| Enter wrong size | too small number | - anser "Adjusted row amount to minimal value of 4" <br /> - "Adjusted row amount to minimal value of 5" <br /> - Question about difficulty | passed |
| Enter wrong size | too small number for row (4)  | - anser "Adjusted row amount to minimal value of 5" <br /> - Question about difficulty | passed |
| Enter wrong size | too small number | - anser "Adjusted row amount to maximal value of 26" <br /> - "Adjusted row amount to maximal value of 26" <br /> - Question about difficulty | passed |
| Enter wrong size | too small and too big (`[3,33]`) | - anser "Adjusted row amount to minimal value of 4"  <br /> "Adjusted column amount to maximal value of 26" <br /> - Question about difficulty | passed |
| Questions difficulty | entering nothing | - answer: "I choose "Advanced" for you.
" <br /> - visualisation signs for both maps - start of game | passed |
| Questions difficulty | entering wrong signs or too small or too high | - answer: "I choose "Advanced" for you.
" <br /> - visualisation signs for both maps - start of game | passed |
| Easy AI |  | - chooses randomly | passed |
| Advanced AI | | - chooses randomly and continue with hit ship until sunk | passed |
| Hard AI | | - if hit then target ship until sunk <br /> - diagonal pattern | passed |
| auto mode on | `/auto` or `/` or `/automatic` | - position is chosen randomely <br /> - next question about to reconfirm | passed |
| auto mode off | enter any sign except `/quit` | - next question is possition | passed |
| quitting | `/quit` instead of position | - Game is finished and lost | passed |
| quitting | `/quit` instead of confirmation of auto mode | - Game is finished and lost | passed |
| enter position | correct position | - position discoverd | passed |
| enter position | wrong position | - reask | passed |
| on hit | turn continues without opponent doing its turn | - ask again | passed |
| finish game | both maps are displayed | - all ships visible <br /> - state of ships is visible | passed |


# Deployment
Easiest way is to install python 3, install the modules listed in the [requirements.txt](/requirements.txt) via pip, download the project from Github and run the [run.py](/run.py) file.

If one wants to deploy his project publicly, for example on Heroku. He must open an account there and add following buildpacks to the app:

1. heroku/python
2. heroku/nodejs

Additionally he has to set a *Config Var* called *PORT* and give it the value *8000*.

# Bugs
While writing and testing various bugs have been occured and corrected.

# Solved Bugs
- The file [requirements.txt](/requirements.txt) was first created with `git list > requirements.txt` but in this case the format of the text file is not as expected. It must be done with `git freeze > requirements.txt`.

- On first implementation the initial position of a ship was for row and column in between *0* and *number_<rows/columns> - length_ship*. This makes it possible that a ship is positioned at the right or lower border of the map.  
Solution was to first decide for a direction and then reduce the area for initial position accordingly.

- There were some mistakes of mixing *row* and *column* coordinates. Numpy arrays take indices as `[row, column]` which is a bit unintuitive.

- When refactoring the diagonal pattern in its own method the `return` command was missing. So the `computer_choice()` was still going to do a random choice.

- When the map size is changed by the user, the amount of ships is recalculated. That should ensure that there is not too much open space on the map.  
An approach of fitting as many ships as happens is not much useful, because one has then too many or to few long ships.  
The calculation of the amount of ships is done approximately. By this fix it is mostly succesful.

- The command `/quit` was meant to work anytime. But since the `random_choice()` was called anyway. This leads to the possibilty of hitting a ship and getting a second choice. The `/quit` command is not revertable but has to wait until an unlucky choice. But if the hit was the last necessary hit, the player won anyway.  
This behaviour was corrected by allowing to return the special position `(-1, -1)`. Which is just ignored. So basically no choice is done and the `/quit` command is effective.

- The method `_target_unsunk_but_hit_ship()` was done not perfectly. The direction was guessed and if in that direction all positions were opened, no position could be guessed and the hit ship was not targeted anymore.  
Solution was to check in the `get_direction_of_hit()` method, whether one position is not possible to choose because of already openend positions and return the other position. The ensures to have always a possible and by that useful direction in which the actual position is guessed.

# Open
It is difficult to use create a simple formula to calculate the amount of ships for a map in way, that not much free space is left. It is possible that on some sizes not all needed ships are deployed and the code breaks with a message. If so, one can rerun the programm and enter again the sizes or enter different sizes.

Lately this was not observed anymore but still it can not be excluded.

# Credits
I list shortly the sources, how to achive something. Some of them are not used anymore in the latest version.

## Code Ideas
- [https://www.statology.org/numpy-array-to-int/](https://www.statology.org/numpy-array-to-int/)  
Here it is described how to transform a numpy array into a numpy array  of type integer. But I later I remembered to just specify the `dtype="int"` while creating it.

- [https://numpy.org/doc/stable/reference/generated/numpy.argwhere.html](https://numpy.org/doc/stable/reference/generated/numpy.argwhere.html)  
Getting the indices for an numpy array, whichs value fulfill a given condition.

- [https://docs.python.org/3/library/string.html#string.ascii_lowercase](https://docs.python.org/3/library/string.html#string.ascii_lowercase)  
Importing a string containing alphabet letters. This is faster approach than typing them manually and additionally failsafe.

- [https://dev.to/ra1nbow1/8-ways-to-add-an-element-to-the-beginning-of-a-list-and-string-in-python-925](https://dev.to/ra1nbow1/8-ways-to-add-an-element-to-the-beginning-of-a-list-and-string-in-python-925)  
Here are some useful ways how to change a list or a string.

- In the [test.py](/test.py) I have needed the help given on following sources:

    - [https://pynput.readthedocs.io/en/latest/keyboard.html](https://pynput.readthedocs.io/en/latest/keyboard.html)  
    Here it is described how to catch the keyboard events and handle the input.

    - [https://stackoverflow.com/questions/49578801/preventing-key-presses-from-appearing-on-screen](https://stackoverflow.com/questions/49578801/preventing-key-presses-from-appearing-on-screen)  
    With the `subprocess` module it is possible to change the terminals settings for `echo`. This is not working on the terminal on the webpage prepared by Codeinstitute. Maybe the terminal echo setting requires a direct graphical OS. 

# Final Words
In the end I can say, I could build the game to be handled quickly. One input line and no unneeded responses make the game play fast. For bigger fields it is even faster to enter a targeted position by giving the coordinates rather than pushing multiple times on the arrow keys and navigate to the new position. For this case it was anyway planned to allow additional the coordinate input. Handling the various ways of keyboard input would have been more challenging.
