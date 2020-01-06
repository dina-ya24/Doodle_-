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

FPS = 60
v = 3
start = False


def start_pictures(fon, intro_text, record):
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 75)
    text_coord = 50
    screen.blit(font.render(intro_text[0], 1, (0, 0, 0)), (70, 10))
    font = pygame.font.Font(None, 20)
    for line in intro_text[1:]:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    screen.blit(font.render("Ваш рекорд: {}".format(record), 1, (0, 0, 0)), (10, 550))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Doodle_Прыг", "",
                  "Нажимая клавиши 'вправо', 'влево',",
                  "перемещайте героя на платформы.",
                  "Избегайте монстров и старайтесь не падать.",
                  "Крылья помогут вам взлететь!"]

    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, record_height), 'r+') as f:
        record = int(f.read())
    fon = pygame.transform.scale(load_image('fon.jpg'), size)

    run = True
    start = False
    time_picture = 0
    first = False
    while run:
        ev = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or \
                    start is True:
                if start is False:
                    first = True
                    start = True
                else:
                    first = False
                ev = event
        if start is True:
            the_game(first, time_picture, ev)
        if int(time_picture % 2) == 0 and start is False:
            start_pictures(fon, intro_text, record)
            screen.blit(doodle, (-20, 170))
        elif start is False:
            start_pictures(fon, intro_text, record)
            screen.blit(doodle_jump, (-20, 170))
        time_picture += v / FPS
        # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


class Doodle:
    def __init__(self):
        self.coor = (self.x, self.y) = (210, 540)
        self.hight = -10

    def jump(self):
        self.coor = (self.x, self.y + self.hight)

    def right(self):
        self.coor = (self.x + 10, self.coor[1])

    def left(self):
        self.coor = (self.x - 10, self.coor[1])

    def change_high(self, time):
        if time % 33333333:
            if time < 100:
                self.hight += 1
            else:
                self.hight -= 1

    def get_posit(self):
        return self.coor

    def check_end(self):
        if self.y >= 1200 or self.collision():
            Start_End.end(Background.get_result())

    def collision(self):
        x1 = self.x
        y1 = self.y
        l1 = 18  # ширина doodle
        h1 = 12  # длина doodle
        l2 = 18  # ширина monster
        h2 = 12  # длина monster
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
        h1 = 10  #длина doodle
        l1 = 10  #ширина doodle
        collis = False
        for i in platforms:
            h2 = i.get_height()  #длина platf
            l2 = i.get_len  #ширина platf
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
        pass


class Background:
    def __init__(self):
        self.result = 0
        self.dir = os.path.dirname(__file__)

    def get_result(self):
        with open(os.path.join(self.dir, record_height), 'r+') as f:
            self.record = int(f.read())
        if self.result > self.record:  # новый рекорд
            self.record = self.result
            with open(os.path.join(self.dir, record_height), 'w') as f:  # изменение рекорда
                f.write(str(self.result))
            return 'Поздравляем! Увас новый рекорд', self.record
        else:
            return 'Рекорд: {}'.format(self.record), 'Ваш результат: {}'.format(self.result)


platforms = []
monsters = []

main = Doodle()


def the_game(first, time, ev=None):
    global doodle, doodle_jump, start
    if first is True:
        screen.fill((0, 191, 255))
        screen.fill(pygame.Color('green'), pygame.Rect(0, 550, width, height - 550))
        doodle = pygame.transform.scale(doodle, (90, 60))
    screen.blit(doodle, main.get_posit())
    main.change_high(time)
    if ev:
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_LEFT:
                main.left()
            elif ev.key == pygame.K_RIGHT:
                main.right()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[0] < main.get_posit()[0]:
                main.left()
            elif pygame.mouse.get_pos()[0] > main.get_posit()[0]:
                main.right()
        if main.check_end:
            start = False


start_screen()
