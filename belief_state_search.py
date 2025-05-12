from Puzzle import Puzzle
from collections import deque
import random

GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]

def get_possible_states(puzzle):
    # Trong bài toán 8-puzzle, belief state là tập hợp các trạng thái có thể
    # Ở đây chúng ta giả định rằng chúng ta không biết chính xác vị trí của một số ô
    possible_states = []
    current_state = puzzle.state
    
    # Tạo một số trạng thái có thể bằng cách hoán đổi ngẫu nhiên các ô
    for _ in range(3):
        new_state = [row[:] for row in current_state]
        # Hoán đổi ngẫu nhiên 2 ô không phải ô trống
        non_zero_positions = [(x, y) for y in range(3) for x in range(3) if new_state[y][x] != 0]
        if len(non_zero_positions) >= 2:
            pos1, pos2 = random.sample(non_zero_positions, 2)
            new_state[pos1[1]][pos1[0]], new_state[pos2[1]][pos2[0]] = new_state[pos2[1]][pos2[0]], new_state[pos1[1]][pos1[0]]
            possible_states.append(new_state)
    
    return possible_states

def solve(puzzle: Puzzle):
    visited = set()
    queue = deque([(puzzle, [puzzle])])
    
    while queue:
        current, path = queue.popleft()
        
        # Kiểm tra nếu bất kỳ trạng thái nào trong belief state là goal state
        if current.state == GOAL_STATE:
            return path
            
        state_key = str(current.state)
        if state_key in visited:
            continue
            
        visited.add(state_key)
        
        # Lấy các trạng thái có thể từ belief state
        possible_states = get_possible_states(current)
        
        for state in possible_states:
            new_puzzle = Puzzle(state)
            x0, y0 = new_puzzle.find_zero()
            
            # Thử các bước di chuyển có thể
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x0+dx, y0+dy
                if 0<=nx<3 and 0<=ny<3:
                    next_puzzle = new_puzzle.copy()
                    if next_puzzle.move(nx, ny):
                        if str(next_puzzle.state) not in visited:
                            queue.append((next_puzzle, path + [next_puzzle]))
    
    return [] 