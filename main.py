from game.game import Game
from game.scenes import *
from player.player import Player, Hand
from chart.chart import Chart
from chart.conductor import Conductor
from chart.lane import Lane
from logic.judgement import JudgementSystem
from logic.input_handler import InputHandler
import pygame

def build_match(game):
    chart = Chart()
    judgement = JudgementSystem()
    chart.load_file('./assets/Wet Hands/C418 - Wet Hands (Slyme) [Nostalgia].osu') # create metadata
    chart.load_audio('./assets/Wet Hands/audio.mp3')
    conductor = Conductor(chart)

    notes = chart.notes

    x0 = 160
    x1 = 320
    left_lane0 = Lane(pygame.K_a, x0 + 0 * 90, 600, judgement, notes=[n for n in notes if n.owner == 'left'])
    left_lane1 = Lane(pygame.K_s, x0 + 1 * 90, 600, judgement, notes=[n for n in notes if n.owner == 'left'])
    left_lane2 = Lane(pygame.K_d, x0 + 2 * 90, 600, judgement, notes=[n for n in notes if n.owner == 'left'])
    left_lane3 = Lane(pygame.K_f, x0 + 3 * 90, 600, judgement, notes=[n for n in notes if n.owner == 'left'])

    right_lane0 = Lane(pygame.K_j, x1 + 4 * 90, 600, judgement, notes=[n for n in notes if n.owner == 'right'])
    right_lane1 = Lane(pygame.K_k, x1 + 5 * 90, 600, judgement, notes=[n for n in notes if n.owner == 'right'])
    right_lane2 = Lane(pygame.K_l, x1 + 6 * 90, 600, judgement, notes=[n for n in notes if n.owner == 'right'])
    right_lane3 = Lane(pygame.K_SEMICOLON, x1 + 7 * 90, 600, judgement, notes=[n for n in notes if n.owner == 'right'])

    left = Player(
        'left', 
        [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f], 
        [left_lane0, left_lane1, left_lane2, left_lane3]
    )
    right = Player(
        'right',
        [pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON],
        [right_lane0, right_lane1, right_lane2, right_lane3]
    )
    
    return {
        'players': {'left': left, 'right': right},
        'hand': Hand(),
        'chart': chart,
        'conductor': conductor,
        'judgement': judgement,
        'input_handler': InputHandler(),
        'audio': chart,
        'assets': None
    }

def main():
    Game(match_factory=build_match).run()


if __name__ == '__main__':
    main()