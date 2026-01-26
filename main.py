import pygame
import random
import json
from pathlib import Path
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pendu")

# ===== Background =====
background = pygame.image.load("docs/image/background.png")
background = pygame.transform.scale(background, (800, 600))

game_background = pygame.image.load("docs/image/background2.png")
game_background = pygame.transform.scale(game_background, (800, 600))

# ===== Colors =====
white = (255, 255, 255)
grey = (150, 150, 150)
red = (255, 0, 0)
orange = (255, 165, 0)
green = (0, 255, 0)
black = (0, 0, 0)

font = pygame.font.Font(None, 36)

# ===== inputs =====
play_display = pygame.Rect(300, 450, 200, 80)
return_display = pygame.Rect(580, 520, 200, 60)

easy_display = pygame.Rect(250, 250, 300, 60)
medium_display = pygame.Rect(250, 330, 300, 60)
hard_display = pygame.Rect(250, 410, 300, 60)

# ===== Texts =====
input_rect = pygame.Rect(250, 300, 300, 50)
name = ""
active_input = False

visible_cursor = True
last_blink = time.time()

# ===== Status =====
status = "menu"
difficulty = None
game_end = False

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

def add_score(name):
    data = load_score()
    for player in data["scores"]:
        if player["nom"] == name:
            player["score"] += 1
            save_score(data)
            return
    data["scores"].append({"nom": name, "score": 1})
    save_score(data)

# ===== PENDU =====
word = ""
found_letters = []
used_letters = []
failure = 0
max_failures = 10

def new_game(diff):
    global word, found_letters, used_letters, failure, game_end , added_score
    word = get_random_word(diff)
    found_letters = []
    used_letters = []
    failure = 0
    game_end = False
    added_score = False

def draw_hangman(failure):
    if failure >= 1:
        pygame.draw.line(screen, white, (150, 450), (300, 450), 4)
    if failure >= 2:
        pygame.draw.line(screen, white, (225, 450), (225, 150), 4)
    if failure >= 3:
        pygame.draw.line(screen, white, (225, 150), (350, 150), 4)
    if failure >= 4:
        pygame.draw.line(screen, white, (350, 150), (350, 180), 4)
    if failure >= 5:
        pygame.draw.circle(screen, white, (350, 210), 30, 3)
    if failure >= 6:
        pygame.draw.line(screen, white, (350, 240), (350, 330), 3)
    if failure >= 7:
        pygame.draw.line(screen, white, (350, 260), (310, 300), 3)
    if failure >= 8:
        pygame.draw.line(screen, white, (350, 260), (390, 300), 3)
    if failure >= 9:
        pygame.draw.line(screen, white, (350, 330), (310, 390), 3)
    if failure >= 10:
        pygame.draw.line(screen, white, (350, 330), (390, 390), 3)

def draw_word():
    x = 220
    y = 470
    for letter in word:
        pygame.draw.rect(screen, white, (x, y, 40, 50), 2)
        if letter in found_letters:
            txt = font.render(letter.upper(), True, white)
            screen.blit(txt, (x + 10, y + 10))
        x += 50

def display_used_letter():
    x_start, y_start = 450, 10
    width, height = 330, 90

    pygame.draw.rect(screen, black, (x_start, y_start, width, height))
    pygame.draw.rect(screen, white, (x_start, y_start, width, height), 2)

    x, y = x_start + 10, y_start + 10
    for letter in used_letters:
        txt = font.render(letter.upper(), True, white)
        if x + txt.get_width() > x_start + width - 10:
            x = x_start + 10
            y += 30
        screen.blit(txt, (x, y))
        x += txt.get_width() + 10

# ===== Loop =====
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    cursor = pygame.SYSTEM_CURSOR_ARROW

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ===== Mouse =====
        if event.type == pygame.MOUSEBUTTONDOWN:
            if status == "menu":
                active_input = input_rect.collidepoint(event.pos)
                if play_display.collidepoint(event.pos) and name.strip():
                    status = "difficulty"

            elif status == "difficulty":
                if easy_display.collidepoint(event.pos):
                    difficulty = "easy"
                elif medium_display.collidepoint(event.pos):
                    difficulty = "medium"
                elif hard_display.collidepoint(event.pos):
                    difficulty = "hard"

                if difficulty:
                    new_game(difficulty)
                    status = "pendu"

            elif status == "pendu" and game_end:
                if return_display.collidepoint(event.pos):
                    status = "menu"
                    name = ""

        # ===== Keyboard =====
        if event.type == pygame.KEYDOWN:
            if status == "menu" and active_input:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

            elif status == "pendu" and not game_end:
                letter = event.unicode.lower()
                if letter.isalpha() and letter not in found_letters and letter not in used_letters:
                    if letter in word:
                        found_letters.append(letter)
                    else:
                        failure += 1
                        used_letters.append(letter)

    # ===== CURSEUR CLIGNOTANT =====
    if time.time() - last_blink > 0.5:
        visible_cursor = not visible_cursor
        last_blink = time.time()

    # ===== CURSEUR MAIN =====
    if status == "menu" and play_display.collidepoint(mouse_pos):
        cursor = pygame.SYSTEM_CURSOR_HAND
    if status == "difficulty" and (easy_display.collidepoint(mouse_pos) or medium_display.collidepoint(mouse_pos) or hard_display.collidepoint(mouse_pos)):
        cursor = pygame.SYSTEM_CURSOR_HAND
    if status == "pendu" and game_end and return_display.collidepoint(mouse_pos):
        cursor = pygame.SYSTEM_CURSOR_HAND

    pygame.mouse.set_cursor(cursor)

    # ===== Display =====
    screen.fill((0, 0, 0))

    if status == "menu":
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, white, input_rect, 2)
        txt = font.render(name if name else "Entrez un nom", True, white if name else grey)
        screen.blit(txt, (input_rect.x + 5, input_rect.y + 10))

        if active_input and visible_cursor:
            x = input_rect.x + 5 + font.size(name)[0]
            pygame.draw.line(screen, white, (x, input_rect.y + 10), (x, input_rect.y + 40), 2)

        pygame.draw.rect(screen, red if name else grey, play_display, border_radius=20)
        screen.blit(font.render("JOUER", True, white), (play_display.x + 60, play_display.y + 25))

    elif status == "difficulty":
        screen.blit(game_background, (0, 0))
        pygame.draw.rect(screen, green, easy_display, border_radius=15)
        pygame.draw.rect(screen, orange, medium_display, border_radius=15)
        pygame.draw.rect(screen, red, hard_display, border_radius=15)

        screen.blit(font.render("FACILE", True, white), (350, 265))
        screen.blit(font.render("MOYEN", True, white), (340, 345))
        screen.blit(font.render("DIFFICILE", True, white), (325, 425))

    elif status == "pendu":
        screen.blit(game_background, (0, 0))
        draw_hangman(failure)
        draw_word()
        display_used_letter()

        if failure >= max_failures:
            game_end = True
            screen.blit(font.render(f"{name}, tu as perdu", True, red), (200, 550))
        elif all(l in found_letters for l in word):
            game_end = True
            screen.blit(font.render(f"bravo {word} tu as gagné", True, green), (200, 550))
            if not added_score :
                add_score(name)  # <= ajout du score 
                added_score = True

        if game_end:
            pygame.draw.rect(screen, red, return_display, border_radius=15)
            screen.blit(font.render("RETOUR MENU", True, white), (590, 540))

    pygame.display.flip()

pygame.quit()