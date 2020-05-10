# sprites for player and computer
import pygame as pg
import random
from os import path
from settings import *


class Psymb(pg.sprite.Sprite):
    # sprite for the player symbol
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(self.game.img_dir, "X.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x, y


class Comp():
    # simple AI to play against
    def __init__(self, game):
        self.game = game
        self.state = game.state

    def play(self):
        # first check if there's a chance to win, then if you can lose
        # place symbol randomly if going first
        # digit 2 used for computer in the game 2D array 
        count = 2
        while count > 0:
            a = self.check_state(2, count)
            if a:
                return a
            b = self.check_state(1, count)
            if b:
                return b
            count -= 1
        x = random.randrange(0, 3)
        y = random.randrange(0, 3)
        return (x, y)

    def check_state(self, pl, count):
        # first checks diagonals, then rows, then columns
        # prefers the first pos found in case of multiple possibilities
        cols = [col for col in list(zip(*self.state))]
        dia1 = [self.state[0][0], self.state[1][1], self.state[2][2]]
        dia2 = [self.state[2][0], self.state[1][1], self.state[0][2]]
        if dia1.count(pl) == count:
            miss = [i for i in range(3) if dia1[i] != pl][0]
            if not self.state[miss][miss]:
                return (miss, miss)
        if dia2.count(pl) == count:
            miss = [i for i in range(3) if dia2[i] != pl][0]
            if not self.state[2 - miss][miss]:
                return(2 - miss, miss)
        for i, row in enumerate(self.state):
            if row.count(pl) == count:
                miss = [j for j in range(3) if row[j] != pl][0]
                if not self.state[i][miss]:
                    return (i, miss)
        for j, col in enumerate(cols):
            if col.count(pl) == count:
                miss = [i for i in range(3) if col[i] != pl][0]
                if not self.state[miss][j]:
                    return (miss, j)
        return None


class Compsymb(pg.sprite.Sprite):
    # sprite for the computer symbol
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(self.game.img_dir, "O.png")).convert_alpha()
        self.image = pg.transform.scale(self.image, (84, 71))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x, y


class Menurect(pg.sprite.Sprite):
    # Start menu rectangles
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((110, 50))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x, y

    def update(self):
        # change color if mouse hovers over the rectangle
        pos = pg.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        if hit:
            self.image.fill(LIGHTGREY)
        else:
            self.image.fill(GREY)
