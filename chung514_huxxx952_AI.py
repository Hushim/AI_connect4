class chung514_huxxx952_AI:

    def __init__(self, player):
        self.player = player
        self.rival = 1
        if self.player == self.rival:
            self.rival = 2

    def name(self):
        return "lalala"



    def decide(self, board):
        maxScore = -99999999999
        maxCol = 0
        for i in range(len(board[0])):
            if board[0][i] != 0: # column already full
                continue
            droppedRow = self.dropDisc(board, i, self.player)
            score = self.minimax_rec(board, 3, -99999999999, 99999999999, self.rival)
            if score > maxScore:
                maxScore = score
                maxCol = i
            board[droppedRow][i] = 0
        return maxCol

    def dropDisc(self, board, drop_col, player):
        row = len(board)
        for i in range(0, row):
            if board[i][drop_col] != 0:
                board[i-1][drop_col] = player
                return i-1
        board[row-1][drop_col] = player
        return row-1


    def minimax_rec(self, board, depth, alpha, beta, player):
        wins = self.checkWin(board)
        if wins == self.player:
            return 99999999999 # We win, return max score
        if wins == self.rival:
            return -99999999999 # Rival wins, return min score

        if depth == 0:
            return self.heuristic(board)

        if player == self.rival: # Rival playing
            minScore = 9999999999
            for i in range(len(board[0])): # each column
                if board[0][i] != 0: # column already full
                    continue
                droppedRow = self.dropDisc(board, i, self.rival)
                score = self.minimax_rec(board, depth-1, alpha, beta, self.player)
                if score < minScore:
                    minScore = score
                if minScore < beta:
                    beta = minScore
                if beta <= alpha:
                    board[droppedRow][i] = 0
                    break
                board[droppedRow][i] = 0
            return minScore
        else: # We playing
            maxScore = -9999999999
            for i in range(len(board[0])): # each column
                if board[0][i] != 0: # column already full
                    continue
                droppedRow = self.dropDisc(board, i, self.player)
                score = self.minimax_rec(board, depth-1, alpha, beta, self.rival)
                if score > maxScore:
                    maxScore = score
                if maxScore > alpha:
                    alpha = maxScore
                if beta <= alpha:
                    board[droppedRow][i] = 0
                    break
                board[droppedRow][i] = 0
            return maxScore


    def heuristic(self, board):
        score = 0
        row = len(board)
        col = len(board[0])
        delta = [[0, 1], [1, 1], [-1, 1]]
        singleDelta = [[-1,-1], [0, -1], [1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1]]


        """MODIFY HERE"""
        scores = [[[1, 3, 6, 10, 15, 21, 28], [20, 60], [200, 9999999]],
                  [[-1, -3, -6, -10, -15, -21, -28], [-20, -5000], [-10000, -99999999]]]


        players = [self.player, self.rival]
        for z in range(2): # player and rival
            player = players[z]
            for i in range(row):
                for j in range(col):
                    for length in [3, 2]: # search for conneciton length: 3 and 2 (will deal with 1 later)
                        for k in delta: # horizontal and diagonal
                            for l in range(length):
                                if 0 > i+l*k[0] or i+l*k[0] >= row or 0 > j+l*k[1] or j+l*k[1] >= col or board[i+l*k[0]][j+l*k[1]] != player:
                                    break
                                if l == length - 1: # long enough, check open ends
                                    ends = 0
                                    if (0 <= i-k[0] < row and 0 <= j-k[1] < col and board[i-k[0]][j-k[1]] == player) or \
                                            (0 <= i+length*k[0] < row and 0 <= j+length*k[1] < col and board[i+length*k[0]][j+length*k[1]] == player):
                                        # too long
                                        break
                                    if 0 <= i-k[0] < row and 0 <= j-k[1] < col and board[i-k[0]][j-k[1]] == 0:
                                        ends += 1
                                    if 0 <= i+length*k[0] < row and 0 <= j+length*k[1] < col and board[i+length*k[0]][j+length*k[1]] == 0:
                                        ends += 1
                                    if ends > 0:
                                        score += scores[z][length-1][ends-1]
                    #veritcal
                    if i > 0 and board[i-1][j] == 0 and board[i][j] == player:
                        count = 1
                        while i+count < row and board[i+count][j] == player:
                            count += 1
                        if count > 1:
                            score += scores[z][count-1][0]
                    #single
                    if board[i][j] == player:
                        single = True
                        opens = 0
                        for d in singleDelta:
                            if 0 <= i+d[0] < row and 0 <= j+d[1] < col:
                                if board[i+d[0]][j+d[1]] == 0:
                                    opens += 1
                        if single and opens > 0:
                            score += scores[z][0][opens-1]

        return score

    def checkWin(self, board):
        row = len(board)
        col = len(board[0])
        tops = []
        for i in range(col):
            for j in range(row):
                if board[j][i] != 0:
                    tops.append(j)
                    break
                if j == row-1 and board[j][i] == 0:
                    tops.append(-1)
        for k in range(len(tops)):
            if tops[k] == -1:
                continue
            new_row = tops[k]
            new_col = k
            count = 1
            player = board[new_row][new_col]
            for i in range(new_row+1, row):
                if board[i][new_col] == player:
                    count += 1
                    if count == 4:
                        return player
                else:
                    break

            #Test for column to see whether there's a 4 consecutive one
            count = 1
            for i in reversed(range(0, new_col)):
                if board[new_row][i] == player:
                    count += 1
                else:
                    break
            for i in range(new_col+1, col):
                if board[new_row][i] == player:
                    count += 1
                else:
                    break
            if count >= 4:
                return player
            #Test for diagonals to see whether there's a 4 consecutive one
            count = 1
            for i in range(1, row):
                if new_row + i >= row or new_col + i >= col:
                    break
                elif board[new_row+i][new_col+i] == player:
                    count += 1
                else:
                    break
            for i in range(1, row):
                if new_row - i < 0 or new_col - i < 0:
                    break
                elif board[new_row-i][new_col-i] == player:
                    count += 1
                else:
                    break
            if count >= 4:
                return player
            count = 1
            for i in range(1, row):
                if new_row + i >= row or new_col - i < 0:
                    break
                elif board[new_row+i][new_col-i] == player:
                    count += 1
                else:
                    break
            for i in range(1, row):
                if new_row - i < 0 or new_col + i >= col:
                    break
                elif board[new_row-i][new_col+i] == player:
                    count += 1
                else:
                    break
            if count >= 4:
                return player
        # If no consecutive 4 discs are found, return -1
        return -1


