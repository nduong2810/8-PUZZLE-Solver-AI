from Puzzle import Puzzle
import time
import pygame

def is_goal(state):
    GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]
    return state == GOAL_STATE

def get_goal_pos(num):
    if num == 0:
        return 2, 2
    return (num - 1) // 3, (num - 1) % 3

def backtrack(state, used, idx, puzzle, path, found,
              screen, buttons, puzzleA, puzzleB, historyA, historyB, scroll_offset_A, scroll_offset_B):
    if idx == 9:
        if is_goal(state):
            found[0] = True
        return found[0]

    for num in range(9):
        if not used[num]:
            goal_row, goal_col = get_goal_pos(num)
            # Nếu vị trí đích còn trống, thử điền vào đó trước
            if state[goal_row][goal_col] == -1:
                row, col = goal_row, goal_col
            else:
                # Nếu vị trí đích đã bị chiếm, thử các vị trí còn lại
                found_empty = False
                for r in range(3):
                    for c in range(3):
                        if state[r][c] == -1:
                            row, col = r, c
                            found_empty = True
                            break
                    if found_empty:
                        break
            state[row][col] = num
            used[num] = True
            puzzle.state = [r[:] for r in state]
            path.append(puzzle.copy())
            historyB.clear()
            historyB.append(puzzle.copy())
            from ui import draw_ui
            draw_ui(screen, puzzleA, puzzleB, buttons, historyA, historyB, scroll_offset_A, scroll_offset_B, [])
            pygame.display.flip()
            pygame.time.wait(10)
            if backtrack(state, used, idx+1, puzzle, path, found,
                         screen, buttons, puzzleA, puzzleB, historyA, historyB, scroll_offset_A, scroll_offset_B):
                return True
            # Backtrack
            state[row][col] = -1
            used[num] = False
            puzzle.state = [r[:] for r in state]
            path.append(puzzle.copy())
            historyB.clear()
            historyB.append(puzzle.copy())
            draw_ui(screen, puzzleA, puzzleB, buttons, historyA, historyB, scroll_offset_A, scroll_offset_B, [])
            pygame.display.flip()
            pygame.time.wait(10)
    return False

def solve(puzzle: Puzzle, screen=None, buttons=None, puzzleA=None, puzzleB=None,
          historyA=None, historyB=None, scroll_offset_A=0, scroll_offset_B=0):
    print("Bắt đầu Backtracking Search...")
    start_time = time.time()
    puzzle.state = [[-1]*3 for _ in range(3)]
    state = [[-1]*3 for _ in range(3)]
    used = [False]*9
    path = [puzzle.copy()]
    found = [False]
    backtrack(state, used, 0, puzzle, path, found,
              screen, buttons, puzzleA, puzzleB, historyA, historyB, scroll_offset_A, scroll_offset_B)
    end_time = time.time()
    print(f"Tìm thấy lời giải sau {end_time - start_time:.2f} giây")
    print(f"Số bước: {len(path) - 1}")
    return path if found[0] else None
