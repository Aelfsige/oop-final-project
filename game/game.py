from collections.abc import Callable

import pygame

from .scenes import MenuScene


class Game:
    def __init__(self, match_factory: Callable | None = None, size=(1280, 720), fps=60):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Rhythm Cream-Pie")
        self.clock = pygame.time.Clock()
        self.current_scene = None
        self.running = True
        self.fps = fps
        self.match_factory = match_factory
        self.change_scene(MenuScene(self))

    def new_match(self):
        if self.match_factory is None:
            raise RuntimeError("Game classes are not wired yet: provide a match_factory.")
        return self.match_factory(self)

    def change_scene(self, scene):
        self.current_scene = scene

    def run(self):
        try:
            while self.running:
                dt = self.clock.tick(self.fps) / 1000
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                    self.current_scene.handle_event(event)

                if self.running:
                    self.current_scene.update(dt)
                    self.current_scene.draw(self.screen)
                    pygame.display.flip()
        finally:
            pygame.quit()
