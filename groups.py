from settings import *


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2() # initialize offset to adjust sprite positions based on camera

    def draw(self, target_position):
        # calculate the offset to center the target position (the player's position) on the screen
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)
        # separate sprites into two layers: ground (those with a 'ground' attribute) and object sprites (those without)
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]
        # draw each layer in order, with ground sprites first and object sprites second
        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery): # sort sprites by vertical position (y-axis)
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset) # draw sprite with offset applied