import Data.List.Split ( splitOn )
import Data.List ( elemIndex )
import Data.Maybe ( fromJust )

parseInput :: [Char] -> [Int]
parseInput rawInput = map read (splitOn "," rawInput) :: [Int]

-- from https://stackoverflow.com/questions/19554984/haskell-count-occurrences-function
count :: Eq a => a -> [a] -> Int
count x = length . filter (x==)

game :: Int -> [Int] -> Int
game max nums
    | length nums == max = head nums
    | otherwise = 
        if count (head nums) nums == 1 then
            game max (0:nums)
        else
            let lastIdx = fromJust (elemIndex  (head nums) (tail nums)) + 1 in
                game max (lastIdx:nums)

main :: IO()
main = do
    inputContents <- readFile "inputs/15.txt"
    let startNums = reverse . parseInput $ inputContents
    print . (++) "Part 1: " . show . game 2020 $ startNums
    print . (++) "Part 2: " . show . game 30000000 $ startNums
    