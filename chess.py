
import tkinter as tk
from game import Game


class Square(tk.Canvas):

    def __init__(self, parent, color, coordinates):
        """coordinates can be for example "a1"."""
        tk.Canvas.__init__(self, parent, width=square_side_length,
                           height=square_side_length, bg=color, highlightthickness=0)
        self.bind("<Button-1>", self.mouse_click)
        self.coordinates = coordinates
        self.highlight = False
        self.highlight_rectangle = self.create_rectangle(0, 0, square_side_length-1,
                                       square_side_length-1, width=7, outline=highlight_color,
                                       state=tk.HIDDEN)
        self.piece = None
        self.image = self.create_image(0, 0, anchor=tk.NW, state=tk.HIDDEN)

    def unbind_mouse(self):
        self.unbind("<Button-1>")

    def rebind_mouse(self):
        self.bind("<Button-1>", self.mouse_click)

    def update_image(self):
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

    def toggle_highlight(self):
        self.highlight = not self.highlight
        if self.highlight:
            self.itemconfig(self.highlight_rectangle, state=tk.NORMAL)
        else:
            self.itemconfig(self.highlight_rectangle, state=tk.HIDDEN)

    def reset_highlight(self):
        self.highlight = False
        self.itemconfig(self.highlight_rectangle, state=tk.HIDDEN)

    def mouse_click(self, event):
        global highlight_square
        if highlight_square == None:
            if game.board_value(self.coordinates) != None:
                if player_is_white:
                    if game.board_value(self.coordinates) in "KQRBNP":
                        highlight_square = self
                        self.toggle_highlight()
                else:
                    if game.board_value(self.coordinates) in "kqrbnp":
                        highlight_square = self
                        self.toggle_highlight()
        else:
            if highlight_square == self:
                highlight_square = None
                self.toggle_highlight()
            else:
                if game.board_value(self.coordinates) != None:
                    if player_is_white:
                        if game.board_value(self.coordinates) in "KQRBNP":
                            highlight_square.toggle_highlight()
                            highlight_square = self
                            self.toggle_highlight()
                            return
                    else:
                        if game.board_value(self.coordinates) in "kqrbnp":
                            highlight_square.toggle_highlight()
                            highlight_square = self
                            self.toggle_highlight()
                            return
                move = highlight_square.coordinates + self.coordinates
                # If white promotion.
                if game.board_value(highlight_square.coordinates) == "P":
                    if highlight_square.coordinates[1] == "7":
                        move += "q"
                # If black promotion.
                if game.board_value(highlight_square.coordinates) == "p":
                    if highlight_square.coordinates[1] == "2":
                        move += "q"
                highlight_square.toggle_highlight()
                highlight_square = None
                if game.legal(move):
                    board.unbind_mouse()
                    game.make_move(move)
                    board.update_squares()

                    if game.check_mate():
                        status_bar.set_text("You win! Check mate.")
                        return
                    if game.stale_mate():
                        status_bar.set_text("Stale mate")
                        return
                    if game.insufficient_material():
                        status_bar.set_text("Draw by insufficient material.")
                        return
                    if game.threefold_repetition():
                        status_bar.set_text("Draw by threefold repetition.")
                        return
                    if game.possible_draw_by_50_move_rule():
                        status_bar.set_text("Draw by the 50 move rule.")
                        return

                    status_bar.set_text("Thinking..")
                    root.update_idletasks()
                    move = game.computer_move()
                    game.make_move(move)
                    board.update_squares()

                    if game.check_mate():
                        status_bar.set_text("Computer win! Check mate.")
                        return
                    if game.stale_mate():
                        status_bar.set_text("Stale mate")
                        return
                    if game.insufficient_material():
                        status_bar.set_text("Draw by insufficient material.")
                        return
                    if game.threefold_repetition():
                        status_bar.set_text("Draw by threefold repetition.")
                        return
                    if game.possible_draw_by_50_move_rule():
                        status_bar.set_text("Draw by the 50 move rule.")
                        return

                    status_bar.set_text("Your turn")
                    board.update() # Handle possible events.
                    board.rebind_mouse()


class Board(tk.Frame):

    def __init__(self, parent):
        self.square_list = []
        self.rank_labels = []
        self.file_labels = []
        tk.Frame.__init__(self, parent, bg=coordinate_label_color)

        # Make squares.
        for r in range(0, 8):
            for f in range(1, 9):
                color = [dark_square_color, light_square_color][(r + f) % 2]
                coordinates = "abcdefgh"[f-1] + str(8-r)
                square = Square(self, color, coordinates)
                square.grid(row=r, column=f)
                self.square_list.append(square)

        # Make labels.
        for r in range(0, 8):
            rank_label = tk.Label(self, text=str(8-r), padx=4, bg=coordinate_label_color)
            rank_label.grid(row=r, column=0)
            self.rank_labels.append(rank_label)

        for f in range(1, 9):
            file_label = tk.Label(self, text="abcdefgh"[f-1], bg=coordinate_label_color)
            file_label.grid(row=8, column=f)
            self.file_labels.append(file_label)

    def unbind_mouse(self):
        for square in self.square_list:
            square.unbind_mouse()

    def rebind_mouse(self):
        for square in self.square_list:
            square.rebind_mouse()

    def set_normal_orientation(self):
        for square in self.square_list:
            r = 8 - int(square.coordinates[1])
            f = "abcdefgh".find(square.coordinates[0]) + 1
            square.grid(row=r, column = f)
        for n in range(8):
            self.rank_labels[n].grid(row=n)
            self.file_labels[n].grid(column=n+1)

    def set_upside_down_orientation(self):
        for square in self.square_list:
           r = int(square.coordinates[1]) - 1
           f = 8 - "abcdefgh".find(square.coordinates[0])
           square.grid(row=r, column = f)
        for n in range(8):
            self.rank_labels[n].grid(row=7-n)
            self.file_labels[n].grid(column=8-n)

    def reset_highlight(self):
        global highlight_square
        highlight_square = None
        for square in self.square_list:
            square.reset_highlight()

    def update_squares(self):
        for square in self.square_list:
            square.update_image()


class StatusBar(tk.Label):

    def __init__(self, parent):
        tk.Label.__init__(self, parent, text="", anchor=tk.W, bg=status_bar_color)

    def set_text(self, new_text):
        self.config(text=new_text)


def new_game_white():
    global player_is_white
    player_is_white = True
    global game
    game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")
    board.set_normal_orientation()
    board.reset_highlight()
    board.update_squares()
    board.rebind_mouse()
    status_bar.set_text("Your turn")

def new_game_black():
    global player_is_white
    player_is_white = False
    global game
    game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")
    status_bar.set_text("Thinking..")
    root.update_idletasks()
    move = game.computer_move()
    game.make_move(move)
    board.set_upside_down_orientation()
    board.reset_highlight()
    board.update_squares()
    board.rebind_mouse()
    status_bar.set_text("Your turn")

game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")

player_is_white = True
highlight_square = None
coordinate_label_color = "#DDDDDD"
light_square_color = "#DDDDDD"
dark_square_color = "#405088"
status_bar_color = "#CCCCCC"
highlight_color = "#00DDFF"

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

square_side_length = 60

board = Board(root)
board.update_squares()
board.pack()

status_bar = StatusBar(root)
status_bar.pack(fill=tk.X)
status_bar.set_text("Your turn")

menubar = tk.Menu(root, relief="flat", borderwidth=0)
menu = tk.Menu(menubar, tearoff=0)
menu.add_command(label="New game - white", command=new_game_white)
menu.add_command(label="New game - black", command=new_game_black)
menu.add_separator()
menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Menu", menu=menu)
root.config(menu=menubar)

root.mainloop()

