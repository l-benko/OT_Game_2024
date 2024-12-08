from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites):
        super().__init__(groups)
        # initialize player graphics and set up the sprite
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []} # store animations for all movement directions
        self.load_images() # load images for the animations
        self.state, self.frame_index = 'down', 0 # set the initial state and frame index for animation
        self.image = pygame.image.load(join('assets','player',self.state,'0.png')).convert_alpha() # load the first image of the state
        self.image = pygame.transform.scale(self.image, (128, 128)) # scale up the image as it is too small
        self.rect = self.image.get_frect(center=position) # create rectangle for the image
        self.hitbox_rect = self.rect.inflate(-120, -120)  # solves the gap between image and obstacle
        # move player
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def load_images(self):
        # load all images for the different movement states (up, down, left, right)
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('assets','player',state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name) # gets the fullpath to the image
                        surface = pygame.image.load(full_path).convert_alpha() # create surface for image
                        self.frames[state].append(surface) # append surface into dictionary

    def animate(self, delta):
        # set player animation based on movement direction
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x >0 else 'left' # determine horizontal direction
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y >0 else 'up' # determine vertical direction
        self.frame_index = (self.frame_index +5 * delta) if self.direction else 0 # update the animation frame
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])] # get the current frame image
        self.image = pygame.transform.scale(self.image, (128, 128)) # scale the image

    def move(self, delta):
        # move player and handle collisions with obstacles
        #self.rect.center += self.direction * self.speed * delta
        self.hitbox_rect.x += self.direction.x * self.speed * delta
        self.collision("horizontal")
        self.hitbox_rect.y += self.direction.y * self.speed * delta
        self.collision("vertical")
        self.rect.center = self.hitbox_rect.center # update the main rect position after moving

    def collision(self, direction):
        # check for collisions with other sprites
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect): # if a collision is detected
                if direction == 'horizontal':
                    if self.direction.x > 0: # move right
                        self.hitbox_rect.right = sprite.rect.left # stop at the left edge of the obstacle
                    if self.direction.x < 0: # move left
                        self.hitbox_rect.left = sprite.rect.right # stop at the right edge of the obstacle
                if direction == 'vertical':
                    if self.direction.y > 0: # move up
                        self.hitbox_rect.bottom = sprite.rect.top # stop at the top edge of the obstacle
                    if self.direction.y < 0: # move down
                        self.hitbox_rect.top = sprite.rect.bottom # stop at the bottom edge of the obstacle

    def input(self):
        # handle player input and update movement direction
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT])-int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def update(self, delta):
        # update player movement and animation each frame
        self.input()
        self.move(delta)
        self.animate(delta)