import pygame
from src.pendu import display
from src.pendu import random_word

def init_font():
    return pygame.font.Font(None, 36)

mot = ""
lettres_trouvees = []
lettres_utilisees = []
erreurs = 0
erreurs_max = 10

def new_game(diff):
    global mot, lettres_trouvees, lettres_utilisees, erreurs, fin_jeu, score_ajoute
    mot = random_word.get_random_word(diff)
    lettres_trouvees = []
    lettres_utilisees = []
    erreurs = 0
    fin_jeu = False
    score_ajoute = False  

def draw_hangman(erreurs):
    if erreurs >= 1:
        pygame.draw.line(display.screen, display.white, (150, 450), (300, 450), 4)
    if erreurs >= 2:
        pygame.draw.line(display.screen, display.white, (225, 450), (225, 150), 4)
    if erreurs >= 3:
        pygame.draw.line(display.screen, display.white, (225, 150), (350, 150), 4)
    if erreurs >= 4:
        pygame.draw.line(display.screen, display.white, (350, 150), (350, 180), 4)
    if erreurs >= 5:
        pygame.draw.circle(display.screen, display.white, (350, 210), 30, 3)
    if erreurs >= 6:
        pygame.draw.line(display.screen, display.white, (350, 240), (350, 330), 3)
    if erreurs >= 7:
        pygame.draw.line(display.screen, display.white, (350, 260), (310, 300), 3)
    if erreurs >= 8:
        pygame.draw.line(display.screen, display.white, (350, 260), (390, 300), 3)
    if erreurs >= 9:
        pygame.draw.line(display.screen, display.white, (350, 330), (310, 390), 3)
    if erreurs >= 10:
        pygame.draw.line(display.screen, display.white, (350, 330), (390, 390), 3)

def draw_word():
    x = 220
    y = 470
    for lettre in mot:
        pygame.draw.rect(display.screen, display.white, (x, y, 40, 50), 2)
        if lettre in lettres_trouvees:
            txt = display.font.render(lettre.upper(), True, display.white)
            display.screen.blit(txt, (x + 10, y + 10))
        x += 50

def show_used_words():
    x_start, y_start = 450, 10
    largeur, hauteur = 330, 90

    pygame.draw.rect(display.screen, display.black, (x_start, y_start, largeur, hauteur))
    pygame.draw.rect(display.screen, display.white, (x_start, y_start, largeur, hauteur), 2)

    x, y = x_start + 10, y_start + 10
    for lettre in lettres_utilisees:
        txt = display.font.render(lettre.upper(), True, display.white)
        if x + txt.get_width() > x_start + largeur - 10:
            x = x_start + 10
            y += 30
        display.screen.blit(txt, (x, y))
        x += txt.get_width() + 10

