import os
import random
from hangman_visual import lives_visual_dict
import string


def get_valid_word():

    word_no = random.randint(1,8)  # randomly chooses no of the list

    if word_no == 1:
        print("You need to guess a word under \'VEGETABLES\' category......\n")

        vegetables = ['CARROT', 'BROCCOLI ', 'CAULIFLOWER ', 'CORN ', 'CUCUMBER ', 'EGGPLANT', 'GREENPEPPER ',
                    'LETTUCE ', 'MUSHROOMS', 'ONION', 'POTATO', 'PUMPKIN ', 'REDPEPPER', 'TOMATO ', 'BEETROOT', 'PEAS',
                    'RADISH', 'CABBAGE', 'CHILI', 'GARLIC', 'SWEETPOTATO', 'CORIANDER','TAMARIND' ]
        word = random.choice(vegetables)

    if word_no == 2:
        print("You need to guess a word under \'VEHICLES\' category......\n")

        vehicles = ['HELICOPTER', 'AIRPLANE', 'ROCKET', 'SAILBOAT', 'CRUISESHIP', 'CARGOSHIP', 'JETSKI',
                   'SHIP', 'BOAT', 'SUBMARINE','BICYCLE', 'CAR', 'BUS', 'TRAIN', 'TRUCK', 'VAN',
                   'MOTORCYCLE','Taxi','Policecar','Ambulance','Skateboard','Mountainbike','Scooter','Fireengine',
                   'Crane','Forklift','Tractor','Cementmixer','Dumptruck','Gasballoon','Tram','Carriage']
        word = random.choice(vehicles)

    if word_no == 3:
        print("You need to guess a word under \'ANIMALS\' category......\n")

        Animals = ['Hummingbird','BIRD', 'DOG', 'DONKEY', 'GIRAFFE', 'ALLIGATOR', 'CAT', 'HORSE', 'LION', 'MONKEY', 'BEE', 'DUCK',
                  'FROG', 'ELEPHANT', 'CROCODILE', 'DOLPHIN', 'GORILLA', 'MOUSE', 'TIGER', 'RABBIT','RAT']

        word = random.choice(Animals)

    if word_no == 4:
        print("You need to guess a word under \'HUMANORGANS\' category......\n")

        Bodyparts =['Head','Face','Hair','Ear','Neck','Forehead','Beard','Eye','Nose','Mouth','Chin','Shoulder','Elbow',
            'Arm','Chest','Armpit','Forearm','Wrist','Back','Navel','Toes','Ankle','Instep','Toenail','Waist','Abdomen',
            'Buttock','Hip','Leg','Thigh','Knee','Foot','Hand','Thumb']
        word = random.choice(Bodyparts)

    if word_no == 5:
        print("You need to guess a word under \'COLOURS\' category......\n")

        Colours = ['RED', 'YELLOW', 'BLUE', 'GREEN', 'ORANGE', 'PURPLE', 'LIME', 'BROWN', 'NAVY', 'PINK', 'GOLD',
                 'SILVER', 'BLACK', 'WHITE','INDIGO','TURKISHBLUE','VIOLET','SAFRON','ROSE','MAGENTA','MAROON']
        word = random.choice(Colours)

    if word_no == 6:
        print("You need to guess a word under \'FRUITS\' category......\n")

        fruits = ['APPLE', 'GUAVA', 'PEACH', 'PEAR', 'MANGO', 'PAPAYA', 'ORANGE', 'GRAPES', 'KIWI', 'CHERRY',
                 'WATERMELON', 'PINEAPPLE', 'BLUEBERRY', 'BANANA', 'COCONUT', 'CUSTARDAPPLE', 'LEMON', 'MULBERRY']
        word = random.choice(fruits)

    if word_no == 7:
        print("You need to guess a word under \'SHAPES\' category......\n")

        shapes = ['CIRCLE', 'DIAMOND', 'HEART', 'OCTAGON', 'SQUARE', 'STAR', 'TRIANGLE'
          'Nonagon','Octagon','Heptagon','Hexagon','Scalenetriangle','Righttriangle','Parallelogram','Rhombus',
          'Pentagon','Oval','Heart','Cross','Arrow','Cube','Cylinder','Crescent']
        word = random.choice(shapes)

    if word_no == 8:
        print("You need to guess a word under \'INSECTS\' category......\n")

        insects = ['Armyants','Bumblebees','Cicadas','dragonflies','Earwigs','Fireflies','Grasshoppers','Jewelbeetles','Katydids',
           'Lacewings','Mosquitoes','Netwings','flies','Paperwasps','Queentermites','Robberflies','Spiderwasps','beetles',
           'moths','butterflies','Weevils','bees','Yuccamoths']
        word = random.choice(insects)

    length = len(word)
    print(f"Its {length} letter word make a guess!\n")
    return word.upper()


def hangman(hscore = 0):
    word = get_valid_word()
    word_letters = set(word)  # letters in the word
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # what the user has guessed
    lives = 7

    # getting user input
    while len(word_letters) > 0 and lives > 0:
        # letters used
        # ' '.join(['a', 'b', 'cd']) --> 'a b cd'
        print('You have', lives, 'lives left and you have used these letters: ', ' '.join(used_letters))

        # what current word is (ie W - R D)
        word_list = [letter if letter in used_letters else '-' for letter in word]
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
        hscore += 0
        print('Your Score:',hscore)
        
    else:
        print('YAY! You guessed the word', word, '!!')
        hscore += 20
        print('Your Score:',hscore)
        
        
    
    user_x = input("Do you like to return to Main terminal if yes press\'y\':").lower()
    if user_x == 'y':
       os.system('python MainTerminal.py')



if __name__ == '__main__':

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

    print('''How to play this game...
                        A random word is choosen you have to guess the word within several chances.\n''')
    hangman()



