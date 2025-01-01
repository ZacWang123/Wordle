from tkinter import *
import tkinter.messagebox as messagebox
import random
import sys

def initialise_variables():
    global gridEntries, keyboardEntries, word, row, col, gameActive 
    
    gridEntries = [[None for x in range(5)] for y in range(6)] 
    keyboardEntries = [None for x in range(28)]
    word = ""
    row = 0
    col = 0
    gameActive = True

def start_gameloop(window):
    enable_entry(row, col)
    window.after(5, game_intervels, window)
    
def game_intervels(window):
    global row, col, gameActive
    
    if gameActive:
        if col < 5:
            if (gridEntries[row][col].get() != ""):
                disable_entry(row, col)
                col += 1
                if col < 5:
                    enable_entry(row, col)
        
        window.after(20, game_intervels, window)
    else:
        return
    
def button_click(letter):
    global row, col
    
    if col < 5:
        if (gridEntries[row][col].get() == ""):
            gridEntries[row][col].insert(0, letter)
            
    
def create_buttons(window):
    global keyboard
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    keyboard = Frame(window)
    keyboard['bg'] = "#222222"
    keyboard.pack(padx=10, pady=10)    
    
    for i, letter in enumerate(alphabet):
        button = Button(keyboard, 
                        bd = 0,
                        text=letter, 
                        width=5, 
                        height=2, 
                        command=lambda l=letter: button_click(l))
        button.grid(row=i // 7, column=i % 7, padx=5, pady=5)
        keyboardEntries[i] = button
        
    enterButton = Button(keyboard, 
                        bd = 0,
                        text="Enter", 
                        width=5, 
                        height=2, 
                        command=lambda l=letter: enter_button(window))
    enterButton.grid(row = 3, column = 5, padx=5, pady=5)
    keyboardEntries[26] = enterButton
    
    backButton = Button(keyboard, 
                        bd = 0,
                        text="<-", 
                        width=5, 
                        height=2, 
                        command=lambda l=letter: backspace_button())
    backButton.grid(row = 3, column = 6, padx=5, pady=5)
    keyboardEntries[27] = backButton
    
def enter_button(window):
    global row, col

    if col == 5:
        if not validate_word():
            invalid_word_popup(window)
            return
        if row < 6:
            check_row(row, window)
            row += 1
            if row == 6:
                end_game("lose", window)
            col = 0
            enable_entry(row, col)
            
def backspace_button():
    global row, col
    
    if col > 0:
        if col < 5:
            disable_entry(row, col)
        col -= 1
        enable_entry(row, col)
        delete_entry(row, col)

def create_letterbox(window):
    grid = Frame(window)
    grid['bg'] = "#222222"
    grid.pack(padx = (0, 0))
    grid.pack(pady = (50, 0))
    
    vcmd = (window.register(validate_entry), "%P")
    
    for x in range(6):
        for y in range(5):
            entry = Entry(grid,
                        width = 2,
                        bg = "#222222",
                        fg = "#FFFFFF",
                        font=("Arial", 36),
                        insertwidth = 0,
                        insertbackground = "#222222",
                        relief = "solid",
                        highlightthickness = 5,
                        highlightbackground = "grey",
                        justify = "center",
                        validate="key",
                        validatecommand = vcmd)            
            entry.grid(row = x, column = y, padx = 10, pady = 10)
            entry.bind("<BackSpace>", lambda event, x=x, y=y: detect_backspace(event, x, y))
            entry.bind("<KeyPress>", lambda event, x=x, y=y: upper_case(event, x, y))
            entry.bind("<Return>", lambda event, x=x, y=y: detect_enter(event, x, y, window))
            gridEntries[x][y] = entry
            disable_entry(x, y)
            
def disable_entry(x, y):
    gridEntries[x][y].config(state='disabled', disabledbackground = "#222222", disabledforeground = "#FFFFFF")
    
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
    
    random_number = random.randint(0, 14855)
    
    with open("5-letter_words.txt", "r") as file:
        for lineNum, line in enumerate(file):
            if lineNum == random_number:
                word = line.strip().upper()
                break
            
def validate_word():
    userWord = ""
    
    for y in range(5):
        userWord += gridEntries[row][y].get()
        
    with open("5-letter_words.txt", "r") as file:
        for lineNum, line in enumerate(file):
            if line.strip().upper() == userWord:
                return True
    return False

def detect_backspace(event, x, y):
    global row
    global col
    
    if col > 0:
        if col < 5:
            disable_entry(row, col)
        col -= 1
        enable_entry(row, col)
        delete_entry(row, col)
        
def invalid_word_popup(window):
    popup = Toplevel(window)
    popup.title("Invalid Word")
    
    popup_width = 300
    popup_height = 100
    
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()

    positionX = int(screenWidth /2 - popup_width/2)
    positionY = int(screenHeight / 4 - popup_height/2)
    
    popup.geometry(f"{popup_width}x{popup_height}+{positionX}+{positionY}")
    
    label = Label(popup, text="Invalid word! Please try again.", font=("Arial", 12))
    label.pack(pady=20)
    popup.after(500, popup.destroy)
    
def detect_enter(event, x, y, window):
    global row, col
    
    if col == 5:
        if not validate_word():
            invalid_word_popup(window)
            return
        if row < 6:
            check_row(row, window)
            row += 1
            if row == 6:
                end_game("lose", window)
            col = 0
            enable_entry(row, col)
            
def check_row(row, window):
    global word
    
    userLetters = [0] * 5
    userWord = ""
    
    for y in range(5):
        letter = gridEntries[row][y].get()
        if letter == word[y]:
            userLetters[y] = 1
            gridEntries[row][y].config(disabledbackground = "#008000")
            for keybtn in keyboardEntries:
                if keybtn["text"] == letter:
                    keybtn.config(bg = "#008000")
            
    for y in range(5):
        letter = gridEntries[row][y].get()
        if letter != word[y] and letter in word:
            for i in range(5):
                if word[i] == letter and userLetters[i] == 0:
                    userLetters[i] = 1  
                    gridEntries[row][y].config(disabledbackground = "#FFBF00")
                    for keybtn in keyboardEntries:
                        if keybtn["text"] == letter:
                            keybtn.config(bg = "#FFBF00")
                            
    for y in range(5):
        letter = gridEntries[row][y].get()
        if letter not in word:
            for keybtn in keyboardEntries:
                if keybtn["text"] == letter:
                    keybtn.config(bg = "#5A5A5A")
            
    for y in range(5):
        userWord += gridEntries[row][y].get()
        
    if (userWord == word):
        end_game("win", window)
    
def end_game(status, window):
    global word
    
    msg = ""
    
    if status == "win":
        msg = "Congratulations you have won"
    elif status == "lose":
        msg = "The word was " + word
        
    popup = Toplevel(window)
    popup.title("Game Over")
    
    popup_width = 500
    popup_height = 200
    
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()

    positionX = int(screenWidth / 2 - popup_width/2)
    positionY = int(screenHeight / 2 - popup_height/2)
    
    popup.geometry(f"{popup_width}x{popup_height}+{positionX}+{positionY}")
    
    label = Label(popup, text = msg, font=("Arial", 12))
    label.pack(pady=20)
    
    def restart_game():
        global gameActive
        
        gameActive = False
        popup.destroy()
        window.quit()
        window.destroy()
        main()
        
    def exit_game():
        popup.destroy()
        window.quit()
        sys.exit()
    
    playAgainBTN = Button(popup, text="Play Again", command = restart_game, width = 15, height = 2)
    playAgainBTN.pack(side=LEFT, padx=20, pady=10)
    
    exitBTN = Button(popup, text = "Exit", command = exit_game, width = 15, height = 2)
    exitBTN.pack(side = RIGHT, padx = 20, pady = 10)
    
    
def upper_case(event, x, y):
    gridEntries[x][y].delete(0, END)
    char = event.char.upper()
    
    if char.isalpha():
        event.widget.insert(0, char)
    return "break"
    

def create_window():
    window = Tk()
    window.title("Wordle")
    window['bg'] = "#222222"
    
    windowWidth = 600
    windowHeight = 800
    
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()

    positionX = int(screenWidth/2 - windowWidth/2)
    positionY = int(screenHeight/2 - windowHeight/2)

    window.geometry(f"{windowWidth}x{windowHeight}+{positionX}+{positionY}")
    
    return window
    
def main():
    initialise_variables()
    
    window = create_window()
    
    create_letterbox(window)
    
    create_buttons(window)
    
    generate_word()
    
    global word
    print(word)
    
    start_gameloop(window)
        
    window.mainloop()
    
if __name__ == "__main__":
    main()