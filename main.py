import pygame
import sys
import importlib
import time
from Puzzle import Puzzle
from ui import draw_ui, TILE_SIZE, MARGIN

def show_no_solution_popup(screen, width, height):
    # Tạo một surface mới cho popup
    popup_width = 300
    popup_height = 150
    popup = pygame.Surface((popup_width, popup_height))
    popup.fill((50, 50, 50))  # Màu nền tối
    
    # Vẽ viền cho popup
    pygame.draw.rect(popup, (200, 200, 200), (0, 0, popup_width, popup_height), 2)
    
    # Tạo font và text
    font = pygame.font.Font(None, 36)
    text = font.render("No Solution Found!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(popup_width//2, popup_height//2))
    
    # Vẽ text lên popup
    popup.blit(text, text_rect)
    
    # Tính toán vị trí để hiển thị popup ở giữa màn hình
    popup_rect = popup.get_rect(center=(width//2, height//2))
    
    # Tạo một surface mờ cho nền
    overlay = pygame.Surface((width, height))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)  # Độ trong suốt
    
    # Vẽ overlay và popup lên màn hình
    screen.blit(overlay, (0, 0))
    screen.blit(popup, popup_rect)
    pygame.display.flip()
    
    # Đợi 2 giây
    pygame.time.wait(2000)

def main():
    pygame.init()

    WIDTH = MARGIN * 5 + TILE_SIZE * 3 * 4
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8 Puzzle - Thuật toán + Animation")

    # Lưu trạng thái ban đầu của ma trận A
    INITIAL_STATE_A = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
    puzzleA = Puzzle(INITIAL_STATE_A)
    puzzleB = Puzzle([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    historyA = [puzzleA.copy()]
    historyB = [puzzleB.copy()]

    scroll_offset_A = 0
    scroll_offset_B = 0
    scroll_step = TILE_SIZE * 3 + 10
    max_scroll_A = 0
    max_scroll_B = 0

    buttons = {
        'reset': pygame.Rect(WIDTH // 2 - 75, 10, 150, 40),
        'matA': pygame.Rect(MARGIN, 70, TILE_SIZE*3, TILE_SIZE*3),
        'historyA': pygame.Rect(MARGIN + TILE_SIZE*3 + MARGIN, 70, TILE_SIZE*3, HEIGHT - 200),
        'matB': pygame.Rect(MARGIN + TILE_SIZE*3*2 + MARGIN*2, 70, TILE_SIZE*3, TILE_SIZE*3),
        'historyB': pygame.Rect(MARGIN + TILE_SIZE*3*3 + MARGIN*3, 70, TILE_SIZE*3, HEIGHT - 200),
        'menu': pygame.Rect(WIDTH // 2 - 100, HEIGHT - 60, 200, 40)
    }

    algorithm_names = [
        "bfs", "dfs", "ucs", "ids", "greedy_search", "a_star", "ida_star", "hill_climbing_simple", "hill_climbing_steepest",
        "hill_climbing_stochastic", "beam_search", "simulated_annealing", "genetic_algorithm", "and_or_graph_search",
        "belief_state_search", "partially_observable_search", "q_learning", "backtracking"
    ]
    # Danh sách tên viết tắt cho thuật toán
    algo_short_names = [
        "BFS", "DFS", "UCS", "IDS", "GRE", "AST", "IDA", "HC-S", "HC-T",
        "HC-R", "BEAM", "SA", "GA", "AO", "BEL", "POS", "QL", "BT"
    ]
    algo_buttons = []
    for i, (name, short) in enumerate(zip(algorithm_names, algo_short_names)):
        x = buttons['matA'].x + (i % 4) * (TILE_SIZE * 3 + 20)
        y = buttons['matA'].bottom + 20 + (i // 4) * 50
        rect = pygame.Rect(x, y, 90, 40)
        algo_buttons.append((rect, name, short))

    selected_algo = algorithm_names[0]  # Thuật toán mặc định
    show_menu = False

    def reset_matrix_a():
        nonlocal puzzleA, historyA, scroll_offset_A
        puzzleA = Puzzle(INITIAL_STATE_A)
        historyA = [puzzleA.copy()]
        scroll_offset_A = 0

    def run_algorithm(algo_name):
        nonlocal puzzleA, puzzleB, historyA, historyB, scroll_offset_A, scroll_offset_B
        # Đảm bảo ma trận A được reset về trạng thái ban đầu
        reset_matrix_a()
        
        try:
            module = importlib.import_module(algo_name)
            start_time = time.perf_counter()
            
            # Chạy thuật toán trên ma trận B nếu là Backtracking
            if algo_name == "backtracking":
                steps = module.solve(
                    puzzleB.copy(), screen, buttons, puzzleA, puzzleB, historyA, historyB, scroll_offset_A, scroll_offset_B
                )
                history = historyB
                scroll_offset = scroll_offset_B
                puzzle = puzzleB
                history_rect = buttons['historyB']
            else:
                steps = module.solve(puzzleA.copy())
                history = historyA
                scroll_offset = scroll_offset_A
                puzzle = puzzleA
                history_rect = buttons['historyA']
            
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            # Kiểm tra cả trường hợp steps là None hoặc danh sách rỗng
            if steps is None or len(steps) == 0:
                print(f"No solution found for {algo_name}!")
                show_no_solution_popup(screen, WIDTH, HEIGHT)
            else:
                history.clear()
                for step in steps:
                    if algo_name == "backtracking":
                        puzzleB = step.copy()
                        historyB.append(puzzleB.copy())
                    else:
                        puzzleA = step.copy()
                        historyA.append(puzzleA.copy())
                    # Xử lý sự kiện trong khi thuật toán đang chạy
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEWHEEL:
                            mouse_x, _ = pygame.mouse.get_pos()
                            if history_rect.x <= mouse_x <= history_rect.right:
                                max_scroll = max(0, (len(history) - 1) * scroll_step)
                                new_offset = scroll_offset - event.y * scroll_step
                                scroll_offset = max(0, min(new_offset, max_scroll))
                    draw_ui(screen, puzzleA, puzzleB, buttons, historyA, historyB, scroll_offset_A, scroll_offset_B, [])
                    pygame.time.wait(250)
                
                # Hiển thị thông tin về thời gian và số bước
                font = pygame.font.Font(None, 36)
                if execution_time < 1:
                    time_str = f"Time: {execution_time*1000:.2f} ms"
                else:
                    time_str = f"Time: {execution_time:.4f} s"
                time_text = font.render(time_str, True, (0, 255, 0))
                steps_text = font.render(f"Steps: {len(steps)}", True, (0, 255, 0))
                
                # Tính toán vị trí dưới ma trận tương ứng
                info_y = buttons['matB'].bottom + 20 if algo_name == "backtracking" else buttons['matA'].bottom + 20
                info_x = buttons['matB'].centerx if algo_name == "backtracking" else buttons['matA'].centerx
                
                time_rect = time_text.get_rect(midtop=(info_x, info_y))
                steps_rect = steps_text.get_rect(midtop=(info_x, info_y + 40))
                
                screen.blit(time_text, time_rect)
                screen.blit(steps_text, steps_rect)
                pygame.display.flip()
                pygame.time.wait(2000)  # Hiển thị thông tin trong 2 giây
                
        except Exception as e:
            print(f"Lỗi chạy thuật toán {algo_name}:", e)
            show_no_solution_popup(screen, WIDTH, HEIGHT)

    while True:
        # Vẽ UI, ẩn lịch sử khi show_menu
        if not show_menu:
            draw_ui(screen, puzzleA, puzzleB, buttons, historyA, historyB, scroll_offset_A, scroll_offset_B, [])
        else:
            draw_ui(screen, puzzleA, puzzleB, buttons, [], [], 0, 0, [(r, s) for r, n, s in algo_buttons])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if buttons['reset'].collidepoint(pos):
                    reset_matrix_a()
                    puzzleB = Puzzle([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                    historyB = [puzzleB.copy()]
                    scroll_offset_B = 0

                elif buttons['menu'].collidepoint(pos):
                    show_menu = not show_menu

                if show_menu:
                    for rect, name, short in algo_buttons:
                        if rect.collidepoint(pos):
                            selected_algo = name
                            show_menu = False
                            run_algorithm(selected_algo)
                else:
                    if buttons['matA'].collidepoint(pos):
                        tx = (pos[0] - buttons['matA'].x) // TILE_SIZE
                        ty = (pos[1] - buttons['matA'].y) // TILE_SIZE
                        prev = puzzleA.copy()
                        if puzzleA.move(tx, ty):
                            historyA.append(puzzleA.copy())

                    elif buttons['matB'].collidepoint(pos):
                        tx = (pos[0] - buttons['matB'].x) // TILE_SIZE
                        ty = (pos[1] - buttons['matB'].y) // TILE_SIZE
                        prev = puzzleB.copy()
                        if puzzleB.move(tx, ty):
                            historyB.append(puzzleB.copy())

            elif event.type == pygame.MOUSEWHEEL:
                mouse_x, _ = pygame.mouse.get_pos()
                if buttons['historyA'].x <= mouse_x <= buttons['historyA'].right:
                    # Tính toán giới hạn cuộn dựa trên số lượng bước trong lịch sử
                    max_scroll_A = max(0, (len(historyA) - 1) * scroll_step)
                    new_offset = scroll_offset_A - event.y * scroll_step
                    scroll_offset_A = max(0, min(new_offset, max_scroll_A))
                elif buttons['historyB'].x <= mouse_x <= buttons['historyB'].right:
                    # Tính toán giới hạn cuộn dựa trên số lượng bước trong lịch sử
                    max_scroll_B = max(0, (len(historyB) - 1) * scroll_step)
                    new_offset = scroll_offset_B - event.y * scroll_step
                    scroll_offset_B = max(0, min(new_offset, max_scroll_B))

        pygame.time.delay(30)

if __name__ == "__main__":
    main()
