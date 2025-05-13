from Puzzle import Puzzle
import time

GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]

def get_possible_moves(puzzle):
    x0, y0 = puzzle.find_zero()
    moves = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x0+dx, y0+dy
        if 0<=nx<3 and 0<=ny<3:
            moves.append((nx, ny))
    return moves

def serialize(state):
    return str(state)

def and_or_dfs(puzzle, path, visited, max_depth=100):
    if puzzle.state == GOAL_STATE:
        return path + [puzzle]
    if len(path) > max_depth:
        return None
    key = serialize(puzzle.state)
    if key in visited:
        return None
    visited.add(key)
    moves = get_possible_moves(puzzle)
    # Sắp xếp các nước đi theo heuristic tăng dần (nước đi tốt nhất trước)
    def h(move):
        new_puzzle = puzzle.copy()
        new_puzzle.move(move[0], move[1])
        return sum(1 for y in range(3) for x in range(3) if new_puzzle.state[y][x] != 0 and new_puzzle.state[y][x] != GOAL_STATE[y][x])
    moves.sort(key=h)
    for move in moves:
        new_puzzle = puzzle.copy()
        if new_puzzle.move(move[0], move[1]):
            result = and_or_dfs(new_puzzle, path + [puzzle], visited, max_depth)
            if result:
                return result
    visited.remove(key)
    return None

def solve(puzzle: Puzzle):
    print("Bắt đầu AND-OR Graph Search kết hợp DFS...")
    start_time = time.perf_counter()
    visited = set()
    path = and_or_dfs(puzzle.copy(), [], visited, max_depth=100)
    end_time = time.perf_counter()
    if path:
        print(f"Tìm thấy lời giải sau {end_time - start_time:.4f} giây")
        print(f"Số bước: {len(path) - 1}")
        return path
    else:
        print("Không tìm thấy lời giải!")
        return None 