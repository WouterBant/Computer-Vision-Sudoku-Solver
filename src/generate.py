import random
import copy
from test import valid, solve
import time


def generate_configuration():
    configuration = [[0]*9 for _ in range(9)]
    rows = [set(range(1,10)) for _ in range(9)]
    columns = [set(range(1,10)) for _ in range(9)]
    squares = [[set(range(1,10)) for r in range(3)] for c in range(3)]

    for r in range(9):
        for c in range(9):
            possibilities = rows[r].intersection(columns[c]).intersection(squares[r//3][c//3])

            if not possibilities:
                return None
            
            number = random.choice(list(possibilities))

            rows[r].remove(number)
            columns[c].remove(number)
            squares[r//3][c//3].remove(number)

            configuration[r][c] = number

    return configuration


def generate_solution_puzzle():
    while True:
        configuration = generate_configuration()
        if configuration:
            assert valid(configuration) == True
            return configuration
        

def omit_numbers(solution, attempted_numbers_to_omit=70):
    """
    Omit numbers while ensuring the resulting puzzle has a unique solution.
    """
    cells_left = set((r, c) for r in range(9) for c in range(9))
    number_cells_omitted = 0
    configuration = copy.deepcopy(solution)

    def able_to_omit(row, col):
        number = configuration[row][col]
        configuration[row][col] = -1

        def number_possible(r, c):
            for j in range(9):
                if (configuration[r][j] == number or 
                    configuration[j][c] == number or 
                    configuration[(r//3)*3 + j//3][(c//3)*3 + j%3] == number):
                    return False
            configuration[row][col] = number
            return True

        # Check whether an empty cell could contain number
        for i in range(9):
            if configuration[row][i] == 0:
                if number_possible(row, i):
                    return False
            if configuration[i][col] == 0:
                if number_possible(i, col):
                    return False
            if configuration[(row//3)*3 + i//3][(col//3)*3 + i%3] == 0:
                if number_possible((row//3)*3 + i//3, (col//3)*3 + i%3):
                    return False

        return True

    for _ in range(attempted_numbers_to_omit):
        row, column = random.choice(list(cells_left))
        cells_left.remove((row, column))
        
        if able_to_omit(row, column):
            configuration[row][column] = 0
            number_cells_omitted += 1

    return configuration

def generate_puzzle():
    """
    Generates a Sudoku puzzle and its unique solution
    """
    solution = generate_solution_puzzle()
    puzzle = omit_numbers(solution)
    assert solve(puzzle) == solution  # Uniqueness requirement
    return (solution, puzzle)


if __name__ == "__main__":
    start_time = time.time()
    for _ in range(10):
        generate_puzzle()
    print(f"Time elapsed: {time.time() - start_time}")
