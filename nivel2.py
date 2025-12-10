import pygame
import random
import math
import subprocess
import sys
from pygame import Rect

# --- Configuración inicial ---
WIDTH, HEIGHT = 960, 540
FPS = 60

# Colores
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (220, 40, 40)
GREEN = (80, 200, 120)
YELLOW = (240, 220, 80)
BLUE = (80, 160, 240)
GREY = (200,200,200)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)
PURPLE = (180, 80, 220)
CYAN = (80, 220, 220)
DARK_RED = (150, 20, 20)
LIGHT_BLUE = (100, 180, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nivel 2 - Un Alma que Tratar")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 36)
title_font = pygame.font.SysFont("Arial", 48)
dialogue_font = pygame.font.SysFont("Arial", 28)

# --- Recursos ---
fondo_img = pygame.image.load("img/bosque.png").convert()
fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))

# Nuevo fondo para fase 2
try:
    fondo_fase2_img = pygame.image.load("img/infierno.png").convert()
    fondo_fase2_img = pygame.transform.scale(fondo_fase2_img, (WIDTH, HEIGHT))
    has_fondo_fase2 = True
except:
    print("No se pudo cargar fondo_fase2.png, usando fondo original")
    fondo_fase2_img = fondo_img
    has_fondo_fase2 = False

nave_img_original = pygame.image.load("img/nave.png").convert_alpha()
boss_img = pygame.image.load("img/e3.png").convert_alpha()
boss_img = pygame.transform.scale(boss_img, (200, 200))

# Cargar imágenes para efectos
try:
    ok_image = pygame.image.load("img/ok.png").convert_alpha()
    ok_image = pygame.transform.scale(ok_image, (320, 180))
    has_ok_image = True
except:
    print("No se pudo cargar ok.png")
    has_ok_image = False

# Cargar imágenes para la introducción
try:
    diablito_img = pygame.image.load("img/e3.png").convert_alpha()
    diablito_img = pygame.transform.scale(diablito_img, (300, 300))
    has_diablito_img = True
except:
    print("No se pudo cargar la imagen del diablito")
    has_diablito_img = False

try:
    player_nave_img = pygame.image.load("img/niño.png").convert_alpha()
    player_nave_img = pygame.transform.scale(player_nave_img, (200, 200))
    has_player_nave_img = True
except:
    print("No se pudo cargar la imagen de la nave")
    has_player_nave_img = False

# Cargar imágenes para enemigos y obstáculos
try:
    obstacle_img = pygame.image.load("img/obstacle.png").convert_alpha()
    obstacle_img = pygame.transform.scale(obstacle_img, (70, 70))
    has_obstacle_img = True
except:
    print("No se pudo cargar obstacle.png")
    has_obstacle_img = False

try:
    basic_enemy_img = pygame.image.load("img/basic_enemy.png").convert_alpha()
    basic_enemy_img = pygame.transform.scale(basic_enemy_img, (70, 70))
    has_basic_enemy_img = True
except:
    print("No se pudo cargar basic_enemy.png")
    has_basic_enemy_img = False

try:
    fast_enemy_img = pygame.image.load("img/fast_enemy.png").convert_alpha()
    fast_enemy_img = pygame.transform.scale(fast_enemy_img, (70, 70))
    has_fast_enemy_img = True
except:
    print("No se pudo cargar fast_enemy.png")
    has_fast_enemy_img = False

try:
    tank_enemy_img = pygame.image.load("img/tank_enemy.png").convert_alpha()
    tank_enemy_img = pygame.transform.scale(tank_enemy_img, (70, 70))
    has_tank_enemy_img = True
except:
    print("No se pudo cargar tank_enemy.png")
    has_tank_enemy_img = False

# Música y sonidos
pygame.mixer.music.load("sound/f3.mp3")   
pygame.mixer.music.set_volume(0.4)

sonido_inicio = pygame.mixer.Sound("sound/inicio1.mp3")   
sonido_derrota = pygame.mixer.Sound("sound/kn.mp3")       
sonido_daño = pygame.mixer.Sound("sound/hit.mp3")        
sonido_coin = pygame.mixer.Sound("sound/coin2.mp3")       
sonido_victoria = pygame.mixer.Sound("sound/victoria.mp3")
sonido_texto = pygame.mixer.Sound("sound/text.mp3")

victory_music = "sound/vic.mp3"
intro_music = "sound/vic.mp3"

# --- Nuevos Sistemas de Efectos y Animaciones Mejorados ---

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_particles(self, x, y, color, count=8, speed_range=(50, 200), 
                     size_range=(2, 6), lifetime_range=(0.3, 0.8), 
                     spread_angle=2*math.pi, gravity=0):
        for _ in range(count):
            angle = random.uniform(0, spread_angle)
            speed = random.uniform(speed_range[0], speed_range[1])
            lifetime = random.uniform(lifetime_range[0], lifetime_range[1])
            size = random.uniform(size_range[0], size_range[1])
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'color': color,
                'size': size,
                'gravity': gravity,
                'original_color': color
            })
            
    def update(self, dt):
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] += particle['gravity'] * dt
            particle['lifetime'] -= dt
            
            # Efecto de desvanecimiento
            progress = particle['lifetime'] / particle['max_lifetime']
            if progress < 0.3:
                particle['size'] *= 0.95
                
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
                
    def draw(self, surf):
        for particle in self.particles:
            alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
            # Asegurarse de que el color esté en el rango correcto
            color = list(particle['color'])
            if len(color) == 3:
                # Asegurar que cada componente esté en [0, 255]
                color = [max(0, min(255, c)) for c in color]
                color.append(alpha)
            else:
                # Asegurar que cada componente esté en [0, 255]
                color = [max(0, min(255, c)) for c in color[:3]]
                color.append(alpha)
                
            pygame.draw.circle(
                surf, 
                color, 
                (int(particle['x']), int(particle['y'])), 
                int(particle['size'])
            )

class ScreenShake:
    def __init__(self):
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_timer = 0
        
    def start_shake(self, intensity=5, duration=0.3):
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_timer = duration
        
    def update(self, dt):
        if self.shake_timer > 0:
            self.shake_timer -= dt
            return True
        return False
        
    def get_offset(self):
        if self.shake_timer <= 0:
            return (0, 0)
        progress = self.shake_timer / self.shake_duration
        current_intensity = self.shake_intensity * progress
        offset_x = random.uniform(-current_intensity, current_intensity)
        offset_y = random.uniform(-current_intensity, current_intensity)
        return (offset_x, offset_y)

class HitEffect(ParticleSystem):
    def add_hit(self, x, y, color=RED, count=12):
        # Asegurar que el color esté en el rango correcto
        safe_color = [max(0, min(255, c)) for c in color]
        super().add_particles(x, y, safe_color, count, 
                            speed_range=(80, 250), 
                            size_range=(3, 8),
                            lifetime_range=(0.4, 1.0))

class BossAttackEffects:
    def __init__(self):
        self.phase_effects = []
        self.special_effects = []
        self.particle_system = ParticleSystem()
        
    def add_phase_effect(self, x, y, phase):
        if phase == 1:
            # Efecto rojo para fase 1 con partículas
            for i in range(12):
                angle = i * math.pi / 6
                self.phase_effects.append({
                    'x': x, 'y': y,
                    'angle': angle,
                    'radius': 0,
                    'max_radius': 100,
                    'speed': 300,
                    'width': 3,
                    'color': RED,
                    'lifetime': 1.0,
                    'pulse_speed': 2.0
                })
            # Partículas de fuego
            self.particle_system.add_particles(x, y, RED, 15, 
                                             speed_range=(50, 150),
                                             size_range=(2, 5),
                                             lifetime_range=(0.5, 1.2))
            
        elif phase == 2:
            # Efecto naranja para fase 2
            for i in range(8):
                angle = random.uniform(0, 2 * math.pi)
                self.phase_effects.append({
                    'x': x, 'y': y,
                    'angle': angle,
                    'radius': 20,
                    'max_radius': 150,
                    'speed': 200,
                    'width': 4,
                    'color': ORANGE,
                    'lifetime': 1.5,
                    'pulse_speed': 3.0
                })
            # Partículas de energía
            self.particle_system.add_particles(x, y, ORANGE, 20,
                                             speed_range=(80, 200),
                                             size_range=(3, 6))
            
        elif phase == 3:
            # Efecto púrpura para fase 3
            for i in range(6):
                self.phase_effects.append({
                    'x': x, 'y': y,
                    'angle': 0,
                    'radius': 50 + i * 20,
                    'max_radius': 200,
                    'speed': 150,
                    'width': 5,
                    'color': PURPLE,
                    'lifetime': 2.0,
                    'pulse_speed': 1.5
                })
            # Partículas mágicas
            self.particle_system.add_particles(x, y, PURPLE, 25,
                                             speed_range=(60, 180),
                                             size_range=(2, 4))
            
        elif phase == 4:
            # Efecto dorado para fase final
            for i in range(16):
                angle = i * math.pi / 8
                self.phase_effects.append({
                    'x': x, 'y': y,
                    'angle': angle,
                    'radius': 0,
                    'max_radius': 120,
                    'speed': 400,
                    'width': 2,
                    'color': GOLD,
                    'lifetime': 0.8,
                    'pulse_speed': 4.0
                })
            # Partículas doradas
            self.particle_system.add_particles(x, y, GOLD, 30,
                                             speed_range=(100, 300),
                                             size_range=(1, 3))
                
    def add_special_effect(self, x, y, effect_type):
        if effect_type == "spawn":
            # Efecto de spawn de minienemigos con partículas
            for i in range(20):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(100, 300)
                self.special_effects.append({
                    'x': x, 'y': y,
                    'vx': math.cos(angle) * speed,
                    'vy': math.sin(angle) * speed,
                    'start_radius': 5,
                    'end_radius': 0,
                    'duration': 0.5,
                    'timer': 0.5,
                    'color': CYAN
                })
            self.particle_system.add_particles(x, y, CYAN, 25,
                                             speed_range=(150, 400),
                                             size_range=(1, 4))
            
        elif effect_type == "homing":
            # Efecto para misiles homing
            for i in range(8):
                self.special_effects.append({
                    'x': x, 'y': y,
                    'radius': 30 + i * 10,
                    'max_radius': 100,
                    'width': 2,
                    'alpha': 255,
                    'duration': 0.6,
                    'timer': 0.6,
                    'color': ORANGE
                })
            self.particle_system.add_particles(x, y, ORANGE, 15,
                                             speed_range=(50, 120),
                                             size_range=(2, 5))
                
    def update(self, dt):
        # Actualizar efectos de fase
        for effect in self.phase_effects[:]:
            effect['radius'] += effect['speed'] * dt
            effect['lifetime'] -= dt
            
            # Efecto de pulso
            if 'pulse_speed' in effect:
                pulse = math.sin(pygame.time.get_ticks() * 0.001 * effect['pulse_speed']) * 3
                effect['width'] = max(1, effect['width'] + pulse)
                
            if effect['radius'] > effect['max_radius'] or effect['lifetime'] <= 0:
                self.phase_effects.remove(effect)
                
        # Actualizar efectos especiales
        for effect in self.special_effects[:]:
            if 'vx' in effect:  # Efecto de partículas
                effect['x'] += effect['vx'] * dt
                effect['y'] += effect['vy'] * dt
            effect['timer'] -= dt
            if effect['timer'] <= 0:
                self.special_effects.remove(effect)
                
        # Actualizar sistema de partículas
        self.particle_system.update(dt)
                
    def draw(self, surf):
        # Dibujar efectos de fase (anillos)
        for effect in self.phase_effects:
            progress = effect['radius'] / effect['max_radius']
            alpha = int(255 * (1 - progress))
            color = list(effect['color'])
            # Asegurar que el color esté en el rango correcto
            color = [max(0, min(255, c)) for c in color]
            color.append(alpha)
            
            pygame.draw.circle(
                surf, 
                color, 
                (int(effect['x']), int(effect['y'])), 
                int(effect['radius']), 
                int(effect['width'])
            )
            
        # Dibujar efectos especiales
        for effect in self.special_effects:
            if 'vx' in effect:  # Partículas
                progress = effect['timer'] / effect['duration']
                radius = effect['start_radius'] * progress
                alpha = int(255 * progress)
                color = list(effect['color'])
                # Asegurar que el color esté en el rango correcto
                color = [max(0, min(255, c)) for c in color]
                color.append(alpha)
                
                pygame.draw.circle(
                    surf,
                    color,
                    (int(effect['x']), int(effect['y'])),
                    int(radius)
                )
            else:  # Anillos concéntricos
                progress = 1 - (effect['timer'] / effect['duration'])
                current_radius = effect['radius'] * progress
                alpha = int(255 * (1 - progress))
                color = list(effect['color'])
                # Asegurar que el color esté en el rango correcto
                color = [max(0, min(255, c)) for c in color]
                color.append(alpha)
                
                pygame.draw.circle(
                    surf,
                    color,
                    (int(effect['x']), int(effect['y'])),
                    int(current_radius),
                    effect['width']
                )
        
        # Dibujar partículas
        self.particle_system.draw(surf)

class BulletTrail:
    def __init__(self):
        self.trails = []
        
    def add_trail(self, x, y, color, owner, size_multiplier=1.0):
        size = (8 if owner == "boss" else 4) * size_multiplier
        # Asegurar que el color esté en el rango correcto
        safe_color = [max(0, min(255, c)) for c in color]
        self.trails.append({
            'x': x, 'y': y,
            'color': safe_color,
            'owner': owner,
            'timer': 0.3,
            'max_timer': 0.3,
            'size': size,
            'original_size': size
        })
        
    def update(self, dt):
        for trail in self.trails[:]:
            trail['timer'] -= dt
            trail['size'] = trail['original_size'] * (trail['timer'] / trail['max_timer'])
            if trail['timer'] <= 0:
                self.trails.remove(trail)
                
    def draw(self, surf):
        for trail in self.trails:
            alpha = int(255 * (trail['timer'] / trail['max_timer']))
            color = list(trail['color'])
            if len(color) == 3:
                # Asegurar que cada componente esté en [0, 255]
                color = [max(0, min(255, c)) for c in color]
                color.append(alpha)
            else:
                # Asegurar que cada componente esté en [0, 255]
                color = [max(0, min(255, c)) for c in color[:3]]
                color.append(alpha)
                
            pygame.draw.circle(
                surf,
                color,
                (int(trail['x']), int(trail['y'])),
                max(1, int(trail['size']))
            )

# --- Efectos Visuales Mejorados para Entidades ---

class PlayerGlow:
    def __init__(self, player):
        self.player = player
        self.glow_timer = 0
        self.glow_intensity = 0
        
    def update(self, dt):
        if self.player.invulnerable:
            self.glow_timer += dt * 10
            self.glow_intensity = abs(math.sin(self.glow_timer)) * 255
        else:
            self.glow_intensity = max(0, self.glow_intensity - dt * 200)
            
    def draw(self, surf):
        if self.glow_intensity > 10:
            glow_surface = pygame.Surface((self.player.size + 20, self.player.size + 20), pygame.SRCALPHA)
            center = (glow_surface.get_width() // 2, glow_surface.get_height() // 2)
            
            # Múltiples capas de glow
            for radius in range(15, 5, -2):
                alpha = int(self.glow_intensity * (radius / 15))
                # Asegurar que el color esté en el rango correcto
                pygame.draw.circle(glow_surface, (255, 255, 100, alpha), center, radius)
                
            surf.blit(glow_surface, 
                     (self.player.x - 10, self.player.y - 10), 
                     special_flags=pygame.BLEND_ADD)

class BossAura:
    def __init__(self, boss):
        self.boss = boss
        self.phase_colors = [RED, ORANGE, PURPLE, GOLD]
        self.aura_timer = 0
        
    def update(self, dt):
        self.aura_timer += dt
        
    def draw(self, surf):
        phase_index = self.boss.phase - 1
        if phase_index < 0 or phase_index >= len(self.phase_colors):
            return
            
        base_color = self.phase_colors[phase_index]
        center_x = self.boss.x + self.boss.w // 2
        center_y = self.boss.y + self.boss.h // 2
        
        # Aura pulsante
        pulse = math.sin(self.aura_timer * 3) * 5 + 10
        
        # Crear superficie para el aura
        aura_size = max(self.boss.w, self.boss.h) + int(pulse * 2)
        aura_surface = pygame.Surface((aura_size, aura_size), pygame.SRCALPHA)
        aura_center = (aura_size // 2, aura_size // 2)
        
        # Dibujar múltiples anillos concéntricos
        for i in range(3):
            radius = (aura_size // 2) - i * 8
            alpha = 50 - i * 15
            color = list(base_color)
            # Asegurar que el color esté en el rango correcto
            color = [max(0, min(255, c)) for c in color]
            color.append(alpha)
            
            pygame.draw.circle(aura_surface, color, aura_center, radius, 3)
            
        surf.blit(aura_surface, 
                 (center_x - aura_size // 2, center_y - aura_size // 2),
                 special_flags=pygame.BLEND_ADD)

# --- Efecto de Knockout Mejorado ---
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
        sonido_derrota.play()

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
            ok_rect = ok_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
            effect_surface.blit(ok_text, ok_rect)
            
            ko_font = pygame.font.SysFont("Arial", int(40 * self.scale))
            ko_text = ko_font.render("KNOCKOUT!", True, (255, 50, 50))
            ko_rect = ko_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            effect_surface.blit(ko_text, ko_rect)
        
        surf.blit(effect_surface, (0, 0))
        
# --- Sistema de Introducción ---
class IntroductionSystem:
    def __init__(self):
        self.active = True
        self.current_dialogue = 0
        self.dialogues = [
            {
                "speaker": "diablito",
                "text": "¡Je je je! Vi tu batalla con ese robot... Impresionante.",
                "position": "right"
            },
            {
                "speaker": "diablito", 
                "text": "Te propongo un trato, humano. Una batalla por tu alma.",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "¿Mi alma? Eres más astuto de lo que pareces.",
                "position": "left"
            },
            {
                "speaker": "player",
                "text": "Mi nombre es Jony, y tal vez sea un pecado aceptar...",
                "position": "left"
            },
            {
                "speaker": "player",
                "text": "Pero acepto tu apuesta.",
                "position": "left"
            },
            {
                "speaker": "player",
                "text": "¡Y te aseguro que soy el mejor que jamás vas a encontrar!",
                "position": "left"
            },
            {
                "speaker": "diablito",
                "text": "¡Excelente! Para que sea justo te dare 2 vidas mas.",
                "position": "right"
            },
            {
                "speaker": "diablito",
                "text": "Que comience nuestro duelo. ¡Muéstrame tu valía!",
                "position": "right"
            },
            {
                "speaker": "both",
                "text": "¡QUE COMIENCE EL DUELO POR EL ALMA!",
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
        self.particle_system = ParticleSystem()
        self.diablito_pulse = 0

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
        
        # Actualizar partículas
        self.particle_system.update(dt)
        self.diablito_pulse += dt
        
        # Agregar partículas aleatorias
        if random.random() < 0.1:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            color = random.choice([RED, PURPLE, ORANGE])
            # Asegurar que el color esté en el rango correcto
            safe_color = [max(0, min(255, c)) for c in color]
            self.particle_system.add_particles(x, y, safe_color, 1, 
                                             speed_range=(10, 30),
                                             size_range=(1, 3),
                                             lifetime_range=(1.0, 2.0))
        
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
        
        # Dibujar partículas de fondo
        self.particle_system.draw(surf)
        
        # Marco decorativo con efecto de pulso
        pulse = math.sin(self.diablito_pulse * 3) * 2 + 2
        pygame.draw.rect(surf, GREY, (20, 20, WIDTH-40, HEIGHT-40), int(4 + pulse), border_radius=10)
        pygame.draw.rect(surf, RED, (30, 30, WIDTH-60, HEIGHT-60), 2, border_radius=8)
        
        current_dialogue = self.dialogues[self.current_dialogue]
        
        # Dibujar personajes según quién habla
        if current_dialogue["speaker"] == "diablito" or current_dialogue["speaker"] == "both":
            if has_diablito_img:
                char_x = WIDTH - 350
                char_y = HEIGHT//2 - 150
                
                # Efecto de pulso para el diablito
                pulse_scale = 1.0 + math.sin(self.diablito_pulse * 4) * 0.05
                scaled_diablito = pygame.transform.scale(diablito_img, 
                                                       (int(300 * pulse_scale), 
                                                        int(300 * pulse_scale)))
                diablito_colored = scaled_diablito.copy()
                diablito_colored.fill(RED, special_flags=pygame.BLEND_RGBA_MULT)
                surf.blit(diablito_colored, (char_x, char_y))
        
        if current_dialogue["speaker"] == "player" or current_dialogue["speaker"] == "both":
            if has_player_nave_img:
                char_x = 50
                char_y = HEIGHT//2 - 100
                
                # Efecto sutil para el jugador
                player_alpha = 200 + int(math.sin(self.diablito_pulse * 2) * 55)
                player_nave_img.set_alpha(player_alpha)
                surf.blit(player_nave_img, (char_x, char_y))
        
        # Configurar posición del cuadro de diálogo
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
        
        # Dibujar cuadro de diálogo con efecto de brillo
        pygame.draw.rect(surf, (20, 20, 40), dialog_rect, border_radius=15)
        glow_alpha = int(abs(math.sin(self.diablito_pulse * 5)) * 100)
        glow_surface = pygame.Surface((dialog_rect.width, dialog_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (255, 50, 50, glow_alpha), 
                        glow_surface.get_rect(), border_radius=15)
        surf.blit(glow_surface, dialog_rect.topleft)
        pygame.draw.rect(surf, RED, dialog_rect, 3, border_radius=15)
        
        # Nombre del personaje
        speaker_names = {
            "diablito": "DIABLITO",
            "player": "JONY",
            "both": "DUELO POR EL ALMA"
        }
        
        name_colors = {
            "diablito": RED,
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
        
        # Indicador de continuación
        if self.can_advance:
            prompt_text = "Presiona X para continuar" if self.current_dialogue < len(self.dialogues) - 1 else "Presiona X para comenzar el duelo"
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
        self.particle_system = ParticleSystem()
        self.title_pulse = 0
        
    def update(self, dt):
        self.timer += dt
        self.title_pulse += dt
        
        # Actualizar partículas
        self.particle_system.update(dt)
        
        # Agregar partículas de estrellas
        if random.random() < 0.3:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            self.particle_system.add_particles(x, y, WHITE, 1,
                                             speed_range=(0, 0),
                                             size_range=(1, 3),
                                             lifetime_range=(2.0, 4.0))
        
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
        
        # Dibujar partículas de fondo
        self.particle_system.draw(surf)
        
        # Efecto de pulso para el título
        pulse_scale = 1.0 + math.sin(self.title_pulse * 3) * 0.1
        
        title_surface = title_font.render("NIVEL 2", True, RED)
        title_surface.set_alpha(self.alpha)
        scaled_title = pygame.transform.scale(title_surface, 
                                            (int(title_surface.get_width() * pulse_scale),
                                             int(title_surface.get_height() * pulse_scale)))
        title_rect = scaled_title.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        surf.blit(scaled_title, title_rect)
        
        subtitle_surface = dialogue_font.render("Un Alma que Tratar", True, RED)
        subtitle_surface.set_alpha(self.alpha)
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
        surf.blit(subtitle_surface, subtitle_rect)
        
        # Efecto de brillo
        if self.phase in [0, 1]:
            glow_alpha = int(abs(math.sin(self.title_pulse * 5)) * 100)
            glow_surface = pygame.Surface((title_rect.width + 40, title_rect.height + 40), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 0, 0, glow_alpha), 
                            glow_surface.get_rect(), border_radius=20)
            surf.blit(glow_surface, (title_rect.centerx - glow_surface.get_width()//2, 
                                   title_rect.centery - glow_surface.get_height()//2))
        
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill(BLACK)
            fade_surface.set_alpha(self.fade_alpha)
            surf.blit(fade_surface, (0, 0))

# --- Sistema de Resultados con Animación ---
class ResultsSystem:
    def __init__(self):
        self.active = False
        self.animation_timer = 0
        self.animation_duration = 2.0
        self.stats = {}
        self.grade = ""
        self.grade_color = WHITE
        self.motivational_phrase = ""
        self.particle_system = ParticleSystem()
        self.result_pulse = 0
        
    def show_results(self, player, continues_used, score, completion_time, boss_defeated):
        self.active = True
        self.animation_timer = 0
        
        accuracy = player.bullets_hit / player.bullets_shot if player.bullets_shot > 0 else 0
        
        self.grade, self.grade_color, self.motivational_phrase = self.calculate_grade(
            continues_used, player.damage_taken, accuracy, completion_time
        )
        
        self.stats = {
            "player_lives": player.lives,
            "player_max_lives": player.max_lives,
            "accuracy": accuracy,
            "score": score,
            "continues_used": continues_used,
            "completion_time": completion_time,
            "player_damage_taken": player.damage_taken,
            "player_bullets_hit": player.bullets_hit,
            "player_bullets_shot": player.bullets_shot,
            "boss_defeated": boss_defeated
        }
        
    def calculate_grade(self, continues_used, damage_taken, accuracy, completion_time):
        score = 100
        if continues_used > 0:
            score -= continues_used * 20
        if damage_taken > 0:
            score -= min(damage_taken * 3, 25)
        if accuracy < 0.6:
            score -= 5
        if completion_time > 150:
            score -= 5

        if score >= 90:
            return "A+", GOLD, "¡PERFECTO! Tu alma está a salvo"
        elif score >= 80:
            return "A", GREEN, "¡Excelente! El diablito no pudo con tu alma"
        elif score >= 70:
            return "B", BLUE, "¡Buen trabajo! Tu espíritu es fuerte"
        elif score >= 55:
            return "C", YELLOW, "¡Bien hecho! Tu alma sigue siendo tuya"
        else:
            return "D", ORANGE, "¡Por los pelos! Cuidado con los tratos futuros"
            
    def update(self, dt):
        if not self.active:
            return False
            
        self.animation_timer += dt
        self.result_pulse += dt
        
        # Actualizar partículas
        self.particle_system.update(dt)
        
        # Agregar partículas de confeti
        if self.animation_timer > 1.0 and random.random() < 0.2:
            x = random.randint(0, WIDTH)
            color = random.choice([RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE])
            # Asegurar que el color esté en el rango correcto
            safe_color = [max(0, min(255, c)) for c in color]
            self.particle_system.add_particles(x, -10, safe_color, 3,
                                             speed_range=(50, 150),
                                             size_range=(2, 5),
                                             lifetime_range=(2.0, 4.0),
                                             gravity=50)
            
        return self.animation_timer >= self.animation_duration
        
    def draw(self, surf):
        if not self.active:
            return
            
        progress = min(1.0, self.animation_timer / self.animation_duration)
        
        # Dibujar partículas
        self.particle_system.draw(surf)
        
        # Fondo con animación de fade in
        overlay_alpha = int(200 * progress)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, overlay_alpha))
        surf.blit(overlay, (0, 0))
        
        # Efecto de pulso
        pulse = math.sin(self.result_pulse * 5) * 0.1 + 1.0
        
        # Título con animación de escala
        title_scale = (0.5 + 0.5 * progress) * pulse
        title_text = title_font.render("¡VICTORIA NIVEL 2!", True, GOLD)
        title_rect = title_text.get_rect(center=(WIDTH//2, int(40 * progress)))
        scaled_title = pygame.transform.scale(title_text, 
                                            (int(title_text.get_width() * title_scale), 
                                             int(title_text.get_height() * title_scale)))
        surf.blit(scaled_title, scaled_title.get_rect(center=title_rect.center))
        
        # Calificación con fade in
        if progress > 0.2:
            grade_alpha = int(255 * min(1.0, (progress - 0.2) / 0.3))
            grade_text = large_font.render(f"Calificación: {self.grade}", True, self.grade_color)
            grade_text.set_alpha(grade_alpha)
            grade_rect = grade_text.get_rect(center=(WIDTH//2, 100))
            surf.blit(grade_text, grade_rect)
        
        # Estadísticas con animación secuencial
        stats_y = 160
        stats_list = [
            f"Tiempo: {self.stats['completion_time']:.1f} segundos",
            f"Puntuación: {self.stats['score']} puntos",
            f"Continues usados: {self.stats['continues_used']}",
            f"Daño recibido: {self.stats['player_damage_taken']} veces",
            f"Precisión: {self.stats['accuracy']*100:.1f}% ({self.stats['player_bullets_hit']}/{self.stats['player_bullets_shot']})",
            f"Vidas restantes: {self.stats['player_lives']}/{self.stats['player_max_lives']}"
        ]
        
        for i, stat in enumerate(stats_list):
            if progress > 0.3 + i * 0.1:
                stat_alpha = int(255 * min(1.0, (progress - 0.3 - i * 0.1) / 0.2))
                stat_text = font.render(stat, True, WHITE)
                stat_text.set_alpha(stat_alpha)
                stat_rect = stat_text.get_rect(center=(WIDTH//2, stats_y))
                surf.blit(stat_text, stat_rect)
            stats_y += 35
        
        # Frase motivacional
        if progress > 0.9:
            phrase_alpha = int(255 * (progress - 0.9) * 10)
            phrase_text = font.render(self.motivational_phrase, True, GREEN)
            phrase_text.set_alpha(phrase_alpha)
            phrase_rect = phrase_text.get_rect(center=(WIDTH//2, stats_y + 20))
            surf.blit(phrase_text, phrase_rect)
        
        # Instrucción para continuar
        if progress >= 1.0:
            instruction_alpha = int((pygame.time.get_ticks() % 1000) / 1000.0 * 255)
            instruction_text = font.render("Presiona ENTER para continuar al nivel 3", True, YELLOW)
            instruction_text.set_alpha(instruction_alpha)
            instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT - 60))
            surf.blit(instruction_text, instruction_rect)

# --- Clases del juego ---

class Player:
    def __init__(self):
        self.base_size = 48
        self.size = self.base_size
        self.x = 80
        self.y = HEIGHT // 2
        self.speed = 5.0
        self.base_speed = 5.0
        self.shrink_speed = 7.0
        self.lives = 5
        self.max_lives = 5
        self.shoot_cooldown = 0.1
        self.shoot_timer = 0.0
        self.is_shrunk = False
        self.rect = Rect(self.x, self.y, self.size, self.size)
        self.invulnerable = False
        self.invulnerable_timer = 0.0
        self.damage_taken = 0
        self.bullets_shot = 0
        self.bullets_hit = 0
        self.trail_particles = []
        self.glow_effect = PlayerGlow(self)

    def update(self, dt, keys):
        self.is_shrunk = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        if self.is_shrunk:
            self.size = int(self.base_size * 0.55)
            speed = self.shrink_speed
        else:
            self.size = self.base_size
            speed = self.base_speed

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

        # Agregar partículas de estela al moverse
        if (vx != 0 or vy != 0) and random.random() < 0.3:
            self.trail_particles.append({
                'x': self.x + self.size//2,
                'y': self.y + self.size//2,
                'size': random.uniform(1, 3),
                'timer': 0.5,
                'color': LIGHT_BLUE
            })

        # Actualizar partículas de estela
        for particle in self.trail_particles[:]:
            particle['timer'] -= dt
            particle['size'] *= 0.95
            if particle['timer'] <= 0:
                self.trail_particles.remove(particle)

        self.rect = Rect(int(self.x), int(self.y), self.size, self.size)

        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        # Actualizar efecto de glow
        self.glow_effect.update(dt)

    def draw(self, surf):
        # Dibujar partículas de estela
        for particle in self.trail_particles:
            alpha = int(255 * (particle['timer'] / 0.5))
            color = list(particle['color'])
            # Asegurar que el color esté en el rango correcto
            color = [max(0, min(255, c)) for c in color]
            color.append(alpha)
            pygame.draw.circle(surf, color, 
                             (int(particle['x']), int(particle['y'])), 
                             int(particle['size']))

        # Dibujar glow
        self.glow_effect.draw(surf)

        nave_scaled = pygame.transform.scale(nave_img_original, (self.size, self.size))
        if self.invulnerable and int(self.invulnerable_timer * 10) % 2 == 0:
            # Efecto de parpadeo cuando es invulnerable
            nave_scaled.set_alpha(128)
        else:
            nave_scaled.set_alpha(255)
            
        surf.blit(nave_scaled, (self.x, self.y))

    def can_shoot(self):
        return (not self.is_shrunk) and self.shoot_timer <= 0

    def shoot(self):
        self.shoot_timer = self.shoot_cooldown
        self.bullets_shot += 1

    def take_damage(self):
        if not self.invulnerable:
            self.lives -= 1
            self.damage_taken += 1
            sonido_daño.play()
            self.invulnerable = True
            self.invulnerable_timer = 2.0
            self.x = max(0, self.x - 40)

    def add_lives(self, amount):
        self.lives += amount
        if self.lives > self.max_lives:
            self.lives = self.max_lives

class Bullet:
    def __init__(self, x, y, vx, vy, color=GREEN, owner="player", size=6, homing=False, speed_factor=1.0):  # Cambiado a GREEN por defecto
        self.x = x
        self.y = y
        self.vx = vx * speed_factor
        self.vy = vy * speed_factor
        self.radius = size
        # Asegurar que el color esté en el rango correcto
        self.color = [max(0, min(255, c)) for c in color]
        self.owner = owner
        self.homing = homing
        self.speed_factor = speed_factor
        self.rect = Rect(int(self.x-self.radius), int(self.y-self.radius), self.radius*2, self.radius*2)

    def update(self, dt, player=None):
        if self.homing and player and self.owner == "boss":
            dx = player.x + player.size/2 - self.x
            dy = player.y + player.size/2 - self.y
            dist = math.hypot(dx, dy) or 1
            self.vx += dx/dist * 100 * dt
            self.vy += dy/dist * 100 * dt
            speed = math.hypot(self.vx, self.vy)
            if speed > 300 * self.speed_factor:
                self.vx = self.vx / speed * 300 * self.speed_factor
                self.vy = self.vy / speed * 300 * self.speed_factor
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)

class Obstacle:
    def __init__(self, phase=1):
        self.w = random.randint(40, 60)
        self.h = random.randint(40, 60)
        self.x = WIDTH + random.randint(20, 100)
        self.y = random.randint(40, HEIGHT-80)
        base_speed = random.randint(120, 180)
        if phase >= 3:
            base_speed = random.randint(180, 220)
        self.speed = base_speed
        self.zigzag = random.choice([-1,1])
        self.zigzag_speed = random.randint(80, 120)
        self.rect = Rect(self.x, self.y, self.w, self.h)

    def update(self, dt):
        self.x -= self.speed * dt
        self.y += self.zigzag * self.zigzag_speed * dt
        if self.y < 0 or self.y + self.h > HEIGHT:
            self.zigzag *= -1
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        if has_obstacle_img:
            scaled_img = pygame.transform.scale(obstacle_img, (self.w, self.h))
            surf.blit(scaled_img, (self.x, self.y))
        else:
            pygame.draw.rect(surf, GREY, self.rect, border_radius=8)

class MiniEnemy:
    def __init__(self, x, y, enemy_type="basic"):
        self.size = 30
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.rect = Rect(self.x, self.y, self.size, self.size)
        self.shoot_cooldown = 2.0 if enemy_type == "basic" else 1.5
        self.shoot_timer = random.uniform(1.0, 2.0)
        self.health = 1
        self.move_timer = 0
        self.move_direction = random.choice([-1, 1])
        
        if enemy_type == "fast":
            self.color = CYAN
            self.shoot_cooldown = 1.2
        elif enemy_type == "tank":
            self.color = ORANGE
            self.health = 2
            self.size = 40
        else:
            self.color = YELLOW

    def update(self, dt, enemy_bullets, player):
        self.move_timer += dt
        if self.move_timer > 1.5:
            self.move_timer = 0
            self.move_direction = random.choice([-1, 1])
        
        self.y += self.move_direction * 60 * dt
        self.y = max(50, min(HEIGHT - 50, self.y))
        
        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_cooldown
            self.shoot(enemy_bullets, player)
        
        self.rect.topleft = (int(self.x), int(self.y))

    def shoot(self, enemy_bullets, player):
        if self.enemy_type == "basic":
            dx = player.x + player.size/2 - self.x
            dy = player.y + player.size/2 - self.y
            dist = math.hypot(dx,dy) or 1
            speed = 220
            enemy_bullets.append(Bullet(self.x, self.y, dx/dist*speed, dy/dist*speed, color=RED, owner="boss"))
        
        elif self.enemy_type == "fast":
            for i in range(2):
                angle_variation = random.uniform(-0.1, 0.1)
                dx = player.x + player.size/2 - self.x
                dy = player.y + player.size/2 - self.y
                dist = math.hypot(dx,dy) or 1
                speed = 250
                enemy_bullets.append(Bullet(self.x, self.y, 
                                          dx/dist*speed + random.uniform(-30,30), 
                                          dy/dist*speed + random.uniform(-30,30), 
                                          color=PURPLE, owner="boss", size=4))
        
        elif self.enemy_type == "tank":
            dx = player.x + player.size/2 - self.x
            dy = player.y + player.size/2 - self.y
            dist = math.hypot(dx,dy) or 1
            speed = 180
            enemy_bullets.append(Bullet(self.x, self.y, dx/dist*speed, dy/dist*speed, 
                                      color=ORANGE, owner="boss", size=8, homing=True, speed_factor=0.6))

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

    def draw(self, surf):
        if self.enemy_type == "basic" and has_basic_enemy_img:
            scaled_img = pygame.transform.scale(basic_enemy_img, (self.size, self.size))
            surf.blit(scaled_img, (self.x, self.y))
        elif self.enemy_type == "fast" and has_fast_enemy_img:
            scaled_img = pygame.transform.scale(fast_enemy_img, (self.size, self.size))
            surf.blit(scaled_img, (self.x, self.y))
        elif self.enemy_type == "tank" and has_tank_enemy_img:
            scaled_img = pygame.transform.scale(tank_enemy_img, (self.size, self.size))
            surf.blit(scaled_img, (self.x, self.y))
        else:
            pygame.draw.rect(surf, self.color, self.rect, border_radius=6)
        
        if self.enemy_type == "tank" and self.health < 2:
            health_width = (self.size * self.health) // 2
            health_rect = Rect(self.x, self.y - 8, health_width, 4)
            pygame.draw.rect(surf, GREEN, health_rect)

class Boss:
    def __init__(self):
        self.w = 200
        self.h = 200
        self.x = WIDTH + 200
        self.y = (HEIGHT - self.h) // 2
        self.max_hp = 8000
        self.hp = self.max_hp
        self.phase = 1
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.attack_timer = 3.0
        self.attack_cooldown = 2.5
        self.dir = 1
        self.entering = True
        self.exiting = False
        self.mini_enemies = []
        self.special_attack_timer = 0
        self.move_timer = 0
        self.move_cooldown = 1.5
        self.aura_effect = BossAura(self)
        self.phase_transition = False
        self.phase_transition_timer = 0
        self.phase2_flash_timer = 0
        self.phase2_flash_duration = 1.0
        self.phase2_flash_active = False
        self.old_phase = 1  # Para detectar cambios de fase

    def update(self, dt, enemy_bullets, player, obstacles, fight_started):
        if self.entering:
            self.x -= 200*dt
            if self.x <= WIDTH - self.w - 40:
                self.entering = False
            self.rect.topleft = (int(self.x), int(self.y))
            return
            
        if self.exiting:
            self.x += 200*dt
            self.rect.topleft = (int(self.x), int(self.y))
            return

        # Detectar cambio de fase
        self.old_phase = self.phase
        ratio = self.hp / self.max_hp
        if ratio > 0.75:
            self.phase = 1
        elif ratio > 0.5:
            self.phase = 2
        elif ratio > 0.25:
            self.phase = 3
        else:
            self.phase = 4
            
        # Activar transición de fase si cambió
        if self.old_phase != self.phase and not self.phase_transition:
            self.phase_transition = True
            self.phase_transition_timer = 1.5
            screen_shake.start_shake(10, 1.0)
            
            # Efecto especial para fase 2
            if self.phase == 2:
                self.phase2_flash_active = True
                self.phase2_flash_timer = self.phase2_flash_duration
        
        # Actualizar flash de fase 2
        if self.phase2_flash_active:
            self.phase2_flash_timer -= dt
            if self.phase2_flash_timer <= 0:
                self.phase2_flash_active = False

        # Actualizar transición de fase
        if self.phase_transition:
            self.phase_transition_timer -= dt
            if self.phase_transition_timer <= 0:
                self.phase_transition = False

        self.move_timer += dt
        if self.move_timer >= self.move_cooldown:
            self.move_timer = 0
            self.move_cooldown = random.uniform(1.5, 2.0)
            self.dir *= -1
        
        self.y += self.dir * 80 * dt
        self.y = max(50, min(HEIGHT - self.h - 50, self.y))

        if not fight_started:
            return

        self.attack_timer -= dt
        self.special_attack_timer -= dt

        if self.attack_timer <= 0:
            self.execute_attack(enemy_bullets, player, obstacles)

        if self.special_attack_timer <= 0:
            self.execute_special_attack(enemy_bullets, player)
            self.special_attack_timer = random.uniform(5.0, 8.0)

        for m in self.mini_enemies[:]:
            m.update(dt, enemy_bullets, player)
            if m.x < -50:
                self.mini_enemies.remove(m)

        self.rect.topleft = (int(self.x), int(self.y))
        
        # Actualizar efectos visuales
        self.aura_effect.update(dt)

    def execute_attack(self, enemy_bullets, player, obstacles):
        if self.phase == 1:
            self.attack_cooldown = 2.0
            self.attack_timer = self.attack_cooldown
            self.attack_simple_spiral(enemy_bullets)
        elif self.phase == 2:
            self.attack_cooldown = 1.8
            self.attack_timer = self.attack_cooldown
            self.attack_aimed_shots(enemy_bullets, player)
        elif self.phase == 3:
            self.attack_cooldown = 1.6
            self.attack_timer = self.attack_cooldown
            self.attack_wave_pattern(enemy_bullets)
        elif self.phase == 4:
            self.attack_cooldown = 1.4
            self.attack_timer = self.attack_cooldown
            self.attack_simple_cross(enemy_bullets)

    def execute_special_attack(self, enemy_bullets, player):
        if self.phase == 1:
            self.spawn_mini_enemies(1, "basic")
        elif self.phase == 2:
            self.spawn_mini_enemies(2, "basic")
        elif self.phase == 3:
            self.spawn_mini_enemies(1, "fast")
            self.attack_homing_missiles(enemy_bullets, player, 2)
        elif self.phase == 4:
            self.spawn_mini_enemies(1, "fast")
            self.spawn_mini_enemies(1, "tank")
            self.attack_homing_missiles(enemy_bullets, player, 3)

    def attack_simple_spiral(self, enemy_bullets):
        cx = self.x
        cy = self.y + self.h//2
        for i in range(8):
            angle = i * math.pi / 4
            vx = -280 * math.cos(angle)
            vy = 280 * math.sin(angle)
            enemy_bullets.append(Bullet(cx, cy, vx, vy, color=RED, owner="boss"))
        # Efecto visual
        boss_attack_effects.add_phase_effect(cx, cy, 1)
        screen_shake.start_shake(3, 0.2)

    def attack_aimed_shots(self, enemy_bullets, player):
        cx = self.x
        cy = self.y + self.h//2
        for i in range(3):
            dx = player.x + player.size/2 - cx
            dy = player.y + player.size/2 - cy
            dist = math.hypot(dx,dy) or 1
            variation = random.uniform(-0.2, 0.2)
            dx_varied = dx + variation * 100
            dy_varied = dy + variation * 100
            dist_varied = math.hypot(dx_varied, dy_varied) or 1
            speed = 300
            enemy_bullets.append(Bullet(cx, cy, dx_varied/dist_varied*speed, dy_varied/dist_varied*speed, color=RED, owner="boss"))
        # Efecto visual
        boss_attack_effects.add_phase_effect(cx, cy, 2)
        screen_shake.start_shake(4, 0.3)

    def attack_wave_pattern(self, enemy_bullets):
        cx = self.x
        cy = self.y + self.h//2
        for i in range(6):
            angle = math.radians(i * 60)
            wave_offset = math.sin(pygame.time.get_ticks() * 0.005) * 0.3
            vx = -320 * math.cos(angle + wave_offset)
            vy = 320 * math.sin(angle + wave_offset)
            enemy_bullets.append(Bullet(cx, cy, vx, vy, color=PURPLE, owner="boss"))
        # Efecto visual
        boss_attack_effects.add_phase_effect(cx, cy, 3)
        screen_shake.start_shake(5, 0.4)

    def attack_simple_cross(self, enemy_bullets):
        cx = self.x
        cy = self.y + self.h//2
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            rad = math.radians(angle)
            vx = -300 * math.cos(rad)
            vy = 300 * math.sin(rad)
            enemy_bullets.append(Bullet(cx, cy, vx, vy, color=ORANGE, owner="boss"))
        # Efecto visual
        boss_attack_effects.add_phase_effect(cx, cy, 4)
        screen_shake.start_shake(6, 0.5)

    def attack_homing_missiles(self, enemy_bullets, player, count):
        cx = self.x
        cy = self.y + self.h//2
        for i in range(count):
            angle = math.radians(random.uniform(0, 360))
            vx = -180 * math.cos(angle)
            vy = 180 * math.sin(angle)
            enemy_bullets.append(Bullet(cx, cy, vx, vy, color=ORANGE, owner="boss", 
                                      homing=True, size=8, speed_factor=0.7))
        # Efecto visual
        boss_attack_effects.add_special_effect(cx, cy, "homing")
        screen_shake.start_shake(4, 0.4)

    def spawn_mini_enemies(self, count, enemy_type):
        for i in range(count):
            x = self.x - random.randint(50, 120)
            y = random.randint(80, HEIGHT-80)
            self.mini_enemies.append(MiniEnemy(x, y, enemy_type))
        # Efecto visual
        boss_attack_effects.add_special_effect(self.x, self.y, "spawn")

    def draw(self, surf):
        # Dibujar aura
        self.aura_effect.draw(surf)
        
        # Dibujar el jefe normalmente sin cuadro blanco
        if self.hp > 0:
            surf.blit(boss_img, (self.x, self.y))

        # Barra de vida mejorada
        bar_w = 220
        bar_h = 18
        bar_x = WIDTH - bar_w - 20
        bar_y = 12
        
        # Fondo con borde
        pygame.draw.rect(surf, (40, 40, 40), (bar_x-2, bar_y-2, bar_w+4, bar_h+4))
        pygame.draw.rect(surf, (80,80,80), (bar_x, bar_y, bar_w, bar_h))
        
        # Barra de vida con gradiente
        hp_fraction = max(0, self.hp / self.max_hp)
        health_width = int(bar_w * hp_fraction)
        
        if health_width > 0:
            for i in range(health_width):
                progress = i / health_width
                if hp_fraction > 0.6:
                    color = (int(200 * (1 - progress)), 200, 40)  # Verde a amarillo
                elif hp_fraction > 0.3:
                    color = (200, int(200 * progress), 40)  # Amarillo a naranja
                else:
                    color = (200, int(80 * progress), 40)  # Naranja a rojo
                    
                pygame.draw.rect(surf, color, (bar_x + i, bar_y, 1, bar_h))
        
        # Texto mejorado
        phase_names = ["I - Furia", "II - Desesperación", "III - Oscuridad", "IV - Final"]
        hp_text = font.render(f"Diablito - {phase_names[self.phase-1]} | HP: {self.hp}/{self.max_hp}", 
                            True, WHITE)
        surf.blit(hp_text, (bar_x, bar_y + bar_h + 2))

        for m in self.mini_enemies:
            m.draw(surf)

# --- Funciones auxiliares ---
def rect_circle_collide(rect: Rect, circle_x, circle_y, radius):
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))
    dx = circle_x - closest_x
    dy = circle_y - closest_y
    return dx*dx + dy*dy <= radius*radius

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
        pygame.mixer.music.load("sound/f3.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except:
        print("No se pudo cargar la música normal")

# --- Estado del juego ---
player = Player()
boss = Boss()
player_bullets = []
enemy_bullets = []
obstacles = []
score = 0
game_over = False
level_cleared = False
fight_timer = 0.0
fight_started = False
boss_defeated_sound_played = False

# Sistema de continuación
continue_countdown = 0
continue_time = 12.0
coins_inserted = 0
continues_used = 0
continue_available = True
lives_per_coin = 3

# Estadísticas
game_start_time = 0
completion_time = 0
victory_sound_played = False
victory_music_playing = False

scroll_x = 0
vel_fondo = 100

# Nuevos sistemas
title_screen = TitleScreen()
introduction = IntroductionSystem()
knockout_effect = KnockoutEffect()
results_system = ResultsSystem()

# Nuevos sistemas de efectos
screen_shake = ScreenShake()
hit_effect = HitEffect()
boss_attack_effects = BossAttackEffects()
bullet_trail = BulletTrail()

# --- Variables para el efecto de flash del fondo ---
fondo_flash_timer = 0
fondo_flash_duration = 0.8
fondo_flash_active = False
current_fondo = fondo_img
target_fondo = fondo_fase2_img

# --- Main loop ---
running = True
game_start_time = pygame.time.get_ticks()

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
                    if len(boss.mini_enemies) > 2:
                        boss.mini_enemies = boss.mini_enemies[:2]
                    player.x = 80
                    player.y = HEIGHT // 2
            if event.key == pygame.K_RETURN and results_system.active and results_system.animation_timer >= results_system.animation_duration:
                running = False
                pygame.quit()
                subprocess.run([sys.executable, "nivel3.py"])
                sys.exit()
            if event.key == pygame.K_x and introduction.active:
                result = introduction.advance_text()
                if result == "start_battle":
                    play_normal_music()
                    fight_started = True
                    sonido_inicio.play()

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

    # Efecto de knockout
    if knockout_effect.active:
        knockout_finished = knockout_effect.update(dt)
        if knockout_finished:
            knockout_effect.active = False
            results_system.show_results(player, continues_used, score, completion_time, True)

    # Sistema de resultados
    if results_system.active:
        results_system.update(dt)
        results_system.draw(screen)
        pygame.display.flip()
        continue

    # Actualizar efectos
    screen_shake.update(dt)
    hit_effect.update(dt)
    boss_attack_effects.update(dt)
    bullet_trail.update(dt)

    # Actualizar conteo regresivo
    if continue_countdown > 0:
        continue_countdown -= dt
        if continue_countdown <= 0:
            continue_countdown = 0
            game_over = True

    # Detectar cambio de fase del jefe para activar flash de fondo
    if boss.old_phase == 1 and boss.phase == 2 and not fondo_flash_active:
        fondo_flash_active = True
        fondo_flash_timer = fondo_flash_duration
        current_fondo = fondo_img
        target_fondo = fondo_fase2_img

    # Actualizar efecto de flash del fondo
    if fondo_flash_active:
        fondo_flash_timer -= dt
        if fondo_flash_timer <= 0:
            fondo_flash_active = False
            current_fondo = target_fondo

    if not game_over and not level_cleared and continue_countdown == 0 and not results_system.active:
        fight_timer += dt
        
        player.update(dt, keys)

        if fight_started and keys[pygame.K_x] and player.can_shoot():
            bx = player.x + player.size + 6
            by = player.y + player.size/2
            bullet = Bullet(bx, by, 600, 0, color=GREEN, owner="player")  # Balas verdes normales
            player_bullets.append(bullet)
            bullet_trail.add_trail(bx, by, GREEN, "player")
            player.shoot()

        boss.update(dt, enemy_bullets, player, obstacles, fight_started)

        for b in enemy_bullets[:]:
            b.update(dt, player)
            bullet_trail.add_trail(b.x, b.y, b.color, "boss")
            if b.x < -50 or b.y < -50 or b.y > HEIGHT+50:
                enemy_bullets.remove(b)
                continue
            if rect_circle_collide(player.rect, b.x, b.y, b.radius):
                player.take_damage()
                hit_effect.add_hit(b.x, b.y, b.color, 12)
                screen_shake.start_shake(8, 0.3)
                if b in enemy_bullets:
                    enemy_bullets.remove(b)

        for b in player_bullets[:]:
            b.update(dt)
            bullet_trail.add_trail(b.x, b.y, b.color, "player")
            if b.x > WIDTH+50:
                player_bullets.remove(b)
                continue
            if rect_circle_collide(boss.rect, b.x, b.y, b.radius) and not boss.entering:
                boss.hp -= 12
                player.bullets_hit += 1
                hit_effect.add_hit(b.x, b.y, b.color, 8)
                screen_shake.start_shake(4, 0.2)
                if b in player_bullets:
                    player_bullets.remove(b)
                score += 5
                if boss.hp <= 0 and not boss_defeated_sound_played:
                    boss_defeated_sound_played = True
                    knockout_effect.activate()
            
            for m in boss.mini_enemies[:]:
                if rect_circle_collide(m.rect, b.x, b.y, b.radius):
                    if m.take_damage():
                        boss.mini_enemies.remove(m)
                        hit_effect.add_hit(b.x, b.y, m.color, 10)
                        score += 25
                    if b in player_bullets:
                        player_bullets.remove(b)
                    break

        if random.random() < 0.01 and fight_started:
            obstacles.append(Obstacle(boss.phase))

        for obs in obstacles[:]:
            obs.update(dt)
            if obs.x < -100:
                obstacles.remove(obs)
                continue
            if player.rect.colliderect(obs.rect):
                player.take_damage()
                hit_effect.add_hit(player.x + player.size/2, player.y + player.size/2, GREY, 15)
                screen_shake.start_shake(10, 0.4)
                obstacles.remove(obs)

        if player.rect.colliderect(boss.rect) and not boss.entering:
            player.take_damage()
            hit_effect.add_hit(player.x + player.size/2, player.y + player.size/2, RED, 20)
            screen_shake.start_shake(12, 0.5)

        if player.lives <= 0 and continue_available:
            continue_countdown = continue_time
            coins_inserted = 0

        if boss.hp <= 0 and not boss.exiting:
            boss.exiting = True
            pygame.mixer.music.stop()
            completion_time = (pygame.time.get_ticks() - game_start_time) / 1000.0

    # --- Dibujado ---
    scroll_x -= vel_fondo * dt
    if scroll_x <= -WIDTH:
        scroll_x = 0
    
    # Aplicar screen shake
    shake_offset = screen_shake.get_offset()
    
    # Dibujar fondo con efecto de flash
    if fondo_flash_active:
        # Efecto de flash intermitente durante la transición
        flash_progress = 1.0 - (fondo_flash_timer / fondo_flash_duration)
        if flash_progress < 0.5:
            # Primera mitad: fondo original con flash blanco
            flash_intensity = int(math.sin(flash_progress * math.pi * 10) * 200)
            screen.blit(current_fondo, (int(scroll_x) + shake_offset[0], 0 + shake_offset[1]))
            screen.blit(current_fondo, (int(scroll_x)+WIDTH + shake_offset[0], 0 + shake_offset[1]))
            
            flash_surface = pygame.Surface((WIDTH, HEIGHT))
            flash_surface.fill(WHITE)
            flash_surface.set_alpha(flash_intensity)
            screen.blit(flash_surface, (0, 0))
        else:
            # Segunda mitad: nuevo fondo aparece gradualmente
            new_alpha = int((flash_progress - 0.5) * 2 * 255)
            screen.blit(current_fondo, (int(scroll_x) + shake_offset[0], 0 + shake_offset[1]))
            screen.blit(current_fondo, (int(scroll_x)+WIDTH + shake_offset[0], 0 + shake_offset[1]))
            
            target_fondo.set_alpha(new_alpha)
            screen.blit(target_fondo, (int(scroll_x) + shake_offset[0], 0 + shake_offset[1]))
            screen.blit(target_fondo, (int(scroll_x)+WIDTH + shake_offset[0], 0 + shake_offset[1]))
    else:
        # Fondo normal según la fase
        if boss.phase >= 2 and has_fondo_fase2:
            screen.blit(target_fondo, (int(scroll_x) + shake_offset[0], 0 + shake_offset[1]))
            screen.blit(target_fondo, (int(scroll_x)+WIDTH + shake_offset[0], 0 + shake_offset[1]))
        else:
            screen.blit(current_fondo, (int(scroll_x) + shake_offset[0], 0 + shake_offset[1]))
            screen.blit(current_fondo, (int(scroll_x)+WIDTH + shake_offset[0], 0 + shake_offset[1]))

    # Dibujar efectos de balas
    bullet_trail.draw(screen)
    
    for b in player_bullets:
        b.draw(screen)
    for b in enemy_bullets:
        b.draw(screen)
    for obs in obstacles:
        obs.draw(screen)

    # Dibujar efectos del jefe
    boss_attack_effects.draw(screen)
    
    boss.draw(screen)
    
    # Dibujar efectos de golpe
    hit_effect.draw(screen)
    
    knockout_effect.draw(screen)
    
    if continue_countdown == 0 and not results_system.active:
        player.draw(screen)

    lives_text = font.render(f"Vidas: {player.lives}", True, WHITE)
    screen.blit(lives_text, (12 + shake_offset[0], 12 + shake_offset[1]))
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (12 + shake_offset[0], 36 + shake_offset[1]))

    if not fight_started and not introduction.active:
        wait_txt = font.render("Presiona X para comenzar el duelo", True, GREY)
        screen.blit(wait_txt, (WIDTH//2 - wait_txt.get_width()//2 + shake_offset[0], HEIGHT-30 + shake_offset[1]))

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
        screen.blit(lives_info, (WIDTH//2 - lives_info.get_width()//2, HEIGHT//2 + 100))

    if game_over and continue_countdown == 0:
        over_surf = font.render("GAME OVER - Presiona ESC para salir", True, RED)
        screen.blit(over_surf, (WIDTH//2 - over_surf.get_width()//2, HEIGHT//2 - 20))

    pygame.display.flip()

pygame.quit()