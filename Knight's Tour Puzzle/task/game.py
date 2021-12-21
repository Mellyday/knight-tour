# Write your code here
import math
import copy
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
        self.count = 1

    def update_position(self, pos: Point, token: str = 'mark'):
        self.position = pos
        if token == 'mark':
            self.matrix[self.position.y][self.position.x] = self.position_mark
        if token == 'number':
            self.matrix[self.position.y][self.position.x] = str(self.count).rjust(self.cell_size)
            self.count += 1

    def place_knight(self):
        msg = "Enter the knight's starting position: "
        point = handle_input(msg, lambda p: p.x in range(1, self.dimensions.x + 1) and p.y in range(1, self.dimensions.y + 1))
        pos = Point(*get_computer_readable_position(self, point))
        self.update_position(pos)

    def get_possible_moves(self, pos: Optional[Point] = None):
        possible_moves = []

        if pos is None:
            pos = self.position

        for move in MOVES:
            temp = list(zip(pos, move))
            for i, e in enumerate(temp):
                temp[i] = sum(list(e))
            new_pos = Point(*temp)

            if new_pos.y < 0 or new_pos.x < 0:
                continue
            if new_pos.y >= self.dimensions.y or new_pos.x >= self.dimensions.x:
                continue

            if self.matrix[new_pos.y][new_pos.x] == self.placeholder:
                possible_moves.append(new_pos)

        return possible_moves

    def check_victory(self):
        for row in self.matrix:
            for cell in row:
                if cell == self.placeholder:
                    return False
        return True

    def undo_position(self, last_pos):
        self.matrix[self.position.y][self.position.x] = self.placeholder
        self.position = last_pos
        self.count -= 1

    def solve_no_mutation(self):
        bo = copy.deepcopy(self)
        possible_moves = bo.get_possible_moves()

        if bo.check_victory():
            return True

        for move in possible_moves:
            saved_pos = Point(*bo.position)
            bo.update_position(move, 'number')
            if bo.solve():
                return True
            bo.undo_position(saved_pos)

        return False

    def solve(self):
        possible_moves = self.get_possible_moves()

        if self.check_victory():
            return True

        for move in possible_moves:
            saved_pos = Point(*self.position)
            self.update_position(move, 'number')
            if self.solve():
                return True
            self.undo_position(saved_pos)

        return False

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
        self.print_warnsdorff()

    def print_warnsdorff(self):
        bo = copy.deepcopy(self)
        possible_moves = bo.get_possible_moves()
        for move in possible_moves:
            pos = Point(*move)
            count = bo.warnsdorff_count(pos)
            bo.matrix[move.y][move.x] = ' ' * (bo.cell_size - 1) + str(count)
        print(bo)

    def warnsdorff_count(self, pos: Point):
        count = len(self.get_possible_moves(pos))
        return count

    def get_user_friendly_coordinate(self) -> UserReadablePoint:
        return UserReadablePoint(self.position.x + 1, self.dimensions.y - self.position.y)

    def play(self):
        while True:
            possible_moves = self.get_possible_moves()

            # This block of code end the game if the game is over.
            if not possible_moves:
                cell_number = self.dimensions.y * self.dimensions.x
                if self.squares_visited() == cell_number:
                    print('What a great tour! Congratulations!')
                    break
                else:
                    print('No more possible moves!')
                    print(f'Your knight visited {self.squares_visited()} squares!')
                    break

            user_input = list(map(int, input('Enter your next move: ').split()))
            user_readable_point = UserReadablePoint(*user_input)
            pos = Point(*get_computer_readable_position(self, user_readable_point))

            if pos not in possible_moves:
                print('Invalid move!', end='')
                continue

            self.make_a_move(pos)

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
        # Error will be raised if:
        # 1. User enter non-digit. eg. 'a 5' # ValueError
        # 2. User enter only one coordinate eg. '5' # TypeError
        # 3. User enter more than two coordinate '1 5 6' # TypeError
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

    while True:
        answer = input('Do you want to try the puzzle? ')

        if answer == 'y':
            if board.solve_no_mutation():
                board.print_warnsdorff()
                board.play()
            else:
                print('No solution exists!')
            break

        if answer == 'n':
            board.update_position(board.position, 'number')
            if board.solve():
                print("Here's the solution!")
                print(board)
            else:
                print('No solution exists!')
            break

        print('Invalid input!')


if __name__ == '__main__':
    main()
