from os import walk
import json
import pygame
import logging


def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_folder_dict(path):
    surface_dict = {}
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = image_surf

    return surface_dict


class AtlasTexture:
    @staticmethod
    def get_image(texture_path, frame, size, scale=(1, 1), color=(0, 0, 0), x_offset=0, y_offset=0):
        texture = pygame.image.load(texture_path).convert_alpha()
        if not any((size, frame, texture)):
            logging.warning("input error")
            return None
        surface = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
        surface.blit(texture, (0, 0), (
            frame[0] * (size[0] - x_offset), frame[1] * (size[1] - y_offset), size[0], size[1]))
        surface = pygame.transform.scale(surface, (size[0] * scale[0], size[1] * scale[1]))
        surface.set_colorkey(color)
        return surface


class SoundManager:
    def __init__(self, sounds):
        self.sounds = {}
        for name, path in sounds.items():
            self.sounds[name] = [pygame.mixer.Sound(path),
                                 Timer(self.seconds_to_miliseconds(pygame.mixer.Sound(path).get_length()))]

    def play_sound(self, name):
        if not self.sounds[name][1].active:
            self.sounds[name][1].activate()
            self.sounds[name][0].play()

    def set_volume_to_sound(self, name, volume):
        self.sounds[name][0].set_volume(volume)

    @staticmethod
    def seconds_to_miliseconds(seconds):
        return seconds * 1000

    def update(self):
        for item in self.sounds.values():
            item[1].update()


class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()


class FileManager:
    @staticmethod
    def get_json_data(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
