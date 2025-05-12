from Puzzle import Puzzle
import numpy as np
import random
from collections import defaultdict
import time

GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]

def heuristic(state):
    return sum(1 for y in range(3) for x in range(3) if state[y][x] != 0 and state[y][x] != GOAL_STATE[y][x])

class QLearning:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, exploration_rate=0.3):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = defaultdict(lambda: defaultdict(float))
        
    def get_state_key(self, puzzle):
        return str(puzzle.state)
        
    def get_action(self, puzzle):
        state_key = self.get_state_key(puzzle)
        x0, y0 = puzzle.find_zero()
        possible_actions = []
        
        # Lấy tất cả các hành động có thể
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x0+dx, y0+dy
            if 0<=nx<3 and 0<=ny<3:
                possible_actions.append((nx, ny))
        
        # Epsilon-greedy strategy
        if random.random() < self.exploration_rate:
            return random.choice(possible_actions)
        else:
            # Chọn hành động có giá trị Q cao nhất
            q_values = [self.q_table[state_key][str(action)] for action in possible_actions]
            max_q = max(q_values)
            best_actions = [action for action, q in zip(possible_actions, q_values) if q == max_q]
            return random.choice(best_actions)
    
    def update_q_value(self, current_puzzle, action, reward, next_puzzle):
        state_key = self.get_state_key(current_puzzle)
        action_key = str(action)
        next_state_key = self.get_state_key(next_puzzle)
        
        # Lấy giá trị Q cao nhất cho trạng thái tiếp theo
        next_q_values = [self.q_table[next_state_key][str(a)] for a in self.get_possible_actions(next_puzzle)]
        max_next_q = max(next_q_values) if next_q_values else 0
        
        # Cập nhật giá trị Q
        current_q = self.q_table[state_key][action_key]
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state_key][action_key] = new_q
    
    def get_possible_actions(self, puzzle):
        x0, y0 = puzzle.find_zero()
        actions = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x0+dx, y0+dy
            if 0<=nx<3 and 0<=ny<3:
                actions.append((nx, ny))
        return actions
    
    def train(self, puzzle, episodes=5000):
        print("Bắt đầu huấn luyện Q-learning...")
        start_time = time.time()
        best_reward = float('-inf')
        successful_episodes = 0
        consecutive_successes = 0
        best_consecutive_successes = 0
        
        for episode in range(episodes):
            current_puzzle = puzzle.copy()
            steps = 0
            max_steps = 100  # Giới hạn số bước cho mỗi episode
            episode_reward = 0
            
            while steps < max_steps:
                if current_puzzle.state == GOAL_STATE:
                    successful_episodes += 1
                    consecutive_successes += 1
                    best_consecutive_successes = max(best_consecutive_successes, consecutive_successes)
                    break
                    
                # Chọn hành động
                action = self.get_action(current_puzzle)
                
                # Thực hiện hành động
                next_puzzle = current_puzzle.copy()
                if next_puzzle.move(action[0], action[1]):
                    # Tính toán phần thưởng
                    reward = -1  # Phạt cho mỗi bước
                    if next_puzzle.state == GOAL_STATE:
                        reward = 200  # Tăng phần thưởng khi đạt goal
                    
                    # Thêm phần thưởng dựa trên heuristic
                    reward -= heuristic(next_puzzle.state) * 0.2
                    
                    # Cập nhật giá trị Q
                    self.update_q_value(current_puzzle, action, reward, next_puzzle)
                    current_puzzle = next_puzzle
                    episode_reward += reward
                
                steps += 1
            
            if current_puzzle.state != GOAL_STATE:
                consecutive_successes = 0
            
            # Cập nhật tỷ lệ khám phá
            self.exploration_rate = max(0.01, self.exploration_rate * 0.9995)
            
            # In thông tin tiến trình
            if (episode + 1) % 100 == 0:
                elapsed_time = time.time() - start_time
                success_rate = (successful_episodes / (episode + 1)) * 100
                print(f"Episode {episode + 1}/{episodes} - Thời gian: {elapsed_time:.1f}s")
                print(f"Tỷ lệ thành công: {success_rate:.1f}% - Chuỗi thành công dài nhất: {best_consecutive_successes}")
                print(f"Tỷ lệ khám phá hiện tại: {self.exploration_rate:.3f}")
                print("-" * 50)
        
        print(f"Hoàn thành huấn luyện sau {episodes} episodes!")
        print(f"Tổng thời gian: {time.time() - start_time:.1f} giây")
        print(f"Tỷ lệ thành công cuối cùng: {(successful_episodes / episodes) * 100:.1f}%")
        print(f"Chuỗi thành công dài nhất: {best_consecutive_successes}")
    
    def get_best_path(self, puzzle):
        print("Đang tìm đường đi tốt nhất...")
        path = [puzzle.copy()]
        current = puzzle.copy()
        visited = set()
        steps = 0
        max_steps = 100
        
        while current.state != GOAL_STATE and steps < max_steps:
            state_key = self.get_state_key(current)
            if state_key in visited:
                break
                
            visited.add(state_key)
            action = self.get_action(current)
            if current.move(action[0], action[1]):
                path.append(current.copy())
            else:
                break
            
            steps += 1
        
        if current.state == GOAL_STATE:
            print(f"Tìm thấy đường đi với {len(path)} bước!")
        else:
            print("Không tìm thấy đường đi!")
        
        return path

def solve(puzzle: Puzzle):
    # Khởi tạo và huấn luyện Q-learning với tham số được điều chỉnh
    q_learning = QLearning(
        learning_rate=0.1,      # Tỷ lệ học
        discount_factor=0.95,   # Hệ số chiết khấu
        exploration_rate=0.3    # Tỷ lệ khám phá ban đầu
    )
    q_learning.train(puzzle, episodes=5000)  # Tăng số episodes lên 5000
    
    # Lấy đường đi tốt nhất
    return q_learning.get_best_path(puzzle) 