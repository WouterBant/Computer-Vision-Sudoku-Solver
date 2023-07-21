import tkinter as tk
from tkinter import ttk
from src.generate import generate_puzzle
from src.camera import take_picture
from functools import partial



def validate_input(row, col, value):
    return solution[row][col] == value


def solve_puzzle():
    global entries
    for i in range(9):
        for j in range(9):
            entry = entries[i][j]
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(solution[i][j]))
            entry.config(foreground="black")


def reset_puzzle():
    global entries, puzzle
    for i in range(9):
        for j in range(9):
            entry = entries[i][j]
            entry.delete(0, tk.END)
            value = puzzle[i][j]
            if value != 0:
                entry.insert(tk.END, str(value))
            entry.config(foreground="black")


def new_puzzle():
    global solution, puzzle, entries
    solution, puzzle = generate_puzzle()
    for i in range(9):
        for j in range(9):
            entry = entries[i][j]
            entry.delete(0, tk.END)
            value = puzzle[i][j]
            if value != 0:
                entry.insert(tk.END, str(value))
            entry.config(foreground="black")


def on_button_click(row, col, button):
    value = button.get()
    if value:
        value = int(button.get())
        if validate_input(row, col, value):
            puzzle[row][col] = value
            button.config(foreground="black")
        else:
            button.config(foreground="red")

def on_entry_focus_in(event):
    event.widget.config(bg="#F5F5F5")

def on_entry_focus_out(event, entries_info):
    entry = event.widget
    row, col = entries_info[entry]
    back_col = "lightgrey" if ((row // 3) + (col // 3)) % 2 else "white"
    entry.config(bg=back_col)


def main():
    global solution, puzzle
    solution, puzzle = generate_puzzle()
    root = tk.Tk()
    root.title("Sudoku Solver")

    grid_frame = tk.Frame(root)
    grid_frame.pack()
    entries_info = {} 

    global entries
    entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            value = puzzle[i][j]
            back_col = "lightgrey" if ((i//3) + (j//3)) % 2 else "white"
            entry = tk.Entry(grid_frame, width=3, justify="center", font=("Arial", 20), bg=back_col, bd=1, relief="solid")
            if value != 0:
                entry.insert(tk.END, str(value))
            entry.grid(row=i, column=j, padx=0, pady=0, ipady=5)
            entries_info[entry] = (i, j)    
            # entry.bind('<FocusIn>', on_entry_focus_in)
            entry.bind('<FocusOut>', lambda event, row=i, col=j, entry=entry: on_button_click(row, col, entry))
            # entry.bind('<FocusOut>', lambda event, entries_info=entries_info: on_entry_focus_out(event, entries_info))
            row_entries.append(entry)

        entries.append(row_entries)

    button_frame1 = tk.Frame(root)
    button_frame1.pack(pady=10)

    reset_button = ttk.Button(button_frame1, text="Puzzle", command=reset_puzzle, style="My.TButton")
    reset_button.pack(side="left", padx=5)

    solve_button = ttk.Button(button_frame1, text="Solution", command=solve_puzzle, style="My.TButton")
    solve_button.pack(side="left", padx=5)

    button_frame2 = tk.Frame(root)
    button_frame2.pack(pady=10)

    new_button = ttk.Button(button_frame2, text="Random Puzzle", command=new_puzzle, style="My.TButton")
    new_button.pack(side="left", padx=5)

    # Add the Capture Frames button
    capture_button = ttk.Button(button_frame2, text="From Picture", command=take_picture, style="My.TButton")
    capture_button.pack(side="left", padx=5)

    # Define a custom style for the ttk.Buttons
    style = ttk.Style()
    style.configure("My.TButton", font=("Arial", 16), foreground="black", background="#EAEAEA", borderwidth=0, padding=10)

    root.mainloop()


if __name__ == "__main__":
    main()
