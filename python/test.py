import index as program
import unittest

class TestStringMethods(unittest.TestCase):
    def test_vertical_win(self):
        board = program.Board()
        symbol = 'X'
        for column in range(0, board.board_size):
            board.place_symbol(column, 0, symbol)
        self.assertTrue(board.check_vertical_win(symbol), 'Should be a vertical win')

    def test_horizontal_win(self):
        board = program.Board()
        symbol = 'X'
        for row in range(0, board.board_size):
            board.place_symbol(0, row, symbol)
        self.assertTrue(board.check_horizontal_win(symbol), 'Should be a horizontal win')

    def test_diagonal_win(self):
        board = program.Board()
        symbol = 'O' # Testing a different symbol this time
        for x in range(0, board.board_size):
            board.place_symbol(x, x, symbol)
        self.assertTrue(board.check_diagonal_win(symbol), 'Should be a diagonal win')

if __name__ == '__main__':
    unittest.main()
