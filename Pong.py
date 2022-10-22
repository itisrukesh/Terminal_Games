import turtle
import winsound
import os


a = False
#Score
score_a = int(input("Enter no of lives:"))
score_b = score_a
#here we change score as lives so if player lose point it will end.

def pong(score_a,score_b):

    os.system('cls')

    print('''
                                                             ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄ 
                                                            ▐░░░░░░░░░░░ ▐░░░░░░░░░░░ ▐░░▌      ▐░ ▐░░░░░░░░░░░▌
                                                            ▐░█▀▀▀▀▀▀▀█░ ▐░█▀▀▀▀▀▀▀█░ ▐░▌░▌     ▐░ ▐░█▀▀▀▀▀▀▀▀▀ 
                                                            ▐░▌       ▐░ ▐░▌       ▐░ ▐░▌▐░▌    ▐░ ▐░▌          
                                                            ▐░█▄▄▄▄▄▄▄█░ ▐░▌       ▐░ ▐░▌ ▐░▌   ▐░ ▐░▌ ▄▄▄▄▄▄▄▄ 
                                                            ▐░░░░░░░░░░░ ▐░▌       ▐░ ▐░▌  ▐░▌  ▐░ ▐░▌▐░░░░░░░░▌
                                                            ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░ ▐░▌   ▐░▌ ▐░ ▐░▌ ▀▀▀▀▀▀█░▌
                                                            ▐░▌          ▐░▌       ▐░ ▐░▌    ▐░▌▐░ ▐░▌       ▐░▌
                                                            ▐░▌          ▐░█▄▄▄▄▄▄▄█░ ▐░▌     ▐░▐░ ▐░█▄▄▄▄▄▄▄█░▌
                                                            ▐░▌          ▐░░░░░░░░░░░ ▐░▌      ▐░░ ▐░░░░░░░░░░░▌
                                                             ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
                                                                                                            
    ''')


    win = turtle.Screen()
    win.title("TERMINAL GAME-PONG")
    win.bgcolor("purple")
    win.setup(width=800, height=600)
    win.tracer(0)


    #Paddle A
    paddle_a = turtle.Turtle()
    paddle_a.speed(0)
    paddle_a.shape("square")
    paddle_a.color("violet")
    paddle_a.shapesize(stretch_wid=5, stretch_len=1)
    paddle_a.penup()
    paddle_a.goto(-350,0)

    #Paddle B
    paddle_b = turtle.Turtle()
    paddle_b.speed(0)
    paddle_b.shape("square")
    paddle_b.color("black")
    paddle_b.shapesize(stretch_wid=5, stretch_len=1)
    paddle_b.penup()
    paddle_b.goto(350,0)

    #BALL
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color("white")
    ball.penup()
    ball.goto(0,0)
    ball.dxp = 0.22
    ball.dyp = -0.22

    #Pen
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("black")
    pen.penup()
    pen.hideturtle()
    pen.goto(0,260)
    pen.write(f"Player A: {score_a} lives left & Player B: {score_b} lives left",align="center", font=("Courier", 12, "normal"))

    #FUNCTION Area:
    def paddle_a_up():
        y = paddle_a.ycor()
        y += 20
        paddle_a.sety(y)

    def paddle_a_down():
        y = paddle_a.ycor()
        y -= 20
        paddle_a.sety(y)

    def paddle_b_up():
        y = paddle_b.ycor()
        y += 20
        paddle_b.sety(y)

    def paddle_b_down():
        y = paddle_b.ycor()
        y -= 20
        paddle_b.sety(y)


    #Keyboard binding
    win.listen()
    win.onkeypress(paddle_a_up,"w")
    win.onkeypress(paddle_a_down,"s")
    win.onkeypress(paddle_b_up,"i")
    win.onkeypress(paddle_b_down,"k")

    #MAIN GAME LOOP
    

    while True:

        win.update()

        #Move the ball
        ball.setx(ball.xcor()+ball.dxp)
        ball.sety(ball.ycor()+ball.dyp)

        #Board checking
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dyp *= -1
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dyp *= -1
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        
        if ball.xcor() > 390:
            ball.goto(0,0)
            ball.dxp *= -1
            score_b -= 1
            pen.clear()
            pen.write(f"Player A: {score_a} lives left & Player B: {score_b} lives left",align="center", font=("Courier", 12, "normal"))

        if ball.xcor() < -390:
            ball.goto(0,0)
            ball.dxp *= -1
            score_a -= 1
            pen.clear()
            pen.write(f"Player A: {score_a} lives left & Player B: {score_b} lives left",align="center", font=("Courier", 12, "normal"))
        
        # Paddle and ball collisions
        if ball.xcor() > 340 and ball.xcor() < 350 and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
            ball.setx(340)
            ball.dxp *= -1
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

        if ball.xcor() < -340 and ball.xcor() > -350 and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
            ball.setx(-340)
            ball.dxp *= -1
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

        if score_a == 0 or score_b == 0:
            break

    print("Game has ended...!!")
    if score_a > score_b:
        print(f"Player A left with {score_a} lives.")
        print("Congratulations... Player A,You Won the game!")
        a = True  
    else:
        print(f"Player B left with {score_b} lives.")
        print("Congratulations... Player B,You Won the game!")
        a = True
    
    user_x = input("Do you like to return to Main terminal if yes press\'y\':").lower()
    if a == True and user_x == 'y':
       os.system('python MainTerminal.py')

    


pong(score_a,score_b)