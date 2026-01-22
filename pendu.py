import sys
import pygame #import library 
import random


with open('words.txt', mode='r', encoding='utf-8') as f: #open file named words.txt choose mode (r)ead, (w)rite, encoding, with automatically close the file once the bloc is over
    random_word = random.choice(f.read().splitlines()).lower() #read the folder, splitlines \n make it a list and choose randomly in that list
guessed_letters = ""
lives = 7


def displayed_word(word, guesses):
    '''
    function that displays "-" or the according letter when called

    :param word: our random word generated previously
    :param guesses: input letters
    '''
    display = ""
    for letter in word:
        if letter in guesses:
            display += letter
        else:
            display += "-"
    return display

# random_word_displayed = displayed_word(random_word, guessed_letters)
# print(random_word_displayed)

pygame.init() #initialize pygame window 

screen = pygame.display.set_mode((800, 600)) #setting screen size
pygame.display.set_caption("Mon Premier Jeu Pygame")
font = pygame.font.Font(None, 200) #setup the font, none is default pygame font
text_render = font.render(displayed_word(random_word, guessed_letters), True, (255,55,255)) #render text, text, antialiasing true, color
text_rectangle = text_render.get_rect(center = (400, 300)) #compute the position of the box containing the text


game_on = True
game_over = False

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if we quit 
            game_on = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.unicode.isalpha(): # verify that the input is a letter and not a special key like SPACE or ESCAPE
                letter = event.unicode.lower() # add that input to the var and convert it in lowercase
                if letter not in guessed_letters:
                    guessed_letters += letter
                if letter not in random_word:
                    lives -= 1

                # Update the text image when a key is pressed
                text_render = font.render(displayed_word(random_word, guessed_letters), True, (255,55,255))
                text_rectangle = text_render.get_rect(center = (screen.get_width()//2, screen.get_height()//2))
    screen.fill((0, 0, 0)) # Clear the screen 
    screen.blit(text_render, text_rectangle) #draw the text can add the coordinates x and y 

    text_render_lives = font.render(str(lives), True, (20,20,255))
    text_rectangle_lives = text_render_lives.get_rect(topleft=(10, 10))
    screen.blit(text_render_lives, text_rectangle_lives)
    
    if lives == 0:
        game_over = True
        text_render_loss = font.render("Perdu", True, (255,55,255))
        text_rectangle_loss = text_render_loss.get_rect(midtop = (screen.get_width()//2, 0))
        screen.blit(text_render_loss, text_rectangle_loss)
    if "-" not in displayed_word(random_word, guessed_letters):
        game_over = True
        text_render_win = font.render("Gagné", True, (12,33,12))
        text_rectangle_win = text_render_win.get_rect(midbottom = (screen.get_width()//2, screen.get_height()))
        screen.blit(text_render_win, text_rectangle_win)

    pygame.display.flip() #continuously update the screen

pygame.quit()
sys.exit()