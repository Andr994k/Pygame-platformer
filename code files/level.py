
import pygame
import random
from settings import *
from tile import Cursor, WinBox, Tiles
from player import Player

class Level:
    def __init__(self):

        #Level setup
        self.display_surface = pygame.display.get_surface()

        #Sprite group setup
        self.visible_sprites = CameraGroup()
        self.cursor_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.destructible_tiles = pygame.sprite.Group()
        self.win_tiles = pygame.sprite.Group()

        self.setup_level()

    def setup_level(self):
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        for row_index,row in enumerate(LEVEL_MAP):
            for col_index,col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'G':
                    Tiles((x,y),[self.visible_sprites,self.collision_sprites], "graphics/tile/grassblock.png")
                if col == 'P':
                    self.player = Player((x,y),[self.visible_sprites,self.active_sprites],self.collision_sprites)
                if col == 'D':
                    Tiles((x,y),[self.visible_sprites,self.collision_sprites, self.destructible_tiles], "graphics/tile/dirtblock.png")
                if col == 'S':
                    chance = random.randint(0,15)
                    if chance == 10:
                        Tiles((x,y),[self.visible_sprites,self.collision_sprites], "graphics/tile/stone_vines.png")
                    else:
                        Tiles((x,y),[self.visible_sprites,self.collision_sprites], "graphics/tile/stone.png")
                if col == "W":
                    WinBox((x,y),[self.visible_sprites, self.win_tiles])
        Cursor([self.cursor_sprites], self.display_surface)

    #Checks for collisions between the cursor_sprites sprite group and the destructible_tiles sprite group when left click is pressed
    #If a collision occurs, the object in the destructible_tiles sprite group will be deleted
    def mouse_collision(self):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            for cursor in self.cursor_sprites.sprites():
                if pygame.sprite.spritecollide(cursor, self.destructible_tiles, True):
                    pass

    def win_check(self):
        for player in self.active_sprites.sprites():
            if pygame.sprite.spritecollide(player, self.win_tiles, True):
                font = pygame.font.Font(None, 200)
                wintext = "You have won!" 
                winnertext = font.render(str(wintext), 1, (255,255,255))
                textrect = winnertext.get_rect()
                self.display_surface.blit(winnertext, (self.display_surface.get_width()//2-textrect.w//2, self.display_surface.get_height()//2-textrect.h//2))
                pygame.display.update()
                pygame.time.delay(5000)
                quit()

    def run(self):
        #Runs the entire game (level)
        self.win_check()
        self.visible_sprites.custom_draw(self.player)
        self.cursor_sprites.update()
        self.cursor_sprites.draw(self.display_surface)
        self.active_sprites.update()
        self.mouse_collision()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100, 300)
        
        #Center camera
        self.half_width = self.display_surface.get_width() //2
        self.half_height = self.display_surface.get_height() //2

    def custom_draw(self, player):
        #Player offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)