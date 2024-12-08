from settings import *


class Button:
    def __init__(self, x, y, width, height, foreground_color, background_color, content, fontsize):
        self.font = pygame.font.Font(join('assets','fonts','Cooper Black Regular.ttf'), fontsize) # load font
        self.image = pygame.Surface((width, height))
        self.image.fill(background_color) # fill the button surface with the background color
        self.rect = self.image.get_frect(topleft=(x, y))
        self.text = self.font.render(content, True, foreground_color) # render the text with the specified foreground color
        self.text_rect = self.text.get_frect(center=(width/2, height/2)) # position the text in the center of the button
        self.image.blit(self.text, self.text_rect) # draw the text onto the button surface

    def is_pressed(self, position, pressed):
        # check if the button is pressed based on the mouse position and the state of the mouse buttons
        if self.rect.collidepoint(position): # check if the mouse is within the bounds of the button
            if pressed[0]: # if the left mouse button is pressed
                return True # button is pressed
            return False # button is not pressed
        return False # mouse is not over the button, so it's not pressed
