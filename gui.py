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
def buttonsFromList(textList, m):
    for bText in textList:
        button = tk.Button(
            master = m,
            text = bText,
            command = partial(buttonTest, bText)
        )
        button.pack()


def buttonTest(label):
    print(f"the {label} button was clicked!")


def main():
    window = tk.Tk()
    window.title("Greetings Outsider? Care for a song?")

    listOfSongs = ["button1","button2","button3","button4","button5","button6"]
    buttonsFromList(listOfSongs, window)

    # testB = tk.Button(
    #     master = window,
    #     text = "song name",
    #     command = buttonTest
    # )
    # testB.pack()


    window.mainloop()


main()
