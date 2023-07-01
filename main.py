import pygame
import random
from pygame import mixer


pygame.init()

# create a screen
screen = pygame.display.set_mode((600, 600))

# Title and Icon
pygame.display.set_caption("Cars!")
icon = pygame.image.load('Menu design/001-racing-car.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('Menu design/background image.png')

# game map
game_map = pygame.image.load('Level maps/game map.png')

# background music
mixer.music.load('Sound/background song.wav')
mixer.music.play(-1)

# score variables
score = 0


# difficulty variables
easy = True
medium = False
hard = False
extreme = False

# general variables
next_page_arrow = pygame.image.load('Menu design/next page arrow.png')
go_back_arrow = pygame.image.load('Menu design/go back arrow.png')
no_collide = True
game_start_screen = True
avatar_screen = False
avatar_screen_two = False
tutorial_screen = False
game_screen = False
purple = (221, 160, 221)
black = (0, 0, 0)
grey = (100, 100, 100)

# Fonts and text
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

# loading bar variables

sprites = [pygame.image.load('Animation/Loading screen/pixil-frame-0.png'),
           pygame.image.load('Animation/Loading screen/pixil-frame-1.png'),
           pygame.image.load('Animation/Loading screen/pixil-frame-2.png'),
           pygame.image.load('Animation/Loading screen/pixil-frame-3.png'),
           pygame.image.load('Animation/Loading screen/pixil-frame-4.png'),
           pygame.image.load('Animation/Loading screen/pixil-frame-5.png'),
           pygame.image.load('Animation/Loading screen/pixil-frame-6.png'),
           pygame.image.load('Animation/Loading screen/pixil-frame-7.png')]

counter = 0

# car
red_car = pygame.image.load('Cars/red car.png')
blue_car = pygame.image.load('Cars/blue car.png')
green_car = pygame.image.load('Cars/green car.png')
orange_car = pygame.image.load('Cars/orange car.png')
purple_car = pygame.image.load('Cars/purple car.png')
grey_car = pygame.image.load('Cars/grey car.png')
current_car = red_car
car_x = 10
car_y = 245

# obstacle variables
oil = pygame.image.load('Obstacles/oil.png')
blue_obs = pygame.image.load('Obstacles/blue obstacle.png')
red_obs = pygame.image.load('Obstacles/red obstacle.png')

obstacle_speed = 2.4

obstacle0_x = 500
obstacle1_x = 750
obstacle2_x = 1150
obstacle0_y = 125
obstacle1_y = 275
obstacle2_y = 425


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
                button_sound = mixer.Sound('Sound/button sound.wav')
                button_sound.play()
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
next_page_button = Button(480, 9, next_page_arrow)
go_back_button = Button(50, 5, go_back_arrow)

def game_over():
    with open('highscore.txt', 'r+') as file:
        try:
            highscore = int(file.read())
        except ValueError:
            highscore = 0

    death_message = my_font.render('...You Died...', False, (255, 255, 255))
    if highscore < score:
        highscore = score
        with open('highscore.txt', 'r+') as file:
            file.write(str(highscore))
    highscore_message = my_font.render(f'Highscore: {str(highscore)}', False, (255, 255, 255))
    screen.blit(death_message, (50, 50))
    screen.blit(highscore_message, (50, 150))


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


def fade_screen_game_over(width, height):
    fade_game_over = pygame.Surface((width, height))
    fade_game_over.fill(black)
    for alpha in range(0, 300):
        fade_game_over.set_alpha(alpha)
        screen.blit(fade_game_over, (0, 0))
        game_over()
        pygame.display.update()
        pygame.time.delay(5)


def fade_screen_loading(width, height):
    fade_loading = pygame.Surface((width, height))
    fade_loading.fill(black)
    for alpha in range(0, 300):
        fade_loading.set_alpha(alpha)
        screen.blit(fade_loading, (0, 0))
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


def player():
    user = screen.blit(current_car, (car_x, car_y))


def game():
    global game_start_screen
    global game_screen
    global no_collide
    global obstacle0_x
    global obstacle1_x
    global obstacle2_x
    global obstacle0_y
    global obstacle1_y
    global obstacle2_y
    global obstacle_speed
    global score
    user = screen.blit(current_car, (car_x, car_y))
    screen.blit(game_map, (0, 0))
    player()
    obstacle0 = pygame.Rect(obstacle0_x, obstacle0_y, 50, 50)
    obstacle1 = pygame.Rect(obstacle1_x, obstacle1_y, 50, 50)
    obstacle2 = pygame.Rect(obstacle2_x, obstacle2_y, 50, 50)

    screen.blit(oil, (obstacle0_x, obstacle0_y))
    screen.blit(blue_obs, (obstacle1_x, obstacle1_y))
    screen.blit(red_obs, (obstacle2_x, obstacle2_y))

    if no_collide:
        obstacle0_x -= obstacle_speed
        obstacle1_x -= obstacle_speed
        obstacle2_x -= obstacle_speed

        if obstacle0_x < -50:
            obstacle0_x = random.randrange(1200, 2000, 400)
            obstacle0_y = random.randrange(125, 525, 150)
            score += 1
            if score >= 10:
                obstacle_speed += 0.1

        if obstacle1_x < -50:
            obstacle1_x = obstacle0_x + 300
            obstacle1_y = random.randrange(125, 525, 150)
            score += 1
            if score >= 10:
                obstacle_speed += 0.1

        if obstacle2_x < -50:
            obstacle2_x = obstacle1_x + 600
            obstacle2_y = random.randrange(125, 525, 150)
            score += 1
            if score >= 10:
                obstacle_speed += 0.1

        if user.colliderect(obstacle0) or user.colliderect(obstacle1) or user.colliderect(obstacle2):
            no_collide = False
            game_screen = False
            game_start_screen = True
            fade_screen_game_over(600, 600)


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
    # next page arrow
    pygame.draw.rect(screen, black, pygame.Rect(465, 18, 120, 83))
    pygame.draw.rect(screen, purple, pygame.Rect(465, 18, 120, 83), 2)


def avatar_page_2():
    # title
    pygame.draw.rect(screen, black, pygame.Rect(225, 27, 157, 47))
    pygame.draw.rect(screen, purple, pygame.Rect(225, 27, 157, 47), 3)
    screen.blit(avatar_title, (230, 18))
    # go back arrow
    pygame.draw.rect(screen, black, pygame.Rect(45, 18, 120, 83))
    pygame.draw.rect(screen, purple, pygame.Rect(45, 18, 120, 83), 2)
    # current car
    pygame.draw.rect(screen, grey, pygame.Rect(200, 100, 180, 100))
    pygame.draw.rect(screen, purple, pygame.Rect(200, 100, 180, 100), 2)
    screen.blit(current_car, (225, 95))

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
        score_display = my_font_start.render(f'Score: {score}', False, (255, 255, 255))
        screen.blit(score_display, (450, 25))
        difficulty_title = my_font_start.render('Difficulty: ', False, (255, 255, 255))
        screen.blit(difficulty_title, (50, 25))
        if easy:
            easy_title = my_font_start.render('Easy :)', False, (0, 255, 0))
            screen.blit(easy_title, (190, 25))
        if 15 <= score < 30:
            easy = False
            medium = True
            if medium:
                medium_title = my_font_start.render('Medium :|', False, (228, 155, 15))
                screen.blit(medium_title, (190, 25))
        if 50 <= score < 75:
            medium = False
            hard = True
            if hard:
                hard_title = my_font_start.render('Hard :(', False, (255, 0, 0))
                screen.blit(hard_title, (190, 25))
        if score >= 75:
            hard = False
            extreme = True
            if extreme:
                extreme_title = my_font_start.render('Extreme >:(', False, (180, 0, 0))
                screen.blit(extreme_title, (190, 25))

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

        if next_page_button.draw():
            avatar_screen = False
            avatar_screen_two = True

    if avatar_screen_two:
        avatar_page_2()
        if go_back_button.draw():
            avatar_screen_two = False
            avatar_screen = True

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # avatar screen
            if game_start_screen:
                if event.key == pygame.K_a:
                    button_sound = mixer.Sound('Sound/button sound.wav')
                    button_sound.play()
                    fade_screen_loading(600, 600)
                    game_start_screen = False
                    tutorial_screen = False
                    game_screen = False
                    avatar_screen = True
                # tutorial screen
            if game_start_screen:
                if event.key == pygame.K_t:
                    button_sound = mixer.Sound('Sound/button sound.wav')
                    button_sound.play()
                    fade_screen_loading(600, 600)
                    game_start_screen = False
                    game_screen = False
                    avatar_screen = False
                    tutorial_screen = True
                # game screen
            if game_start_screen:
                if event.key == pygame.K_SPACE:
                    button_sound = mixer.Sound('Sound/button sound.wav')
                    button_sound.play()
                    fade_screen_loading(600, 600)
                    car_x = 10
                    car_y = 245
                    obstacle0_x = 500
                    obstacle1_x = 750
                    obstacle2_x = 1150
                    obstacle0_y = 125
                    obstacle1_y = 275
                    obstacle2_y = 425
                    obstacle_speed = 2.4
                    score = 0
                    no_collide = True
                    game_start_screen = False
                    tutorial_screen = False
                    avatar_screen = False
                    game_screen = True

            if game_screen:
                if event.key == pygame.K_UP:
                    if car_y > 0:
                        car_y -= 150
                    if car_y - 50 < 0:
                        image_border_sound = mixer.Sound('Sound/image border sound.wav')
                        image_border_sound.play()
                        car_y += 150
                if event.key == pygame.K_DOWN:
                    if car_y < 600:
                        car_y += 150
                    if car_y + 50 > 500:
                        image_border_sound = mixer.Sound('Sound/image border sound.wav')
                        image_border_sound.play()
                        car_y -= 150

        # go back to starting screen
        if not game_start_screen:
            if event.type == pygame.KEYDOWN:
                if not avatar_screen_two:
                    if event.key == pygame.K_ESCAPE:
                        button_sound = mixer.Sound('Sound/button sound.wav')
                        button_sound.play()
                        tutorial_screen = False
                        avatar_screen = False
                        avatar_screen_two = False
                        game_screen = False
                        game_start_screen = True

        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
