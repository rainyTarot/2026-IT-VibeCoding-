from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from pathlib import Path

import pygame


WIDTH = 1280
HEIGHT = 720
FPS = 60
GAME_DURATION = 30.0

def resolve_asset_dir() -> Path:
    if getattr(sys, "frozen", False):
        runtime_dir = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
        candidates = [
            runtime_dir / "assets",
            Path(sys.executable).resolve().parent / "assets",
            Path(sys.executable).resolve().parent / "_internal" / "assets",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return candidates[0]

    return Path(__file__).parent / "assets"


ASSET_DIR = resolve_asset_dir()

BG_PATH = ASSET_DIR / "bg_spaceship_farm.png"
HOLE_PATH = ASSET_DIR / "hole_neon.png"
MOLE_IDLE_PATH = ASSET_DIR / "mole_idle.png"
MOLE_HIT_PATH = ASSET_DIR / "mole_hit.png"
PANEL_PATH = ASSET_DIR / "ui_panel.png"
BUTTON_PATH = ASSET_DIR / "button_frame.png"
CROSSHAIR_PATH = ASSET_DIR / "crosshair_laser.png"
SFX_START_PATH = ASSET_DIR / "sfx_start.wav"
SFX_HIT_PATH = ASSET_DIR / "sfx_hit.wav"
SFX_MISS_PATH = ASSET_DIR / "sfx_miss.wav"
SFX_GAME_OVER_PATH = ASSET_DIR / "sfx_game_over.wav"

HOLE_POSITIONS = [
    (145, 300), (530, 300), (915, 300),
    (145, 415), (530, 415), (915, 415),
    (145, 530), (530, 530), (915, 530),
]


@dataclass
class Hole:
    rect: pygame.Rect
    mole_rect: pygame.Rect
    active: bool = False
    hit: bool = False
    pop_timer: float = 0.0
    cooldown: float = 0.0


class SpaceFarmWhack:
    def __init__(self) -> None:
        self.audio_enabled = self.init_audio()
        pygame.init()
        pygame.display.set_caption("Space Farm Mole Patrol")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.background = self.load_image(BG_PATH, (WIDTH, HEIGHT))
        self.hole_image = self.load_image(HOLE_PATH)
        self.mole_idle = self.load_image(MOLE_IDLE_PATH)
        self.mole_hit = self.load_image(MOLE_HIT_PATH)
        self.panel_image = self.load_image(PANEL_PATH, (390, 112))
        self.button_image = self.load_image(BUTTON_PATH, (260, 82))
        self.crosshair = self.load_image(CROSSHAIR_PATH, (92, 92))
        self.sounds = self.load_sounds()

        self.title_font = pygame.font.SysFont("consolas", 46, bold=True)
        self.label_font = pygame.font.SysFont("consolas", 24, bold=True)
        self.value_font = pygame.font.SysFont("consolas", 32, bold=True)
        self.info_font = pygame.font.SysFont("consolas", 18)

        self.holes = self.build_holes()
        self.button_rect = pygame.Rect(0, 0, 260, 82)
        self.button_rect.center = (WIDTH // 2, HEIGHT - 92)

        self.state = "start"
        self.score = 0
        self.combo = 0
        self.best_score = 0
        self.time_left = GAME_DURATION
        self.spawn_delay = 0.8
        self.spawn_timer = 0.25
        self.popup_duration = 0.9
        self.difficulty_level = 1.0
        self.hit_flash_timer = 0.0
        self.last_hit_index = -1
        self.mouse_pos = (WIDTH // 2, HEIGHT // 2)

        pygame.mouse.set_visible(False)

    def init_audio(self) -> bool:
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
        except pygame.error:
            return False
        return True

    def load_image(self, path: Path, size: tuple[int, int] | None = None) -> pygame.Surface:
        image = pygame.image.load(path.as_posix()).convert_alpha()
        if size is not None:
            image = pygame.transform.smoothscale(image, size)
        return image

    def load_sounds(self) -> dict[str, pygame.mixer.Sound]:
        if not self.audio_enabled:
            return {}

        sounds = {
            "start": pygame.mixer.Sound(SFX_START_PATH.as_posix()),
            "hit": pygame.mixer.Sound(SFX_HIT_PATH.as_posix()),
            "miss": pygame.mixer.Sound(SFX_MISS_PATH.as_posix()),
            "game_over": pygame.mixer.Sound(SFX_GAME_OVER_PATH.as_posix()),
        }
        sounds["start"].set_volume(0.35)
        sounds["hit"].set_volume(0.40)
        sounds["miss"].set_volume(0.28)
        sounds["game_over"].set_volume(0.40)
        return sounds

    def play_sound(self, name: str) -> None:
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def build_holes(self) -> list[Hole]:
        holes: list[Hole] = []
        hole_width, hole_height = self.hole_image.get_size()
        mole_width = 168
        mole_height = 183

        for x, y in HOLE_POSITIONS:
            hole_rect = pygame.Rect(x, y, hole_width, hole_height)
            mole_x = hole_rect.centerx - mole_width // 2
            mole_y = hole_rect.top - 82
            mole_rect = pygame.Rect(mole_x, mole_y, mole_width, mole_height)
            holes.append(Hole(rect=hole_rect, mole_rect=mole_rect))
        return holes

    def reset_game(self) -> None:
        self.state = "playing"
        self.score = 0
        self.combo = 0
        self.time_left = GAME_DURATION
        self.spawn_delay = 0.8
        self.spawn_timer = 0.2
        self.popup_duration = 0.9
        self.difficulty_level = 1.0
        self.hit_flash_timer = 0.0
        self.last_hit_index = -1
        for hole in self.holes:
            hole.active = False
            hole.hit = False
            hole.pop_timer = 0.0
            hole.cooldown = 0.0
        self.play_sound("start")

    def activate_random_hole(self) -> None:
        available = [index for index, hole in enumerate(self.holes) if not hole.active and hole.cooldown <= 0]
        if not available:
            return

        index = random.choice(available)
        hole = self.holes[index]
        hole.active = True
        hole.hit = False
        hole.pop_timer = self.popup_duration
        hole.cooldown = 0.15
        self.last_hit_index = index

    def handle_click(self, pos: tuple[int, int]) -> None:
        if self.state in {"start", "game_over"}:
            if self.button_rect.collidepoint(pos):
                self.reset_game()
            return

        for index, hole in enumerate(self.holes):
            if hole.active and not hole.hit and hole.mole_rect.collidepoint(pos):
                hole.hit = True
                hole.pop_timer = 0.22
                gained = 10 + min(self.combo, 5) * 2
                self.score += gained
                self.combo += 1
                self.hit_flash_timer = 0.16
                self.last_hit_index = index
                self.play_sound("hit")
                return

        self.combo = 0
        self.play_sound("miss")

    def update_playing(self, dt: float) -> None:
        self.time_left = max(0.0, self.time_left - dt)
        if self.time_left <= 0:
            self.state = "game_over"
            self.best_score = max(self.best_score, self.score)
            for hole in self.holes:
                hole.active = False
                hole.hit = False
            self.play_sound("game_over")
            return

        progress = 1.0 - (self.time_left / GAME_DURATION)
        combo_pressure = min(self.combo, 12) / 12.0

        base_spawn_delay = 0.8 - progress * 0.42
        combo_spawn_bonus = combo_pressure * 0.20
        self.spawn_delay = max(0.20, base_spawn_delay - combo_spawn_bonus)

        base_popup_duration = 0.9 - progress * 0.32
        combo_popup_penalty = combo_pressure * 0.18
        self.popup_duration = max(0.28, base_popup_duration - combo_popup_penalty)

        time_difficulty = progress * 0.8
        combo_difficulty = combo_pressure * 0.7
        self.difficulty_level = 1.0 + time_difficulty + combo_difficulty

        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.activate_random_hole()
            self.spawn_timer = self.spawn_delay

        for hole in self.holes:
            hole.cooldown = max(0.0, hole.cooldown - dt)
            if not hole.active:
                continue

            hole.pop_timer -= dt
            if hole.pop_timer <= 0:
                if not hole.hit:
                    self.combo = 0
                hole.active = False
                hole.hit = False
                hole.pop_timer = 0.0
                hole.cooldown = 0.12

        self.hit_flash_timer = max(0.0, self.hit_flash_timer - dt)

    def draw_panel(self, position: tuple[int, int], label: str, value: str, accent: tuple[int, int, int]) -> None:
        panel_rect = self.panel_image.get_rect(topleft=position)
        self.screen.blit(self.panel_image, panel_rect)

        label_surface = self.label_font.render(label, True, accent)
        value_surface = self.value_font.render(value, True, (220, 250, 255))
        self.screen.blit(label_surface, (panel_rect.x + 26, panel_rect.y + 20))
        self.screen.blit(value_surface, (panel_rect.x + 26, panel_rect.y + 50))

    def draw_button(self, text: str) -> None:
        self.screen.blit(self.button_image, self.button_rect)
        text_surface = self.label_font.render(text, True, (220, 255, 245))
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_title_block(self, subtitle: str, instruction: str) -> None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((4, 8, 20, 140))
        self.screen.blit(overlay, (0, 0))

        title = self.title_font.render("SPACE FARM MOLE PATROL", True, (125, 245, 255))
        subtitle_surface = self.label_font.render(subtitle, True, (255, 110, 120))
        instruction_surface = self.info_font.render(instruction, True, (210, 236, 245))

        title_rect = title.get_rect(center=(WIDTH // 2, 120))
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, 168))
        instruction_rect = instruction_surface.get_rect(center=(WIDTH // 2, 208))

        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle_surface, subtitle_rect)
        self.screen.blit(instruction_surface, instruction_rect)

    def draw_game(self) -> None:
        self.screen.blit(self.background, (0, 0))

        for hole in self.holes:
            if hole.active:
                image = self.mole_hit if hole.hit else self.mole_idle
                scaled = pygame.transform.smoothscale(image, hole.mole_rect.size)
                self.screen.blit(scaled, hole.mole_rect)

            self.screen.blit(self.hole_image, hole.rect)

        self.draw_panel((38, 22), "SCORE", f"{self.score:04d}", (255, 110, 120))
        self.draw_panel((445, 22), "TIME", f"{self.time_left:04.1f}", (125, 245, 255))
        self.draw_panel((852, 22), "COMBO", f"x{self.combo}", (130, 255, 195))
        difficulty_text = self.info_font.render(f"Threat level {self.difficulty_level:.2f}x", True, (255, 190, 120))
        self.screen.blit(difficulty_text, (950, 142))

        objective = self.info_font.render("Protect the hydroponic bay. Laser-click the rogue moles.", True, (190, 228, 240))
        self.screen.blit(objective, (44, 142))

        if self.hit_flash_timer > 0:
            alpha = int(70 * (self.hit_flash_timer / 0.16))
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash.fill((80, 255, 210, alpha))
            self.screen.blit(flash, (0, 0))

        if self.state == "start":
            self.draw_title_block("Hydroponic sabotage detected", "Click moles before they chew through the crops.")
            self.draw_button("BEGIN PATROL")
        elif self.state == "game_over":
            self.draw_title_block(f"Shift complete. Final score {self.score}", "Click below to start a new patrol run.")
            best = self.label_font.render(f"Best score {self.best_score}", True, (130, 255, 195))
            best_rect = best.get_rect(center=(WIDTH // 2, 252))
            self.screen.blit(best, best_rect)
            self.draw_button("RESTART")

        crosshair_rect = self.crosshair.get_rect(center=self.mouse_pos)
        self.screen.blit(self.crosshair, crosshair_rect)

    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            if self.state == "playing":
                self.update_playing(dt)

            self.draw_game()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    SpaceFarmWhack().run()
