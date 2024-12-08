from settings import *


class Button:
    def __init__(self, x, y, width, height, foreground_color, background_color, content, fontsize):
        self.font = pygame.font.Font(join('assets','fonts','Cooper Black Regular.ttf'), fontsize)
        self.image = pygame.Surface((width, height))
        self.image.fill(background_color)
        self.rect = self.image.get_frect(topleft=(x, y))
        self.text = self.font.render(content, True, foreground_color)
        self.text_rect = self.text.get_frect(center=(width/2, height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, position, pressed):
        if self.rect.collidepoint(position):
            if pressed[0]:
                return True
            return False
        return False
