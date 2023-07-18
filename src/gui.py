import tkinter as tk
from generate import generate_puzzle


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


def on_button_click(row, col, button):
    value = button.get()
    if value:
        value = int(button.get())
        if validate_input(row, col, value):
            puzzle[row][col] = value
            button.config(foreground="black")
        else:
            button.config(foreground="red")
    else:
        print("Not entered a number")


def main():
    root = tk.Tk()
    root.title("Sudoku Solver")

    grid_frame = tk.Frame(root)
    grid_frame.pack()

    global entries
    entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            value = puzzle[i][j]
            back_col = "lightgrey" if ((i//3) + (j//3)) % 2 else "white"
            entry = tk.Entry(grid_frame, width=3, justify="center", font=("Arial", 20), bg=back_col, bd=1.5)
            if value != 0:
                entry.insert(tk.END, str(value))
            entry.grid(row=i, column=j, padx=0, pady=0, ipady=5)
            entry.bind('<FocusOut>', lambda event, row=i, col=j, entry=entry: on_button_click(row, col, entry))
            row_entries.append(entry)

        entries.append(row_entries)

    solve_button = tk.Button(root, text="Solve", command=solve_puzzle, font=("Arial", 16))
    solve_button.pack(pady=10)

    reset_button = tk.Button(root, text="reset", command=reset_puzzle, font=("Arial", 16))
    reset_button.pack(pady=10)

    new_button = tk.Button(root, text="new", command=new_puzzle, font=("Arial", 16))
    new_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    solution, puzzle = generate_puzzle()
    main()
