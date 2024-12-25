from tkinter import *

gridEntries = [[None for x in range(5)] for y in range(6)] 
row = 0
col = 0

def start_gameloop(window):
    enable_entry(row, col)
    window.after(1, game_intervels, window)
    
def game_intervels(window):
    global row
    global col
    
    if (col < 4):
        if (gridEntries[row][col].get() != ""):
            disable_entry(row, col)
            col += 1
            enable_entry(row, col)
        
    window.after(100, game_intervels, window)

def create_letterbox(window):
    grid = Frame(window)
    grid['bg'] = "#3b3b3b"
    grid.pack(padx = (0, 0))
    grid.pack(pady = (50, 0))
    
    vcmd = (window.register(validate_entry), "%P")
    
    for x in range(6):
        for y in range(5):
            entry = Entry(grid, width = 2, font=("Arial", 36), justify = "center", validate="key", validatecommand = vcmd)
            entry.grid(row = x, column = y, padx = 10, pady = 10)
            entry.bind("<BackSpace>", lambda event, x=x, y=y: detect_backspace(event, x, y))
            gridEntries[x][y] = entry
            disable_entry(x, y)
            
def disable_entry(x, y):
    gridEntries[x][y].config(state='disabled')
    
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

def detect_backspace(event, x, y):
    global row
    global col
    
    if gridEntries[x][y].get() == "":
        if col > 0:
            disable_entry(row, col)
            col -= 1
            enable_entry(row, col)
            delete_entry(row, col)

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
    
    start_gameloop(window)
        
    window.mainloop()
    
if __name__ == "__main__":
    main()