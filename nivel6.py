import pygame
import random
import math
import subprocess
import sys
from pygame import Rect

# --- Configuración ---
WIDTH, HEIGHT = 960, 540
FPS = 90

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
GREEN = (80, 200, 120)
YELLOW = (240, 220, 80)
BLUE = (80, 160, 240)
GREY = (200, 200, 200)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
PURPLE = (180, 80, 220)
CYAN = (80, 220, 220)
DARK_RED = (139, 0, 0)
BROWN = (139, 69, 19)
PINK = (255, 105, 180)
LIME = (50, 255, 50)
HOT_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
ELECTRIC_BLUE = (125, 249, 255)
LAYLA_COLOR = (255, 105, 180)  # Color rosa más brillante para Layla

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nivel 7 - Caza Fantasmas")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 48)
dialogue_font = pygame.font.SysFont("Arial", 28)

# --- Recursos ---
try:
    fondo_img = pygame.image.load("img/bosque.png").convert()
    fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))
except:
    print("No se pudo cargar bosque.png, usando fondo por defecto")
    fondo_img = pygame.Surface((WIDTH, HEIGHT))
    fondo_img.fill((20, 10, 40))  # Fondo morado oscuro

nave_img_original = pygame.image.load("img/nave.png").convert_alpha()

# Cargar imagen de fantasmas
try:
    ghost_img = pygame.image.load("img/fantasma.png").convert_alpha()
    ghost_img = pygame.transform.scale(ghost_img, (80, 80))
    has_ghost_img = True
except:
    print("No se pudo cargar fantasma.png, usando imagen por defecto")
    ghost_img = pygame.Surface((80, 80), pygame.SRCALPHA)
    pygame.draw.circle(ghost_img, (200, 200, 255, 180), (40, 40), 35)
    has_ghost_img = False

# Cargar imágenes para la introducción
try:
    player_nave_img = pygame.image.load("img/niño.png").convert_alpha()
    player_nave_img = pygame.transform.scale(player_nave_img, (200, 200))
    has_player_nave_img = True
except:
    print("No se pudo cargar la imagen del niño")
    has_player_nave_img = False

# Cargar imagen para Layla
try:
    layla_img = pygame.image.load("img/ine2.png").convert_alpha()
    layla_img = pygame.transform.scale(layla_img, (200, 200))
    has_layla_img = True
except:
    print("No se pudo cargar la imagen de Layla, usando imagen por defecto")
    has_layla_img = False

# Cargar imagen de nave para Layla en el juego
try:
    layla_nave_img = pygame.image.load("img/ine.png").convert_alpha()
    layla_nave_img = pygame.transform.scale(layla_nave_img, (60, 60))
    has_layla_nave_img = True
except:
    print("No se pudo cargar la nave de Layla, creando una por defecto")
    has_layla_nave_img = False
    layla_nave_img = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.circle(layla_nave_img, LAYLA_COLOR, (30, 30), 25)
    # Dibujar detalles en la nave
    pygame.draw.circle(layla_nave_img, (255, 255, 255), (45, 30), 8)

# Cargar GIF del OK
try:
    ok_image = pygame.image.load("img/bravo.png").convert_alpha()
    ok_image = pygame.transform.scale(ok_image, (320, 180))
    has_ok_image = True
except:
    print("No se pudo cargar ok.png, se usará texto alternativo")
    has_ok_image = False

# Música y sonidos
try:
    # Música para la introducción
    intro_music = "sound/vic.mp3"
    # Música para el nivel
    nivel_music = "sound/f7.mp3"

    pygame.mixer.music.set_volume(0.8)
    has_music = True
except:
    print("No se pudo cargar la música")
    has_music = False

sonido_inicio = pygame.mixer.Sound("sound/inicio1.mp3")   
sonido_daño = pygame.mixer.Sound("sound/hit.mp3")        
sonido_coin = pygame.mixer.Sound("sound/coin2.mp3")       
sonido_victoria = pygame.mixer.Sound("sound/victoria.mp3") 
sonido_misil = pygame.mixer.Sound("sound/misil.mp3")
sonido_texto = pygame.mixer.Sound("sound/text.mp3")

# Cargar sonido de fantasma
try:
    sonido_fantasma = pygame.mixer.Sound("sound/boo.mp3")
    sonido_fantasma.set_volume(0.5)
    has_ghost_sound = True
except:
    print("No se pudo cargar boo.mp3")
    has_ghost_sound = False

# Cargar sonido de KO
try:
    sonido_knockout = pygame.mixer.Sound("sound/bravo.mp3")
    has_knockout_sound = True
except:
    print("No se pudo cargar bravo.mp3")
    has_knockout_sound = False

# --- Nave Aliada (Layla/Ine) ---
class AllyShip:
    def __init__(self):
        self.x = 150  # Lado izquierdo de la pantalla
        self.y = HEIGHT // 2
        self.size = 60
        self.speed = 60
        self.shoot_cooldown = 0.7
        self.shoot_timer = random.uniform(0, 0.7)
        self.target_y = HEIGHT // 2
        self.move_timer = 0
        self.move_duration = 2.0
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        self.direction = 1  # 1 para arriba, -1 para abajo
        self.bounce_height = 100  # Altura máxima del rebote
        
    def update(self, dt, enemy_bullets, ghosts):
        # Movimiento vertical en patrón de rebote
        self.move_timer += dt
        
        # Cambiar dirección cuando alcanza los límites
        if self.y <= 100:
            self.direction = 1
        elif self.y >= HEIGHT - 100 - self.size:
            self.direction = -1
        
        # Movimiento suave con patrón de onda
        wave_offset = math.sin(self.move_timer * 2) * 30
        self.y += self.direction * self.speed * dt + wave_offset * dt
        
        # Mantener dentro de límites
        self.y = max(80, min(HEIGHT - 80 - self.size, self.y))
        
        # Disparar a los fantasmas
        self.shoot_timer -= dt
        if self.shoot_timer <= 0 and ghosts:
            # Encontrar todos los fantasmas en pantalla
            visible_ghosts = [ghost for ghost in ghosts if ghost.x < WIDTH - 100]
            
            if visible_ghosts:
                # Elegir un fantasma aleatorio para disparar
                target_ghost = random.choice(visible_ghosts)
                
                # Calcular dirección hacia el fantasma
                dx = target_ghost.x - (self.x + self.size)
                dy = target_ghost.y - (self.y + self.size//2)
                dist = max(0.1, math.sqrt(dx*dx + dy*dy))
                
                # Crear bala aliada
                bullet = Bullet(
                    self.x + self.size,  # Disparar desde el lado derecho de la nave
                    self.y + self.size//2,
                    (dx/dist) * 350, (dy/dist) * 350,
                    color=LAYLA_COLOR, owner="ally", damage=12
                )
                enemy_bullets.append(bullet)
                
                self.shoot_timer = self.shoot_cooldown
                self.shoot_cooldown = random.uniform(0.5, 0.9)
        
        self.rect.topleft = (int(self.x), int(self.y))
    
    def draw(self, surf):
        if has_layla_nave_img:
            surf.blit(layla_nave_img, (int(self.x), int(self.y)))
        else:
            # Dibujar nave por defecto (forma de nave más estilizada)
            pygame.draw.polygon(surf, LAYLA_COLOR, [
                (self.x, self.y + self.size//2),
                (self.x + self.size, self.y + 10),
                (self.x + self.size, self.y + self.size - 10),
                (self.x, self.y + self.size//2)
            ])
            
            # Detalles de la nave
            pygame.draw.circle(surf, (255, 255, 255), 
                             (int(self.x + self.size - 15), int(self.y + self.size//2)), 8)
            pygame.draw.circle(surf, (255, 100, 255), 
                             (int(self.x + self.size - 15), int(self.y + self.size//2)), 5)

# --- Efecto de Knockout ---
class KnockoutEffect:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.duration = 4.0
        self.alpha = 0
        self.scale = 0.1
        self.sound_played = False
        self.freeze_game = False
        self.show_stats = False

    def activate(self):
        self.active = True
        self.timer = 0
        self.alpha = 0
        self.scale = 0.1
        self.sound_played = False
        self.freeze_game = True
        self.show_stats = False
        if has_knockout_sound:
            sonido_knockout.play()

    def update(self, dt):
        if not self.active:
            return False
            
        self.timer += dt
        progress = min(1.0, self.timer / self.duration)
        
        if progress < 0.3:
            self.alpha = int(progress / 0.3 * 255)
            self.scale = 0.1 + (1.0 - 0.1) * (progress / 0.3)
        elif progress < 0.6:
            self.alpha = 255
            self.scale = 1.0
        elif progress < 0.8:
            self.alpha = int((1.0 - (progress - 0.6) / 0.2) * 255)
            self.scale = 1.0
        else:
            self.show_stats = True
            self.alpha = 0
            
        if progress >= 1.0:
            self.active = False
            self.freeze_game = False
            return True
        return False

    def draw(self, surf):
        if not self.active:
            return
            
        effect_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        if not self.show_stats:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            effect_surface.blit(overlay, (0, 0))
            
            if has_ok_image:
                scaled_ok = pygame.transform.scale(ok_image, 
                                                 (int(320 * self.scale), 
                                                  int(180 * self.scale)))
                scaled_ok.set_alpha(self.alpha)
                ok_rect = scaled_ok.get_rect(center=(WIDTH//2, HEIGHT//2))
                effect_surface.blit(scaled_ok, ok_rect)
            else:
                ok_font = pygame.font.SysFont("Arial", int(80 * self.scale))
                ok_text = ok_font.render("OK", True, (255, 255, 0))
                ok_rect = ok_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
                effect_surface.blit(ok_text, ok_rect)
                
                ko_font = pygame.font.SysFont("Arial", int(40 * self.scale))
                ko_text = ko_font.render("¡NIVEL COMPLETADO!", True, (255, 50, 50))
                ko_rect = ko_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
                effect_surface.blit(ko_text, ko_rect)
        else:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            effect_surface.blit(overlay, (0, 0))
            
            victory_font = pygame.font.SysFont("Arial", 48)
            victory_text = victory_font.render("¡VICTORIA!", True, GOLD)
            effect_surface.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, HEIGHT//2 - 100))
            
            continue_font = pygame.font.SysFont("Arial", 24)
            continue_text = continue_font.render("Presiona ESPACIO para ver estadísticas", True, WHITE)
            effect_surface.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 50))
        
        surf.blit(effect_surface, (0, 0))

# --- Sistema de Scroll ---
class ScrollSystem:
    def __init__(self):
        self.scroll_x = 0
        self.scroll_speed = 100
        self.base_speed = 100
        
    def update(self, dt):
        self.scroll_x -= self.scroll_speed * dt
        if self.scroll_x <= -WIDTH:
            self.scroll_x = 0
            
    def get_scroll_offset(self):
        return self.scroll_x

# --- Sistema de Partículas para Fantasmas ---
class GhostParticleSystem:
    def __init__(self):
        self.particles = []
        
    def create_ghost_trail(self, x, y, count=5):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(10, 30)
            lifetime = random.uniform(0.5, 1.5)
            size = random.randint(8, 15)
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': (random.randint(150, 255), random.randint(150, 255), 255, random.randint(100, 180)),
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'size': size
            })
            
    def update(self, dt):
        for p in self.particles[:]:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['lifetime'] -= dt
                
            if p['lifetime'] <= 0:
                self.particles.remove(p)
                
    def draw(self, surf):
        for p in self.particles:
            alpha = int(255 * (p['lifetime'] / p['max_lifetime']))
            color = (p['color'][0], p['color'][1], p['color'][2], alpha)
            
            particle_surf = pygame.Surface((p['size'], p['size']), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, (p['size']//2, p['size']//2), p['size']//2)
            surf.blit(particle_surf, (int(p['x']), int(p['y'])))

# --- Efecto de Flash y Oscuridad MEJORADO ---
class FlashEffect:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.duration = 0.3
        self.flash_alpha = 0
        self.dark_alpha = 180
        self.dark_mode = True
        self.dark_timer = 0
        self.dark_duration = 5.0
        self.light_duration = 3.0
        self.cycle_timer = 0
        self.initial_darkness = True
        self.initial_dark_timer = 0
        self.initial_dark_duration = 21.0
        
    def activate_flash(self):
        self.active = True
        self.timer = 0
        self.flash_alpha = 255
        
    def update(self, dt):
        if self.initial_darkness:
            self.initial_dark_timer += dt
            if self.initial_dark_timer >= self.initial_dark_duration:
                self.initial_darkness = False
                self.activate_flash()
                self.dark_mode = False
                self.dark_timer = 0
            return
        
        self.cycle_timer += dt
        
        if self.dark_mode:
            self.dark_timer += dt
            if self.dark_timer >= self.dark_duration:
                self.dark_mode = False
                self.dark_timer = 0
                self.activate_flash()
        else:
            self.dark_timer += dt
            if self.dark_timer >= self.light_duration:
                self.dark_mode = True
                self.dark_timer = 0
                self.activate_flash()
        
        if self.active:
            self.timer += dt
            progress = min(1.0, self.timer / self.duration)
            self.flash_alpha = int(255 * (1 - progress))
            
            if progress >= 1.0:
                self.active = False
                
    def draw(self, surf):
        if self.initial_darkness:
            dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, self.dark_alpha))
            surf.blit(dark_overlay, (0, 0))
           
        else:
            if self.dark_mode:
                dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                dark_overlay.fill((0, 0, 0, 150))
                surf.blit(dark_overlay, (0, 0))
                
        if self.active:
            flash_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_overlay.fill((255, 255, 255, self.flash_alpha))
            surf.blit(flash_overlay, (0, 0))

# --- Sistema de Introducción para Nivel 7 ---
class IntroductionSystem:
    def __init__(self):
        self.active = True
        self.current_dialogue = 0
        self.dialogues = [
            {
                "speaker": "player",
                "text": "¿Qué es esto? Parece una casa embrujada...",
                "position": "left"
            },
            {
                "speaker": "layla", 
                "text": "Este es el camino más corto para salir",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "Pero está lleno de fantasmas",
                "position": "left"
            },
            {
                "speaker": "layla",
                "text": "Vamos, tú me salvaste de ese cazador. ¡Tú puedes con esto!",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "Está bien, lo haré",
                "position": "left"
            },
            {
                "speaker": "layla",
                "text": "Yo te ayudaré y te guiaré",
                "position": "right"
            }
        ]
        self.text_speed = 30
        self.current_char = 0
        self.text_timer = 0
        self.sound_played = False
        self.music_started = False
        self.text_complete = False
        self.can_advance = False

    def start_intro_music(self):
        if not self.music_started and has_music:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(intro_music)
                pygame.mixer.music.set_volume(0.8)
                pygame.mixer.music.play(-1)
                self.music_started = True
            except:
                print("No se pudo cargar la música de introducción")

    def stop_intro_music(self):
        pygame.mixer.music.stop()
        self.music_started = False
        
    def start_level_music(self):
        if has_music:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(nivel_music)
                pygame.mixer.music.set_volume(0.8)
                pygame.mixer.music.play(-1)
            except:
                print("No se pudo cargar la música del nivel")

    def update(self, dt):
        current_dialogue = self.dialogues[self.current_dialogue]
        
        if not self.text_complete:
            self.text_timer += dt
            target_chars = int(self.text_timer * self.text_speed)
            
            if target_chars > self.current_char:
                chars_to_add = target_chars - self.current_char
                old_char = self.current_char
                self.current_char = min(self.current_char + chars_to_add, len(current_dialogue["text"]))
                
                if old_char == 0 and self.current_char > 0 and not self.sound_played:
                    sonido_texto.play()
                    self.sound_played = True
                
                if self.current_char >= len(current_dialogue["text"]):
                    self.text_complete = True
                    self.can_advance = True

    def draw(self, surf):
        surf.fill((5, 2, 10))
        
        # Dibujar silueta de casa embrujada
        pygame.draw.rect(surf, (15, 8, 25), (WIDTH//2 - 200, HEIGHT//2 - 150, 400, 300))
        pygame.draw.polygon(surf, (20, 10, 30), [(WIDTH//2 - 200, HEIGHT//2 - 150), 
                                               (WIDTH//2, HEIGHT//2 - 250), 
                                               (WIDTH//2 + 200, HEIGHT//2 - 150)])
        
        # Ventanas
        pygame.draw.rect(surf, (255, 255, 100), (WIDTH//2 - 150, HEIGHT//2 - 100, 40, 60))
        pygame.draw.rect(surf, (255, 255, 100), (WIDTH//2 + 110, HEIGHT//2 - 100, 40, 60))
        
        # Puerta
        pygame.draw.rect(surf, (60, 30, 10), (WIDTH//2 - 40, HEIGHT//2, 80, 150))
        
        current_dialogue = self.dialogues[self.current_dialogue]
        
        if current_dialogue["speaker"] == "player" and has_player_nave_img:
            char_x = 50
            char_y = HEIGHT//2 - 100
            surf.blit(player_nave_img, (char_x, char_y))
        
        if current_dialogue["speaker"] == "layla" and has_layla_img:
            char_x = WIDTH - 250
            char_y = HEIGHT//2 - 100
            surf.blit(layla_img, (char_x, char_y))
        
        dialog_rect = pygame.Rect(50, HEIGHT - 200, WIDTH - 100, 150)
        
        pygame.draw.rect(surf, (10, 5, 20), dialog_rect, border_radius=15)
        pygame.draw.rect(surf, PURPLE, dialog_rect, 3, border_radius=15)
        
        speaker_names = {
            "player": "Jony",
            "layla": "Ines"
        }
        
        name_colors = {
            "player": CYAN,
            "layla": LAYLA_COLOR
        }
        
        name_text = title_font.render(speaker_names[current_dialogue["speaker"]], True, name_colors[current_dialogue["speaker"]])
        surf.blit(name_text, (dialog_rect.x + 20, dialog_rect.y + 15))
        
        current_text = current_dialogue["text"][:self.current_char]
        
        words = current_text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if dialogue_font.size(test_line)[0] < dialog_rect.width - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        if current_line:
            lines.append(current_line)
        
        text_y = dialog_rect.y + 60
        for line in lines:
            if line.strip():
                line_surface = dialogue_font.render(line, True, WHITE)
                surf.blit(line_surface, (dialog_rect.x + 20, text_y))
                text_y += 35
        
        if self.can_advance:
            prompt_text = "Presiona X para continuar" if self.current_dialogue < len(self.dialogues) - 1 else "Presiona X para comenzar"
            prompt = dialogue_font.render(prompt_text, True, GREEN)
            surf.blit(prompt, (dialog_rect.x + 20, dialog_rect.bottom - 40))
            
            if pygame.time.get_ticks() % 800 < 400:
                triangle_x = dialog_rect.x + 20 + prompt.get_width() + 20
                triangle_points = [
                    (triangle_x, dialog_rect.bottom - 25),
                    (triangle_x + 20, dialog_rect.bottom - 25),
                    (triangle_x + 10, dialog_rect.bottom - 5)
                ]
                pygame.draw.polygon(surf, YELLOW, triangle_points)
        else:
            if pygame.time.get_ticks() % 600 < 300:
                dots_text = dialogue_font.render("...", True, YELLOW)
                surf.blit(dots_text, (dialog_rect.right - 50, dialog_rect.bottom - 40))

    def advance_text(self):
        if not self.can_advance:
            return "writing"
            
        sonido_texto.play()
        
        self.current_dialogue += 1
        self.current_char = 0
        self.text_timer = 0
        self.text_complete = False
        self.can_advance = False
        self.sound_played = False
        
        if self.current_dialogue >= len(self.dialogues):
            self.active = False
            self.stop_intro_music()
            return "start_battle"
        
        return "continue"

# --- Sistema de Presentación ---
class TitleScreen:
    def __init__(self):
        self.active = True
        self.timer = 0
        self.total_time = 5.0
        self.phase = 0
        self.alpha = 0
        self.fade_alpha = 0
        
    def update(self, dt):
        self.timer += dt
        
        if self.phase == 0:
            self.alpha = min(255, int((self.timer / 2.0) * 255))
            if self.timer >= 2.0:
                self.phase = 1
                self.timer = 0
                
        elif self.phase == 1:
            if self.timer >= 3.0:
                self.phase = 2
                self.timer = 0
                
        elif self.phase == 2:
            self.alpha = max(0, 255 - int((self.timer / 1.0) * 255))
            if self.timer >= 1.0:
                self.phase = 3
                self.timer = 0
                
        elif self.phase == 3:
            self.fade_alpha = min(255, int(self.timer * 255))
            if self.fade_alpha >= 255:
                self.active = False
                return True
        return False
        
    def draw(self, surf):
        surf.fill((5, 2, 10))
        
        title_surface = title_font.render("NIVEL 7", True, CYAN)
        title_surface.set_alpha(self.alpha)
        surf.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, HEIGHT//2 - 100))
        
        subtitle_surface = dialogue_font.render("Caza Fantasmas", True, CYAN)
        subtitle_surface.set_alpha(self.alpha)
        surf.blit(subtitle_surface, (WIDTH//2 - subtitle_surface.get_width()//2, HEIGHT//2 - 20))
        
        if self.phase in [0, 1, 2]:
            for i in range(15):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                size = random.randint(1, 3)
                brightness = random.randint(100, 200)
                pygame.draw.circle(surf, (brightness, brightness, 255), (x, y), size)
        
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill((5, 2, 10))
            fade_surface.set_alpha(self.fade_alpha)
            surf.blit(fade_surface, (0, 0))

# --- Clase Fantasma ---
class Ghost:
    def __init__(self, ghost_type="normal"):
        self.type = ghost_type
        self.size = random.randint(60, 90)
        
        if ghost_type == "normal":
            self.speed = random.uniform(100, 200)
            self.hp = 30
            self.color = (200, 200, 255, 180)
            self.points = 10
            self.attack_cooldown = 1.0
        elif ghost_type == "shooter":
            self.speed = random.uniform(80, 150)
            self.hp = 50
            self.color = (255, 150, 150, 200)
            self.points = 20
            self.shoot_cooldown = 2.0
            self.shoot_timer = random.uniform(0, 2.0)
            self.attack_cooldown = 1.0
        elif ghost_type == "charger":
            self.speed = random.uniform(150, 250)
            self.hp = 70
            self.color = (150, 255, 150, 220)
            self.points = 30
            self.charge_timer = 0
            self.charging = False
            self.attack_cooldown = 0.5
        
        self.x = random.randint(WIDTH + 50, WIDTH + 300)
        self.y = random.randint(50, HEIGHT - 50)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        self.alpha = random.randint(150, 220)
        self.float_timer = 0
        self.float_speed = random.uniform(2, 4)
        self.float_amount = random.uniform(10, 20)
        self.attack_timer = 0
        self.last_sound_time = 0
        self.sound_cooldown = 3.0
        
    def update(self, dt, enemy_bullets, player, ally_ship):
        self.float_timer += dt
        float_offset = math.sin(self.float_timer * self.float_speed) * self.float_amount

        if self.type == "charger" and self.charging:
            dx = player.x - self.x
            dy = (player.y + float_offset) - self.y
            dist = max(0.1, math.sqrt(dx*dx + dy*dy))
            self.x += (dx/dist) * self.speed * 1.5 * dt
            self.y += (dy/dist) * self.speed * 1.5 * dt
        elif self.type == "normal":
            dx = player.x - self.x
            dy = player.y - self.y
            dist = max(0.1, math.sqrt(dx*dx + dy*dy))
            if dist < 200:
                self.x += (dx/dist) * self.speed * 0.8 * dt
                self.y += (dy/dist) * self.speed * 0.8 * dt
            else:
                self.x -= self.speed * dt
                self.y += float_offset * dt * 0.5
        else:
            self.x -= self.speed * dt
            self.y += float_offset * dt * 0.5
        
        self.y = max(30, min(HEIGHT - 30, self.y))
        
        if self.type == "shooter":
            self.shoot_timer -= dt
            if self.shoot_timer <= 0:
                self.shoot(enemy_bullets, player)
                self.shoot_timer = self.shoot_cooldown
                
        elif self.type == "charger":
            self.charge_timer += dt
            if not self.charging and self.charge_timer >= 3.0:
                self.charging = True
                self.charge_timer = 0
            elif self.charging and self.charge_timer >= 1.5:
                self.charging = False
                self.charge_timer = 0
        
        self.attack_timer -= dt
        dist_to_player = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
        if dist_to_player < 50 and self.attack_timer <= 0:
            player.take_damage()
            self.attack_timer = self.attack_cooldown
            
            current_time = pygame.time.get_ticks() / 1000.0
            if has_ghost_sound and current_time - self.last_sound_time > self.sound_cooldown and random.random() < 0.3:
                sonido_fantasma.play()
                self.last_sound_time = current_time
        
        self.rect.topleft = (int(self.x), int(self.y))
        
    def shoot(self, enemy_bullets, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max(0.1, math.sqrt(dx*dx + dy*dy))
        
        bullet_color = (255, 100, 100) if self.type == "shooter" else (100, 255, 100)
        enemy_bullets.append(Bullet(
            self.x, self.y + self.size//2,
            (dx/dist) * 300, (dy/dist) * 300,
            color=bullet_color, owner="ghost", damage=15
        ))
        
    def take_damage(self, damage):
        self.hp -= damage
        destroyed = self.hp <= 0
        
        if destroyed and has_ghost_sound and random.random() < 0.4:
            current_time = pygame.time.get_ticks() / 1000.0
            if current_time - self.last_sound_time > 1.0:
                sonido_fantasma.play()
                self.last_sound_time = current_time
                
        return destroyed
        
    def draw(self, surf):
        ghost_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        if has_ghost_img:
            ghost_img_scaled = pygame.transform.scale(ghost_img, (self.size, self.size))
            ghost_surface.blit(ghost_img_scaled, (0, 0))
        else:
            pygame.draw.circle(ghost_surface, self.color, (self.size//2, self.size//2), self.size//2)
            
            eye_size = self.size // 5
            pygame.draw.circle(ghost_surface, (255, 0, 0), (self.size//3, self.size//2 - 5), eye_size)
            pygame.draw.circle(ghost_surface, (255, 0, 0), (2*self.size//3, self.size//2 - 5), eye_size)
            
            mouth_rect = pygame.Rect(self.size//3, 2*self.size//3, self.size//3, self.size//10)
            pygame.draw.ellipse(ghost_surface, (100, 0, 0), mouth_rect)
        
        surf.blit(ghost_surface, (int(self.x), int(self.y)))

# --- Clases del Juego ---
class Player:
    def __init__(self):
        self.base_size = 48
        self.size = self.base_size
        self.x = 80
        self.y = HEIGHT // 2
        self.speed = 5.0
        self.shrink_speed = 7.0
        self.lives = 3
        self.max_lives = 5
        self.shoot_cooldown = 0.15
        self.shoot_timer = 0.0
        self.is_shrunk = False
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.invulnerable = False
        self.invulnerable_timer = 0.0
        self.damage_taken = 0
        self.bullets_shot = 0
        self.bullets_hit = 0
        self.active = False
        
        self.energy = 0
        self.max_energy = 500
        self.missile_cooldown = 0.0
        self.missile_cooldown_time = 2.0
        
        self.victory_invincible = False
        self.victory_invincible_timer = 0.0

    def update(self, dt, keys):
        if not self.active:
            return
            
        self.is_shrunk = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        if self.is_shrunk:
            self.size = int(self.base_size * 0.55)
            speed = self.shrink_speed
        else:
            self.size = self.base_size
            speed = self.speed

        vx = vy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vy = 1
        if vx != 0 and vy != 0:
            vx *= 0.7071
            vy *= 0.7071

        self.x += vx * speed
        self.y += vy * speed

        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))

        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)

        if self.shoot_timer > 0:
            self.shoot_timer -= dt
            
        if self.missile_cooldown > 0:
            self.missile_cooldown -= dt

        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        if self.victory_invincible:
            self.victory_invincible_timer -= dt
            if self.victory_invincible_timer <= 0:
                self.victory_invincible = False

    def draw(self, surf):
        nave_scaled = pygame.transform.scale(nave_img_original, (self.size, self.size))
        if self.invulnerable and int(self.invulnerable_timer * 10) % 2 == 0:
            return
        surf.blit(nave_scaled, (self.x, self.y))

    def can_shoot(self):
        return self.active and (not self.is_shrunk) and self.shoot_timer <= 0

    def shoot(self):
        self.shoot_timer = self.shoot_cooldown
        self.bullets_shot += 1

    def can_launch_missile(self):
        return (self.active and 
                self.energy >= 100 and 
                self.missile_cooldown <= 0)

    def launch_missile(self):
        if self.can_launch_missile():
            self.energy -= 100
            self.missile_cooldown = self.missile_cooldown_time
            sonido_misil.play()
            return True
        return False

    def add_energy(self, amount):
        self.energy = min(self.max_energy, self.energy + amount)
        
    def add_lives(self, amount):
        self.lives = min(self.max_lives, self.lives + amount)

    def take_damage(self):
        if self.victory_invincible:
            return
            
        if not self.invulnerable:
            self.lives -= 1
            self.damage_taken += 1
            sonido_daño.play()
            self.invulnerable = True
            self.invulnerable_timer = 2.0
            self.x = max(0, self.x - 40)

    def activate_victory_invincibility(self, duration=10.0):
        self.victory_invincible = True
        self.victory_invincible_timer = duration

    def activate(self):
        self.active = True

class Bullet:
    def __init__(self, x, y, vx, vy, color=YELLOW, owner="player", damage=10):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 6 if owner == "player" else 8
        self.color = color
        self.owner = owner
        self.damage = damage
        self.rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)

class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.speed = 400
        self.color = PURPLE
        self.trail_particles = []
        self.rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)
        self.damage = 200

    def update(self, dt):
        self.x += self.speed * dt
        
        if random.random() < 0.7:
            self.trail_particles.append({
                'x': self.x - 10,
                'y': self.y + random.uniform(-5, 5),
                'size': random.randint(2, 5),
                'life': 1.0
            })
        
        for particle in self.trail_particles[:]:
            particle['life'] -= dt * 2
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
                
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))

    def draw(self, surf):
        for particle in self.trail_particles:
            alpha = int(particle['life'] * 255)
            color = (255, 100, 255, alpha)
            particle_surf = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, (particle['size']//2, particle['size']//2), particle['size']//2)
            surf.blit(particle_surf, (particle['x'], particle['y']))
        
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surf, YELLOW, (int(self.x + 8), int(self.y)), 4)

# --- Sistema de UI para Energía ---
class EnergyUI:
    def __init__(self):
        self.bar_width = 300
        self.bar_height = 20
        self.x = WIDTH - self.bar_width - 20
        self.y = 15

    def draw(self, surf, player):
        pygame.draw.rect(surf, (50, 50, 50), (self.x, self.y, self.bar_width, self.bar_height), border_radius=10)
        
        energy_ratio = player.energy / player.max_energy
        energy_width = int(self.bar_width * energy_ratio)
        
        if energy_ratio >= 1.0:
            bar_color = PURPLE
        elif energy_ratio >= 0.2:
            bar_color = BLUE
        else:
            bar_color = RED
            
        pygame.draw.rect(surf, bar_color, (self.x, self.y, energy_width, self.bar_height), border_radius=10)
        pygame.draw.rect(surf, WHITE, (self.x, self.y, self.bar_width, self.bar_height), 2, border_radius=10)
        
        energy_text = font.render(f"Energía: {player.energy}/{player.max_energy}", True, WHITE)
        surf.blit(energy_text, (self.x, self.y - 25))
        
        if player.energy >= 100:
            missile_text = font.render("MISIL LISTO (Z)", True, GREEN)
        else:
            missile_text = font.render(f"Necesitas {100 - player.energy} más para misil", True, YELLOW)
        surf.blit(missile_text, (self.x, self.y + 25))

# --- Barra de Progreso de Salida ---
class ProgressBar:
    def __init__(self):
        self.width = 400
        self.height = 25
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 40
        self.progress = 0.0
        self.max_progress = 150.0
        
    def update(self, current_time):
        self.progress = min(self.max_progress, current_time)
        
    def draw(self, surf):
        pygame.draw.rect(surf, (50, 50, 50), (self.x, self.y, self.width, self.height), border_radius=5)
        
        progress_width = int((self.progress / self.max_progress) * self.width)
        if progress_width > 0:
            pygame.draw.rect(surf, GREEN, (self.x, self.y, progress_width, self.height), border_radius=5)
        
        pygame.draw.rect(surf, WHITE, (self.x, self.y, self.width, self.height), 2, border_radius=5)
        
        time_left = max(0, self.max_progress - self.progress)
        minutes = int(time_left // 60)
        seconds = int(time_left % 60)
        time_text = font.render(f"SALIDA: {minutes:02d}:{seconds:02d}", True, WHITE)
        surf.blit(time_text, (self.x + self.width // 2 - time_text.get_width() // 2, self.y - 25))

# --- Sistema de Resultados ---
class ResultsSystem:
    def __init__(self):
        self.active = False
        self.grade = ""
        self.grade_color = WHITE
        self.motivational_phrase = ""
        
    def calculate_grade(self, continues_used, damage_taken, accuracy, completion_time, ghosts_defeated):
        score = 100
        
        if continues_used > 0:
            score -= continues_used * 25
            
        if damage_taken > 0:
            score -= min(damage_taken * 5, 30)
            
        if accuracy < 0.6:
            score -= 10
            
        if completion_time > 150:
            score -= 10
            
        if ghosts_defeated < 30:
            score -= 10

        if score >= 95:
            return "A+", GOLD, "¡EXCELENTE! Eres un cazafantasmas profesional"
        elif score >= 85:
            return "A", GREEN, "¡Muy bien! La casa está limpia de fantasmas"
        elif score >= 75:
            return "B", BLUE, "¡Buen trabajo! Pocos fantasmas escaparon"
        elif score >= 60:
            return "C", YELLOW, "¡Bien hecho! Sobreviviste a la casa embrujada"
        else:
            return "D", ORANGE, "¡Logrado! Escapaste de la casa embrujada"
            
    def show_results(self, player, continues_used, score, completion_time, ghosts_defeated):
        self.active = True
        
        accuracy = player.bullets_hit / player.bullets_shot if player.bullets_shot > 0 else 0
        
        self.grade, self.grade_color, self.motivational_phrase = self.calculate_grade(
            continues_used, player.damage_taken, accuracy, completion_time, ghosts_defeated
        )
        
        self.player_lives = player.lives
        self.player_max_lives = player.max_lives
        self.accuracy = accuracy
        self.score = score
        self.continues_used = continues_used
        self.completion_time = completion_time
        self.player_damage_taken = player.damage_taken
        self.player_bullets_hit = player.bullets_hit
        self.player_bullets_shot = player.bullets_shot
        self.ghosts_defeated = ghosts_defeated
        
    def draw(self, surf):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surf.blit(overlay, (0, 0))
        
        title_text = title_font.render("¡VICTORIA! - NIVEL 7", True, CYAN)
        surf.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 40))
        
        grade_text = large_font.render(f"Calificación: {self.grade}", True, self.grade_color)
        surf.blit(grade_text, (WIDTH//2 - grade_text.get_width()//2, 100))
        
        stats_y = 160
        stats = [
            f"Tiempo: {self.completion_time:.1f} segundos",
            f"Puntuación: {self.score} puntos",
            f"Continues usados: {self.continues_used}",
            f"Daño recibido: {self.player_damage_taken} veces",
            f"Precisión: {self.accuracy*100:.1f}% ({self.player_bullets_hit}/{self.player_bullets_shot})",
            f"Vidas restantes: {self.player_lives}/{self.player_max_lives}",
            f"Fantasmas derrotados: {self.ghosts_defeated}"
        ]
        
        for stat in stats:
            stat_text = font.render(stat, True, WHITE)
            surf.blit(stat_text, (WIDTH//2 - stat_text.get_width()//2, stats_y))
            stats_y += 35
        
        phrase_text = font.render(self.motivational_phrase, True, GREEN)
        surf.blit(phrase_text, (WIDTH//2 - phrase_text.get_width()//2, stats_y + 20))
        
        instruction_text = font.render("Presiona ENTER para continuar", True, YELLOW)
        surf.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 60))

# --- Funciones auxiliares ---
def rect_circle_collide(rect, circle_x, circle_y, radius):
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))
    dx = circle_x - closest_x
    dy = circle_y - closest_y
    return dx * dx + dy * dy <= radius * radius

# --- Estado del juego ---
player = Player()
player_bullets = []
enemy_bullets = []
missiles = []
ghosts = []
title_screen = TitleScreen()
introduction = IntroductionSystem()
energy_ui = EnergyUI()
results_system = ResultsSystem()
flash_effect = FlashEffect()
ghost_particles = GhostParticleSystem()
scroll_system = ScrollSystem()
progress_bar = ProgressBar()
knockout_effect = KnockoutEffect()
ally_ship = AllyShip()  # Nave de Layla/Ine

score = 0
game_over = False
level_cleared = False
fight_started = False
ghosts_defeated = 0
victory_sound_played = False
knockout_shown = False

continue_countdown = 0
continue_time = 10.0
coins_inserted = 0
continues_used = 0
continue_available = True
lives_per_coin = 3

start_time = pygame.time.get_ticks()
completion_time = 0

ghost_spawn_timer = 0
ghost_spawn_interval = 1.5
level_duration = 150
level_timer = 0

# --- Main loop ---
running = True
while running:
    dt_ms = clock.tick(FPS)
    dt = dt_ms / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_c and continue_countdown > 0 and continue_available:
                coins_inserted += 1
                continues_used += 1
                sonido_coin.play()
                player.add_lives(lives_per_coin)
                if coins_inserted >= 1:
                    continue_countdown = 0
                    player.invulnerable = True
                    player.invulnerable_timer = 3.0
                    enemy_bullets.clear()
                    player.x = 80
                    player.y = HEIGHT // 2
            if event.key == pygame.K_RETURN and results_system.active:
                running = False
                pygame.quit()
                try:
                    subprocess.run([sys.executable, "nivel7.py"])
                except:
                    print("No se pudo cargar el siguiente nivel")
                sys.exit()
            if event.key == pygame.K_SPACE and knockout_effect.active and knockout_effect.show_stats:
                knockout_effect.active = False
                knockout_effect.freeze_game = False
                results_system.show_results(player, continues_used, score, completion_time, ghosts_defeated)
            if event.key == pygame.K_x and introduction.active:
                result = introduction.advance_text()
                if result == "start_battle":
                    introduction.start_level_music()
                    player.activate()
                    fight_started = True
                    battle_start_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    if title_screen.active:
        if title_screen.update(dt):
            introduction.start_intro_music()
        title_screen.draw(screen)
        pygame.display.flip()
        continue

    if introduction.active:
        introduction.update(dt)
        introduction.draw(screen)
        pygame.display.flip()
        continue

    if results_system.active:
        results_system.draw(screen)
        pygame.display.flip()
        continue

    if knockout_effect.active:
        knockout_finished = knockout_effect.update(dt)
        if knockout_finished:
            knockout_effect.active = False
            knockout_effect.freeze_game = False
            results_system.show_results(player, continues_used, score, completion_time, ghosts_defeated)

    if not game_over and not level_cleared and fight_started and not results_system.active and not knockout_effect.freeze_game:
        level_timer += dt
        
        scroll_system.update(dt)
        progress_bar.update(level_timer)
        flash_effect.update(dt)
        
        # Actualizar nave de Layla/Ine
        ally_ship.update(dt, enemy_bullets, ghosts)
        
        if level_timer >= level_duration and not knockout_shown:
            level_cleared = True
            completion_time = (pygame.time.get_ticks() - start_time) / 1000.0
            if not victory_sound_played:
                sonido_victoria.play()
                victory_sound_played = True
            knockout_effect.activate()
            knockout_shown = True

        ghost_particles.update(dt)
        
        ghost_spawn_timer += dt
        
        if level_timer < 30:
            current_spawn_interval = 2.0
            spawn_chance = 0.8
            max_ghosts = 5
            
        elif level_timer < 90:
            current_spawn_interval = 1.2
            spawn_chance = 0.9
            max_ghosts = 8
            
        elif level_timer < 120:
            current_spawn_interval = 0.8
            spawn_chance = 0.95
            max_ghosts = 12
            
        else:
            current_spawn_interval = 2.5
            spawn_chance = 0.4
            max_ghosts = 6
        
        if (ghost_spawn_timer >= current_spawn_interval and 
            len(ghosts) < max_ghosts and
            random.random() < spawn_chance):
            
            ghost_spawn_timer = 0
            
            ghost_type_chance = random.random()
            if level_timer < 30:
                ghost_type = "normal"
            elif level_timer < 60:
                ghost_type = "normal" if ghost_type_chance < 0.7 else "shooter"
            elif level_timer < 90:
                ghost_type = "normal" if ghost_type_chance < 0.5 else "shooter"
            elif level_timer < 120:
                if ghost_type_chance < 0.4:
                    ghost_type = "normal"
                elif ghost_type_chance < 0.7:
                    ghost_type = "shooter"
                else:
                    ghost_type = "charger"
            else:
                if ghost_type_chance < 0.6:
                    ghost_type = "normal"
                elif ghost_type_chance < 0.9:
                    ghost_type = "shooter"
                else:
                    ghost_type = "charger"
            
            ghosts.append(Ghost(ghost_type))

        player.update(dt, keys)

        if keys[pygame.K_x] and player.can_shoot():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            bullet = Bullet(bx, by, 600, 0, color=CYAN, owner="player")
            player_bullets.append(bullet)
            player.shoot()

        if keys[pygame.K_z] and player.can_launch_missile():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            missile = Missile(bx, by)
            missiles.append(missile)
            player.launch_missile()

        for ghost in ghosts[:]:
            ghost.update(dt, enemy_bullets, player, ally_ship)
            
            if ghost.x < -100:
                ghosts.remove(ghost)
                continue

        for b in player_bullets[:]:
            b.update(dt)
            if b.x > WIDTH + 50:
                player_bullets.remove(b)
                continue
                
            for ghost in ghosts[:]:
                if rect_circle_collide(ghost.rect, b.x, b.y, b.radius):
                    if ghost.take_damage(b.damage):
                        score += ghost.points
                        player.add_energy(20)
                        ghosts_defeated += 1
                        ghost_particles.create_ghost_trail(ghost.x + ghost.size//2, ghost.y + ghost.size//2, 20)
                        ghosts.remove(ghost)
                    else:
                        player.add_energy(5)
                        ghost_particles.create_ghost_trail(b.x, b.y, 8)
                    player.bullets_hit += 1
                    if b in player_bullets:
                        player_bullets.remove(b)
                    break

        for m in missiles[:]:
            m.update(dt)
            if m.x > WIDTH + 50:
                missiles.remove(m)
                continue
                
            for ghost in ghosts[:]:
                if rect_circle_collide(ghost.rect, m.x, m.y, m.radius):
                    if ghost.take_damage(m.damage):
                        score += ghost.points
                        player.add_energy(30)
                        ghosts_defeated += 1
                        ghost_particles.create_ghost_trail(ghost.x + ghost.size//2, ghost.y + ghost.size//2, 30)
                        ghosts.remove(ghost)
                    else:
                        player.add_energy(15)
                        ghost_particles.create_ghost_trail(m.x, m.y, 15)
                    if m in missiles:
                        missiles.remove(m)
                    break

        for b in enemy_bullets[:]:
            b.update(dt)
            if b.x < -50 or b.y < -50 or b.y > HEIGHT + 50:
                enemy_bullets.remove(b)
                continue
            
            if b.owner == "ghost" and rect_circle_collide(player.rect, b.x, b.y, b.radius):
                player.take_damage()
                ghost_particles.create_ghost_trail(b.x, b.y, 10)
                if b in enemy_bullets:
                    enemy_bullets.remove(b)
            
            elif b.owner == "ally":
                for ghost in ghosts[:]:
                    if rect_circle_collide(ghost.rect, b.x, b.y, b.radius):
                        if ghost.take_damage(b.damage):
                            score += ghost.points
                            player.add_energy(10)
                            ghosts_defeated += 1
                            ghost_particles.create_ghost_trail(ghost.x + ghost.size//2, ghost.y + ghost.size//2, 15)
                            ghosts.remove(ghost)
                        else:
                            player.add_energy(3)
                            ghost_particles.create_ghost_trail(b.x, b.y, 5)
                        if b in enemy_bullets:
                            enemy_bullets.remove(b)
                        break

        if player.lives <= 0 and continue_available and continue_countdown == 0:
            continue_countdown = continue_time
            coins_inserted = 0

    if continue_countdown > 0:
        continue_countdown -= dt
        if continue_countdown <= 0:
            continue_countdown = 0
            game_over = True

    # --- DIBUJADO ---
    screen.fill(BLACK)
    
    scroll_offset = scroll_system.get_scroll_offset()
    for i in range(2):
        bg_x = int(scroll_offset + i * WIDTH)
        screen.blit(fondo_img, (bg_x, 0))
    
    if not knockout_effect.freeze_game:
        for b in player_bullets:
            b.draw(screen)
        for b in enemy_bullets:
            b.draw(screen)
        for m in missiles:
            m.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)

        if continue_countdown == 0:
            player.draw(screen)
            # Dibujar nave de Layla/Ine en el lado izquierdo
            ally_ship.draw(screen)
    
    ghost_particles.draw(screen)
    
    flash_effect.draw(screen)
    
    # NOTA: Se eliminó el efecto de neblina (fog_effect.draw(screen))
    
    if knockout_effect.active:
        knockout_effect.draw(screen)

    energy_ui.draw(screen, player)
    
    lives_text = font.render(f"Vidas: {player.lives}", True, WHITE)
    screen.blit(lives_text, (12, 12))
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (12, 36))
    
    progress_bar.draw(screen)
    
    ghosts_text = font.render(f"Fantasmas: {ghosts_defeated}", True, CYAN)
    screen.blit(ghosts_text, (WIDTH - 150, 12))
    
    if level_timer < 30:
        diff_text = font.render("DIFICULTAD: FÁCIL", True, GREEN)
    elif level_timer < 90:
        diff_text = font.render("DIFICULTAD: MEDIO", True, YELLOW)
    elif level_timer < 120:
        diff_text = font.render("DIFICULTAD: DIFÍCIL", True, ORANGE)
    else:
        diff_text = font.render("DIFICULTAD: FINAL - SOBREVIVE", True, RED)
    screen.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, HEIGHT - 80))
    
    # Indicador de Laylá ayudando
    if fight_started:
        layla_help_text = font.render("Laylá/Ine te está ayudando", True, LAYLA_COLOR)
        screen.blit(layla_help_text, (20, HEIGHT - 30))

    if continue_countdown > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        continue_text = large_font.render("¡HAS MUERTO!", True, RED)
        screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 - 100))
        
        countdown_text = large_font.render(f"Tiempo: {int(continue_countdown)}", True, ORANGE)
        screen.blit(countdown_text, (WIDTH//2 - countdown_text.get_width()//2, HEIGHT//2 - 40))
        
        instruction_text = font.render("Presiona C para insertar moneda y continuar", True, WHITE)
        screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 20))
        
        coins_text = font.render(f"Monedas insertadas: {coins_inserted}", True, YELLOW)
        screen.blit(coins_text, (WIDTH//2 - coins_text.get_width()//2, HEIGHT//2 + 60))
        
        lives_info = font.render(f"Cada moneda te da {lives_per_coin} vidas", True, GREEN)
        screen.blit(lives_info, (WIDTH//2 - lives_info.get_width()//2, HEIGHT//2 + 90))

    if game_over and continue_countdown == 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        over_surf = large_font.render("GAME OVER", True, RED)
        screen.blit(over_surf, (WIDTH//2 - over_surf.get_width()//2, HEIGHT//2 - 50))
        
        instruction_text = font.render("Presiona ESC para salir", True, WHITE)
        screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()

pygame.quit()