import sys

from settings import *
from pytmx.util_pygame import load_pygame
from sprites import *


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("OT Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.setup_map()


    def setup_map(self):
        map = load_pygame(join('assets', 'map', 'level.tmx'))
        for x, y, image in map.get_layer_by_name('terrain').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), image, self.all_sprites)

    def run(self):
        while self.running:
            delta = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()