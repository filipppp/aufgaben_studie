text = """
.|F7.
LFJ|.
SJ.L7
|F--J
LJ.L.
"""[1:-1]

matrix = [list(row) for row in text.split('\n')]

rows = len(matrix)
cols = len(matrix[0])
out = "\\begin{tikzpicture}\n\draw[step=1cm, gray, very thin] (0,0) grid (" + str(rows) + "," + str(cols) + ");\n"
for i in range(rows):
    for j in range(cols):
        symbol = matrix[-i - 1][j]
        if symbol == '|':
            symbol = "\\textbar"
        elif symbol == 'S':
            symbol = "\\textbf{S}"
        out += f"\\node at ({j+0.5}, {i+0.5})" + "{" + symbol + "};\n"
out += "\\end{tikzpicture}"

f = open("output.txt", "w")
f.write(out)