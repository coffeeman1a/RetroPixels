import pygame
from settings import *
from player import Player
from pytmx.util_pygame import load_pygame
from support import *
from camera import CameraGroup
from sprites import Generic, GenericAnimation, GenericPhysics, Door, Chest


class Level:
    def __init__(self):
        self.clock = None
        self.inventory = None
        self.player = None
        self.display_surface = pygame.display.get_surface()
        # sprite groups
        debug_mode = False
        self.all_sprites = CameraGroup(debug_mode)
        self.collision_sprites = pygame.sprite.Group()
        self.physics_sprites = pygame.sprite.Group()

        # objects
        self.objects = []

        self.CLASS_MAP = {
            'Generic': Generic,
            'GenericAnimation': GenericAnimation,
            'GenericPhysics': GenericPhysics,
            'Chest': Chest,
            'Door': Door
        }

        self.GROUP_MAP = {
            'all_sprites': self.all_sprites,
            'collision_sprites': self.collision_sprites,
            'physics_sprites': self.physics_sprites
        }

        # delay
        self.window_delay = 200

        # logic
        self.last_inv_toggle_time = 0
        self.inv_active = False

        # music
        self.music = {
            'first_level': MUSIC_PATH['first_level']
        }
        self.sound_manager = SoundManager(self.music)

        self.setup()

    def setup(self):
        # self.player = Player(
        #     pos=(1000, 500),
        #     toggle_inventory=self.toggle_inventory,
        #     group=self.all_sprites,
        #     collision_sprites=self.collision_sprites
        # )

        # player
        # for obj in tmx_data.get_layer_by_name('Player'):
        #     if obj.name == 'Start':
        #         self.player = Player(
        #             pos = (obj.x, obj.y),
        #             group = self.all_sprites)
        self.load_level_data('level_data.json')

    def load_level_data(self, data_path):
        tmx_data = load_pygame('tiled/level1_1.tmx')
        level_data = FileManager.get_json_data(data_path)

        tile_id = 0

        for layer_info in level_data['layers']:
            tmx_layer_name = layer_info['name']
            groups = []

            for group in layer_info['groups']:
                groups.append(self.GROUP_MAP[group])

            display_layer = layer_info['display_layer']
            title_class = self.CLASS_MAP[layer_info['class']]
            Level.populate_world_tiles(tile_id, tmx_data, tmx_layer_name, title_class, groups, LAYERS[display_layer])

            tile_id += 1

        for obj_info in level_data["objects"]:
            tmx_layer_name = obj_info['name']

            if tmx_layer_name == 'player':
                self.spawn_player(tmx_data, tmx_layer_name)
                continue

            sprite_groups = []

            for group in obj_info['groups']:
                sprite_groups.append(self.GROUP_MAP[group])

            display_layer = obj_info['display_layer']
            obj_class = self.CLASS_MAP[obj_info['class']]

            self.objects.extend(Level.populate_world_objects(tile_id, tmx_data, tmx_layer_name, obj_class, sprite_groups, LAYERS[display_layer]))

            tile_id += 1

    def spawn_player(self, tmx_data, tmx_layer_name):
        for obj in tmx_data.get_layer_by_name(tmx_layer_name):
            if obj.name == 'start':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.physics_sprites)

        self.sound_manager.play_sound('first_level')
        self.sound_manager.set_volume_to_sound('first_level', 0.2)

    @staticmethod
    def populate_world_tiles(tile_id, tmx_data, tmx_layer, tile_class, groups, z, scale=(6, 6)):
        layer = tmx_data.get_layer_by_name(tmx_layer)

        for x, y, surf in layer.tiles():
            tile_class(tile_id, (x * TILE_SIZE, y * TILE_SIZE), surf, groups, z, scale, name=tmx_layer)

    @staticmethod
    def populate_world_objects(obj_id, tmx_data, tmx_layer, obj_class, groups, z, scale=(6, 6)):
        layer = tmx_data.get_layer_by_name(tmx_layer)
        objects_list = []

        for obj in layer:
            image_scale = None

            if obj.name in OBJECTS_SCALE.keys():
                image_scale = OBJECTS_SCALE[obj.name]

            objects_list.append(obj_class(obj_id, (obj.x, obj.y), obj.image, groups, z, scale, name=obj.name, image_scale=image_scale))

            obj_id += 1

        return objects_list

    def toggle_inventory(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_inv_toggle_time > self.window_delay:
            self.inv_active = not self.inv_active
            self.last_inv_toggle_time = current_time

    def run(self, dt):
        # drawing logic
        self.display_surface.fill('Black')
        self.all_sprites.custom_draw(self.player)
        self.player.update(dt)
        self.sound_manager.update()

        for obj in self.objects:
            obj.update(dt)