import pytest
from five_in_a_row import (
    initialiseBoard, initialiseBoardTest, assignOtherPiece,
    Coord, White, Black, checkWin, isBoardFull, getAIMove
)

def test_initialise_board():
    board = initialiseBoard()
    assert len(board) == 15 * 15
    assert all(cell is None for cell in board.values())

def test_assign_other_piece():
    assert isinstance(assignOtherPiece(White()), Black)
    assert isinstance(assignOtherPiece(Black()), White)

def test_coord_valid():
    coord = Coord(5, 5)
    assert coord.x == 5 and coord.y == 5

def test_coord_invalid_x():
    with pytest.raises(ValueError):
        Coord(0, 5)

def test_coord_invalid_y():
    with pytest.raises(ValueError):
        Coord(5, 16)

def test_check_win_horizontal():
    board = initialiseBoard()
    for i in range(5):
        board[Coord(x=1+i, y=1)] = White()
    assert checkWin(board) is True

def test_check_win_vertical():
    board = initialiseBoard()
    for i in range(5):
        board[Coord(x=1, y=1+i)] = Black()
    assert checkWin(board) is True

def test_check_win_diagonal():
    board = initialiseBoard()
    for i in range(5):
        board[Coord(x=1+i, y=1+i)] = White()
    assert checkWin(board) is True

def test_is_board_full_false():
    board = initialiseBoard()
    assert isBoardFull(board) is False

def test_is_board_full_true():
    board = initialiseBoardTest()
    board[Coord(15, 15)] = White()
    assert isBoardFull(board) is True

def test_ai_moves_on_empty_board():
    board = initialiseBoard()
    move = getAIMove(board, ai=White(), player=Black())
    assert isinstance(move, Coord)
    assert board[move] is None