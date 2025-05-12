from Puzzle import Puzzle
import random
import copy

GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]

def heuristic(state):
    return sum(1 for y in range(3) for x in range(3) if state[y][x] != 0 and state[y][x] != GOAL_STATE[y][x])

class Individual:
    def __init__(self, puzzle, moves=None):
        self.puzzle = puzzle
        self.moves = moves if moves else []
        self.fitness = self.calculate_fitness()
    
    def calculate_fitness(self):
        if not self.moves:
            return float('inf')
        return len(self.moves) + heuristic(self.puzzle.state)
    
    def mutate(self):
        if not self.moves:
            return self
        
        new_moves = self.moves.copy()
        # Đột biến: thay đổi một số bước di chuyển
        mutation_point = random.randint(0, len(new_moves)-1)
        x0, y0 = new_moves[mutation_point].find_zero()
        possible_moves = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x0+dx, y0+dy
            if 0<=nx<3 and 0<=ny<3:
                possible_moves.append((nx, ny))
        if possible_moves:
            new_pos = random.choice(possible_moves)
            new_puzzle = new_moves[mutation_point].copy()
            if new_puzzle.move(new_pos[0], new_pos[1]):
                new_moves[mutation_point] = new_puzzle
        
        return Individual(new_moves[-1], new_moves)

def crossover(parent1, parent2):
    if not parent1.moves or not parent2.moves:
        return parent1
    
    # Lấy điểm cắt ngẫu nhiên
    crossover_point = random.randint(0, min(len(parent1.moves), len(parent2.moves))-1)
    
    # Tạo con mới bằng cách kết hợp các bước di chuyển
    child_moves = parent1.moves[:crossover_point] + parent2.moves[crossover_point:]
    return Individual(child_moves[-1], child_moves)

def solve(puzzle: Puzzle, population_size=50, generations=100):
    # Khởi tạo quần thể
    population = []
    for _ in range(population_size):
        moves = [puzzle.copy()]
        current = puzzle.copy()
        for _ in range(20):  # Tạo 20 bước di chuyển ngẫu nhiên
            x0, y0 = current.find_zero()
            possible_moves = []
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x0+dx, y0+dy
                if 0<=nx<3 and 0<=ny<3:
                    possible_moves.append((nx, ny))
            if possible_moves:
                new_pos = random.choice(possible_moves)
                if current.move(new_pos[0], new_pos[1]):
                    moves.append(current.copy())
        population.append(Individual(moves[-1], moves))
    
    for generation in range(generations):
        # Sắp xếp quần thể theo độ thích nghi
        population.sort(key=lambda x: x.fitness)
        
        # Kiểm tra nếu đã tìm thấy giải pháp
        if population[0].puzzle.state == GOAL_STATE:
            return population[0].moves
        
        # Tạo quần thể mới
        new_population = population[:2]  # Giữ lại 2 cá thể tốt nhất
        
        while len(new_population) < population_size:
            # Chọn cha mẹ
            parent1 = random.choice(population[:10])
            parent2 = random.choice(population[:10])
            
            # Lai ghép
            child = crossover(parent1, parent2)
            
            # Đột biến
            if random.random() < 0.1:  # 10% cơ hội đột biến
                child = child.mutate()
            
            new_population.append(child)
        
        population = new_population
    
    # Trả về giải pháp tốt nhất tìm được
    population.sort(key=lambda x: x.fitness)
    return population[0].moves if population[0].moves else [] 