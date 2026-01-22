import pygame
import json
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("image/background.png")
background = pygame.transform.scale(background, (800, 600))

red = (255, 0, 0)
white = (255, 255, 255)
grey = (150, 150, 150)

# Bouton JOUER
bouton_rect = pygame.Rect(300, 450, 200, 80)

# Champ nom
input_rect = pygame.Rect(250, 300, 300, 50)
nom = ""

font = pygame.font.Font(None, 36)
active_input = False
running = True

# Curseur clignotant simple
cursor_visible = True
last_blink = time.time()

while running:
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            active_input = input_rect.collidepoint(event.pos)
            if bouton_rect.collidepoint(event.pos) and nom.strip() != "":
                print(f"Partie commencée pour {nom} !")

        if event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_BACKSPACE:
                nom = nom[:-1]
            else:
                nom += event.unicode

    # Curseur main
    if bouton_rect.collidepoint(pygame.mouse.get_pos()) and nom.strip() != "":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # Dessiner champ texte
    pygame.draw.rect(screen, white, input_rect, 2, border_radius=5)

    # Clignotement du curseur
    if time.time() - last_blink > 0.5:
        cursor_visible = not cursor_visible
        last_blink = time.time()

    # Afficher le texte ou le placeholder
    if nom == "":
        screen.blit(font.render("Entrez un pseudo", True, grey), (input_rect.x + 5, input_rect.y + 10))
        if active_input and cursor_visible:
            pygame.draw.line(screen, white, (input_rect.x + 5, input_rect.y + 10), (input_rect.x + 5, input_rect.y + 40), 2)
    else:
        text_surface = font.render(nom, True, white)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 10))
        if active_input and cursor_visible:
            cursor_x = input_rect.x + 5 + text_surface.get_width()
            pygame.draw.line(screen, white, (cursor_x, input_rect.y + 10), (cursor_x, input_rect.y + 40), 2)

    # Bouton JOUER
    couleur_bouton = grey if nom.strip() == "" else red
    pygame.draw.rect(screen, couleur_bouton, bouton_rect, border_radius=20)
    screen.blit(font.render(" JOUER", True, white), (bouton_rect.x + 50, bouton_rect.y + 25))

    pygame.display.flip()

pygame.quit()
