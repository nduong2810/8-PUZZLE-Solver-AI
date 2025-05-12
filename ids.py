from Puzzle import Puzzle
from collections import deque

GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]

def depth_limited_search(puzzle, depth_limit):
    visited = set()
    stack = [(puzzle, [puzzle], 0)]  # (current_state, path, current_depth)
    
    while stack:
        current, path, depth = stack.pop()
        
        if current.state == GOAL_STATE:
            return path
            
        if depth >= depth_limit:
            continue
            
        state_key = str(current.state)
        if state_key in visited:
            continue
            
        visited.add(state_key)
        
        # Thử các bước di chuyển có thể
        x0, y0 = current.find_zero()
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x0+dx, y0+dy
            if 0<=nx<3 and 0<=ny<3:
                next_puzzle = current.copy()
                if next_puzzle.move(nx, ny):
                    if str(next_puzzle.state) not in visited:
                        stack.append((next_puzzle, path + [next_puzzle], depth + 1))
    
    return None

def solve(puzzle: Puzzle):
    # Tăng dần độ sâu tìm kiếm
    for depth in range(1, 100):  # Giới hạn độ sâu tối đa là 100
        result = depth_limited_search(puzzle, depth)
        if result is not None:
            return result
    return [] 