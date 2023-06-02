import copy
import random
import sys
import pygame
import numpy as np

from constants import *
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

icon = pygame.image.load("game (1).png")
pygame.display.set_icon(icon)
screen.fill(Bg_color)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.Empty_square = self.squares # list of empty squares
        self.marked_square = 0
        # 1st Test to check the zeros in the board
        # print(self.squares)

        # 2nd Test to check a player in the board if it will update or not
        """
        self.mark_square(1, 1, 2)
        print(self.squares)
        """
    # we know we have two players in the game the usage of this function is when a player
    # Marks a square it becomes no more zero

    def final_state(self, display=False):
        """

        i created this function to return zero if there is a draw (no win )
        return one if player one wins
        return 2 if player 2 wins
        """
        # Checking the vertical wins on the board
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if display:
                    color = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    initial_pos =(col * SQUIZE + SQUIZE // 2, 20)
                    final_pos = (col * SQUIZE + SQUIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, initial_pos, final_pos, Line_width)
                return self.squares[0][col] # any one from the condition above because each one have the same value

        # Checking the horizontal win on the board
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if display:
                    color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    initial_pos =(20, row * SQUIZE + SQUIZE // 2)
                    final_pos = (WIDTH - 20,  row * SQUIZE + SQUIZE // 2)
                    pygame.draw.line(screen, color, initial_pos, final_pos, Line_width)
                return self.squares[row][1]

        # Desc diagonal line for the win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if display:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                initial_pos = (20, 20)
                final_pos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, initial_pos, final_pos, CROSS_WIDTH)
            return self.squares[1][1]

        # Asc diagonal line for the win
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if display:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                initial_pos = (20, HEIGHT - 20)
                final_pos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, initial_pos, final_pos, CROSS_WIDTH)
            return self.squares[1][1]

        # no win yet
        return 0


    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_square += 1



    def Is_full(self):
        return  self.marked_square == 9

    def Is_empty(self):
        return self.marked_square == 0

    def empty_square(self, row, col):
        return self.squares[row][col] == 0

    # return a list of empty squares
    def get_empty_square(self):
        empty_sqr = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row, col):
                    empty_sqr.append((row, col))

        return empty_sqr

class AI:
    # level 0 represent the random AI
    # level 1 represent the min_max algorithm
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def random_choice(self, board):
        # here we get the empty squares from the board to an variable
        empty_squares = board.get_empty_square()
        # here we will make a random choice from the the random selection of the squares
        index = random.randrange(0, len(empty_squares))
        return empty_squares[index] # returning row and col

    def mini_max(self, board, maximizing):
        # first we will code the terminal state
        case = board.final_state()
        # we need to return a tuple of the evaluation and the move
        # Player 1 wins the game
        if case == 1:
            return 1, None
        # Player 2 wins the game
        elif case == 2:
            return -1, None # player 2 is the ai and it will minimize
        # Draw
        elif board.Is_full():
            return 0, None
        if maximizing:
            maximum_evaluate = -100
            best_move = None
            empty_squares = board.get_empty_square()

            # this will be the move
            for (row, col) in empty_squares:
                # we don't need to affect our board in testing
                temp_board = copy.deepcopy(board)
                # mark in the copied one
                temp_board.mark_square(row, col, 1)
                # as we will return a tuple with the evaluation and the move we need evaluation here with index [0]
                evaluation = self.mini_max(temp_board, False)[0]

                if evaluation > maximum_evaluate:
                    maximum_evaluate = evaluation
                    best_move = (row, col)
            return maximum_evaluate, best_move

        elif not maximizing:
            minimum_evaluate = 100
            best_move = None
            empty_squares = board.get_empty_square()

            # this will be the move
            for (row, col) in empty_squares:
                # we don't need to affect our board in testing
                temp_board = copy.deepcopy(board)
                # mark in the copied one
                temp_board.mark_square(row, col, self.player)
                # as we will return a tuple with the evaluation and the move we need evaluation here with index [0]
                evaluation = self.mini_max(temp_board, True)[0]

                if evaluation < minimum_evaluate:
                    minimum_evaluate = evaluation
                    best_move = (row, col)
            return minimum_evaluate, best_move


    def evaluate(self, main_board):
        if self.level == 0:
            # random choice
            evaluation = 'random'
            move = self.random_choice(main_board)


        else:
            # min_max algorithm will terminate here the usage of it
            # the ai is the one who will minimize
            evaluation, move = self.mini_max(main_board, False)
        print(f" the AI choose to mark the square in position {move} with an evaluation of:  {evaluation} ")
        return move # is a row and col



class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # 1st is the cross  # 2nd is the circle
        self.gamemode ='ai'
        self.running = True # this attribute for when the ai was Playing it crashed when there isn't a place to play
        self.show_lines()

    # in order to make a clean code i made this method to call it each time i want to write this 3 lines inside it
    # instead of each time i write three lines
    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.Next_turn()


    def show_lines(self):
        # fixing the bug that shown when i restart the game we must fill with the background with the color
        screen.fill(Bg_color)


        # showing here the vertical lines
        pygame.draw.line(screen, Line_color, (SQUIZE, 0), (SQUIZE, HEIGHT), Line_width)
        pygame.draw.line(screen, Line_color, (WIDTH - SQUIZE, 0), (WIDTH - SQUIZE, HEIGHT), Line_width)
        # showing here the horizontal lines
        pygame.draw.line(screen, Line_color, (0, SQUIZE), (WIDTH, SQUIZE), Line_width)
        pygame.draw.line(screen, Line_color, (0, HEIGHT-SQUIZE), (WIDTH, HEIGHT - SQUIZE), Line_width)

    def Next_turn(self):
        # Here we will change to
        self.player = self.player % 2 + 1

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (col * SQUIZE + OFFSET, row * SQUIZE + OFFSET)
            end_desc = (col * SQUIZE + SQUIZE - OFFSET, row * SQUIZE + SQUIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # asc line
            start_Asc = (col * SQUIZE + OFFSET, row * SQUIZE + SQUIZE - OFFSET)
            end_Asc = (col * SQUIZE + SQUIZE - OFFSET, row * SQUIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_Asc, end_Asc, CROSS_WIDTH)



        elif self.player == 2:
            # draw circle
            CENTER = (col * SQUIZE + SQUIZE // 2, row * SQUIZE + SQUIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, CENTER, RADIUS, CIRCLE_WIDTH)

    # This function to change the mode of the game from pvp (Player vs Player) to AI ;)
    def change_mode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def reset(self):
        self.__init__()

    def is_over(self):
        # here checking if we reach the final state or the board is already full
        # by making display = True it will draw the win
        return self.board.final_state(display=True) != 0 or self.board.Is_full()



def main():

    # creating the object each time we start the game to use the methods of it
    game = Game()
    board = game.board
    ai = game.ai
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Getting the position on screen while clicking on the board in any pos like(164, 292)
                # Test
                # print(event.pos)

                # Making the pos in the the board like (0, 0) , (1, 1)
                pos = event.pos
                row = pos[1] // SQUIZE
                col = pos[0] // SQUIZE
                # Test if the we make it to the board or not and we make it ;)
                # print(row, col)

                # board.mark_square(row, col, 1)
                # Test
                #  print(board.squares)

                # Here we check if the square is empty or not if empty we will make a mark 1 in the matrix
                # if it's not empty we will not mark it again
                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)
                    """board.mark_square(row, col, game.player)
                    game.draw_fig(row, col)
                    game.Next_turn()
                    # Test
                    # print(board.squares)
                    """
                    # checking if we are in the end game this for human play
                    if game.is_over():
                        game.running = False
            if event.type == pygame.KEYDOWN:
                # changing the game mode from an ai to a pvp (player vs player) or random
                if event.key == pygame.K_g:
                    game.change_mode()

                # Getting every thing in its right position
                if event.key == pygame.K_r:
                    game.reset()
                    # this two line of code because we want a new board from the beginning
                    board = game.board
                    ai = game.ai

                # randome  ai -> 0
                if event.key == pygame.K_0:
                    ai.level = 0


                # randome ai -> 1
                if event.key == pygame.K_1:
                    ai.level = 1
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # we need here to update the screen
            pygame.display.update()
            # the method of AI HERE
            # as we can see here we will make the board visualised with the moves as me made with the human
            # the same function
            row, col = ai.evaluate(board)
            game.make_move(row, col)
            """board.mark_square(row, col, ai.player)
            game.draw_fig(row, col)
            game.Next_turn()
            """

            # here checking if we in the end game with respect for ai
            if game.is_over():
                game.running = False



        pygame.display.update()


main()
