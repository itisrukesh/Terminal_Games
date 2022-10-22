import random
import math
import os

gscore = 0
os.system('cls')

print('''
                                                ███████ ██   ██  █████   ██████ ████████     ███    ███  █████  ████████  ██████ ██   ██ 
                                                ██       ██ ██  ██   ██ ██         ██        ████  ████ ██   ██    ██    ██      ██   ██ 
                                                █████     ███   ███████ ██         ██        ██ ████ ██ ███████    ██    ██      ███████ 
                                                ██       ██ ██  ██   ██ ██         ██        ██  ██  ██ ██   ██    ██    ██      ██   ██ 
                                                ███████ ██   ██ ██   ██  ██████    ██        ██      ██ ██   ██    ██     ██████ ██   ██ 
                                                                                                                                    
                                                                                                                                        
''')

print("Guessing (by the user) number game!!!\n")
victory=0
# Taking Inputs
lower = int(input("Enter Lower range:- "))

# Taking Inputs
upper = int(input("Enter Upper range:- "))

# generating random number between
# the lower and upper
x = random.randint(lower, upper)
chances = round(math.log(upper - lower + 1, 2))
print("\n\tNow you can guess any integer from",lower,"to",upper,"and You've only",chances,"chances!\n")

# Initializing the number of guesses.
count = 0

# for calculation of minimum number of
# guesses depends upon range
while count < chances:
    count += 1

    # taking guessing number as input
    guess = int(input("Guess a number:- "))

    # Condition testing
    if x == guess:
        victory=1
        print("\t The number is",x,"!Congratulations you did it in",count,"try")
        gscore += 20
        print(f'Your score:',gscore)
        # Once guessed, loop will break
        break
    elif x > guess:
        print("\tYou guessed too small!")
    elif x < guess:
        print("\tYou Guessed too high!")

# If Guessing is more than required guesses,
# shows this output.
if victory == 0:
    print("\nThe number is %d" % x)
    print("\tBetter Luck Next time!")
    gscore += 0
    print(f'Your score:',gscore)

user_x = input("Do you like to return to Main terminal if yes press\'y\':").lower()
if user_x == 'y':
    os.system('python MainTerminal.py')



'''def comguess(x):
    upp=x
    low=1
    clues="NULL"
    while clues!="c":
        guessNumber=random.randint(low,upp)
        clues=input(f'\nThe guessing number is {guessNumber} if too high (H), if too low(L), if correct (C) :').lower()
        if clues=="h":
            upp=guessNumber-1
        elif clues=="l":
            low=guessNumber+1
    print(f'{guessNumber} is correct computer won the game')'''
    

'''n=int(input("Enter the limit to guess a number:"))
print('\nNow you can Assume any positive number upto',n)'''
'''comguess(n)'''


