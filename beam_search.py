from Puzzle import Puzzle
import heapq
GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]
def heuristic(state):
    return sum(1 for y in range(3) for x in range(3) if state[y][x] != 0 and state[y][x] != GOAL_STATE[y][x])
def serialize(state):
    return str(state)
def solve(puzzle: Puzzle, beam_width=2):
    beam = [(heuristic(puzzle.state), 0, puzzle.copy(), [])]
    visited = set()
    counter = 0
    while beam:
        new_beam = []
        for h, _, current, path in beam:
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
                        counter += 1
                        new_beam.append((heuristic(new_puzzle.state), counter, new_puzzle, path+[current]))
        beam = sorted(new_beam)[:beam_width]
    return [] 