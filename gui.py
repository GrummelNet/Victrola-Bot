# this file defines a grid of buttons in a window to control what the bot is playing
import tkinter as tk
from functools import partial


# takes in a number, returns the smallest square that can fit that number of things
# so, if I pass in 14 it would return 4 since 4^2=16
def smallestSquare(iCt):
    rv = 1
    while iCt > (rv*rv):
        rv += 1
    return rv


# takes in a list of button texts and returns a list of buttons with those texts
# arranges them in a grid
def buttonsFromList(textList, m):
    width = smallestSquare(len(textList))

    r = 0
    c = 0
    for bText in textList:
        button = tk.Button(
            master = m,
            text = bText,
            command = partial(buttonTest, bText),
            height = 5,
            width =  15
        )
        button.grid(row=r, column=c)
        # button.pack()
        c += 1
        if c > width:
            c = 0
            r += 1
    # TODO: add connect + disconnect buttons


def buttonTest(label):
    print(f"the {label} button was clicked!")


def main():
    window = tk.Tk()
    window.title("Greetings, traveler! Care for a song?")

    listOfSongs = ["button1","button2","button3","button4","button5","button6"]
    buttonsFromList(listOfSongs, window)

    window.mainloop()


main()
