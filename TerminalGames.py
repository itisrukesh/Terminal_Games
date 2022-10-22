import random
import os
import math
import re
import string
import time
import mysql.connector
import turtle
import winsound
from pprint import pprint

over_all_score = 0

# MINESWEEPER GAME CODE:


class Board:

    def __init__(self, dim_size, num_bombs):
        # let's keep track of these parameters, they will be useful later
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # lets create the board
        # helper function
        self.board = self.make_new_board()  # plant the bombs
        self.assign_values_to_board()

        # initialize a set to keep track of which locations we have uncovered
        # we'll save (row,col) tuples into this set
        self.dug = set()  # if we dig at 0,0 then self.dug={(0,0)}

    def make_new_board(self):
        # construct a new board based on the dim size and num bombs
        # we should construct the list of lists here (or whatever representation you prefer,
        # but since we have a 2-D board, list of lists is most natural)

        # generate a new board
        board = [[None for _ in range(self.dim_size)]
                 for _ in range(self.dim_size)]
        # this creates an array like this:
        # [[None, None, ..., None], [None, None, ..., None], ..., [None, None, ..., None]]
        # we can see how this represnts a board

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2-1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                # this means we've actually planted a bomb there already so keep going
                continue
            board[row][col] = '*'  # palnt the bomb
            bombs_planted += 1
        return board

    def assign_values_to_board(self):
        # now that we have planted the bombs, let's assign a number 0-8 for all the empty spaces, which represents
        # how many neighboring bombs there are. we can precompute these and it'll save us some effort checking what's
        # around the board later on :
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if this is alrady a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # let's iterate through each of the neighboring positions and sum number of bombs
        # top left (row-1, col-1)
        # top middle (row-1, col)
        # top right (row-1, col+1)
        # left (row, col-1)
        # right (row, col+1)
        # bottom left (row+1, col-1)
        # bottom middle (row+1, col)
        # bottom right (row+1, col+1)

        # make sure to not go out of bounds!

        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at that location
        # return true if successfull dig, false if bomb dug

        # a few scenarios:
        # hit a bomb -> game over
        # dig at location with neighboring bombs -> finish dig
        # dig at location with no neighboring bombs -> recursively dig neighbors!

        self.dug.add((row, col))  # keep track that we dug here

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue  # don't dig where you have already dig
                self.dig(r, c)

        # if our initial dig didn't hit a bomb, we should'nt hit a bomb here
        return True

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first lets create a new array represents what the user would see
        visible_board = [[None for _ in range(
            self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = '  '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing

        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key=len)))

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '  # leaves space for '0' in horizantal heading
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '   '.join(cells)
        indices_row += ' \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' | '.join(cells)
            string_rep += ' | \n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def MinesWeeper(dim_size=10, num_bombs=10, score=0):
    # step 1: create the board and plant the bombs
    global over_all_score
    board = Board(dim_size, num_bombs)
    # step 2: show the user the board and ask for where they want to dig
    # step 3a: if location is a bomb, show game over message
    # step 3b: if location is not a bomb, dig recursively until each square is at least next to a bomb
    # step 4: repeat step 2 and 3a/b until there are no more places to dig -> VICTORY

    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print('')
        print(board)
        print('Over All Score : ', over_all_score)
        user_input = re.split(
            ',(\\s)*', input("Where would you like to dig? \nEnter the position as row, col :"))  # 0,0 or 0, 0
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location, try again")
            continue
        # if it is valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb ahhhhhhhhhh
            break  # game over rip
        else:
            over_all_score += 5
    # 2 ways to end loop, lets check which one
    if safe:
        print("Your over all score is : ", over_all_score)
        print("Congratulation you won the game")
    else:
        over_all_score += score
        print("Your over all score is : ", over_all_score)
        print("Sorry game over")
        # lets reveal the whole board
        board.dug = [(r, c) for r in range(board.dim_size)
                     for c in range(board.dim_size)]
        print(board)

# MINESWEEPER CODE ENDS HERE.

# HANGMAN CODE:


def hangman():
    global over_all_score
    word_no = random.randint(1, 8)  # randomly chooses no of the list

    if word_no == 1:
        print("You need to guess a word under \'VEGETABLES\' category......\n")

        vegetables = ['CARROT', 'BROCCOLI', 'CAULIFLOWER', 'CORN', 'CUCUMBER', 'EGGPLANT', 'GREENPEPPER',
                      'LETTUCE', 'MUSHROOMS', 'ONION', 'POTATO', 'PUMPKIN', 'REDPEPPER', 'TOMATO', 'BEETROOT', 'PEAS',
                      'RADISH', 'CABBAGE', 'CHILI', 'GARLIC', 'SWEETPOTATO', 'CORIANDER', 'TAMARIND']
        word = random.choice(vegetables)

    if word_no == 2:
        print("You need to guess a word under \'VEHICLES\' category......\n")

        vehicles = ['HELICOPTER', 'AIRPLANE', 'ROCKET', 'SAILBOAT', 'CRUISESHIP', 'CARGOSHIP', 'JETSKI',
                    'SHIP', 'BOAT', 'SUBMARINE', 'BICYCLE', 'CAR', 'BUS', 'TRAIN', 'TRUCK', 'VAN',
                    'MOTORCYCLE', 'Taxi', 'Policecar', 'Ambulance', 'Skateboard', 'Mountainbike', 'Scooter', 'Fireengine',
                    'Crane', 'Forklift', 'Tractor', 'Cementmixer', 'Dumptruck', 'Gasballoon', 'Tram', 'Carriage']
        word = random.choice(vehicles)

    if word_no == 3:
        print("You need to guess a word under \'ANIMALS\' category......\n")

        Animals = ['Hummingbird', 'BIRD', 'DOG', 'DONKEY', 'GIRAFFE', 'ALLIGATOR', 'CAT', 'HORSE', 'LION', 'MONKEY', 'BEE', 'DUCK',
                   'FROG', 'ELEPHANT', 'CROCODILE', 'DOLPHIN', 'GORILLA', 'MOUSE', 'TIGER', 'RABBIT', 'RAT']

        word = random.choice(Animals)

    if word_no == 4:
        print("You need to guess a word under \'HUMANORGANS\' category......\n")

        Bodyparts = ['Head', 'Face', 'Hair', 'Ear', 'Neck', 'Forehead', 'Beard', 'Eye', 'Nose', 'Mouth', 'Chin', 'Shoulder', 'Elbow',
                     'Arm', 'Chest', 'Armpit', 'Forearm', 'Wrist', 'Back', 'Navel', 'Toes', 'Ankle', 'Instep', 'Toenail', 'Waist', 'Abdomen',
                     'Buttock', 'Hip', 'Leg', 'Thigh', 'Knee', 'Foot', 'Hand', 'Thumb']
        word = random.choice(Bodyparts)

    if word_no == 5:
        print("You need to guess a word under \'COLOURS\' category......\n")

        Colours = ['RED', 'YELLOW', 'BLUE', 'GREEN', 'ORANGE', 'PURPLE', 'LIME', 'BROWN', 'NAVY', 'PINK', 'GOLD',
                   'SILVER', 'BLACK', 'WHITE', 'INDIGO', 'TURKISHBLUE', 'VIOLET', 'SAFRON', 'ROSE', 'MAGENTA', 'MAROON']
        word = random.choice(Colours)

    if word_no == 6:
        print("You need to guess a word under \'FRUITS\' category......\n")

        fruits = ['APPLE', 'GUAVA', 'PEACH', 'PEAR', 'MANGO', 'PAPAYA', 'ORANGE', 'GRAPES', 'KIWI', 'CHERRY',
                  'WATERMELON', 'PINEAPPLE', 'BLUEBERRY', 'BANANA', 'COCONUT', 'CUSTARDAPPLE', 'LEMON', 'MULBERRY']
        word = random.choice(fruits)

    if word_no == 7:
        print("You need to guess a word under \'SHAPES\' category......\n")

        shapes = ['CIRCLE', 'DIAMOND', 'HEART', 'OCTAGON', 'SQUARE', 'STAR', 'TRIANGLE'
                  'Nonagon', 'Octagon', 'Heptagon', 'Hexagon', 'Scalenetriangle', 'Righttriangle', 'Parallelogram', 'Rhombus',
                  'Pentagon', 'Oval', 'Heart', 'Cross', 'Arrow', 'Cube', 'Cylinder', 'Crescent']
        word = random.choice(shapes)

    if word_no == 8:
        print("You need to guess a word under \'INSECTS\' category......\n")

        insects = ['Armyants', 'Bumblebees', 'Cicadas', 'dragonflies', 'Earwigs', 'Fireflies', 'Grasshoppers', 'Jewelbeetles', 'Katydids',
                   'Lacewings', 'Mosquitoes', 'Netwings', 'flies', 'Paperwasps', 'Queentermites', 'Robberflies', 'Spiderwasps', 'beetles',
                   'moths', 'butterflies', 'Weevils', 'bees', 'Yuccamoths']
        word = random.choice(insects)

    length = len(word)
    print(f"Its {length} letter word make a guess!\n")
    final_word = word.upper()

    lives_visual_dict = {
        0: """
            ___________
            | /        | 
            |/        ( )
            |          |
            |         / \\
            |
        """,
        1: """
            ___________
            | /        | 
            |/        ( )
            |          |
            |         / 
            |
        """,
        2: """
            ___________
            | /        | 
            |/        ( )
            |          |
            |          
            |
        """,
        3: """
            ___________
            | /        | 
            |/        ( )
            |          
            |          
            |
        """,
        4: """
            ___________
            | /        | 
            |/        
            |          
            |          
            |
        """,
        5: """
            ___________
            | /        
            |/        
            |          
            |          
            |
        """,
        6: """
            |
            |
            |
            |
            |
        """,
        7: "", }

    word = final_word
    word_letters = set(word)  # letters in the word
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # what the user has guessed
    lives = 7

    # getting user input
    while len(word_letters) > 0 and lives > 0:
        # letters used
        # ' '.join(['a', 'b', 'cd']) --> 'a b cd'
        print('You have', lives, 'lives left and you have used these letters: ',
              ' '.join(used_letters))

        # what current word is (ie W - R D)
        word_list = [
            letter if letter in used_letters else '-' for letter in word]
        print(lives_visual_dict[lives])
        print('Current word: ', ' '.join(word_list))

        user_letter = input('Guess a letter: ').upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                print('')

            else:
                lives = lives - 1  # takes away a life if wrong
                print('\nYour letter,', user_letter, 'is not in the word.')

        elif user_letter in used_letters:
            print('\nYou have already used that letter. Guess another letter.')

        else:
            print('\nThat is not a valid letter.')

    # gets here when len(word_letters) == 0 OR when lives == 0
    if lives == 0:
        print(lives_visual_dict[lives])
        print('You died, sorry. The word was', word)
        over_all_score += 0
        print('Your Score:', over_all_score)

    else:
        print('YAY! You guessed the word', word, '!!')
        over_all_score += 20
        print('Your Score:', over_all_score)

# END OF HANGMAN CODE.

# ROCKPAPERSCISSORS CODE:


def RockPaperScissor():
    global over_all_score
    player_score = 0
    comp_score = 0
    total_score = int(input('Enter total score to decide the winner : '))
    total_score *= 10
    while player_score < total_score and comp_score < total_score:
        player = input(
            "\n\t Choose any one : Rock(R), Paper(P), Scissor(S) : ")
        comp = random.choice(['R', 'P', 'S'])
        if player == comp:
            print('Tie!')
        elif player == "R" or player == "r":
            if comp == "P":
                comp_score += 10
                print(
                    '\t Computer choose Paper \n\t Paper covers the Rock Computer won the point ')
            else:
                player_score += 10
                print(
                    '\t Computer choose Scissor \n\t Rock smashes the scissor Player won the point ')
        elif player == "P" or player == "p":
            if comp == "S":
                comp_score += 10
                print(
                    '\t Computer choose Scissor \n\t Scissor cuts the paper computer won the point ')
            else:
                player_score += 10
                print(
                    '\t computer choose Rock \n\t Paper covers the rock player won the point')
        elif player == "S" or player == "s":
            if comp == "R":
                comp_score += 10
                print(
                    '\t Computer choose Rock \n\t Rock smashes the scissor computer won the point')
            else:
                player_score += 10
                print(
                    '\t Computer choose paper \n\t Scissor cuts the paper player won the point ')
        else:
            print('\t Check your spelling !!')
    if player_score == total_score:
        over_all_score += player_score
        print('\nComputer Score : ', comp_score, '\tPlayer Score : ',
              player_score, ' \tPlayer won the game')
    else:
        over_all_score += player_score
        print('\nComputer Score : ', comp_score, '\tPlayer Score : ',
              player_score, ' \tComputer won the game')

# END OF ROCKPAPERSCISSORS CODE.


# GUESSING NUMBER CODE:
def GuessingNumberByUser():
    global over_all_score
    victory = 0
    # Taking Inputs
    lower = int(input("Enter Lower bound:- "))

    # Taking Inputs
    upper = int(input("Enter Upper bound:- "))

    # generating random number between
    # the lower and upper
    x = random.randint(lower, upper)
    chances = round(math.log(upper - lower + 1, 2))
    print("\n\tNow you can guess any integer and You've only ", chances, " chances!")

    # Initializing the number of guesses.
    count = 0

    # for calculation of minimum number of
    # guesses depends upon range
    while count < chances:
        count += 1

        # taking guessing number as input
        guess = int(input("\n\tGuess a number:- "))

        # Condition testing
        if x == guess:
            victory = 1
            over_all_score += 10
            print("\n\tThe number is ", x, "! Congratulations you did it in ",
                  count, " try")
            # Once guessed, loop will break
            break
        elif x > guess:
            print("\tYou guessed too small!")
        elif x < guess:
            print("\tYou Guessed too high!")

    # If Guessing is more than required guesses,
    # shows this output.
    if victory == 0:
        print("\n You have exceeded the chances, The number is %d" % x)
        print("\tBetter Luck Next time!")

# END OF GUESSING NUMBER CODE.


'''def GuessingNumberByComputer():
    global over_all_score
    victory=0
    lower = int(input("Enter Lower bound:- "))
    upper = int(input("Enter Upper bound:- "))
    chances = round(math.log(upper - lower + 1, 2))
    print("\n\t Now the computer started to guess the integer with in ",chances," chances!\n")
    count = 0

    while count < chances:
        count += 1
        guessNumber=random.randint(lower,upper)
        clues=input(f'The guessing number is {guessNumber} if too high (H), if too low(L), if correct (C) : \n').lower()
        if clues=="h":
            upper=guessNumber-1
        elif clues=="l":
            lower=guessNumber+1
        elif clues=="c":
            victory=1
            
            print("\t The number is ",guessNumber,"! computer won the game in ",count," try")
            break
            
    if victory == 0:
        over_all_score += 50
        print("\t Computer loss and Player won the game!")
        print("Over All Score is: ",over_all_score)'''

# TicTacToe CODE:


class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-9): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val


class RandomComputer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class SmartComputer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = 'O' if player == 'X' else 'X'

        # first we want to check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            # each score should maximize
            best = {'position': None, 'score': -math.inf}
        else:
            # each score should minimize
            best = {'position': None, 'score': math.inf}
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            # simulate a game after making that move
            sim_score = self.minimax(state, other_player)

            # undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            # this represents the move optimal next move
            sim_score['position'] = possible_move

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best


class TicTacToe():

    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i*3:(i+1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2
        number_board = [[str(i) for i in range(j*3, (j+1)*3)]
                        for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check the row
        row_ind = math.floor(square / 3)
        row = self.board[row_ind*3:(row_ind+1)*3]
        # print('row', row)
        if all([s == letter for s in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        # print('col', column)
        if all([s == letter for s in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            # print('diag1', diagonal1)
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            # print('diag2', diagonal2)
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]


def play(game, x_player, o_player, print_game=True):

    global over_all_score
    if print_game:
        game.print_board_nums()

    letter = "X"
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        if game.make_move(square, letter):

            if print_game:
                print(letter + ' makes a move to square {}'.format(square))
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                    if user_choices == letter.lower():
                        over_all_score += 20
                        print("Your score:", over_all_score)
                    else:
                        over_all_score += 0
                        print("Your score:", over_all_score)

                return letter  # ends the loop and exits the game
            letter = 'O' if letter == 'X' else 'X'  # switches player

        time.sleep(.8)

    if print_game:
        print('It\'s a tie!')
        over_all_score += 0
        print("Your score:", over_all_score)

# END OF TicTacToe CODE.


# MAIN CODE STARTS HERE
os.system('cls')
user = input("Please enter your name:").upper()
print(f"Welcome {user}\n You're now in the terminal games")
clear = input("Click any alphabet keys to start playing......").lower()
if clear in 'abcdefghijklmnopqrstuvwxyz':
    os.system('cls')

# BLOCK OF GAMES STARTS HERE
willing = 'yes'
while willing == "yes" or willing == "y":

    os.system('cls')
    print('''
                                                                                                                                                                    
       888888888888                                         88                           88       ,ad8888ba,                                                          
            88                                              ""                           88      d8"'    `"8b                                                         
            88                                                                           88     d8'                                                                   
            88   ,adPPYba,  8b,dPPYba,  88,dPYba,,adPYba,   88  8b,dPPYba,   ,adPPYYba,  88     88             ,adPPYYba,  88,dPYba,,adPYba,    ,adPPYba,  ,adPPYba,  
            88  a8P_____88  88P'   "Y8  88P'   "88"    "8a  88  88P'   `"8a  ""     `Y8  88     88      88888  ""     `Y8  88P'   "88"    "8a  a8P_____88  I8[    ""  
            88  8PP"""""""  88          88      88      88  88  88       88  ,adPPPPP88  88     Y8,        88  ,adPPPPP88  88      88      88  8PP"""""""   `"Y8ba,   
            88  "8b,   ,aa  88          88      88      88  88  88       88  88,    ,88  88      Y8a.    .a88  88,    ,88  88      88      88  "8b,   ,aa  aa    ]8I  
            88   `"Ybbd8"'  88          88      88      88  88  88       88  `"8bbdP"Y8  88       `"Y88888P"   `"8bbdP"Y8  88      88      88   `"Ybbd8"'  `"YbbdP"'  
                                                                                                                                                                    
                                                                                                                                                                    
    ''')

    print('\t1. Rock Paper Scissor')
    print('\t2. Guessing Number')
    print('\t3. MinesWeeper')
    print('\t4. TicTacToe')
    print('\t5. Hangman\n')
    print(f'''Description:\n\tHii {user}, you're now in Terminal games.It's a platform which provides above mentioned arcade games for you to play...!\n
    Hope you enjoy it! ;-)''')

    ch = input('\nWhich game you want to play? "Enter the the game number": ')
    if ch == "1":
        os.system('cls')
        print('''
                                                      Yb        dP w                        8                        
                                                       Yb  db  dP  w 8d8b.    .d8b. 8d8b    8 .d8b. d88b .d88b       
                                                        YbdPYbdP   8 8P Y8    8' .8 8P      8 8' .8 `Yb. 8.dP'       
                                                         YP  YP    8 8   8    `Y8P' 8       8 `Y8P' Y88P `Y88P w w w 
                                                                                                                     
        ''')
        print('\nYou have Choosen the game "Rock Paper Scissor!!!"\n')
        print('''Description:\n\tIn this game you've to enter your choice, you've three options(Rock,Paper,Scissors).\nIf you beat the computer you will win. you'll earn a point or else point goes to computer. Here you have to decide the match point, so choose wisely... O_O\n\nTip:Dont rush to win... Be steady and think!\n''')
        RockPaperScissor()

    elif ch == "2":
        os.system('cls')
        print('''
                                                ███████ ██   ██  █████   ██████ ████████     ███    ███  █████  ████████  ██████ ██   ██ 
                                                ██       ██ ██  ██   ██ ██         ██        ████  ████ ██   ██    ██    ██      ██   ██ 
                                                █████     ███   ███████ ██         ██        ██ ████ ██ ███████    ██    ██      ███████ 
                                                ██       ██ ██  ██   ██ ██         ██        ██  ██  ██ ██   ██    ██    ██      ██   ██ 
                                                ███████ ██   ██ ██   ██  ██████    ██        ██      ██ ██   ██    ██     ██████ ██   ██ 
                                                                                                                                                                                                                                                                   
        ''')

        print('\nYou have Choosen the game "Guessing Number by the User!!!"\n')
        print('''Descripton:\n\tIn this game you've to enter the lower guess limit-(starting number) and you also have to enter the upper guess limit-(ending number).\nAfter that computer will randomly pick a number which lies between the mentioned range. Now you have to guess the number within several chances.\n\nNote: Your chances are given based on your entered limits."KNOCK IT OFF!!"\n''')
        GuessingNumberByUser()

    elif ch == "3":
        os.system('cls')
        print('''

                                              ███╗   ███╗██╗███╗   ██╗███████╗███████╗██╗    ██╗███████╗███████╗██████╗ ███████╗██████╗ ██╗
                                              ████╗ ████║██║████╗  ██║██╔════╝██╔════╝██║    ██║██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗██║
                                              ██╔████╔██║██║██╔██╗ ██║█████╗  ███████╗██║ █╗ ██║█████╗  █████╗  ██████╔╝█████╗  ██████╔╝██║
                                              ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ╚════██║██║███╗██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██╗╚═╝
                                              ██║ ╚═╝ ██║██║██║ ╚████║███████╗███████║╚███╔███╔╝███████╗███████╗██║     ███████╗██║  ██║██╗
                                              ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝
                                                                                                                                           
        ''')

        print('\nYou have Choosen the game "Minesweeper!!!"')
        print('''\nDescrpition:\n\tMinesweeper is single-player logic-based computer game played on rectangular board whose object is to locate a predetermined number of randomly-placed "mines" in\nthe shortest possible time by clicking on "safe" squares while avoiding the squares with mines. If the player clicks on a mine, the game ends.\nHere the dimension is 9X9 it contians 10-mines.\n\nTip:Start digging the corners first!!\n''')
        MinesWeeper()

    elif ch == "5":
        os.system('cls')
        print('''
                                         ▄█    █▄       ▄████████ ███▄▄▄▄      ▄██████▄    ▄▄▄▄███▄▄▄▄      ▄████████ ███▄▄▄▄   
                                        ███    ███     ███    ███ ███▀▀▀██▄   ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ███▀▀▀██▄ 
                                        ███    ███     ███    ███ ███   ███   ███    █▀  ███   ███   ███   ███    ███ ███   ███ 
                                       ▄███▄▄▄▄███▄▄   ███    ███ ███   ███  ▄███        ███   ███   ███   ███    ███ ███   ███ 
                                      ▀▀███▀▀▀▀███▀  ▀███████████ ███   ███ ▀▀███ ████▄  ███   ███   ███ ▀███████████ ███   ███ 
                                        ███    ███     ███    ███ ███   ███   ███    ███ ███   ███   ███   ███    ███ ███   ███ 
                                        ███    ███     ███    ███ ███   ███   ███    ███ ███   ███   ███   ███    ███ ███   ███ 
                                        ███    █▀      ███    █▀   ▀█   █▀    ████████▀   ▀█   ███   █▀    ███    █▀   ▀█   █▀  
                                                                                                                                
        ''')

        print('\nYou have Choosen the game "Hangman!!!"')
        print('''\nDescription:\n\tHangman it is a word predicition game. Here you've to guess the letters of word that has been selected under specific catagory by the computer. If the entered letter is in word it gets placed in its right position. you've 7 chances to save the man. if you can't find the word then man will die and the game ends there! :(\n\nTip: Guess with all 26 letters LOL!!\n''')
        hangman()

    elif ch == "4":

        os.system('cls')

        print('''
                                                                       ╔╦╗┬┌─┐  ╔╦╗┌─┐┌─┐  ╔╦╗┌─┐┌─┐   ╔═╗╦
                                                                        ║ ││     ║ ├─┤│     ║ │ │├┤ ───╠═╣║
                                                                        ╩ ┴└─┘   ╩ ┴ ┴└─┘   ╩ └─┘└─┘   ╩ ╩╩
        ''')

        print('\nYou have Choosen the game "TicTaeToe!!!"\n')
        print('''\nDescription:\n\tIn this game you've to pick the symbol you like to play. Here your opponent is computer. It has two difficulty level (easy) & (hard). you can pick you're difficulty. Twoplayers alternately put Xs and Os in compartments of a figure formed by two vertical lines crossing two horizontal lines and each tries to get a row of three Xs or three O's\t\tbefore the opponent does. The player who puts three X's or O's in a row will win the game!.\n\nTip: Its impossible to win in hard mode!, you can always pick easy mode to win the game.\n
Challenge (by-creater): Try to win the game in hard mode!.\n''')

        print('Choose the difficult level you would like to play....\n')

        game_mode = input("Press \'e\'(easy) or \'h\'(hard):").lower()

        if game_mode == 'e':
            user_choices = input("Want do you pick \'X\'or\'O\':").lower()
            if user_choices == 'X'.lower():
                x_player = HumanPlayer('X')
                o_player = RandomComputer('O')
            elif user_choices == 'O'.lower():
                x_player = RandomComputer('X')
                o_player = HumanPlayer('O')

        if game_mode == 'h':
            user_choices = input("Want do you pick \'X\'or\'O\':").lower()
            if user_choices == 'X'.lower():
                x_player = HumanPlayer('X')
                o_player = SmartComputer('O')
            elif user_choices == 'O'.lower():
                x_player = SmartComputer('X')
                o_player = HumanPlayer('O')

        t = TicTacToe()
        play(t, x_player, o_player, print_game=True)

    '''elif ch=="":
        print('\nYou have Choosen the game "Guessing Number by the Computer!!!"')
        GuessingNumberByComputer()'''

    print('\nYour overall score is: ', over_all_score)
    willing = input(
        ('\n If you want to continue press "yes" or "y" otherwise press "no" or "n":'))
    if willing == "y":
        continue
    elif willing == 'n':

        print("------------you're existed terminal games------------\n".center(170))
        print(f"{user} Overall score is:", over_all_score)
        # Database connectivity code begins here:
        username = user.lower()
        score = over_all_score
        conn = mysql.connector.connect(
            host='localhost', user='root', password='', database='project')
        cursor = conn.cursor()

        querry = "INSERT INTO gameusers(username,score,Id_no) VALUES(%s,%s,%s);"
        VALUES = (username, score, "")
        cursor.execute(querry, VALUES)

        print("registered successfull in database...!!!")

        conn.commit()
        conn.close()
        # End of database connectivity.

# End of Terminal games Code.

# screen = input("Do you want to go to next set of games if yes enter 'y':").lower()
# if screen == 'y':
#     os.system('cls')
# Nextgame = input("Enter 'p' to run 'Pong' or 's' to run 'suduko':").lower()
# if Nextgame == 'p':

#     #Score
#     score_a = int(input("Enter no of lives:"))
#     score_b = score_a
#     #here we change score as lives so if player lose point it will end.

#     def pong(score_a,score_b):

#         os.system('cls')

#         print('''
#                                                                 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄
#                                                                 ▐░░░░░░░░░░░ ▐░░░░░░░░░░░ ▐░░▌      ▐░ ▐░░░░░░░░░░░▌
#                                                                 ▐░█▀▀▀▀▀▀▀█░ ▐░█▀▀▀▀▀▀▀█░ ▐░▌░▌     ▐░ ▐░█▀▀▀▀▀▀▀▀▀
#                                                                 ▐░▌       ▐░ ▐░▌       ▐░ ▐░▌▐░▌    ▐░ ▐░▌
#                                                                 ▐░█▄▄▄▄▄▄▄█░ ▐░▌       ▐░ ▐░▌ ▐░▌   ▐░ ▐░▌ ▄▄▄▄▄▄▄▄
#                                                                 ▐░░░░░░░░░░░ ▐░▌       ▐░ ▐░▌  ▐░▌  ▐░ ▐░▌▐░░░░░░░░▌
#                                                                 ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░ ▐░▌   ▐░▌ ▐░ ▐░▌ ▀▀▀▀▀▀█░▌
#                                                                 ▐░▌          ▐░▌       ▐░ ▐░▌    ▐░▌▐░ ▐░▌       ▐░▌
#                                                                 ▐░▌          ▐░█▄▄▄▄▄▄▄█░ ▐░▌     ▐░▐░ ▐░█▄▄▄▄▄▄▄█░▌
#                                                                 ▐░▌          ▐░░░░░░░░░░░ ▐░▌      ▐░░ ▐░░░░░░░░░░░▌
#                                                                 ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀

#         ''')


#         win = turtle.Screen()
#         win.title("TERMINAL GAME-PONG")
#         win.bgcolor("purple")
#         win.setup(width=800, height=600)
#         win.tracer(0)


#         #Paddle A
#         paddle_a = turtle.Turtle()
#         paddle_a.speed(0)
#         paddle_a.shape("square")
#         paddle_a.color("violet")
#         paddle_a.shapesize(stretch_wid=5, stretch_len=1)
#         paddle_a.penup()
#         paddle_a.goto(-350,0)

#         #Paddle B
#         paddle_b = turtle.Turtle()
#         paddle_b.speed(0)
#         paddle_b.shape("square")
#         paddle_b.color("black")
#         paddle_b.shapesize(stretch_wid=5, stretch_len=1)
#         paddle_b.penup()
#         paddle_b.goto(350,0)

#         #BALL
#         ball = turtle.Turtle()
#         ball.speed(0)
#         ball.shape("circle")
#         ball.color("white")
#         ball.penup()
#         ball.goto(0,0)
#         ball.dxp = 0.22
#         ball.dyp = -0.22

#         #Pen
#         pen = turtle.Turtle()
#         pen.speed(0)
#         pen.color("black")
#         pen.penup()
#         pen.hideturtle()
#         pen.goto(0,260)
#         pen.write(f"Player A: {score_a} lives left & Player B: {score_b} lives left",align="center", font=("Courier", 12, "normal"))

#         #FUNCTION Area:
#         def paddle_a_up():
#             y = paddle_a.ycor()
#             y += 20
#             paddle_a.sety(y)

#         def paddle_a_down():
#             y = paddle_a.ycor()
#             y -= 20
#             paddle_a.sety(y)

#         def paddle_b_up():
#             y = paddle_b.ycor()
#             y += 20
#             paddle_b.sety(y)

#         def paddle_b_down():
#             y = paddle_b.ycor()
#             y -= 20
#             paddle_b.sety(y)


#         #Keyboard binding
#         win.listen()
#         win.onkeypress(paddle_a_up,"w")
#         win.onkeypress(paddle_a_down,"s")
#         win.onkeypress(paddle_b_up,"i")
#         win.onkeypress(paddle_b_down,"k")

#         #MAIN GAME LOOP


#         while True:

#             win.update()

#             #Move the ball
#             ball.setx(ball.xcor()+ball.dxp)
#             ball.sety(ball.ycor()+ball.dyp)

#             #Board checking
#             if ball.ycor() > 290:
#                 ball.sety(290)
#                 ball.dyp *= -1
#                 winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

#             if ball.ycor() < -290:
#                 ball.sety(-290)
#                 ball.dyp *= -1
#                 winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

#             if ball.xcor() > 390:
#                 ball.goto(0,0)
#                 ball.dxp *= -1
#                 score_b -= 1
#                 pen.clear()
#                 pen.write(f"Player A: {score_a} lives left & Player B: {score_b} lives left",align="center", font=("Courier", 12, "normal"))

#             if ball.xcor() < -390:
#                 ball.goto(0,0)
#                 ball.dxp *= -1
#                 score_a -= 1
#                 pen.clear()
#                 pen.write(f"Player A: {score_a} lives left & Player B: {score_b} lives left",align="center", font=("Courier", 12, "normal"))

#             # Paddle and ball collisions
#             if ball.xcor() > 340 and ball.xcor() < 350 and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
#                 ball.setx(340)
#                 ball.dxp *= -1
#                 winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

#             if ball.xcor() < -340 and ball.xcor() > -350 and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
#                 ball.setx(-340)
#                 ball.dxp *= -1
#                 winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

#             if score_a == 0 or score_b == 0:
#                 break

#         print("Game has ended...!!")
#         if score_a > score_b:
#             print(f"Player A left with {score_a} lives.")
#             print("Congratulations... Player A,You Won the game!")

#         else:
#             print(f"Player B left with {score_b} lives.")
#             print("Congratulations... Player B,You Won the game!")

#     pong(score_a,score_b)

# else:

#     def find_next_empty(puzzle):
#         # finds the next row, col on the puzzle that's not filled yet --> rep with -1
#         # return row, col tuple (or (None, None) if there is none)

#         # keep in mind that we are using 0-8 for our indices
#         for r in range(9):
#             for c in range(9): # range(9) is 0, 1, 2, ... 8
#                 if puzzle[r][c] == -1:
#                     return r, c

#         return None, None  # if no spaces in the puzzle are empty (-1)

#     def is_valid(puzzle, guess, row, col):
#         # figures out whether the guess at the row/col of the puzzle is a valid guess
#         # returns True or False

#         # for a guess to be valid, then we need to follow the sudoku rules
#         # that number must not be repeated in the row, column, or 3x3 square that it appears in

#         # let's start with the row
#         row_vals = puzzle[row]
#         if guess in row_vals:
#             return False # if we've repeated, then our guess is not valid!

#         # now the column
#         # col_vals = []
#         # for i in range(9):
#         #     col_vals.append(puzzle[i][col])
#         col_vals = [puzzle[i][col] for i in range(9)]
#         if guess in col_vals:
#             return False

#         # and then the square
#         row_start = (row // 3) * 3 # 10 // 3 = 3, 5 // 3 = 1, 1 // 3 = 0
#         col_start = (col // 3) * 3

#         for r in range(row_start, row_start + 3):
#             for c in range(col_start, col_start + 3):
#                 if puzzle[r][c] == guess:
#                     return False

#         return True

#     def solve_sudoku(puzzle):
#         # solve sudoku using backtracking!
#         # our puzzle is a list of lists, where each inner list is a row in our sudoku puzzle
#         # return whether a solution exists
#         # mutates puzzle to be the solution (if solution exists)

#         # step 1: choose somewhere on the puzzle to make a guess
#         row, col = find_next_empty(puzzle)

#         # step 1.1: if there's nowhere left, then we're done because we only allowed valid inputs
#         if row is None:  # this is true if our find_next_empty function returns None, None
#             return True

#         # step 2: if there is a place to put a number, then make a guess between 1 and 9
#         for guess in range(1, 10): # range(1, 10) is 1, 2, 3, ... 9
#             # step 3: check if this is a valid guess
#             if is_valid(puzzle, guess, row, col):
#                 # step 3.1: if this is a valid guess, then place it at that spot on the puzzle
#                 puzzle[row][col] = guess
#                 # step 4: then we recursively call our solver!
#                 if solve_sudoku(puzzle):
#                     return True

#             # step 5: it not valid or if nothing gets returned true, then we need to backtrack and try a new number
#             puzzle[row][col] = -1

#         # step 6: if none of the numbers that we try work, then this puzzle is UNSOLVABLE!!
#         return False

#     if __name__ == '__main__':

#         os.system('cls')

#         example_board = [
#             [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
#             [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
#             [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

#             [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
#             [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
#             [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

#             [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
#             [6, 7, -1,   1, -1, 5,   -1, 4, -1],
#             [1, -1, 9,   -1, -1, -1,   2, -1, -1]
#         ]

#         '''example_board = [
#             [5, 3, -1, -1, 7, -1, -1, -1, -1],
#             [6, -1, -1,  1, 9, 5, -1, -1, -1],
#             [-1, 9, 8, -1, -1, -1, -1, 6, -1],

#             [8, -1, -1, -1, 6, -1,  -1, -1, 3],
#             [4, -1, -1, 8, -1, 3, -1, -1, 1],
#             [7, -1, -1, -1, 2, -1,  -1, -1, 6],

#             [-1, 6, -1, -1, -1, -1, 2, 8, -1],
#             [-1, -1, -1,  4, 1, 9, -1, -1, 5],
#             [-1, -1, -1, -1, 8, -1, -1, 7, 9]
#         ]'''

#         print("Solved The Give Suduko Puzzle Question:",solve_sudoku(example_board))
#         pprint(example_board)
