from Puzzle import Puzzle
import math, random
GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]
def heuristic(state):
    return sum(1 for y in range(3) for x in range(3) if state[y][x] != 0 and state[y][x] != GOAL_STATE[y][x])
def serialize(state):
    return str(state)
def solve(puzzle: Puzzle):
    current = puzzle.copy()
    path = [current.copy()]
    T = 100.0
    T_min = 1e-6
    alpha = 0.90
    max_steps = 10000
    steps = 0
    while T > T_min and steps < max_steps:
        x0, y0 = current.find_zero()
        neighbors = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x0+dx, y0+dy
            if 0<=nx<3 and 0<=ny<3:
                new_puzzle = current.copy()
                if new_puzzle.move(nx, ny):
                    neighbors.append(new_puzzle)
        if not neighbors:
            break
        next_state = random.choice(neighbors)
        delta = heuristic(next_state.state) - heuristic(current.state)
        if delta < 0 or random.random() < math.exp(-delta/T):
            current = next_state
            path.append(current.copy())
            if current.state == GOAL_STATE:
                return path
        T *= alpha
        steps += 1
    return None 