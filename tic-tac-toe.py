import random

board = [[' ' for _ in range(9)] for _ in range(9)]
player = 'X'

def print_board():
    print('-------------')
    for i in range(9):
        print('|', end='')
        for j in range(9):
            print(board[i][j], '|', end='')
        print()
        print('-------------')

def check_win():
    # check rows
    for i in range(9):
        for j in range(5):
            if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] != ' ':
                return True
    # check columns
    for i in range(5):
        for j in range(9):
            if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] != ' ':
                return True
    # check diagonal
    for i in range(5):
        for j in range(5):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] != ' ':
                return True
            if board[i][j+3] == board[i+1][j+2] == board[i+2][j+1] == board[i+3][j] != ' ':
                return True
    return False

# def make_move(row, col, player):
#     if board[row][col] == ' ':
#         board[row][col] = player
#     else:
#         valid_moves = []
#         for i in range(row-1, row+2):
#             for j in range(col-1, col+2):
#                 if i < 0 or i >= 9 or j < 0 or j >= 9 or (i == row and j == col) or board[i][j] != ' ':
#                     continue
#                 valid_moves.append((i, j))
#         if len(valid_moves) > 0:
#             new_row, new_col = random.choice(valid_moves)
#             board[new_row][new_col] = player

while True:
    print_board()
    row = int(input(f'Player {player}, choose row (1-9): ')) - 1
    col = int(input(f'Player {player}, choose column (1-9): ')) - 1
    make_move(row, col, player)
    if check_win():
        print_board()
        print(f'Player {player} wins!')
        break
    player = 'O' if player == 'X' else 'X'