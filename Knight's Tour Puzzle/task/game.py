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

    def move_is_illegal(self, pos: Point):
        """
        IMPORTANT! this does not flag all illegal moves. It only flag illegal moves in one of the following cases:
        1. The position is not outside the board (eg. if pos.x is less than 0 or larger than the dimension of the board, then it's out of bounds)
        2. The position has not been previously visited.
        3. The position is not our current location
        :param pos:
        :return:
        """
        if pos.x < 0 or pos.y < 0:
            return True
        elif pos.x >= self.dimensions.x or pos.y >= self.dimensions.y:
            return True
        elif self.matrix[pos.y][pos.x] == self.position_mark or self.matrix[pos.y][pos.x] == self.visited:
            return True
        return False

    def warnsdorff(self):
        possible_moves = self.get_possible_moves()
        for move in possible_moves:
            pos = Point(*move)
            count = self.warnsdorff_count(pos)
            self.matrix[move.y][move.x] = ' ' * (self.cell_size - 1) + str(count)

    def warnsdorff_count(self, pos: Point):
        count = 0
        for move in MOVES:
            row = pos.y + move[0]
            col = pos.x + move[1]
            move_is_illegal = self.move_is_illegal(Point(col, row))
            if not move_is_illegal:
                count += 1
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
                print('Invalid move! ')
                continue

            self.make_a_move(pos)
            print(self)

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
            if self.matrix[new_pos.y][new_pos.x] == self.position_mark:
                continue
            if self.matrix[new_pos.y][new_pos.x] == self.visited:
                continue

            possible_moves.append(new_pos)

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
    board.warnsdorff()
    print(board)
    board.play()


if __name__ == '__main__':
    main()
