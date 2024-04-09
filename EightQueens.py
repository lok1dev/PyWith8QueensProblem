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
placed_pieces = []  # List to store user-placed pieces

p.display.set_caption("Eight Queens")

def loadImages():
    pieces = ['wQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("assets/piece/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def drawButtons(screen, placing):
    # Draw "Place" button
    p.draw.rect(screen, p.Color("green") if not placing else p.Color("red"), p.Rect(0, 512, 90, 25))
    font = p.font.Font(None, 32)
    text = font.render("Place", True, p.Color("white"))
    screen.blit(text, (15, 513))

    # Draw "Result" button
    p.draw.rect(screen, p.Color("blue"), p.Rect(90, 512, 100, 25))
    font = p.font.Font(None, 32)
    text = font.render("Result", True, p.Color("white"))
    screen.blit(text, (106, 513))

    # Draw "Clear" button
    p.draw.rect(screen, p.Color("#CCCC00"), p.Rect(190, 512, 100, 25))
    font = p.font.Font(None, 32)
    text = font.render("Clear", True, p.Color("white"))
    screen.blit(text, (206, 513))

    # Draw "Random" button
    p.draw.rect(screen, p.Color("#606060"), p.Rect(280, 512, 100, 25))
    font = p.font.Font(None, 32)
    text = font.render("Random", True, p.Color("white"))
    screen.blit(text, (286, 513))

def displayRandomSolution(screen, placed_pieces):
    solution_files = [file for file in os.listdir(RESULTS_FOLDER) if file.startswith("solution_")]
    if solution_files:
        random_file = random.choice(solution_files)
        with open(os.path.join(RESULTS_FOLDER, random_file), "r") as file:
            for r, line in enumerate(file):
                for c, piece in enumerate(line.split()):
                    if piece == 'wQ':
                        placed_pieces.append((r, c))

def drawPlacedPieces(screen, placed_pieces):
    for row, col in placed_pieces:
        # Vẽ hình ảnh quân cờ từ thư mục "images"
        piece_image = p.transform.scale(p.image.load("assets/piece/wQ.png"), (SQ_SIZE, SQ_SIZE))
        screen.blit(piece_image, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece !='--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawSolution(screen, n, placed_pieces):
    solution_file = f"solution_{n}.txt"
    remaining_pieces = {'wQ': (0, 0)}  # Initialize with all possible pieces
    if os.path.exists(solution_file):
        with open(solution_file, "r") as file:
            for r, line in enumerate(file):
                for c, piece in enumerate(line.split()):
                    if piece != '--':
                        remaining_pieces[piece] = (r, c)  # Record the position of the piece in the solution

    # Filter out placed pieces
    remaining_pieces = {piece: pos for piece, pos in remaining_pieces.items() if piece not in placed_pieces}

    # Now display remaining pieces
    for piece, pos in remaining_pieces.items():
        screen.blit(IMAGES[piece], p.Rect(pos[1] * SQ_SIZE, pos[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))


    # Now display remaining pieces
    for piece, pos in remaining_pieces.items():
        if piece not in placed_pieces:  # Only display if not placed by the user
            screen.blit(IMAGES[piece], p.Rect(pos[1] * SQ_SIZE, pos[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def main():
    # Initialize the game state
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT + 25))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True

    placing = False  # Flag to track whether user is in "placing" mode
    current_solution = 1
    placed_pieces = []  # Khai báo placed_pieces ở mức độ toàn cục trước khi sử dụng

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if 90 <= e.pos[0] <= 190 and 512 <= e.pos[1] <= 537:  # Check if "Results" button clicked
                    drawSolution(screen, current_solution, placed_pieces)
                    placing = False
                elif 190 <= e.pos[0] <= 290 and 512 <= e.pos[1] <= 537:  # Check if "Clear" button clicked
                    placed_pieces = []  # Xóa tất cả các quân cờ đã đặt trước đó   
                elif 280 <= e.pos[0] <= 380 and 512 <= e.pos[1] <= 537:  # Check if "Random" button clicked
                    placed_pieces.clear()
                    displayRandomSolution(screen, placed_pieces)
                elif 0 <= e.pos[0] <= 90 and 512 <= e.pos[1] <= 537:  # Check if "Place" button clicked
                    placing = True
                    placed_pieces = []  # Xóa tất cả các quân cờ đã đặt trước đó    

            if placing:
                if e.type == p.MOUSEBUTTONUP:  # If in "placing" mode and mouse released
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
