import pygame

class Tiles(pygame.sprite.Sprite):
    def __init__(self,pos,groups,image):
        super().__init__(groups)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft = pos)

class Cursor(pygame.sprite.Sprite):
    def __init__(self, groups, display_surface):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/cursor/cursor.png")
        self.display_surface = display_surface
        pos = pygame.mouse.get_pos()
        self.rect = self.image.get_rect(topleft = pos)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect = self.image.get_rect(topleft = pos)

class WinBox(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/tile/diamond.png")
        self.rect = self.image.get_rect(topleft = pos)