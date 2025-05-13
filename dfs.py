from Puzzle import Puzzle
GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]

def serialize(state):
    return tuple(tuple(row) for row in state)

def solve(puzzle: Puzzle, max_depth=40):
    stack = [(puzzle.copy(), [], 0)]  # (trạng thái, đường đi, độ sâu)
    visited = set()
    while stack:
        current, path, depth = stack.pop()
        key = serialize(current.state)
        if key in visited:
            continue
        visited.add(key)
        if current.state == GOAL_STATE:
            return path + [current]
        if depth >= max_depth:
            continue
        x0, y0 = current.find_zero()
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x0+dx, y0+dy
            if 0<=nx<3 and 0<=ny<3:
                new_puzzle = current.copy()
                if new_puzzle.move(nx, ny):
                    new_key = serialize(new_puzzle.state)
                    if new_key not in visited:
                        stack.append((new_puzzle, path+[current], depth+1))
    return None 