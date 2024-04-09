import pygame as p, sys
from button import Button
import EightQueens 
import KnightTour

p.init()

SCREEN = p.display.set_mode((512,512))

p.display.set_caption("GAME")
p.display.set_icon(p.image.load("assets/piece/bN.png"))

BG = p.image.load("assets/Home/Background-512width.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return p.font.Font("assets/font.ttf", size)

def Eight_Queens():
    while True:
        QUEEN_MOUSE_POS = p.mouse.get_pos()
        p.display.update()
    
def Knight_Tour():
    while True:
        KNIGHT_MOUSE_POS = p.mouse.get_pos()
        p.display.update()

def home_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = p.mouse.get_pos()

        MENU_TEXT = get_font(45).render("MAIN MENU", True, "#FFFFFF")
        MENU_RECT = MENU_TEXT.get_rect(center=(256, 180))

        QUEEN_BUTTON = Button(image=p.image.load("assets/Home/8Queens Rect.jpg"), pos=(256, 262), 
                            text_input="8 QUEENS", font=get_font(22), base_color="#d7fcd4", hovering_color="White")
        KNIGHT_BUTTON = Button(image=p.image.load("assets/Home/KnightTour Rect.jpg"), pos=(256, 346), 
                            text_input="KNIGHT's TOUR", font=get_font(24), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=p.image.load("assets/Home/Quit Rect.jpg"), pos=(256, 430), 
                            text_input="QUIT", font=get_font(22), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [QUEEN_BUTTON, KNIGHT_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if QUEEN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Eight_Queens(EightQueens.main())
                if KNIGHT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Knight_Tour(KnightTour.main())
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    p.quit()
                    sys.exit()

        p.display.update()

home_menu()