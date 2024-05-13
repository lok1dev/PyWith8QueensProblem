import pygame as p
import sys
import EightQueens 
import KnightTour 
from button import Button

p.init()

SCREEN = p.display.set_mode((512, 512))
p.display.set_caption("GAME")
p.display.set_icon(p.image.load("assets/piece/bN.png"))
BG = p.image.load("assets/Home/Background-512width.jpg")

def get_font(size):
    return p.font.Font("assets/font.ttf", size)

def clear_screen():
    SCREEN.fill((0, 0, 0))

def create_button(image_path, pos, text_input, font, base_color, hovering_color):
    return Button(image=p.image.load(image_path), pos=pos, text_input=text_input,
                  font=font, base_color=base_color, hovering_color=hovering_color)

def home_menu():
    while True:
        clear_screen()
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = p.mouse.get_pos()

        MENU_TEXT = get_font(45).render("MAIN MENU", True, "#FFFFFF")
        MENU_RECT = MENU_TEXT.get_rect(center=(256, 180))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        buttons = [
            create_button("assets/Home/8Queens Rect.jpg", (256, 262), "8 QUEENS", get_font(22), "#d7fcd4", "White"),
            create_button("assets/Home/KnightTour Rect.jpg", (256, 346), "KNIGHT's TOUR", get_font(22), "#d7fcd4", "White"),
            create_button("assets/Home/Quit Rect.jpg", (256, 430), "QUIT", get_font(22), "#d7fcd4", "White")
        ]

        for button in buttons:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if buttons[0].checkForInput(MENU_MOUSE_POS):
                    queen_menu()
                if buttons[1].checkForInput(MENU_MOUSE_POS):
                    KnightTour.main()
                    home_menu()
                if buttons[2].checkForInput(MENU_MOUSE_POS):
                    p.quit()
                    sys.exit()

        p.display.update()

def queen_menu():
    while True:
        clear_screen()
        SCREEN.blit(BG, (0, 0))
        QUEEN_MOUSE_POS = p.mouse.get_pos()

        MENU_TEXT = get_font(38).render("EIGHT QUEENS", True, "#FFFFFF")
        MENU_RECT = MENU_TEXT.get_rect(center=(256, 180))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        buttons = [
            create_button("assets/Home/8Queens Rect.jpg", (256, 262), "NEW GAME", get_font(22), "#d7fcd4", "White"),
            create_button("assets/Home/8Queens Rect.jpg", (256, 346), "CONTINUE", get_font(22), "#d7fcd4", "White"),
            create_button("assets/Home/KnightTour Rect.jpg", (256, 430), "BACK TO MENU", get_font(22), "#d7fcd4", "White")
        ]

        for button in buttons:
            button.changeColor(QUEEN_MOUSE_POS)
            button.update(SCREEN)
        
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if buttons[0].checkForInput(QUEEN_MOUSE_POS):
                    EightQueens.main(new_game=True)
                    queen_menu()
                if buttons[1].checkForInput(QUEEN_MOUSE_POS):
                    EightQueens.main()
                if buttons[2].checkForInput(QUEEN_MOUSE_POS):
                    home_menu()

        p.display.update()


home_menu()
