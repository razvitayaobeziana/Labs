import math
from random import choice, randint
import pygame
from pygame.draw import *

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450, gravity=-2):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.gravity = gravity

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x >= 800 - 1.5 * self.r:
            self.vx = - 0.8 * self.vx
            self.x = 800 - 1.5 * self.r
        if self.x <= 1.5 * self.r:
            self.vx = - 0.8 * self.vx
            self.x = 1.5 * self.r
        if self.y >= 530 - 1.6 * self.r:
            self.y = 530 - 1.5 * self.r
            self.vy = - 0.8 * self.vy
            self.vx = 0.8 * self.vx
        if abs(self.vx) <= 1:
            self.vx = 0
        if abs(self.y - 530) > 1.5 * self.r:
            self.vy += self.gravity
        self.x += self.vx
        if abs(self.vy) <= 1 and abs(self.y - 530) <= 1.5 * self.r:
            self.vy = 0
            self.y = 530 - 1.5 * self.r
            self.gravity
        self.y -= self.vy
        if abs(self.vy) == 0:
            self.live -= 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):

        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False

class SuperBall(Ball):
    """Пока недоделанный класс второго типа мишени"""
    def __init__(self,*args):
        super().__init__(*args)
        self.r = 30

    def draw(self):
        circle(screen, (199, 199, 0), (self.x, self.y), self.r)
        rect(screen, (0, 0, 0), (self.x - self.r * 0.5, self.y + self.r * 0.5, self.r, self.r * 0.2))
        circle(screen, (240, 0, 0), (self.x - self.r * 0.4, self.y - self.r * 0.25), self.r * 0.2)
        circle(screen, (0, 0, 0), (self.x - self.r * 0.4, self.y - self.r * 0.26), self.r * 0.09)
        circle(screen, (240, 0, 0), (self.x + self.r * 0.4, self.y - self.r * 0.3), self.r * 0.15)
        circle(screen, (0, 0, 0), (self.x + self.r * 0.4, self.y - self.r * 0.3), self.r * 0.07)
        line(screen, (0, 0, 0), (self.x - self.r * 0.2, self.y - self.r * 0.5), (self.x - self.r * 0.75, self.y - self.r * 0.7), int(self.r * 0.15))
        line(screen, (0, 0, 0), (self.x + self.r * 0.1, self.y - self.r * 0.4), (self.x + self.r * 0.65, self.y - self.r * 0.6), int(self.r * 0.15))



class Gun:
    def __init__(self, screen):
        """Конструктор класса Gun"""
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = True

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = False
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0]<=50 and event.pos[1]<=450:
                self.an = -9999999
            elif event.pos[0] <= 50 and event.pos[1] >= 450:
                self.an = 9999999
            else:
                self.an = math.atan((event.pos[1] - 450) / (event.pos[0] -50))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Отрисовка пушки"""
        if self.f2_on:
            pygame.draw.line(screen, YELLOW, (40, 450),
                             (50 + 1 * self.f2_power * math.cos(self.an), 450 + 1 * self.f2_power * math.sin(self.an)),
                             10)
        else:
            pygame.draw.line(screen, GREY, (40, 450), (50 + 10 * math.cos(self.an), 450 + 10 * math.sin(self.an)), 10)

    def power_up(self):
        """Увеличение мощности выстрела при удержании мыши"""
        if self.f2_on:
            if self.f2_power < 150:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY



class Target:
    """Конструктор класса Target"""
    def __init__(self):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели"""
        self.r = randint(20, 50)
        self.x = randint(100 + self.r, 800 - self.r)
        self.y = randint(0 + self.r, 530 - self.r)
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.color = RED

    def move(self):
        """Переместить мишень по прошествии единицы времени.
            Метод описывает перемещение мишени за один кадр перерисовки. То есть, обновляет значения
            self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
            и стен по краям окна (размер окна 800х600)."""
        if self.x >= 800 - self.r:
            self.vx = -self.vx
            self.x = 800 - self.r
        if self.x <= 1.5 * self.r:
            self.vx = -self.vx
            self.x = 1.5 * self.r
        if self.y >= 530 - self.r:
            self.y = 530 - self.r
            self.vy = - self.vy
        if self.y <= 1.5 * self.r:
            self.y = 1.5 * self.r
            self.vy = - self.vy
        self.x += self.vx
        self.y += self.vy

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        """Отрисовка мишени"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, 2)



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
superballs = []

clock = pygame.time.Clock()
gun = Gun(screen)
first_target = Target()
second_target = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    first_target.draw()
    second_target.draw()
    for b in balls:
        if b.live > 0:
            b.draw()

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(first_target) and first_target.live:
            first_target.hit()
            first_target.new_target()
        if b.hittest(second_target) and second_target.live:
            second_target.hit()
            second_target.new_target()
    gun.power_up()
    first_target.move()
    second_target.move()

pygame.quit()
