import pygame
import copy
import random
from support import AtlasTexture
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, id, pos, surf, groups, z=LAYERS['main'], scale=(1, 1), name='Generic', hitbox=True,
                 image_scale=None):
        super().__init__(groups)
        self.id = id
        self.name = name

        if image_scale:
            image = pygame.transform.scale(surf,
                                           (surf.get_width() * image_scale[0], surf.get_height() * image_scale[1]))
        else:
            image = pygame.transform.scale(surf, (surf.get_width() * scale[0], surf.get_height() * scale[1]))

        self.image = image
        self.size = (self.image.get_height(), self.image.get_width())
        scaled_pos = (pos[0] * scale[0], pos[1] * scale[1])
        self.rect = self.image.get_rect(topleft=scaled_pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(OBJECTS_SIZE[self.name][1])


class GenericPhysics(pygame.sprite.Sprite):
    def __init__(self, id, pos, surf, groups, z=LAYERS['main'], scale=(1, 1), name='Generic', hitbox=True, image_scale=None):
        super().__init__([groups[0], groups[2]])
        self.id = id
        self.name = name

        # sprite groups
        self.collision_sprites = groups[1]
        self.physics_sprites = groups[2]

        if image_scale:
            image = pygame.transform.scale(surf,
                                           (surf.get_width() * image_scale[0], surf.get_height() * image_scale[1]))
        else:
            image = pygame.transform.scale(surf, (surf.get_width() * scale[0], surf.get_height() * scale[1]))

        self.image = image
        self.size = OBJECTS_SIZE[self.name][0] if self.name in OBJECTS_SIZE else (self.image.get_height(), self.image.get_width())
        scaled_pos = (pos[0] * scale[0], pos[1] * scale[1])
        self.rect = self.image.get_rect(topleft=scaled_pos)
        self.pos = pygame.math.Vector2(scaled_pos[0], scaled_pos[1])

        self.z = z
        self.hitbox = self.rect.copy().inflate(
            OBJECTS_SIZE[self.name][1]) if self.name in OBJECTS_SIZE else self.rect.copy()
        self.hitbox_offset = pygame.math.Vector2(self.rect.centerx - scaled_pos[0], self.rect.centery - scaled_pos[1])

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.weight = 100

    def move(self, player_direction, dt):
        # normalizing a vector
        if player_direction.magnitude() > 0:
            self.direction = player_direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.weight * dt
        self.hitbox.centerx = round(self.pos.x + self.hitbox_offset.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.weight * dt
        self.hitbox.centery = round(self.pos.y + self.hitbox_offset.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    self.collision_handler(sprite, direction)

        for sprite in self.physics_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox) and sprite.id != self.id:

                    if 'table' in sprite.name and self.name in CAN_BE_PLACED_ON \
                            or 'table' in self.name and sprite.name in CAN_BE_PLACED_ON:
                        return

                    self.collision_handler(sprite, direction)

    def collision_handler(self, sprite, direction):
        if direction == 'horizontal':

            if self.direction.x > 0:  # moving right
                self.hitbox.right = sprite.hitbox.left
            if self.direction.x < 0:  # moving left
                self.hitbox.left = sprite.hitbox.right

            self.rect.centerx = self.hitbox.centerx
            self.pos.x = self.hitbox.centerx - self.hitbox_offset.x

        if direction == 'vertical':

            if self.direction.y > 0:  # moving down
                self.hitbox.bottom = sprite.hitbox.top
            if self.direction.y < 0:  # moving up
                self.hitbox.top = sprite.hitbox.bottom

            self.rect.centery = self.hitbox.centery
            self.pos.y = self.hitbox.centery - self.hitbox_offset.y


class GenericAnimation(pygame.sprite.Sprite):
    def __init__(self, id, pos, surf, groups, z=LAYERS['main'], scale=(1, 1), name='GenericAnimation', hitbox=True, image_scale=None):
        super().__init__(groups)
        self.id = id
        self.name = name
        self.scale = scale
        self.z = z
        self.size = OBJECTS_SIZE[self.name][0]
        self.state = 'idle'
        self.animation_frames = None
        self.animations = None
        self.animation_speed = 6
        self.animation_frame = 0

        self.import_assets()

        self.image = self.animations[self.state][self.animation_frame]
        scaled_pos = (pos[0] * scale[0], pos[1] * scale[1])
        self.pos = pygame.math.Vector2(scaled_pos[0], scaled_pos[1])
        self.rect = self.image.get_rect(topleft=scaled_pos)
        self.hitbox = self.rect.copy().inflate(OBJECTS_SIZE[self.name][1])
        if self.name in HITBOX_OFFSETS:
            self.hitbox.move_ip(HITBOX_OFFSETS[name])

    def import_assets(self):

        self.animation_frames = copy.deepcopy(ANIMATION_FRAMES[self.name])
        self.animations = copy.deepcopy(DEFAULT_ANIMATIONS[self.name])

        for state, animation_frames_list in self.animation_frames.items():
            for frame in animation_frames_list:
                image = AtlasTexture.get_image(texture_path=TEXTURE_PATH[self.name],
                                               frame=frame,
                                               size=self.size,
                                               scale=self.scale)
                self.animations[state].append(image)

    def animate(self, dt):
        self.animation_frame += self.animation_speed * dt
        if self.animation_frame >= len(self.animations[self.state]):
            self.animation_frame = 0

        self.image = self.animations[self.state][int(self.animation_frame)]

    def update(self, dt):
        self.animate(dt)


class GenericPhysicsAnimaton(pygame.sprite.Sprite):
    def __init__(self, id, pos, surf, groups, z=LAYERS['main'], scale=(1, 1), name='Generic', hitbox=True, image_scale=None):
        super().__init__([groups[0], groups[2]])
        self.id = id
        self.name = name

        # sprite groups
        self.collision_sprites = groups[1]
        self.physics_sprites = groups[2]

        self.scale = scale
        self.z = z
        self.size = OBJECTS_SIZE[self.name][0]
        self.state = 'idle'
        self.animation_frames = None
        self.animations = None
        self.animation_speed = 6
        self.animation_frame = 0

        self.import_assets()

        self.image = self.animations[self.state][self.animation_frame]
        scaled_pos = (pos[0] * scale[0], pos[1] * scale[1])
        self.pos = pygame.math.Vector2(scaled_pos[0], scaled_pos[1])
        self.rect = self.image.get_rect(topleft=scaled_pos)
        self.hitbox = self.rect.copy().inflate(OBJECTS_SIZE[self.name][1])
        if self.name in HITBOX_OFFSETS:
            self.hitbox.move_ip(HITBOX_OFFSETS[name])

        self.hitbox_offset = pygame.math.Vector2(self.rect.centerx - scaled_pos[0], self.rect.centery - scaled_pos[1])

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.weight = 100

    def import_assets(self):
        self.animation_frames = copy.deepcopy(ANIMATION_FRAMES[self.name])
        self.animations = copy.deepcopy(DEFAULT_ANIMATIONS[self.name])

        for state, animation_frames_list in self.animation_frames.items():
            for frame in animation_frames_list:
                image = AtlasTexture.get_image(texture_path=TEXTURE_PATH[self.name],
                                               frame=frame,
                                               size=self.size,
                                               scale=self.scale)
                self.animations[state].append(image)

    def move(self, player_direction, dt):
        # normalizing a vector
        if player_direction.magnitude() > 0:
            self.direction = player_direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.weight * dt
        self.hitbox.centerx = round(self.pos.x + self.hitbox_offset.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.weight * dt
        self.hitbox.centery = round(self.pos.y + self.hitbox_offset.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    self.collision_handler(sprite, direction)

        for sprite in self.physics_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox) and sprite.id != self.id:

                    if 'table' in sprite.name and self.name in CAN_BE_PLACED_ON \
                            or 'table' in self.name and sprite.name in CAN_BE_PLACED_ON:
                        return

                    self.collision_handler(sprite, direction)

    def collision_handler(self, sprite, direction):
        if direction == 'horizontal':

            if self.direction.x > 0:  # moving right
                self.hitbox.right = sprite.hitbox.left
            if self.direction.x < 0:  # moving left
                self.hitbox.left = sprite.hitbox.right

            self.rect.centerx = self.hitbox.centerx
            self.pos.x = self.hitbox.centerx - self.hitbox_offset.x

        if direction == 'vertical':

            if self.direction.y > 0:  # moving down
                self.hitbox.bottom = sprite.hitbox.top
            if self.direction.y < 0:  # moving up
                self.hitbox.top = sprite.hitbox.bottom

            self.rect.centery = self.hitbox.centery
            self.pos.y = self.hitbox.centery - self.hitbox_offset.y


class Chest(GenericPhysicsAnimaton):
    def __init__(self, id, pos, surf, groups, z=LAYERS['main'], scale=(1, 1), name='Generic', hitbox=True, image_scale=None):
        super().__init__(id, pos, surf, groups, z, scale, name, hitbox, image_scale)

        self.animation_speed = 25

        self.loot = []
        self.items_pool = ['key', 'ration', 'spider']

        self.generate_loot()

    def animate(self, dt):
        self.animation_frame += self.animation_speed * dt
        if self.animation_frame >= len(self.animations[self.state]):
            return

        self.image = self.animations[self.state][int(self.animation_frame)]

    def generate_loot(self):
        random_item = random.choice(self.items_pool)
        self.loot.append(random_item)

    def open(self):
        if self.state != 'idle':
            return

        self.state = 'opened'
        for item in self.loot:
            print(f'You found {item}')
        self.loot = []

    def update(self, dt):
        if self.state == 'opened':
            self.animate(dt)


class Door(Generic):
    def __init__(self, id, pos, surf, groups, z=LAYERS['main'], scale=(1, 1), name='Generic', hitbox=True):
        super().__init__(pos, surf, groups, z, scale, name, hitbox)
        self.id = id
        self.door_check = self.rect.copy()
