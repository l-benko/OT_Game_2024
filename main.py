import sys

from settings import *
from pytmx.util_pygame import load_pygame
from sprites import *
from player import Player
from groups import AllSprites
from random import choice
from button import Button


class Game:
    def __init__(self):
        pygame.init() # initialize Pygame
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("OT Game")
        self.clock = pygame.time.Clock() # create a clock object for controlling frame rate
        self.running = True
        # initialize sprite groups for managing game entities
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.fireball_sprites = pygame.sprite.Group()
        # shooting cooldown management
        self.can_shoot = True # variable to control if the player can shoot
        self.shoot_time = 0 # the time when the player last shot
        self.shoot_cooldown = 300 # cooldown time between shots (in milliseconds)
        # enemy spawn management
        self.enemy_event = pygame.event.custom_type() # custom event for enemy spawn
        pygame.time.set_timer(self.enemy_event, 500) # set timer for enemy spawn event every 500 ms
        self.enemy_spawn_positions = [] # list to store possible spawn positions for enemies

        # load audio for the game
        self.shoot_sound = pygame.mixer.Sound(join('assets', 'audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.4) # set volume for shoot sound
        self.impact_sound = pygame.mixer.Sound(join('assets', 'audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('assets', 'audio', 'music.wav'))
        self.music.set_volume(0.3) # set background music volume
        self.music.play(loops=-1) # loop the music indefinitely

        self.setup_map()
        self.fireball_surface = pygame.image.load(join('assets', 'fireball', 'ball.png')).convert_alpha()
        self.load_enemies()


    def setup_map(self):
        # load the map using pytmx from Tiled map editor file (.tmx)
        map = load_pygame(join('assets', 'map', 'level.tmx'))
        for x, y, image in map.get_layer_by_name('terrain').tiles(): # set up terrain layer (static ground objects)
            Sprite((x*TILE_SIZE, y*TILE_SIZE), image, self.all_sprites)
        for item in map.get_layer_by_name('objects non'): # set up non-interactive objects
            Sprite((item.x, item.y), item.image, self.all_sprites)
        for item in map.get_layer_by_name('objects'): # set up interactive objects that can trigger collisions
            if item.image is not None:
                CollisionSprite((item.x, item.y), item.image, (self.all_sprites, self.collision_sprites))
        for item in map.get_layer_by_name('collisions'): # set up collision rectangles for specific areas
            CollisionSprite((item.x, item.y), pygame.Surface((item.width, item.height)), self.collision_sprites)
        for item in map.get_layer_by_name('entities'): # set up entities: the player and enemies
            if item.name == 'Player':
                self.player = Player((item.x, item.y), self.all_sprites, self.collision_sprites)
            if item.name == 'Enemy':
                self.enemy_spawn_positions.append((item.x, item.y))

    def load_enemies(self):
        # load enemy images for different enemy types
        folders = list(walk(join('assets','enemies')))[0][1] # get enemy folder names
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('assets','enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surface = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surface)

    def input(self):
        # handle player input for shooting
        if pygame.mouse.get_pressed()[0] and self.can_shoot: # if left mouse button is pressed and can shoot
            self.shoot_sound.play()
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) # get mouse position
            player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)  # player is always centered
            player_direction = (mouse_pos - player_pos).normalize() # calculate direction from player to mouse
            FireBall(self.fireball_surface, self.player.rect.center, player_direction, (self.all_sprites, self.fireball_sprites))
            self.can_shoot = False # set shooting variable to false until cooldown
            self.shoot_time = pygame.time.get_ticks() # record the time when the shot was made

    def shoot_timer(self):
        # handle shooting cooldown timer
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() # get current time
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.can_shoot = True # allow shooting again

    def fireball_collision(self):
        # handle collisions between fireballs and enemies
        if self.fireball_sprites:
            for fireball in self.fireball_sprites:
                collided_sprites = pygame.sprite.spritecollide(fireball, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collided_sprites:
                    self.impact_sound.play()
                    for sprite in collided_sprites:
                        sprite.destroy() # destroy enemy sprite
                    fireball.kill() # destroy fireball after collision

    def player_collision(self):
        # check if the player collides with any enemies
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False # end the game if the player collides with an enemy

    def start_screen(self):
        # display start screen with a start button
        start = True
        start_button = Button(WINDOW_WIDTH//2-50, WINDOW_HEIGHT//2-20, 100, 50, pygame.Color('black'), pygame.Color('white'), 'Start', 32)
        while start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                    self.running = False # quit the game if the window is closed
            mouse_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if start_button.is_pressed(mouse_position, mouse_pressed): # check if start button is pressed
                start = False
                self.run() # start the game
            self.display_surface.blit(start_button.image, start_button.rect)
            self.clock.tick(60)
            pygame.display.update()

    def run(self):
        # main game loop
        while self.running:
            delta = self.clock.tick() / 1000 # calculate time difference for frame rate independence

            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    position = choice(self.enemy_spawn_positions) # randomly select an enemy spawn position
                    enemy = choice(list(self.enemy_frames.values())) # randomly select an enemy type
                    Enemy(position, enemy, (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            # update game state
            self.shoot_timer()  # handle shooting cooldown
            self.input()  # handle player input
            self.all_sprites.update(delta)  # update all sprites
            self.fireball_collision()  # check for fireball collisions
            self.player_collision()  # check for player collisions with enemies
            self.display_surface.fill('black')  # clear the screen
            self.all_sprites.draw(self.player.rect.center)  # draw all sprites
            pygame.display.update()  # update the display surface
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.start_screen() # display the start screen