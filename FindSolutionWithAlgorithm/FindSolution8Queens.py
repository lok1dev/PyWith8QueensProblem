import os

# Check if placing a queen in the given position is safe
def is_safe(board, row, col):
    for i in range(col):
        if board[row][i] == 'wN':
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 'wN':
            return False

    for i, j in zip(range(row, 8, 1), range(col, -1, -1)):
        if board[i][j] == 'wN':
            return False

    return True

# Save the solution to a file
def save_solution(solution, filename):
    with open(filename, 'w') as f:
        for row in solution:
            f.write(' '.join(row) + '\n')

# Solve the N-Queens problem recursively
def solve_queens(board, col, solutions):
    if col >= 8:
        solutions.append([row[:] for row in board])
        return

    for i in range(8):
        if is_safe(board, i, col):
            board[i][col] = 'wN'
            solve_queens(board, col + 1, solutions)
            board[i][col] = '--'

# Find all solutions to the N-Queens problem
def find_queens_solutions():
    if not os.path.exists("results"):
        os.makedirs("results")

    solutions = []
    board = [['--' for _ in range(8)] for _ in range(8)]
    solve_queens(board, 0, solutions)

    for idx, solution in enumerate(solutions, 1):
        filename = f"results/solution_{idx}.txt"
        save_solution(solution, filename)

    return solutions

# Find and save all solutions
solutions = find_queens_solutions()
print(f"Found {len(solutions)} solutions.")
