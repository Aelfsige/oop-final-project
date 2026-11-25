import pygame


class AudioManager:
    def __init__(self, sfx_paths=None, volume=1.0, buffer=512):
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(buffer=buffer)
            except pygame.error:
                pass

        self.volume = max(0.0, min(1.0, volume))
        self.music_path = None
        self.sfx = {}
        if pygame.mixer.get_init():
            for name, path in (sfx_paths or {}).items():
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.volume)
                self.sfx[name] = sound

    def play_music(self, path):
        if not pygame.mixer.get_init():
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.music_path = path

    def play_sfx(self, name):
        sound = self.sfx.get(name)
        if sound is not None:
            sound.play()

    def stop(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.stop()
