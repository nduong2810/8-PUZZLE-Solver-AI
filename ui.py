import pygame

TILE_SIZE = 60
GRID_SIZE = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
GRAY = (211, 211, 211)
MARGIN = 20

# Thêm các màu mới cho các ô số
TILE_COLORS = {
    1: (255, 99, 71),    # Tomato
    2: (255, 165, 0),    # Orange
    3: (255, 255, 0),    # Yellow
    4: (50, 205, 50),    # Lime Green
    5: (0, 191, 255),    # Deep Sky Blue
    6: (147, 112, 219),  # Medium Purple
    7: (255, 20, 147),   # Deep Pink
    8: (0, 255, 127),    # Spring Green
    0: (169, 169, 169)   # Dark Gray
}

# Màu mới cho các nút
BUTTON_COLOR = (100, 149, 237)  # Cornflower Blue
BUTTON_HOVER_COLOR = (65, 105, 225)  # Royal Blue
BUTTON_TEXT_COLOR = (255, 255, 255)  # White

pygame.font.init()
FONT = pygame.font.SysFont(None, 36)

def draw_matrix(screen, matrix, top_left, show_number=True):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            val = matrix[y][x]
            rect = pygame.Rect(top_left[0] + x*TILE_SIZE, top_left[1] + y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = TILE_COLORS.get(val, BLUE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            if show_number:
                if val != -1 and val != 0:
                    text = FONT.render(str(val), True, WHITE)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

def draw_button(screen, rect, text):
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label = FONT.render(text, True, BUTTON_TEXT_COLOR)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_history_column(screen, history, top_left, scroll_offset=0, show_number=True):
    for i, puzzle in enumerate(history):
        offset_y = top_left[1] + i * (TILE_SIZE * 3 + 10) - scroll_offset
        if offset_y + TILE_SIZE * 3 < top_left[1] or offset_y > top_left[1] + 500:
            continue
        draw_matrix(screen, puzzle.state, (top_left[0], offset_y), show_number)

def draw_algorithm_buttons(screen, algo_buttons):
    mouse_pos = pygame.mouse.get_pos()
    for rect, short in algo_buttons:
        color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        label = FONT.render(short, True, BUTTON_TEXT_COLOR)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

def draw_ui(screen, puzzleA, puzzleB, buttons, historyA, historyB, scroll_offset_A=0, scroll_offset_B=0, algo_buttons=[]):
    screen.fill(WHITE)
    draw_button(screen, buttons['reset'], "Reset")
    draw_matrix(screen, puzzleA.state, buttons['matA'].topleft)
    draw_history_column(screen, historyA, buttons['historyA'].topleft, scroll_offset=scroll_offset_A)
    draw_matrix(screen, puzzleB.state, buttons['matB'].topleft, show_number=True)
    draw_history_column(screen, historyB, buttons['historyB'].topleft, scroll_offset=scroll_offset_B, show_number=True)
    draw_button(screen, buttons['menu'], "Menu")
    draw_algorithm_buttons(screen, algo_buttons)
    pygame.display.flip()
