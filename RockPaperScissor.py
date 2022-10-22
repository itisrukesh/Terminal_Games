import random
import os

rpscore = 0
player_score=0
comp_score=0
os.system('cls')

print('''
                                                      Yb        dP w                        8                        
                                                       Yb  db  dP  w 8d8b.    .d8b. 8d8b    8 .d8b. d88b .d88b       
                                                        YbdPYbdP   8 8P Y8    8' .8 8P      8 8' .8 `Yb. 8.dP'       
                                                         YP  YP    8 8   8    `Y8P' 8       8 `Y8P' Y88P `Y88P w w w 
                                                                                                                     
''')

#Program to play Rock,Scissor, and Paper game

total_score=int(input('\nEnter over all score to decide the winner : '))
while player_score<total_score and comp_score<total_score:
    player=input("Choose any one : Rock(R), Paper(P), Scissor(S) : ")
    comp=random.choice(['R','P','S'])
    if player==comp:
        print('Tie!')
    elif player=="R" or player=="r":
        if comp=="P":
            comp_score+=1
            print('\nComputer choose Paper \n Paper covers the Rock Computer won the point ')
        else:
            player_score+=1
            print('\nComputer choose Scissor \n Rock smashes the scissor Player won the point ')
    elif player=="P" or player=="p":
        if comp=="S":
            comp_score+=1
            print('\nComputer choose Scissor \n Scissor cuts the paper computer won the point ')
        else:
            player_score+=1
            print('\ncomputer choose Rock \n Paper covers the rock player won the point')
    elif player=="S" or player=="s":
        if comp=="R":
            comp_score+=1
            print('\nComputer choose Rock \n Rock smashes the scissor computer won the point')
        else:
            player_score+=1
            print('\nComputer choose paper \n Scissor cuts the paper player won the point ')
    else:
        print('Check your spelling !!')

if player_score==total_score:
    print('\nComputer Score :',comp_score,', Player Score :',player_score,'Player won the game!')
    rpscore += 20
    print('Your score:',rpscore)
else:
    print('\nComputer Score :',comp_score,', Player Score :',player_score,'Computer won the game!')
    rpscore += 0
    print('Your score:',rpscore)

user_x = input("Do you like to return to Main terminal if yes press\'y\':").lower()
if user_x == 'y':
    os.system('python MainTerminal.py')