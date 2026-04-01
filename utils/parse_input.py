from model.board import FutoshikiData

def parse_input_file(file_path) -> FutoshikiData:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [
            l.split('#')[0].strip()
            for l in f.readlines()
            if l.split('#')[0].strip()
        ]

    if len(lines) == 0:
        raise ValueError("File rỗng")

    N = int(lines[0])

    expected_lines = 1 + N + N + (N - 1)
    if len(lines) < expected_lines:
        raise ValueError("File không đủ dữ liệu")

    data = FutoshikiData(N)

    # GRID
    for i in range(N):
        row = [int(x.strip()) for x in lines[i + 1].split(',')]
        data.grid[i] = row

    # HORIZONTAL
    for i in range(N):
        row = [int(x.strip()) for x in lines[N + 1 + i].split(',')]
        data.h_constraints.append(row)

    # VERTICAL
    for i in range(N - 1):
        row = [int(x.strip()) for x in lines[2 * N + 1 + i].split(',')]
        data.v_constraints.append(row)

    return data