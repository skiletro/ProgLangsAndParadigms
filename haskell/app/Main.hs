import System.Random

type Board = [Player]
type Turns = [Player]

data Player = X | O | E -- E stands for empty
  deriving (Eq) -- Allows for comparisons

-- Changes how the pieces are displayed when printed
instance Show Player where
  show X = "X"
  show O = "O"
  show E = "-"

outputBoard :: Board -> String
outputBoard [] = [] -- Don't do anything if empty
outputBoard (first:second:third:fourth:rest) = 
  show first ++ " " ++ show second ++ " " ++ show third ++ " " ++ show fourth ++ "\n" ++ outputBoard rest
-- Equivalent code in an imperative style would go row by row and prints out each row

updateBoard :: Int -> Player -> Board -> Board
updateBoard index player board =
  let
    (before, _: after) = splitAt index board
  in
    before ++ [player] ++ after

transposeBoard :: Board -> Board
transposeBoard [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16] =
               [p1, p5, p9, p13, p2, p6, p10, p14, p3, p7, p11, p15, p4, p8, p12, p16]

rotateBoard :: Board -> Board -- Main gimmick of the proposed task.
rotateBoard [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16] =
            [p5, p1, p2, p3, p9, p10, p6, p4, p13, p11, p7, p8, p14, p15, p16, p12]


isRowWinner :: Player -> Board -> Bool
isRowWinner _ [] = False
isRowWinner player (first:second:third:fourth:otherRows)
  | all (== player) [first, second, third, fourth] = True
  | otherwise = isRowWinner player otherRows

isDiagonalWinner :: Player -> Board -> Bool
isDiagonalWinner player [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16]
  | all (== player) [p1, p6, p11, p16] = True
  | all (== player) [p4, p7, p10, p13] = True
  | otherwise = False

isWinner :: Player -> Board -> Bool
isWinner player board
  | isRowWinner player board = True
  | isRowWinner player (transposeBoard board) = True -- checks column winners by transposing board first
  | isDiagonalWinner player board = True
  | otherwise = False

gameLoop :: StdGen -> Turns -> Board -> IO ()
gameLoop _ [] _ = putStrLn "Draw!"
gameLoop rng (player:otherTurns) board = do
  putStrLn(outputBoard board)
  putStrLn("It is " ++ show player ++ "'s turn!")

  let (randomNumber, newRng) = randomR (0, 15) rng
  index <- if player == X then do
              putStrLn "Enter the index of the slot (1-16)"
              input <- getLine
              let number = read input
              return (number - 1)
           else do
              putStrLn "Press ENTER to play the turn."
              _ <- getLine -- What the user actually enters here doesn't matter
              return randomNumber

  -- Add piece onto board
  let newBoard = updateBoard index player board

  -- Check for a win
  if isWinner player newBoard then do
    putStrLn (outputBoard newBoard)
    putStrLn (show player ++ " wins!")
  else
    -- Loop
    if player == O then do
      gameLoop newRng otherTurns (rotateBoard newBoard)
    else
      gameLoop newRng otherTurns newBoard


-- Main function, this is a monad and is what the program launches when you start it
main :: IO ()
main = do
  -- Rng variable for random numbers; turns 
  let rng :: StdGen
      rng = mkStdGen 99693381
      turns :: Turns
      turns = take 16 (cycle [X, O]) -- equivalent to [X, O, ..., X, O] with 16 elements. cycle generates an inf. list
      board :: Board
      board = replicate 16 E -- equivalent to [E, E, ..., E] with 16 elements
  gameLoop rng turns board
  putStrLn "Thank you for playing."
