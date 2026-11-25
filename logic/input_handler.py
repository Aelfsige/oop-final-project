import pygame


class InputHandler:
    def __init__(self, key_map=None):
        self.key_map = key_map if key_map is not None else {
            pygame.K_a: ("left", 0),
            pygame.K_s: ("left", 1),
            pygame.K_d: ("left", 2),
            pygame.K_f: ("left", 3),
            pygame.K_j: ("right", 0),
            pygame.K_k: ("right", 1),
            pygame.K_l: ("right", 2),
            pygame.K_SEMICOLON: ("right", 3),
        }

    def map_key(self, key):
        return self.key_map.get(key)
