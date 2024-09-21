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
avatar_screen = False
avatar_screen_two = False
tutorial_screen = False


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
car_x = 10
car_y = 245

# shop variables:
small_coin_pic = pygame.image.load(get_relative_dir("Menu design/small_coin.png"))
tank_purchase = pygame.image.load(get_relative_dir('Menu design/tank-req.png'))
list_of_purchases = []
unknown = pygame.image.load(get_relative_dir("Menu design/unkown.png"))

# obstacle variables
oil = pygame.image.load(get_relative_dir('Obstacles/oil leak.png'))
cone = pygame.image.load(get_relative_dir('Obstacles/cone.png'))
barrel = pygame.image.load(get_relative_dir('Obstacles/barrel.png'))
coin_pic = pygame.image.load(get_relative_dir('Obstacles/coin.png'))

class GameState():
    total_money = 0
    coin_x = 3000
    coin_y = 275
    current_car = red_car
    car_collide = False
    HP = 350
    game_start_screen = True
    game_screen = False
    no_collide = True
    obstacle0_x = 500
    obstacle1_x = 750
    obstacle2_x = 1150
    obstacle0_y = 100
    obstacle1_y = 250
    obstacle2_y = 400
    obstacle_speed = 2.4
    score = 0
    coin_hit = False
    coin_on_map = False
    coins_gained = 0

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
tank_buy_button = Button(53,251, tank_purchase)

def update_highscore():

    with open(get_relative_dir('Data/highscore.txt'), 'r+') as file:
        try:
            high_score = int(file.read())
        except ValueError:
            high_score = 0

    if high_score < GameState.score:
        high_score = GameState.score
        with open(get_relative_dir('Data/highscore.txt'), 'r+') as file:
            file.write(str(high_score))

    return high_score

def game_over():
    high_score = update_highscore()
    #screen text   
    death_message = my_font.render('...You Died...', False, (255, 255, 255))
    high_score_message = my_font.render(f'High score: {str(high_score)}', False, (255, 255, 255))
    money_gained_message = my_font.render(f'Money gained: {GameState.coins_gained}', False, (255, 255, 255))
    screen.blit(death_message, (50, 50))
    screen.blit(high_score_message, (50, 150))
    screen.blit(money_gained_message, (50, 250))

def loading():
    global counter
    loading_message = my_font.render('Loading', False, (255, 255, 255))
    pygame.draw.rect(screen, GameColours.grey, pygame.Rect(195, 108, 220, 60))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(195, 108, 220, 60), 3)
    screen.blit(loading_message, (208, 118))

    current_sprite = sprites[int(counter)]

    if counter < len(sprites):
        screen.blit(current_sprite, (110, 200))

    if counter + 1 > len(sprites):
        counter = 0

    counter += 0.1


def fade_screen_game_over(width, height):
    fade_game_over = pygame.Surface((width, height))
    fade_game_over.fill(GameColours.black)
    for alpha in range(0, 300):
        fade_game_over.set_alpha(alpha)
        screen.blit(fade_game_over, (0, 0))
        game_over()
        pygame.display.update()
        pygame.time.delay(5)


def fade_screen_loading(width, height):
    fade_loading = pygame.Surface((width, height))
    fade_loading.fill(GameColours.black)
    for alpha in range(0, 300):
        fade_loading.set_alpha(alpha)
        screen.blit(fade_loading, (0, 0))
        loading()
        pygame.display.update()

def start_screen():
    global money_adder_counter

    money_adder_counter = 0
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(90, 38, 423, 60))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(90, 38, 423, 60), 3)
    screen.blit(text_surface, (100, 50))
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(90, 300, 435, 45))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(90, 300, 435, 45), 3)
    screen.blit(text_start, (100, 310))
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(90, 500, 432, 45))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(90, 500, 432, 45), 3)
    screen.blit(text_tutorial, (100, 510))
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(90, 400, 378, 45))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(90, 400, 378, 45), 3)
    screen.blit(text_avatar, (100, 410))

def game():

    screen.blit(game_map, (0, 0))
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(535, 535, 60, 60))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(535, 535, 60, 60), 3)
    screen.blit(small_coin_pic, (540, 540))
    money_text = my_font_start.render(f'{GameState.coins_gained}', False, (255, 255, 255))
    screen.blit(money_text, (548, 540))
    # HEALTH BAR #
    if GameState.HP == 350:
        pygame.draw.rect(screen, GameColours.current_colour, pygame.Rect(20, 540, GameState.HP, 45))
        pygame.draw.rect(screen, GameColours.black, pygame.Rect(20, 540, 350, 45), 3)

    user = pygame.Rect(car_x, car_y, 110, 110)

    coin = pygame.Rect(GameState.coin_x, GameState.coin_y, 50, 50)
    obstacle0 = pygame.Rect(GameState.obstacle0_x, GameState.obstacle0_y, 50, 50)
    obstacle1 = pygame.Rect(GameState.obstacle1_x, GameState.obstacle1_y, 50, 50)
    obstacle2 = pygame.Rect(GameState.obstacle2_x, GameState.obstacle2_y, 50, 50)
    screen.blit(oil, (GameState.obstacle0_x, GameState.obstacle0_y))
    screen.blit(cone, (GameState.obstacle1_x, GameState.obstacle1_y))
    screen.blit(barrel, (GameState.obstacle2_x, GameState.obstacle2_y))

    if GameState.no_collide:
        GameState.obstacle0_x -= GameState.obstacle_speed
        GameState.obstacle1_x -= GameState.obstacle_speed
        GameState.obstacle2_x -= GameState.obstacle_speed

        if GameState.obstacle0_x < -70:
            GameState.obstacle0_x = random.randrange(1200, 2000, 400)
            GameState.obstacle0_y = random.randrange(125, 525, 150)
            GameState.score += 1
            if GameState.score >= 10:
                GameState.obstacle_speed += 0.1

        if GameState.obstacle1_x < -70:
            GameState.obstacle1_x = GameState.obstacle0_x + 300
            GameState.obstacle1_y = random.randrange(125, 525, 150)
            GameState.score += 1
            if GameState.score >= 10:
                GameState.obstacle_speed += 0.1

        if GameState.obstacle2_x < -70:
            GameState.obstacle2_x = GameState.obstacle1_x + 600
            GameState.obstacle2_y = random.randrange(125, 525, 150)
            GameState.score += 1
            if GameState.score >= 10:
                GameState.obstacle_speed += 0.1

        if GameState.score % 10 == 0 or GameState.coin_on_map:
            if coin.colliderect(obstacle0) or coin.colliderect(obstacle1) or coin.colliderect(obstacle2):
                GameState.coin_x = GameState.coin_x + 500
            screen.blit(coin_pic, (GameState.coin_x, GameState.coin_y))
            GameState.coin_x -= GameState.obstacle_speed
            GameState.coin_on_map = True

        if GameState.coin_x < -70:
            GameState.coin_x = GameState.obstacle2_x + 900
            GameState.coin_y = random.randrange(125, 525, 150)
            GameState.coin_on_map = False

        if user.colliderect(obstacle0) or user.colliderect(obstacle1) or user.colliderect(obstacle2):
            pygame.draw.rect(screen, GameColours.current_colour, pygame.Rect(20, 540, GameState.HP, 45))
            pygame.draw.rect(screen, GameColours.black, pygame.Rect(20, 540, 350, 45), 3)
            if GameState.current_car == tank:
                GameState.HP -= GameState.obstacle_speed / 6
            else:
                GameState.HP -= GameState.obstacle_speed / 0.6

        if user.colliderect(coin) and not GameState.coin_hit:
            GameState.total_money += 1
            GameState.coins_gained += 1
            GameState.coin_x = GameState.obstacle2_x + 900
            GameState.coin_y = random.randrange(125, 525, 150)
            GameState.coin_hit = True
            GameState.coin_on_map = False

        if not user.colliderect(coin):
            GameState.coin_hit = False

        if GameState.HP <= 0:
            GameState.no_collide = False
            GameState.game_screen = False
            GameState.game_start_screen = True
            fade_screen_game_over(600, 600)

        pygame.draw.rect(screen, GameColours.current_colour, pygame.Rect(20, 540, GameState.HP, 45))
        pygame.draw.rect(screen, GameColours.black, pygame.Rect(20, 540, 350, 45), 3)

def tutorial():

    pygame.draw.rect(screen, GameColours.black, pygame.Rect(187, 27, 240, 55))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(187, 27, 240, 55), 4)
    screen.blit(tutorial_title, (195, 35))

    pygame.draw.rect(screen, GameColours.black, pygame.Rect(48, 30, 75, 40))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(48, 30, 75, 40), 4)
    screen.blit(start_esc, (58, 38))

    pygame.draw.rect(screen, GameColours.grey, pygame.Rect(30, 130, 540, 430))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(30, 130, 540, 430), 5)

    pygame.draw.line(screen, GameColours.purple, (300, 130), (300, 559), 4)

    pygame.draw.rect(screen, GameColours.red, pygame.Rect(40, 140, 253, 200))
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(40, 140, 253, 200), 4)
    screen.blit(tutorial_text_1, (60, 170))

    pygame.draw.rect(screen, GameColours.green, pygame.Rect(40, 350, 253, 200))
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(40, 350, 253, 200), 4)
    screen.blit(tutorial_text_2, (60, 380))

    screen.blit(oil, (50, 225))
    screen.blit(cone, (130, 225))
    screen.blit(barrel, (210, 225))
    screen.blit(coin_pic, (130, 435))

def avatar():

    # title
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(190, 27, 202, 57))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(190, 27, 202, 57), 4)
    screen.blit(avatar_title, (204, 37))
    # esc
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(48, 30, 75, 40))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(48, 30, 75, 40), 4)
    screen.blit(start_esc, (58, 38))
    # customise box
    pygame.draw.rect(screen, GameColours.grey, pygame.Rect(50, 250, 500, 290))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(50, 250, 500, 290), 5)
    # current car
    pygame.draw.rect(screen, GameColours.grey, pygame.Rect(200, 110, 180, 105))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(200, 110, 180, 105), 4)
    screen.blit(GameState.current_car, (228, 108))
    # box dividers
    pygame.draw.line(screen,GameColours.purple, (50,395), (545, 395), 5) # horizontal
    pygame.draw.line(screen, GameColours.purple, (215,250),(215,538),5) #vertical
    pygame.draw.line(screen, GameColours.purple, (380,250),(380,538),5) #vertical
    # next page arrow
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(465, 18, 120, 83))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(465, 18, 120, 83), 4)
    # money
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(50, 130, 106, 55))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(50, 130, 106, 55), 4)
    screen.blit(small_coin_pic, (40, 120))
    total_money_message = my_font_start.render(f' {final_money}', False, (255, 255, 255))
    screen.blit(total_money_message, (90, 145))

def avatar_page_2():

    # title
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(190, 27, 202, 57))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(190, 27, 202, 57), 4)
    screen.blit(avatar_title, (204, 37))
    # go back arrow
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(10, 18, 120, 83))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(10, 18, 120, 83), 4)
    # current car
    pygame.draw.rect(screen, GameColours.grey, pygame.Rect(200, 110, 180, 105))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(200, 110, 180, 105), 4)
    screen.blit(GameState.current_car, (228, 108))
    # customise box
    pygame.draw.rect(screen, GameColours.grey, pygame.Rect(50, 247, 500, 298))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(50, 247, 500, 298), 5)
    # box dividers
    pygame.draw.line(screen,GameColours.purple, (50,395), (545, 395), 5) # horizontal
    pygame.draw.line(screen, GameColours.purple, (220,250),(220,538),5) #vertical 1
    pygame.draw.line(screen, GameColours.purple, (380,250),(380,538),5) #vertical 2
    # unknowns
    screen.blit(unknown, (218, 251))
    screen.blit(unknown, (380, 251))
    screen.blit(unknown, (53, 396))
    screen.blit(unknown, (218, 396))
    screen.blit(unknown, (380, 396))
    # money
    pygame.draw.rect(screen, GameColours.black, pygame.Rect(50, 130, 106, 55))
    pygame.draw.rect(screen, GameColours.purple, pygame.Rect(50, 130, 106, 55), 4)
    screen.blit(small_coin_pic, (40, 120))
    total_money_message = my_font_start.render(f' {final_money}', False, (255, 255, 255))
    screen.blit(total_money_message, (90, 145))

def update_money():
    global final_money
    
    with open(get_relative_dir('Data/user_money.txt'), 'r+') as file:
        try:
            final_money = int(file.read())
        except ValueError:
            final_money = 0

    with open(get_relative_dir('Data/user_money.txt'), 'r+') as file:
        final_money += GameState.total_money
        file.write(str(final_money))

    GameState.total_money = 0

def check_bought(purchases):
    with open(get_relative_dir('Data/car_unlocks.txt'), 'r+') as file:
        for i, lines in enumerate(file):
            if i < 6:
                purchases.append(str(lines.rstrip()))

def update_bought(purchases, pos):
    change_to = 'True'
    purchases[pos] = change_to
    with open(get_relative_dir('Data/car_unlocks.txt'), 'r+') as file:
        for i, lines in enumerate(purchases):
            if i < 6:
                file.write(str(lines) + '\n')

def deduct_money(cost):
    global final_money
    with open(get_relative_dir('Data/user_money.txt'), 'r+') as file:
        final_money -= 30
        file.write(str(final_money))

running = True
while running:

    screen.blit(background, (0, 0))

    if GameState.game_start_screen:
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

    if GameState.game_screen:
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

        score_display = my_font_start.render(f'Score: {GameState.score}', False, (255, 255, 255))
        screen.blit(score_display, (435, 25))
        difficulty_title = my_font_start.render('Difficulty: ', False, (255, 255, 255))
        screen.blit(difficulty_title, (32, 25))

        if difficulty == GameDifficulty.basic or GameState.score == 0:
            easy_title = my_font_start.render('Basic', False, (0, 0, 190))
            screen.blit(easy_title, (215, 25))
        if 15 <= GameState.score < 30:
            difficulty = GameDifficulty.easy

            medium_title = my_font_start.render('Easy', False, (0, 255, 0))
            screen.blit(medium_title, (215, 25))
        if 30 <= GameState.score < 55:
            difficulty = GameDifficulty.medium

            hard_title = my_font_start.render('Medium', False, (228, 155, 15))
            screen.blit(hard_title, (215, 25))
        if 55 <= GameState.score < 85:
            difficulty = GameDifficulty.hard

            extreme_title = my_font_start.render('Hard', False, (255, 0, 0))
            screen.blit(extreme_title, (215, 25))
        if GameState.score > 85:
            difficulty = GameDifficulty.extreme

            
            extreme_title = my_font_start.render('Extreme', False, (180, 0, 0))
            screen.blit(extreme_title, (215, 25))

        # ~~~DRAWING PLAYER + ANIMATIONS FOR CARS~~~ #
        if GameState.current_car == tank:
            current_tank = tank_sprites[int(tank_counter)]
            tank_counter += 0.07
            if tank_counter >= len(tank_sprites):
                tank_counter = 0
            screen.blit(current_tank, (car_x, car_y))
        else:
            screen.blit(GameState.current_car, (car_x, car_y))

    if avatar_screen:
        if red_car_button.draw():
            GameState.current_car = red_car
            GameColours.current_colour = GameColours.red

        if blue_car_button.draw():
            GameState.current_car = blue_car
            GameColours.current_colour = GameColours.blue
        if green_car_button.draw():
            GameState.current_car = green_car
            GameColours.current_colour = GameColours.green
        if orange_car_button.draw():
            GameState.current_car = orange_car
            GameColours.current_colour = GameColours.orange
        if purple_car_button.draw():
            GameState.current_car = purple_car
            GameColours.current_colour = GameColours.purple_for_car
        if grey_car_button.draw():
            GameState.current_car = grey_car
            GameColours.current_colour = GameColours.grey_for_car
        if next_page_button.draw():
            avatar_screen = False
            avatar_screen_two = True

    if avatar_screen_two:
        update_money()
        avatar_page_2()
        check_bought(list_of_purchases)
        # purchase check for the TANK 
        if list_of_purchases[0] == 'False':
            if tank_buy_button.draw():
                if final_money >= 30:
                    deduct_money(30)
                    update_bought(list_of_purchases,0)        
        if list_of_purchases[0] == 'True':
            pygame.draw.rect(screen, GameColours.grey, pygame.Rect(55, 255, 160, 135))
            if tank_button.draw():
                        GameState.current_car = tank
                        GameColours.current_colour = GameColours.colour_of_tank

        if go_back_button.draw():
            avatar_screen_two = False
            avatar_screen = True

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # avatar screen
            if GameState.game_start_screen:
                if event.key == pygame.K_a:
                    button_sound.play()
                    fade_screen_loading(600, 600)
                    GameState.game_start_screen = False
                    tutorial_screen = False
                    GameState.game_screen = False
                    avatar_screen = True
                # tutorial screen
            if GameState.game_start_screen:
                if event.key == pygame.K_t:
                    button_sound.play()
                    fade_screen_loading(600, 600)
                    GameState.game_start_screen = False
                    GameState.game_screen = False
                    avatar_screen = False
                    tutorial_screen = True
                # game screen
            if GameState.game_start_screen:
                if event.key == pygame.K_SPACE:
                    button_sound.play()
                    fade_screen_loading(600, 600)
                    GameState.car_x = 10
                    GameState.car_y = 245
                    GameState.coin_x = 3000
                    GameState.coin_y = 275
                    GameState.coins_gained = 0
                    GameState.coin_hit = False
                    GameState.coin_on_map = False
                    GameState.obstacle0_x = 500
                    GameState.obstacle1_x = 750
                    GameState.obstacle2_x = 1150
                    GameState.obstacle0_y = 125
                    GameState.obstacle1_y = 275
                    GameState.obstacle2_y = 425
                    GameState.obstacle_speed = 2.4
                    GameState.score = 0
                    GameState.HP = 350
                    GameState.no_collide = True
                    GameState.game_start_screen = False
                    tutorial_screen = False
                    avatar_screen = False
                    GameState.game_screen = True
                    difficulty = GameDifficulty.basic

            if GameState.game_screen:
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
        if not GameState.game_start_screen:
            if event.type == pygame.KEYDOWN:
                if not avatar_screen_two:
                    if event.key == pygame.K_ESCAPE:
                        button_sound.play()
                        tutorial_screen = False
                        avatar_screen = False
                        avatar_screen_two = False
                        GameState.game_screen = False
                        GameState.game_start_screen = True

        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
