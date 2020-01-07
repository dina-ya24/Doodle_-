import pygame
import os
from random import randint
import sys

pygame.init()
size = width, height = 500, 600
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))

clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


record_height = 'record'  # высший результат всех игр
doodle = pygame.transform.scale(load_image('doodle.png', -1), (510, 340))  # главный герой
doodle_jump = pygame.transform.scale(load_image('doodle_jump.png', -1), (510, 340))
wings = pygame.transform.scale(load_image('wings.png', -1), (18, 12))  # крылья
doodle_wings = pygame.transform.scale(load_image('doodle_wings.png', -1), (90, 60))  # doodle с крыльями
monster = pygame.transform.scale(load_image('monster.png', -1), (90, 60))  # "монстры
cloud = pygame.transform.scale(load_image('cloud.png'), (90, 60))  # картинка облака
platf1 = pygame.transform.scale(load_image('platf1.png', -1), (90, 60))  # платформа из земли
platf2 = pygame.transform.scale(load_image('platf2.png', -1), (90, 60))  # платформа из земли поменьше
platf_tr = pygame.transform.scale(load_image('platf_tr.png', -1), (90, 60))  # платформа из дерева
platf_br = pygame.transform.scale(load_image('platf_br.png', -1), (90, 60))  # сломанная платформа из дерева


class Doodle:
    def __init__(self):
        self.coor = (self.x, self.y) = (210, 540)
        self.height = -10

    def jump(self):
        self.y += self.height
        self.coor = (self.x, self.y + self.height)

    def right(self):
        self.x += 5
        self.coor = (self.x, self.y)

    def left(self):
        self.x -= 5
        self.coor = (self.x, self.y)

    def change_high(self, time):
        if time % 3:
            if time < 100:
                self.height += 1
            else:
                self.height -= 1

    def get_posit(self):
        return self.coor

    def check_end(self):
        if self.y > 540 or self.collision():
            Start_End.end(Background.get_result())

    def collision(self):
        x1 = self.x
        y1 = self.y
        l1 = 90  # ширина doodle
        h1 = 60  # длина doodle
        l2 = 90  # ширина monster
        h2 = 60  # длина monster
        collis = False
        for i in monsters:
            x2 = i.get_posit()[0]
            y2 = i.get_posit()[1]
            if (x1 + l1) >= x2 and (y1 + h1 <= y2 or y1 <= y2 + h2) or (x1 <= x2 + l2) and \
                    (y1 + h1 >= y2 or y1 >= y2 + h2):
                collis = True
        return collis

    def platf(self):
        x1 = self.x
        y1 = self.y
        h1 = 10  # длина doodle
        l1 = 10  # ширина doodle
        collis = False
        for i in platforms:
            h2 = i.get_height()  # длина platf
            l2 = i.get_len  # ширина platf
            x2 = i.get_posit()[0]
            y2 = i.get_posit()[1]
            if (x1 + l1) >= x2 and (y1 + h1 <= y2 or y1 <= y2 + h2) or (x1 <= x2 + l2) and \
                    (y1 + h1 >= y2 or y1 >= y2 + h2):
                collis = True
        return collis


class Wings:
    def __init__(self):
        self.height = Background.get_result
        self.coor = (self.x, self.y) = (randint(0, 500), randint(0, 600))

    def get_coor(self):
        return self.coor


class Platforms:
    def __init__(self, y=-1):
        if y == -1:
            self.coor = (self.x, self.y) = (randint(0, 490), randint(0, 500))
        else:
            self.coor = (self.x, self.y) = (randint(0, 490), y)
        self.hight = 3

    def down(self):
        self.coor = (self.x, self.y + self.hight)

    def below_wind(self):
        if self.y > 600:
            self.coor = (self.x, self.y) = (randint(0, 1800), 0)


class Start_End:
    def __init__(self):
        pass

    def end(self):
        return False


class Background:
    def __init__(self):
        self.result = 1
        self.dir = os.path.dirname(__file__)
        self.record = 0

    def get_result(self):
        with open(os.path.join(self.dir, record_height), 'r+') as f:
            self.record = int(f.read())
        if self.result >= self.record:  # новый рекорд
            self.record = self.result
            with open(os.path.join(self.dir, record_height), 'w') as f:  # изменение рекорда
                f.write(str(self.result))
            text = ['Поздравляем!',
                    'У вас новый рекорд: {}'.format(self.result)]
        else:
            text = ['Рекорд: {}'.format(self.record),
                    'Ваш результат: {}'.format(self.result)]
        return text


class Land:
    def __init__(self, coor=550):
        self.land_coor = (0, 550, width, height - 550)

    def in_screen(self):
        if self.land_coor[1] < 600:
            return True
        else:
            return False

    def draw(self):
        screen.fill(pygame.Color('green'), pygame.Rect(self.land_coor))

    def jump(self, height):
        self.land_coor[1] += height


platforms = []
monsters = []
main = Doodle()
land = Land()
back = Background()

FPS = 60
v = 3
jump_time = 0
first_game = True


def start_pictures(fon, text, record=-5, font_num=20):
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 75)
    text_coord = 50
    screen.blit(font.render('Doodle_Прыг', 1, (0, 0, 0)), (70, 10))
    font = pygame.font.Font(None, font_num)
    interval = 10
    if font_num == 40:
        interval = 20
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += interval
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    if record != -5:
        screen.blit(font.render("Ваш рекорд: {}".format(record), 1, (0, 0, 0)), (10, 550))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global first_game, land
    intro_text = ["Нажимая клавиши 'вправо', 'влево',",
                  "перемещайте героя на платформы.",
                  "Избегайте монстров и старайтесь не падать.",
                  "Крылья помогут вам взлететь!"]

    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, record_height), 'r+') as f:
        record = int(f.read())
    fon = pygame.transform.scale(load_image('fon.jpg'), size)

    run = True
    time_picture = 0
    start = False
    while run:
        ev = None
        for event in pygame.event.get():
            ev = None
            if event.type == pygame.QUIT:
                run = False
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if start is False:
                    land = Land(550)
                start = True
                ev = event
        if start:
            the_game(time_picture, ev)  # начинаем игру
        else:
            if int(time_picture % 2) == 0:
                start_pictures(fon, intro_text, record)
                screen.blit(doodle, (-20, 170))
            else:
                start_pictures(fon, intro_text, record)
                screen.blit(doodle_jump, (-20, 170))
        time_picture += v / FPS
        pygame.display.flip()
        clock.tick(FPS)


def the_game(jump_time, ev=None):
    global doodle, doodle_jump, first_game, land
    if main.check_end:
        the_end(jump_time, back.get_result())
    else:
        screen.fill((0, 191, 255))
        if land.in_screen() is True:
            land.draw()
            doodle = pygame.transform.scale(doodle, (90, 60))
        screen.blit(doodle, main.get_posit())
        # main.change_high(time)
        if ev:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT:
                    main.left()
                elif ev.key == pygame.K_RIGHT:
                    main.right()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] < main.get_posit()[0] + 45:
                    main.left()
                elif pygame.mouse.get_pos()[0] > main.get_posit()[0] + 45:
                    main.right()


def the_end(picture_time, results):
    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    start_pictures(fon, results, -5, 40)
    if int(picture_time % 2) == 0:
        screen.blit(doodle, (-20, 170))
    else:
        screen.blit(doodle_jump, (-20, 170))


start_screen()
