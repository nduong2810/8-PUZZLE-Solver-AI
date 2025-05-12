from Puzzle import Puzzle
GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]
def heuristic(state):
    return sum(1 for y in range(3) for x in range(3) if state[y][x] != 0 and state[y][x] != GOAL_STATE[y][x])
def serialize(state):
    return str(state)
def solve(puzzle: Puzzle):
    current = puzzle.copy()
    path = [current.copy()]
    visited = set()
    while True:
        x0, y0 = current.find_zero()
        neighbors = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x0+dx, y0+dy
            if 0<=nx<3 and 0<=ny<3:
                new_puzzle = current.copy()
                if new_puzzle.move(nx, ny):
                    neighbors.append(new_puzzle)
        next_state = None
        min_h = heuristic(current.state)
        for n in neighbors:
            h = heuristic(n.state)
            if h < min_h:
                min_h = h
                next_state = n
        if next_state and serialize(next_state.state) not in visited:
            current = next_state
            path.append(current.copy())
            visited.add(serialize(current.state))
            if current.state == GOAL_STATE:
                return path
        else:
            return None
    return path 