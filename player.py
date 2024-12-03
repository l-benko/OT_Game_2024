from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites):
        super().__init__(groups)
        # load graphics
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        self.load_images()
        self.state, self.frame_index = 'down', 0
        self.image = pygame.image.load(join('assets','player',self.state,'0.png')).convert_alpha()
        self.rect = self.image.get_frect(center=position)
        # move player
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def load_images(self):
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('assets','player',state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surface = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surface)

    def animate(self, delta):
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x >0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y >0 else 'up'
        self.frame_index = (self.frame_index +5 * delta) if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, delta):
        self.animate(delta)