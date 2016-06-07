from Tkinter import *
import time
import threading
import Queue
import string
import numpy as np
import cv2
from sampler_class import Sampler
from state_representation.math import Math
import copy


class GuiPart:
    DEBUG = 1
    DEBUG_BIG_THINGS = 1
    DEBUG_PRINT_FUNCTIONS = 1
    # The Tuneable Constants
    DELAY = 0  # 885=1 sec.
    SQUARESIZE = 50
    PIECE_DIAMETER = 35

    CHECK_COMPLETE = 0
    ACCEPT_MOVE = 0
    JUMBS = 0

    def __init__(self, master, queue):
        self.queue = queue
        """This is the constructor. It includes some basic startup work that
        would not fit anywhere else, and then it calls self.begin_new_game.
        It does not require any variables."""

        self.counter = 0

        global ACCEPT_MOVE

        self.piece_offset = (self.SQUARESIZE - self.PIECE_DIAMETER)  # calulation saver

        if master == None:  # master creator
            master = Tk()
        self.master = master
        self.master.title("Checkers")
        if self.DEBUG:
            self.master.bind("<2>", self.remove_piece)
        self.master.protocol("WM_DELETE_WINDOW", self.end)  # handle the exit
        self.master.bind("<Escape>", self.end)
        # self.master.bind("t", self.erace_temporary)
        # /|\
        # |  there are no temporary objects
        self.master.bind("[", self.go_to_move)
        # self.master.bind("d", self.do_move_one)
        self.make_display()

        self.begin_new_game()

    def get_accept_move(self):
        return self.ACCEPT_MOVE

    def set_accept_move(self, value):
        self.ACCEPT_MOVE = value

    def get_check_complete(self):
        return self.CHECK_COMPLETE

    def set_check_complete(self, value):
        self.CHECK_COMPLETE = value

    def get_jumbs(self):
        return self.JUMBS

    def set_jumbs(self, value):
        self.JUMBS = value

    def make_display(self):
        """This function will create the Canvas for the board, and then the board.
        The variables requiblue by this function are:
            self.master, self.SQUARESIZE."""
        foo = self.SQUARESIZE * 8  # calculation saver
        self.c = Canvas(self.master, height=foo, width=foo)
        self.message = Label(self.master, text="", bd=2, relief=RAISED, \
                             font=("", "10", ""))
        self.make_checker_squares(0, 7, "black")
        self.make_checker_squares(1, 8, "white", "squares")

        history_scroll = Scrollbar(self.master)
        self.history_display = Listbox(self.master, yscrollcommand=history_scroll.set)
        history_scroll.config(command=self.history_display.yview)
        self.history_display.bind("<Double-Button-1>", self.go_to_move)
        self.c.grid(row=1, column=0)
        self.message.grid(row=0, column=0, columnspan=3, pady=5)
        self.history_display.grid(row=1, column=1, sticky=N + S)
        history_scroll.grid(row=1, column=2, sticky=N + S)

        for baz in self.c.find_overlapping(self.SQUARESIZE * 1.5, \
                                           self.SQUARESIZE * 0.5, \
                                           self.SQUARESIZE * 1.5, \
                                           self.SQUARESIZE * 0.5):
            if self.c.type(baz) == "rectangle":
                self.upper_corner_square = baz


    def begin_new_game(self):
        """This is the function that begins a new game.  It will be run whenever
        a new game is needed.  It clears various variables, creates the pieces
        using make_pieces, binds the pieces and squares, binds the exit, and
        sets self.moving to the player who starts.  It then calls self.MoveLoop.
            This function requires self.message."""
        if self.DELAY:
            self.message.config(text="Creating new game...", fg="purple")

        # variable clearing
        self.c.itemconfig("squares", width=1, outline="black")
        self.quux = None  # temporary storage
        self.pieces = {"green": [], "blue": []}  # first list is green's pieces, then blue's pieces.
        self.piece = None
        self.piece_square = None
        self.square = ()
        self.count = -1
        self.oldmessage_info = ["", ""]
        self.c.delete("pieces")
        self.jumps = [[], []]
        self.jump_made = None
        self.c.delete("win_text")
        self.history = []
        self.history_display.delete(0, END)

        # flag setting
        self.got_move = 0
        self.got_piece = 0
        self.end_now = 0
        self.add_mode = 0
        self.remove_mode = 0

        self.make_pieces("green", self.DELAY)
        self.make_pieces("blue", self.DELAY)

        self.c.tag_bind("pieces", "<1>", self.get_piece_click)
        self.c.tag_bind("squares", "<1>", self.get_square_click)

        self.moving = "green"  # reversed since setup_move will switch it.

        if self.DEBUG_BIG_THINGS:
            print "self.pieces: ", self.pieces

        self.setup_move()

            # ++++++++++++++++++++++++++++++++++++++++more detailed functions+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def cleanup_move(self, type):
        """This function clears various variables.  It has a type argument so
        that it can clean only partway so other functions can use some of the
        variables"""
        if type == 3:
            self.jump_made = None
            self.piece = None
        if type == 2:
            self.got_piece = 0
            self.c.itemconfig(self.piece_square, outline="black", width=1)
            self.jumps = [[], []]
        if type == 1:
            self.got_move = 0
            self.square = ()

    def setup_move(self):
        """This does the setup requiblue of a move.  It checks for kings to be
        crowned, and checks for double jumps with the check_for_jumps function.
        If there are no double jumps, it toggles self.moving, sets the
        history, and checks for jumps again."""
        if self.DEBUG_PRINT_FUNCTIONS:
            print "setup_move"
        if self.DEBUG:
            print "lengh of history:", len(self.history)
            print "count:", self.count

        # kingmaker part
        not_crowning = 1
        for piece in self.pieces[self.moving]:
            if self.DEBUG_BIG_THINGS:
                print "self.c.coords(piece): ", self.c.coords(piece)
            if self.moving == "green":
                if self.c.coords(piece)[1] == self.piece_offset:
                    if self.DEBUG:
                        print "green kings!"
                    not_crowning = 0
                    self.c.itemconfig(piece, outline="gold2", width=3)
            if self.moving == "blue":
                if self.c.coords(piece)[1] == (self.SQUARESIZE * 7) + self.piece_offset:
                    if self.DEBUG:
                        print "blue kings!"
                    not_crowning = 0
                    self.c.itemconfig(piece, outline="gold2", width=3)

        # Dobble Jump checker
        self.check_for_jumps()
        if self.DEBUG_BIG_THINGS:
            print "self.jumps[0], self.jump_made: ", self.jumps[0], self.jump_made
        same_piece = 0
        for foo in self.jumps[0]:
            if foo[0] == self.piece:
                same_piece = 1
        if same_piece and not_crowning and self.jump_made != None:
            self.show_message("DOUBLE JUMP!!", 1)
            return
        else:
            # this creates a new turn.
            self.count = self.count + 1
            self.history.append([])
            for foo in self.pieces["blue"] + self.pieces["green"]:
                self.history[-1].append((self.c.itemcget(foo, "fill"), self.c.coords(foo), \
                                         self.c.itemcget(foo, "width")))
            if self.DEBUG_BIG_THINGS:
                print "self.history: ", self.history
            self.jumps = [[], []]
            if self.moving == "green":
                self.moving = "blue"
                self.message.config(text="blue's move!", fg="blue")
            else:
                self.moving = "green"
                self.message.config(text="green's move!", fg="green")
            if self.DEBUG:
                print "changed"
            self.check_for_jumps()

        if self.DEBUG:
            print "lengh of history:", len(self.history)

    def get_piece_click(self, event):
        """This function is called when a piece is clicked on.  It sets
        self.got_piece, and assigns the id of the piece clicked on to
        self.piece"""
        if self.DEBUG_PRINT_FUNCTIONS:
            pass;
            print "got_piece_click"
        if self.piece != None:
            self.c.itemconfig(self.piece_square, outline="green", width=1)
        try:
            self.piece_square, self.piece = self.c.find_overlapping(event.x, event.y, event.x, event.y)
            print "self.piece_square, self.piece: ", self.c.find_overlapping(event.x, event.y, event.x, event.y)
        except ValueError:
            return
        self.got_piece = 1

        if self.check_piece():  # positive numbers are failure, for check_piece
            self.piece_square = None
            self.piece = None
            self.got_piece = 0
        else:
            self.c.itemconfig(self.piece_square, outline="blue", width=3)

    def set_piece(self, piece_square, piece):
        print "i am in set_piece"
        if self.DEBUG_PRINT_FUNCTIONS:
            pass;
            print "set_piece"
        try:
            self.piece_square = piece_square
            self.piece = piece
        except ValueError:
            return
        self.got_piece = 1

        if self.check_piece():  # positive numbers are failure, for check_piece
            self.piece_square = None
            self.piece = None
            self.got_piece = 0

    def check_piece(self):
        """check_piece is called after get_piece returns.  It checks the color
        of the piece and currently does nothing else."""
        if self.DEBUG_PRINT_FUNCTIONS:
            pass;
            print "check_piece"
        # correct player checker
        if self.c.itemcget(self.piece, "fill") != self.moving:
            self.show_message("That is not your piece!")

            return 1
        return 0

    def get_square_click(self, event):
        """This function is called when a square is clicked on.  It only acts if self.got_piece has been
        set before.  When it acts, it sets self.got_move, and assigns the id of the square clicked on to
        self.square."""
        if self.DEBUG_PRINT_FUNCTIONS:
            pass;
            print "got_square_click"
        if self.got_piece:
            self.square = self.c.find_overlapping(event.x, event.y, event.x, event.y)
            if self.DEBUG:
                print "got square:", self.square
            self.got_move = 1

    def set_square(self, square):
        print "i am in set_square"
        if self.DEBUG_PRINT_FUNCTIONS:
            pass;
            print "got_square_click"
        if self.got_piece:
            self.square = square
            if self.DEBUG:
                print "got square:", self.square
            self.got_move = 1

    def check_move(self):
        """This function does all the verifiying requiblue for a move.  It checks
        for errors in the get_piece and get_square functions that cause no move
        to be reported. It then calulates some variables used in later checks.
        Then it checks if the move is a jump(if there are any jumps).  It then
        checks the direction of the move, the move's distence, and finally it
        includes a check for a piece in the square to be moved to, if this has
        not been caught before."""

        if self.DEBUG_PRINT_FUNCTIONS:
            pass;
            print "check_move"

        if len(self.square) != 1 or self.piece == None:
            if self.DEBUG:
                print "missing piece or square!"
            return 5
        sqr_cords = self.c.coords(self.square)  # square coords
        sqr_cntr = apply(self.find_center, sqr_cords)  # square center
        pce_cntr = apply(self.find_center, self.c.coords(self.piece))  # piece center
        vtr = (sqr_cntr[0] - pce_cntr[0], sqr_cntr[1] - pce_cntr[1])  # piece vector(distence and direction)
        if self.DEBUG:
            pass;  # print sqr_cords, sqr_cntr, pce_cntr, vtr

        if self.jumps[0]:  # jump checker
            # if move has not been found by check_for_jumps then fail
            # else, ingore all the other checks, and succeed
            if self.jumps[0].count((self.piece, vtr)) != 1:
                self.show_message("You have a jump!", .8)
                return 5
            else:
                self.jump_made = self.jumps[0].index((self.piece, vtr))
                if self.DEBUG:
                    print "jump_made: ", self.jump_made
                return 0

        # movement direction checker
        if self.c.itemcget(self.piece, "outline") != "gold2":
            if self.moving == "green":
                if vtr[1] > 0:
                    if self.DEBUG:
                        self.show_message("wrong way, green!")
                        print "wrong way, green!"
                    return 3
            else:
                if vtr[1] < 0:
                    if self.DEBUG:
                        self.show_message("wrong way, blue!")
                        print "wrong way, blue!"
                    return 3

        # distence checker
        if abs(vtr[0]) != self.SQUARESIZE or abs(vtr[1]) != self.SQUARESIZE:
            self.show_message("Too far!")
            return 4

        # square emptiness checker
        if self.c.type(self.c.find_overlapping(sqr_cords[0] + (self.SQUARESIZE / 2), \
                                               sqr_cords[1] + (self.SQUARESIZE / 2), \
                                               sqr_cords[2] - (self.SQUARESIZE / 2), \
                                               sqr_cords[3] - (self.SQUARESIZE / 2))) != "rectangle":
            if self.DEBUG:
                print "not empty: ", self.c.find_overlapping(sqr_cords[0] + (self.SQUARESIZE / 2), \
                                                             sqr_cords[1] + (self.SQUARESIZE / 2), \
                                                             sqr_cords[2] - (self.SQUARESIZE / 2), \
                                                             sqr_cords[3] - (self.SQUARESIZE / 2))
            return 2

        return 0

    def do_move(self):
        """This function actually moves the piece in self.piece to the square
        in self.square.  It also handdles various jumping details."""
        if self.DEBUG_PRINT_FUNCTIONS:
            pass;
            print "do_move"
        self.history_display.insert("end", str((self.piece_square - self.upper_corner_square) + 1) + "-" +
                                    str((self.square[0] - self.upper_corner_square) + 1))

        if self.jumps[0]:
            foo = self.pieces.keys()  # ugly hack to get the other color's pieces
            foo.remove(self.moving)

            self.pieces[foo[0]].remove(self.jumps[1][self.jump_made])
            self.c.delete(self.jumps[1][self.jump_made])

        foo = self.c.coords(self.square)  # calulation saver
        self.c.coords(self.piece, \
                      foo[0] + self.piece_offset, foo[1] + self.piece_offset, \
                      foo[2] - self.piece_offset, foo[3] - self.piece_offset)

    def GameDone(self):
        """This is the win checker.  It reports 0 if the game has not ended,
        2 for a win by blue, 1 for a win by green, and 3 for a draw."""
        if self.DEBUG_PRINT_FUNCTIONS:
            pass;  # print "GameDone"
        if self.pieces["green"] == []:
            return 1
        if self.pieces["blue"] == []:
            return 2
        return 0

    def AnotherGame(self):

        """This function asks if another game is wanted, and reports true or false,
        depending on the answer.  It requires module string,
        self.message, and self.master"""
        if self.DEBUG_PRINT_FUNCTIONS:
            pass;  # print "AnotherGame"
        # self.c.create_rectangle(0,0, int(self.c.cget('width')), \
        #                                 int(self.c.cget('height')), \
        #                                 stipple='gray50', fill='green',\
        #                                 tag='end_game_overlay')
        self.message.config(text="Do you want another game?", fg="gray25")

        class Answer:
            ans = ""

            def cb(self, event):
                self.ans = event.char

        answer = Answer()
        self.master.bind("y", answer.cb);
        self.master.bind("Y", answer.cb)
        self.master.bind("n", answer.cb);
        self.master.bind("N", answer.cb)
        while answer.ans == "":
            self.master.update()
        self.master.unbind("y");
        self.master.unbind("Y")
        self.master.unbind("n");
        self.master.unbind("N")
        #        self.c.delete('end_game_overlay')
        if string.lower(answer.ans) == "y":
            return 1
        else:
            return 0

            # ++++++++++++++++++++++++++++++++++++++++++++++helper functions++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def go_to_move(self, event=None, move_number=None, ):
        """This function will recreate previous positions by recreating all the pieces from the information
        in self.history"""
        if move_number == None:
            move_number = self.count - 1
        if event.widget == self.history_display:
            move_number = self.history_display.index("@" + str(event.x) + "," + str(event.y))
        if self.DEBUG:
            print "move_number:", move_number
        if move_number < 0:
            return 1

        self.c.delete("pieces")
        self.pieces["green"] = []
        self.pieces["blue"] = []
        for foo in self.history[move_number]:
            self.pieces[foo[0]].append(apply(self.c.create_oval, foo[1], {"fill": foo[0], "tag": "pieces"}))
            if foo[2] == 3:
                self.c.itemconfig(self.pieces[foo[0]][-1], width=3, outline="gold")
        if move_number % 2 == 0:  # not reversed since setup_move will flip them _twice_.
            self.moving = "green"
        else:
            self.moving = "blue"
        self.cleanup_move(1)
        self.cleanup_move(2)
        self.setup_move()
        self.cleanup_move(3)
        self.count = move_number
        self.history = self.history[:move_number + 1]
        self.history_display.delete(move_number, END)
        if self.DEBUG:
            print "lengh of history:", len(self.history)
        return 0

    def check_for_jumps(self):
        """This function checks all the possible jumps for self.moving pieces"""
        pass
        if self.DEBUG_PRINT_FUNCTIONS:
            print "check_for_jumps"
        if self.moving == "blue":
            baz_normal = [(2 * self.SQUARESIZE, 2 * self.SQUARESIZE), (-2 * self.SQUARESIZE, 2 * self.SQUARESIZE)]
        if self.moving == "green":
            baz_normal = [(2 * self.SQUARESIZE, -2 * self.SQUARESIZE), (-2 * self.SQUARESIZE, -2 * self.SQUARESIZE)]
        baz = baz_normal
        for piece in self.pieces[self.moving]:
            if self.c.itemcget(piece, "outline") == "gold2":
                baz = [(2 * self.SQUARESIZE, 2 * self.SQUARESIZE), \
                       (-2 * self.SQUARESIZE, 2 * self.SQUARESIZE),
                       (2 * self.SQUARESIZE, -2 * self.SQUARESIZE), \
                       (-2 * self.SQUARESIZE, -2 * self.SQUARESIZE)]
            else:
                baz = baz_normal
            for vtr in baz:
                bar = self.c.coords(piece)
                sqr_cords = (bar[0] - self.piece_offset + vtr[0], \
                             bar[1] - self.piece_offset + vtr[1], \
                             bar[2] + self.piece_offset + vtr[0], \
                             bar[3] + self.piece_offset + vtr[1])
                if self.jumpable(vtr, sqr_cords):
                    if len(self.c.find_overlapping(sqr_cords[0] + 5, sqr_cords[1] + 5, \
                                                   sqr_cords[2] - 5, sqr_cords[3] - 5)) == 1:
                        self.jumps[0].append((piece, vtr))
                        self.jumps[1].append(self.quux)
                self.quux = None
        if self.DEBUG_BIG_THINGS:
            print "self.jumps: ", self.jumps

    def jumpable(self, vtr, sqr_coords):
        """This function will determine, based on self.piece & self.square,
        if a move is a legal jump."""

        if self.DEBUG_PRINT_FUNCTIONS:
            pass  # ; print "jumpable"

        if abs(vtr[0]) != self.SQUARESIZE * 2 or abs(vtr[1]) != self.SQUARESIZE * 2:
            return 0  # if the move is not two squares, diagonaly, then fail

        barX = -self.SQUARESIZE * (vtr[0] / abs(vtr[0]))  # the X direction of the jump
        barY = -self.SQUARESIZE * (vtr[1] / abs(vtr[1]))  # the Y direction of the jump
        try:
            self.quux = self.c.find_enclosed(sqr_coords[0] + barX, sqr_coords[1] + barY, \
                                             sqr_coords[2] + barX, sqr_coords[3] + barY)[0]
        except IndexError:
            return 0  # if there is no piece to be jumped, somehow, then fail

        # This is a debuging test that generates too much data, so I comented it out.
        # if self.DEBUG:
        #     print sqr_coords[0]+barX, sqr_coords[1]+barY, \
        #         sqr_coords[2]+barX, sqr_coords[3]+barY
        #     self.c.create_rectangle(sqr_coords[0]+barX, sqr_coords[1]+barY, \
        #         sqr_coords[2]+barX, sqr_coords[3]+barY, width=3, outline="purple", tag="temporary")

        foo = self.pieces.keys()  # ugly hack to get the other color's pieces
        foo.remove(self.moving)

        if self.pieces[foo[0]].count(self.quux) == 1:
            if self.DEBUG:  # if the piece to be jumped is the opponents piece,
                print "yes!"  # then succeed
            return 1
        return 0

    def end(self, unused=None):
        """This function simply sets the self.end_now variable so the loop in MoveLoop will break."""
        self.end_now = 1

    def make_checker_squares(self, start, stop, color, tags=""):
        """This function will create a checkerboard of squares, of the color given, with the tags given.
        The start and stop arguments are a technical way of specifiying which half of the checkerboard is
        to be created.
            The variables requiblue by this function are:
                self.c(a Canvas), self.SQUARESIZE, """
        ##        if self.DEBUG_BIG_THINGS:
        ##            print color
        for y in range(0, 8):
            for x in range(start, stop, 2):
                self.c.create_rectangle(x * self.SQUARESIZE, \
                                        y * self.SQUARESIZE, \
                                        (x + 1) * self.SQUARESIZE, \
                                        (y + 1) * self.SQUARESIZE, \
                                        fill=color, tag=tags)
            if start == 0:
                start = 1;
                stop = 8
            else:
                if start == 1:
                    start = 0;
                    stop = 7
                else:
                    raise Exception, "Incorrect value for start in make_checker_squares"

    def make_pieces(self, color, delay):
        """This function will make, and place in standard starting position, all the pieces for a specified
        color.  The color can be either "green" or "blue".  If it is 0, they are placed on the top half of the board, if it is 1, on the bottom.
            The pieces are appended to the list variable corosponding to the color given, and they are given
            the tag "pieces".  The delay argument sets a delay(duh!), the unit
            is about 885 per sec.
            The variables requiblue by this function are:
                self.pieces(a dictionary of two lists, one for each side), self.c(a Canvas),
                self.SQUARESIZE, self.piece_offset"""

        side = self.pieces[color]
        if color == "blue":
            start = 1;
            stop = 8
            start2 = 0;
            stop2 = 3
        else:
            start = 0;
            stop = 7
            start2 = 5;
            stop2 = 8
        for y in range(start2, stop2):
            for x in range(start, stop, 2):
                for unused in range(delay):
                    self.master.update()
                side.append(self.c.create_oval(x * self.SQUARESIZE + self.piece_offset, \
                                               y * self.SQUARESIZE + self.piece_offset, \
                                               (x + 1) * self.SQUARESIZE - self.piece_offset, \
                                               (y + 1) * self.SQUARESIZE - self.piece_offset, \
                                               fill=color, tag="pieces"))

            if start == 0:
                start = 1;
                stop = 8
            else:
                if start == 1:
                    start = 0;
                    stop = 7
                else:
                    raise Exception, "Incorrect value for start in make_pieces"

    def make_a_piece(self, event):
        if event.num == 1:
            color = 'green'
        else:
            color = 'blue'
        if len(self.c.find_overlapping(event.x, event.y, event.x, event.y)) == 1:
            cords = self.c.coords(self.c.find_overlapping(event.x, event.y, event.x, event.y))
            self.pieces[color].append(self.c.create_oval(cords[0] + self.piece_offset, \
                                                         cords[1] + self.piece_offset, \
                                                         cords[2] - self.piece_offset, \
                                                         cords[3] - self.piece_offset, \
                                                         fill=color, tag='pieces'))

    def find_center(self, x0, y0, x1, y1):
        """This will find the center of a box given by x0, y0 and x1, y1."""
        if self.DEBUG_PRINT_FUNCTIONS:
            pass;
            print "find_center"
        return ((x1 - x0) / 2 + x0, (y1 - y0) / 2 + y0)

    def show_message(self, message, seconds=0.8, color="gray25"):
        """This function sets the message widget to the value of message and
        the fg to color.  It's main use is to show a message for a time, then
        replace it with the previous message"""
        self.oldmessage_info[0] = self.message.cget("text")
        self.oldmessage_info[1] = self.message.cget("foreground")
        self.message.config(text=message, fg=color)
        self.master.after(int(seconds * 1000), self.restore_message)

    def restore_message(self, unused=None):
        """This function sets the message widget to the value of
        self.oldmessage_info[0] and the fg to self.oldmessage_info[1].
        It's main use is to show a message for a time, then replace it with the
        previous message"""
        if self.DEBUG_PRINT_FUNCTIONS:
            pass;
            print "restore_message"
        self.message.config(text=self.oldmessage_info[0])
        self.message.config(fg=self.oldmessage_info[1])

    def erace_temporary(self, unused=None):
        """THis removes any objects on the canvas with the temporary tag"""
        if self.DEBUG_PRINT_FUNCTIONS:
            print "erace_temporary"
        self.c.delete("temporary")

    def remove_piece(self, event=None):
        """This is a function which will remove the piece which is
        clicked on."""
        piece = self.c.find_overlapping(event.x, event.y, event.x, event.y)
        print "piece: ", piece
        if len(piece) == 2 and self.c.type(piece[1]) == "oval":
            piece = piece[1]
            self.c.delete(piece)
            try:
                self.pieces["blue"].remove(piece)
            except:
                self.pieces["green"].remove(piece)
        else:
            if self.DEBUG:
                print "Not a piece!"

    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""

        while self.queue.qsize():
            try:
                # print "Accept move: ", ACCEPT_MOVE
                square_from, piece, square_to = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                self.set_piece(square_from, piece)
                self.set_square(square_to)

                if not self.GameDone():
                    if self.end_now:
                        break
                    self.master.update()
                    if self.got_move:
                        self.set_accept_move(0)
                        if not self.check_move():
                            self.set_accept_move(1)

                            # whenever a move is gotten which is correct, do this stuff
                            self.do_move()
                            self.cleanup_move(2)
                            self.setup_move()
                            self.cleanup_move(3)
                        # whenever a move is goten, do this stuff
                        self.cleanup_move(1)
                    self.set_check_complete(1)
                if self.GameDone() == 2:
                    self.c.create_text(int(self.c.cget("height")) / 2, \
                                       int(self.c.cget("width")) / 2, \
                                       text="green Won!!!", fill="red", \
                                       font=("", "20", ""), tag="win_text")
                if self.GameDone() == 1:
                    self.c.create_text(int(self.c.cget("height")) / 2, \
                                       int(self.c.cget("width")) / 2, \
                                       text="blue Won!!!", fill="red", \
                                       font=("", "23", ""), tag="win_text")
                    self.c.create_text(int(self.c.cget("height")) / 2, \
                                       int(self.c.cget("width")) / 2, \
                                       text="blue Won!!!", fill="red", \
                                       font=("", "20", ""), tag="win_text")
                    # import time
                    # start=time.time()
                    # while start-time.time() < 3:
                    #    self.master.update()

                # if self.AnotherGame():
                #     self.begin_new_game()
                # else:
                #     self.master.destroy()

                print square_to

            except Queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        self.main_checkers_table = [[33, 77], [34, 78], [35, 79], [36, 80],
                                    [37, 81], [38, 82], [39, 83], [40, 84],
                                    [41, 85], [42, 86], [43, 87], [44, 88],
                                    [45, 0], [46, 0], [47, 0], [48, 0],
                                    [49, 0], [50, 0], [51, 0], [52, 0],
                                    [53, 65], [54, 66], [55, 67], [56, 68],
                                    [57, 69], [58, 70], [59, 71], [60, 72],
                                    [61, 73], [62, 74], [63, 75], [64, 76]]

        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    map_curr = []
    map_new = []

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.


    Sampler.debug = 0
    output = np.array([[]])
    cap = cv2.VideoCapture(0)

    def insert_value(self, ndarray, value_x, value_y):
        result = ndarray
        result.resize((64,2))
        acumulator = result[6]
        for x in range(1,(result.size/2)-7):
            if(x % 8 == 0):
                for y in range((result.size/2)-1,x-1,-1):
                    result[y] = result[y-1]
                result[(x-1)] = result[(x-1)-1] + value_x
                x += 1
        for x in range(56,64):
            result[x] = result[x-8] + value_y
        return result

    def first_state_matrix(self):
        matrix = []
        for i in range(1, 33):
            matrix.append([i, i])
        return matrix

    def get_image_state(self, img):
        #img = cv2.imread(img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # blue
        lower_blue = np.array([92, 0, 0])
        upper_blue = np.array([124, 256, 256])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        output = np.array([[]])
        ret = False
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 7), output)
        # If found, add object points, image points (after refining them)
        if ret == True:
            # calculate lenght between two adjecent points
            x_substract = corners[01, [0]] - corners[00, [0]]
            y_substract = corners[07, [0]] - corners[00, [0]]

            result = np.copy(corners)
            result.resize((64, 2))

            self.insert_value(result, x_substract, y_substract)
            result.resize((64, 1, 2))
            # cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            # Przesuniecie punktow na srodek pol
            result = np.subtract(result, x_substract / 2)
            result = np.subtract(result, y_substract / 2)

            # **************************************************
            result = Math.alter_chessboard_middles(img, result)
            # ***************************************************

            self.imgpoints.append(result)
            img = cv2.multiply(img, np.array([1.1]))
            img = cv2.medianBlur(img, 7) #to change orientation if necessary
            str_state_table = Sampler.check_colors(img, result)
            return str_state_table

    def check_move(self, path1, path2, map_current, map_new):
        state1 = self.get_image_state(path1)
        state2 = self.get_image_state(path2)

        difference = []
        null_tile = None
        active_tile = None
        for i in range(0, len(state1)):
            for j in range(0, len(state1[0])):
                if state1[i][j] != state2[i][j]:
                    difference.append([i, j, state1[i][j], state2[i][j]])

        try:
            k = None
            if len(difference) > 2:                                                                                             #if difference is more than 2 then the change is not valid
                print("State change not possible, number of tiles that do not match: " + len(null_tile))
            elif len(difference) == 2:
                if difference[0][3] == 'white':
                    null_tile = difference[0]
                    active_tile = difference[1]
                    k = -1
                else:
                    null_tile = difference[1]
                    active_tile = difference[0]
                    k = 1
            elif len(difference) == 0:
                return
        except Exception as e:
            print('Inaccesible state! Return to the last acceptable')
            return

        map_new[null_tile[0] * 4 + null_tile[1]][1] = 0
        print("zmieniam", map_new[active_tile[0] * 4 + null_tile[1]][0], 'z', map_new[active_tile[0] * 4 + null_tile[1]][1], 'na ',map_current[null_tile[0] * 4 + null_tile[1] + k][1])
        map_new[active_tile[0] * 4 + null_tile[1]][1] = map_current[null_tile[0] * 4 + null_tile[1] + k][1]
        map_current = copy.deepcopy(map_new)            #ONLY if test in logic will prove that it was valid move
        return[map_current, map_new]

            # temp = map_current[null_tile[0] * 4 + null_tile[1] + 1][1]
            # map_new[active_tile[0] * 4 + active_tile[1] + 1] = temp
            # map_new[null_tile[0] * 4 + null_tile[1] + 1] =

            # get_nth_element_of_map(null_tile * 4 + null_tile[1] + 1, map_current)[1] = temp
            # get_nth_element_of_map(difference[1][0] * 4 + difference[1][1] + 1, map_current)[1] =

    def starting_map(self):
        array = []
        for i in range(33, 45):
            array.append([i, i + 44])
        for i in range(45, 53):
            array.append([i, 0])
        for i in range(53, 65):
            array.append([i, i + 12])
        return array

    def get_nth_element_of_map(i, array):
        return array[i + 32][1]

    def checkTables(self, new_table):
        count = 0
        squares_from = []
        squares_to = []
        square_from = 0
        square_to = 0
        piece = 0
        piece_remove = []
        for old_square, new_square in zip(self.main_checkers_table, new_table):
            if old_square[1] <> new_square[1]:
                if new_square[1] == 0:
                    piece_remove.append(old_square[1])
                    squares_from.append([old_square[0], old_square[1]])
                if old_square[1] == 0:
                    squares_to.append([new_square[0], new_square[1]])
                count += 1

        if count > 1 and count < 4:
            if count == 2:
                for move in squares_from:
                    if move[1] == squares_to[0][1]:
                        square_from = move[0]
                        square_to = squares_to[0][0]
                        piece = move[1]
                        piece_remove.remove(piece)
            if count == 3:
                for move in squares_from:
                    if move[1] == squares_to[0][1]:
                        square_from = move[0]
                        square_to = squares_to[0][0]
                        piece = move[1]
                        piece_remove.remove(piece)

            move = (square_from, piece, (square_to,))
            print count, move, piece_remove

            self.queue.put(move)

            while self.gui.get_check_complete() == 0:
                print 'wait for complete'
                time.sleep(0.5)
            if self.gui.get_accept_move():
                print 'Accept move is 1'
                self.main_checkers_table = new_table
                self.gui.set_accept_move(0)
            else:
                self.gui.show_message('Get back to this state', 1)

            self.gui.set_check_complete(0)
        else:
            if count != 0:
                self.gui.show_message('Get back to this state', 1)
            else:
                pass

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """

        self.counter = 0

        # pierwszy odczyt z kamery
        ret, img = self.cap.read()
        # zapisanie pierwszego odczytu z kamery do obrazu
        # ustawienie poczatkowe reprezentacji planszy
        if ret:
            normal = cv2.cvtColor(img, cv2.COLORMAP_BONE)
            map_curr = self.starting_map()
            map_new = self.starting_map()
            cv2.imwrite('old.jpg', normal)
            path1 = cv2.imread('old.jpg')
            path2 = cv2.imread('old.jpg')

        while self.running:
            #cv2.waitKey(4000)
            ret, img = self.cap.read()

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            # mask = cv2.inRange(hsv, lower_blue, upper_blue)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (7,7), self.output)
                # If found, add object points, image points (after refining them)
            if ret == True:

                cv2.waitKey(1000)
                normal = cv2.cvtColor(img, cv2.COLORMAP_BONE)
                #scipy.misc.imsave('new.jpg', normal)
                cv2.imwrite('new.jpg',normal)
                #path2 = scipy.misc.imread('new.jpg')
                path2 = cv2.imread('new.jpg')
                maps = self.check_move(path1, path2, map_curr, map_new)                              #Dziwne przypisanie bo nie zwojowalem wewnatrz funkcji zmiany zawartosci listy podanej jako parametr
                #path2 = scipy.misc.imread('new.jpg')
                if maps is not None:
                    map_curr = maps[0]
                    map_new = maps[1]
                #print(map_curr)
                self.checkTables(map_curr)
                cv2.waitKey(delay=100)



    def endApplication(self):
        self.running = 0
        self.cap.relase()
        cv2.destroyAllWindows()
root = Tk()

client = ThreadedClient(root)
root.mainloop()
