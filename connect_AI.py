import copy
class SimonaAI:
    def __init__(self, player):
        self.player = player
        
    def name(self):
        return "Simona_ver2"               


    def drop_test(self, board, row, col):
        for i in range(0, row):
            if board[i][col] != 0 and i == 0:
                return -1
            elif board[i][col] != 0:
                return i-1
            if i == row-1:
                return row-1

    def decide(self, board):
        row = len(board)
        col = len(board[0])
        #test if the middle of the board's bottom row is empty
        if board[row-1][int(col/2)] == 0:
            return int(col/2)
        #test if the board is almost full
        count = 0
        for i in range(0, row):
            if count > 1:
                break
            for j in range(0, col):
                if board[i][j] == 0:
                    count = count + 1
                if count > 1:
                    break
        if count == 1:
            for i in range(0, col):
                if board[0][i] == 0:
                    return i
                
        #simulate the move of me and the opponent
        turn = 2
        ans = self.future(board, row, col, turn)

        max = -10000000
        select = -1
        for i in range(0, col):
            if ans[i] > max:
                max = ans[i]
                select = i
        return select

    #will return the rate of 7 selection
    def future(self, board, row, col, turn):
        if turn == 0:
            return [0 for i in range(0, col)]
        turn = turn -1
        
        rate = [100000 for i in range(0, col)]
        for i in range(0, col):
            #drop the first disc
            my_row = self.drop_test(board, row, i)
            my_col = i
            if my_row == -1:
                continue
            board[my_row][my_col] = self.player
            for j in range(0, col):
                #drop the second disc
                enemy_row = self.drop_test(board, row, j)
                enemy_col = j
                if enemy_row == -1:
                    continue
                board[enemy_row][enemy_col] = 3 - self.player
                #count the rate
                tmp = self.rating(board, row, col, my_row, my_col, enemy_row, enemy_col)

                if tmp < -500:
                    tmp_list = [0 for k in range(0, col)]
                else:
                    tmp_list = self.future(board, row, col, turn)
                #find the biggest from future
                tmp_max = -20000
                for k in range(0, col):
                    if tmp_list[k] > tmp_max:
                        tmp_max = tmp_list[k]
                tmp = tmp + tmp_max

                if tmp < rate[i] and tmp != 100000:
                    rate[i] = tmp
                board[enemy_row][enemy_col] = 0
            board[my_row][my_col] = 0

        for i in range(0, col):
            if rate[i] == 100000:
                rate[i] = -100000
        return copy.deepcopy(rate)

    def rating(self, board, row, col, my_row, my_col, enemy_row, enemy_col):
        rate = 0
        #check if I made a four, if yes +2000
        if self.checkforfours(board, row, col, my_row, my_col, self.player):
            rate = rate + 2000
        #check if the enemy made a four -999
        if self.checkforfours(board, row, col, enemy_row, enemy_col, 3-self.player):
            rate = rate - 999
            #print(3-self.player,'is s gonna win!!',my_row, my_col, enemy_row, enemy_col)
            #print(board)
        #one point which is going to make me win next time +100
        rate = rate + 50*self.checkfornextwin(board, row, col, self.player)
        #one point which is going to make the opponent win next time -20
        rate = rate + (-10)*self.checkfornextwin(board, row, col, 3-self.player)
        #Check for threes even if they cannot make me win next time
        rate = rate + 50*self.checkforthrees(board, row, col, my_row, my_col, self.player)
        #Check for threes even if they cannot make the opponent win next time
        rate = rate + (-10)*self.checkforthrees(board, row, col, enemy_row, enemy_col, 3-self.player)
        #check for my two consecutive ones, each one worth 2
        rate = rate + 2*self.checkfortwos(board, row, col, my_row, my_col, self.player)
        #check for the opponent's two consecutive ones, each one worth -1
        rate = rate + (-1)*self.checkfortwos(board, row, col, enemy_row, enemy_col, 3-self.player)
        return rate

    def checkforfours(self, board, row, col, new_row, new_col, player):
        # Test for row to see whether there's a 4 consecutive one
        count = 1
        for i in range(new_row+1, row):
            if board[i][new_col] == player:
                count = count + 1
                if count == 4:
                    return True
            else:
                break

        #Test for column to see whether there's a 4 consecutive one
        count = 1
        for i in reversed(range(0, new_col)):
            if board[new_row][i] == player:
                #print('LEFTTTTTTTT',new_col)
                count = count + 1
            else:
                break
        for i in range(new_col+1, col):
            if board[new_row][i] == player:
                #print('RIGHTTTTTT',new_col)
                count = count + 1
            else:
                break
        if count >= 4:
            return True
        #Test for diagonals to see whether there's a 4 consecutive one
        count = 1
        for i in range(1,row):
            if new_row + i >= row or new_col + i >= col:
                break
            elif board[new_row+i][new_col+i] == player:
                count = count + 1
            else:
                break
        for i in range(1, row):
            if new_row - i < 0 or new_col - i < 0:
                break
            elif board[new_row-i][new_col-i] == player:
                count = count + 1
            else:
                break
        if count >= 4:
            return True
        count = 1
        for i in range(1, row):
            if new_row + i >= row or new_col - i < 0:
                break
            elif board[new_row+i][new_col-i] == player:
                count = count + 1
            else:
                break
        for i in range(1, row):
            if new_row - i < 0 or new_col + i >= col:
                break
            elif board[new_row-i][new_col+i] == player:
                count = count + 1
            else:
                break
        if count >= 4:
            return True
        # If no consecutive 4 discs are found, return False
        return False
    
    def checkfornextwin(self, board, row, col, player):
        count = 0
        for i in range(0, col):
            next_row = self.drop_test(board, row, i)
            next_col = i
            if next_row == -1:
                #print('next row test=', next_row)
                #print(board)
                #print("WAT?")
                continue
            if self.checkforfours(board, row, col, next_row, next_col, player):
                count = count + 1
        return count

    def checkforthrees(self, board, row, col, new_row, new_col, player):
        # Test for row to see whether there's a 3 consecutive one
        threes = 0
        count = 1
        for i in range(new_row+1, row):
            if board[i][new_col] == player:
                count = count + 1
                if count == 3:
                    threes = threes + 1
                    break
            else:
                break
        #Test for column to see whether there's a 3 consecutive one
        count = 1
        for i in reversed(range(0, new_col)):
            if board[new_row][i] == player:
                #print('LEFTTTTTTTT',new_col)
                count = count + 1
            else:
                break
        for i in range(new_col+1, col):
            if board[new_row][i] == player:
                #print('RIGHTTTTTT',new_col)
                count = count + 1
            else:
                break
        if count >= 3:
            threes = threes + 1
        #Test for diagonals to see whether there's a 3 consecutive one
        count = 1
        for i in range(1,row):
            if new_row + i >= row or new_col + i >= col:
                break
            elif board[new_row+i][new_col+i] == player:
                count = count + 1
            else:
                break
        for i in range(1, row):
            if new_row - i < 0 or new_col - i < 0:
                break
            elif board[new_row-i][new_col-i] == player:
                count = count + 1
            else:
                break
        if count >= 3:
            threes = threes + 1
        count = 1
        for i in range(1, row):
            if new_row + i >= row or new_col - i < 0:
                break
            elif board[new_row+i][new_col-i] == player:
                count = count + 1
            else:
                break
        for i in range(1, row):
            if new_row - i < 0 or new_col + i >= col:
                break
            elif board[new_row-i][new_col+i] == player:
                count = count + 1
            else:
                break
        if count >= 3:
            threes = threes + 1
        # Return the number of threes
        return threes
    
    def checkfortwos(self, board, row, col, new_row, new_col, player):
        count = 0
        if new_row - 1 >= 0 and board[new_row-1][new_col] == player:
            count = count + 1
        if new_row + 1 < row and board[new_row+1][new_col] == player:
            count = count + 1
        if new_col - 1 >= 0 and board[new_row][new_col-1] == player:
            count = count + 1
        if new_col + 1 < col and board[new_row][new_col+1] == player:
            count = count + 1
        if new_row - 1 >= 0 and new_col - 1 >= 0 and board[new_row-1][new_col-1] == player:
            count = count + 1
        if new_row - 1 >= 0 and new_col + 1 < col and board[new_row-1][new_col+1] == player:
            count = count + 1
        if new_row + 1 < row and new_col - 1 >= 0 and board[new_row+1][new_col-1] == player:
            count = count + 1
        if new_row + 1 < row and new_col + 1 < col and board[new_row+1][new_col+1] == player:
            count = count + 1
        return count
        
        
    
