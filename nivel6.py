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
PINK = (255, 105, 180)
LIME = (50, 255, 50)
HOT_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
ELECTRIC_BLUE = (125, 249, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nivel 6 - El Número Uno")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 48)
dialogue_font = pygame.font.SysFont("Arial", 28)

# --- Recursos ---
fondo_img = pygame.image.load("img/espectaculo.png").convert()
fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))

nave_img_original = pygame.image.load("img/nave.png").convert_alpha()

# Cargar imagen del nuevo enemigo "Número Uno"
try:
    boss_img = pygame.image.load("img/numero1.png").convert_alpha()
    boss_img = pygame.transform.scale(boss_img, (120, 120))
    has_boss_img = True
except:
    print("No se pudo cargar numero1.png, usando imagen por defecto")   
    boss_img = pygame.Surface((120, 120))
    boss_img.fill(RED)
    has_boss_img = False

# Cargar imágenes para la introducción
try:
    numero_uno_img = pygame.image.load("img/numero1.png").convert_alpha()
    numero_uno_img = pygame.transform.scale(numero_uno_img, (300, 300))
    has_numero_uno_img = True
except:
    print("No se pudo cargar la imagen del número uno")
    has_numero_uno_img = False

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
pygame.mixer.music.load("sound/we_are_number_one.mp3")
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

# --- Sistema de Partículas de Fiesta MODIFICADO ---
class PartyParticleSystem:
    def __init__(self):
        self.particles = []
        self.colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, LIME, CYAN, HOT_PINK, NEON_GREEN, ELECTRIC_BLUE]
        self.max_particles = 50  # LÍMITE MÁXIMO DE PARTÍCULAS
        self.confetti_enabled = True
        
    def create_burst(self, x, y, count=15):  # REDUCIDO de 20 a 15
        # Verificar límite de partículas
        if len(self.particles) > self.max_particles:
            return
            
        for _ in range(min(count, self.max_particles - len(self.particles))):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(80, 250)  # REDUCIDA velocidad
            lifetime = random.uniform(0.8, 2.0)  # REDUCIDA duración
            size = random.randint(2, 6)  # REDUCIDO tamaño
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': random.choice(self.colors),
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'size': size,
                'type': random.choice(['circle', 'sparkle'])  # ELIMINADO 'star' para simplificar
            })
            
    def create_confetti(self, count=5):  # REDUCIDO de 10 a 5
        if not self.confetti_enabled or len(self.particles) > self.max_particles:
            return
            
        for _ in range(min(count, self.max_particles - len(self.particles))):
            self.particles.append({
                'x': random.randint(0, WIDTH),
                'y': -10,
                'vx': random.uniform(-30, 30),  # REDUCIDA velocidad
                'vy': random.uniform(80, 150),  # REDUCIDA velocidad
                'color': random.choice(self.colors),
                'lifetime': random.uniform(2.0, 4.0),  # REDUCIDA duración
                'max_lifetime': 4.0,
                'size': random.randint(2, 4),  # REDUCIDO tamaño
                'type': 'confetti',
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-3, 3)  # REDUCIDA velocidad rotación
            })
    
    def disable_confetti(self):
        self.confetti_enabled = False
        
    def enable_confetti(self):
        self.confetti_enabled = True
            
    def update(self, dt):
        for p in self.particles[:]:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['lifetime'] -= dt
            
            # Gravedad para confeti (más suave)
            if p['type'] == 'confetti':
                p['vy'] += 30 * dt  # REDUCIDA gravedad
                p['rotation'] += p['rotation_speed']
                
            # Rebote en bordes para algunas partículas
            if p['x'] < 0 or p['x'] > WIDTH:
                p['vx'] *= -0.8
            if p['y'] > HEIGHT and p['type'] == 'confetti':
                p['vy'] *= -0.5
                p['y'] = HEIGHT - 1
                
            if p['lifetime'] <= 0:
                self.particles.remove(p)
                
    def draw(self, surf):
        for p in self.particles:
            alpha = int(255 * (p['lifetime'] / p['max_lifetime']))
            color = p['color']
            
            if p['type'] == 'circle':
                pygame.draw.circle(surf, color, (int(p['x']), int(p['y'])), p['size'])
            elif p['type'] == 'sparkle':
                size = int(p['size'] * (p['lifetime'] / p['max_lifetime']))
                pygame.draw.circle(surf, WHITE, (int(p['x']), int(p['y'])), size)
            elif p['type'] == 'confetti':
                # Dibujar confeti como pequeños rectángulos rotados
                confetti_surf = pygame.Surface((p['size']*2, p['size']), pygame.SRCALPHA)
                pygame.draw.rect(confetti_surf, color, (0, 0, p['size']*2, p['size']))
                rotated_confetti = pygame.transform.rotate(confetti_surf, p['rotation'])
                surf.blit(rotated_confetti, (p['x'] - rotated_confetti.get_width()//2, 
                                           p['y'] - rotated_confetti.get_height()//2))

# --- Efectos de Fiesta MODIFICADOS ---
class PartyEffects:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.color_timer = 0
        self.current_bg_color = BLACK
        self.flash_timer = 0
        self.flash_visible = False
        self.pulse_timer = 0
        self.pulse_scale = 1.0
        self.confetti_timer = 0
        self.strobe_timer = 0
        self.strobe_visible = True
        self.intensity = 1.0  # CONTROL DE INTENSIDAD
        
    def set_intensity(self, intensity):
        self.intensity = max(0.0, min(1.0, intensity))

    def activate(self):
        self.active = True
        self.timer = 0
        self.color_timer = 0
        self.current_bg_color = BLACK
        self.flash_timer = 0
        self.flash_visible = False
        self.pulse_timer = 0
        self.pulse_scale = 1.0
        self.confetti_timer = 0
        self.strobe_timer = 0
        self.strobe_visible = True

    def update(self, dt):
        if not self.active:
            return
            
        self.timer += dt
        self.color_timer += dt
        self.flash_timer += dt
        self.pulse_timer += dt
        self.confetti_timer += dt
        self.strobe_timer += dt
        
        # Cambio de color de fondo cada 0.3 segundos (modulado por intensidad)
        if self.color_timer >= 0.3 * (2 - self.intensity):
            self.color_timer = 0
            if random.random() < self.intensity:  # Menos cambios a baja intensidad
                self.current_bg_color = random.choice([PURPLE, BLUE, HOT_PINK, NEON_GREEN, ORANGE, CYAN])
            
        # Flash aleatorio cada 0.5-2 segundos (menos frecuente a baja intensidad)
        if self.flash_timer >= random.uniform(0.5 * (2 - self.intensity), 2.0 * (2 - self.intensity)):
            self.flash_timer = 0
            if random.random() < self.intensity:  # Menos flashes a baja intensidad
                self.flash_visible = True
            
        if self.flash_visible and self.flash_timer > 0.1:
            self.flash_visible = False
            
        # Efecto de pulso
        self.pulse_scale = 1.0 + math.sin(self.pulse_timer * 8) * 0.1 * self.intensity
        
        # Efecto estroboscópico rápido (menos intenso)
        if self.strobe_timer >= 0.1 * (2 - self.intensity):
            self.strobe_timer = 0
            if random.random() < self.intensity:  # Menos strobe a baja intensidad
                self.strobe_visible = not self.strobe_visible
            
    def draw(self, surf):
        if not self.active:
            return
            
        # Fondo de color cambiante (más transparente a baja intensidad)
        bg_alpha = int(30 * self.intensity)
        bg_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        bg_overlay.fill((*self.current_bg_color, bg_alpha))
        surf.blit(bg_overlay, (0, 0))
        
        # Flash blanco ocasional (más transparente a baja intensidad)
        if self.flash_visible:
            flash_alpha = int(100 * self.intensity)
            flash_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_overlay.fill((255, 255, 255, flash_alpha))
            surf.blit(flash_overlay, (0, 0))
            
        # Efecto estroboscópico (más suave a baja intensidad)
        if not self.strobe_visible:
            strobe_alpha = int(80 * self.intensity)
            strobe_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            strobe_overlay.fill((255, 255, 255, strobe_alpha))
            surf.blit(strobe_overlay, (0, 0))

# --- Sistema de Scroll Acelerado ---
class AcceleratedScroll:
    def __init__(self):
        self.base_speed = 100
        self.current_speed = 100
        self.target_speed = 100
        self.acceleration = 0
        self.max_speed = 800
        self.scroll_x = 0
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.speed_boost_duration = 10.0
        
    def activate_speed_boost(self, target_speed=600, duration=9999.0):  # Duración muy larga
        self.target_speed = target_speed
        self.speed_boost_active = True
        self.speed_boost_timer = duration
        self.acceleration = (target_speed - self.current_speed) / 1.0  # Acelerar en 1 segundo
        
    def deactivate_speed_boost(self):
        self.speed_boost_active = False
        self.target_speed = self.base_speed
        self.acceleration = (self.base_speed - self.current_speed) / 2.0  # Desacelerar en 2 segundos
        
    def update(self, dt):
        # Actualizar scroll
        self.scroll_x -= self.current_speed * dt
        if self.scroll_x <= -WIDTH:
            self.scroll_x = 0
            
        # Manejar aceleración/desaceleración
        if self.speed_boost_active:
            self.speed_boost_timer -= dt
            # No desactivar automáticamente (duración muy larga)
                
        # Aplicar aceleración
        if abs(self.current_speed - self.target_speed) > 1:
            self.current_speed += self.acceleration * dt
            self.current_speed = max(self.base_speed, min(self.max_speed, self.current_speed))
        else:
            self.current_speed = self.target_speed
            
    def get_scroll_offset(self):
        return self.scroll_x
        
    def is_high_speed(self):
        return self.current_speed > 400

# --- Sistema de Introducción Mejorado ---
class IntroductionSystem:
    def __init__(self):
        self.active = True
        self.current_dialogue = 0
        self.dialogues = [
            {
                "speaker": "numero_uno",
                "text": "¡JAJAJA! ¡Por fin llegas! Pensé que nunca te atreverías a enfrentarme.",
                "position": "right"
            },
            {
                "speaker": "player", 
                "text": "¿Quién eres tú? No reconozco tu forma...",
                "position": "left"
            },
            {
                "speaker": "numero_uno",
                "text": "¡Soy el NÚMERO UNO! El mejor de todos, el más poderoso.",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "Número uno... No era el Bicho? Siuuuu.",
                "position": "left"
            },
            {
                "speaker": "numero_uno", 
                "text": "quien? no, yo  Soy perfecto en todo. Fuerza, velocidad, inteligencia...",
                "position": "right"
            },
            {
                "speaker": "numero_uno",
                "text": "Mira mis movimientos, mi estilo. Nadie puede igualarme.",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "La arrogancia suele ser la caída de los que se creen perfectos.",
                "position": "left"
            },
            {
                "speaker": "numero_uno",
                "text": "¡JA! Palabras de envidioso. Prepárate para ver por qué soy el mejor.",
                "position": "right"
            },
            {
                "speaker": "numero_uno",
                "text": "¡Te mostraré movimientos que ni en tus sueños podrías imaginar!",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "Demuéstralo entonces. No tengo tiempo para fanfarrones.",
                "position": "left"
            },
            {
                "speaker": "both",
                "text": "¡QUE COMIENCE EL ESPECTÁCULO!",
                "position": "center"
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
        surf.fill(BLACK)
        
        pygame.draw.rect(surf, BROWN, (20, 20, WIDTH-40, HEIGHT-40), 4, border_radius=10)
        pygame.draw.rect(surf, GOLD, (30, 30, WIDTH-60, HEIGHT-60), 2, border_radius=8)
        
        current_dialogue = self.dialogues[self.current_dialogue]
        
        if current_dialogue["speaker"] == "numero_uno" or current_dialogue["speaker"] == "both":
            if has_numero_uno_img:
                char_x = WIDTH - 350
                char_y = HEIGHT//2 - 150
                numero_colored = numero_uno_img.copy()
                numero_colored.fill(GOLD, special_flags=pygame.BLEND_RGBA_MULT)
                surf.blit(numero_colored, (char_x, char_y))
        
        if current_dialogue["speaker"] == "player" or current_dialogue["speaker"] == "both":
            if has_player_nave_img:
                char_x = 50
                char_y = HEIGHT//2 - 100
                surf.blit(player_nave_img, (char_x, char_y))
        
        if current_dialogue["position"] == "left":
            dialog_rect = pygame.Rect(50, HEIGHT - 200, WIDTH//2 - 80, 150)
            name_x = dialog_rect.x + 20
            text_align = "left"
        elif current_dialogue["position"] == "right":
            dialog_rect = pygame.Rect(WIDTH//2 + 30, HEIGHT - 200, WIDTH//2 - 80, 150)
            name_x = dialog_rect.x + 20
            text_align = "left"
        else:
            dialog_rect = pygame.Rect(WIDTH//4, HEIGHT - 200, WIDTH//2, 150)
            name_x = dialog_rect.centerx
            text_align = "center"
        
        pygame.draw.rect(surf, (30, 30, 50), dialog_rect, border_radius=15)
        pygame.draw.rect(surf, GOLD, dialog_rect, 3, border_radius=15)
        
        speaker_names = {
            "numero_uno": "NÚMERO UNO",
            "player": "TU NAVE",
            "both": "ENFRENTAMIENTO"
        }
        
        name_colors = {
            "numero_uno": GOLD,
            "player": BLUE, 
            "both": PURPLE
        }
        
        name_text = title_font.render(speaker_names[current_dialogue["speaker"]], True, name_colors[current_dialogue["speaker"]])
        if text_align == "center":
            surf.blit(name_text, (name_x - name_text.get_width()//2, dialog_rect.y + 15))
        else:
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
            prompt_text = "Presiona X para continuar" if self.current_dialogue < len(self.dialogues) - 1 else "Presiona X para comenzar la batalla"
            prompt = dialogue_font.render(prompt_text, True, GREEN)
            
            if text_align == "center":
                prompt_x = dialog_rect.centerx - prompt.get_width()//2
            else:
                prompt_x = dialog_rect.x + 20
            
            surf.blit(prompt, (prompt_x, dialog_rect.bottom - 40))
            
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
        
        title_surface = title_font.render("NIVEL 6", True, GOLD)
        title_surface.set_alpha(self.alpha)
        surf.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, HEIGHT//2 - 100))
        
        subtitle_surface = dialogue_font.render("El Número Uno", True, GOLD)
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

# --- Efecto de Knockout MEJORADO ---
class KnockoutEffect:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.duration = 4.0  # Un poco más largo para mejor visibilidad
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
        self.freeze_game = True  # Congelar el juego
        self.show_stats = False
        if has_knockout_sound:
            sonido_knockout.play()

    def update(self, dt):
        if not self.active:
            return False
            
        self.timer += dt
        progress = min(1.0, self.timer / self.duration)
        
        if progress < 0.3:
            # Fase 1: Aparece el KO
            self.alpha = int(progress / 0.3 * 255)
            self.scale = 0.1 + (1.0 - 0.1) * (progress / 0.3)
        elif progress < 0.6:
            # Fase 2: Se mantiene visible
            self.alpha = 255
            self.scale = 1.0
        elif progress < 0.8:
            # Fase 3: Comienza a desaparecer
            self.alpha = int((1.0 - (progress - 0.6) / 0.2) * 255)
            self.scale = 1.0
        else:
            # Fase 4: Mostrar estadísticas
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
            # Dibujar efecto KO
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
                ko_text = ko_font.render("KNOCKOUT!", True, (255, 50, 50))
                ko_rect = ko_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
                effect_surface.blit(ko_text, ko_rect)
        else:
            # Dibujar mensaje de victoria
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

# --- Efectos Especiales para el Nivel 6 ---
class DiscoEffect:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.color_timer = 0
        self.current_color = RED
        self.colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, LIME, CYAN]

    def activate(self):
        self.active = True
        self.timer = 0
        self.color_timer = 0

    def update(self, dt):
        if not self.active:
            return False
            
        self.timer += dt
        self.color_timer += dt
        
        if self.color_timer >= 0.2:
            self.color_timer = 0
            self.current_color = random.choice(self.colors)
            
        # No se desactiva automáticamente, solo cuando se llame deactivate()
        return False

    def deactivate(self):
        self.active = False

    def draw(self, surf):
        if not self.active:
            return
            
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((*self.current_color, 50))
        surf.blit(overlay, (0, 0))

class SpeedEffect:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.speed_lines = []

    def activate(self):
        self.active = True
        self.timer = 0
        self.speed_lines = []

    def update(self, dt):
        if not self.active:
            return False
            
        self.timer += dt
        
        # Generar líneas de velocidad (más frecuentemente a alta velocidad)
        if random.random() < 0.4:
            self.speed_lines.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'length': random.randint(30, 80),
                'width': random.randint(2, 5),
                'life': 0.8
            })
        
        for line in self.speed_lines[:]:
            line['life'] -= dt * 3
            if line['life'] <= 0:
                self.speed_lines.remove(line)
                
        # No se desactiva automáticamente
        return False

    def deactivate(self):
        self.active = False

    def draw(self, surf):
        if not self.active:
            return
            
        for line in self.speed_lines:
            alpha = int(line['life'] * 255)
            color = (255, 255, 255, alpha)
            line_surf = pygame.Surface((line['length'], line['width']), pygame.SRCALPHA)
            line_surf.fill(color)
            surf.blit(line_surf, (line['x'], line['y']))

class UpsideDownEffect:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.duration = 10.0
        self.rotation_angle = 0
        self.flash_timer = 0
        self.flash_visible = True

    def activate(self):
        self.active = True
        self.timer = 0
        self.rotation_angle = 0
        self.flash_timer = 0
        self.flash_visible = True

    def update(self, dt):
        if not self.active:
            return False
            
        self.timer += dt
        self.flash_timer += dt
        
        # Animación de rotación
        self.rotation_angle = (self.rotation_angle + 180 * dt) % 360
        
        # Efecto de parpadeo
        if self.flash_timer >= 0.1:
            self.flash_timer = 0
            self.flash_visible = not self.flash_visible
            
        if self.timer >= self.duration:
            self.active = False
            return True
        return False

    def draw(self, surf):
        if not self.active:
            return
            
        # Efecto de parpadeo
        if self.flash_visible:
            flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, 30))
            surf.blit(flash_surface, (0, 0))
        
        # Mensaje de advertencia
        warning_font = pygame.font.SysFont("Arial", 36)
        warning_text = warning_font.render("¡MUNDO AL REVÉS!", True, RED)
        warning_rect = warning_text.get_rect(center=(WIDTH//2, 50))
        
        # Efecto de temblor en el texto
        shake_x = random.randint(-3, 3)
        shake_y = random.randint(-3, 3)
        surf.blit(warning_text, (warning_rect.x + shake_x, warning_rect.y + shake_y))

# --- Clase Obstáculo modificada ---
class Obstacle:
    def __init__(self, x, y, obstacle_type="meteor"):
        self.x = x
        self.y = y
        self.type = obstacle_type
        self.speed = random.uniform(200, 350)
        self.size = random.randint(25, 35)
        self.color = RED if obstacle_type == "meteor" else ORANGE
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)
        # Dirección: de derecha a izquierda
        self.direction = -1

    def update(self, dt):
        self.x += self.direction * self.speed * dt
        self.rotation += self.rotation_speed
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
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
        self.upside_down = False
        self.upside_down_timer = 0

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

    def start_upside_down(self, duration=10.0):
        self.upside_down = True
        self.upside_down_timer = duration

    def update(self, dt):
        if self.earthquake_active:
            self.earthquake_timer += dt
            self.shake_intensity = self.earthquake_intensity * (1 - (self.earthquake_timer / self.earthquake_duration))
            
            if self.earthquake_timer >= self.earthquake_duration:
                self.earthquake_active = False
                self.shake_intensity = 0
        
        if self.upside_down:
            self.upside_down_timer -= dt
            if self.upside_down_timer <= 0:
                self.upside_down = False
        
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

# --- NumeroUno MODIFICADO para fase final ---
class NumeroUno:
    def __init__(self):
        self.w = 120
        self.h = 120
        self.x = WIDTH + 200
        self.y = HEIGHT // 3
        self.max_hp = 5000
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
        self.charge_timer = 0
        self.charging = False
        self.charge_direction = 0
        self.charge_speed = 800
        self.returning = False
        
        self.phase_attack_cooldowns = [1.5, 1.0, 0.7]
        self.phase_move_speeds = [100, 180, 250]
        
        self.color = GOLD
        self.bullet_color = ORANGE
        self.rain_active = False
        self.rain_timer = 0
        self.rain_duration = 5.0
        self.upside_down_timer = 0
        self.upside_down_active = False
        self.obstacle_timer = 0
        self.obstacle_interval = 2.0  # AUMENTADO intervalo entre obstáculos
        self.obstacle_count_phase3 = 2  # MÁXIMO de obstáculos por vez en fase 3

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
            return True
        return False

    def update(self, dt, enemy_bullets, player, obstacles, camera_effect, upside_down_effect):
        if self.entering:
            self.x -= 200 * dt
            if self.x <= WIDTH - self.w - 100:
                self.entering = False
            self.rect.topleft = (int(self.x), int(self.y))
            return
            
        if self.exiting:
            self.x += 300 * dt
            self.rect.topleft = (int(self.x), int(self.y))
            return

        if not self.active:
            return

        phase_changed = self.update_phase()
        if phase_changed:
            sonido_fase.play()
            # REDUCIR intensidad de efectos en fase 3 para mejor jugabilidad
            if self.phase == 3:
                party_effects.set_intensity(0.3)  # MENOS intenso en fase final
                party_particles.disable_confetti()  # DESACTIVAR confeti en fase 3

        # Ataque de carga en fase 1
        if self.phase == 1 and not self.charging and not self.returning:
            self.charge_timer += dt
            if self.charge_timer >= 3.0:
                self.charging = True
                self.charge_timer = 0
                self.charge_direction = -1

        if self.charging:
            self.x += self.charge_direction * self.charge_speed * dt
            if self.x <= 100:
                self.charging = False
                self.returning = True
                self.charge_direction = 1

        if self.returning:
            self.x += self.charge_direction * 400 * dt
            if self.x >= WIDTH - self.w - 100:
                self.returning = False

        # Efecto de pantalla al revés en fase 2
        if self.phase == 2 and not self.upside_down_active:
            self.upside_down_timer += dt
            if self.upside_down_timer >= 5.0:
                self.upside_down_active = True
                camera_effect.start_upside_down(10.0)
                upside_down_effect.activate()
                self.upside_down_timer = 0

        # Generar obstáculos en fase 3 de manera MÁS CONTROLADA
        if self.phase == 3:
            self.obstacle_timer += dt
            if self.obstacle_timer >= self.obstacle_interval:
                self.obstacle_timer = 0
                # Solo generar 1 obstáculo a la vez en fase 3
                num_obstacles = random.randint(1, 1)  # SIEMPRE 1 en fase 3
                for i in range(num_obstacles):
                    # Verificar que no haya muchos obstáculos en pantalla
                    if len(obstacles) < 3:  # MÁXIMO 3 obstáculos en pantalla
                        obstacles.append(Obstacle(
                            random.randint(WIDTH + 50, WIDTH + 200),
                            random.randint(100, HEIGHT - 100),
                            "meteor"
                        ))

        self.move_timer += dt
        move_speed = self.phase_move_speeds[self.phase - 1]
        
        if not self.charging and not self.returning:
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
        if self.attack_timer <= 0 and not self.charging and not self.returning:
            self.attack_timer = self.attack_cooldown
            
            if self.phase == 1:
                self.attack_phase1(enemy_bullets)
            elif self.phase == 2:
                self.attack_phase2(enemy_bullets, player)
            elif self.phase == 3:
                self.attack_phase3(enemy_bullets, player, obstacles)

        self.rect.topleft = (int(self.x), int(self.y))

    def attack_phase1(self, enemy_bullets):
        # Disparos en patrón de abanico
        for i in range(7):
            angle = math.radians(-45 + i * 15)
            enemy_bullets.append(Bullet(
                self.x + self.w//2, self.y + self.h,
                -350 * math.cos(angle), 250 * math.sin(angle),
                color=self.bullet_color, owner="boss", damage=15
            ))

    def attack_phase2(self, enemy_bullets, player):
        # Disparos dirigidos al jugador
        for i in range(5):
            angle_offset = random.uniform(-0.3, 0.3)
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy) or 1
            enemy_bullets.append(Bullet(
                self.x + self.w//2, self.y + self.h//2,
                (dx/dist + angle_offset) * 400, (dy/dist + angle_offset) * 400,
                color=self.bullet_color, owner="boss", damage=20
            ))

    def attack_phase3(self, enemy_bullets, player, obstacles):
        attack_type = random.choice(["rain", "circle", "missile", "obstacles"])
        
        if attack_type == "rain":
            self.rain_active = True
            self.rain_timer = self.rain_duration
            # REDUCIDO número de meteoritos en fase 3
            for i in range(3):  # REDUCIDO de 5 a 3
                obstacles.append(Obstacle(
                    random.randint(WIDTH + 50, WIDTH + 200),
                    random.randint(50, HEIGHT - 50),
                    "meteor"
                ))
                    
        elif attack_type == "circle":
            for i in range(8):  # REDUCIDO de 12 a 8
                angle = math.radians(i * 45)
                enemy_bullets.append(Bullet(
                    self.x + self.w//2, self.y + self.h//2,
                    math.cos(angle) * 300, math.sin(angle) * 300,
                    color=self.bullet_color, owner="boss", damage=25
                ))
                
        elif attack_type == "missile":
            # Lanzar misiles especiales
            for i in range(2):  # REDUCIDO de 3 a 2
                enemy_bullets.append(Bullet(
                    self.x + self.w//2, self.y + self.h//2 + (i-1) * 30,
                    -400, 0,
                    color=PURPLE, owner="boss", damage=30
                ))
        
        elif attack_type == "obstacles":
            # Generar obstáculos controlados - MÁXIMO 2 en fase 3
            for i in range(min(2, self.obstacle_count_phase3)):
                obstacles.append(Obstacle(
                    random.randint(WIDTH + 50, WIDTH + 150),
                    random.randint(100, HEIGHT - 100),
                    "meteor"
                ))

    def take_damage(self, damage):
        self.hp -= damage
        return self.hp <= 0

    def start_exit(self):
        self.exiting = True
        self.active = False

    def draw(self, surf):
        if not self.active and self.exiting:
            return
            
        phase_colors = [
            GOLD,
            ORANGE,
            RED
        ]
        current_color = phase_colors[self.phase - 1]
            
        boss_colored = boss_img.copy()
        boss_colored.fill(current_color, special_flags=pygame.BLEND_RGBA_MULT)
        surf.blit(boss_colored, (self.x, self.y))
        
        bar_width = 200
        bar_height = 15
        bar_x = self.x + self.w//2 - bar_width//2
        bar_y = self.y - 25
        
        pygame.draw.rect(surf, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
        hp_fraction = max(0, self.hp / self.max_hp)
        pygame.draw.rect(surf, current_color, (bar_x, bar_y, int(bar_width * hp_fraction), bar_height))
        
        names = ["Número Uno", "Modo Arrogante", "Furia Final"]
        name_text = font.render(f"{names[self.phase-1]}: {self.hp}/{self.max_hp}", True, WHITE)
        surf.blit(name_text, (bar_x, bar_y - 20))

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

# --- Sistema de Resultados MEJORADO ---
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
            return "A+", GOLD, "¡PERFECTO! El número uno ha caído"
        elif score >= 85:
            return "A", GREEN, "¡Excelente! Derrotaste al arrogante"
        elif score >= 75:
            return "B", BLUE, "¡Buen trabajo! Venciste al número uno"
        elif score >= 60:
            return "C", YELLOW, "¡Bien hecho! Superaste el desafío"
        else:
            return "D", ORANGE, "¡Logrado! El número uno ha sido derrotado"
            
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
        
        title_text = title_font.render("¡VICTORIA! - NIVEL 6", True, GOLD)
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
            f"Número Uno derrotado: {'Sí' if self.boss_defeated else 'No'}"
        ]
        
        for stat in stats:
            stat_text = font.render(stat, True, WHITE)
            surf.blit(stat_text, (WIDTH//2 - stat_text.get_width()//2, stats_y))
            stats_y += 35
        
        phrase_text = font.render(self.motivational_phrase, True, GREEN)
        surf.blit(phrase_text, (WIDTH//2 - phrase_text.get_width()//2, stats_y + 20))
        
        instruction_text = font.render("Presiona ENTER para continuar al siguiente nivel", True, YELLOW)
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
        pygame.mixer.music.load("sound/we_are_number_one.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except:
        print("No se pudo cargar la música normal")

# --- Estado del juego ---
player = Player()
player_bullets = []
enemy_bullets = []
missiles = []
obstacles = []
numero_uno = NumeroUno()
title_screen = TitleScreen()
introduction = IntroductionSystem()
energy_ui = EnergyUI()
results_system = ResultsSystem()
camera_effect = CameraEffect()
knockout_effect = KnockoutEffect()
disco_effect = DiscoEffect()
speed_effect = SpeedEffect()
upside_down_effect = UpsideDownEffect()

# NUEVOS SISTEMAS DE EFECTOS
party_effects = PartyEffects()
party_particles = PartyParticleSystem()
accelerated_scroll = AcceleratedScroll()

score = 0
game_over = False
level_cleared = False
fight_started = False
boss_defeated = 0
victory_sound_played = False
knockout_shown = False
battle_start_time = 0

continue_countdown = 0
continue_time = 10.0
coins_inserted = 0
continues_used = 0
continue_available = True
lives_per_coin = 3

start_time = pygame.time.get_ticks()
completion_time = 0

# Variables para control de efectos
disco_activated = False
speed_activated = False
party_activated = False
scroll_boost_activated = False

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
            if event.key == pygame.K_RETURN and results_system.active:
                running = False
                pygame.quit()
                try:
                    subprocess.run([sys.executable, "nivel7.py"])
                except:
                    print("No se pudo cargar el siguiente nivel")
                sys.exit()
            if event.key == pygame.K_SPACE and knockout_effect.active and knockout_effect.show_stats:
                # Saltar directamente a las estadísticas
                knockout_effect.active = False
                knockout_effect.freeze_game = False
                results_system.show_results(player, continues_used, score, completion_time, boss_defeated)
            if event.key == pygame.K_x and introduction.active:
                result = introduction.advance_text()
                if result == "start_battle":
                    play_normal_music()
                    player.activate()
                    numero_uno.entering = True
                    fight_started = True
                    battle_start_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

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
        introduction.draw(screen)
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
            knockout_effect.freeze_game = False
            results_system.show_results(player, continues_used, score, completion_time, boss_defeated)

    # Juego principal (batalla) - CONGELADO durante knockout
    if not game_over and not level_cleared and fight_started and not results_system.active and not knockout_effect.freeze_game:
        current_battle_time = (pygame.time.get_ticks() - battle_start_time) / 1000.0
        
        # EFECTOS SINCRONIZADOS CON LA MÚSICA - MODIFICADOS PARA MENOS CONFETI
        if current_battle_time >= 6.0 and not scroll_boost_activated:
            # ACTIVAR SCROLL ACELERADO EN SEGUNDO 6 Y MANTENERLO
            accelerated_scroll.activate_speed_boost(800, 9999.0)  # Duración casi infinita
            scroll_boost_activated = True
            
        if current_battle_time >= 6.0 and not disco_activated:
            disco_effect.activate()
            disco_activated = True
            
        if current_battle_time >= 6.0 and not speed_activated:
            speed_effect.activate()
            speed_activated = True
            
        if current_battle_time >= 6.0 and not party_activated:
            party_effects.activate()
            party_effects.set_intensity(0.7)  # INTENSIDAD MODERADA
            party_activated = True
            # Crear explosión inicial de partículas (MÁS PEQUEÑA)
            party_particles.create_burst(WIDTH//2, HEIGHT//2, 30)  # REDUCIDO de 50 a 30
        
        # Actualizar sistemas
        player.update(dt, keys)
        camera_effect.update(dt)
        disco_effect.update(dt)
        speed_effect.update(dt)
        upside_down_effect.update(dt)
        accelerated_scroll.update(dt)
        party_effects.update(dt)
        party_particles.update(dt)
        
        # Generar confeti continuo durante el efecto de fiesta - MUCHO MENOS FRECUENTE
        if party_activated and random.random() < 0.1:  # REDUCIDO de 0.3 a 0.1
            party_particles.create_confetti(3)  # REDUCIDO de 5 a 3

        # Disparar balas normales
        if keys[pygame.K_x] and player.can_shoot():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            bullet = Bullet(bx, by, 600, 0, color=GREEN, owner="player")
            player_bullets.append(bullet)
            player.shoot()

        # Lanzar misil
        if keys[pygame.K_z] and player.can_launch_missile():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            missile = Missile(bx, by)
            missiles.append(missile)
            player.launch_missile()

        # Actualizar número uno
        if numero_uno.active or numero_uno.entering or numero_uno.exiting:
            numero_uno.update(dt, enemy_bullets, player, obstacles, camera_effect, upside_down_effect)

        # Actualizar obstáculos
        for obstacle in obstacles[:]:
            obstacle.update(dt)
            # Eliminar obstáculos cuando salgan por la izquierda
            if obstacle.x < -50:
                obstacles.remove(obstacle)
                continue
            if player.rect.colliderect(obstacle.rect):
                player.take_damage()
                if obstacle in obstacles:
                    obstacles.remove(obstacle)

        # Actualizar balas del jugador
        for b in player_bullets[:]:
            b.update(dt)
            if b.x > WIDTH + 50:
                player_bullets.remove(b)
                continue
            if numero_uno.active and rect_circle_collide(numero_uno.rect, b.x, b.y, b.radius):
                if numero_uno.take_damage(b.damage):
                    numero_uno.start_exit()
                    boss_defeated = 1
                    score += 1000
                    player.add_energy(100)
                    player.activate_victory_invincibility(10.0)
                    # ACTIVAR KNOCKOUT EFFECT cuando se derrota al jefe
                    if not knockout_shown:
                        knockout_effect.activate()
                        knockout_shown = True
                        completion_time = (pygame.time.get_ticks() - start_time) / 1000.0
                        pygame.mixer.music.stop()
                        if not victory_sound_played:
                            sonido_victoria.play()
                            victory_sound_played = True
                else:
                    player.add_energy(15)
                    # Pequeña explosión al golpear
                    party_particles.create_burst(b.x, b.y, 10)
                player.bullets_hit += 1
                if b in player_bullets:
                    player_bullets.remove(b)

        # Actualizar misiles
        for m in missiles[:]:
            m.update(dt)
            if m.x > WIDTH + 50:
                missiles.remove(m)
                continue
            if numero_uno.active and rect_circle_collide(numero_uno.rect, m.x, m.y, m.radius):
                if numero_uno.take_damage(m.damage):
                    numero_uno.start_exit()
                    boss_defeated = 1
                    score += 1000
                    player.add_energy(150)
                    player.activate_victory_invincibility(10.0)
                    # ACTIVAR KNOCKOUT EFFECT cuando se derrota al jefe
                    if not knockout_shown:
                        knockout_effect.activate()
                        knockout_shown = True
                        completion_time = (pygame.time.get_ticks() - start_time) / 1000.0
                        pygame.mixer.music.stop()
                        if not victory_sound_played:
                            sonido_victoria.play()
                            victory_sound_played = True
                else:
                    player.add_energy(40)
                    # Explosión de misil
                    party_particles.create_burst(m.x, m.y, 20)
                if m in missiles:
                    missiles.remove(m)

        # Actualizar balas enemigas
        for b in enemy_bullets[:]:
            b.update(dt)
            if b.x < -50 or b.y < -50 or b.y > HEIGHT + 50:
                enemy_bullets.remove(b)
                continue
            if rect_circle_collide(player.rect, b.x, b.y, b.radius):
                player.take_damage()
                # Explosión al recibir daño
                party_particles.create_burst(b.x, b.y, 15)
                if b in enemy_bullets:
                    enemy_bullets.remove(b)

        # Verificar game over
        if player.lives <= 0 and continue_available and continue_countdown == 0:
            continue_countdown = continue_time
            coins_inserted = 0

    # Actualizar conteo de continuación
    if continue_countdown > 0:
        continue_countdown -= dt
        if continue_countdown <= 0:
            continue_countdown = 0
            game_over = True

    # --- DIBUJADO MEJORADO CON EFECTOS DE FIESTA ---
    screen.fill(BLACK)
    
    # Aplicar efectos de fiesta primero (fondo)
    party_effects.draw(screen)
    
    # Dibujar fondo con scroll acelerado
    scroll_offset = accelerated_scroll.get_scroll_offset()
    
    # Dibujar fondo con efecto de velocidad
    for i in range(2):
        bg_x = int(scroll_offset + i * WIDTH)
        screen.blit(fondo_img, (bg_x, 0))

    # Aplicar efectos de cámara en una superficie temporal
    game_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    # Dibujar todos los elementos del juego (solo si no está congelado)
    if not knockout_effect.freeze_game:
        numero_uno.draw(game_surface)

        for b in player_bullets:
            b.draw(game_surface)
        for b in enemy_bullets:
            b.draw(game_surface)
        for m in missiles:
            m.draw(game_surface)
        for obstacle in obstacles:
            obstacle.draw(game_surface)

        if continue_countdown == 0:
            player.draw(game_surface)
    
    # Aplicar efectos visuales al juego
    disco_effect.draw(game_surface)
    speed_effect.draw(game_surface)
    upside_down_effect.draw(game_surface)
    
    # Dibujar partículas de fiesta (encima del juego pero debajo de la UI)
    party_particles.draw(game_surface)
    
    # Aplicar la superficie del juego a la pantalla principal
    screen.blit(game_surface, (0, 0))

    # Aplicar efecto de pantalla al revés si está activo
    if camera_effect.upside_down:
        screen.blit(pygame.transform.flip(screen, False, True), (0, 0))

    # Dibujar efecto de knockout (encima de todo)
    if knockout_effect.active:
        knockout_effect.draw(screen)

    # UI (sin efectos de cámara)
    energy_ui.draw(screen, player)
    
    lives_text = font.render(f"Vidas: {player.lives}", True, WHITE)
    screen.blit(lives_text, (12, 12))
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (12, 36))
    
    boss_text = font.render(f"Número Uno: {'Derrotado' if boss_defeated else 'Vivo'}", True, YELLOW)
    screen.blit(boss_text, (WIDTH//2 - boss_text.get_width()//2, 12))
    
    # Indicador de velocidad del scroll
    if accelerated_scroll.is_high_speed():
        speed_text = font.render(f"¡VELOCIDAD EXTREMA! {int(accelerated_scroll.current_speed)}", True, HOT_PINK)
        screen.blit(speed_text, (WIDTH//2 - speed_text.get_width()//2, HEIGHT - 100))
    
    # Indicador de invencibilidad por victoria
    if player.victory_invincible:
        invincible_text = font.render("INVENCIBLE", True, PURPLE)
        screen.blit(invincible_text, (WIDTH//2 - invincible_text.get_width()//2, 40))
    
    # Indicador de fase y efectos
    if fight_started and not level_cleared and not knockout_effect.freeze_game:
        phase_text = font.render(f"Fase: {numero_uno.phase}/3", True, GOLD)
        screen.blit(phase_text, (WIDTH - 120, 60))
        
        if camera_effect.upside_down:
            upside_text = font.render("¡PANTALLA AL REVÉS!", True, RED)
            screen.blit(upside_text, (WIDTH//2 - upside_text.get_width()//2, HEIGHT - 40))
        
        if numero_uno.rain_active:
            rain_text = font.render("¡LLUVIA DE METEORITOS!", True, ORANGE)
            screen.blit(rain_text, (WIDTH//2 - rain_text.get_width()//2, HEIGHT - 70))
        
        if party_activated:
            party_text = font.render("¡MODO FIESTA ACTIVADO!", True, NEON_GREEN)
            screen.blit(party_text, (WIDTH//2 - party_text.get_width()//2, HEIGHT - 130))

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
        
        coins_text = font.render(f"Monedas insertadas: {coins_inserted}", True, YELLOW)
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