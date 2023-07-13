import copy


def valid(configuration):
    """
    Checks whether the configuration of the board is a valid solution.
    
    It must hold that:
    1.) No row contains the same number
    2.) No column contains the same number
    3.) No square contains the same number
    """
    rows = [set() for _ in range(9)]
    columns = [set() for _ in range(9)]
    squares = [[set() for r in range(3)] for c in range(3)]

    for r in range(9):
        for c in range(9):
            digit = configuration[r][c]
            if digit in rows[r] or digit in columns[c] or digit in squares[r//3][c//3]:
                return False 
            rows[r].add(digit)
            columns[c].add(digit)
            squares[r//3][c//3].add(digit)
    return True


def solve(configuration):
    board = copy.deepcopy(configuration)

    def solve_h():
        def possible_placement(r, c, n):
            if (any(board[r][i]==n for i in range(9))
                or any(board[i][c]==n for i in range(9))
                or any(board[i][j]==n for i in range(3*(r//3), 3*(r//3)+3) 
                                        for j in range(3*(c//3), 3*(c//3)+3))):
                return False
            return True
        
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    continue
                for n in (1,2,3,4,5,6,7,8,9):
                    if possible_placement(r, c, n):
                        board[r][c] = n
                        if solve_h():
                            return True
                        board[r][c] = 0
                return False
        return True
    solve_h()
    
    return board

        
