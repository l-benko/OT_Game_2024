from settings import *


class Sprite(pygame.sprite.Sprite):
    # basic sprite class to handle a static object
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=position)
        self.ground = True


class CollisionSprite(pygame.sprite.Sprite):
    # collisionSprite class for handling sprites that can collide, but without animations
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)


class Enemy(pygame.sprite.Sprite):
    # enemy class that follows and animates based on player movement
    def __init__(self, position, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        # initialize enemy animation frames
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6
        # initialize rectangle and hitbox for collision detection
        self.rect = self.image.get_frect(center = position)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 150
        self.death_time = 0 # track the time when the enemy dies
        self.death_duration = 400 # duration for the death animation or timer

    def animate(self, delta):
        # animate enemy sprite by looping through frames based on delta time
        self.frame_index += self.animation_speed * delta
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def move(self, delta):
        # calculate movement direction towards the player
        player_position = pygame.Vector2(self.player.rect.center)
        enemy_position = pygame.Vector2(self.rect.center)
        self.direction = (player_position - enemy_position).normalize() # get normalized direction vector
        self.hitbox_rect.x += self.direction.x * self.speed * delta # move horizontally
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * delta # move vertically
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center # update the main rectangle's position based on the hitbox

    def collision(self, direction):
        # handle collision with other sprites
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect): # if the enemy collides with another sprite
                if direction == "horizontal":
                    if self.direction.x > 0: # moves right
                        self.hitbox_rect.right = sprite.rect.left # stop at the left side of the sprite
                    if self.direction.x < 0: # moves left
                        self.hitbox_rect.left = sprite.rect.right # stop at the right side of the sprite
                if direction == "vertical":
                    if self.direction.y > 0: # moves up
                        self.hitbox_rect.bottom = sprite.rect.top # stop at the top side of the sprite
                    if self.direction.y < 0: # moves down
                        self.hitbox_rect.top = sprite.rect.bottom # stop at the bottom side of the sprite

    def update(self, delta):
        # update enemy behavior based on its state
        if self.death_time == 0: # if the enemy is alive
            self.move(delta)
            self.animate(delta)
        else:
            self.death_timer() # handle death logic if the enemy is dead

    def death_timer(self):
        # handle the death timer and remove the enemy after a set duration
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill() # remove the enemy sprite from the game

    def destroy(self):
        self.death_time = pygame.time.get_ticks() # record the time of death
        surface = pygame.mask.from_surface(self.frames[0]).to_surface()  # create a silhouette of the enemy for death animation
        surface.set_colorkey('black') # set the color key for transparency
        self.image = surface # set the death image


class FireBall(pygame.sprite.Sprite):
    def __init__(self, surface, position, direction, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center = position)
        self.direction = direction
        self.speed = 1000
        self.lifetime = 1000 # lifetime of the fireball in milliseconds
        self.spawn_time = pygame.time.get_ticks() # record the time the fireball was spawned

    def update(self, delta):
        # move the fireball and check if it has lived long enough to be removed
        self.rect.center += self.direction * self.speed * delta
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
