import pygame
import random
import json
from pathlib import Path
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pendu")

# ===== IMAGES =====
background = pygame.image.load("image/background.png")
background = pygame.transform.scale(background, (800, 600))

background_jeu = pygame.image.load("image/background2.png")
background_jeu = pygame.transform.scale(background_jeu, (800, 600))

# ===== COULEURS =====
white = (255, 255, 255)
grey = (150, 150, 150)
red = (255, 0, 0)
orange = (255, 165, 0)
green = (0, 255, 0)
black = (0, 0, 0)

font = pygame.font.Font(None, 36)

# ===== BOUTONS =====
bouton_jouer = pygame.Rect(300, 450, 200, 80)
bouton_retour = pygame.Rect(580, 520, 200, 60)

facile_btn = pygame.Rect(250, 250, 300, 60)
moyen_btn = pygame.Rect(250, 330, 300, 60)
difficile_btn = pygame.Rect(250, 410, 300, 60)

# ===== CHAMP TEXTE =====
input_rect = pygame.Rect(250, 300, 300, 50)
nom = ""
active_input = False

cursor_visible = True
last_blink = time.time()

# ===== ETATS =====
etat = "menu"
difficulte = None
fin_jeu = False

added_score = False

# ===== JSON =====
words_file = Path(__file__).resolve().parent / "words.json"
score_file = Path(__file__).resolve().parent / "score.json"

def load_words():
    with open(words_file, "r", encoding="utf-8") as f:
        return json.load(f)

def get_random_word(diff):
    words = load_words()
    return random.choice(words[diff])

def load_score():
    if not score_file.exists():
        return {"scores": []}
    with open(score_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_score(data):
    with open(score_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_score(nom):
    data = load_score()
    for player in data["scores"]:
        if player["nom"] == nom:
            player["score"] += 1
            save_score(data)
            return
    data["scores"].append({"nom": nom, "score": 1})
    save_score(data)

# ===== PENDU =====
mot = ""
lettres_trouvees = []
lettres_utilisees = []
erreurs = 0
erreurs_max = 10

def new_game(diff):
    global mot, lettres_trouvees, lettres_utilisees, erreurs, fin_jeu
    mot = get_random_word(diff)
    lettres_trouvees = []
    lettres_utilisees = []
    erreurs = 0
    fin_jeu = False
    added_score = False

def dessiner_pendu(erreurs):
    if erreurs >= 1:
        pygame.draw.line(screen, white, (150, 450), (300, 450), 4)
    if erreurs >= 2:
        pygame.draw.line(screen, white, (225, 450), (225, 150), 4)
    if erreurs >= 3:
        pygame.draw.line(screen, white, (225, 150), (350, 150), 4)
    if erreurs >= 4:
        pygame.draw.line(screen, white, (350, 150), (350, 180), 4)
    if erreurs >= 5:
        pygame.draw.circle(screen, white, (350, 210), 30, 3)
    if erreurs >= 6:
        pygame.draw.line(screen, white, (350, 240), (350, 330), 3)
    if erreurs >= 7:
        pygame.draw.line(screen, white, (350, 260), (310, 300), 3)
    if erreurs >= 8:
        pygame.draw.line(screen, white, (350, 260), (390, 300), 3)
    if erreurs >= 9:
        pygame.draw.line(screen, white, (350, 330), (310, 390), 3)
    if erreurs >= 10:
        pygame.draw.line(screen, white, (350, 330), (390, 390), 3)

def dessiner_mot():
    x = 220
    y = 470
    for lettre in mot:
        pygame.draw.rect(screen, white, (x, y, 40, 50), 2)
        if lettre in lettres_trouvees:
            txt = font.render(lettre.upper(), True, white)
            screen.blit(txt, (x + 10, y + 10))
        x += 50

def afficher_lettres_utilisees():
    x_start, y_start = 450, 10
    largeur, hauteur = 330, 90

    pygame.draw.rect(screen, black, (x_start, y_start, largeur, hauteur))
    pygame.draw.rect(screen, white, (x_start, y_start, largeur, hauteur), 2)

    x, y = x_start + 10, y_start + 10
    for lettre in lettres_utilisees:
        txt = font.render(lettre.upper(), True, white)
        if x + txt.get_width() > x_start + largeur - 10:
            x = x_start + 10
            y += 30
        screen.blit(txt, (x, y))
        x += txt.get_width() + 10

# ===== BOUCLE =====
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    cursor = pygame.SYSTEM_CURSOR_ARROW

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ===== SOURIS =====
        if event.type == pygame.MOUSEBUTTONDOWN:
            if etat == "menu":
                active_input = input_rect.collidepoint(event.pos)
                if bouton_jouer.collidepoint(event.pos) and nom.strip():
                    etat = "difficulte"

            elif etat == "difficulte":
                if facile_btn.collidepoint(event.pos):
                    difficulte = "easy"
                elif moyen_btn.collidepoint(event.pos):
                    difficulte = "medium"
                elif difficile_btn.collidepoint(event.pos):
                    difficulte = "hard"

                if difficulte:
                    new_game(difficulte)
                    etat = "pendu"

            elif etat == "pendu" and fin_jeu:
                if bouton_retour.collidepoint(event.pos):
                    etat = "menu"
                    nom = ""

        # ===== CLAVIER =====
        if event.type == pygame.KEYDOWN:
            if etat == "menu" and active_input:
                if event.key == pygame.K_BACKSPACE:
                    nom = nom[:-1]
                else:
                    nom += event.unicode

            elif etat == "pendu" and not fin_jeu:
                lettre = event.unicode.lower()
                if lettre.isalpha() and lettre not in lettres_trouvees and lettre not in lettres_utilisees:
                    if lettre in mot:
                        lettres_trouvees.append(lettre)
                    else:
                        erreurs += 1
                        lettres_utilisees.append(lettre)

    # ===== CURSEUR CLIGNOTANT =====
    if time.time() - last_blink > 0.5:
        cursor_visible = not cursor_visible
        last_blink = time.time()

    # ===== CURSEUR MAIN =====
    if etat == "menu" and bouton_jouer.collidepoint(mouse_pos):
        cursor = pygame.SYSTEM_CURSOR_HAND
    if etat == "difficulte" and (facile_btn.collidepoint(mouse_pos) or moyen_btn.collidepoint(mouse_pos) or difficile_btn.collidepoint(mouse_pos)):
        cursor = pygame.SYSTEM_CURSOR_HAND
    if etat == "pendu" and fin_jeu and bouton_retour.collidepoint(mouse_pos):
        cursor = pygame.SYSTEM_CURSOR_HAND

    pygame.mouse.set_cursor(cursor)

    # ===== AFFICHAGE =====
    screen.fill((0, 0, 0))

    if etat == "menu":
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, white, input_rect, 2)
        txt = font.render(nom if nom else "Entrez un nom", True, white if nom else grey)
        screen.blit(txt, (input_rect.x + 5, input_rect.y + 10))

        if active_input and cursor_visible:
            x = input_rect.x + 5 + font.size(nom)[0]
            pygame.draw.line(screen, white, (x, input_rect.y + 10), (x, input_rect.y + 40), 2)

        pygame.draw.rect(screen, red if nom else grey, bouton_jouer, border_radius=20)
        screen.blit(font.render("JOUER", True, white), (bouton_jouer.x + 60, bouton_jouer.y + 25))

    elif etat == "difficulte":
        pygame.draw.rect(screen, green, facile_btn, border_radius=15)
        pygame.draw.rect(screen, orange, moyen_btn, border_radius=15)
        pygame.draw.rect(screen, red, difficile_btn, border_radius=15)

        screen.blit(font.render("FACILE", True, white), (350, 265))
        screen.blit(font.render("MOYEN", True, white), (340, 345))
        screen.blit(font.render("DIFFICILE", True, white), (325, 425))

    elif etat == "pendu":
        dessiner_pendu(erreurs)
        dessiner_mot()
        afficher_lettres_utilisees()

        if erreurs >= erreurs_max:
            fin_jeu = True
            screen.blit(font.render(f"{nom}, tu as perdu", True, red), (200, 550))
        elif all(l in lettres_trouvees for l in mot):
            fin_jeu = True
            screen.blit(font.render(f"bravo {nom} tu as gagné", True, green), (200, 550))
            if not added_score :
                add_score(nom)  # <= ajout du score 
                added_score = True

        if fin_jeu:
            pygame.draw.rect(screen, red, bouton_retour, border_radius=15)
            screen.blit(font.render("RETOUR MENU", True, white), (590, 540))

    pygame.display.flip()

pygame.quit()