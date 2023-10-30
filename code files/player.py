import pygame
from Animations import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)
        self.import_player_assets()
        #Animation
        self.frame_index = 0
        self.animation_speed = 0.015
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        #Player attributes
        
        #Movement
        self.direction = pygame.math.Vector2()
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = 16
        self.dash_speed = 5
        self.is_dashing = False
        self.is_wall_jumping = False
        self.wall_jump_horizontal_speed = 2
        self.on_floor = False
        self.dash_index = 0

        #Status
        self.status = "idle"
        self.collision_sprites = collision_sprites
        self.facing_right = True
        #Space and shift key state management used for disallowing the player to hold down the button
        self.previous_space_key_state = False
        self.previous_shift_key_state = False
        #Left and right wall touch checks, which are by default false.
        self.left_wall_touch = False
        self.right_wall_touch = False

        self.time = 0

    def import_player_assets(self):
        #Gets the folder with 4 subfolders of the different animations
        player_path = 'animations/character/'
        self.animations = {"idle":[],"run":[],"jump":[],"fall":[]}
        #Attaches one of the subfolders to the player path, and stores it in "full_path"
        #Which now looks something like this: "../animations/character/idle" for example
        for animation in self.animations.keys():
            full_path  = player_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations["idle"]

        #Loop over frame index number
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

    def player_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1:
            self.status = "fall"
        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                self.status = "idle"

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not self.is_dashing or keys[pygame.K_d] and not self.is_dashing:
            self.direction.x = 1
            self.facing_right = True

                
        elif keys[pygame.K_LEFT] and not self.is_dashing or keys[pygame.K_a] and not self.is_dashing:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        #Jumping
        if keys[pygame.K_SPACE] and self.on_floor or keys[pygame.K_w] and self.on_floor or keys[pygame.K_UP] and self.on_floor :
            self.direction.y = -self.jump_speed

        #Dash mechanic with a timer 
        self.current_shift_key_state = keys[pygame.K_LSHIFT]
        if self.current_shift_key_state and not self.previous_shift_key_state:
            if pygame.time.get_ticks() > self.time + 500:
                self.time = pygame.time.get_ticks()
                self.is_dashing = True
        self.previous_shift_key_state = self.current_shift_key_state

        #Wall jump mechanics
        self.current_space_key_state = keys[pygame.K_SPACE]
        if self.current_space_key_state and not self.previous_space_key_state and self.left_wall_touch and not self.on_floor:
            self.is_wall_jumping = True
            self.direction.y = -self.jump_speed-3
        if self.current_space_key_state and not self.previous_space_key_state and self.right_wall_touch and not self.on_floor:
            self.is_wall_jumping = True
            self.direction.y = -self.jump_speed-3
        self.previous_space_key_state = self.current_space_key_state

           
    def horizontal_collisions(self):
        self.right_wall_touch = False
        self.left_wall_touch = False
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                    self.left_wall_touch = True
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                    self.right_wall_touch = True
    
    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_floor = True
                if  self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
        if self.on_floor and self.direction.y != 0:
            self.on_floor = False

    #Applies gravity when the player is not currently dashing
    def apply_gravity(self):
        if self.is_dashing == False:
            self.direction.y += self.gravity
            self.rect.y += self.direction.y

    #Moves the player with haste in the direction they are facing when dashing'
    def dash(self):
        if self.is_dashing and self.facing_right:
            self.direction.x = self.dash_speed
            self.dash_index += 1
            if self.dash_index >= 7:
                self.dash_index = 0
                self.is_dashing = False
        if self.is_dashing and not self.facing_right:
            self.direction.x = -self.dash_speed
            self.dash_index += 1    
            if self.dash_index >= 7:
                self.dash_index = 0
                self.is_dashing = False

    #Moves the player up, and slightly away from the wall they were jumping from.
    def wall_jump(self):
        if self.is_wall_jumping and self.facing_right:
            self.direction.x = -self.wall_jump_horizontal_speed
            self.wall_jump_horizontal_speed += 2
            if self.wall_jump_horizontal_speed >= 8:
                self.wall_jump_horizontal_speed = 2
                self.is_wall_jumping = False
        if self.is_wall_jumping and not self.facing_right:
            self.direction.x = self.wall_jump_horizontal_speed
            self.wall_jump_horizontal_speed += 2
            if self.wall_jump_horizontal_speed >= 8:
                self.wall_jump_horizontal_speed = 2
                self.is_wall_jumping = False

    def update(self):
        self.input()
        self.player_status()
        self.animate()
        self.dash()
        self.wall_jump()
        self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()
        self.apply_gravity()
        self.vertical_collisions()