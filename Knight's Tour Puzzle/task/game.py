# Write your code here
import math
from collections import namedtuple
from typing import Optional, Callable

INVALID_INPUT_ERROR_MSG = 'Invalid dimensions!'
Dimensions = namedtuple('Dimensions', 'x y')
Position = namedtuple('Position', 'x y')
Point = namedtuple('Point', 'x y')


class Board:
    def __init__(self, dimensions: Dimensions, position: Optional[Position] = None):
        self.dimensions = dimensions
        self.position = position
        self.cell_size = count_digits(self.dimensions.x * self.dimensions.y)
        len_of_placeholder = count_digits(self.dimensions.x * self.dimensions.y)
        self.matrix = [['_' * len_of_placeholder for _j in range(self.dimensions.x)] for _i in range(self.dimensions.y)]

    def get_x_dim(self):
        return self.dimensions.x

    def get_y_dim(self):
        return self.dimensions.y

    def place_knight(self):
        msg = "Enter the knight's starting position: "
        point = handle_input(msg, lambda p: p.x in range(1, self.dimensions.x + 1) and p.y in range(1, self.dimensions.y + 1))
        self.position = Position(convert_coordinate(point.x, self.dimensions.y, 'col'), convert_coordinate(point.y, self.dimensions.y, 'row'))
        self.matrix[self.position.y][self.position.x] = ' ' * (self.cell_size - 1) + 'X'

    def mark_possible_moves(self):
        moves = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
        for move in moves:
            row = self.position.y + move[0]
            col = self.position.x + move[1]
            if row < 0 or col < 0:
                pass
            else:
                try:
                    self.matrix[row][col] = ' ' * (self.cell_size - 1) + 'O'
                except IndexError:
                    pass

    def __str__(self) -> str:
        result = []
        len_of_left_border = count_digits(self.dimensions.y)
        len_of_horizontal_border = self.dimensions.x * (self.cell_size + 1) + 3
        top_header = [''.rjust(len_of_left_border), '-' * len_of_horizontal_border, '\n']
        result.extend(top_header)

        main_lines = []
        row_num = self.dimensions.y
        for row in self.matrix:
            main_lines.append(f'{str(row_num).rjust(len_of_left_border)}| {" ".join(row)} |\n')
            row_num -= 1
        result.extend(main_lines)

        footer = [''.rjust(len_of_left_border), '-' * len_of_horizontal_border, '\n']
        result.extend(footer)

        len_of_bottom_row_leading_spaces = len_of_left_border + 2
        num_footer = [' ' * len_of_bottom_row_leading_spaces, ' '.join([str(num).rjust(self.cell_size) for num in range(1, self.dimensions.x + 1)])]
        result.extend(num_footer)
        return ''.join(result)


def handle_input(msg: str, condition: Callable):
    while True:
        try:
            user_input = input(msg)
            point = Point(*tuple(map(int, user_input.split())))
            if condition(point):
                return point
            print(INVALID_INPUT_ERROR_MSG)
        except (ValueError, TypeError):
            print(INVALID_INPUT_ERROR_MSG)


def make_board() -> Board:
    dimensions = Dimensions(*handle_input('Enter your board dimensions: ', lambda p: p.x > 0 and p.y > 0))
    return Board(dimensions)


def convert_coordinate(coord, row_len, row_or_col):
    """
    @params
    :param coord: raw coordinate from user input
    :param row_len: number of rows of the board
    :param row_or_col: the string 'row' if you are converting row, and the string 'col' if you are converting col
    :return: an index in the form of integer
    """
    if row_or_col == 'row':
        return row_len - coord
    if row_or_col == 'col':
        return coord - 1


def count_digits(num):
    """
    This function return the number of digit num has.
    eg. 4949 has 4 digits, 42 has 2 digits
    :param num: an integer
    :return: the number of digits num has
    """
    return int(math.log10(num)) + 1


def main():
    board = make_board()
    board.place_knight()
    board.mark_possible_moves()
    print('Here are the possible moves:')
    print(board)


if __name__ == '__main__':
    main()
