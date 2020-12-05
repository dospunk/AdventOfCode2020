import Data.List ( sort )

--Math in Haskell is a PAIN

mid :: Fractional a => a -> a -> a
mid lo hi = lo+((hi-lo)/2)

search :: (RealFrac a) => [Char] -> a -> a -> a
search ('B':"") _ hi = hi
search ('F':"") lo _ = lo
search ('R':"") _ hi = hi
search ('L':"") lo _ = lo
search ('B':rest) lo hi = search rest (fromIntegral . ceiling $ mid lo hi) hi
search ('F':rest) lo hi = search rest lo (fromIntegral . floor $ mid lo hi)
search ('R':rest) lo hi = search rest (fromIntegral . ceiling $ mid lo hi) hi
search ('L':rest) lo hi = search rest lo (fromIntegral . floor $ mid lo hi)

findRow :: (RealFrac a) => String -> a
findRow s = search (take 7 s) 0 127

findColumn :: (RealFrac a) => String -> a
findColumn s = search (drop 7 s) 0 7


findSeatId :: (RealFrac a) => String -> a
findSeatId s = (findRow s * 8) + findColumn s

findHighestSeatId :: (RealFrac p) => [String] -> p
findHighestSeatId [a,b] = max (findSeatId a) (findSeatId b)
findHighestSeatId (x:xs) = max (findSeatId x) (findHighestSeatId xs)

findMissing :: (Eq a, Enum a) => [a] -> a
findMissing (x:y:rest) = if y == succ x
    then findMissing (y:rest) 
    else succ x

main :: IO()
main = do
    inputContents <- readFile "inputs/5.txt"
    let inputLines = lines inputContents
    putStr "Highest Seat ID: "
    print . toInteger . round . findHighestSeatId $ inputLines
    putStr "My Seat: "
    print . findMissing . sort $ map findSeatId inputLines