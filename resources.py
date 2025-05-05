import pygame
import os

ASSETS_DIR = 'assets'


def load_image(name):
    path = os.path.join(ASSETS_DIR, name)
    return pygame.image.load(path).convert_alpha()


def load_images(prefix, count):
    return [load_image(f"{prefix}{i}.png") for i in range(count)]


def load_runner_animations():
    return {
        'run': load_images('runner_run_', 6),
        'jump': load_images('runner_jump_', 1),
    }


def load_garbage_images():
    return [
        load_image('garbage1.png'),
        load_image('garbage2.png'),
        load_image('garbage3.png')
    ]