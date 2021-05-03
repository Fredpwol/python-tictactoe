import tkinter as tk
from tkinter import messagebox


class MainGame(tk.Tk):
    
    def __init__(self, height=600, width=700):
        tk.Tk.__init__(self)
        self.height = height
        self.width = width
        self.geometry(f"{self.width}x{self.height}")
        tk.Label(self, text="Tic-Tac-Toe", font=("Roboto", 28, "bold"), anchor="e").place(relx=0.4, rely=0.3)
        tk.Button(self, text="One-on-One",  font=("Roboto", 16), bg="#91c1f2",anchor="center", command=self.start_vs_opponents).place(relx=0.2, rely=0.4, relwidth=0.6, height=70)
        tk.Button(self, text="Vs-Ai",  font=("Roboto", 16), bg="#91c1f2",anchor="center", command=self.start_vs_ai).place(relx=0.2, rely=0.53, relwidth=0.6, height=70)
        tk.Button(self, text="Vs-Multiplayer",  font=("Roboto", 16), bg="#91c1f2",anchor="center").place(relx=0.2, rely=0.66, relwidth=0.6, height=70)

    def start_vs_ai(self):
        self.destroy()
        TicTacToe(is_ai=True).mainloop()


    def start_vs_opponents(self):
        self.destroy()
        TicTacToe(is_ai=False).mainloop()

class TicTacToe(tk.Tk):

    def __init__(self, height=600, width=700, is_ai=False):
        tk.Tk.__init__(self)
        self.height = height
        self.width = width
        self.BOARD =  [[tk.StringVar(),tk.StringVar() , tk.StringVar()],
                      [tk.StringVar(), tk.StringVar(), tk.StringVar()],  
                      [tk.StringVar(), tk.StringVar(), tk.StringVar()]]
        self.geometry(f"{self.width}x{self.height}")
        self.grid_height = 600 // 3
        self.grid_width = 700 // 3
        self.player1 = 'X'
        self.player2 = "O"
        self.is_ai = is_ai
        self.grade = {"X":-1, "O":1, "": 0}
        self.current_player = self.player1
        self.board_grid = tk.Frame(self,height=self.height, width=self.width )
        self.board_grid.pack()
        for i in range(len(self.BOARD)):
            for j in range(3):
                grid = tk.Frame(self.board_grid, height=self.grid_height, width=self.grid_width, borderwidth=5, relief="solid")
                value = tk.Label(grid, font=("Roboto", 50), textvariable=self.BOARD[i][j])
                value.place(relheight=0.5, relwidth=0.5, relx=0.5, rely=0.5, anchor="center")
                grid.grid(row=i, column=j)
                value.bind("<Button1-ButtonRelease>", self.change_grid)
                grid.bind("<Button1-ButtonRelease>", self.change_grid)
                # self.grids.append(point)
        
    def change_grid(self, event):
        x1 = event.x_root - self.board_grid.winfo_rootx()
        y1 = event.y_root - self.board_grid.winfo_rooty()
        # event.widget.configure(text=self.current_player)

        col, row = self.board_grid.grid_location(x1, y1)
        if (self.BOARD[row][col].get() == ""):
            self.BOARD[row][col].set(self.current_player)
            val = self.check_board()
            if (val):
                messagebox.showinfo(title="Game Over", message=f"Congrats {val}  you Have won the Game!")
                self.reset_board()
            elif (val == ""):
                messagebox.showinfo(title="Game Over", message=f"Game over with a Draw!!")
                self.reset_board()
            else:
                self.current_player = self.player1 if self.current_player == self.player2 else self.player2
                if self.is_ai:
                    self.ai_play()


    def check_board(self):
        for i in range(3):
            if (self.BOARD[i][0].get() == self.BOARD[i][1].get() == self.BOARD[i][2].get()) and (self.BOARD[i][0].get() != ""):
                return self.BOARD[i][0].get()
        for i in range(3):
            if (self.BOARD[0][i].get() == self.BOARD[1][i].get() == self.BOARD[2][i].get()) and (self.BOARD[0][i].get() != ""):
                return self.BOARD[0][i].get()
        if (self.BOARD[0][0].get() == self.BOARD[1][1].get() == self.BOARD[2][2].get()) and (self.BOARD[0][0].get() != ""):
            return self.BOARD[0][0].get()
        
        if (self.BOARD[2][0].get() == self.BOARD[1][1].get() == self.BOARD[0][2].get()) and (self.BOARD[2][0].get() != ""):
            return self.BOARD[0][2].get()
        
        for i in range(3):
            for j in range(3):
                if self.BOARD[i][j].get() == "":
                    return None
        return ""

    
    def reset_board(self):
        self.current_player = self.player1
        for i in range(3):
            for j in range(3):
                self.BOARD[i][j].set("")


    def ai_play(self):
        max_eval = -1*float('inf')
        row, col = 0, 0
        alpha, beta = -1*float("inf"), float("inf")
        for i in range(3):
            for j in range(3):
                if self.BOARD[i][j].get() == "":
                    self.BOARD[i][j].set(self.current_player)
                    # uncomment this line and the method below to use alpha beta
                    score = self.minimax_alpha_beta(alpha, beta, maximize=False)
                    # score = self.minimax(maximize=False)
                    if score >= max_eval:
                        row, col = i, j
                        max_eval = score
                    self.BOARD[i][j].set("")
        self.BOARD[row][col].set(self.current_player)
        val = self.check_board()
        if (val):
            messagebox.showinfo(title="Game Over", message=f"Congrats {val}  you Have won the Game!")
            self.reset_board()
        elif (val == ""):
            messagebox.showinfo(title="Game Over", message=f"Game over with a Draw!!")
            self.reset_board()
        else:
            self.current_player = self.player1 if self.current_player == self.player2 else self.player2


    def minimax(self, maximize=True):
        """
        This is the vanilla algorithm for calculating minimax
        #NOTE: This is very computionally inefficient and is advised to use alpha beta prunning
        """
        score = self.check_board()
        if score != None:
            return self.grade[score]

        if maximize:
            maxEval = -float("inf")
            for i in range(3):
                for j in range(3):
                    if self.BOARD[i][j].get() == "":
                        self.BOARD[i][j].set(self.player2)
                        eval = self.minimax(maximize=False)
                        self.BOARD[i][j].set("")
                        maxEval = max(eval, maxEval)
            return maxEval
        else:
            minEval = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.BOARD[i][j].get() == "":
                        self.BOARD[i][j].set(self.player1)
                        eval = self.minimax(maximize=True)
                        self.BOARD[i][j].set("")
                        minEval = min(eval, minEval)
            return minEval




    def minimax_alpha_beta(self, alpha, beta, maximize=True):
        """
        Minmax with alpha beta prunning is a tweak to the normal minimax algorithm to improve perfromance by
        using heuristics to check wether a branch in the minimax tree is worth going through.

        ##UNCOMMENT the block of in the ai_play method to use alpha beta prunning
        """
        score = self.check_board()
        if score != None:
            # print(score)
            return self.grade[score]

        if maximize:
            maxEval = -float("inf")
            for i in range(3):
                for j in range(3):
                    if self.BOARD[i][j].get() == "":
                        self.BOARD[i][j].set("O")
                        eval0 = self.minimax_alpha_beta(alpha, beta, maximize=False)
                        self.BOARD[i][j].set("")
                        maxEval = max(eval0, maxEval)
                        alpha = max(alpha, eval0)
                        if alpha > maxEval:
                             return maxEval
            return maxEval
        else:
            minEval = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.BOARD[i][j].get() == "":
                        self.BOARD[i][j].set("X")
                        eval1 = self.minimax_alpha_beta(alpha, beta, maximize=True)
                        self.BOARD[i][j].set("")
                        minEval = min(eval1, minEval)
                        beta = min(beta, eval1)
                        if beta < minEval:
                           return minEval
            return minEval
        





if __name__ == "__main__":
    app = MainGame()
    app.mainloop()




