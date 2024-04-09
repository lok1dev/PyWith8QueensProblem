import pygame as p
import os
import ChessEngine
import random

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30 
IMAGES = {}
RESULTS_FOLDER = "results"
placed_pieces = []

p.display.set_caption("Eight Queens")
p.display.set_icon(p.image.load("assets/piece/bQ.png"))

# Loads and scales chess piece images from the assets folder.
def loadImages():
    pieces = ['wQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("assets/piece/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# Draws the action buttons 
def drawButtons(screen, placing):
    p.draw.rect(screen, p.Color("green") if not placing else p.Color("red"), p.Rect(0, 512, 90, 25))
    font = p.font.Font(None, 32)
    text = font.render("Place", True, p.Color("white"))
    screen.blit(text, (15, 513))

    p.draw.rect(screen, p.Color("blue"), p.Rect(90, 512, 100, 25))
    font = p.font.Font(None, 32)
    text = font.render("Result", True, p.Color("white"))
    screen.blit(text, (106, 513))

    p.draw.rect(screen, p.Color("#CCCC00"), p.Rect(190, 512, 100, 25))
    font = p.font.Font(None, 32)
    text = font.render("Clear", True, p.Color("white"))
    screen.blit(text, (206, 513))

    p.draw.rect(screen, p.Color("#606060"), p.Rect(280, 512, 100, 25))
    font = p.font.Font(None, 32)
    text = font.render("Random", True, p.Color("white"))
    screen.blit(text, (286, 513))

# Random solution 
def displayRandomSolution(screen, placed_pieces):
    solution_files = [file for file in os.listdir(RESULTS_FOLDER) if file.startswith("solution_")]
    if solution_files:
        random_file = random.choice(solution_files)
        with open(os.path.join(RESULTS_FOLDER, random_file), "r") as file:
            for r, line in enumerate(file):
                for c, piece in enumerate(line.split()):
                    if piece == 'wQ':
                        placed_pieces.append((r, c))

# Draws the placed pieces on the board
def drawPlacedPieces(screen, placed_pieces):
    for row, col in placed_pieces:
        piece_image = p.transform.scale(p.image.load("assets/piece/wQ.png"), (SQ_SIZE, SQ_SIZE))
        screen.blit(piece_image, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draws the chess board and pieces
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

# Draws the chess board
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draws the chess pieces
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece !='--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draws the solution from the solution file
def drawSolution(screen, n, placed_pieces):
    solution_file = f"solution_{n}.txt"
    remaining_pieces = {'wQ': (0, 0)} 
    if os.path.exists(solution_file):
        with open(solution_file, "r") as file:
            for r, line in enumerate(file):
                for c, piece in enumerate(line.split()):
                    if piece != '--':
                        remaining_pieces[piece] = (r, c)

    remaining_pieces = {piece: pos for piece, pos in remaining_pieces.items() if piece not in placed_pieces}

    for piece, pos in remaining_pieces.items():
        screen.blit(IMAGES[piece], p.Rect(pos[1] * SQ_SIZE, pos[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT + 25))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True

    placing = False  
    current_solution = 1
    placed_pieces = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if 90 <= e.pos[0] <= 190 and 512 <= e.pos[1] <= 537:  
                    drawSolution(screen, current_solution, placed_pieces)
                    placing = False
                elif 190 <= e.pos[0] <= 290 and 512 <= e.pos[1] <= 537:  
                    placed_pieces = []  
                elif 280 <= e.pos[0] <= 380 and 512 <= e.pos[1] <= 537:  
                    placed_pieces.clear()
                    displayRandomSolution(screen, placed_pieces)
                elif 0 <= e.pos[0] <= 90 and 512 <= e.pos[1] <= 537:  
                    placing = True
                    placed_pieces = []   

            if placing:
                if e.type == p.MOUSEBUTTONUP:  
                    col = e.pos[0] // SQ_SIZE
                    row = e.pos[1] // SQ_SIZE
                    if (0 <= row < DIMENSION) and (0 <= col < DIMENSION):
                        placed_pieces.append((row, col))

        drawGameState(screen, gs)
        drawButtons(screen, placing)
        drawPlacedPieces(screen, placed_pieces)
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()
