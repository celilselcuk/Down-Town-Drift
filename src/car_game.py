import pygame
import random
from pygame import mixer
from pathlib import Path

# Gets directories relative to the path of 'car_game.py' or '__file__'
def get_relative_dir(dir: str) -> str:
    return Path(__file__).parent.joinpath(dir)

pygame.init()

# create a screen
screen = pygame.display.set_mode((600, 600))

# Title and Icon
pygame.display.set_caption("Cars!")
icon = pygame.image.load(get_relative_dir('Menu design/001-racing-car.png'))
pygame.display.set_icon(icon)

# background
background = pygame.image.load(get_relative_dir('Menu design/background image.png'))

# game map
game_map = pygame.image.load(get_relative_dir('Level maps/game map.png'))

#button sounds
button_sound = mixer.Sound(get_relative_dir('Sound/button sound.wav'))
image_border_sound = mixer.Sound(get_relative_dir('Sound/image border sound.wav'))

#background music
start_screen_music = pygame.mixer.Sound(get_relative_dir('Sound/background song.wav'))
avatar_tutorial_screen_music = pygame.mixer.Sound(get_relative_dir('Sound/avatar music.mp3'))
game_screen_music = pygame.mixer.Sound(get_relative_dir('Sound/gran prix upbeat.mp3'))
called_start = False
called_avatar_tutorial = False
called_game = False

start_screen_channel = pygame.mixer.Channel(0)
avatar_tutorial_screen_channel = pygame.mixer.Channel(1)
game_screen_channel = pygame.mixer.Channel(2)

# score 
score = 0

# difficulty variables
class GameDifficulty():
    basic = 0
    easy = 1
    medium = 2
    hard = 3
    extreme = 4

# initialising difficulty (will be declared later)
difficulty: GameDifficulty

# general variables
next_page_arrow = pygame.image.load(get_relative_dir('Menu design/next page arrow.png'))
go_back_arrow = pygame.image.load(get_relative_dir('Menu design/go back arrow.png'))
no_collide = True
game_start_screen = True
avatar_screen = False
avatar_screen_two = False
tutorial_screen = False
game_screen = False

# colour variables
class GameColours():
    purple = (221, 160, 221)
    black = (0, 0, 0)
    grey = (100, 100, 100)
    red = (140, 0, 0)
    blue = (16, 47, 87)
    green = (28, 77, 28)
    orange = (201, 59, 12)
    grey_for_car = (87, 87, 87)
    purple_for_car = (100, 13, 166)
    colour_of_tank = (61, 122, 61)
    current_colour = red

# Fonts and text
my_font = pygame.font.Font(get_relative_dir('Font/BACKTO1982.TTF'), 32)
text_surface = my_font.render('Down Town Drift', False, (255, 255, 255))

my_font_start = pygame.font.Font(get_relative_dir('Font/BACKTO1982.TTF'), 20)
small_font = pygame.font.Font(get_relative_dir('Font/BACKTO1982.TTF'), 10)
text_avatar = my_font_start.render('Press A to view Avatar', False, (255, 255, 255))

text_tutorial = my_font_start.render('Press T to start Tutorial', False, (255, 255, 255))

text_start = my_font_start.render('Press SPACE to start Game', False, (255, 255, 255))

avatar_title = my_font.render('Avatar', False, (255, 255, 255))
start_esc = my_font_start.render('ESC', False, (255, 255, 255))

tutorial_title = my_font.render('Tutorial', False, (255, 255, 255))

game_title = my_font.render('Game', False, (255, 255, 255))

tutorial_text_1 = my_font_start.render('BAD - LOSE HP', False, (255, 255, 255))

tutorial_text_2 = my_font_start.render('GET COINS $$$', False, (255, 255, 255))

# loading bar variables

sprites = [pygame.image.load(get_relative_dir('Animation/Loading screen/pixil-frame-0.png')),
           pygame.image.load(get_relative_dir('Animation/Loading screen/pixil-frame-1.png')),
           pygame.image.load(get_relative_dir('Animation/Loading screen/pixil-frame-2.png')),
           pygame.image.load(get_relative_dir('Animation/Loading screen/pixil-frame-3.png')),
           pygame.image.load(get_relative_dir('Animation/Loading screen/pixil-frame-4.png')),
           pygame.image.load(get_relative_dir('Animation/Loading screen/pixil-frame-5.png')),
           pygame.image.load(get_relative_dir('Animation/Loading screen/pixil-frame-6.png')),
           pygame.image.load(get_relative_dir('Animation/Loading screen/pixil-frame-7.png'))]
counter = 0
money_adder_counter = 0
tank_sprites = [pygame.image.load(get_relative_dir('Animation/Tank/tank-frame-0.png')),
                pygame.image.load(get_relative_dir('Animation/Tank/tank-frame-1.png'))]
tank_counter = 0

# car
red_car = pygame.image.load(get_relative_dir('Cars/red car.png'))
blue_car = pygame.image.load(get_relative_dir('Cars/blue car.png'))
green_car = pygame.image.load(get_relative_dir('Cars/green car.png'))
orange_car = pygame.image.load(get_relative_dir('Cars/orange car.png'))
purple_car = pygame.image.load(get_relative_dir('Cars/purple car.png'))
grey_car = pygame.image.load(get_relative_dir('Cars/grey car.png'))
tank = pygame.image.load(get_relative_dir('Cars/2s3m.png'))
current_car = red_car
car_x = 10
car_y = 245
HP = 350
car_collide = False

# shop variables:
total_money = 0
coins_gained = 0
small_coin_pic = pygame.image.load(get_relative_dir("Menu design/small_coin.png"))

# obstacle variables
oil = pygame.image.load(get_relative_dir('Obstacles/oil leak.png'))
cone = pygame.image.load(get_relative_dir('Obstacles/cone.png'))
barrel = pygame.image.load(get_relative_dir('Obstacles/barrel.png'))
coin_pic = pygame.image.load(get_relative_dir('Obstacles/coin.png'))

obstacle_speed = 2.4

obstacle0_x = 500
obstacle1_x = 750
obstacle2_x = 1150
obstacle0_y = 100
obstacle1_y = 250
obstacle2_y = 400
coin_x = 3000
coin_y = 275
coin_hit = False
coin_on_map = False


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
                button_sound = mixer.Sound(get_relative_dir('Sound/button sound.wav'))
                button_sound.play()
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


tank_button = Button(80, 260, tank)
red_car_button = Button(80, 260, red_car)
blue_car_button = Button(240, 260, blue_car)
green_car_button = Button(400, 260, green_car)
orange_car_button = Button(80, 400, orange_car)
purple_car_button = Button(240, 400, purple_car)
grey_car_button = Button(400, 400, grey_car)
next_page_button = Button(480, 9, next_page_arrow)
go_back_button = Button(15, 5, go_back_arrow)

def update_highscore():

    with open(get_relative_dir('Data/highscore.txt'), 'r+') as file:
        try:
            high_score = int(file.read())
        except ValueError:
            high_score = 0

    if high_score < score:
        high_score = score
        with open(get_relative_dir('Data/highscore.txt'), 'r+') as file:
            file.write(str(high_score))

high_score = 0

def game_over():
    update_highscore()
    #screen text   
    death_message = my_font.render('...You Died...', False, (255, 255, 255))
    high_score_message = my_font.render(f'High score: {str(high_score)}', False, (255, 255, 255))
    money_gained_message = my_font.render(f'Money gained: {coins_gained}', False, (255, 255, 255))
    screen.blit(death_message, (50, 50))
    screen.blit(high_score_message, (50, 150))
    screen.blit(money_gained_message, (50, 250))


def loading():
    global counter
    loading_message = my_font.render('Loading', False, (255, 255, 255))
    pygame.draw.rect(screen, grey, pygame.Rect(195, 108, 220, 60))
    pygame.draw.rect(screen, purple, pygame.Rect(195, 108, 220, 60), 3)
    screen.blit(loading_message, (208, 118))

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
    global money_adder_counter

    money_adder_counter = 0
    pygame.draw.rect(screen, black, pygame.Rect(90, 38, 423, 60))
    pygame.draw.rect(screen, purple, pygame.Rect(90, 38, 423, 60), 3)
    screen.blit(text_surface, (100, 50))
    pygame.draw.rect(screen, black, pygame.Rect(90, 300, 435, 45))
    pygame.draw.rect(screen, purple, pygame.Rect(90, 300, 435, 45), 3)
    screen.blit(text_start, (100, 310))
    pygame.draw.rect(screen, black, pygame.Rect(90, 500, 432, 45))
    pygame.draw.rect(screen, purple, pygame.Rect(90, 500, 432, 45), 3)
    screen.blit(text_tutorial, (100, 510))
    pygame.draw.rect(screen, black, pygame.Rect(90, 400, 378, 45))
    pygame.draw.rect(screen, purple, pygame.Rect(90, 400, 378, 45), 3)
    screen.blit(text_avatar, (100, 410))


def game():
    global total_money
    global coin_x
    global coin_y
    global current_car
    global car_collide
    global HP
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
    global coin_hit
    global coin_on_map
    global coins_gained

    screen.blit(game_map, (0, 0))
    pygame.draw.rect(screen, black, pygame.Rect(535, 535, 60, 60))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(535, 535, 60, 60), 3)
    screen.blit(small_coin_pic, (540, 540))
    money_text = my_font_start.render(f'{coins_gained}', False, (255, 255, 255))
    screen.blit(money_text, (548, 540))
    # HEALTH BAR #
    if HP == 350:
        pygame.draw.rect(screen, current_colour, pygame.Rect(20, 540, HP, 45))
        pygame.draw.rect(screen, black, pygame.Rect(20, 540, 350, 45), 3)

    user = pygame.Rect(car_x, car_y, 110, 110)

    coin = pygame.Rect(coin_x, coin_y, 50, 50)
    obstacle0 = pygame.Rect(obstacle0_x, obstacle0_y, 50, 50)
    obstacle1 = pygame.Rect(obstacle1_x, obstacle1_y, 50, 50)
    obstacle2 = pygame.Rect(obstacle2_x, obstacle2_y, 50, 50)
    screen.blit(oil, (obstacle0_x, obstacle0_y))
    screen.blit(cone, (obstacle1_x, obstacle1_y))
    screen.blit(barrel, (obstacle2_x, obstacle2_y))

    if no_collide:
        obstacle0_x -= obstacle_speed
        obstacle1_x -= obstacle_speed
        obstacle2_x -= obstacle_speed

        if obstacle0_x < -70:
            obstacle0_x = random.randrange(1200, 2000, 400)
            obstacle0_y = random.randrange(125, 525, 150)
            score += 1
            if score >= 10:
                obstacle_speed += 0.1

        if obstacle1_x < -70:
            obstacle1_x = obstacle0_x + 300
            obstacle1_y = random.randrange(125, 525, 150)
            score += 1
            if score >= 10:
                obstacle_speed += 0.1

        if obstacle2_x < -70:
            obstacle2_x = obstacle1_x + 600
            obstacle2_y = random.randrange(125, 525, 150)
            score += 1
            if score >= 10:
                obstacle_speed += 0.1

        if score % 10 == 0 or coin_on_map:
            if coin.colliderect(obstacle0) or coin.colliderect(obstacle1) or coin.colliderect(obstacle2):
                coin_x = coin_x + 500
            screen.blit(coin_pic, (coin_x, coin_y))
            coin_x -= obstacle_speed
            coin_on_map = True

        if coin_x < -70:
            coin_x = obstacle2_x + 900
            coin_y = random.randrange(125, 525, 150)
            coin_on_map = False

        if user.colliderect(obstacle0) or user.colliderect(obstacle1) or user.colliderect(obstacle2):
            pygame.draw.rect(screen, current_colour, pygame.Rect(20, 540, HP, 45))
            pygame.draw.rect(screen, black, pygame.Rect(20, 540, 350, 45), 3)
            if current_car == tank:
                HP -= obstacle_speed / 6
            else:
                HP -= obstacle_speed / 0.6

        if user.colliderect(coin) and not coin_hit:
            total_money += 1
            coins_gained += 1
            coin_x = obstacle2_x + 900
            coin_y = random.randrange(125, 525, 150)
            coin_hit = True
            coin_on_map = False

        if not user.colliderect(coin):
            coin_hit = False

        if HP <= 0:
            no_collide = False
            game_screen = False
            game_start_screen = True
            fade_screen_game_over(600, 600)

        pygame.draw.rect(screen, current_colour, pygame.Rect(20, 540, HP, 45))
        pygame.draw.rect(screen, black, pygame.Rect(20, 540, 350, 45), 3)


def tutorial():

    pygame.draw.rect(screen, black, pygame.Rect(187, 27, 240, 55))
    pygame.draw.rect(screen, purple, pygame.Rect(187, 27, 240, 55), 4)
    screen.blit(tutorial_title, (195, 35))

    pygame.draw.rect(screen, black, pygame.Rect(48, 30, 75, 40))
    pygame.draw.rect(screen, purple, pygame.Rect(48, 30, 75, 40), 4)
    screen.blit(start_esc, (58, 38))

    pygame.draw.rect(screen, grey, pygame.Rect(30, 130, 540, 430))
    pygame.draw.rect(screen, purple, pygame.Rect(30, 130, 540, 430), 5)

    pygame.draw.line(screen, purple, (300, 130), (300, 559), 4)

    pygame.draw.rect(screen, red, pygame.Rect(40, 140, 253, 200))
    pygame.draw.rect(screen, black, pygame.Rect(40, 140, 253, 200), 4)
    screen.blit(tutorial_text_1, (60, 170))

    pygame.draw.rect(screen, green, pygame.Rect(40, 350, 253, 200))
    pygame.draw.rect(screen, black, pygame.Rect(40, 350, 253, 200), 4)
    screen.blit(tutorial_text_2, (60, 380))

    screen.blit(oil, (50, 225))
    screen.blit(cone, (130, 225))
    screen.blit(barrel, (210, 225))
    screen.blit(coin_pic, (130, 435))


def avatar():

    # title
    pygame.draw.rect(screen, black, pygame.Rect(190, 27, 202, 57))
    pygame.draw.rect(screen, purple, pygame.Rect(190, 27, 202, 57), 4)
    screen.blit(avatar_title, (204, 37))
    # esc
    pygame.draw.rect(screen, black, pygame.Rect(48, 30, 75, 40))
    pygame.draw.rect(screen, purple, pygame.Rect(48, 30, 75, 40), 4)
    screen.blit(start_esc, (58, 38))
    # customise box
    pygame.draw.rect(screen, grey, pygame.Rect(50, 250, 500, 290))
    pygame.draw.rect(screen, purple, pygame.Rect(50, 250, 500, 290), 5)
    # current car
    pygame.draw.rect(screen, grey, pygame.Rect(200, 110, 180, 105))
    pygame.draw.rect(screen, purple, pygame.Rect(200, 110, 180, 105), 4)
    screen.blit(current_car, (228, 108))
    # next page arrow
    pygame.draw.rect(screen, black, pygame.Rect(465, 18, 120, 83))
    pygame.draw.rect(screen, purple, pygame.Rect(465, 18, 120, 83), 4)
    # money
    pygame.draw.rect(screen, black, pygame.Rect(50, 130, 106, 55))
    pygame.draw.rect(screen, purple, pygame.Rect(50, 130, 106, 55), 4)
    screen.blit(small_coin_pic, (40, 120))
    total_money_message = my_font_start.render(f' {final_money}', False, (255, 255, 255))
    screen.blit(total_money_message, (90, 145))


def avatar_page_2():

    # title
    pygame.draw.rect(screen, black, pygame.Rect(190, 27, 202, 57))
    pygame.draw.rect(screen, purple, pygame.Rect(190, 27, 202, 57), 4)
    screen.blit(avatar_title, (204, 37))
    # go back arrow
    pygame.draw.rect(screen, black, pygame.Rect(10, 18, 120, 83))
    pygame.draw.rect(screen, purple, pygame.Rect(10, 18, 120, 83), 4)
    # current car
    pygame.draw.rect(screen, grey, pygame.Rect(200, 110, 180, 105))
    pygame.draw.rect(screen, purple, pygame.Rect(200, 110, 180, 105), 4)
    screen.blit(current_car, (228, 108))
    # customise box
    pygame.draw.rect(screen, grey, pygame.Rect(50, 250, 500, 290))
    pygame.draw.rect(screen, purple, pygame.Rect(50, 250, 500, 290), 5)
    # money
    pygame.draw.rect(screen, black, pygame.Rect(50, 130, 106, 55))
    pygame.draw.rect(screen, purple, pygame.Rect(50, 130, 106, 55), 4)
    screen.blit(small_coin_pic, (40, 120))
    total_money_message = my_font_start.render(f' {final_money}', False, (255, 255, 255))
    screen.blit(total_money_message, (90, 145))

def update_money():
    global total_money, final_money, coins_gained
    
    with open(get_relative_dir('Data/user_money.txt'), 'r+') as file:
        try:
            final_money = int(file.read())
        except ValueError:
            final_money = 0

    with open(get_relative_dir('Data/user_money.txt'), 'r+') as file:
        final_money += total_money
        file.write(str(final_money))

    total_money = 0

running = True
while running:

    screen.blit(background, (0, 0))

    if game_start_screen:
        update_money()
        update_highscore()
        start_screen()
        if not called_start:
           avatar_tutorial_screen_channel.fadeout(500)
           game_screen_channel.fadeout(500)
           start_screen_channel.play(start_screen_music, -1)
           called_avatar_tutorial = False
           called_game = False
           called_start = True


    if avatar_screen:
        update_money()
        avatar()
        if not called_avatar_tutorial:
           start_screen_channel.fadeout(500)
           game_screen_channel.fadeout(500)
           avatar_tutorial_screen_channel.play(avatar_tutorial_screen_music, -1)
           called_avatar_tutorial = True
           called_game = False
           called_start = False

    if tutorial_screen:
        update_money()
        tutorial()
        if not called_avatar_tutorial:
           start_screen_channel.fadeout(500)
           game_screen_channel.fadeout(500)
           avatar_tutorial_screen_channel.play(avatar_tutorial_screen_music, -1)
           called_avatar_tutorial = True
           called_game = False
           called_start = False

    if game_screen:
        update_money()
        update_highscore()
        game()
        if not called_game:
           start_screen_channel.fadeout(500)
           avatar_tutorial_screen_channel.fadeout(500)
           game_screen_channel.play(game_screen_music, -1)
           called_avatar_tutorial = False
           called_game = True
           called_start = False

        score_display = my_font_start.render(f'Score: {score}', False, (255, 255, 255))
        screen.blit(score_display, (435, 25))
        difficulty_title = my_font_start.render('Difficulty: ', False, (255, 255, 255))
        screen.blit(difficulty_title, (32, 25))
        if basic or score == 0:
            easy_title = my_font_start.render('Basic', False, (0, 0, 190))
            screen.blit(easy_title, (215, 25))
        if 15 <= score < 30:
            basic = False
            easy = True
            if easy:
                medium_title = my_font_start.render('Easy', False, (0, 255, 0))
                screen.blit(medium_title, (215, 25))
        if 30 <= score < 55:
            easy = False
            medium = True
            if medium:
                hard_title = my_font_start.render('Medium', False, (228, 155, 15))
                screen.blit(hard_title, (215, 25))
        if 55 <= score < 85:
            medium = False
            hard = True
            if hard:
                extreme_title = my_font_start.render('Hard', False, (255, 0, 0))
                screen.blit(extreme_title, (215, 25))
        if score > 85:
            hard = False
            extreme = True
            if extreme:
                extreme_title = my_font_start.render('Extreme', False, (180, 0, 0))
                screen.blit(extreme_title, (215, 25))

        # ~~~DRAWING PLAYER + ANIMATIONS FOR CARS~~~ #
        if current_car == tank:
            current_tank = tank_sprites[int(tank_counter)]
            tank_counter += 0.07
            if tank_counter >= len(tank_sprites):
                tank_counter = 0
            screen.blit(current_tank, (car_x, car_y))
        else:
            screen.blit(current_car, (car_x, car_y))

    if avatar_screen:
        if red_car_button.draw():
            current_car = red_car
            current_colour = red

        if blue_car_button.draw():
            current_car = blue_car
            current_colour = blue
        if green_car_button.draw():
            current_car = green_car
            current_colour = green
        if orange_car_button.draw():
            current_car = orange_car
            current_colour = orange
        if purple_car_button.draw():
            current_car = purple_car
            current_colour = purple_for_car
        if grey_car_button.draw():
            current_car = grey_car
            current_colour = grey_for_car
        if next_page_button.draw():
            avatar_screen = False
            avatar_screen_two = True

    if avatar_screen_two:
        update_money()
        avatar_page_2()
        if tank_button.draw():
            current_car = tank
            current_colour = colour_of_tank

        if go_back_button.draw():
            avatar_screen_two = False
            avatar_screen = True

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # avatar screen
            if game_start_screen:
                if event.key == pygame.K_a:
                    button_sound.play()
                    fade_screen_loading(600, 600)
                    game_start_screen = False
                    tutorial_screen = False
                    game_screen = False
                    avatar_screen = True
                # tutorial screen
            if game_start_screen:
                if event.key == pygame.K_t:
                    button_sound.play()
                    fade_screen_loading(600, 600)
                    game_start_screen = False
                    game_screen = False
                    avatar_screen = False
                    tutorial_screen = True
                # game screen
            if game_start_screen:
                if event.key == pygame.K_SPACE:
                    button_sound.play()
                    fade_screen_loading(600, 600)
                    car_x = 10
                    car_y = 245
                    coin_x = 3000
                    coin_y = 275
                    coins_gained = 0
                    coin_hit = False
                    coin_on_map = False
                    obstacle0_x = 500
                    obstacle1_x = 750
                    obstacle2_x = 1150
                    obstacle0_y = 125
                    obstacle1_y = 275
                    obstacle2_y = 425
                    obstacle_speed = 2.4
                    score = 0
                    HP = 350
                    no_collide = True
                    game_start_screen = False
                    tutorial_screen = False
                    avatar_screen = False
                    game_screen = True
                    basic = True

            if game_screen:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if car_y > 0:
                        car_y -= 150
                    if car_y - 50 < 0:
                        image_border_sound.play()
                        car_y += 150
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if car_y < 600:
                        car_y += 150
                    if car_y + 50 > 500:
                        image_border_sound.play()
                        car_y -= 150

        # go back to starting screen
        if not game_start_screen:
            if event.type == pygame.KEYDOWN:
                if not avatar_screen_two:
                    if event.key == pygame.K_ESCAPE:
                        button_sound.play()
                        tutorial_screen = False
                        avatar_screen = False
                        avatar_screen_two = False
                        game_screen = False
                        game_start_screen = True

        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
