text = """
>|<\.
.v.^.
.v.^.
<->|.
.\</.
"""[1:-1]



illuminate = True

matrix = [list(row) for row in text.split('\n')]

rows = len(matrix)
cols = len(matrix[0])
out = "\\begin{tikzpicture}\n"
nodes = ""
fills = ""
for i in range(rows):
    for j in range(cols):
        symbol = matrix[-i - 1][j]
        if symbol == '|':
            symbol = "\\textbar"
        elif symbol == 'S':
            symbol = "\\textbf{S}"
        elif symbol == '\\':
            symbol = "\\textbackslash"
        elif symbol == '<':
            symbol = "$<$"
        elif symbol == '>':
            symbol = "$>$"
        elif symbol == '^':
            symbol = "$\\wedge$"
        elif symbol == 'v':
            symbol = "$\\vee$"
        if illuminate and symbol != ".":
            fills += f"\\fill[gray!40] ({j},{i}) rectangle ({j+1},{i+1});\n"
        nodes += f"\\node at ({j+0.5}, {i+0.5})" + "{" + symbol + "};\n"
out += fills + nodes + "\draw[step=1cm, gray, very thin] (0,0) grid (" + str(rows) + "," + str(cols) + ");\n" + "\\end{tikzpicture}"

f = open("output.txt", "w")
f.write(out)