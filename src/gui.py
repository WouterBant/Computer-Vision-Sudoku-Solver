import tkinter as tk
from test import solve
from generate import generate_puzzle


# Create a function to validate the user's input
def validate_input(row, col, value):
    print(solution[row][col] == value)
    return solution[row][col] == value

# Create a function to handle button click event
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
    # Create the GUI
    root = tk.Tk()
    root.title("Sudoku Solver")

    # Create a frame for the Sudoku grid
    grid_frame = tk.Frame(root)
    grid_frame.pack()

    # Create buttons for each cell in the Sudoku puzzle
    entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            value = puzzle[i][j]
            entry = tk.Entry(grid_frame, width=3, justify="center", font=("Arial", 20))
            if value != 0:
                entry.insert(tk.END, str(value))
            entry.grid(row=i, column=j, padx=2, pady=2, ipady=5)  # Add padding around each entry
            entry.bind('<FocusOut>', lambda event, row=i, col=j, entry=entry: on_button_click(row, col, entry))
            row_entries.append(entry)

        entries.append(row_entries)

    # Create the Solve button
    solve_button = tk.Button(root, text="Solve", command=solve(puzzle), font=("Arial", 16))
    solve_button.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    solution, puzzle = generate_puzzle()
    main()