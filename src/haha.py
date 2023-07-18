import tkinter as tk

root = tk.Tk()

grid_frame = tk.Frame(root)
grid_frame.pack()

canvas_frame = tk.Frame(grid_frame)
canvas_frame.pack()

# Add a canvas widget inside the canvas_frame
canvas = tk.Canvas(canvas_frame, width=400, height=300)
canvas.pack()

# Draw horizontal lines
for i in range(10):
    y = i * 30  # Adjust the spacing between lines if needed
    canvas.create_line(0, y, 400, y, fill="black")

# Draw vertical lines
for i in range(11):
    x = i * 40  # Adjust the spacing between lines if needed
    canvas.create_line(x, 0, x, 300, fill="black")

root.mainloop()
