import pygame
import copy
from settings import *
from support import AtlasTexture, SoundManager, Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, physics_sprites):
        super().__init__(group)
        self.name = 'player'
        self.scale = (7, 7)
        self.size = (16, 16)
        self.animation_frames = None
        self.player_animations = None
        self.accessories_animations = None
        self.accessories = None
        self.sounds = None
        self.sound_manager = None
        self.import_assets()
        self.animation_frame = 0
        self.state = 'down_idle'
        self.animation_speed = 7

        # general setup
        self.image = self.player_animations[self.state][self.animation_frame]
        scaled_pos = (pos[0] * 6, pos[1] * 6)
        self.rect = self.image.get_rect(midbottom=scaled_pos)
        self.rect = self.rect.move(0, 100)
        self.z = LAYERS['main']

        # movement attributes
        self.speed = 200
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()

        # logic attributes
        self.sleep = False
        self.can_sound = True

        # collision
        self.hitbox = self.rect.copy().inflate(-60, -40)
        self.collision_sprites = collision_sprites
        self.physics_sprites = physics_sprites
        # self.pickups_sprites = pickups_sprites

        # # accessories
        # self.active_accessories = {
        #     'hair': None,
        #     'body': None,
        #     'legs': None,
        #     'boots': None
        # }

    def import_assets(self):
        # self.atlas_texture = AtlasTexture(TEXTURE_PATH['player'])

        default_animation_dict = {'up': [], 'down': [], 'right': [], 'left': [],
                                  'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': []}

        self.animation_frames = {'down_idle': [(0, 0)],
                                 'up_idle': [(0, 1)],
                                 'left_idle': [(0, 2)],
                                 'right_idle': [(0, 3)],
                                 'down': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)],
                                 'up': [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)],
                                 'left': [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2)],
                                 'right': [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3)]}

        self.player_animations = copy.deepcopy(default_animation_dict)
        for direction, animation_frames_list in self.animation_frames.items():
            for frame in animation_frames_list:
                image = AtlasTexture.get_image(texture_path=TEXTURE_PATH['player'],
                                               frame=frame,
                                               size=self.size,
                                               scale=self.scale)
                self.player_animations[direction].append(image)

        # accessories
        # self.accessories = {
        #     'hair_1': TEXTURE_PATH['hair_1'],
        #     'body_1': TEXTURE_PATH['body_1'],
        #     'legs_1': TEXTURE_PATH['legs_1'],
        #     'boots_1': TEXTURE_PATH['boots_1']
        # }
        # self.accessories_animations = {}
        #
        # for name, texture_path in self.accessories.items():
        #     animations = copy.deepcopy(default_animation_dict)
        #     for direction, animation_frames_list in self.animation_frames.items():
        #         for frame in animation_frames_list:
        #             image = AtlasTexture.get_image(texture_path=texture_path,
        #                                            frame=frame,
        #                                            size=self.size,
        #                                            scale=self.scale)
        #             animations[direction].append(image)
        #             self.accessories_animations[name] = animations

        # sounds
        self.sounds = {
            'step': SOUND_PATH['player_step']
        }
        self.sound_manager = SoundManager(self.sounds)

    # def set_accessory(self, name):
    #     self.active_accessories[name.split('_')[0]] = self.accessories_animations[name]

    def animate(self, dt):
        self.animation_frame += self.animation_speed * dt
        if self.animation_frame >= len(self.player_animations[self.state]):
            self.animation_frame = 0

        if self.direction.x > 0 and self.direction.y == 0:
            self.state = "right"
        elif self.direction.x < 0 and self.direction.y == 0:
            self.state = "left"

        if self.direction.y < 0:
            self.state = "up"
        elif self.direction.y > 0:
            self.state = "down"

        self.image = self.player_animations[self.state][int(self.animation_frame)]

        # # accessories
        # for name, animation in self.active_accessories.items():
        #     if animation:
        #         self.image.blit(animation[self.state][int(self.animation_frame)], (0, 0))

        # sounds
        if abs(self.direction.x) or abs(self.direction.y) and self.can_sound:
            self.sound_manager.play_sound('step')

    def get_state(self):
        # idle
        if self.direction.magnitude() == 0:
            self.state = self.state.split('_')[0] + '_idle'

    def input(self):
        if self.sleep:
            return

        # direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # if keys[pygame.K_TAB]:
        #     self.toggle_inventory()

    def move(self, dt):
        # normilizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal', dt)

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical', dt)

    def collision(self, direction, dt):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    self.collision_handler(sprite, direction)

        for sprite in self.physics_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    self.collision_handler(sprite, direction)
                    sprite.move(self.direction, dt)

                    if 'chest' in sprite.name:
                        sprite.open()

    def collision_handler(self, sprite, direction):
        if direction == 'horizontal':

            if self.direction.x > 0:  # moving right
                self.hitbox.right = sprite.hitbox.left
            if self.direction.x < 0:  # moving left
                self.hitbox.left = sprite.hitbox.right

            self.rect.centerx = self.hitbox.centerx
            self.pos.x = self.hitbox.centerx

        if direction == 'vertical':

            if self.direction.y > 0:  # moving down
                self.hitbox.bottom = sprite.hitbox.top
            if self.direction.y < 0:  # moving up
                self.hitbox.top = sprite.hitbox.bottom

            self.rect.centery = self.hitbox.centery
            self.pos.y = self.hitbox.centery

    def update(self, dt):
        self.input()
        self.get_state()
        # self.update_timers()
        # self.get_target_pos()
        self.move(dt)
        self.animate(dt)
        self.sound_manager.update()
