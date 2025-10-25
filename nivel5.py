import pygame
import random
import math
import subprocess
import sys
from pygame import Rect

# --- Configuración ---
WIDTH, HEIGHT = 960, 540
FPS = 60

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

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nivel 5 - Mi Clon Malvado")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 48)
dialogue_font = pygame.font.SysFont("Arial", 28)

# --- Recursos ---
fondo_img = pygame.image.load("img/pasillo.jpg").convert()
fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))

nave_img_original = pygame.image.load("img/nave.png").convert_alpha()
boss_img = pygame.image.load("img/clonM.png").convert_alpha()
boss_img = pygame.transform.scale(boss_img, (120, 120))

# Cargar imágenes para la introducción
try:
    evil_clone_img = pygame.image.load("img/clonM.png").convert_alpha()
    evil_clone_img = pygame.transform.scale(evil_clone_img, (300, 300))
    has_evil_clone_img = True
except:
    print("No se pudo cargar la imagen del clon malvado")
    has_evil_clone_img = False

try:
    player_nave_img = pygame.image.load("img/niño.png").convert_alpha()
    player_nave_img = pygame.transform.scale(player_nave_img, (200, 200))
    has_player_nave_img = True
except:
    print("No se pudo cargar la imagen de la nave")
    has_player_nave_img = False

# Cargar GIF del OK
try:
    ok_image = pygame.image.load("img/ok.png").convert_alpha()
    ok_image = pygame.transform.scale(ok_image, (320, 180))
    has_ok_image = True
except:
    print("No se pudo cargar ok.png, se usará texto alternativo")
    has_ok_image = False

# Música y sonidos
pygame.mixer.music.load("sound/cosmo.mp3")   
pygame.mixer.music.set_volume(0.4)

sonido_inicio = pygame.mixer.Sound("sound/inicio1.mp3")   
sonido_daño = pygame.mixer.Sound("sound/hit.mp3")        
sonido_coin = pygame.mixer.Sound("sound/coin.mp3")       
sonido_victoria = pygame.mixer.Sound("sound/victoria.mp3") 
sonido_misil = pygame.mixer.Sound("sound/misil.mp3")
sonido_fase = pygame.mixer.Sound("sound/coin.mp3")
sonido_terremoto = pygame.mixer.Sound("sound/terremoto.mp3")
sonido_texto = pygame.mixer.Sound("sound/text.mp3")

# Cargar sonido de KO
try:
    sonido_knockout = pygame.mixer.Sound("sound/kn.mp3")
    has_knockout_sound = True
except:
    print("No se pudo cargar kn.mp3")
    has_knockout_sound = False

victory_music = "sound/vic.mp3"
intro_music = "sound/vic.mp3"

# --- NUEVO: Sistema de Partículas Mejorado ---
class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_explosion(self, x, y, color=ORANGE, count=20, speed=100, size_range=(2, 6), duration=1.0):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed_var = random.uniform(speed * 0.5, speed * 1.5)
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed_var,
                'vy': math.sin(angle) * speed_var,
                'color': color,
                'size': random.uniform(size_range[0], size_range[1]),
                'life': duration,
                'max_life': duration,
                'gravity': random.uniform(50, 150)
            })
    
    def add_sparkle(self, x, y, color=YELLOW, count=5):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            distance = random.uniform(10, 30)
            self.particles.append({
                'x': x + math.cos(angle) * distance,
                'y': y + math.sin(angle) * distance,
                'vx': 0, 'vy': 0,
                'color': color,
                'size': random.uniform(1, 3),
                'life': 0.5,
                'max_life': 0.5,
                'gravity': 0
            })
    
    def add_trail(self, x, y, color=CYAN, count=3):
        for _ in range(count):
            self.particles.append({
                'x': x + random.uniform(-5, 5),
                'y': y + random.uniform(-5, 5),
                'vx': random.uniform(-20, 20),
                'vy': random.uniform(-20, 20),
                'color': color,
                'size': random.uniform(1, 2),
                'life': 0.3,
                'max_life': 0.3,
                'gravity': 50
            })
    
    def add_energy_glow(self, x, y, color=PURPLE, count=8):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            radius = random.uniform(5, 15)
            self.particles.append({
                'x': x + math.cos(angle) * radius,
                'y': y + math.sin(angle) * radius,
                'vx': 0, 'vy': 0,
                'color': color,
                'size': random.uniform(2, 4),
                'life': 0.8,
                'max_life': 0.8,
                'gravity': 0
            })
    
    def add_lightning(self, start_x, start_y, end_x, end_y, color=CYAN, count=3):
        for _ in range(count):
            segments = 8
            points = [(start_x, start_y)]
            current_x, current_y = start_x, start_y
            
            for i in range(1, segments):
                progress = i / segments
                next_x = start_x + (end_x - start_x) * progress + random.uniform(-30, 30)
                next_y = start_y + (end_y - start_y) * progress + random.uniform(-20, 20)
                points.append((next_x, next_y))
                
            points.append((end_x, end_y))
            
            # Añadir partículas a lo largo del rayo
            for i in range(len(points) - 1):
                dist = math.sqrt((points[i+1][0]-points[i][0])**2 + (points[i+1][1]-points[i][1])**2)
                steps = int(dist / 3)
                for j in range(steps):
                    t = j / steps
                    px = points[i][0] + (points[i+1][0]-points[i][0]) * t
                    py = points[i][1] + (points[i+1][1]-points[i][1]) * t
                    self.particles.append({
                        'x': px, 'y': py,
                        'vx': 0, 'vy': 0,
                        'color': color,
                        'size': random.uniform(1, 2),
                        'life': 0.2,
                        'max_life': 0.2,
                        'gravity': 0
                    })
    
    def update(self, dt):
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] += particle['gravity'] * dt
            particle['life'] -= dt
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, surf):
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            size = int(particle['size'] * (particle['life'] / particle['max_life']))
            if size < 1: size = 1
            
            color = list(particle['color'])
            if len(color) == 3:
                color.append(alpha)
            
            particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, (size, size), size)
            surf.blit(particle_surf, (int(particle['x'] - size), int(particle['y'] - size)))

# --- NUEVO: Efectos de Pantalla Completa ---
class ScreenEffects:
    def __init__(self):
        self.flash_alpha = 0
        self.flash_duration = 0
        self.flash_color = WHITE
        self.shake_intensity = 0
        self.shake_duration = 0
        self.chromatic_aberration = 0
        self.radial_blur = 0
        
    def screen_flash(self, color=WHITE, duration=0.2):
        self.flash_color = color
        self.flash_alpha = 255
        self.flash_duration = duration
        
    def screen_shake(self, intensity=10, duration=0.5):
        self.shake_intensity = intensity
        self.shake_duration = duration
        
    def add_chromatic_aberration(self, amount=3):
        self.chromatic_aberration = amount
        
    def add_radial_blur(self, amount=5):
        self.radial_blur = amount
        
    def update(self, dt):
        # Update flash
        if self.flash_alpha > 0:
            self.flash_alpha -= 255 * (dt / self.flash_duration)
            if self.flash_alpha < 0:
                self.flash_alpha = 0
                
        # Update shake
        if self.shake_duration > 0:
            self.shake_duration -= dt
            self.shake_intensity = max(0, self.shake_intensity * (self.shake_duration / 0.5))
        else:
            self.shake_intensity = 0
            
        # Reduce effects over time
        self.chromatic_aberration *= 0.9
        self.radial_blur *= 0.9
        
    def get_shake_offset(self):
        if self.shake_intensity > 0:
            return (random.uniform(-self.shake_intensity, self.shake_intensity),
                    random.uniform(-self.shake_intensity, self.shake_intensity))
        return (0, 0)

# --- NUEVO: Efectos de Transición ---
class TransitionEffects:
    def __init__(self):
        self.active = False
        self.type = "fade"
        self.progress = 0
        self.duration = 1.0
        self.color = BLACK
        
    def start_fade(self, color=BLACK, duration=1.0):
        self.active = True
        self.type = "fade"
        self.progress = 0
        self.duration = duration
        self.color = color
        
    def start_wipe(self, direction="right", duration=1.0):
        self.active = True
        self.type = f"wipe_{direction}"
        self.progress = 0
        self.duration = duration
        
    def update(self, dt):
        if self.active:
            self.progress += dt / self.duration
            if self.progress >= 1.0:
                self.active = False
                self.progress = 0
                
    def draw(self, surf):
        if not self.active:
            return
            
        if self.type == "fade":
            alpha = int(255 * self.progress)
            fade_surf = pygame.Surface((WIDTH, HEIGHT))
            fade_surf.fill(self.color)
            fade_surf.set_alpha(alpha)
            surf.blit(fade_surf, (0, 0))
            
        elif self.type.startswith("wipe"):
            wipe_surf = pygame.Surface((WIDTH, HEIGHT))
            wipe_surf.fill(BLACK)
            
            if self.type == "wipe_right":
                wipe_width = int(WIDTH * self.progress)
                pygame.draw.rect(wipe_surf, BLACK, (0, 0, wipe_width, HEIGHT))
            elif self.type == "wipe_left":
                wipe_width = int(WIDTH * self.progress)
                pygame.draw.rect(wipe_surf, BLACK, (WIDTH - wipe_width, 0, wipe_width, HEIGHT))
            elif self.type == "wipe_down":
                wipe_height = int(HEIGHT * self.progress)
                pygame.draw.rect(wipe_surf, BLACK, (0, 0, WIDTH, wipe_height))
            elif self.type == "wipe_up":
                wipe_height = int(HEIGHT * self.progress)
                pygame.draw.rect(wipe_surf, BLACK, (0, HEIGHT - wipe_height, WIDTH, wipe_height))
                
            surf.blit(wipe_surf, (0, 0))

# --- Sistema de Introducción Mejorado con Nuevos Efectos ---
class IntroductionSystem:
    def __init__(self):
        self.active = True
        self.current_dialogue = 0
        self.dialogues = [
            {
                "speaker": "evil_clone",
                "text": "¡Por fin apareciste! Te he estado esperando...",
                "position": "right",
                "effect": "lightning"
            },
            {
                "speaker": "player",
                "text": "¿Quién eres tú? No reconozco esta forma...",
                "position": "left",
                "effect": "glow"
            },
            {
                "speaker": "evil_clone", 
                "text": "Soy tu reflejo oscuro, todo lo que podrías haber sido.",
                "position": "right",
                "effect": "dark_aura"
            },
            {
                "speaker": "player",
                "text": "Eres como yo, pero... corrupto. ¿Qué quieres?",
                "position": "left",
                "effect": "pulse"
            },
            {
                "speaker": "evil_clone",
                "text": "Mientras tú jugabas a ser héroe, yo me hacía más fuerte.",
                "position": "right",
                "effect": "power_up"
            },
            {
                "speaker": "player", 
                "text": "No importa de dónde vengas, no permitiré que causes daño.",
                "position": "left",
                "effect": "energy_surge"
            },
            {
                "speaker": "evil_clone",
                "text": "¡JAJAJA! ¡Tus palabras son tan vacías como tu destino!",
                "position": "right",
                "effect": "laugh"
            },
            {
                "speaker": "player",
                "text": "Mi destino lo forjo yo, no una copia imperfecta.",
                "position": "left",
                "effect": "determination"
            },
            {
                "speaker": "evil_clone",
                "text": "¿Imperfecta? ¡Yo soy la evolución! ¡La mejora!",
                "position": "right",
                "effect": "transform"
            },
            {
                "speaker": "player",
                "text": "Eres un error que debo corregir... ¡Prepárate!",
                "position": "left",
                "effect": "final_stand"
            },
            {
                "speaker": "both",
                "text": "¡QUE COMIENCE LA BATALLA FINAL!",
                "position": "center",
                "effect": "clash"
            }
        ]
        self.text_speed = 30
        self.current_char = 0
        self.text_timer = 0
        self.sound_played = False
        self.music_started = False
        self.text_complete = False
        self.can_advance = False
        self.effect_timer = 0
        self.current_effect = None

    def start_intro_music(self):
        if not self.music_started:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(intro_music)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                self.music_started = True
            except:
                print("No se pudo cargar la música de introducción")

    def stop_intro_music(self):
        pygame.mixer.music.stop()
        self.music_started = False

    def update(self, dt):
        current_dialogue = self.dialogues[self.current_dialogue]
        
        # Gestionar efectos especiales
        if current_dialogue.get("effect") and self.effect_timer == 0:
            self.current_effect = current_dialogue["effect"]
            self.effect_timer = 0.1
            
        if self.effect_timer > 0:
            self.effect_timer -= dt
        
        # Texto normal
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

    def draw_effect(self, surf, particle_system):
        if not self.current_effect or self.effect_timer <= 0:
            return
            
        effect_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        if self.current_effect == "lightning":
            for i in range(3):
                start_x = WIDTH - 100
                start_y = 100 + i * 80
                end_x = random.randint(200, WIDTH - 50)
                end_y = random.randint(50, HEIGHT - 50)
                particle_system.add_lightning(start_x, start_y, end_x, end_y, CYAN)
                
        elif self.current_effect == "glow":
            glow_radius = 150 + math.sin(pygame.time.get_ticks() * 0.01) * 20
            pygame.draw.circle(effect_surf, (255, 255, 100, 50), (150, HEIGHT//2), glow_radius)
            
        elif self.current_effect == "dark_aura":
            for i in range(3):
                radius = 120 + i * 30
                alpha = 100 - i * 30
                pulse = math.sin(pygame.time.get_ticks() * 0.005 + i) * 10
                pygame.draw.circle(effect_surf, (100, 0, 0, alpha), 
                                 (WIDTH - 200, HEIGHT//2), radius + pulse, 3)
                
        elif self.current_effect == "clash":
            center_x = WIDTH // 2
            wave_radius = 200 + math.sin(pygame.time.get_ticks() * 0.02) * 50
            for i in range(3):
                radius = wave_radius + i * 40
                alpha = 150 - i * 50
                pygame.draw.circle(effect_surf, (255, 100, 100, alpha), 
                                 (center_x, HEIGHT//2), radius, 5)
        
        surf.blit(effect_surf, (0, 0))

    def draw(self, surf, particle_system):
        surf.fill(BLACK)
        
        # Dibujar efecto especial primero
        self.draw_effect(surf, particle_system)
        
        # Marco decorativo con animación
        pulse = math.sin(pygame.time.get_ticks() * 0.003) * 2 + 2
        pygame.draw.rect(surf, BROWN, (20, 20, WIDTH-40, HEIGHT-40), int(2 + pulse), border_radius=10)
        pygame.draw.rect(surf, GOLD, (30, 30, WIDTH-60, HEIGHT-60), 2, border_radius=8)
        
        current_dialogue = self.dialogues[self.current_dialogue]
        
        # Dibujar personajes con efectos
        if current_dialogue["speaker"] == "evil_clone" or current_dialogue["speaker"] == "both":
            if has_evil_clone_img:
                char_x = WIDTH - 350
                char_y = HEIGHT//2 - 150
                
                breath = math.sin(pygame.time.get_ticks() * 0.004) * 3
                scaled_clone = pygame.transform.scale(evil_clone_img, 
                                                    (300 + int(breath), 300 + int(breath)))
                
                clone_colored = scaled_clone.copy()
                r = 220 + int(math.sin(pygame.time.get_ticks() * 0.005) * 35)
                g = 40 + int(math.sin(pygame.time.get_ticks() * 0.003) * 20)
                b = 40 + int(math.cos(pygame.time.get_ticks() * 0.004) * 20)
                clone_colored.fill((r, g, b, 255), special_flags=pygame.BLEND_RGBA_MULT)
                
                surf.blit(clone_colored, (char_x - breath//2, char_y - breath//2))
        
        if current_dialogue["speaker"] == "player" or current_dialogue["speaker"] == "both":
            if has_player_nave_img:
                char_x = 50
                char_y = HEIGHT//2 - 100
                
                pulse = math.sin(pygame.time.get_ticks() * 0.005) * 2
                scaled_player = pygame.transform.scale(player_nave_img, 
                                                     (200 + int(pulse), 200 + int(pulse)))
                
                player_colored = scaled_player.copy()
                r = 80 + int(math.sin(pygame.time.get_ticks() * 0.002) * 20)
                g = 160 + int(math.cos(pygame.time.get_ticks() * 0.003) * 40)
                b = 240 + int(math.sin(pygame.time.get_ticks() * 0.004) * 15)
                player_colored.fill((r, g, b, 255), special_flags=pygame.BLEND_RGBA_MULT)
                
                surf.blit(player_colored, (char_x - pulse//2, char_y - pulse//2))
        
        # Configurar posición del cuadro de diálogo según el hablante
        if current_dialogue["position"] == "left":
            dialog_rect = pygame.Rect(50, HEIGHT - 200, WIDTH//2 - 80, 150)
            name_x = dialog_rect.x + 20
            text_align = "left"
        elif current_dialogue["position"] == "right":
            dialog_rect = pygame.Rect(WIDTH//2 + 30, HEIGHT - 200, WIDTH//2 - 80, 150)
            name_x = dialog_rect.x + 20
            text_align = "left"
        else:  # center
            dialog_rect = pygame.Rect(WIDTH//4, HEIGHT - 200, WIDTH//2, 150)
            name_x = dialog_rect.centerx
            text_align = "center"
        
        # Dibujar cuadro de diálogo
        pygame.draw.rect(surf, (30, 30, 50), dialog_rect, border_radius=15)
        pygame.draw.rect(surf, PURPLE, dialog_rect, 3, border_radius=15)
        
        # Nombre del personaje que habla
        speaker_names = {
            "evil_clone": "CLON MALVADO",
            "player": "TU NAVE",
            "both": "ENFRENTAMIENTO"
        }
        
        name_colors = {
            "evil_clone": RED,
            "player": BLUE, 
            "both": PURPLE
        }
        
        name_text = title_font.render(speaker_names[current_dialogue["speaker"]], True, name_colors[current_dialogue["speaker"]])
        if text_align == "center":
            surf.blit(name_text, (name_x - name_text.get_width()//2, dialog_rect.y + 15))
        else:
            surf.blit(name_text, (name_x, dialog_rect.y + 15))
        
        # Texto del diálogo actual
        current_text = current_dialogue["text"][:self.current_char]
        
        # Formatear texto para múltiples líneas
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
                if text_align == "center":
                    surf.blit(line_surface, (dialog_rect.centerx - line_surface.get_width()//2, text_y))
                else:
                    surf.blit(line_surface, (dialog_rect.x + 20, text_y))
                text_y += 35
        
        # Indicador de continuación (solo cuando el texto esté completo)
        if self.can_advance:
            prompt_text = "Presiona X para continuar" if self.current_dialogue < len(self.dialogues) - 1 else "Presiona X para comenzar la batalla"
            prompt = dialogue_font.render(prompt_text, True, GREEN)
            
            if text_align == "center":
                prompt_x = dialog_rect.centerx - prompt.get_width()//2
            else:
                prompt_x = dialog_rect.x + 20
            
            surf.blit(prompt, (prompt_x, dialog_rect.bottom - 40))
            
            # Triángulo parpadeante
            if pygame.time.get_ticks() % 800 < 400:
                if text_align == "center":
                    triangle_x = dialog_rect.centerx + prompt.get_width()//2 + 20
                else:
                    triangle_x = prompt_x + prompt.get_width() + 20
                
                triangle_points = [
                    (triangle_x, dialog_rect.bottom - 25),
                    (triangle_x + 20, dialog_rect.bottom - 25),
                    (triangle_x + 10, dialog_rect.bottom - 5)
                ]
                pygame.draw.polygon(surf, YELLOW, triangle_points)
        else:
            # Puntos suspensivos mientras se escribe
            if pygame.time.get_ticks() % 600 < 300:
                dots_text = dialogue_font.render("...", True, YELLOW)
                if text_align == "center":
                    surf.blit(dots_text, (dialog_rect.centerx - dots_text.get_width()//2, dialog_rect.bottom - 40))
                else:
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
        surf.fill(BLACK)
        
        title_surface = title_font.render("NIVEL 5", True, GOLD)
        title_surface.set_alpha(self.alpha)
        surf.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, HEIGHT//2 - 100))
        
        subtitle_surface = dialogue_font.render("Mi Clon Malvado", True, RED)
        subtitle_surface.set_alpha(self.alpha)
        surf.blit(subtitle_surface, (WIDTH//2 - subtitle_surface.get_width()//2, HEIGHT//2 - 20))
        
        if self.phase in [0, 1, 2]:
            for i in range(20):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                size = random.randint(1, 3)
                brightness = random.randint(100, 255)
                pygame.draw.circle(surf, (brightness, brightness, brightness), (x, y), size)
        
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill(BLACK)
            fade_surface.set_alpha(self.fade_alpha)
            surf.blit(fade_surface, (0, 0))

# --- Efecto de Knockout ---
class KnockoutEffect:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.duration = 3.0
        self.alpha = 0
        self.scale = 0.1
        self.sound_played = False

    def activate(self):
        self.active = True
        self.timer = 0
        self.alpha = 0
        self.scale = 0.1
        self.sound_played = False
        if has_knockout_sound:
            sonido_knockout.play()

    def update(self, dt):
        if not self.active:
            return False
            
        self.timer += dt
        progress = min(1.0, self.timer / self.duration)
        
        if progress < 0.4:
            self.alpha = int(progress / 0.4 * 255)
            self.scale = 0.1 + (1.0 - 0.1) * (progress / 0.4)
        elif progress < 0.8:
            self.alpha = 255
            self.scale = 1.0
        else:
            self.alpha = int((1.0 - (progress - 0.8) / 0.2) * 255)
            self.scale = 1.0
            
        if progress >= 1.0:
            self.active = False
            return True
        return False

    def draw(self, surf):
        if not self.active:
            return
            
        effect_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
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
            ok_text.set_alpha(self.alpha)
            ok_rect = ok_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
            effect_surface.blit(ok_text, ok_rect)
            
            ko_font = pygame.font.SysFont("Arial", int(40 * self.scale))
            ko_text = ko_font.render("KNOCKOUT!", True, (255, 50, 50))
            ko_text.set_alpha(self.alpha)
            ko_rect = ko_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            effect_surface.blit(ko_text, ko_rect)
        
        surf.blit(effect_surface, (0, 0))

# --- Sistema de Victoria con Diálogos ---
class VictorySystem:
    def __init__(self):
        self.active = False
        self.current_dialogue = 0
        self.dialogues = [
            {
                "speaker": "evil_clone",
                "text": "¡No puede ser! ¿Cómo he podido perder?",
                "position": "right"
            },
            {
                "speaker": "player", 
                "text": "¿Lo ves? Solo eras una copia imperfecta.",
                "position": "left"
            },
            {
                "speaker": "evil_clone",
                "text": "Pero... yo era más fuerte, más poderoso...",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "La fuerza no lo es todo. Tengo algo que tú nunca tuviste.",
                "position": "left"
            },
            {
                "speaker": "evil_clone", 
                "text": "¿Qué? ¿De qué hablas?",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "Tengo amigos que proteger, una razón para luchar.",
                "position": "left"
            },
            {
                "speaker": "evil_clone",
                "text": "Amigos... esa debilidad...",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "No, es mi fuerza. Y ahora no perderé más tiempo contigo.",
                "position": "left"
            },
            {
                "speaker": "player",
                "text": "Tengo que rescatar a mi amigo. ¡Se acabó!",
                "position": "left"
            }
        ]
        self.text_speed = 30
        self.current_char = 0
        self.text_timer = 0
        self.sound_played = False
        self.text_complete = False
        self.can_advance = False
        self.ok_timer = 0
        self.ok_duration = 3.0
        self.show_ok = True
        self.fade_alpha = 0
        self.fade_duration = 2.0
        self.fade_timer = 0
        self.all_dialogues_complete = False

    def activate(self):
        self.active = True
        self.current_dialogue = 0
        self.current_char = 0
        self.text_timer = 0
        self.sound_played = False
        self.text_complete = False
        self.can_advance = False
        self.ok_timer = 0
        self.show_ok = True
        self.fade_alpha = 0
        self.fade_timer = 0
        self.all_dialogues_complete = False

    def update(self, dt):
        if not self.active:
            return False
            
        if self.show_ok:
            self.ok_timer += dt
            if self.ok_timer >= self.ok_duration:
                self.show_ok = False
                self.ok_timer = 0
            return False
            
        if self.all_dialogues_complete:
            self.fade_timer += dt
            self.fade_alpha = min(255, int((self.fade_timer / self.fade_duration) * 255))
            if self.fade_alpha >= 255:
                self.active = False
                return True
            return False
            
        if self.current_dialogue >= len(self.dialogues):
            self.all_dialogues_complete = True
            self.fade_timer = 0
            return False
            
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
                    
        return False

    def advance_text(self):
        if not self.can_advance:
            return False
            
        sonido_texto.play()
        
        self.current_dialogue += 1
        self.current_char = 0
        self.text_timer = 0
        self.text_complete = False
        self.can_advance = False
        self.sound_played = False
        
        if self.current_dialogue >= len(self.dialogues):
            self.all_dialogues_complete = True
            self.fade_timer = 0
            return True
            
        return False

    def draw(self, surf):
        if not self.active:
            return
            
        if self.show_ok:
            effect_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            if has_ok_image:
                ok_rect = ok_image.get_rect(center=(WIDTH//2, HEIGHT//2))
                effect_surface.blit(ok_image, ok_rect)
            else:
                ok_font = pygame.font.SysFont("Arial", 80)
                ok_text = ok_font.render("OK", True, (255, 255, 0))
                ok_rect = ok_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
                effect_surface.blit(ok_text, ok_rect)
                
                ko_font = pygame.font.SysFont("Arial", 40)
                ko_text = ko_font.render("KNOCKOUT!", True, (255, 50, 50))
                ko_rect = ko_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
                effect_surface.blit(ko_text, ko_rect)
            
            surf.blit(effect_surface, (0, 0))
        elif self.all_dialogues_complete:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill(BLACK)
            fade_surface.set_alpha(self.fade_alpha)
            surf.blit(fade_surface, (0, 0))
        else:
            surf.fill(BLACK)
            
            pygame.draw.rect(surf, BROWN, (20, 20, WIDTH-40, HEIGHT-40), 4, border_radius=10)
            pygame.draw.rect(surf, GOLD, (30, 30, WIDTH-60, HEIGHT-60), 2, border_radius=8)
            
            if self.current_dialogue < len(self.dialogues):
                current_dialogue = self.dialogues[self.current_dialogue]
                
                if current_dialogue["speaker"] == "evil_clone":
                    if has_evil_clone_img:
                        char_x = WIDTH - 350
                        char_y = HEIGHT//2 - 150
                        clone_colored = evil_clone_img.copy()
                        clone_colored.fill((150, 0, 0, 180), special_flags=pygame.BLEND_RGBA_MULT)
                        surf.blit(clone_colored, (char_x, char_y))
                
                if current_dialogue["speaker"] == "player":
                    if has_player_nave_img:
                        char_x = 50
                        char_y = HEIGHT//2 - 100
                        surf.blit(player_nave_img, (char_x, char_y))
                
                if current_dialogue["position"] == "left":
                    dialog_rect = pygame.Rect(50, HEIGHT - 200, WIDTH//2 - 80, 150)
                    name_x = dialog_rect.x + 20
                    text_align = "left"
                else:
                    dialog_rect = pygame.Rect(WIDTH//2 + 30, HEIGHT - 200, WIDTH//2 - 80, 150)
                    name_x = dialog_rect.x + 20
                    text_align = "left"
                
                pygame.draw.rect(surf, (30, 30, 50), dialog_rect, border_radius=15)
                pygame.draw.rect(surf, PURPLE, dialog_rect, 3, border_radius=15)
                
                speaker_names = {
                    "evil_clone": "CLON MALVADO",
                    "player": "TU NAVE"
                }
                
                name_colors = {
                    "evil_clone": RED,
                    "player": BLUE
                }
                
                name_text = title_font.render(speaker_names[current_dialogue["speaker"]], True, name_colors[current_dialogue["speaker"]])
                surf.blit(name_text, (name_x, dialog_rect.y + 15))
                
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
                        if text_align == "center":
                            surf.blit(line_surface, (dialog_rect.centerx - line_surface.get_width()//2, text_y))
                        else:
                            surf.blit(line_surface, (dialog_rect.x + 20, text_y))
                        text_y += 35
                
                if self.can_advance:
                    prompt_text = "Presiona X para continuar"
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

# --- Clases para obstáculos y efectos ---
class Obstacle:
    def __init__(self, x, y, obstacle_type="meteor"):
        self.x = x
        self.y = y
        self.type = obstacle_type
        self.speed = random.uniform(150, 300)
        self.size = random.randint(20, 40)
        self.color = RED if obstacle_type == "meteor" else ORANGE
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)
        self.trail_particles = []

    def update(self, dt):
        self.y += self.speed * dt
        self.rotation += self.rotation_speed
        self.rect.topleft = (int(self.x), int(self.y))
        
        # Añadir partículas de estela
        if random.random() < 0.3:
            self.trail_particles.append({
                'x': self.x + self.size//2,
                'y': self.y + self.size,
                'size': random.uniform(2, 4),
                'life': 0.5
            })
        
        # Actualizar partículas
        for particle in self.trail_particles[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)

    def draw(self, surf):
        # Dibujar estela
        for particle in self.trail_particles:
            alpha = int(255 * (particle['life'] / 0.5))
            size = int(particle['size'] * (particle['life'] / 0.5))
            if size > 0:
                trail_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surf, (255, 100, 50, alpha), (size, size), size)
                surf.blit(trail_surf, (int(particle['x'] - size), int(particle['y'] - size)))
        
        meteor_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(meteor_surface, self.color, (self.size//2, self.size//2), self.size//2)
        pygame.draw.circle(meteor_surface, YELLOW, (self.size//2, self.size//2), self.size//4)
        
        rotated_meteor = pygame.transform.rotate(meteor_surface, self.rotation)
        new_rect = rotated_meteor.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
        surf.blit(rotated_meteor, new_rect.topleft)

class CameraEffect:
    def __init__(self):
        self.zoom_active = False
        self.zoom_timer = 0
        self.zoom_duration = 8.0
        self.zoom_level = 1.0
        self.target_zoom = 0.7
        self.shake_intensity = 0
        self.shake_timer = 0
        self.earthquake_active = False
        self.earthquake_timer = 0
        self.earthquake_duration = 5.0
        self.earthquake_intensity = 15
        self.returning_from_zoom = False
        self.return_timer = 0
        self.return_duration = 1.5

    def start_zoom_out(self):
        self.zoom_active = True
        self.zoom_timer = 0
        self.returning_from_zoom = False
        self.shake_intensity = 5
        self.shake_timer = 1.0

    def start_earthquake(self):
        self.earthquake_active = True
        self.earthquake_timer = 0
        self.shake_intensity = self.earthquake_intensity
        sonido_terremoto.play()

    def update(self, dt):
        if self.earthquake_active:
            self.earthquake_timer += dt
            self.shake_intensity = self.earthquake_intensity * (1 - (self.earthquake_timer / self.earthquake_duration))
            
            if self.earthquake_timer >= self.earthquake_duration:
                self.earthquake_active = False
                self.shake_intensity = 0
        
        if self.zoom_active:
            self.zoom_timer += dt
            
            if not self.returning_from_zoom:
                if self.zoom_timer < self.zoom_duration:
                    progress = min(1.0, self.zoom_timer / 1.0)
                    self.zoom_level = 1.0 + (self.target_zoom - 1.0) * progress
                else:
                    self.returning_from_zoom = True
                    self.return_timer = 0
            else:
                self.return_timer += dt
                return_progress = min(1.0, self.return_timer / self.return_duration)
                self.zoom_level = self.target_zoom + (1.0 - self.target_zoom) * return_progress
                
                if return_progress >= 1.0:
                    self.zoom_active = False
                    self.returning_from_zoom = False
                    self.zoom_level = 1.0
                    self.shake_intensity = 0
            
            if self.shake_timer > 0:
                self.shake_timer -= dt
                if not self.earthquake_active:
                    self.shake_intensity = max(0, self.shake_intensity - dt * 5)
        else:
            self.zoom_level = 1.0
            if not self.earthquake_active:
                self.shake_intensity = 0

    def get_offset(self):
        if self.shake_intensity > 0:
            return (random.uniform(-self.shake_intensity, self.shake_intensity),
                    random.uniform(-self.shake_intensity, self.shake_intensity))
        return (0, 0)

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
        self.trail_particles = []

    def update(self, dt, keys, particle_system):
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

        old_x, old_y = self.x, self.y
        self.x += vx * speed
        self.y += vy * speed

        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))

        # Añadir partículas de estela al moverse
        if (vx != 0 or vy != 0) and random.random() < 0.3:
            particle_system.add_trail(self.x + self.size//2, self.y + self.size//2, BLUE, 1)

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
            
        # Efecto de brillo cuando es invencible por victoria
        if self.victory_invincible:
            glow_alpha = int((math.sin(pygame.time.get_ticks() * 0.01) * 0.5 + 0.5) * 100)
            glow_surf = pygame.Surface((self.size + 10, self.size + 10), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 100, glow_alpha), 
                             (self.size//2 + 5, self.size//2 + 5), self.size//2 + 5)
            surf.blit(glow_surf, (self.x - 5, self.y - 5))
        
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

    def take_damage(self, particle_system, screen_effects):
        if self.victory_invincible:
            return
            
        if not self.invulnerable:
            self.lives -= 1
            self.damage_taken += 1
            sonido_daño.play()
            self.invulnerable = True
            self.invulnerable_timer = 2.0
            self.x = max(0, self.x - 40)
            
            # Efectos de daño
            particle_system.add_explosion(self.x + self.size//2, self.y + self.size//2, RED, 15, 80)
            screen_effects.screen_flash(RED, 0.2)
            screen_effects.screen_shake(8, 0.3)

    def activate_victory_invincibility(self, duration=10.0):
        self.victory_invincible = True
        self.victory_invincible_timer = duration

    def activate(self):
        self.active = True

# --- NUEVO: Bullets con Mejores Efectos ---
class AnimatedBullet:
    def __init__(self, x, y, vx, vy, color=YELLOW, owner="player", damage=10, trail_color=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 6 if owner == "player" else 8
        self.color = color
        self.owner = owner
        self.damage = damage
        self.rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)
        self.trail = []
        self.trail_color = trail_color or color
        self.glow_timer = 0
        
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))
        
        # Añadir partícula de estela
        self.trail.append({
            'x': self.x, 
            'y': self.y, 
            'life': 0.3,
            'size': self.radius * 0.8
        })
        
        # Actualizar estela
        for particle in self.trail[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.trail.remove(particle)
                
        self.glow_timer += dt * 10
        
    def draw(self, surf):
        # Dibujar estela
        for particle in self.trail:
            alpha = int(255 * (particle['life'] / 0.3))
            size = int(particle['size'] * (particle['life'] / 0.3))
            if size > 0:
                trail_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                trail_color = list(self.trail_color)
                trail_color.append(alpha)
                pygame.draw.circle(trail_surf, trail_color, (size, size), size)
                surf.blit(trail_surf, (int(particle['x'] - size), int(particle['y'] - size)))
        
        # Dibujar bala con efecto de brillo
        glow = math.sin(self.glow_timer) * 0.2 + 0.8
        current_radius = int(self.radius * glow)
        
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), current_radius)
        
        # Núcleo brillante
        core_color = WHITE
        pygame.draw.circle(surf, core_color, (int(self.x), int(self.y)), current_radius // 2)

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
        self.glow_timer = 0

    def update(self, dt):
        self.x += self.speed * dt
        
        # Partículas de estela mejoradas
        if random.random() < 0.7:
            self.trail_particles.append({
                'x': self.x - 10,
                'y': self.y + random.uniform(-5, 5),
                'size': random.randint(3, 6),
                'life': 1.0,
                'color': random.choice([PURPLE, (255, 100, 255), (200, 80, 255)])
            })
        
        for particle in self.trail_particles[:]:
            particle['life'] -= dt * 2
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
                
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))
        self.glow_timer += dt * 8

    def draw(self, surf):
        # Dibujar estela
        for particle in self.trail_particles:
            alpha = int(particle['life'] * 255)
            size = int(particle['size'] * particle['life'])
            if size > 0:
                particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                color = list(particle['color'])
                color.append(alpha)
                pygame.draw.circle(particle_surf, color, (size, size), size)
                surf.blit(particle_surf, (int(particle['x'] - size), int(particle['y'] - size)))
        
        # Misil con efecto de pulso
        glow = (math.sin(self.glow_timer) * 0.3 + 0.7)
        current_radius = int(self.radius * glow)
        
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), current_radius)
        
        # Núcleo brillante
        core_glow = (math.sin(self.glow_timer + 1) * 0.2 + 0.8)
        core_radius = int(current_radius * 0.6 * core_glow)
        pygame.draw.circle(surf, YELLOW, (int(self.x), int(self.y)), core_radius)
        
        # Destello frontal
        flash_radius = int(4 * (math.sin(self.glow_timer * 2) * 0.5 + 0.5))
        pygame.draw.circle(surf, WHITE, (int(self.x + 8), int(self.y)), flash_radius)

# --- MODIFICADO: EvilClone con Mejores Efectos ---
class EvilClone:
    def __init__(self):
        self.w = 120
        self.h = 120
        self.x = WIDTH + 200
        self.y = HEIGHT // 3
        self.max_hp = 8000
        self.hp = self.max_hp
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.attack_timer = 2.0
        self.attack_cooldown = 1.5
        self.entering = True
        self.exiting = False
        self.active = True
        self.phase = 1
        self.move_timer = 0
        self.move_direction = 1
        self.phase_change_timer = 0
        self.earthquake_cooldown = 0
        self.earthquake_interval = 10.0
        
        self.phase_attack_cooldowns = [1.5, 1.0, 0.7]
        self.phase_move_speeds = [80, 150, 200]
        
        self.color = RED
        self.bullet_color = ORANGE
        self.rain_active = False
        self.rain_timer = 0
        self.rain_duration = 8.0
        
        # NUEVO: Efectos visuales
        self.damage_flash = 0
        self.aura_particles = []
        self.phase_transition_effect = 0

    def update_phase(self):
        hp_percentage = self.hp / self.max_hp
        
        if hp_percentage > 0.66:
            new_phase = 1
        elif hp_percentage > 0.33:
            new_phase = 2
        else:
            new_phase = 3
            
        if new_phase != self.phase:
            self.phase = new_phase
            self.attack_cooldown = self.phase_attack_cooldowns[self.phase - 1]
            self.phase_transition_effect = 1.0
            return True
        return False

    def update(self, dt, enemy_bullets, player, obstacles, camera_effect, particle_system, screen_effects):
        if self.entering:
            self.x -= 200 * dt
            if self.x <= WIDTH - self.w - 100:
                self.entering = False
                screen_effects.screen_flash(RED, 0.3)
                screen_effects.screen_shake(15, 0.5)
                particle_system.add_explosion(self.x + self.w//2, self.y + self.h//2, RED, 30, 150)
            self.rect.topleft = (int(self.x), int(self.y))
            return
            
        if self.exiting:
            self.x += 300 * dt
            self.rect.topleft = (int(self.x), int(self.y))
            return

        if not self.active:
            return

        if self.damage_flash > 0:
            self.damage_flash -= dt
            
        if self.phase_transition_effect > 0:
            self.phase_transition_effect -= dt
            if self.phase_transition_effect <= 0:
                screen_effects.screen_shake(20, 0.8)
                particle_system.add_explosion(self.x + self.w//2, self.y + self.h//2, PURPLE, 30, 200)

        phase_changed = self.update_phase()
        if phase_changed:
            sonido_fase.play()
            screen_effects.screen_flash(PURPLE, 0.4)
            screen_effects.screen_shake(25, 1.0)

        if self.phase == 2:
            self.earthquake_cooldown -= dt
            if self.earthquake_cooldown <= 0 and not camera_effect.earthquake_active:
                camera_effect.start_earthquake()
                self.earthquake_cooldown = self.earthquake_interval
                particle_system.add_explosion(WIDTH//2, HEIGHT//2, ORANGE, 50, 100)

        if self.rain_active:
            self.rain_timer -= dt
            if random.random() < 0.3:
                obstacles.append(Obstacle(
                    random.randint(100, WIDTH - 100),
                    random.randint(-100, -20)
                ))
            
            if self.rain_timer <= 0:
                self.rain_active = False

        self.move_timer += dt
        move_speed = self.phase_move_speeds[self.phase - 1]
        
        if self.phase == 1:
            if self.move_timer >= 1.0:
                self.move_timer = 0
                self.move_direction *= -1
            
            self.y += self.move_direction * move_speed * dt
            self.y = max(HEIGHT//4, min(HEIGHT//2, self.y))
                
        elif self.phase == 2:
            if self.move_timer >= 0.5:
                self.move_timer = 0
                self.move_direction = random.choice([-1, 1])
            
            if camera_effect.earthquake_active:
                self.y += self.move_direction * move_speed * 1.5 * dt
            else:
                self.y += self.move_direction * move_speed * dt
            self.y = max(HEIGHT//5, min(HEIGHT//1.7, self.y))
                
        elif self.phase == 3:
            if self.move_timer >= 0.3:
                self.move_timer = 0
                self.move_direction = random.choice([-1, 1])
            
            wave_movement = math.sin(pygame.time.get_ticks() * 0.01) * 50
            self.y += self.move_direction * move_speed * dt + wave_movement * dt
            self.y = max(HEIGHT//6, min(HEIGHT//1.5, self.y))

        self.attack_timer -= dt
        if self.attack_timer <= 0:
            self.attack_timer = self.attack_cooldown
            
            if self.phase == 1:
                self.attack_phase1(enemy_bullets, particle_system)
            elif self.phase == 2:
                self.attack_phase2(enemy_bullets, player, camera_effect, particle_system)
            elif self.phase == 3:
                self.attack_phase3(enemy_bullets, player, obstacles, camera_effect, particle_system, screen_effects)

        # Añadir partículas de aura continuas
        if random.random() < 0.3:
            particle_system.add_energy_glow(
                self.x + random.randint(0, self.w),
                self.y + random.randint(0, self.h),
                RED if self.phase == 1 else PURPLE if self.phase == 2 else DARK_RED,
                random.randint(1, 3)
            )

        self.rect.topleft = (int(self.x), int(self.y))

    def attack_phase1(self, enemy_bullets, particle_system):
        base_y = self.y + self.h
        for i in range(5):
            offset = math.sin(pygame.time.get_ticks() * 0.01 + i) * 30
            bullet = AnimatedBullet(
                self.x + self.w//2, base_y + offset,
                -350, 200,
                color=self.bullet_color, owner="boss", damage=15,
                trail_color=ORANGE
            )
            enemy_bullets.append(bullet)
            particle_system.add_sparkle(bullet.x, bullet.y, YELLOW, 2)

    def attack_phase2(self, enemy_bullets, player, camera_effect, particle_system):
        if camera_effect.earthquake_active:
            for i in range(12):
                angle = math.radians(i * 30)
                bullet = AnimatedBullet(
                    self.x + self.w//2, self.y + self.h//2,
                    math.cos(angle) * 300, math.sin(angle) * 300,
                    color=self.bullet_color, owner="boss", damage=25,
                    trail_color=RED
                )
                enemy_bullets.append(bullet)
            particle_system.add_explosion(self.x + self.w//2, self.y + self.h//2, RED, 20, 100)
        else:
            for angle in range(-45, 46, 15):
                rad = math.radians(angle)
                bullet = AnimatedBullet(
                    self.x + self.w//2, self.y + self.h,
                    -350 * math.cos(rad), 250 * math.sin(rad),
                    color=self.bullet_color, owner="boss", damage=20,
                    trail_color=ORANGE
                )
                enemy_bullets.append(bullet)

    def attack_phase3(self, enemy_bullets, player, obstacles, camera_effect, particle_system, screen_effects):
        attack_type = random.choice(["rain", "circle", "targeted", "spiral"])
        
        if attack_type == "rain":
            if not camera_effect.zoom_active:
                camera_effect.start_zoom_out()
                self.rain_active = True
                self.rain_timer = self.rain_duration
                screen_effects.screen_shake(10, 0.5)
                particle_system.add_explosion(WIDTH//2, 50, ORANGE, 25, 80)
                for i in range(10):
                    obstacles.append(Obstacle(
                        random.randint(100, WIDTH - 100),
                        random.randint(-100, -20)
                    ))
                    
        elif attack_type == "circle":
            particle_system.add_explosion(self.x + self.w//2, self.y + self.h//2, PURPLE, 30, 120)
            for i in range(16):
                angle = math.radians(i * 22.5)
                bullet = AnimatedBullet(
                    self.x + self.w//2, self.y + self.h//2,
                    math.cos(angle) * 250, math.sin(angle) * 250,
                    color=self.bullet_color, owner="boss", damage=30,
                    trail_color=PURPLE
                )
                enemy_bullets.append(bullet)
                
        elif attack_type == "targeted":
            screen_effects.add_chromatic_aberration(5)
            for i in range(10):
                angle_offset = random.uniform(-0.5, 0.5)
                dx = player.x - self.x
                dy = player.y - self.y
                dist = math.hypot(dx, dy) or 1
                bullet = AnimatedBullet(
                    self.x + self.w//2, self.y + self.h//2,
                    (dx/dist + angle_offset) * 400, (dy/dist + angle_offset) * 400,
                    color=self.bullet_color, owner="boss", damage=35,
                    trail_color=RED
                )
                enemy_bullets.append(bullet)
                
        elif attack_type == "spiral":
            time_factor = pygame.time.get_ticks() * 0.005
            particle_system.add_energy_glow(self.x + self.w//2, self.y + self.h//2, PURPLE, 15)
            for i in range(8):
                angle = math.radians(i * 45 + time_factor * 50)
                radius = 100 + math.sin(time_factor) * 50
                bullet = AnimatedBullet(
                    self.x + self.w//2 + math.cos(angle) * radius,
                    self.y + self.h//2 + math.sin(angle) * radius,
                    math.cos(angle) * 200, math.sin(angle) * 200,
                    color=self.bullet_color, owner="boss", damage=30,
                    trail_color=CYAN
                )
                enemy_bullets.append(bullet)

    def take_damage(self, damage, particle_system, screen_effects):
        self.hp -= damage
        self.damage_flash = 0.1
        particle_system.add_explosion(
            self.x + random.randint(0, self.w),
            self.y + random.randint(0, self.h),
            ORANGE, 8, 60
        )
        screen_effects.screen_shake(5, 0.2)
        return self.hp <= 0

    def start_exit(self):
        self.exiting = True
        self.active = False

    def draw(self, surf):
        if not self.active and self.exiting:
            return
            
        # Efecto de daño (flash blanco)
        if self.damage_flash > 0:
            flash_surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, 150))
            surf.blit(flash_surf, (self.x, self.y))
            
        # Efecto de transición de fase
        if self.phase_transition_effect > 0:
            transition_alpha = int(200 * self.phase_transition_effect)
            transition_surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            transition_color = PURPLE if self.phase == 2 else DARK_RED if self.phase == 3 else RED
            transition_surf.fill((*transition_color, transition_alpha))
            surf.blit(transition_surf, (self.x, self.y))

        phase_colors = [RED, DARK_RED, PURPLE]
        current_color = phase_colors[self.phase - 1]
            
        boss_colored = boss_img.copy()
        
        # Efecto de pulso según la fase
        pulse = math.sin(pygame.time.get_ticks() * 0.005 * self.phase) * 0.1 + 0.9
        boss_colored.fill((*current_color, int(255 * pulse)), special_flags=pygame.BLEND_RGBA_MULT)
        surf.blit(boss_colored, (self.x, self.y))
        
        # Barra de vida con efectos
        bar_width = 200
        bar_height = 15
        bar_x = self.x + self.w//2 - bar_width//2
        bar_y = self.y - 25
        
        # Fondo de la barra con efecto de glow
        pygame.draw.rect(surf, (30, 30, 30), (bar_x-2, bar_y-2, bar_width+4, bar_height+4), border_radius=8)
        pygame.draw.rect(surf, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height), border_radius=6)
        
        hp_fraction = max(0, self.hp / self.max_hp)
        health_width = int(bar_width * hp_fraction)
        
        # Barra de vida con gradiente
        if health_width > 0:
            health_surf = pygame.Surface((health_width, bar_height), pygame.SRCALPHA)
            for i in range(health_width):
                progress = i / health_width
                r = int(255 * (1 - progress) + current_color[0] * progress)
                g = int(100 * progress)
                b = int(current_color[2] * progress)
                pygame.draw.line(health_surf, (r, g, b), (i, 0), (i, bar_height))
            health_surf.set_alpha(200)
            surf.blit(health_surf, (bar_x, bar_y))
        
        # Borde brillante
        pygame.draw.rect(surf, current_color, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=6)
        
        names = ["Clon Malvado", "Clon Enfurecido", "Forma Final"]
        name_text = font.render(f"{names[self.phase-1]}: {self.hp}/{self.max_hp}", True, WHITE)
        surf.blit(name_text, (bar_x, bar_y - 20))

# --- Sistema de UI para Energía ---
class EnergyUI:
    def __init__(self):
        self.bar_width = 300
        self.bar_height = 20
        self.x = WIDTH - self.bar_width - 20
        self.y = 15
        self.pulse_timer = 0

    def draw(self, surf, player):
        self.pulse_timer += 0.05
        
        pygame.draw.rect(surf, (50, 50, 50), (self.x, self.y, self.bar_width, self.bar_height), border_radius=10)
        
        energy_ratio = player.energy / player.max_energy
        energy_width = int(self.bar_width * energy_ratio)
        
        if energy_ratio >= 1.0:
            bar_color = PURPLE
            # Efecto de pulso cuando está llena
            pulse = (math.sin(self.pulse_timer) * 0.2 + 0.8)
            energy_width = int(self.bar_width * pulse)
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

# --- Sistema de Resultados ---
class ResultsSystem:
    def __init__(self):
        self.active = False
        self.grade = ""
        self.grade_color = WHITE
        self.motivational_phrase = ""
        
    def calculate_grade(self, continues_used, damage_taken, accuracy, completion_time):
        score = 100
        
        if continues_used > 0:
            score -= continues_used * 25
            
        if damage_taken > 0:
            score -= min(damage_taken * 5, 30)
            
        if accuracy < 0.6:
            score -= 10
            
        if completion_time > 180:
            score -= 10

        if score >= 95:
            return "A+", GOLD, "¡PERFECTO! Tu clon no era rival para ti"
        elif score >= 85:
            return "A", GREEN, "¡Excelente! Dominaste a tu clon malvado"
        elif score >= 75:
            return "B", BLUE, "¡Buen trabajo! Venciste a tu clon"
        elif score >= 60:
            return "C", YELLOW, "¡Bien hecho! Superaste el desafío"
        else:
            return "D", ORANGE, "¡Logrado! El clon ha caído"
            
    def show_results(self, player, continues_used, score, completion_time, boss_defeated):
        self.active = True
        
        accuracy = player.bullets_hit / player.bullets_shot if player.bullets_shot > 0 else 0
        
        self.grade, self.grade_color, self.motivational_phrase = self.calculate_grade(
            continues_used, player.damage_taken, accuracy, completion_time
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
        self.boss_defeated = boss_defeated
        
    def draw(self, surf):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surf.blit(overlay, (0, 0))
        
        title_text = title_font.render("¡VICTORIA! - NIVEL 5", True, GOLD)
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
            f"Clon malvado derrotado: {'Sí' if self.boss_defeated else 'No'}"
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

def play_victory_music():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(victory_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except:
        print("No se pudo cargar la música de victoria")

def play_normal_music():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sound/cosmo.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except:
        print("No se pudo cargar la música normal")

# --- Inicializar sistemas ---
player = Player()
player_bullets = []
enemy_bullets = []
missiles = []
obstacles = []
evil_clone = EvilClone()
title_screen = TitleScreen()
introduction = IntroductionSystem()
energy_ui = EnergyUI()
results_system = ResultsSystem()
camera_effect = CameraEffect()
knockout_effect = KnockoutEffect()
victory_system = VictorySystem()

# NUEVOS SISTEMAS
particle_system = ParticleSystem()
screen_effects = ScreenEffects()
transition_effects = TransitionEffects()

score = 0
game_over = False
level_cleared = False
fight_started = False
boss_defeated = 0
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

scroll_x = 0
vel_fondo = 100

saved_game_state = None

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
                    obstacles.clear()
                    player.x = 80
                    player.y = HEIGHT // 2
                    game_over = False
            if event.key == pygame.K_RETURN and results_system.active:
                running = False
                pygame.quit()
                try:
                    subprocess.run([sys.executable, "nivel6.py"])
                except:
                    print("No se pudo cargar el siguiente nivel")
                sys.exit()
            if event.key == pygame.K_x and introduction.active:
                result = introduction.advance_text()
                if result == "start_battle":
                    play_normal_music()
                    player.activate()
                    evil_clone.entering = True
                    fight_started = True
            if event.key == pygame.K_x and victory_system.active and victory_system.can_advance:
                victory_system.advance_text()

    keys = pygame.key.get_pressed()

    # Actualizar nuevos sistemas
    particle_system.update(dt)
    screen_effects.update(dt)
    transition_effects.update(dt)

    # Pantalla de título
    if title_screen.active:
        if title_screen.update(dt):
            introduction.start_intro_music()
        title_screen.draw(screen)
        pygame.display.flip()
        continue

    # Sistema de introducción
    if introduction.active:
        introduction.update(dt)
        introduction.draw(screen, particle_system)
        pygame.display.flip()
        continue

    # Sistema de victoria
    if victory_system.active:
        victory_finished = victory_system.update(dt)
        if victory_finished:
            victory_system.active = False
            results_system.show_results(player, continues_used, score, completion_time, boss_defeated)
        victory_system.draw(screen)
        pygame.display.flip()
        continue

    # Sistema de resultados
    if results_system.active:
        results_system.draw(screen)
        pygame.display.flip()
        continue

    # Efecto de knockout
    if knockout_effect.active:
        knockout_finished = knockout_effect.update(dt)
        if knockout_finished:
            knockout_effect.active = False
            victory_system.activate()

    # Juego principal (batalla)
    if not game_over and not level_cleared and fight_started and not victory_system.active:
        player.update(dt, keys, particle_system)
        camera_effect.update(dt)

        # Disparar balas normales
        if keys[pygame.K_x] and player.can_shoot():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            bullet = AnimatedBullet(bx, by, 600, 0, color=GREEN, owner="player", trail_color=CYAN)
            player_bullets.append(bullet)
            player.shoot()
            particle_system.add_sparkle(bx, by, GREEN, 2)

        # Lanzar misil
        if keys[pygame.K_z] and player.can_launch_missile():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            missile = Missile(bx, by)
            missiles.append(missile)
            player.launch_missile()
            screen_effects.screen_shake(5, 0.2)

        # Actualizar clon malvado
        if evil_clone.active or evil_clone.entering or evil_clone.exiting:
            evil_clone.update(dt, enemy_bullets, player, obstacles, camera_effect, particle_system, screen_effects)

        # Actualizar obstáculos
        for obstacle in obstacles[:]:
            obstacle.update(dt)
            if obstacle.y > HEIGHT + 50:
                obstacles.remove(obstacle)
                continue
            if player.rect.colliderect(obstacle.rect):
                player.take_damage(particle_system, screen_effects)
                if obstacle in obstacles:
                    obstacles.remove(obstacle)

        # Actualizar balas del jugador
        for b in player_bullets[:]:
            b.update(dt)
            if b.x > WIDTH + 50:
                player_bullets.remove(b)
                continue
            if evil_clone.active and rect_circle_collide(evil_clone.rect, b.x, b.y, b.radius):
                if evil_clone.take_damage(b.damage, particle_system, screen_effects):
                    evil_clone.start_exit()
                    boss_defeated = 1
                    score += 1000
                    player.add_energy(100)
                    player.activate_victory_invincibility(10.0)
                    if not knockout_shown:
                        knockout_effect.activate()
                        knockout_shown = True
                else:
                    player.add_energy(15)
                player.bullets_hit += 1
                particle_system.add_explosion(b.x, b.y, ORANGE, 10, 80)
                if b in player_bullets:
                    player_bullets.remove(b)

        # Actualizar misiles
        for m in missiles[:]:
            m.update(dt)
            if m.x > WIDTH + 50:
                missiles.remove(m)
                continue
            if evil_clone.active and rect_circle_collide(evil_clone.rect, m.x, m.y, m.radius):
                if evil_clone.take_damage(m.damage, particle_system, screen_effects):
                    evil_clone.start_exit()
                    boss_defeated = 1
                    score += 1000
                    player.add_energy(150)
                    player.activate_victory_invincibility(10.0)
                    if not knockout_shown:
                        knockout_effect.activate()
                        knockout_shown = True
                else:
                    player.add_energy(40)
                particle_system.add_explosion(m.x, m.y, PURPLE, 20, 120)
                screen_effects.screen_shake(10, 0.3)
                if m in missiles:
                    missiles.remove(m)

        # Actualizar balas enemigas
        for b in enemy_bullets[:]:
            b.update(dt)
            if b.x < -50 or b.y < -50 or b.y > HEIGHT + 50:
                enemy_bullets.remove(b)
                continue
            if rect_circle_collide(player.rect, b.x, b.y, b.radius):
                player.take_damage(particle_system, screen_effects)
                particle_system.add_explosion(b.x, b.y, RED, 8, 60)
                if b in enemy_bullets:
                    enemy_bullets.remove(b)

        # Verificar si el clon fue derrotado
        if boss_defeated >= 1 and not level_cleared and not knockout_effect.active and not victory_system.active:
            level_cleared = True
            completion_time = (pygame.time.get_ticks() - start_time) / 1000.0
            pygame.mixer.music.stop()
            if not victory_sound_played:
                sonido_victoria.play()
                victory_sound_played = True

        # Verificar game over
        if player.lives <= 0 and continue_available and continue_countdown == 0:
            continue_countdown = continue_time
            coins_inserted = 0
            saved_game_state = {
                'player_bullets': player_bullets[:],
                'enemy_bullets': enemy_bullets[:],
                'missiles': missiles[:],
                'obstacles': obstacles[:],
                'evil_clone_hp': evil_clone.hp,
                'evil_clone_phase': evil_clone.phase,
                'score': score,
                'player_energy': player.energy
            }

    # Actualizar conteo de continuación
    if continue_countdown > 0:
        continue_countdown -= dt
        if continue_countdown <= 0:
            continue_countdown = 0
            game_over = True

    # --- Dibujado con efectos de cámara ---
    screen.fill(BLACK)
    
    # Aplicar efectos de cámara
    zoom_surface = pygame.Surface((WIDTH, HEIGHT))
    zoom_surface.fill(BLACK)
    
    # Fondo con scroll y zoom
    scroll_x -= vel_fondo * dt
    if scroll_x <= -WIDTH:
        scroll_x = 0
    
    # Calcular transformaciones de cámara
    zoom_offset_x = (WIDTH - WIDTH * camera_effect.zoom_level) / 2
    zoom_offset_y = (HEIGHT - HEIGHT * camera_effect.zoom_level) / 2
    shake_offset = camera_effect.get_offset()
    
    # Añadir shake de efectos de pantalla
    screen_shake_offset = screen_effects.get_shake_offset()
    total_offset = (shake_offset[0] + screen_shake_offset[0], 
                   shake_offset[1] + screen_shake_offset[1])
    
    # Dibujar fondo con zoom
    scaled_bg = pygame.transform.scale(fondo_img, (int(WIDTH * camera_effect.zoom_level), 
                                                  int(HEIGHT * camera_effect.zoom_level)))
    for i in range(2):
        bg_x = int((scroll_x + i * WIDTH) * camera_effect.zoom_level + zoom_offset_x + total_offset[0])
        bg_y = int(zoom_offset_y + total_offset[1])
        zoom_surface.blit(scaled_bg, (bg_x, bg_y))

    # Dibujar todos los elementos en la superficie de zoom
    evil_clone.draw(zoom_surface)

    for b in player_bullets:
        b.draw(zoom_surface)
    for b in enemy_bullets:
        b.draw(zoom_surface)
    for m in missiles:
        m.draw(zoom_surface)
    for obstacle in obstacles:
        obstacle.draw(zoom_surface)

    if continue_countdown == 0:
        player.draw(zoom_surface)

    # Dibujar partículas en la superficie de zoom
    particle_system.draw(zoom_surface)

    # Aplicar la superficie zoomada a la pantalla principal
    screen.blit(zoom_surface, (0, 0))

    # Dibujar efecto de knockout (encima de todo)
    if knockout_effect.active:
        knockout_effect.draw(screen)

    # UI (sin efectos de cámara)
    energy_ui.draw(screen, player)
    
    lives_text = font.render(f"Vidas: {player.lives}", True, WHITE)
    screen.blit(lives_text, (12, 12))
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (12, 36))
    
    boss_text = font.render(f"Clon Malvado: {'Derrotado' if boss_defeated else 'Vivo'}", True, YELLOW)
    screen.blit(boss_text, (WIDTH//2 - boss_text.get_width()//2, 12))
    
    # Indicador de invencibilidad por victoria
    if player.victory_invincible:
        invincible_text = font.render("INVENCIBLE", True, PURPLE)
        screen.blit(invincible_text, (WIDTH//2 - invincible_text.get_width()//2, 40))
    
    # Indicador de fase y terremoto
    if fight_started and not level_cleared:
        phase_text = font.render(f"Fase: {evil_clone.phase}/3", True, PURPLE)
        screen.blit(phase_text, (WIDTH - 120, 60))
        
        if camera_effect.earthquake_active:
            quake_text = font.render("¡TERREMOTO!", True, RED)
            screen.blit(quake_text, (WIDTH//2 - quake_text.get_width()//2, HEIGHT - 40))
        
        if evil_clone.rain_active:
            rain_text = font.render("¡LLUVIA DE METEORITOS!", True, ORANGE)
            screen.blit(rain_text, (WIDTH//2 - rain_text.get_width()//2, HEIGHT - 70))

    # Aplicar efectos de pantalla
    if screen_effects.flash_alpha > 0:
        flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        flash_surf.fill(screen_effects.flash_color)
        flash_surf.set_alpha(screen_effects.flash_alpha)
        screen.blit(flash_surf, (0, 0))

    # Dibujar transiciones
    transition_effects.draw(screen)

    # Pantalla de continuación
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
        
        coins_text = font.render(f"Monedas insertadas: {coins_inserted}/1", True, YELLOW)
        screen.blit(coins_text, (WIDTH//2 - coins_text.get_width()//2, HEIGHT//2 + 60))
        
        lives_info = font.render(f"Cada moneda te da {lives_per_coin} vidas", True, GREEN)
        screen.blit(lives_info, (WIDTH//2 - lives_info.get_width()//2, HEIGHT//2 + 90))

    # Game Over
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