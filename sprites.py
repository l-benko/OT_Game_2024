from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=position)
        self.ground = True


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        # image
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6
        # rectangle
        self.rect = self.image.get_frect(center = position)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 150

    def animate(self, delta):
        self.frame_index += self.animation_speed * delta
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def move(self, delta):
        player_position = pygame.Vector2(self.player.rect.center)
        enemy_position = pygame.Vector2(self.rect.center)
        print(self.direction)
        self.direction = (player_position - enemy_position).normalize()
        self.hitbox_rect.x = self.direction.x * self.speed * delta
        self.hitbox_rect.y = self.direction.y * self.speed * delta
        self.rect.center = self.hitbox_rect.center

    def update(self, delta):
        self.move(delta)
        self.animate(delta)