import random, sys

from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias, Optional, Dict, Literal, Optional

'''
https://code.activestate.com/recipes/384122-infix-operators/
'''
class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

pipe = Infix(lambda x,f: f(x))

'''
eprint puts all errors into a textfile for review
'''
eprint = lambda msg: print(msg, file=sys.stderr)

''' 
Piece = {White,Black}
'''
@dataclass(frozen=True, eq=True)
class White:
    letter : str = "W"

    def __str__(self) -> str:
        return "White"

@dataclass(frozen=True, eq=True)
class Black:
    letter : str = "B"

    def __str__(self) -> str:
        return "Black"

Piece : TypeAlias = White | Black

'''
Cell = Piece ∪ {None}
'''
Cell = Optional[Piece]

'''
(XCoord:P)/(XCoord={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15})
XCoord = {x: Uchar │ x ≤ 15}
'''
XCoord = int

'''
(YCoord:P)/(YCoord={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15})
YCoord = {x: Uchar │ x ≤ 15}
'''
YCoord = int

'''
Coord = Xcoord ∪ YCoord
'''
@dataclass(frozen=True, eq=True)
class Coord:
    x: XCoord
    y: YCoord

    def __post_init__(self):
        if not (1 <= self.x <= 15):
            raise ValueError(f"Invalid x-coordinate: {self.x}. Must be between A and O.")
        if not (1 <= self.y <= 15):
            raise ValueError(f"Invalid y-coordinate: {self.y}. Must be between 1 and 15.")
        
    def __str__(self) -> str:
        return f"Coordinate {self.x,self.y}"

'''
Board = dict <Coord, Cell>
'''
Board = Dict[Coord, Cell]

'''
MenuOption = {SinglePlayer,Multiplayer,Quit}
'''
class MenuOption(Enum):
    Singleplayer = 1
    Multiplayer = 2
    Quit = 3

    @staticmethod
    def parseMenuOption(s:str) -> Optional['MenuOption']:
        """
        parseMenuOption is a function
        which parses an input string from the user to an Optional MenuOption value

        Parameters:
            s (String) : An input string via stdinp

        Returns:
            Optional[MenuOption] : The result of a valid MenuOption value or 
            returns None to create an error
        """
        match s.strip().upper():
            case "1" | "ONE" | "SINGLE" | "SINGLEPLAYER" | "ONE PLAYER":
                return MenuOption.Singleplayer
            case "2" | "TWO" | "MULTI" | "MULTIPLAYER" | "TWO PLAYER":
                return MenuOption.Multiplayer
            case "3" | "THREE" | "QUIT" | "EXIT" | "CLOSE":
                return MenuOption.Quit
            case _:
                return None

main_title : str = """
+-----------------------+
| Gomoku                |
| by Shea Conlon-Swain  |
| ID No. 23129542       |
| S2 2024/25            |
+-----------------------+
"""

menu_string : str = """
+-----------------------+-----------------------+
| Main Menu                                     |
| Please select a menu option [1-3]             |
| 1: Singleplayer                               |
| 2: Multiplayer                                |
| 3: Quit                                       |
+-----------------------+-----------------------+
>>> """

piece_choice_string : str = """
+-----------------------+-----------------------+
| Player 1, choose your piece!                  |
| Please select a menu option [1-2]             |
| 1: White                                      |
| 2: Black                                      |
+-----------------------+-----------------------+
>>> """

def displayMainTitle() -> None:
    """
    displayMenuTitle is a subroutine
    which simply prints the main title string to the command line

    Parameters:
        None

    Returns:
        None
    """
    main_title |pipe| print
    return

def navigateMainMenu() -> None:
    """
    navigateMainMenu is a subroutine
    which allows for the program to go to the specified menu option

    Parameters:
        None

    Returns:
        None
    """
    displayMainTitle()
    while True:
        promptMenuInput() |pipe| goToSelectedOption

def promptMenuInput() -> MenuOption:
    """
    promptMenuInput is a 'function'
    which takes a user input for the main menu selection

    Parameters:
        Input string from the user via stdinp (Not technically an input)

    Returns:
        option (MenuOption) : The particular option the user requests. Can
            result in a None value being returned if the user has made an invalid
            request
    """
    while True:
        match menu_string |pipe| input |pipe| MenuOption.parseMenuOption:
            case option if type(option) == MenuOption:
                return option
            case _:
                "ERROR: Not a valid menu option" |pipe| eprint

def goToSelectedOption(option:MenuOption) -> None:
    """
    promptMenuInput is a subroutine
    which directs the program to the correct function/subroutine relating to
    the selected game mode

    Parameters:
        option (MenuOption) : The particular option the user has requested

    Returns:
        None
    """
    match option:
        case MenuOption.Singleplayer:
               playSingleGame()
        case MenuOption.Multiplayer:
               playMultiGame()
        case MenuOption.Quit:
            """
            Closing Gomoku...
            Thanks for playing!
            """ |pipe| print
            0 |pipe| sys.exit
            '''Closes the game and provides a "0" as the exit code,
            meaning that no errors have occured'''

def playSingleGame() -> None:
    """
    playSingleGame is a subroutine
    which plays the singleplayer game with 1 human player and the computer

    Parameters:
        Input string from the user via stdinp (Not technically an input)

    Returns:
        None
    """
    main_board : Board = initialiseBoard()
    playerPiece : Piece = getPieceChoiceInput()
    opponentPiece : Piece = assignOtherPiece(playerPiece)
    currentPiece : Piece = White()
    while True:
        if currentPiece == playerPiece:
            displayBoard(main_board)

        if currentPiece == opponentPiece:
            inputCoord = getAIMove(main_board, opponentPiece, playerPiece)
            print(f"AI chooses: {chr(ord('A') + inputCoord.x - 1)}{inputCoord.y}")
        else:
            inputCoord : Coord = parseCoordValue()

        match main_board.get(inputCoord):

            case White() | Black():
                "ERROR: Piece already placed here" |pipe| eprint

            case None:
                main_board.update({inputCoord: currentPiece})
                if checkWin(main_board) == True:
                    break
                match currentPiece:
                    case White():
                        currentPiece = Black()
                    case Black():
                        currentPiece = White()

def playMultiGame() -> None:
    """
    playMultiGame is a subroutine
    which plays the multiplayer game with 2 human players

    Parameters:
        Input string from the user via stdinp (Not technically an input)

    Returns:
        None
    """
    main_board : Board = initialiseBoard()
    playerPiece : Piece = getPieceChoiceInput()
    opponentPiece : Piece = assignOtherPiece(playerPiece)
    currentPiece : Piece = White()
    while True:
        displayBoard(main_board)
        f"{currentPiece}'s turn!" |pipe| print
        inputCoord : Coord = parseCoordValue()

        match main_board.get(inputCoord):

            case White() | Black():
                "ERROR: Piece already placed here" |pipe| eprint

            case None:
                main_board.update({inputCoord: currentPiece})
                if checkWin(main_board) == True or isBoardFull(main_board):
                    break
                match currentPiece:
                    case White():
                        currentPiece = Black()
                    case Black():
                        currentPiece = White()


def parseCoordValue() -> Coord:
    """
    parseCoordValue is a 'function'
    which takes a coordinate from the player and parses it into
    a usable Coord data model, ready to place the piece onto the
    Go board

    Parameters:
        Input string from the user via stdinp (Not technically an input)

    Returns:
        coord (Coord) : The resulting coord data model from the user's
            input with an XCoord and YCoord value
    """
    while True:
        try:
            coordInput : str = input("Enter a coordinate (e.g., A5): ").strip().upper()
            if len(coordInput) < 2 or not coordInput[0].isalpha() or not coordInput[1:].isdigit(): 
                raise ValueError
            x = ord(coordInput[0]) - ord('A') + 1
            y = int(coordInput[1:])
            return Coord(x=x, y=y)
        except ValueError:
            "ERROR: Not a valid coordinate" |pipe| eprint

def getPieceChoiceInput() -> Piece:
    """
    getPieceChoiceInput is a 'function'
    which takes a piece colour selection from the first player,
    to allow the AI or second player to take the other colour

    Parameters:
        Input string from the user via stdinp (Not technically an input)

    Returns:
        piece (Piece) : The corresponding colour of the piece that the
            first player has selected
    """
    while True:
        match input(piece_choice_string).strip().upper():
            case "1" | "WHITE":
                return White()
            case "2" | "BLACK":
                return Black()
            case _:
                "ERROR: Not a valid piece option" |pipe| eprint

def assignOtherPiece(p:Piece) -> Piece:
    """
    parseCoordValue is a function
    which assigns the remaining piece to the other player/AI

    Parameters:
        p (Piece) : The first player's piece colour choice

    Returns:
        piece (Piece) : The remaining colour option to be used by
            the second player/AI
    """
    match p.letter:
        case "W":
            return Black()
        case "B":
            return White()
        
def getAIMove(b: Board, ai: Piece, player: Piece) -> Coord:
    """
    getAIMove is a function
    which allows for the AI to make a move based on a few basic
    channels of information. It can either:
     - Place a piece in a random location
     - Place a piece to benefit it's own game
     - Place a piece to block the human player

    Parameters:
        b (Board) : The current board state
        ai (Piece) : The piece colour used by the AI for assessing currently placed
            pieces
        player (Piece) : The piece colour used by the human for assessing currently 
            placed pieces

    Returns:
        coord (Coord) : The choice of coordinate for the AI to place their piece at
    """
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    def valid_coord(x: int, y: int) -> bool:
        return 1 <= x <= 15 and 1 <= y <= 15

    def five_in_line(start: Coord, dx: int, dy: int) -> list[tuple[Coord, Cell]]:
        return [
            (Coord(start.x + i * dx, start.y + i * dy), b.get(Coord(start.x + i * dx, start.y + i * dy)))
            for i in range(5)
            if valid_coord(start.x + i * dx, start.y + i * dy)
        ]

    def find_critical_move(target_piece: Piece) -> Optional[Coord]:
        critical_lines = [
            line for coord, cell in b.items() if cell == target_piece
            for dx, dy in directions
            if len(line := five_in_line(coord, dx, dy)) == 5
            and sum(1 for _, c in line if c == target_piece) == 4
            and any(c is None for _, c in line)
        ]
        empty_spots = [coord for line in critical_lines for coord, c in line if c is None]
        return empty_spots[0] if empty_spots else None

    return (
        find_critical_move(ai)        # Try to win
        or find_critical_move(player) # Try to block
        or next((coord for coord, cell in b.items() if cell is None), None)  # Else, pick any empty cell
    )


    '''
    # Very basic AI

    empty_coords = [coord for coord, piece in b.items() if piece is None]
    return random.choice(empty_coords) if empty_coords else None'''
        
def checkWin(b:Board) -> bool:
    """
    checkWin is a function
    which checks the current state of the board to see if there are 5 pieces
    in a row from either player

    Parameters:
        b (Board) : The current board state

    Returns:
        boolean (bool) : True if there is a winning state, false if there is no
            current winning state
    """

    # Extremely long winded way of doing this but oh well
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    def is_winning_line(start: Coord, dx: int, dy: int, piece: Piece) -> bool:
        for i in range(5):
            x = start.x + i * dx
            y = start.y + i * dy
            if not (1 <= x <= 15 and 1 <= y <= 15):
                return False
            if b.get(Coord(x, y)) != piece:
                return False
        return True

    winning_positions = (
        (coord, dx, dy, piece)
        for coord, piece in b.items()
        if piece is not None
        for dx, dy in directions
    )

    winner = next(
        (
            piece
            for coord, dx, dy, piece in winning_positions
            if is_winning_line(coord, dx, dy, piece)
        ),
        None,
    )

    if winner:
        f"{winner} wins!" |pipe| print
        return True

    return False

def isBoardFull(b: Board) -> bool:
    for x_value in range(1,16): 
        for y_value in range(1,16):
            coord = Coord(x=x_value,y=y_value)
            if b.get(coord) == None:
                return False
    "Game draw!" |pipe| print
    return True

def initialiseBoard() -> Board:
    """
    initialiseBoard is a subroutine
    which creates a fresh version of the board to be used for a new game

    Parameters:
        None

    Returns:
        board (Board) : The fresh board, ready to be used in either a 
            singleplayer or multiplayer game
    """
    board: Board = {}
    for x_value in range(1,16): 
        for y_value in range(1,16):
            coord = Coord(x=x_value,y=y_value)
            board[coord] = None
    return board

def initialiseBoardTest() -> Board:
    """
    A test version of initialiseBoard, used to test for a full board
    """
    board: Board = {}
    for x_value in range(1,16): 
        for y_value in range(1,16):
            coord = Coord(x=x_value,y=y_value)
            board[coord] = White
    return board

def displayBoard(b: Board) -> None:
    """
    displayBoard is a subrountine
    which displays the current state of the board, with all the positions
    of the pieces

    Parameters:
        board (Board) : The current board state

    Returns:
        None
    """
    "   " + "   ".join(chr(ord('A') + i) for i in range(15)) |pipe| print
    "   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |" |pipe| print
    for y in range(1, 16):
        row : str = str(y) + "  "
        row = row[0:3]
        for x in range(1, 16):
            cell = b[Coord(x, y)]
            if isinstance(cell, White): row += 'W---'
            elif isinstance(cell, Black): row += 'B---'
            else: row += '+---'
        row |pipe| print
        "   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |" |pipe| print

if __name__ == "__main__":
    navigateMainMenu()