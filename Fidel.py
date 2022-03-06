from random import randrange, choice, choices

accessible_tiles = ["B", "R", "M", "H", "E", "D", " "]
dir_coord_map = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
dir_arrow_map = {"N": "↑", "E": "→", "S": "↓", "W": "←"}  # "Leash" https://www.i2symbol.com/symbols/arrows


# create board with given params
def create_board(r=5, c=5, baby_freq=0.2, reg_freq=0.2, mama_freq=0.05, health_freq=0.1, wall_freq=0.05,
                 start_loc=None, end_loc=None):
    # error checking
    if r <= 1 or c <= 1:
        print(f"Error, size {r}x{c} is too small")
        return
    freqs = [baby_freq, reg_freq, mama_freq, health_freq, wall_freq]
    if sum(freqs) > 1:
        print(f"Error, frequencies add up to {sum(freqs)}, must be at most 0")
        return
    if any(f < 0 for f in freqs):
        print(f"Error, a frequency is negative")
        return
    freqs = [baby_freq, reg_freq, mama_freq, health_freq, wall_freq, 1 - sum(freqs)]
    if start_loc is None:
        start_loc = (0, randrange(c))
    if end_loc is None:
        end_loc = (r - 1, randrange(c))
    if start_loc[0] < 0 or end_loc[0] < 0 or start_loc[0] > r - 1 or end_loc[0] > r - 1 or \
       start_loc[1] < 0 or end_loc[1] < 0 or start_loc[1] > c - 1 or end_loc[1] > c - 1:
        print(f"Error, start_loc {start_loc} or end_loc {end_loc} is out of bounds")
        return

    tiles = ["B", "R", "M", "H", "W", " "]
    random_tiles = choices(tiles, freqs, k=(r*c - 2))
    i = 0

    board = [[0 for y in range(c)] for x in range(r)]
    for row in range(r):
        for col in range(c):
            if (row, col) == start_loc:
                board[row][col] = "S"
            elif (row, col) == end_loc:
                board[row][col] = "D"
            else:
                board[row][col] = random_tiles[i]
                i += 1

    return board


# display board in human readable way
def display_board(board):
    l = len(board[0])
    cols = [str(c) for c in range(len(board[0]))]
    print((l * 2 + 1) * "_")
    print(" ", " ".join(cols))
    r = 0
    for row in board:
        row = (str(c) for c in row)
        print(f"{r}", " ".join(row))
        r += 1


# give current pos of Fidel based on start and place Fidel
def start_game(board):
    curr_pos = (0, 0)
    for row in range(len(board)):
        if "S" in board[row]:
            curr_pos = (row, board[row].index("S"))

    board[curr_pos[0]][curr_pos[1]] = "F"
    return curr_pos, board


# returns array of possible directions you can go to
# only returns if possible to move, even if you die moving here
def possible_moves(curr_pos, board):
    rows = len(board)
    cols = len(board[0])
    curr_r, curr_c = curr_pos
    possible_moves = []

    # North
    if curr_r > 0 and board[curr_r - 1][curr_c] in accessible_tiles:
        possible_moves.append("N")
    # East
    if curr_c < cols - 1 and board[curr_r][curr_c + 1] in accessible_tiles:
        possible_moves.append("E")
    # South
    if curr_r < rows - 1 and board[curr_r + 1][curr_c] in accessible_tiles:
        possible_moves.append("S")
    # West
    if curr_c > 0 and board[curr_r][curr_c - 1] in accessible_tiles:
        possible_moves.append("W")

    return possible_moves


# adds coords of current pos and next move
def next_loc(curr_pos, next_move):
    if next_move[0] is str:
        next_move = dir_coord_map[next_move]
    return (curr_pos[0] + next_move[0], curr_pos[1] + next_move[1])


def next_step_tile(curr_pos, step):
    next_pos = next_loc(curr_pos, step)
    return board[next_pos[0]][next_pos[1]]


def take_step(curr_pos, board, next_move):
    char = dir_arrow_map[next_move]
    board[curr_pos[0]][curr_pos[1]] = char

    step = dir_coord_map[next_move]
    next_pos = next_loc(curr_pos, step)
    board[next_pos[0]][next_pos[1]] = "F"
    return next_pos, board


board = create_board(r=6, c=5)
curr_pos, board = start_game(board)
print(f"START: {curr_pos}")

# BELOW IS JUST TO PLAY AROUND

pos_moves = possible_moves(curr_pos, board)
while (len(pos_moves) > 0):
    next_step = choice(pos_moves)
    curr_pos, board = take_step(curr_pos, board, next_step)
    pos_moves = possible_moves(curr_pos, board)

display_board(board)

