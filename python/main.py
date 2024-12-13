from typing import NamedTuple
import random

class Board:
    def __init__(self) -> None:
        self.board_size: int = 4
        self.blank_symbol: str = '-'
        self.board_array: list[list[str]] = [[self.blank_symbol] * self.board_size for _ in range(self.board_size)]
                              # If we let board_size = 3, the code above would evaluate to:
                              # [['-', '-', '-'],
                              #  ['-', '-', '-'],
                              #  ['-', '-', '-']]

    def print_horizontal_border(self) -> None:
        """
        Constructs the horizontal borders between board cells
        i.e., the "+---+---+" part
        """
        for _ in range(self.board_size):
            print('+---', end='') #The end='' stops the print function making a new line
        print('+')

    def print_board(self) -> None:
        """
        Uses the print_horizontal_border to construct and print the whole board
        """
        for row in self.board_array:
            self.print_horizontal_border()
            for element in row:
                print('| {} '.format(element), end='')
            print('|')
        self.print_horizontal_border()

    def place_symbol(self, row: int, column: int, symbol: str) -> bool:
        """
        Tries to place a symbol onto the board and returns True if it can,
        otherwise it returns False
        """
        if self.board_array[row][column] == self.blank_symbol:
            self.board_array[row][column] = symbol
            return True
        else:
            return False

    def check_horizontal_win(self, symbol: str) -> bool:
        """
        Checks for a horizontal win by looping over each row, which is
        represented as [s, s, s, s], then checks if all of the elements in that row
        match. If they do, then it's a win.
        """
        for row in self.board_array:
            if all(element == symbol for element in row):
                return True
        return False

    def check_vertical_win(self, symbol: str) -> bool:
        """
        Checks for a vertical win by checking the 1st to nth value in
        each row, and checking if they all match, if they do, then it's a win.
        """
        for column in range(0, self.board_size):
            if all(self.board_array[row][column] == symbol for row in range(0, self.board_size)):
                return True
        return False

    def check_diagonal_win(self, symbol: str) -> bool:
        # Checks top left to bottom right
        if all(self.board_array[value][value] == symbol for value in range(0, self.board_size)):
            return True

        # Checks top right to bottom left
        if all(self.board_array[self.board_size-1-value][value] == symbol for value in range(1, self.board_size)):
            return True

        # If neither are a match...
        return False

    def check_win(self, symbol: str) -> bool:
        """
        Checks for a win for all directions
        """
        if self.check_horizontal_win(symbol):
            return True
        elif self.check_vertical_win(symbol):
            return True
        elif self.check_diagonal_win(symbol):
            return True
        else:
            return False

    def rotate_board(self) -> None:
        """
        Function that rotates the outer and inner numbers in a matrix/2D array clockwise.
        Using the map_array array which contains where the numbers should be mapped to, the
        numbers are set to their new locations.

        i.e., the values in the array are used to tell the program where to put the new values
        """
        # Create our array of new locations
        map_array: list[list[list[int]]] = [[[0,1], [0,2], [0,3], [1,3]],
                                             [[0,0], [1,2], [2,2], [2,3]],
                                             [[1,0], [1,1], [2,1], [3,3]],
                                             [[2,0], [3,0], [3,1], [3,2]]]

        # Create empty board to put the symbols and their new locations in
        new_board: list[list[str]] = [[self.blank_symbol] * self.board_size for _ in range(self.board_size)]
        for x in range(0, 4):
            for y in range(0, 4):
                new_row: int
                new_column: int
                new_row, new_column = map_array[x][y]
                # Set the values at the new locations to the old values.
                new_board[new_row][new_column] = self.board_array[x][y]

        self.board_array = new_board

# Class with struct-like behaviour
class Player(NamedTuple):
    name: str
    symbol: str

class Game:
    def __init__(self) -> None:
        self.board: Board = Board()
        self.player1: Player = Player('Player 1', 'X') # This is the human player
        self.player2: Player = Player('Player 2', 'O') # This is the robot player

    def play(self, seed: int) -> None:
        random.seed(seed)

        loop_count: int = 0
        while True:
            # Player 1's Logic
            self.board.print_board()
            print("{}'s Turn".format(self.player1.name))
            self.place_piece_prompt(self.player1.symbol)
            # Check for a win after user has placed their symbol.
            if self.check_for_wins():
                # Exit the loop
                break

            # Player 2's Logic (the robot player)
            self.board.print_board()
            print("{}'s Turn".format(self.player2.name))
            input("Press enter to play {}'s turn.".format(self.player2.name))
            while True: # Keep looping until a valid piece is placed.
                # Generate random values for the row and column in the bounds of the board.
                row: int = random.randint(0, self.board.board_size)
                column: int = random.randint(0, self.board.board_size)
                # If the piece is placed in a valid location...
                if self.board.place_symbol(row-1, column-1, self.player2.symbol) == True:
                    # Let the player know what they placed.
                    print("{} placed a piece in row {}, column {}".format(self.player2.name, row, column))
                    # Exit the loop
                    break
            # Checking for a win if after the robot player has placed their symbol.
            if self.check_for_wins():
                break

            # Incrementing the loop counter to check if there is a draw yet.
            loop_count += 1
            if loop_count >= 8: # 16 possible slots on the board to place symbols: 2 placed symbols per loop => 8 loops
                self.board.print_board()
                print("The game has ended in a draw.")
                break

            # If the code gets this far, the game is still in play and it's time for another loop.
            print("Rotating the board...")
            self.board.rotate_board()
            # Check for a win one last time.
            if self.check_for_wins():
                break

    def check_for_wins(self) -> bool:
        """
        This function checks if either player won, and outputs text accordingly.
        """
        player1_won: bool = self.board.check_win(self.player1.symbol)
        player2_won: bool = self.board.check_win(self.player2.symbol)

        if player1_won:
            self.board.print_board()
            print("{} wins!".format(self.player1.name))
            return True
        elif player2_won:
            self.board.print_board()
            print("{} wins!".format(self.player2.name))
            return True
        else:
            return False

    def place_piece_prompt(self, symbol: str) -> None:
        while True: # Keep looping until a valid piece has been placed.
            # The idea is that if at any point the piece is invalid, then an error is thrown and caught to be dealt with.
            try:
                row: int = int(input("Enter the row: ")) # If anything is entered here that isn't an integer, then ValueError is thrown.
                column: int = int(input("Enter the column: ")) # Same for this variable

                # Checks if the number is 0. Causes some weird issues with settng the piece if it is.
                if (row or column) <= 0:
                    raise IndexError

                # Try to place the piece and store whether it placed successfully or not
                placed_valid_piece: bool = self.board.place_symbol(row-1, column-1, symbol) # Row and column offset as arrays start at 0.
                # If the piece was unable to be placed because a piece is already there...
                if placed_valid_piece:
                    break # Exit the loop
                else:
                    raise Exception("Piece already exists there.")

            # If for whatever reason the piece can't be placed and an error is thrown, it gets dealt with here with a simple message.
            except (ValueError, IndexError, Exception):
                print("Invalid location. Try again.")

if __name__ == '__main__':
    try:
        game: Game = Game()
        game.play(99693381) # This will result in the same game every time because it's the same seed
    except KeyboardInterrupt: # Handles CTRl+C'ing to exit the game (gets rid of the ugly error)
        print("\n\nEnded game through keyboard.")
    finally:
        print("Thank you for playing!")
