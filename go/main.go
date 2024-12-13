package main

import (
  "fmt"
  "os"
  "math/rand"
)

// Board functions
func createBoard() [4][4]rune {
  var board [4][4]rune
  var emptySymbol rune = '-'

  for row := 0; row < 4; row++ {
    for column := 0; column < 4; column++ {
      board[row][column] = emptySymbol
    }
  }

  return board
}

func printBoard(board [4][4]rune) {
  for _, row := range board {
    fmt.Printf("%c %c %c %c\n", row[0], row[1], row[2], row[3])
  }
}

func rotateBoard(board [4][4]rune) [4][4]rune {
  mapArray := [4][4][2]int{
      {{0,1}, {0,2}, {0,3}, {1,3}},
      {{0,0}, {1,2}, {2,2}, {2,3}},
      {{1,0}, {1,1}, {2,1}, {3,3}},
      {{2,0}, {3,0}, {3,1}, {3,2}},
  }

  var rotatedBoard [4][4]rune = createBoard()

  for row := 0; row < 4; row++ {
    for column := 0; column < 4; column++ {
      var newRow int = mapArray[row][column][0]
      var newColumn int = mapArray[row][column][1]
      rotatedBoard[newRow][newColumn] = board[row][column]
    }
  }

  return rotatedBoard
}

// Win checking
func checkWinSingleRow(row [4]rune, symbol rune) bool {
  for _, cell := range row {
    if cell != symbol {
      return false
    }
  }
  return true
}

func checkWinRows(board [4][4]rune, symbol rune) bool {
  for _, row := range board {
    if checkWinSingleRow(row, symbol) {
      return true
    }
  }
  return false
}

func checkWinColumns(board [4][4]rune, symbol rune) bool {
  // Loop over every column number
  for column := 0; column < 4; column++ {
    // Initially assume every check returns True
    var isValid bool = true
    for row := 0; row < 4; row++ {
      if board[row][column] != symbol {
        // If a value is found that isn't the symbol, the whole row is not a winner, so the rest can be skipped.
        isValid = false
        break
      }
    }
    // If a winner is found, then the function can return straight away without checking other columns.
    if isValid { return true }
  }
  return false
}

func checkWinDiagonals(board [4][4]rune, symbol rune) bool {
  if checkWinDiagonalTLBR(board, symbol) { return true }
  if checkWinDiagonalTRBL(board, symbol) { return true }
  return false
}

func checkWinDiagonalTLBR(board [4][4]rune, symbol rune) bool { // Top left to bottom right
  for i := 0; i < 4; i++ {
    if board[i][i] != symbol {
      return false
    }
  }
  return true
}

func checkWinDiagonalTRBL(board [4][4]rune, symbol rune) bool { // Top right to bottom left
  for i := 0; i < 4; i++ {
    if board[i][i] != symbol {
      return false
    }
  }
  return true
}

func checkIfPlayerWon(board [4][4]rune, symbol rune) bool {
  if checkWinRows(board, symbol) { return true }
  if checkWinColumns(board, symbol) { return true }
  if checkWinDiagonals(board, symbol) { return true }
  
  return false
}

func gameHasBeenWon(board [4][4]rune, player1 Player, player2 Player) bool {
  if checkIfPlayerWon(board, player1.Symbol) {
    printBoard(board)
    fmt.Printf("%s has won!\n", player1.Name)
    return true
  }

  if checkIfPlayerWon(board, player2.Symbol) {
    printBoard(board)
    fmt.Printf("%s has won!\n", player2.Name)
    return true
  }

  return false
} 

// Game functions
func userPlacePiece(board *[4][4]rune, symbol rune) {
  for { // Loop forever
    var row int
    var column int
    
    fmt.Println("Enter the row and the column, with a space between the numbers.")
    amount, err := fmt.Scan(&row, &column)

    // Try again if the values aren't numbers, or 
    if err != nil || amount != 2 {
      fmt.Println("Invalid input. Try again.")
      continue // Goes back to the start of the loop.
    }

    // If code reaches here, it is assumed that the row and column integers were set correctly.
    if !(1 <= row && 4 >= row && 1 <= column && 4 >= column) { 
      fmt.Println("One or more value is out of bounds. Try again.")
      continue
    }

    // Finally, check if there is already a symbol in the cell.
    if board[row-1][column-1] != '-' {
      fmt.Println("There is already a piece there. Try again.")
      continue
    }

    board[row-1][column-1] = symbol
    break
  }
}

func robotPlacePiece(board *[4][4]rune, symbol rune) {
  for {
    var row int = rand.Intn(4) // Random integer between 0 and 3
    var column int = rand.Intn(4)

    // If the cell is empty
    if board[row][column] == '-' {
      // Place the piece
      fmt.Printf("'%c' was placed in row %d, column %d.\n", symbol, row+1, column+1)
      board[row][column] = symbol
      // Stop the infinite loop
      break
    }
    // Otherwise, the loop continues until it finds an open space.
  }
}

// Misc
type Player struct {
  Name string
  Symbol rune
}

func winAndClose(board [4][4]rune, playerOne Player, playerTwo Player) {
  if gameHasBeenWon(board, playerOne, playerTwo) {
    // Exit program
    os.Exit(0)
  }
}

// Main game logic
func main() {
  rand.Seed(99693381)

  // Create board array
  var board[4][4]rune = createBoard()

  // Create player1 data structure
  var playerOne Player = Player{
    Name: "Player 1",
    Symbol: 'X',
  }
  // Create player2 data structure
  var playerTwo Player = Player{
    Name: "Player 2",
    Symbol: 'O',
  }

  // Loop 8 times:
  for i := 0; i < 8; i++ {
    //rotate board
    board = rotateBoard(board)
    winAndClose(board, playerOne, playerTwo)
    
    //player 1s turn
    fmt.Printf("%s's turn!\n", playerOne.Name)
    //print current board
    printBoard(board)
    //prompt user to place piece
    userPlacePiece(&board, playerOne.Symbol)
    winAndClose(board, playerOne, playerTwo)


    //player 2s turn
    fmt.Printf("%s's turn!\n", playerTwo.Name)
    //print current board
    printBoard(board)
    //prompt user to press enter to play player2s turn
    fmt.Printf("Press ENTER to play %s's turn.\n", playerTwo.Name)
    fmt.Scanln()
    //place piece in random location
    robotPlacePiece(&board, playerTwo.Symbol)
    winAndClose(board, playerOne, playerTwo)
  }

  //if code reaches here, it means that the board is full with no winner
  printBoard(board)
  fmt.Println("Board is full with no winner. Draw.")
}
