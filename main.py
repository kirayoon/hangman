import pygame
import os
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# colors and fonts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (100, 71, 48)
LIGHT_BROWN = (169, 140, 98)
BLUE = (69, 88, 96)
BEIGE = (234, 226, 200)
game_font = pygame.font.SysFont('comicsans', 30)
game_font_small = pygame.font.SysFont('comicsans', 20)

# load images
images = []
for i in range(8):
    image = pygame.image.load('hangman_' + str(i) + '.png')
    images.append(image)

# button variables
RADIUS = 20
GAP = 15
letters = []
start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 400
for i in range(26):
    x_cord = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y_cord = start_y + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x_cord, y_cord, chr(65 + i), True])

# globals
limbs = 0
words = ['DEVELOPER', 'DEVELOPER', 'DEVELOPER']
word = random.choice(words)
buttons = []
guessed_true = []
guessed_false = []


def draw():
    win.fill(BEIGE)
    win.blit(pygame.transform.scale(images[limbs], (270, 270)), (90, 70))

    # draw word
    display_word = ''
    for letter in word:
        if letter in guessed_true:
            display_word += letter + ' '
        else:
            display_word += '_ '
    right_text = game_font.render(display_word, True, BROWN)
    win.blit(right_text, (400, 200))

    # draw wrong guesses
    wrong_guesses = ''
    for letter in guessed_false:
        wrong_guesses += letter + ' '
    wrong_text = game_font_small.render(wrong_guesses, True, LIGHT_BROWN)
    win.blit(wrong_text, (400, 300))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLUE, (x, y), RADIUS, 3)
            text = game_font.render(ltr, True, BLUE)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    pygame.display.update()


def end(won):
    if won:
        display_message("You Won!")
    else:
        display_message("You Lost!")
    reset()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(BEIGE)
    text = game_font.render(message, True, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def reset():
    global limbs, guessed_true, guessed_false, word
    limbs = 0
    guessed_true = []
    guessed_false = []
    word = random.choice(words)
    for letter in letters:
        letter[3] = True


# game loop
def main():
    global limbs

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in letters:
                    x_pos, y_pos, ltr, visible = letter
                    distance = math.sqrt((x_pos - mouse_x) ** 2 + (y_pos - mouse_y) ** 2)
                    if distance < RADIUS:
                        letter[3] = False
                        guessed_true.append(ltr)
                        if ltr not in word:
                            guessed_false.append(ltr)
                            limbs += 1

        draw()

        # check if won
        won = True
        for letter in word:
            if letter not in guessed_true:
                won = False
                break

        if won:
            end(True)
            break

        if limbs == 6:
            pygame.time.delay(1000)
            limbs = 7
            draw()
            end(False)
            break


while True:
    win.fill(BEIGE)
    text = game_font.render("Click anywhere to start", True, BROWN)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            main()
