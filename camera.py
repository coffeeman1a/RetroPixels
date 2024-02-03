import pygame
from sprites import Generic, GenericAnimation, GenericPhysics, GenericPhysicsAnimaton
from settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self, debug_mode=False):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.debug_mode = debug_mode

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):  # sorted by y-axis
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    if self.debug_mode:

                        if sprite == player:
                            pygame.draw.rect(self.display_surface,'red', offset_rect, 5)
                            hitbox_rect = player.hitbox.copy()
                            hitbox_rect.center = offset_rect.center
                            pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)

                        if isinstance(sprite, Generic):
                            hitbox_rect = sprite.hitbox.copy()
                            hitbox_rect.center = offset_rect.center
                            pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)

                        if isinstance(sprite, GenericAnimation):
                            hitbox_rect = sprite.hitbox.copy()
                            hitbox_rect.center = offset_rect.center
                            pygame.draw.rect(self.display_surface, 'yellow', hitbox_rect, 5)

                        if isinstance(sprite, GenericPhysics):
                            hitbox_rect = sprite.hitbox.copy()
                            hitbox_rect.center = offset_rect.center
                            pygame.draw.rect(self.display_surface, 'purple', hitbox_rect, 5)

                        if isinstance(sprite, GenericPhysicsAnimaton):
                            hitbox_rect = sprite.hitbox.copy()
                            hitbox_rect.center = offset_rect.center
                            pygame.draw.rect(self.display_surface, 'pink', hitbox_rect, 5)