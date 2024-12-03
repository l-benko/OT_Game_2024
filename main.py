import sys

from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("OT Game")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            delta = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()