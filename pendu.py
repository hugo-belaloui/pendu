import sys
import pygame #import library 
import random


with open('words.txt', mode='r', encoding='utf-8') as f: #open file named words.txt choose mode (r)ead, (w)rite, encoding, with automatically close the file once the bloc is over
    random_word = random.choice(f.read().splitlines()).lower() #read the folder, splitlines \n make it a list and choose randomly in that list

guessed_letters = ""

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
while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if we quit 
            game_on = False
        if event.type == pygame.KEYDOWN:
            guessed_letters += event.unicode
            # Update the text image when a key is pressed
            text_render = font.render(displayed_word(random_word, guessed_letters), True, (255,55,255))
            text_rectangle = text_render.get_rect(center = (400, 300))

    screen.fill((0, 0, 0)) # Clear the screen 
    screen.blit(text_render, text_rectangle) #draw the text can add the coordinates x and y 
    pygame.display.flip() #continuously update the screen

pygame.quit()
sys.exit()