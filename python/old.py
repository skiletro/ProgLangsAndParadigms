class Player:
    def __init__(self, name: str, symbol: str):
        self.name: str = name
        self.symbol: str = symbol
        self.has_won: bool = False

class Board:
    def __init__(self):
        self.board_size: int = 3
        self.board: str = [['-']*self.board_size for _ in range(self.board_size)] #https://stackoverflow.com/a/21036188

    def print_horizontal_border(self):
        for cell in range(self.board_size):
            print('+---', end='') #The end='' stops the print function making a new line
        print('+')

    def print_board(self):
        for row in self.board:
            self.print_horizontal_border()
            for element in row:
                print('| {} '.format(element), end='')
            print('|')
        self.print_horizontal_border()

    def place_symbol(self, row: int, column: int, symbol: str):
        self.board[row-1][column-1] = symbol

    def check_horizontal_win(self, player: Player):
        for row in self.board:
            if all(element == player.symbol for element in row):
                return True
        return False

    def check_diagonal_win(self, player: Player):
        if all(self.board[element][element] == player.symbol for element in range(self.board_size)):
            return True
        else:
            return False

    def transpose_board(self):
        result: str = [['-']*self.board_size for _ in range(self.board_size)]
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                result[column][row] = self.board[row][column]
        self.board = result

    def shuffle_board(self): #TODO: Main gimmick of the game, have the outer ring rotate closewise, and the inner ring counterclosewise in a 4x4 grid
        # TODO: Rotate entire board clockwise, then rotate inner squares twice, counter-clockwise
        return 0

    def check_win(self, player: Player):
        has_won: bool = False
        if self.check_horizontal_win(player) == True: has_won = True
        if self.check_diagonal_win(player) == True: has_won = True
        self.transpose_board() #Transpose the board in order to check for vertical wins
        if self.check_horizontal_win(player) == True: has_won = True
        if self.check_diagonal_win(player) == True: has_won = True
        self.transpose_board() #Transpose it back
        return has_won

class Game:
    def __init__(self, player1: Player, player2: Player):
        self.board: Board = Board()
        self.player1: Player = player1
        self.player2: Player = player2

    def swap_players(self, player: Player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def play_turn(self, player: Player):
        entered_valid_input: bool = False
        bounds = range(1, self.board.board_size+1)
        print('It is {}\'s turn.'.format(player.name))
        while not entered_valid_input:
            row: int = int(input('Enter the row: '))
            column: int = int(input('Enter the column: '))

            if row in bounds and column in bounds:
                self.board.place_symbol(row, column, player.symbol)
                entered_valid_input = True
            else:
                print("Invalid input, try again")

    def start_game(self):
        current_player = self.player1
        while self.player1.has_won == False and self.player2.has_won == False:
            self.board.print_board()
            self.play_turn(current_player)
            self.player1.has_won = self.board.check_win(self.player1)
            self.player2.has_won = self.board.check_win(self.player2)
            current_player = self.swap_players(current_player)

            if self.player1.has_won:
                print('{} has won!'.format(self.playerswap_players1.name))

            if self.player2.has_won:
                print('{} has won!'.format(self.player2.name))

if __name__ == "__main__":
    game = Game(Player('Player 1', 'X'),
                Player('Player 2', 'O'))
    game.start_game()

