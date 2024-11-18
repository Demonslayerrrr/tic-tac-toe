from random import choice
from copy import deepcopy

class TicTacToe:
    def __init__(self):
        self.board = [["_","_","_"] for _ in range(3)]

    def get_valid_moves(self):
        valid_moves= []

        for r_index,row in enumerate(self.board):
            for c_index,column in enumerate(row):
                if column == "_":
                    valid_moves.append((r_index,c_index))
        return valid_moves
    
    def check_winner(self,board):
        for row in board:
            if row == ["X", "X", "X"]:
                return "X"
            elif row == ["O", "O", "O"]:
                return "O"

        for col in range(3):
            column = [board[row][col] for row in range(3)]
            if column == ["X", "X", "X"]:
                return "X"
            elif column == ["O", "O", "O"]:
                return "O"


        diagonal1 = [board[i][i] for i in range(3)]  
        diagonal2 = [board[i][2 - i] for i in range(3)] 

        if diagonal1 == ["X", "X", "X"] or diagonal2 == ["X", "X", "X"]:
            return "X"
        elif diagonal1 == ["O", "O", "O"] or diagonal2 == ["O", "O", "O"]:
            return "O"


        if all(cell != "_" for row in self.board for cell in row):
            return "_"

        return None

    
    def whose_turn(self):
        count_1 = sum(row.count("X") for row in self.board) 
        count_minus1 = sum(row.count("O") for row in self.board)

        return "X" if count_1 <= count_minus1 else "O"
    
    def simulate_game(self,board,turn):
        while True:
            winner = self.check_winner(board)
            if winner is not None:
                return winner  
            
            valid_moves = self.get_valid_moves()
            move = choice(valid_moves)  
            board[move[0]][move[1]] = turn
            turn = "X" if turn == "O" else "O"
        
    def agent_move(self):
        valid_moves = self.get_valid_moves()

        move_score = {move: 0 for move in valid_moves}

        epochs = 100

        for move in valid_moves:
            for _ in range(epochs):

                simulated_board = deepcopy(self.board)

                simulated_board[move[0]][move[1]] = "X"

                result = self.simulate_game(simulated_board,"O")

                if result == "X":
                    move_score[move]+=1
                elif result == "_":
                    move_score[move]+=0.5

        best_move = max(move_score, key=move_score.get)

        self.board[best_move[0]][best_move[1]] = "X"

        return self.board
    
    def opponent_move(self):
        move = choice(self.get_valid_moves())

        row,col = move

        self.board[row][col] = "O"

        return self.board
    
    def run(self):
        winner = None

        while winner is None:
            print("Current board\n")
            
            for i in self.board:
                print(i)

            turn = self.whose_turn()

            if turn == "X":  
                print("------------\nAgent's Turn")
                board = self.agent_move()
            else:  
                print("------------\nOpponent's Turn")
                board = self.opponent_move()
    
            winner = self.check_winner(board)

        if winner == "X":
            print("Agent Wins!")
        elif winner == "O":
            print("Opponent Wins!")
        else:
            print("It's a Draw!")

        for i in self.board:
            print(i)
    
a = TicTacToe()

a.run()
