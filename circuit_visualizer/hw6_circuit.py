"""
15-110 Hw6 - Circuit Simulator Project
Name: Tiffany Han
AndrewID: tianhui2
"""

import hw6_circuit_tests as test

project = "Circuit"

#### CHECK-IN 1 ####

"""
findMatchingParen(expr, index)
#1 [Check6-1]
Parameters: str ; int
Returns: int
"""


def findMatchingParen(expr, index):
    open_count = 0
    for i, c in enumerate(expr[index:]):
        if c == "(":
            open_count += 1
        if c == ")":
            open_count -= 1
        if open_count == 0:
            return i + index
    # open_count = 0
    # close_count = 0
    # for i in range(len(expr[index:])):
    #     if expr[index:][i] == "(":
    #         open_count += 1
    #     if expr[index:][i] == ")":
    #         close_count += 1
    #     if open_count == close_count:
    #         return i + index


"""
getTokenBounds(expr, start)
#2 [Check6-1]
Parameters: str ; int
Returns: list of ints
"""


def getTokenBounds(expr, start):
    while expr[start] == " ":
        start += 1
    end = start
    while end < len(expr) and expr[end] != " ":
        end += 1
    return [start, end - 1]

    # ran = []
    # for i in range(start, len(expr)):
    #     if expr[i] != " " and len(ran) < 1:
    #         ran.append(i)
    #     if expr[i] == " " and len(ran) == 1:
    #         ran.append(i - 1)
    #     if i == len(expr) - 1 and len(ran) < 2:
    #         ran.append(i)
    # return ran


"""
parseExpr(expr)
#3 [Check6-1]
Parameters: str
Returns: tree of strs
"""


def parseExpr(expr):
    expr = expr.strip()
    # (X and Y)-> X and Y
    if expr[0] == "(":
        end = findMatchingParen(expr, 0)
        if end == len(expr) - 1:
            return parseExpr(expr[1 : len(expr) - 1])
    # "Y"
    if " " not in expr:
        return {"contents": expr, "children": []}
    # "(NOT X) AND Y"
    if (expr[0:3]).upper() == "NOT":
        return {"contents": "NOT", "children": [parseExpr(expr[3:])]}
    else:
        if expr[0] == "(":
            close = findMatchingParen(expr, 0)
        else:
            left_bounds = getTokenBounds(expr, 0)
            close = left_bounds[1]
        left_expr = expr[0 : close + 1]
        operator = getTokenBounds(expr, close + 1)
        right_expr = expr[operator[1] + 1 :]
        return {
            "contents": expr[operator[0] : operator[1] + 1],
            "children": [parseExpr(left_expr), parseExpr(right_expr)],
        }


"""
validateTree(t)
#4 [Check6-1]
Parameters: tree of strs
Returns: bool
"""


def validateTree(t):
    operators = ["AND", "OR", "XOR"]
    # That's an empty tree
    if t == {}:
        return False
    # At the end of the tree (a variable) and its not a token
    if t["children"] == [] and (t["contents"] not in operators):
        return True
    # Have children means it's an operator
    # But if it's not any of the recognized operators
    # And it's not "NOT", then it's wrong -> (A HAHA B)  -> FALSE
    if t["children"] != [] and (
        ((t["contents"]).upper() not in operators) and (t["contents"]).upper() != "NOT"
    ):
        return False
    else:
        # Check if it has nodes called children and contents.
        for key in t:
            if (
                key != "children" and key != "contents" and key != "powered"
            ):  # Later modified
                return False
        # If it's an operator, then there should be two children
        if (t["contents"]).upper() in operators:
            if len(t["children"]) != 2:
                operator = t["contents"]
                print(f"Please check the variables connected by operator {operator} ")
                return False
        # One child if it's "NOT"
        if t["contents"] == "NOT":
            if len(t["children"]) != 1:
                return False
        for child in t["children"]:
            return validateTree(child)


"""
runWeek1()
#5 [Check6-1]
Parameters: no parameters
Returns: None
"""


def runWeek1():
    bool_expr = input("Input you boolean expression:")
    # try:
    #     unvalidated_t = parseExpr(bool_expr)
    #     validated_t = validateTree(unvalidated_t)
    #     if validated_t:
    #         print(unvalidated_t)
    #     else:
    #         print("the expression you entered was invalid, try again.")
    #         runWeek1()
    # except:
    #     print("the expression you entered was invalid, try again.")
    #     runWeek1()
    try:
        init_tree = parseExpr(bool_expr)
    except:
        runWeek1()
        print("the expression you entered was invalid, try again.")
    else:
        if validateTree(init_tree):
            print(init_tree)
        else:
            print("Invalid tree!")


#### CHECK-IN 2 ####

"""
getLeaves(t)
#1 [Check6-2]
Parameters: tree of strs
Returns: list of strs
"""


def getLeaves(t):
    if t["children"] == []:
        return [t["contents"]]
    else:
        res = []
        for child in t["children"]:
            for i in getLeaves(child):
                if i not in res:
                    res += [i]
        res.sort()
        return res


"""
generateAllInputs(n)
#2 [Check6-2]
Parameters: int
Returns: 2D list of bools
"""


def generateAllInputs(n: int):
    if n == 0:
        return [[]]
    else:
        res = []
        for lst in generateAllInputs(n - 1):
            res += [[False] + lst]
            res += [[True] + lst]
        return res


"""
evalTree(t, inputs)
#3 [Check6-2] & #4 [Hw6]
Parameters: tree of strs ; dict mapping strs to bools
Returns: bool
"""


def evalTree(t: dict, inputs: dict):
    if t["children"] == []:
        t["powered"] = inputs[t["contents"]]
        return inputs[t["contents"]]
    else:
        children = []
        for child in t["children"]:
            children.append(evalTree(child, inputs))
        if t["contents"].upper() == "AND":
            t["powered"] = children[0] and children[1]
            return children[0] and children[1]
        if t["contents"].upper() == "OR":
            t["powered"] = children[0] or children[1]
            return children[0] or children[1]
        if t["contents"].upper() == "NOT":
            t["powered"] = not children[0]
            return not children[0]
        if t["contents"].upper() == "XOR":
            t["powered"] = children[0] != children[1]
            return children[0] != children[1]


"""
makeTruthTable(tree)
#4 [Check6-2]
Parameters: tree of strs
Returns: None
"""


def makeTruthTable(tree):
    text = []
    variables = getLeaves(tree)
    inputs = generateAllInputs(len(variables))
    print(" | ".join(variables), " |", "Out")
    var_text = " | ".join(variables) + " | " + "Out"
    text.append(var_text)
    for ip in inputs:
        d = {}
        bi = ["1" if val else "0" for val in ip]
        for i in range(len(ip)):
            d[variables[i]] = ip[i]
        res = evalTreeforTruthTable(tree, d)
        r = 0
        if res:
            r = 1
        tab_line = " | ".join(bi) + " | " + str(r)
        text.append(tab_line)
        print(" | ".join(bi), " |", r)
    return text


def evalTreeforTruthTable(t: dict, inputs: dict):
    if t["children"] == []:
        return inputs[t["contents"]]
    else:
        children = []
        for child in t["children"]:
            children.append(evalTreeforTruthTable(child, inputs))
        if t["contents"].upper() == "AND":
            return children[0] and children[1]
        if t["contents"].upper() == "OR":
            return children[0] or children[1]
        if t["contents"].upper() == "NOT":
            return not children[0]
        if t["contents"].upper() == "XOR":
            return children[0] != children[1]


"""
runWeek2()
#5 [Check6-2]
Parameters: no parameters
Returns: None
"""


def runWeek2():
    bool_expr = input("Input you boolean expression:")
    try:
        t = parseExpr(bool_expr)
        validated_t = validateTree(t)
        if validated_t:
            makeTruthTable(t)
        else:
            print("the expression you entered was invalid, try again.")
            runWeek2()
    except:
        print("the expression you entered was invalid, try again.")


### WEEK 3 ###

"""
makeModel(data)
#2 [Hw6]
Parameters: dict mapping strs to values
Returns: None
"""


def makeModel(data: dict):
    data["expression"] = ""
    data["tree"] = None
    data["inputs"] = []
    # ignore the below line
    # it's for showing the truth table on tkinter
    data["showtt"] = False


"""
makeView(data, canvas)
#2 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
"""


def makeView(data, canvas):
    expr = "Expression: " + data["expression"]
    canvas.create_text(30, 620, text=expr, anchor=W)
    canvas.create_text(30, 637, text="(type * to display truth table)", anchor=W)
    if data["tree"] != None:
        drawCircuit(data, canvas)
    if data["showtt"]:
        if validateTree(data["tree"]):
            text = makeTruthTable(data["tree"])
            show_table(canvas, 500, 20, text)


def show_table(canvas, x1, y1, text: list):
    for line in text:
        canvas.create_text(x1, y1, text=line, anchor=W)
        y1 += 15


"""
keyPressed(data, event)
#2 [Hw6]
Parameters: dict mapping strs to values ; key event object
Returns: None
"""


def keyPressed(data, event):
    if event.keysym == "BackSpace":
        if len(data["expression"]) >= 1:
            data["expression"] = data["expression"].rstrip(data["expression"][-1])
    elif event.keysym == "Return":
        try:
            print(data["expression"])
            data["tree"] = parseExpr(data["expression"].strip())
            print(data["tree"])
        except:
            print("Please input a valid expression2")
        if validateTree(data["tree"]):
            runInitialCircuit(
                data
            )  # This should really specify data... not data["tree"]
        else:
            print("Please input a valid expression1")
    elif event.keysym == "Tab":
        if validateTree(data["tree"]):
            makeTruthTable(data["tree"])
        else:
            print("Please input a valid expression3")
    elif event.keysym == "asterisk":
        data["showtt"] = not data["showtt"]
    else:
        data["expression"] += str(event.char)


"""
mousePressed(data, event)
#4 [Hw6]
Parameters: dict mapping strs to values ; mouse event object
Returns: None
"""


def mousePressed(data, event):
    for inp in data[
        "inputs"
    ]:  # It would really help if data["inputLocations"] had an example...
        if (
            data["inputLocations"][inp]["left"]
            < event.x
            < data["inputLocations"][inp]["right"]
        ):
            if (
                data["inputLocations"][inp]["top"]
                < event.y
                < data["inputLocations"][inp]["bottom"]
            ):
                data["inputs"][inp] = not data["inputs"][inp]
    data["output"] = evalTree(data["tree"], data["inputs"])


"""
runInitialCircuit(data)
#2 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values
Returns: None
"""


def runInitialCircuit(data):
    inputs = {}
    inp_lst = getLeaves(data["tree"])
    for var in inp_lst:
        inputs[var] = False
    data["inputs"] = inputs
    data["outputs"] = evalTree(data["tree"], data["inputs"])


"""
drawNode(canvas, value, x, y, size, lit)
#3 [Hw6]
Parameters: Tkinter canvas ; str ; int ; int ; int ; bool
Returns: None
"""


def drawNode(canvas, value: str, x, y, size, lit: bool):

    canvas.create_rectangle(
        x - size // 2,
        y - size // 2,
        x + size // 2,
        y + size // 2,
        fill="yellow" if lit else "white",
    )
    canvas.create_text(x, y, text=value)


"""
drawWire(canvas, x1, y1, x2, y2, lit)
#3 [Hw6]
Parameters: Tkinter canvas ; int ; int ; int ; int ; bool
Returns: None
"""


def drawWire(canvas, x1, y1, x2, y2, lit):
    canvas.create_line(
        x1,
        y1,
        x2,
        y2,
        fill="yellow" if lit else "black",
    )


#### WEEK 3 PROVIDED CODE ####

""" getTreeDepth() finds the depth of the tree, the max length from root to leaf """


def getTreeDepth(t):
    if len(t["children"]) == 0:
        return 0
    max = 0
    for child in t["children"]:
        tmp = getTreeDepth(child)
        if tmp > max:
            max = tmp
    return max + 1


""" getTreeWidth() finds the width of the tree, the max number of nodes on the same level """


def getTreeWidth(t):
    if len(t["children"]) == 0:
        return 0
    elif len(t["children"]) == 1:
        return max(1, getTreeWidth(t["children"][0]))
    else:
        biggestChildSize = max(
            getTreeWidth(t["children"][0]), getTreeWidth(t["children"][1])
        )
        return max(1, 2 * biggestChildSize)


""" This function draws all the inputs of the circuit. They should all go on
    the left side of the screen. """


def drawInputs(data, canvas, size):
    """We'll track the locations of inputs for button-pressing later on"""
    if "inputLocations" not in data:
        data["inputLocations"] = {}
    keys = list(data["inputs"].keys())
    keys.sort()

    # make the inputs centered on the Y axis
    margin = (600 - (len(keys) * size)) / 2
    centerX = size / 2
    for i in range(len(keys)):
        var = keys[i]
        if var not in data["inputLocations"]:
            data["inputLocations"][var] = {}
        inp = data["inputLocations"][var]
        centerY = size * i + size / 2 + margin
        # Store the location so we can use it to click buttons later on
        inp["left"] = centerX - size / 2
        inp["top"] = centerY - size / 2
        inp["right"] = centerX + size / 2
        inp["bottom"] = centerY + size / 2
        drawNode(canvas, var, centerX, centerY, size / 2, data["inputs"][var])


""" This function draws a circuit tree within the specified bounding box.
    It returns the location where the node was drawn, to make drawing wires easier. """


def drawTree(data, canvas, t, size, left, top, right, bottom):
    if "powered" not in t:
        t["powered"] = False
    centerX = (left + right) / 2
    centerY = (top + bottom) / 2
    # Don't draw the leaves- they're all on the left side of the screen!
    if len(t["children"]) == 0:
        var = t["contents"]
        d = data["inputLocations"][var]
        # Instead, return the location of the leaf, to make drawing wires easier.
        return [
            (d["left"] + d["right"]) / 2 + size / 4,
            (d["top"] + d["bottom"]) / 2,
            data["inputs"][var],
        ]
    elif len(t["children"]) == 1:
        drawNode(canvas, t["contents"], centerX, centerY, size / 2, t["powered"])
        # Position the child at the same Y position, but to the left
        [childX, childY, childOn] = drawTree(
            data, canvas, t["children"][0], size, left - size, top, right - size, bottom
        )
        drawWire(canvas, childX, childY, centerX - size / 4, centerY, childOn)
        return [centerX + size / 4, centerY, t["powered"]]
    else:
        drawNode(canvas, t["contents"], centerX, centerY, size / 2, t["powered"])
        # Split the Y dimension in half, and give each to one child.
        # Left child
        [childX, childY, childOn] = drawTree(
            data,
            canvas,
            t["children"][0],
            size,
            left - size,
            top,
            right - size,
            centerY,
        )
        drawWire(canvas, childX, childY, centerX - size / 4, centerY, childOn)

        # Right child
        [childX, childY, childOn] = drawTree(
            data,
            canvas,
            t["children"][1],
            size,
            left - size,
            centerY,
            right - size,
            bottom,
        )
        drawWire(canvas, childX, childY, centerX - size / 4, centerY, childOn)
        return [centerX + size / 4, centerY, t["powered"]]


""" This function draws the entire circuit. It first determines the size of each
    circuit node by measuring the width/height of the tree. Then it draws the
    inputs and outputs. Then it recursively draws the circuit tree. """


def drawCircuit(data, canvas):
    t = data["tree"]
    if "output" not in data:
        data["output"] = False
    depth = 2 + getTreeDepth(t)
    width = max(1, len(data["inputs"]), getTreeWidth(t))
    size = 600 / max(depth, width)

    drawInputs(data, canvas, size)

    outLeft, outRight = 600 - size, 600
    outTop, outBottom = 0, 600
    outX, outY = (outLeft + outRight) / 2, (outTop + outBottom) / 2
    drawNode(canvas, "Out", outX, outY, size / 2, data["output"])

    [childX, childY, childOn] = drawTree(
        data, canvas, t, size, outLeft - size, outTop, outRight - size, outBottom
    )
    drawWire(canvas, childX, childY, outLeft + size / 4, outY, childOn)


#### SIMULATION STARTER CODE ###

from tkinter import *


def keyEventHandler(data, canvas, event):
    if event.keysym == "Return":
        # Clear previous data, if it exists
        if "inputLocations" in data:
            del data["inputLocations"]
    keyPressed(data, event)

    canvas.delete(ALL)
    makeView(data, canvas)
    canvas.update()


def mouseEventHandler(data, canvas, event):
    mousePressed(data, event)

    canvas.delete(ALL)
    makeView(data, canvas)
    canvas.update()


def runSimulation(w, h):
    data = {}
    makeModel(data)

    root = Tk()
    canvas = Canvas(root, width=w, height=h)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    makeView(data, canvas)

    root.bind("<Key>", lambda event: keyEventHandler(data, canvas, event))
    root.bind("<Button-1>", lambda event: mouseEventHandler(data, canvas, event))

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#" * 15 + " WEEK 1 TESTS " + "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#" * 15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # runWeek1()

    ## Uncomment these for Week 2 ##

    # print("\n" + "#" * 15 + " WEEK 2 TESTS " + "#" * 16 + "\n")
    # test.week2Tests()
    # print("\n" + "#" * 15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    # runWeek2()

    # ## Uncomment these for Week 3 ##
    print("\n" + "#" * 5 + " NO WEEK 3 OUTPUT - SEE SIMULATION " + "#" * 5 + "\n")
    ## Finally, run the simulation to test it manually ##
    runSimulation(600, 650)
