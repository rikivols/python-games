"""
Squares game in tkinter. Clicking on green square adds one point, clicking on red square subtracts 2
points.

Game contains 4 levels, and it always gets harder. To win 30 points are needed.
"""

import tkinter
import random as rd

w = 800
h = 800
canvas = tkinter.Canvas(width=w, height=h)
canvas.pack()

level = 1
is_poisoned = -1  # red (poisoned) square
points = 0
r = 40            # radius of the square
win = 0           # check if we already won game (used when resetting game)
was_first_green = 0     # was first click on green square (to fix a bug - adding 2 points at the start)


def draw_outline():
    """
    Draw outline / background of the program.

    Uses 2 global variables: points, level
    """
    
    canvas.create_text(w/9.3, h/40, text="Level 1: 0 - 9 p", font="Times 20")
    canvas.create_text(w/8, h/16, text="Level 2: 10 - 14 p", font="Times 20")
    canvas.create_text(w/8, h/10, text="Level 3: 15 - 19 p", font="Times 20")
    canvas.create_text(w/5.26, h/7.27, text="Level 4: 20+ p (impossible)",
                       font="Times 20")
    canvas.create_text(w/14, h/5.71, text="Win: 30 b", font="Times 20")
    canvas.create_text(w/2, h/14.5, text=f"Points: ", font="Times 40 bold")
    canvas.create_text(w/1.61, h/14, text=points, font="Times 40 bold")
    
    canvas.create_text(w/2, h/6.5, text=f"Level: ", font="Times 40 bold")
    canvas.create_text(w/1.61, h/6.5, text=level, font="Times 40 bold")

    canvas.create_text(w/1.18, h/20, text="Warning, red square", font="Times 20")
    canvas.create_text(w/1.18, h/11, text="is poisoned", font="Times 20")
    canvas.create_text(w/1.21, h/6, text="Right click: reset", font="Times 20")


def rect():
    """
    Main function, draws squares, controls points...

    In the first part distributes levels depending on points, also changes
    radius of the squares and speed of changing of squares.

    Next it randomly generates red or green square. Handles changing of points. With
    help of function click checks squares which have been clicked.

    global variables:
    x_, y_: coordinates
    r: radius of randomly generated square
    points: points of player
    is_poisoned: 1 - square is red 0 - square is green
    level: on which level we are currently on
    win: 1 if the game was won
    was_clicked: check if we already clicked on some square (fixes bug - repeated
                 clicking on square increased points)
    """

    global x_, y_, r, points, is_poisoned, level, win, was_clicked

    was_clicked = 0

    """
    Depending on points distributes levels. With each changed level changes also radius 
    of squares and speed of changing.
    """

    if points >= 30:  # win
        canvas.delete("all")
        canvas.create_text(w/2, h/2.6, text="Congratulations, you won.",
                           font="Times 50")
        canvas.create_text(w/2, h/1.78, text="Play again? (left click)",
                           font="Times 30")
        win = 1
        return
    # level 4
    elif points >= 20:
        level = 4
        r = 20
        speed = 650
        
    # level 3
    elif points >= 15:
        level = 3
        r = 20
        speed = 800
        
    # level 2
    elif points >= 10:
        level = 2
        r = 25
        speed = 800

    # level 1
    else:
        level = 1
        r = 40
        speed = 1000

    """
    ------------------------------------------------------------------------------
    """

    canvas.delete("all")

    points = max(points, 0)  # fixes bug, at the start we could have negative points
    draw_outline()  # draws background

    green_red = rd.randint(1, 10)  # chance 2/10 on red square, 8/10 on green square

    x_ = rd.randint(r, 800 - r)
    y_ = rd.randint(170 + r, 800 - r)

    if green_red in range(1, 3):  # red square
        color = "red"
        is_poisoned = 1

    else:  # green square
        color = "green"
        is_poisoned = 0
        points -= 1
        
    canvas.create_rectangle(x_ - r, y_ - r, x_ + r, y_ + r, fill=color, tags="del")
    canvas.after(speed, rect)

    points = max(0, points)  # gets rid of negative points
    

def click(event):
    """
    Handles user's left click and changes points accordingly

    was_first_green:   was first click on green square (to fix a bug - adding 2 points at the start)
    was_clicked: check if we already clicked on some square (fixes bug - repeated
                 clicking on square increased points)
    """
    global points, was_first_green, was_clicked
    
    click_x = event.x
    click_y = event.y

    if click_x in range(x_ - r, x_ + r) and click_y in range(y_ - r, y_ + r):

        if was_clicked == 0:
            if is_poisoned == 1:
                points -= 2
            else:
                if was_first_green == 0:
                    points += 1
                    was_first_green = 1
                else:
                    points += 2
                  
    canvas.delete("square")
    was_clicked = 1
    return


def nova_hra(_):
    """
    Resets game.

    r: radius of randomly generated square
    points: points of player
    is_poisoned: 1 - square is red 0 - square is green
    level: on which level we are currently on
    win: 1 if the game was won
    was_first_green: was first click on green square (to fix a bug - adding 2 points at the start)
    """

    global r, points, is_poisoned, level, win, was_first_green

    level = 1
    is_poisoned = -1
    points = 0
    r = 40
    was_first_green = 0
    canvas.delete("all")
    # if we called rect and the game wasn't won, game would unexpectedly speed up.
    if win == 1:
        win = 0
        rect()
    

canvas.bind('<Button-1>', click)
canvas.bind('<Button-3>', nova_hra)
rect()
