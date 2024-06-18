import tkinter as tk
from game import Game
from settings import *

root = tk.Tk()

def startGameWithSelectedSize():
    for i in listbox.curselection():
        size = listbox.get(i).split("x")

        with open("settings.py", "r") as settings:
            lines = settings.readlines()
            lines[0] = f"WIDTH, HEIGHT = {size[0]}, {size[1]}\n"
            settings.close()
            
        with open("settings.py", "w") as settings:
            settings.writelines(lines)
            settings.close()

        root.destroy()

        game = Game()
        while game.running:
            game.run()

if __name__ == "__main__":
    
    size_list = ("1920x1080", "1366x768", "1280x1024", "1440x900", "1600x900", "1680x1050", "1280x800", "1024x768")

    root.geometry('600x400')
    root.title('Escape of the RedHood Menu')

    description = tk.Label(root, text="Please choose a window size to start the game.", font=("Courier", 14))

    listbox = tk.Listbox(root, height = 8, font=("Courier", 14))
    scrollbar = tk.Scrollbar(root) 
    scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)  
    for values in size_list: 
        listbox.insert(tk.END, values) 
    listbox.config(yscrollcommand = scrollbar.set) 
    scrollbar.config(command = listbox.yview)
    
    btn = tk.Button(root, text='Start Game', command=startGameWithSelectedSize, font=("Courier", 14))
    
    description.pack(side='top')
    listbox.pack(side = tk.LEFT, fill = tk.BOTH)
    btn.pack(side='bottom')
    
    root.mainloop()

    