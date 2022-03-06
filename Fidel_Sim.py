from random import seed, randrange, choice, choices

accessible_tiles = ["B", "R", "M", "H", "E", "D", " "]
dir_coord_map = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
dir_arrow_map = {"N": "↑", "E": "→", "S": "↓", "W": "←"}  # "Leash" https://www.i2symbol.com/symbols/arrows

seed(202)  # comment out if needed, here for reproducibility


class FidelBoard:

    # create board with given params
    def __init__(self, r=5, c=5, baby_freq=0.2, reg_freq=0.2, mama_freq=0.05, health_freq=0.1, wall_freq=0.05,
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

        self.board = board
        self.curr_pos = start_loc
        self.curr_experience = 0
        self.max_health = 2
        self.curr_health = self.max_health
        self.kill_streak = 0
        self.curr_leash = []

    # display board in human readable way
    def display_board(self):
        l = len(self.board[0])
        cols = [str(c) for c in range(len(self.board[0]))]
        print((l * 2 + 1) * "_")
        print(" ", " ".join(cols))
        r = 0
        for row in self.board:
            row = (str(c) for c in row)
            print(f"{r}", " ".join(row))
            r += 1

    # give current pos of Fidel based on start and place Fidel
    def start_game(self):
        curr_pos = (0, 0)
        for row in range(len(self.board)):
            if "S" in self.board[row]:
                curr_pos = (row, self.board[row].index("S"))

        #self.board[curr_pos[0]][curr_pos[1]] = "F"

    # returns array of possible directions you can go to
    # only returns if possible to move, even if you die moving here
    def possible_moves(self):
        rows = len(self.board)
        cols = len(self.board[0])
        curr_r, curr_c = self.curr_pos
        possible_moves = []

        # North
        if curr_r > 0 and self.board[curr_r - 1][curr_c] in accessible_tiles:
            possible_moves.append("N")
        # East
        if curr_c < cols - 1 and self.board[curr_r][curr_c + 1] in accessible_tiles:
            possible_moves.append("E")
        # South
        if curr_r < rows - 1 and self.board[curr_r + 1][curr_c] in accessible_tiles:
            possible_moves.append("S")
        # West
        if curr_c > 0 and self.board[curr_r][curr_c - 1] in accessible_tiles:
            possible_moves.append("W")

        return possible_moves

    # adds coords of current pos and next move
    def next_loc(self, next_move):
        if next_move[0] is str:
            next_move = dir_coord_map[next_move]
        return (self.curr_pos[0] + next_move[0], self.curr_pos[1] + next_move[1])

    # returns tile of next step
    def next_step_tile(self, step):
        next_pos = self.next_loc(self.curr_pos, step)
        return self.board[next_pos[0]][next_pos[1]]

    # moves Fidel to that board place
    def take_step(self, next_move):
        char = dir_arrow_map[next_move]
        self.board[self.curr_pos[0]][self.curr_pos[1]] = char

        step = dir_coord_map[next_move]
        next_pos = self.next_loc(step)

        self.board[next_pos[0]][next_pos[1]] = "F"
        self.curr_pos = next_pos
        self.curr_leash.append(next_move)


# for playing around, ignore/ delete below

board = FidelBoard(r=5, c=6)
board.start_game()

pos_moves = board.possible_moves()
while (len(pos_moves) > 0):
    next_step = choice(pos_moves)
    board.take_step(next_step)
    pos_moves = board.possible_moves()

board.display_board()

