from tkinter import *
import random

gridEntries = [[None for x in range(5)] for y in range(6)] 
word = ""
row = 0
col = 0

def start_gameloop(window):
    enable_entry(row, col)
    window.after(1, game_intervels, window)
    
def game_intervels(window):
    global row
    global col
    
    if col < 5:
        if (gridEntries[row][col].get() != ""):
            disable_entry(row, col)
            col += 1
            if col < 5:
                enable_entry(row, col)
        
    window.after(20, game_intervels, window)

def create_letterbox(window):
    grid = Frame(window)
    grid['bg'] = "#3b3b3b"
    grid.pack(padx = (0, 0))
    grid.pack(pady = (50, 0))
    
    vcmd = (window.register(validate_entry), "%P")
    
    for x in range(6):
        for y in range(5):
            entry = Entry(grid, width = 2, font=("Arial", 36), justify = "center", validate="key", validatecommand = vcmd)
            entry.config(insertbackground = 'white')
            entry.grid(row = x, column = y, padx = 10, pady = 10)
            entry.bind("<BackSpace>", lambda event, x=x, y=y: detect_backspace(event, x, y))
            entry.bind("<KeyPress>", lambda event, x=x, y=y: upper_case(event, x, y))
            entry.bind("<Return>", lambda event, x=x, y=y: detect_enter(event, x, y))
            gridEntries[x][y] = entry
            disable_entry(x, y)
            
def disable_entry(x, y):
    gridEntries[x][y].config(state='disabled', disabledforeground = "black")
    
def enable_entry(x,y):
    gridEntries[x][y].config(state='normal')
    gridEntries[x][y].focus_set()
    
def delete_entry(x, y):
    gridEntries[x][y].delete(0, END)
    
def validate_entry(entry):
    if len(entry) <= 1:
        return True
    else:
        return False
    
def generate_word():
    global word
    
    random_number = random.randint(0, 2309)
    
    with open("5-letter_words.txt", "r") as file:
        for lineNum, line in enumerate(file):
            if lineNum == random_number:
                word = line.strip().upper()
                break

def detect_backspace(event, x, y):
    global row
    global col
    
    if col > 0:
        if col < 5:
            disable_entry(row, col)
        col -= 1
        enable_entry(row, col)
        delete_entry(row, col)
        
def detect_enter(event, x, y):
    global row
    global col
    
    if col == 5:
        print("asdasdasdasd")
            
def upper_case(event, x, y):
    gridEntries[x][y].delete(0, END)
    char = event.char.upper()
    
    if char.isalpha():
        event.widget.insert(0, char)
    return "break"
    

def create_window():
    window = Tk()
    window.title("Wordle")
    window['bg'] = "#3b3b3b"
    
    windowWidth = 600
    windowHeight = 800
    
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()

    positionX = int(screenWidth/2 - windowWidth/2)
    positionY = int(screenHeight/2 - windowHeight/2)

    window.geometry(f"{windowWidth}x{windowHeight}+{positionX}+{positionY}")
    
    return window
    
def main():
    window = create_window()
    
    create_letterbox(window)
    
    generate_word()
    
    start_gameloop(window)
        
    window.mainloop()
    
if __name__ == "__main__":
    main()