import os
import sys

import pygame

from game.game import Game
from player.player import Player, Hand
from chart.chart import Chart
from chart.conductor import Conductor
from chart.lane import Lane
from logic.judgement import JudgementSystem
from logic.input_handler import InputHandler

DEFAULT_SONG = './assets/Wet Hands'     # a folder or a .osu file
SFX_FOLDER = './assets/sfx'             # optional: hit.wav, miss.wav, splat.wav
HIT_LINE_Y = 600
LANE_SPACING = 80                       # Lane.WIDTH is 70, so 10 px gap
AUDIO_OFFSET = 0.0                      # seconds; raise it if notes feel late, lower it if early

LEFT_KEYS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]
RIGHT_KEYS = [pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON]


def find_osu(path):
    """Accept a .osu file, or a folder containing one."""
    if os.path.isdir(path):
        maps = sorted(f for f in os.listdir(path) if f.lower().endswith('.osu'))
        if not maps:
            raise RuntimeError(f"No .osu file found in {path}")
        return os.path.join(path, maps[0])
    return path


def make_lanes(keys, center_x, notes, judgement):
    """The four Lane objects for one player, centred on center_x."""
    start_x = center_x - (3 * LANE_SPACING + Lane.WIDTH) // 2
    return [
        Lane(key, start_x + i * LANE_SPACING, HIT_LINE_Y, judgement,
             notes=[n for n in notes if n.lane == i])
        for i, key in enumerate(keys)
    ]


def build_match(game):
    try:
        osu_path = find_osu(getattr(game, 'song_path', DEFAULT_SONG))
        chart = Chart()
        chart.load_file(osu_path)       # notes, title, bpm and the music path
        chart.load_sfx(SFX_FOLDER)
    except (OSError, ValueError) as error:
        raise RuntimeError(str(error))  # the menu shows RuntimeError messages

    judgement = JudgementSystem()
    conductor = Conductor(bpm=chart.bpm, offset=AUDIO_OFFSET, audio=chart)

    width = game.screen.get_width()     # players sit at the same x as their face and score
    left = Player('left', LEFT_KEYS,
                  make_lanes(LEFT_KEYS, width // 5, chart.notes_for('left'), judgement))
    right = Player('right', RIGHT_KEYS,
                   make_lanes(RIGHT_KEYS, width * 4 // 5, chart.notes_for('right'), judgement))

    return {
        'players': {'left': left, 'right': right},
        'hand': Hand(),
        'chart': chart,
        'conductor': conductor,
        'judgement': judgement,
        'input_handler': InputHandler(),
        'audio': chart,                 # Chart plays the music and sound effects
        'assets': None,
    }


def main():
    # python main.py [song folder or .osu file]
    song_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SONG
    game = Game(match_factory=build_match)
    game.song_path = song_path
    game.run()


if __name__ == '__main__':
    main()