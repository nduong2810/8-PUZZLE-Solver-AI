from Puzzle import Puzzle
GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]
def serialize(state):
    return str(state)
def solve(puzzle: Puzzle):
    stack = [(puzzle.copy(), [])]
    visited = set()
    while stack:
        current, path = stack.pop()
        if current.state == GOAL_STATE:
            return path + [current]
        key = serialize(current.state)
        if key in visited:
            continue
        visited.add(key)
        x0, y0 = current.find_zero()
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x0+dx, y0+dy
            if 0<=nx<3 and 0<=ny<3:
                new_puzzle = current.copy()
                if new_puzzle.move(nx, ny):
                    stack.append((new_puzzle, path+[current]))
    return [] 