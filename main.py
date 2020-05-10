# Tic Tac Toe game with Pygame 1.9.6, April 2020 Kerman
# Game music: Observing the Star, by yd
# Menu music: Loading screen loop, by Brandon Morris
# Sound effects: bfxr.net
import pygame as pg
from os import environ, path
from sprites import *
from settings import *

# center the screen when opening app
environ['SDL_VIDEO_CENTERED'] = '1'


class Game():
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Tic Tac Toe")
        self.font_name = pg.font.match_font("segoe print")
        self.running = True
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, "img")
        self.snd_dir = path.join(self.dir, "snd")
        self.back = pg.image.load(path.join(self.img_dir, "Back.png")).convert()
        self.back.set_colorkey(BLACK)
        self.back_rect = self.back.get_rect()
        self.back_rect.topleft = (30, 25)
        self.gridi = ([30, 170], [175, 310], [315, 455])
        self.gridj = ([25, 165], [170, 310], [320, 455])
        self.clickx, self.clicky = 0, 0
        self.player_sound = pg.mixer.Sound(path.join(self.snd_dir, "player_move.wav"))
        self.player_sound.set_volume(0.2)
        self.comp_sound = pg.mixer.Sound(path.join(self.snd_dir, "comp_move.wav"))
        self.comp_sound.set_volume(0.2)
        self.select = pg.mixer.Sound(path.join(self.snd_dir, "select.wav"))
        self.select.set_volume(0.4)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        # initialize the game array with all zeros
        self.state = [[0] * 3 for i in range(3)]
        self.count = self.initial
        self.comtimer = pg.time.get_ticks()
        self.pos, self.winner = None, None
        self.comp = Comp(self)
        pg.mixer.music.load(path.join(self.snd_dir, "ObservingTheStar.ogg"))
        self.run()

    def run(self):
        self.playing = True
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.2)
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                clickx, clicky = pg.mouse.get_pos()
                # only check if clicked position is valid
                if 30 <= clickx <= 455 and 25 <= clicky <= 455:
                    self.pos = self.grid_pos_from_mouse(clickx, clicky)

    def update(self):
        self.all_sprites.update()
        # count holds the information for whose turn it is
        if self.count % 2 == 0:
            if self.pos and not self.state[self.pos[1]][self.pos[0]]:
                Psymb(self, sum(self.gridi[self.pos[0]]) // 2, sum(self.gridj[self.pos[1]]) // 2)
                self.player_sound.play()
                self.state[self.pos[1]][self.pos[0]] = 1
                self.pos = None
                self.count += 1
                self.comtimer = pg.time.get_ticks()
        else:
            # wait for a second for the computer to play for more immersion
            if pg.time.get_ticks() - self.comtimer > 1000:
                a, b = self.comp.play()
                self.state[a][b] = 2
                Compsymb(self, sum(self.gridj[b]) // 2, sum(self.gridi[a]) // 2)
                self.comp_sound.play()
                self.count += 1

        # check if game has ended after every move
        self.check_end()

    def draw(self):
        self.screen.fill(LIGHTGREY)
        self.screen.blit(self.back, self.back_rect)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, "TremLoadingloopl.ogg"))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.3)
        back = pg.image.load(path.join(self.img_dir, "Start.jpg")).convert()
        back_rect = back.get_rect()
        rect_grp = pg.sprite.Group()
        p1 = Menurect(self, WIDTH / 2 - 60, HEIGHT / 2 - 30)
        rect_grp.add(p1)
        com = Menurect(self, WIDTH / 2 + 60, HEIGHT / 2 - 30)
        rect_grp.add(com)

        # wait for the player to choose on start screen
        flag = True
        while flag:
            self.clock.tick(FPS)
            self.screen.blit(back, back_rect)
            rect_grp.update()
            pg.draw.rect(self.screen, [0, 0, 0], (WIDTH / 2 - 117, HEIGHT / 2 - 57, 114, 53), 2)
            pg.draw.rect(self.screen, [0, 0, 0], (WIDTH / 2 + 3, HEIGHT / 2 - 57, 114, 53), 2)
            rect_grp.draw(self.screen)
            self.draw_text("TIC TAC TOE", 40, BLACK, WIDTH / 2, HEIGHT / 2 - 180)
            self.draw_text("Who starts ? ", 30, BLACK, WIDTH / 2, HEIGHT / 2 - 120)
            self.draw_text("Me", 20, BLACK, WIDTH / 2 - 60, HEIGHT / 2 - 50)
            self.draw_text("Computer", 20, BLACK, WIDTH / 2 + 60, HEIGHT / 2 - 50)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    flag = False
                    self.running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    # check who starts the game
                    pos = pg.mouse.get_pos()
                    hit1 = p1.rect.collidepoint(pos)
                    if hit1:
                        self.initial = 0
                        flag = False
                    hit2 = com.rect.collidepoint(pos)
                    if hit2:
                        self.comtimer = pg.time.get_ticks()
                        self.initial = 1
                        flag = False
        self.select.play()
        pg.mixer.music.fadeout(500)

    def end_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, "TremLoadingloopl.ogg"))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.3)
        if self.running:
            if self.winner == 0:
                self.draw_text("It's a draw !", 20, BLACK, WIDTH / 2, HEIGHT / 2 - 244)
            if self.winner == 1:
                self.draw_text("You win !", 20, BLACK, WIDTH / 2, HEIGHT / 2 - 244)
            if self.winner == 2:
                self.draw_text("Computer wins !", 20, BLACK, WIDTH / 2, HEIGHT / 2 - 244)
            self.draw_text("Press anywhere to play again", 20, BLACK, WIDTH / 2, HEIGHT / 2 + 208)
            pg.display.flip()
            self.wait_for_key()

    def wait_for_key(self):
        w_start = pg.time.get_ticks()
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN and pg.time.get_ticks() - w_start > 500:
                    waiting = False
                    self.select.play()
                    pg.mixer.music.fadeout(500)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def grid_pos_from_mouse(self, x, y):
        # get the position in 2D game array by checking where player clicked
        i = [i for i in range(3) if self.gridi[i][0] <= x <= self.gridi[i][1]][0]
        j = [j for j in range(3) if self.gridj[j][0] <= y <= self.gridj[j][1]][0]
        return (i, j)

    def check_end(self):
        # check for a win of a player or a draw
        for player in [1, 2]:
            cols = [col for col in list(zip(*self.state))]
            dia1 = [self.state[0][0], self.state[1][1], self.state[2][2]]
            dia2 = [self.state[2][0], self.state[1][1], self.state[0][2]]
            for row in self.state:
                if all(row[j] == player for j in range(3)):
                    self.playing = False
                    self.winner = player
            for col in cols:
                if all(col[j] == player for j in range(3)):
                    self.playing = False
                    self.winner = player
            if dia1.count(player) == 3:
                self.playing = False
                self.winner = player
            if dia2.count(player) == 3:
                self.playing = False
                self.winner = player

        # check if all elements of game array have been changed
        if 0 not in [item for sublist in self.state for item in sublist]:
            if self.playing:
                self.playing = False
                self.winner = 0


# game loop
g = Game()
g.start_screen()
while g.running:
    g.new()
    g.end_screen()

pg.quit()
