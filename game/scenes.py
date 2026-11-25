from time import monotonic

import pygame


class Scene:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 32)
        self.message = ""

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN or getattr(event, "repeat", False):
            return
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            try:
                self.game.change_scene(PlayScene(self.game))
            except RuntimeError as error:
                self.message = str(error)

    def draw(self, screen):
        screen.fill((26, 23, 35))
        _center(screen, self.title_font, "Rhythm Cream-Pie", (255, 242, 224), 250)
        _center(screen, self.font, "Press Enter to start", (205, 198, 210), 330)
        if self.message:
            _center(screen, self.font, self.message, (255, 170, 150), 390)


class PlayScene(Scene):
    HIT_PUSH = 0.12
    MISS_PUSH = 0.08

    def __init__(self, game):
        super().__init__(game)
        match = game.new_match()
        self.players = match["players"]
        self.hand = match["hand"]
        self.chart = match["chart"]
        self.conductor = match["conductor"]
        self.judgement = match["judgement"]
        self.input_handler = match["input_handler"]
        self.audio = match["audio"]
        self.assets = match["assets"]
        self.hud = HUD(self.players, self.hand)
        self.conductor.start()

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN or getattr(event, "repeat", False):
            return
        mapped = self.input_handler.map_key(event.key)
        if mapped is None:
            return

        side, lane_index = mapped
        player = self.players[side]
        result = player.press(lane_index, self.conductor.song_time())
        self._resolve(side, result)

    def update(self, dt):
        song_time = self.conductor.song_time()
        for side, player in self.players.items():
            for lane in player.lanes:
                lane.spawn_notes(song_time)
                pending = tuple(note for note in lane.active_notes if note.state == "pending")
                lane.update(song_time)
                for note in pending:
                    if note.state == "missed":
                        self._resolve(side, "miss")

        self.hand.update(dt)
        for side in ("left", "right"):
            if self.hand.reached(side):
                self.players[side].face.set_state("cream_pied")
                self.audio.play_sfx("splat")
                winner = self.players["right" if side == "left" else "left"]
                self.game.change_scene(GameOverScene(self.game, winner))
                return

    def draw(self, screen):
        screen.fill((26, 23, 35))
        for player in self.players.values():
            for lane in player.lanes:
                lane.draw(screen)
            player.face.draw(screen)

        self.hud.draw(screen)

    def _resolve(self, side, result):
        self.hud.show_judgement(result, side)
        if result == "miss":
            self.players[side].reset_combo()
            self.hand.push(side, self.MISS_PUSH)
            self.audio.play_sfx("miss")
            return

        self.players[side].add_combo()
        self.players[side].face.set_state("hit")
        opponent = "right" if side == "left" else "left"
        self.hand.pass_to(side)
        self.hand.push(opponent, self.HIT_PUSH)
        self.audio.play_sfx("hit")


class GameOverScene(Scene):
    def __init__(self, game, winner):
        super().__init__(game)
        self.winner = winner
        self.title_font = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 32)
        self.message = ""

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN or getattr(event, "repeat", False):
            return
        if event.key in (pygame.K_RETURN, pygame.K_r):
            try:
                self.game.change_scene(PlayScene(self.game))
            except RuntimeError as error:
                self.message = str(error)
        elif event.key in (pygame.K_ESCAPE, pygame.K_m):
            self.game.change_scene(MenuScene(self.game))

    def draw(self, screen):
        screen.fill((26, 23, 35))
        side = getattr(self.winner, "side", self.winner)
        _center(screen, self.title_font, f"{side.title()} wins!", (255, 242, 224), 250)
        _center(screen, self.font, "Enter/R: restart    Esc/M: menu", (205, 198, 210), 330)
        if self.message:
            _center(screen, self.font, self.message, (255, 170, 150), 390)


class HUD:
    def __init__(self, players, hand):
        self.players = players
        self.hand = hand
        self.font = pygame.font.Font(None, 30)
        self.popup_font = pygame.font.Font(None, 42)
        self.popup = None

    def show_judgement(self, text, side):
        self.popup = (text.title(), side, monotonic())

    def draw(self, screen):
        width, height = screen.get_size()
        left, right = width // 5, width * 4 // 5

        for side, x in (("left", left), ("right", right)):
            player = self.players[side]
            label = self.font.render(
                f"{side.title()}  {player.score:,}  x{player.combo}",
                True,
                (255, 242, 224),
            )
            screen.blit(label, label.get_rect(center=(x, 36)))

        y = height - 48
        x = round(left + (right - left) * (self.hand.position + 1) / 2)
        pygame.draw.line(screen, (125, 105, 120), (left, y), (right, y), 4)
        pygame.draw.circle(screen, (255, 238, 216), (x, y), max(10, height // 45))

        if self.popup:
            text, side, started = self.popup
            elapsed = monotonic() - started
            if elapsed < 0.7:
                surface = self.popup_font.render(text, True, (255, 242, 224))
                surface.set_alpha(round(255 * (1 - elapsed / 0.7)))
                x = left if side == "left" else right
                screen.blit(surface, surface.get_rect(center=(x, height // 2 - 100)))
            else:
                self.popup = None


def _center(screen, font, text, color, y):
    surface = font.render(text, True, color)
    screen.blit(surface, surface.get_rect(center=(screen.get_width() // 2, y)))
