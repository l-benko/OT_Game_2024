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
        self.direction = (player_position - enemy_position).normalize()
        self.hitbox_rect.x = self.direction.x * self.speed * delta
        self.collision('horizontal')
        self.hitbox_rect.y = self.direction.y * self.speed * delta
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.direction.x > 0: # moves right
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: # moves left
                        self.hitbox_rect.left = sprite.rect.right
                if direction == "vertical":
                    if self.direction.y > 0: # moves up
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: # moves down
                        self.hitbox_rect.top = sprite.rect.bottom

    def update(self, delta):
        self.move(delta)
        self.animate(delta)