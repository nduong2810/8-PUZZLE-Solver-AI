from Puzzle import Puzzle
import time
from collections import defaultdict

GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]

def heuristic(state):
    return sum(1 for y in range(3) for x in range(3) if state[y][x] != 0 and state[y][x] != GOAL_STATE[y][x])

class ANDORNode:
    def __init__(self, puzzle, is_or_node=True):
        self.puzzle = puzzle
        self.is_or_node = is_or_node  # True cho OR node, False cho AND node
        self.children = []
        self.solved = False
        self.cost = float('inf')
        self.parent = None

def get_possible_moves(puzzle):
    x0, y0 = puzzle.find_zero()
    moves = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x0+dx, y0+dy
        if 0<=nx<3 and 0<=ny<3:
            moves.append((nx, ny))
    return moves

def create_and_or_tree(puzzle, max_depth=50):
    root = ANDORNode(puzzle, is_or_node=True)
    nodes = {str(puzzle.state): root}
    
    def expand_node(node, depth):
        if depth >= max_depth or node.puzzle.state == GOAL_STATE:
            node.solved = (node.puzzle.state == GOAL_STATE)
            node.cost = 0 if node.solved else float('inf')
            return
        
        if node.is_or_node:
            # OR node: chọn một trong các hành động có thể
            moves = get_possible_moves(node.puzzle)
            for move in moves:
                new_puzzle = node.puzzle.copy()
                if new_puzzle.move(move[0], move[1]):
                    state_key = str(new_puzzle.state)
                    if state_key not in nodes:
                        child = ANDORNode(new_puzzle, is_or_node=False)
                        nodes[state_key] = child
                        child.parent = node
                        node.children.append(child)
                        expand_node(child, depth + 1)
        else:
            # AND node: tất cả các hành động phải thành công
            moves = get_possible_moves(node.puzzle)
            for move in moves:
                new_puzzle = node.puzzle.copy()
                if new_puzzle.move(move[0], move[1]):
                    state_key = str(new_puzzle.state)
                    if state_key not in nodes:
                        child = ANDORNode(new_puzzle, is_or_node=True)
                        nodes[state_key] = child
                        child.parent = node
                        node.children.append(child)
                        expand_node(child, depth + 1)
    
    expand_node(root, 0)
    return root, nodes

def solve_and_or_tree(root, nodes):
    def update_costs(node):
        if not node.children:
            node.solved = (node.puzzle.state == GOAL_STATE)
            node.cost = 0 if node.solved else float('inf')
            return node.solved, node.cost
        
        if node.is_or_node:
            # OR node: chọn con có chi phí thấp nhất
            min_cost = float('inf')
            solved = False
            for child in node.children:
                child_solved, child_cost = update_costs(child)
                if child_solved and child_cost < min_cost:
                    min_cost = child_cost
                    solved = True
            node.solved = solved
            node.cost = min_cost + 1 if solved else float('inf')
        else:
            # AND node: tất cả các con phải giải được
            total_cost = 0
            solved = True
            for child in node.children:
                child_solved, child_cost = update_costs(child)
                if not child_solved:
                    solved = False
                    break
                total_cost += child_cost
            node.solved = solved
            node.cost = total_cost + 1 if solved else float('inf')
        
        return node.solved, node.cost
    
    update_costs(root)
    return root.solved

def get_solution_path(root):
    if not root.solved:
        return []
    
    path = [root.puzzle.copy()]
    current = root
    
    while current.children:
        if current.is_or_node:
            # Chọn con có chi phí thấp nhất
            best_child = min(current.children, key=lambda x: x.cost)
            current = best_child
        else:
            # Thêm tất cả các con vào đường đi
            for child in current.children:
                path.extend(get_solution_path(child))
            break
        path.append(current.puzzle.copy())
    
    return path

def solve(puzzle: Puzzle):
    print("Bắt đầu AND-OR Graph Search...")
    start_time = time.time()
    
    # Tạo cây AND-OR
    root, nodes = create_and_or_tree(puzzle)
    
    # Giải cây AND-OR
    solved = solve_and_or_tree(root, nodes)
    
    if solved:
        # Lấy đường đi giải
        path = get_solution_path(root)
        end_time = time.time()
        print(f"Tìm thấy lời giải sau {end_time - start_time:.2f} giây")
        print(f"Số bước: {len(path) - 1}")
        return path
    else:
        print("Không tìm thấy lời giải!")
        return None 