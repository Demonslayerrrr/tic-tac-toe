import json
from copy import deepcopy
from random import choice, random

class TicTacToe:
    def __init__(self):
        self.board = [["_", "_", "_"] for _ in range(3)]
        self.game_history = []  
        self.memory_file = "game_memory.json" 
        self.learned_memory = self.load_memory() 

    def load_memory(self):
        try:
            with open(self.memory_file, "r") as file:
                raw_memory = json.load(file)
                return {eval(key): value for key, value in raw_memory.items()}
        except FileNotFoundError:
            return {}

    def save_memory(self):
        saveable_memory = {str(key): value for key, value in self.learned_memory.items()}
        with open(self.memory_file, "w") as file:
            json.dump(saveable_memory, file, indent=4)

    def update_memory(self, winner):
        for entry in self.game_history:
            move = tuple(entry["move"]) 
            if move not in self.learned_memory:
                self.learned_memory[move] = {"wins": 0, "losses": 0, "draws": 0}

            if winner == "X":
                self.learned_memory[move]["wins"] += 1
            elif winner == "O":
                self.learned_memory[move]["losses"] += 1
            else:
                self.learned_memory[move]["draws"] += 1

    def get_valid_moves(self):
        valid_moves = []
        for r_index, row in enumerate(self.board):
            for c_index, column in enumerate(row):
                if column == "_":
                    valid_moves.append((r_index, c_index))
        return valid_moves

    def check_winner(self, board):
        # Check rows, columns, and diagonals
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

        if all(cell != "_" for row in board for cell in row):
            return "_"

        return None

    def simulate_game(self, board, turn):
        while True:
            winner = self.check_winner(board)
            if winner is not None:
                return winner
            
            valid_moves = self.get_valid_moves_for_board(board)
            move = choice(valid_moves)
            board[move[0]][move[1]] = turn
            turn = "X" if turn == "O" else "O"

    def get_valid_moves_for_board(self, board):
        valid_moves = []
        for r_index, row in enumerate(board):
            for c_index, column in enumerate(row):
                if column == "_":
                    valid_moves.append((r_index, c_index))
        return valid_moves

    def agent_move(self):
        valid_moves = self.get_valid_moves()
        move_scores = {move: 0 for move in valid_moves}
        simulations_per_move = 100


        for move in valid_moves:
            simulated_board = deepcopy(self.board)
            simulated_board[move[0]][move[1]] = "X"
            if self.check_winner(simulated_board) == "X":
                move_scores[move] += 10  


        for move in valid_moves:
            for _ in range(simulations_per_move):
                simulated_board = deepcopy(self.board)
                simulated_board[move[0]][move[1]] = "X"
                result = self.simulate_game(simulated_board, "O")
                if result == "X":
                    move_scores[move] += 1
                elif result == "_":
                    move_scores[move] += 0.5  


            if move in self.learned_memory:
                move_scores[move] += 2 * self.learned_memory[move]["wins"]
                move_scores[move] -= 2 * self.learned_memory[move]["losses"]

        best_move = max(move_scores, key=move_scores.get)
        self.board[best_move[0]][best_move[1]] = "X"
        self.game_history.append({"move": best_move, "board": deepcopy(self.board)})
        return self.board

    def human_move(self):
        valid_moves = self.get_valid_moves()
        print("\nYour turn! Enter your move as `col,row`: ")
        while True:
            try:
                move = input("> ").strip()
                col, row = map(int, move.split(","))
                if (row, col) in valid_moves:
                    self.board[row][col] = "O"
                    self.game_history.append({"move": (row, col), "board": deepcopy(self.board)})
                    return self.board
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter in the format `row,col`.")

    def run(self):
        who_starts = random()

        if who_starts < 0.5:
            turn = "X"
        else:
            turn = "O"

        winner = None

        while winner is None:
            print("\nCurrent board:\n")
            for row in self.board:
                print(" ".join(row))

            if turn == "X":  
                print("\nAgent's Turn")
                self.agent_move()
                turn = "O"  
            else: 
                self.human_move()
                turn = "X"  

            winner = self.check_winner(self.board)

        print("\nFinal board:")
        for row in self.board:
            print(row)

        if winner in ["X", "O"]:
            print(f"{winner} wins")
        else:
            print("draw")


        self.update_memory(winner) 
        self.save_memory() 
        print("\nGame memory updated and saved!")


a = TicTacToe()
a.run()
