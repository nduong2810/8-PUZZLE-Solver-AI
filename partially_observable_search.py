from Puzzle import Puzzle
from collections import deque
import random

GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]

def get_observable_state(puzzle):
    # Trong bài toán 8-puzzle, chúng ta giả định rằng một số ô không thể quan sát được
    # Chúng ta sẽ thay thế các ô không quan sát được bằng -1
    observable_state = [row[:] for row in puzzle.state]
    num_hidden = random.randint(1, 3)  # Số lượng ô không quan sát được
    
    # Chọn ngẫu nhiên các ô để ẩn
    positions = [(x, y) for y in range(3) for x in range(3)]
    hidden_positions = random.sample(positions, num_hidden)
    
    for x, y in hidden_positions:
        observable_state[y][x] = -1
    
    return observable_state

def is_goal_state(observable_state):
    # Kiểm tra xem trạng thái có thể là goal state không
    # Bỏ qua các ô không quan sát được (-1)
    for y in range(3):
        for x in range(3):
            if observable_state[y][x] != -1 and observable_state[y][x] != GOAL_STATE[y][x]:
                return False
    return True

def solve(puzzle: Puzzle):
    visited = set()
    queue = deque([(puzzle, [puzzle])])
    
    while queue:
        current, path = queue.popleft()
        
        # Lấy trạng thái có thể quan sát được
        observable_state = get_observable_state(current)
        
        # Kiểm tra nếu trạng thái có thể là goal state
        if is_goal_state(observable_state):
            return path
            
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
                        queue.append((next_puzzle, path + [next_puzzle]))
    
    return [] 