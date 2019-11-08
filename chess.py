
import tkinter as tk
from game import Game


class Square(tk.Canvas):

    def __init__(self, parent, side_length, color, coordinates):
        """coordinates can be for example "a1"."""
        tk.Canvas.__init__(self, parent, width=side_length, height=side_length,
                           bg=color, highlightthickness=0)
        self.bind("<Button-1>", self.mouse_click)
        self.coordinates = coordinates
        self.side_length = side_length
        self.high_light = False
        self.high_light_rectangle = self.create_rectangle(0, 0, self.side_length-1,
                                       self.side_length-1, width=7, outline="#00DDFF",
                                       state=tk.HIDDEN)
        self.piece = None
        self.image = self.create_image(0, 0, anchor=tk.NW, state=tk.HIDDEN)

    def update(self):
        piece = game.board_value(self.coordinates)
        if self.piece != piece:
            if piece == None:
                self.itemconfig(self.image, state=tk.HIDDEN)
            if piece == "K":
                self.itemconfig(self.image, image=image_K, state=tk.NORMAL)
            if piece == "Q":
                self.itemconfig(self.image, image=image_Q, state=tk.NORMAL)
            if piece == "R":
                self.itemconfig(self.image, image=image_R, state=tk.NORMAL)
            if piece == "B":
                self.itemconfig(self.image, image=image_B, state=tk.NORMAL)
            if piece == "N":
                self.itemconfig(self.image, image=image_N, state=tk.NORMAL)
            if piece == "P":
                self.itemconfig(self.image, image=image_P, state=tk.NORMAL)
            if piece == "k":
                self.itemconfig(self.image, image=image_k, state=tk.NORMAL)
            if piece == "q":
                self.itemconfig(self.image, image=image_q, state=tk.NORMAL)
            if piece == "r":
                self.itemconfig(self.image, image=image_r, state=tk.NORMAL)
            if piece == "b":
                self.itemconfig(self.image, image=image_b, state=tk.NORMAL)
            if piece == "n":
                self.itemconfig(self.image, image=image_n, state=tk.NORMAL)
            if piece == "p":
                self.itemconfig(self.image, image=image_p, state=tk.NORMAL)
            self.piece = piece

    def toggle_high_light(self):
        self.high_light = not self.high_light
        if self.high_light:
            self.itemconfig(self.high_light_rectangle, state=tk.NORMAL)
        else:
            self.itemconfig(self.high_light_rectangle, state=tk.HIDDEN)

    def mouse_click(self, event):
        global high_light_square
        if high_light_square == None:
            if game.board_value(self.coordinates) != None:
                if game.board_value(self.coordinates) in "KQRBNP":
                    high_light_square = self
                    self.toggle_high_light()
        else:
            if high_light_square == self:
                high_light_square = None
                self.toggle_high_light()
            else:
                if game.board_value(self.coordinates) != None:
                    if game.board_value(self.coordinates) in "KQRBNP":
                        high_light_square.toggle_high_light()
                        high_light_square = self
                        self.toggle_high_light()
                        return
                move = high_light_square.coordinates + self.coordinates
                # If white promotion.
                if game.board_value(high_light_square.coordinates) == "P":
                    if high_light_square.coordinates[1] == "7":
                        move += "q"
                # If black promotion.
                if game.board_value(high_light_square.coordinates) == "p":
                    if high_light_square.coordinates[1] == "2":
                        move += "q"
                high_light_square.toggle_high_light()
                high_light_square = None
                print(move)
                if game.legal(move):
                    game.make_move(move)
                    squares.update()
                    move = game.computer_move()
                    game.make_move(move)
                    squares.update()


class Squares(tk.Frame):

    def __init__(self, parent):
        self.side_length = 60
        self.light_square_color = "#DDDDDD"
        self.dark_square_color = "#222244"
        tk.Frame.__init__(self, parent)
        self.square_list = []
 
        def rank(parent, number):
            frame = tk.Frame(parent)
            for n in range(8):
                color = [self.dark_square_color, self.light_square_color][(n + number + 1) % 2]
                coordinates = "abcdefgh"[n] + str(number)
                square = Square(frame, self.side_length, color, coordinates)
                square.pack(side=tk.LEFT)
                self.square_list.append(square)
            return frame

        for n in range(1, 9):
            rank(self, n).pack(side=tk.BOTTOM)

    def update(self):
        for square in self.square_list:
            square.update()


#game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")
game = Game("4k2r/P7/8/8/5n2/7b/8/3NK3 w K -")

high_light_square = None

root = tk.Tk()
root.title("Chess")
root.resizable(False, False)

image_K = tk.PhotoImage(file="Images/Chess_klt60.gif")
image_Q = tk.PhotoImage(file="Images/Chess_qlt60.gif")
image_R = tk.PhotoImage(file="Images/Chess_rlt60.gif")
image_B = tk.PhotoImage(file="Images/Chess_blt60.gif")
image_N = tk.PhotoImage(file="Images/Chess_nlt60.gif")
image_P = tk.PhotoImage(file="Images/Chess_plt60.gif")
image_k = tk.PhotoImage(file="Images/Chess_kdt60.gif")
image_q = tk.PhotoImage(file="Images/Chess_qdt60.gif")
image_r = tk.PhotoImage(file="Images/Chess_rdt60.gif")
image_b = tk.PhotoImage(file="Images/Chess_bdt60.gif")
image_n = tk.PhotoImage(file="Images/Chess_ndt60.gif")
image_p = tk.PhotoImage(file="Images/Chess_pdt60.gif")

squares = Squares(root)
squares.pack()
squares.update()

root.mainloop()




