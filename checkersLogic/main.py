from checkersLib.checkers import CheckersInterface
from enum import Enum

class PIECE(Enum):
    EMPTY = 0
    WHITE_PAWNS = 1
    BLACK_PAWNS = 2
    WHITE_PAWNS_PROMOTED = 3
    BLACK_PAWNS_PROMOTED = 4

BOARD_ARRAY = [[PIECE.EMPTY.value for x in range(8)] for x in range(8)]

START_BOARD_ARRAY = [[1, 0, 1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0, 1, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 2, 0, 2, 0, 2, 0, 2],
                     [2, 0, 2, 0, 2, 0, 2, 0],
                     [0, 2, 0, 2, 0, 2, 0, 2]]

BOARD_ARRAY = START_BOARD_ARRAY

# print(BOARD_ARRAY)

def move_white_paws(type, fromWhere, toWhere):
    if BOARD_ARRAY[toWhere[0]][toWhere[1]] != 0:
        BOARD_ARRAY[toWhere[0]][toWhere[1]] = type
        BOARD_ARRAY[fromWhere[0]][fromWhere[1]] = 0

CI = CheckersInterface()
# CI.set_piece(42, 86)
# CI.set_square(47)
CI.start()
print 'Now we can continue running code while mainloop runs!'
CI.set_piece(42, 86)
CI.set_square(47)