import copy
from connect_AI import *
from chung514_huxxx952_AI import *

class ConnectFour:
    # Initiate the Connect Four game board
    # row - how many rows the board are
    # col - how many columns the board are
    # turn - which player's turn, player 1 or player 2
    # board - the game board constructed by a two-dimensional list

    
    def __init__ (self, row, col):
        print('col=',col,'row=',row)
        self.row = row
        self.col = col
        self.turn = 1
        self.board = []
        self.board = [[0 for i in range(0, col)] for j in range(0, row)]
        print(self.board)

    # drop a disc in a column
    # drop_col - the column the player want to drop a disc
    # player - which player, 1 or 2
    def dropDisc(self, drop_col, player):
        print("player", player, 'drops in col',drop_col)
        for i in range(0, self.row):
            if self.board[i][drop_col] != 0 and i == 0:
                return -1
            elif self.board[i][drop_col] != 0:
                self.board[i-1][drop_col] = player
                return i-1
            if i == self.row-1:
                self.board[i][drop_col] = player
                return self.row-1

    # test if dropping this disc will make the player win
    # new_row - which row the disc dropped is at
    # new_col - which column the disc dropped is at
    def goalTest(self, new_row, new_col):
        # Test for row to see whether there's a 4 consecutive one
        count = 1
        player = self.board[new_row][new_col]
        for i in range(new_row+1, self.row):
            if self.board[i][new_col] == player:
                count = count + 1
                if count == 4:
                    return True
            else:
                break

        #Test for column to see whether there's a 4 consecutive one
        count = 1
        for i in reversed(range(0, new_col)):
            if self.board[new_row][i] == player:
                count = count + 1
            else:
                break
        for i in range(new_col+1, self.col):
            if self.board[new_row][i] == player:
                count = count + 1
            else:
                break
        if count >= 4:
            return True
        #Test for diagonals to see whether there's a 4 consecutive one
        count = 1
        for i in range(1,self.row):
            if new_row + i >= self.row or new_col + i >= self.col:
                break
            elif self.board[new_row+i][new_col+i] == player:
                count = count + 1
            else:
                break
        for i in range(1, self.row):
            if new_row - i < 0 or new_col - i < 0:
                break
            elif self.board[new_row-i][new_col-i] == player:
                count = count + 1
            else:
                break
        if count >= 4:
            return True
        count = 1
        for i in range(1, self.row):
            if new_row + i >= self.row or new_col - i < 0:
                break
            elif self.board[new_row+i][new_col-i] == player:
                count = count + 1
            else:
                break
        for i in range(1, self.row):
            if new_row - i < 0 or new_col + i >= self.col:
                break
            elif self.board[new_row-i][new_col+i] == player:
                count = count + 1
            else:
                break
        if count >= 4:
            return True
        # If no consecutive 4 discs are found, return False
        return False
    
    # print the board
    def printboard(self):
        for i in range(0,self.row):
            print(self.board[i])
            
    # A player drop a disc at the "in_col" column
    # and check whether he/she wins or not
    #-1 : not accept, 0 : not finish, 1 : game is finished
    def play(self, in_col, player):
        if player != self.turn:
            return -1
        else:
            in_row = 0
            in_row = self.dropDisc(in_col, player)
            if in_row == -1:
                return -1
            else:
                print('incol=',in_col,'inrow=',in_row)
                self.printboard()
                win = -1
                win = self.goalTest(in_row, in_col)
                if win:
                    #print('Player', player, 'wins !!')
                    return 1
                else:
                    if self.turn == 1:
                        self.turn = 2
                    else:
                        self.turn = 1
                    return 0

    def checkBoard(self):
        return copy.deepcopy(self.board)

class human:

    def __init__(self, player):
        self.player = player
        self.rival = 1
        if self.player == self.rival:
            self.rival = 2

    def name(self):
        return "human"

    def decide(self, board):
        return int(input())


# This is an example of how to play
def main(mode):
    game = ConnectFour(6, 8)
    isFinish = False
    #create two AI here
    if mode == 1:
        AI1 = SimonaAI(1)
        AI2 = chung514_huxxx952_AI(2)
    elif mode == 2:
        AI1 = chung514_huxxx952_AI(1)
        AI2 = SimonaAI(2)
    print("Player1 : ", AI1.name(), "Player2 : ", AI2.name())
        
    while isFinish == False:
        if game.turn == 1:
            ans = AI1.decide(game.checkBoard())
            result = game.play(ans, 1)
            if result == -1:
                print(AI1.name(), "left the game!")
                isFinish = True
            elif result == 0:
                continue
            else:
                print(AI1.name(), "win this game")
                isFinish = True
        else:
            ans = AI2.decide(game.checkBoard())
            result = game.play(ans, 2)
            if result == -1:
                print(AI2.name(), "left the game!")
                isFinish = True
            elif result == 0:
                continue
            else:
                print(AI2.name(), "win the game")
                isFinish = True


if __name__ == "__main__":
    main(1)
    main(2)

