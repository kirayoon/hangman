import pygame
import random


# Initialize and create window
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


class Hangman(object):
    images = []
    for i in range(8):
        image = pygame.image.load('hangman_' + str(i) + '.png')
        images.append(image)

    def __init__(self):
        self.limbs = 0

    def draw(self, window):
        window.blit(pygame.transform.scale(self.images[self.limbs], (270, 270)), (90, 70))


class RandomWord(object):
    def __init__(self, filename):
        with open(filename) as file:
            words = file.read().splitlines()
            self.word = random.choice(words).upper()

    def draw_correct(self, window, guessed_true):
        display_word = ''
        for letter in self.word:
            if letter in guessed_true:
                display_word += letter + ' '
            else:
                display_word += '_ '
        right_text = game_font.render(display_word, True, BROWN)
        window.blit(right_text, (400, 200))

    @staticmethod
    def draw_wrong(window, wrong_guess):
        wrong_guesses = ''
        for letter in wrong_guess:
            wrong_guesses += letter + ' '
        wrong_text = game_font_small.render(wrong_guesses, True, LIGHT_BROWN)
        window.blit(wrong_text, (400, 300))


class Button(object):
    def __init__(self, x, y, letter, visible):
        self.x = x
        self.y = y
        self.letter = letter
        self.visible = visible
        self.radius = 20
        self.gap = 15

    def create_buttons(self):
        buttons = []
        start_x = round((800 - (self.radius * 2 + self.gap) * 13) / 2)
        start_y = 400
        for i in range(26):
            x_cord = start_x + self.gap * 2 + ((self.radius * 2 + self.gap) * (i % 13))
            y_cord = start_y + ((i // 13) * (self.gap + self.radius * 2))
            buttons.append([x_cord, y_cord, chr(65 + i), True])
        return buttons

    def draw(self, window):
        if self.visible:
            pygame.draw.circle(window, BLUE, (self.x, self.y), self.radius, 3)
            text = game_font_small.render(self.letter, True, BLUE)
            window.blit(text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2))

    def click(self, pos):
        mouse_x, mouse_y = pos
        distance = ((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2) ** 0.5
        if distance < self.radius:
            return True
        else:
            return False

    def set_visible(self, visible):
        self.visible = visible

    def get_visible(self):
        return self.visible

    def get_letter(self):
        return self.letter


class Game(object):
    def __init__(self):
        self.secret_word = RandomWord('wordlist.txt')
        self.hangman = Hangman()
        self.buttons = [Button(x, y, letter, visible) for x, y, letter, visible in Button(0, 0, '', True).create_buttons()]
        self.right_guesses = []
        self.wrong_guesses = []

    def draw(self):
        self.secret_word.draw_correct(win, self.right_guesses)
        self.secret_word.draw_wrong(win, self.wrong_guesses)
        self.hangman.draw(win)
        for button in self.buttons:
            button.draw(win)

    def check_won(self):
        won = True
        for letter in self.secret_word.word:
            if letter not in self.right_guesses:
                won = False
                break
        return won

    def end(self, won):
        if won:
            self.display_message('You won!')
        else:
            self.hangman.limbs = 7
            self.hangman.draw(win)
            pygame.display.update()
            self.display_message('You lost!')

    def display_message(self, message):
        pygame.draw.rect(win, BEIGE, (WIDTH / 2 - 100, HEIGHT/4 - 50, 400, 200))

        text1 = game_font.render(message, True, BROWN)
        word = "Word: " + self.secret_word.word
        text2 = game_font_small.render(word, True, BROWN)
        text3 = game_font.render("Click anywhere to play again", True, BROWN)
        win.blit(text1, (WIDTH / 2 - text1.get_width() / 2 + 160, HEIGHT / 4 - 50))
        win.blit(text2, (WIDTH / 2 - text2.get_width() / 2 + 160, 1.5*HEIGHT / 4 - 50))
        win.blit(text3, (WIDTH / 2 - text3.get_width() / 2 + 160, 2*HEIGHT / 4 - 50))
        pygame.display.update()
        self.reset()

    def reset(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.secret_word = RandomWord('wordlist.txt')
                    self.hangman = Hangman()
                    self.hangman.limbs = 0
                    self.right_guesses = []
                    self.wrong_guesses = []
                    for button in self.buttons:
                        button.set_visible(True)
                    self.run()

    def run(self):
        while self.hangman.limbs <= 7:
            win.fill(BEIGE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.click(mouse_pos):
                            button.set_visible(False)
                            if button.get_letter() in self.secret_word.word:
                                self.right_guesses.append(button.get_letter())
                            else:
                                self.wrong_guesses.append(button.get_letter())
                                self.hangman.limbs += 1

            self.draw()
            pygame.display.update()

            if self.check_won():
                self.end(True)
                break
            if self.hangman.limbs == 7:
                self.end(False)
                break


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
