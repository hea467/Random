import tkinter as tk
from tkinter.constants import ALL
import copy

board = [
    [5, 3, 0, 0, 7, 0, 9, 0, 0],
    [6, 0, 0, 1, 0, 5, 0, 0, 0],
    [1, 9, 8, 3, 4, 0, 5, 0, 7],
    [8, 5, 0, 7, 0, 0, 0, 0, 3],
    [4, 0, 6, 0, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

# Really long time...
# board = [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9],
# ]

# board = [[0 for j in range(9)] for i in range(9)]
ori_board = copy.deepcopy(board)

order = []


line_space = 540 // 9


def makegrid(canvas, width, height):
    for i in range(10):
        canvas.create_line(
            5 + (i * (line_space)),
            5,
            5 + (i * (line_space)),
            width - 5,
            width=3 if i % 3 == 0 else 1,
        )
        canvas.create_line(
            5,
            5 + (i * (line_space)),
            height - 5,
            5 + (i * (line_space)),
            width=3 if i % 3 == 0 else 1,
        )


def fillboard(canvas, board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] != 0:
                x1 = line_space * col + 5 + line_space // 2
                y1 = line_space * row + 5 + line_space // 2
                canvas.create_text(
                    x1, y1, text=str(board[row][col]), font=("Times", "20", "bold")
                )


def check_horizontal(board, location: tuple, curr):
    for val in board[location[0]]:
        if val == curr:
            return False
    return True


def check_vertical(board, location: tuple, curr):
    for rows in board:
        if rows[location[1]] == curr:
            return False
    return True


def check_square(board, location: tuple, curr):
    small_square = []
    x = location[0] // 3
    y = location[1] // 3
    for i in range(x * 3, x * 3 + 3):
        small_square.append(board[i][y * 3 : y * 3 + 3])
    for j in [0, 1, -1]:
        for k in [0, 1, -1]:
            if small_square[j][k] == curr:
                return False
    return True


def valid(row, col, num):
    return (
        check_horizontal(board, (row, col), num)
        and check_vertical(board, (row, col), num)
        and check_square(board, (row, col), num)
    )


def solveboard(board, row, col):
    if (row, col) == (9, 0):
        return True
    # Empty spot
    if board[row][col] == 0:
        for num in range(1, 10):
            order.append([(row, col), num])
            # Loop thru 1-9 at (row, col)
            if valid(row, col, num):  # If that number is valid at that location
                board[row][col] = num
                # Set that location to that number
                # Now check the next location
                if col == 8:  # If it's at the end of the row
                    # Call function on the next row, first spot
                    if solveboard(board, row + 1, 0):
                        return True
                else:
                    # Call the next location in row
                    if solveboard(board, row, col + 1):
                        return True
                board[row][col] = 0
    else:  # If the spot has already been filled
        # Call the next one
        if col == 8:
            return solveboard(board, row + 1, 0)
        else:
            return solveboard(board, row, col + 1)
    return False


solveboard(board, 0, 0)

##########################################


def make_view(canvas, order: list):
    if order:
        tmp = order.pop(0)
        y1 = tmp[0][0] * 60 + 5
        x1 = tmp[0][1] * 60 + 5
        canvas.create_rectangle(x1, y1, x1 + 60, y1 + 60, fill="skyblue")
        canvas.create_text(x1 + 30, y1 + 30, text=tmp[1])


def time_loop(canvas, time_rate: int):
    make_view(canvas, order)
    canvas.update()
    canvas.after(time_rate, time_loop, canvas, time_rate)


def makeCanvas(width, height, time_rate: int):

    root = tk.Tk()
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    makegrid(canvas, width, height)
    fillboard(canvas, ori_board)
    make_view(canvas, order)
    canvas.after(time_rate, time_loop, canvas, time_rate)

    root.mainloop()


makeCanvas(550, 550, 10)
print(board)
