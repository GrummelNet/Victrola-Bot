# this file defines a grid of buttons in a window to control what the bot is playing
import tkinter as tk
from functools import partial


# takes in a number, returns the smallest square that can fit that number of things
# so, if I pass in 14 it would return 4 since 4^2=16
def smallestSquare(iCt):
    rv = 1
    while iCt > (rv*rv):
        rv += 1
    print(f"ss: {rv}")
    return rv


def buttonTest(label):
    print(f"the {label} button was clicked!")


def makeWindow():
    window = tk.Tk()
    window.title("Greetings, traveler! Care for a song?")
    return window

# def main():
#     window = tk.Tk()
#     window.title("Greetings, traveler! Care for a song?")
#
#     listOfSongs = ["button1","button2","button3","button4","button5","button6"]
#     buttonsFromList(listOfSongs, window)
#
#     window.mainloop()


# main()
