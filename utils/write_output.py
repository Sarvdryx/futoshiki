def write_output_file(data, file_path):
    n = data.n
    grid = data.grid
    h = data.h_constraints
    v = data.v_constraints

    with open(file_path, "w", encoding="utf-8") as f:
        for r in range(n):
            # dòng grid + horizontal
            line = ""
            for c in range(n):
                line += str(grid[r][c])

                if c < n - 1:
                    if h[r][c] == 1:
                        line += " < "
                    elif h[r][c] == -1:
                        line += " > "
                    else:
                        line += "   "

            f.write(line + "\n")

            # dòng vertical
            if r < n - 1:
                line = ""
                for c in range(n):
                    if v[r][c] == 1:
                        line += "^"
                    elif v[r][c] == -1:
                        line += "v"
                    else:
                        line += " "

                    if c < n - 1:
                        line += "   "

                f.write(line + "\n")