import pygame as p
import os
import random
import pickle
import ChessEngine

# Constants
WIDTH, HEIGHT = 512, 512
MAX_FPS = 60
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
RESULTS_FOLDER = "results"

# Initialize Pygame display settings
p.display.set_caption("Eight Queens")
p.display.set_icon(p.image.load("assets/piece/bQ.png"))

# Load and scale images for the pieces
IMAGES = {}
def load_images():
    piece = 'wQ'
    img = p.image.load(os.path.join("assets/piece", f"{piece}.png"))
    IMAGES[piece] = p.transform.scale(img, (SQ_SIZE, SQ_SIZE))

def draw_buttons(screen, placing):
    colors = {"Place": "red", "Result": "blue", "Clear": "#CCCC00", "Random": "#606060", "Quit": "orange"}
    button_info = [("Place", 0), ("Result", 100), ("Clear", 200), ("Random", 300), ("Quit", 400)]
    
    for text, x_offset in button_info:
        rect = p.Rect(x_offset, HEIGHT, 100, 25)
        color = colors[text] if placing or text != "Place" else "green"
        p.draw.rect(screen, p.Color(color), rect)
        font = p.font.Font(None, 33)
        text_render = font.render(text, True, p.Color("white"))
        text_rect = text_render.get_rect(center=rect.center)
        screen.blit(text_render, text_rect)

def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)

def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_placed_pieces(screen, placed_pieces):
    for row, col in placed_pieces:
        screen.blit(IMAGES["wQ"], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def auto_place_remaining_pieces(placed_pieces):
    solutions = []
    start_col = len(placed_pieces)
    used_cols = {col for _, col in placed_pieces}
    next_col = 0
    while next_col in used_cols:
        next_col += 1
    place_queens(next_col, placed_pieces, solutions)
    if solutions:
        placed_pieces.extend(solutions[0][len(placed_pieces):])

def place_queens(col, placed_pieces, solutions):
    if col >= DIMENSION:
        if len(placed_pieces) == DIMENSION:
            solutions.append(placed_pieces.copy())
        return

    used_cols = {c for _, c in placed_pieces}
    while col in used_cols and col < DIMENSION:
        col += 1
    
    if col >= DIMENSION:
        return

    for row in range(DIMENSION):
        if is_valid_move(row, col, placed_pieces):
            placed_pieces.append((row, col))
            place_queens(col + 1, placed_pieces, solutions)
            placed_pieces.pop()

def is_valid_move(row, col, placed_pieces):
    for r, c in placed_pieces:
        if row == r or col == c or abs(row - r) == abs(col - c):
            return False
    return True

def display_random_solution(screen, placed_pieces):
    solution_files = [file for file in os.listdir(RESULTS_FOLDER) if file.startswith("solution_")]
    if solution_files:
        random_file = random.choice(solution_files)
        with open(os.path.join(RESULTS_FOLDER, random_file), "r") as file:
            for r, line in enumerate(file):
                for c, piece in enumerate(line.split()):
                    if piece == 'wQ':
                        placed_pieces.append((r, c))

def main(new_game=False):
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT + 25))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    load_images()
    running = True
    placing = False  
    placed_pieces = load_game_state(new_game)

    if not placed_pieces:  
        placed_pieces = []  
    else:
        placing = True  

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if 0 <= e.pos[0] <= 100 and HEIGHT <= e.pos[1] <= HEIGHT + 25:  # Place button
                    placing = True
                    placed_pieces = []
                elif 100 <= e.pos[0] <= 200 and HEIGHT <= e.pos[1] <= HEIGHT + 25:  # Result button
                    if placed_pieces:  
                        auto_place_remaining_pieces(placed_pieces)
                        placing = False
                elif 200 <= e.pos[0] <= 300 and HEIGHT <= e.pos[1] <= HEIGHT + 25:  # Clear button
                    placed_pieces = []  
                elif 300 <= e.pos[0] <= 400 and HEIGHT <= e.pos[1] <= HEIGHT + 25:  # Random button
                    placed_pieces.clear()
                    display_random_solution(screen, placed_pieces)
                elif 400 <= e.pos[0] <= 500 and HEIGHT <= e.pos[1] <= HEIGHT + 25:  # Quit button
                    save_game_state(placed_pieces)
                    running = False    
                if placing:
                    if e.button == 1:  # Left click
                        col = e.pos[0] // SQ_SIZE
                        row = e.pos[1] // SQ_SIZE
                        if (0 <= row < DIMENSION) and (0 <= col < DIMENSION) and is_valid_move(row, col, placed_pieces):
                            placed_pieces.append((row, col))
                    elif e.button == 3:  # Right click
                        if placed_pieces:
                            placed_pieces.pop()

        draw_game_state(screen, gs)
        draw_buttons(screen, placing)
        draw_placed_pieces(screen, placed_pieces)
        clock.tick(MAX_FPS)
        p.display.flip()

    if new_game:
        save_game_state(placed_pieces)

def load_game_state(new_game=False):
    try:
        if not new_game and os.path.exists("game_state.pickle"):
            with open("game_state.pickle", "rb") as f:
                return pickle.load(f)
    except Exception as e:
        print("Loading Fail:", e)
    return []

def save_game_state(placed_pieces):
    try:
        with open("game_state.pickle", "wb") as f:
            pickle.dump(placed_pieces, f)
    except Exception as e:
        print("Errors !! :", e)

if __name__ == "__main__":
    main()
