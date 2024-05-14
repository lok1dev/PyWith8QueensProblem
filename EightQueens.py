import pygame as p
import os
import ChessEngine
import random
import pickle

# Constants
WIDTH, HEIGHT = 512, 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30 
IMAGES = {}
RESULTS_FOLDER = "results"

# Initialize Pygame display settings
p.display.set_caption("Eight Queens")
p.display.set_icon(p.image.load("assets/piece/bQ.png"))

def loadImages():
    """Load and scale images for the pieces."""
    piece = 'wQ'
    img = p.image.load(os.path.join("assets/piece", f"{piece}.png"))
    IMAGES[piece] = p.transform.scale(img, (SQ_SIZE, SQ_SIZE))

def drawButtons(screen, placing):
    """Draws buttons on the screen."""
    colors = {"Place": "red", "Result": "blue", "Clear": "#CCCC00", "Random": "#606060", "Quit": "orange"}
    button_info = [("Place", 0), ("Result", 100), ("Clear", 200), ("Random", 300), ("Quit", 400)]
    
    for text, x_offset in button_info:
        rect = p.Rect(x_offset, HEIGHT, 120, 25)
        color = colors[text] if placing or text != "Place" else "green"
        p.draw.rect(screen, p.Color(color), rect)
        font = p.font.Font(None, 32)
        text_render = font.render(text, True, p.Color("white"))
        text_rect = text_render.get_rect(center=rect.center)
        text_rect.center = (text_rect.center[0] - 10, text_rect.center[1])
        screen.blit(text_render, text_rect)

def displayRandomSolution(screen, placed_pieces):
    """Displays a random solution from the saved solutions."""
    solution_files = [file for file in os.listdir(RESULTS_FOLDER) if file.startswith("solution_")]
    if solution_files:
        random_file = random.choice(solution_files)
        with open(os.path.join(RESULTS_FOLDER, random_file), "r") as file:
            for r, line in enumerate(file):
                for c, piece in enumerate(line.split()):
                    if piece == 'wQ':
                        placed_pieces.append((r, c))

def drawPlacedPieces(screen, placed_pieces):
    """Draws the placed pieces on the board."""
    for row, col in placed_pieces:
        screen.blit(IMAGES["wQ"], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawGameState(screen, gs):
    """Draws the current game state."""
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    """Draws the chess board."""
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    """Draws the pieces on the board."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawSolution(screen, n, placed_pieces):
    """Draws the solution from a file."""
    solution_file = f"solution_{n}.txt"
    remaining_pieces = {'wQ': (0, 0)} 
    if os.path.exists(solution_file):
        with open(solution_file, "r") as file:
            for r, line in enumerate(file):
                for c, piece in enumerate(line.split()):
                    if piece != '--':
                        remaining_pieces[piece] = (r, c)

    remaining_pieces = {piece: pos for piece, pos in remaining_pieces.items() if piece not in placed_pieces}

    if remaining_pieces:
        for piece, pos in remaining_pieces.items():
            screen.blit(IMAGES[piece], p.Rect(pos[1] * SQ_SIZE, pos[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    else:
        font = p.font.Font(None, 32)
        text = font.render("No solution", True, p.Color("red"))
        screen.blit(text, (300, 513))

def isValidMove(row, col, placed_pieces):
    """Checks if a move is valid."""
    for r, c in placed_pieces:
        if row == r or col == c or abs(row - r) == abs(col - c):
            return False
    return True

def main(new_game=False):
    """Main function to run the game."""
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT + 25))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    placing = False  
    placed_pieces = loadGameState(new_game)
    current_solution = 0  

    if not placed_pieces:  
        placed_pieces = []  
    else:
        placing = True  

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if 0 <= e.pos[0] <= 120 and HEIGHT <= e.pos[1] <= HEIGHT + 25:  # Place button
                    placing = True
                    placed_pieces = []
                elif 120 <= e.pos[0] <= 220 and HEIGHT <= e.pos[1] <= HEIGHT + 25:  # Result button
                    drawSolution(screen, current_solution, placed_pieces)
                    placing = False
                elif 220 <= e.pos[0] <= 320 and HEIGHT <= e.pos[1] <= HEIGHT + 25:  # Clear button
                    placed_pieces = []  
                elif 320 <= e.pos[0] <= 420 and HEIGHT <= e.pos[1] <= HEIGHT + 25:  # Random button
                    placed_pieces.clear()
                    displayRandomSolution(screen, placed_pieces)
                elif 420 <= e.pos[0] <= 520 and HEIGHT <= e.pos[1] <= HEIGHT + 25:  # Quit button
                    saveGameState(placed_pieces)
                    running = False    
                
                if placing:
                    if e.button == 1:  # Left click
                        col = e.pos[0] // SQ_SIZE
                        row = e.pos[1] // SQ_SIZE
                        if (0 <= row < DIMENSION) and (0 <= col < DIMENSION) and isValidMove(row, col, placed_pieces):
                            placed_pieces.append((row, col))
                    elif e.button == 3:  # Right click
                        if placed_pieces:
                            placed_pieces.pop()

        drawGameState(screen, gs)
        drawButtons(screen, placing)
        drawPlacedPieces(screen, placed_pieces)
        clock.tick(MAX_FPS)
        p.display.flip()

    if new_game:
        saveGameState(placed_pieces)

def loadGameState(new_game=False):
    """Loads the game state from a file."""
    try:
        if not new_game and os.path.exists("game_state.pickle"):
            with open("game_state.pickle", "rb") as f:
                placed_pieces = pickle.load(f)
            return placed_pieces
        else:
            return []
    except Exception as e:
        print("Loading Fail:", e)
        return []

def saveGameState(placed_pieces):
    """Saves the game state to a file."""
    try:
        with open("game_state.pickle", "wb") as f:
            pickle.dump(placed_pieces, f)
    except Exception as e:
        print("Errors !! :", e)

if __name__ == "__main__":
    placed_pieces = loadGameState()
    main()
