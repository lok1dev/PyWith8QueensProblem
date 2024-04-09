import pygame as p
import random
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30 
IMAGES = {}

p.display.set_caption("Knight's Tour")

p.display.set_icon(p.image.load("assets/piece/bN.png"))

def loadImages():
    pieces = ['wN', 'x.png']
    for piece in pieces:
        if piece == 'x.png':
            IMAGES[piece] = p.transform.scale(p.image.load("assets/piece/" + piece), (SQ_SIZE, SQ_SIZE))
        else:
            IMAGES[piece] = p.transform.scale(p.image.load("assets/piece/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def knight_tour(gs, start):
    path = []
    path.append(start)
    moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
             (-2, -1), (-1, -2), (1, -2), (2, -1)]
    while len(path) < DIMENSION * DIMENSION:
        possible_moves = []
        for move in moves:
            next_row = path[-1][0] + move[0]
            next_col = path[-1][1] + move[1]
            if 0 <= next_row < DIMENSION and 0 <= next_col < DIMENSION and (next_row, next_col) not in path:
                possible_moves.append((next_row, next_col))
        if possible_moves:
            next_move = random.choice(possible_moves)
            path.append(next_move)
        else:
            break
    return path

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

def drawKnightTour(screen, path, gs):
    for move in path:
        r, c = move
        screen.blit(IMAGES['wN'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        p.time.wait(300)
        gs.board[r][c] = 'x.png'
        drawGameState(screen, gs)

def showMessage(screen, message):
    p.font.init()
    font = p.font.SysFont('Arial', 30)
    text = font.render(message, True, p.Color('red'))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    p.display.flip()

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()  # Assuming you have the ChessEngine module implemented
    loadImages()
    running = True
    knight_tour_started = False
    knight_position = None
    knight_tour_path = None

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not knight_tour_started:
                    col = e.pos[0] // SQ_SIZE
                    row = e.pos[1] // SQ_SIZE
                    if 0 <= col < DIMENSION and 0 <= row < DIMENSION:
                        gs.board[row][col] = 'wN'
                        knight_position = (row, col)
                        knight_tour_started = True
                        knight_tour_path = knight_tour(gs, knight_position)

        drawGameState(screen, gs)
        if knight_tour_started:
            drawKnightTour(screen, knight_tour_path, gs)
            running = False
            showMessage(screen, "No Solution")

        clock.tick(MAX_FPS)
        p.display.flip()

    # Handle exit
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                return
            elif e.type == p.KEYDOWN:
                if e.key == p.K_RETURN:  # User pressed Enter
                    p.quit()
                    return

if __name__ == "__main__":
    main()
