import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    index = 0
    levels = ["level1.tmx", "level2.tmx"]
    def __init__(self):
        pg.init()
        pg.mixer.init(frequency=2000)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) #Add pg.FULLSCREEN to enable full screen.
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        audio_folder = path.join(game_folder, 'audio')
        self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        if (self.index < len(self.levels) - 1):
            self.index = self.index + 1
        else:
            self.index = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.shadow = pg.sprite.Group()
        self.exit = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'enemy':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'shadow':
                Shadow(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name in ['key']:
                Item(self, obj_center, 'key')
            if tile_object.name == 'exit':
                Exit(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'key':
                hit.kill()
                self.player.has_key = True
                print(self.player.has_key)
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
            hit.vel = vec(0, 0)
        hits = pg.sprite.spritecollide(self.player, self.doors, False, collide_hit_rect)
        for hit in hits:
            if(hit.type == 'Door'):
                if(self.player.has_rk == True):
                    hit.kill()
                    self.player.has_rk = False
                else:
                    self.player.collide_with_walls(self.doors, 'x')
                    self.player.collide_with_walls(self.doors, 'y')
        hits = pg.sprite.spritecollide(self.player, self.exit, False, collide_hit_rect)
        for hit in hits:
            if self.player.has_key:
                game_folder = path.dirname(__file__)
                map_folder = path.join(game_folder, 'maps')
                self.map = TiledMap(path.join(map_folder, self.levels[self.index]))
                self.map_img = self.map.make_map()
                self.map_rect = self.map_img.get_rect()
                self.new()
            else:
                self.player.objective = "Door is locked. Find the key"

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions

        self.draw_text(self.player.objective, 20, BLACK, (WIDTH/2) +1,21)
        self.draw_text(self.player.objective, 20, WHITE, WIDTH/2,20)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.draw_debug = not self.draw_debug

    def show_start_screen(self):

        self.menu_music = pg.mixer.music.load('audio/Full of memories.ogg')
        pg.mixer.music.play()
        self.screen.fill(LIGHTBLUE)
        self.draw_text(TITLE, 40, RED, WIDTH/2, (HEIGHT/2)-60)
        self.draw_text("press any key to play", 20, RED, WIDTH/2, (HEIGHT/2) + 30)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.stop()


    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("You have been diagnosed", 30, WHITE, WIDTH/2, (HEIGHT/2)-40)
        self.draw_text("with dead.",30,WHITE, WIDTH/2, (HEIGHT/2))
        pg.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
    g.show_start_screen()



# Full Of Memories was created by Alexandr Zhelanov, and the song was found on OpenGameArt.org
    # https://opengameart.org/content/full-of-memories

