
import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

def toggle(cell):
    return "🌞" if cell == "🌚" else "🌚"

def press(row, col, record=True):
    global moves
    for r, c in [(row, col), (row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        if 0 <= r < 5 and 0 <= c < 5:
            grid[r][c] = toggle(grid[r][c])
            buttons[r][c].config(
                text=grid[r][c],
                fg="gold" if grid[r][c] == "🌞" else "white",
                bg="#333333"
            )
    if record:
        moves += 1
        move_label.config(text=f"Moves: {moves}")
    if do_you_win() and record:
        messagebox.showinfo("🎉 You Win!", f"😎 Bravo! You won in {moves} moves.")
        restart_game()

def do_you_win():
    return all(cell == "🌚" for row in grid for cell in row)

def restart_game():
    global grid, moves
    moves = 0
    move_label.config(text="Moves: 0")
    grid = [["🌚" for _ in range(5)] for _ in range(5)]
    presses = [(random.randint(0, 4), random.randint(0, 4)) for _ in range(10)]
    for r, c in presses:
        press(r, c, record=False)
    for i in range(5):
        for j in range(5):
            buttons[i][j].config(text="🌚", fg="white", bg="#333333")

def grid_to_string(g):
    return sum(
        (1 << (5 * i + j)) if g[i][j] == "🌞" else 0
        for i in range(5) for j in range(5)
    )

def apply_press_to_string(mask, row, col):
    for r, c in [(row, col), (row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        if 0 <= r < 5 and 0 <= c < 5:
            mask ^= (1 << (5 * r + c))
    return mask

def show_solution():
    current_state = [row.copy() for row in grid]
    start_mask = grid_to_string(current_state)

    queue = deque([(start_mask, [])])
    visited = set([start_mask])

    solution = None
    while queue:
        state, path = queue.popleft()
        if state == 0:
            solution = path
            break
        for i in range(5):
            for j in range(5):
                new_state = apply_press_to_string(state, i, j)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [(i, j)]))

    if not solution:
        messagebox.showwarning("❌ No Solution", "This puzzle is unsolvable.")
        return

    for i in range(5):
        for j in range(5):
            buttons[i][j].config(bg="#333333", text=grid[i][j])

    for index, (r, c) in enumerate(solution):
        buttons[r][c].config(bg="#2277FF", text=str(index + 1))

    steps = "\n".join([f"({r+1}, {c+1})" for r, c in solution])
    messagebox.showinfo("💡 Solution", f"Press these {len(solution)} cells (blue):\n\n{steps}")

root = tk.Tk()
root.title("🌞🌚 Lights Out Game")
root.configure(bg="#222222")

grid = [["🌚" for _ in range(5)] for _ in range(5)]
buttons = [[None for _ in range(5)] for _ in range(5)]
moves = 0

top_frame = tk.Frame(root, bg="#222222")
top_frame.pack(pady=10)

move_label = tk.Label(top_frame, text="Moves: 0", font=("Arial", 14), fg="white", bg="#222222")
move_label.pack(side="left", padx=10)

restart_button = tk.Button(top_frame, text="🔁 Restart", command=restart_game,
                           bg="#444444", fg="white", activebackground="#666666")
restart_button.pack(side="left", padx=10)

solve_button = tk.Button(top_frame, text="🔍 Show Solution",
                         command=show_solution,
                         bg="#444444", fg="white", activebackground="#666666")
solve_button.pack(side="left", padx=10)

frame = tk.Frame(root, bg="#222222")
frame.pack()

for i in range(5):
    for j in range(5):
        btn = tk.Button(frame, text="🌚", font=("Arial", 20), width=4, height=2,
                        bg="#333333", fg="white", activebackground="#555555",
                        command=lambda r=i, c=j: press(r, c))
        btn.grid(row=i, column=j, padx=2, pady=2)
        buttons[i][j] = btn

restart_game()
root.mainloop()
