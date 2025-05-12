from Puzzle import Puzzle
GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]
def heuristic(state):
    return sum(1 for y in range(3) for x in range(3) if state[y][x] != 0 and state[y][x] != GOAL_STATE[y][x])
def serialize(state):
    return str(state)
def dfs(puzzle, g, bound, path, visited):
    f = g + heuristic(puzzle.state)
    if f > bound:
        return f, None
    if puzzle.state == GOAL_STATE:
        return f, path + [puzzle]
    min_bound = float('inf')
    key = serialize(puzzle.state)
    visited.add(key)
    x0, y0 = puzzle.find_zero()
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x0+dx, y0+dy
        if 0<=nx<3 and 0<=ny<3:
            new_puzzle = puzzle.copy()
            if new_puzzle.move(nx, ny):
                nkey = serialize(new_puzzle.state)
                if nkey not in visited:
                    t, res = dfs(new_puzzle, g+1, bound, path+[puzzle], visited)
                    if res:
                        return t, res
                    if t < min_bound:
                        min_bound = t
    visited.remove(key)
    return min_bound, None
def solve(puzzle: Puzzle):
    bound = heuristic(puzzle.state)
    path = []
    while True:
        visited = set()
        t, res = dfs(puzzle.copy(), 0, bound, path, visited)
        if res:
            return res
        if t == float('inf'):
            return []
        bound = t 