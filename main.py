import sys

from settings import *
from pytmx.util_pygame import load_pygame
from sprites import *
from player import Player
from groups import AllSprites
from random import choice


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("OT Game")
        self.clock = pygame.time.Clock()
        self.running = True
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.fireball_sprites = pygame.sprite.Group()
        # enemy spawn timer and positions
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 500)
        self.enemy_spawn_positions = []

        self.setup_map()
        self.fireball_surface = pygame.image.load(join('assets', 'fireball', 'ball.png')).convert_alpha()
        self.load_enemies()


    def setup_map(self):
        map = load_pygame(join('assets', 'map', 'level.tmx'))
        for x, y, image in map.get_layer_by_name('terrain').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), image, self.all_sprites)
        for item in map.get_layer_by_name('objects non'):
            Sprite((item.x, item.y), item.image, self.all_sprites)
        for item in map.get_layer_by_name('objects'):
            if item.image is not None:
                CollisionSprite((item.x, item.y), item.image, (self.all_sprites, self.collision_sprites))
        for item in map.get_layer_by_name('collisions'):
            CollisionSprite((item.x, item.y), pygame.Surface((item.width, item.height)), self.collision_sprites)
        for item in map.get_layer_by_name('entities'):
            if item.name == 'Player':
                self.player = Player((item.x, item.y), self.all_sprites, self.collision_sprites)
            if item.name == 'Enemy':
                self.enemy_spawn_positions.append((item.x, item.y))

    def load_enemies(self):
        folders = list(walk(join('assets','enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('assets','enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surface = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surface)

    def input(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)  # because the player is always in window center
            player_direction = (mouse_pos - player_pos).normalize()
            FireBall(self.fireball_surface, self.player.rect.center, player_direction, (self.all_sprites, self.fireball_sprites))

    def run(self):
        while self.running:
            delta = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    position = choice(self.enemy_spawn_positions)
                    enemy = choice(list(self.enemy_frames.values()))
                    Enemy(position, enemy, (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            # update
            self.input()
            self.all_sprites.update(delta)
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()