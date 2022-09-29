import tkinter as tk

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

line_space = 540 // 9


def makegrid(canvas, width, height):
    for i in range(10):
        canvas.create_line(
            5 + (i * (line_space)),
            5,
            5 + (i * (line_space)),
            545,
            width=3 if i % 3 == 0 else 1,
        )
        canvas.create_line(
            5,
            5 + (i * (line_space)),
            545,
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


def not_empty(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    return False


def solveboard(board):
    if not not_empty(board):
        return True
    else:
        row, col = not_empty(board)[0], not_empty(board)[1]
        for num in range(1, 10):
            if (
                check_horizontal(board, (row, col), num)
                and check_vertical(board, (row, col), num)
                and check_square(board, (row, col), num)
            ):
                board[row][col] = num
                if solveboard(board):
                    return True
                board[row][col] = 0
    return False


def makeCanvas(width, height):
    root = tk.Tk()
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    makegrid(canvas, width, height)
    fillboard(canvas, board)

    root.mainloop()


makeCanvas(550, 550)
