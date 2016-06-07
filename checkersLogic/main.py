from checkersLib.checkers import CheckersInterface

CI = CheckersInterface()
# CI.set_piece(42, 86)
# CI.set_square(47)
CI.start()
print 'Now we can continue running code while mainloop runs!'
CI.set_piece(42, 86)
CI.set_square(47)