# Write your code here
import math
from collections import namedtuple
from typing import Optional, Callable

INVALID_INPUT_ERROR_MSG = 'Invalid dimensions!'
MOVES = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
UserReadablePoint = namedtuple('UserReadablePoint', 'x y')
Point = namedtuple('Point', 'x y')


class Board:
    def __init__(self, dimensions: Point, position: Optional[Point] = None):
        self.dimensions = dimensions
        self.position = position
        self.cell_size = count_digits(self.dimensions.x * self.dimensions.y)
        self.placeholder = '_' * self.cell_size
        self.position_mark = ' ' * (self.cell_size - 1) + 'X'
        self.visited = ' ' * (self.cell_size - 1) + '*'
        self.matrix = [[self.placeholder for _j in range(self.dimensions.x)] for _i in range(self.dimensions.y)]

    def update_position(self, pos: Point):
        self.position = pos
        self.matrix[self.position.y][self.position.x] = self.position_mark

    def place_knight(self):
        msg = "Enter the knight's starting position: "
        point = handle_input(msg, lambda p: p.x in range(1, self.dimensions.x + 1) and p.y in range(1, self.dimensions.y + 1))
        pos = Point(*get_computer_readable_position(self, point))
        self.update_position(pos)

    def make_a_move(self, pos: Point):
        self.matrix[self.position.y][self.position.x] = self.visited
        self.update_position(pos)
        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if cell == self.position_mark:
                    continue
                if cell == self.visited:
                    continue
                self.matrix[i][j] = self.placeholder
        self.warnsdorff()

    def warnsdorff(self):
        for move in MOVES:
            row = self.position.y + move[0]
            col = self.position.x + move[1]
            if row < 0 or col < 0:
                pass
            elif row >= self.dimensions.y or col >= self.dimensions.x:
                pass
            elif self.matrix[row][col] == self.position_mark or self.matrix[row][col] == self.visited:
                pass
            else:
                count = 0
                for mv in MOVES:
                    r = row + mv[0]
                    c = col + mv[1]
                    if r < 0 or c < 0:
                        continue
                    elif c >= self.dimensions.x or r >= self.dimensions.y:
                        continue
                    elif self.matrix[r][c] == self.position_mark or self.matrix[r][c] == self.visited:
                        continue
                    else:
                        count += 1
                self.matrix[row][col] = ' ' * (self.cell_size - 1) + str(count)

    def get_user_friendly_coordinate(self) -> UserReadablePoint:
        return UserReadablePoint(self.position.x + 1, self.dimensions.y - self.position.y)

    def get_possible_moves(self):
        possible_moves = []

        for move in MOVES:
            temp = list(zip(self.position, move))
            for i, e in enumerate(temp):
                temp[i] = sum(list(e))
            pos = Point(*temp)

            if pos.y < 0 or pos.x < 0:
                continue
            if pos.y >= self.dimensions.y or pos.x >= self.dimensions.x:
                continue
            if self.matrix[pos.y][pos.x] == self.position_mark:
                continue
            if self.matrix[pos.y][pos.x] == self.visited:
                continue

            possible_moves.append(pos)

        return possible_moves

    def squares_visited(self):
        count = 0
        for row in self.matrix:
            for cell in row:
                if cell == self.visited or cell == self.position_mark:
                    count += 1
        return count

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
    dimensions = Point(*handle_input('Enter your board dimensions: ', lambda p: p.x > 0 and p.y > 0))
    return Board(dimensions)


def get_user_readable_position(board: Board, pos: Point) -> UserReadablePoint:
    return UserReadablePoint(pos.x + 1, board.dimensions.y - pos.y)


def get_computer_readable_position(board: Board, pos: UserReadablePoint) -> Point:
    return Point(pos.x - 1, board.dimensions.y - pos.y)


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
    board.warnsdorff()
    print(board)

    game_over = False
    while not game_over:
        possible_moves = board.get_possible_moves()

        if not possible_moves:
            if board.squares_visited() == board.dimensions.y * board.dimensions.x:
                print('What a great tour! Congratulations!')
                break
            else:
                print('No more possible moves!')
                print(f'Your knight visited {board.squares_visited()} squares!')
                break

        user_input = list(map(int, input('Enter your next move: ').split()))
        user_readable_point = UserReadablePoint(*user_input)
        pos = Point(*get_computer_readable_position(board, user_readable_point))

        if pos not in possible_moves:
            print('Invalid move! ')
            continue

        board.make_a_move(pos)
        print(board)


if __name__ == '__main__':
    main()
