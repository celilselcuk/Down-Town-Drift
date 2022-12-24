import pygame
from pygame import mixer


pygame.init()

# create a screen
screen = pygame.display.set_mode((600, 600))

# Title and Icon
pygame.display.set_caption("Cars!")
icon = pygame.image.load('001-racing-car.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('background image.png')

# game map
map = pygame.image.load('')

# background music
mixer.music.load('background song.wav')
mixer.music.play(-1)

my_font = pygame.font.SysFont('bahnschrift', 50)
text_surface = my_font.render('Down Town Drift', False, (255, 255, 255))

my_font_start = pygame.font.SysFont('bahnschrift', 30)
text_avatar = my_font_start.render('Press A to view Avatar!', False, (255, 255, 255))

text_tutorial = my_font_start.render('Press T to start Tutorial!', False, (255, 255, 255))

text_start = my_font_start.render('Press SPACE to start Game!', False, (255, 255, 255))

avatar_title = my_font.render('Avatar', False, (255, 255, 255))
start_esc = my_font_start.render('ESC', False, (255, 255, 255))

tutorial_title = my_font.render('Tutorial', False, (255, 255, 255))

game_title = my_font.render('Game', False, (255, 255, 255))

# loading bar screen

sprites = [pygame.image.load('pixil-frame-0.png'),
           pygame.image.load('pixil-frame-1.png'),
           pygame.image.load('pixil-frame-2.png'),
           pygame.image.load('pixil-frame-3.png'),
           pygame.image.load('pixil-frame-4.png'),
           pygame.image.load('pixil-frame-5.png'),
           pygame.image.load('pixil-frame-6.png'),
           pygame.image.load('pixil-frame-7.png')]

counter = 0

# player
red_car = pygame.image.load('red car.png')
blue_car = pygame.image.load('blue car.png')
green_car = pygame.image.load('green car.png')
orange_car = pygame.image.load('orange car.png')
purple_car = pygame.image.load('purple car.png')
grey_car = pygame.image.load('grey car.png')

car_x = 300
car_y = 300

current_car = red_car

game_start_screen = True
avatar_screen = False
tutorial_screen = False
game_screen = False
purple = (221, 160, 221)
black = (0, 0, 0)
grey = (100, 100, 100)


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):

        action = False

        # finding mouse position

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


red_car_button = Button(80, 260, red_car)
blue_car_button = Button(240, 260, blue_car)
green_car_button = Button(400, 260, green_car)
orange_car_button = Button(80, 400, orange_car)
purple_car_button = Button(240, 400, purple_car)
grey_car_button = Button(400, 400, grey_car)


def loading():
    global counter
    loading_message = my_font.render('Loading...', False, (255, 255, 255))
    pygame.draw.rect(screen, grey, pygame.Rect(195, 108, 220, 60))
    pygame.draw.rect(screen, purple, pygame.Rect(195, 108, 220, 60), 3)
    screen.blit(loading_message, (200, 100))

    current_sprite = sprites[int(counter)]

    if counter < len(sprites):
        screen.blit(current_sprite, (110, 200))

    if counter + 1 > len(sprites):
        counter = 0

    counter += 0.1


def fade_screen(width, height):
    fade = pygame.Surface((width, height))
    fade.fill(black)
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        loading()
        pygame.display.update()


def start_screen():
    pygame.draw.rect(screen, black, pygame.Rect(107, 38, 375, 55))
    pygame.draw.rect(screen, purple, pygame.Rect(107, 38, 375, 55), 3)
    screen.blit(text_surface, (109, 30))
    pygame.draw.rect(screen, black, pygame.Rect(112, 300, 400, 45))
    pygame.draw.rect(screen, purple, pygame.Rect(112, 300, 400, 45), 3)
    screen.blit(text_start, (120, 300))
    pygame.draw.rect(screen, black, pygame.Rect(112, 500, 345, 45))
    pygame.draw.rect(screen, purple, pygame.Rect(112, 500, 345, 45), 3)
    screen.blit(text_tutorial, (120, 500))
    pygame.draw.rect(screen, black, pygame.Rect(112, 400, 335, 45))
    pygame.draw.rect(screen, purple, pygame.Rect(112, 400, 335, 45), 3)
    screen.blit(text_avatar, (120, 400))


def game():
    pygame.draw.rect(screen, black, pygame.Rect(225, 27, 138, 47))
    pygame.draw.rect(screen, purple, pygame.Rect(225, 27, 138, 47), 3)
    screen.blit(game_title, (230, 18))
    pygame.draw.rect(screen, black, pygame.Rect(48, 30, 60, 40))
    pygame.draw.rect(screen, purple, pygame.Rect(48, 30, 60, 40), 3)
    screen.blit(start_esc, (50, 30))
    player()


def tutorial():
    pygame.draw.rect(screen, black, pygame.Rect(207, 27, 180, 47))
    pygame.draw.rect(screen, purple, pygame.Rect(207, 27, 180, 47), 3)
    screen.blit(tutorial_title, (210, 18))
    pygame.draw.rect(screen, black, pygame.Rect(48, 30, 60, 40))
    pygame.draw.rect(screen, purple, pygame.Rect(48, 30, 60, 40), 3)
    screen.blit(start_esc, (50, 30))
    player()


def avatar():
    # title
    pygame.draw.rect(screen, black, pygame.Rect(225, 27, 157, 47))
    pygame.draw.rect(screen, purple, pygame.Rect(225, 27, 157, 47), 3)
    screen.blit(avatar_title, (230, 18))
    # esc
    pygame.draw.rect(screen, black, pygame.Rect(48, 30, 60, 40))
    pygame.draw.rect(screen, purple, pygame.Rect(48, 30, 60, 40), 3)
    screen.blit(start_esc, (50, 30))
    # customise box
    pygame.draw.rect(screen, grey, pygame.Rect(50, 250, 500, 290))
    pygame.draw.rect(screen, purple, pygame.Rect(50, 250, 500, 290), 5)
    # current car
    pygame.draw.rect(screen, grey, pygame.Rect(200, 100, 180, 100))
    pygame.draw.rect(screen, purple, pygame.Rect(200, 100, 180, 100), 2)
    screen.blit(current_car, (225, 95))


def player():
    screen.blit(current_car, (car_x, car_y))


running = True
while running:

    screen.blit(background, (0, 0))

    if game_start_screen:
        start_screen()
    if avatar_screen:
        avatar()
    if tutorial_screen:
        tutorial()
    if game_screen:
        game()

    if avatar_screen:
        if red_car_button.draw():
            current_car = red_car

        if blue_car_button.draw():
            current_car = blue_car

        if green_car_button.draw():
            current_car = green_car

        if orange_car_button.draw():
            current_car = orange_car

        if purple_car_button.draw():
            current_car = purple_car

        if grey_car_button.draw():
            current_car = grey_car

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            # avatar screen
            if game_start_screen:
                if event.key == pygame.K_a:
                    button_sound = mixer.Sound('button sound.wav')
                    button_sound.play()
                    fade_screen(600, 600)
                    game_start_screen = False
                    tutorial_screen = False
                    game_screen = False
                    avatar_screen = True
                # tutorial screen
            if game_start_screen:
                if event.key == pygame.K_t:
                    button_sound = mixer.Sound('button sound.wav')
                    button_sound.play()
                    fade_screen(600, 600)
                    game_start_screen = False
                    game_screen = False
                    avatar_screen = False
                    tutorial_screen = True
                # game screen
            if game_start_screen:
                if event.key == pygame.K_SPACE:
                    button_sound = mixer.Sound('button sound.wav')
                    button_sound.play()
                    fade_screen(600, 600)
                    game_start_screen = False
                    tutorial_screen = False
                    avatar_screen = False
                    game_screen = True

        # go back to starting screen
        if not game_start_screen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    button_sound = mixer.Sound('button sound.wav')
                    button_sound.play()
                    tutorial_screen = False
                    avatar_screen = False
                    game_screen = False
                    game_start_screen = True

        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
