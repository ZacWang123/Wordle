from tkinter import *

def create_letterbox(window):
    entry = Entry(window, width = 1)
    entry.grid(pady=10)

def create_window():
    window = Tk()
    window.title("Wordle")

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