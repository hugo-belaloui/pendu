import pygame
import random
import json
from pathlib import Path
import time
import sys
ROOT = Path(__file__).resolve().parents[2]   # <--- ici
sys.path.append(str(ROOT))

from src.pendu import score
from src.pendu import random_word
from src.pendu import pendu

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pendu")

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
score_ajoute = False   # ✅ FLAG IMPORTANT

# ===== JSON =====
words_file = Path(__file__).resolve().parent / "words.json"
score_file = Path(__file__).resolve().parent / "score.json"

random_word.load_words()

random_word.get_random_word()


score.load_score()

score.save_score()


score.add_score()



pendu.new_game()

pendu.draw_hangman()


pendu.draw_word()

pendu.show_used_words()

# ===== BOUCLE PRINCIPALE =====
running = True
while running:
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
                    pendu.new_game(difficulte)
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
                if lettre.isalpha() and lettre not in pendu.lettres_trouvees and lettre not in pendu.lettres_utilisees:
                    if lettre in pendu.mot:
                        pendu.lettres_trouvees.append(lettre)
                    else:
                        erreurs += 1
                        pendu.lettres_utilisees.append(lettre)

    # ===== AFFICHAGE =====
    screen.fill(black)

    if etat == "menu":
        pygame.draw.rect(screen, white, input_rect, 2)
        txt = font.render(nom if nom else "Entrez un nom", True, white if nom else grey)
        screen.blit(txt, (input_rect.x + 5, input_rect.y + 10))

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
        pendu.draw_hangman(erreurs)
        pendu.draw_word()
        pendu.show_used_words()

        if pendu.erreurs >= pendu.erreurs_max:
            fin_jeu = True
            screen.blit(font.render(f"{nom} TU AS PERDU", True, red), (330, 550))

        elif all(l in pendu.lettres_trouvees for l in pendu.mot):
            fin_jeu = True
            screen.blit(font.render(f"BRAVO {nom} TU AS GAGNÉ", True, green), (330, 550))

            if not score_ajoute:   
                score.add_score(nom)
                score_ajoute = True

        if fin_jeu:
            pygame.draw.rect(screen, red, bouton_retour, border_radius=15)
            screen.blit(font.render("RETOUR MENU", True, white), (590, 540))

    pygame.display.flip()

pygame.quit()
