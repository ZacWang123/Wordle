from tkinter import *

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
            

def validate_entry(entry):
    if len(entry) <= 1:
        return True
    else:
        return False
    
    
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
    
    window.mainloop()
    
if __name__ == "__main__":
    main()