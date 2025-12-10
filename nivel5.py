import pygame
import random
import math
import subprocess
import sys
from pygame import Rect

# --- Configuración ---
WIDTH, HEIGHT = 960, 540
FPS = 90

# Colores
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
CYAN = (80, 220, 220)  # NUEVO: Color cian para las balas del jugador
DARK_RED = (139, 0, 0)
BROWN = (139, 69, 19)
PINK = (255, 105, 180)
LIME = (50, 255, 50)
DARK_BROWN = (101, 67, 33)
HUNTER_GREEN = (53, 94, 59)
FOREST_GREEN = (34, 139, 34)
MOONLIGHT = (200, 200, 230)
BLOOD_RED = (138, 3, 3)
NEON_RED = (255, 20, 20)
BRIGHT_YELLOW = (255, 255, 100)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nivel 5 - Suerte de Cazador")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 48)
dialogue_font = pygame.font.SysFont("Arial", 28)

# --- Cargar imágenes para la introducción ---
try:
    laynes_img = pygame.image.load("img/laynes.png").convert_alpha()
    laynes_img = pygame.transform.scale(laynes_img, (250, 250))
    has_laynes_img = True
except:
    print("No se pudo cargar laynes.png")
    has_laynes_img = False

try:
    niño_img = pygame.image.load("img/nave.png").convert_alpha()
    niño_img = pygame.transform.scale(niño_img, (250, 250))
    has_niño_img = True
except:
    print("No se pudo cargar niño.png")
    has_niño_img = False

try:
    cazador_img = pygame.image.load("img/cazador.png").convert_alpha()
    cazador_img = pygame.transform.scale(cazador_img, (280, 280))
    has_cazador_img = True
except:
    print("No se pudo cargar cazador.png")
    has_cazador_img = False

try:
    cazador_jaula_img = pygame.image.load("img/Cazador_Jaula.png").convert_alpha()
    cazador_jaula_img = pygame.transform.scale(cazador_jaula_img, (350, 350))
    has_cazador_jaula_img = True
except:
    print("No se pudo cargar cazador_jaula.png")
    has_cazador_jaula_img = False

# Cargar imagen "MORIR"
try:
    morir_img = pygame.image.load("img/morir.png").convert_alpha()
    morir_img = pygame.transform.scale(morir_img, (400, 200))
    has_morir_img = True
except:
    print("No se pudo cargar morir.png, se usará texto alternativo")
    has_morir_img = False

# Imágenes del juego
try:
    fondo_img_original = pygame.image.load("img/bosquetetrico.png").convert()
    fondo_img_original = pygame.transform.scale(fondo_img_original, (WIDTH * 2, HEIGHT))  # Doble ancho para scroll
    has_fondo_img = True
except:
    print("No se pudo cargar bosque_tetrico.png, usando fondo por defecto")
    has_fondo_img = False

try:
    nave_img_original = pygame.image.load("img/nave.png").convert_alpha()
    has_nave_img = True
except:
    print("No se pudo cargar nave.png")
    has_nave_img = False

try:
    boss_img = pygame.image.load("img/cazador2.png").convert_alpha()
    boss_img = pygame.transform.scale(boss_img, (150, 200))
    has_boss_img = True
except:
    print("No se pudo cargar cazador_boss.png, usando imagen por defecto")
    boss_img = pygame.Surface((150, 200))
    boss_img.fill(DARK_BROWN)
    has_boss_img = False

# Cargar imagen de mira para fase 1
try:
    mira_img = pygame.image.load("img/mira.png").convert_alpha()
    mira_img = pygame.transform.scale(mira_img, (40, 40))
    has_mira_img = True
except:
    print("No se pudo cargar mira.png")
    has_mira_img = False

# Cargar imagen de murciélago - AUMENTADO EL TAMAÑO
try:
    bat_img = pygame.image.load("img/murcielago.png").convert_alpha()
    bat_img = pygame.transform.scale(bat_img, (60, 45))  # CAMBIADO: De 40x30 a 60x45
    has_bat_img = True
except:
    print("No se pudo cargar murcielago.png")
    has_bat_img = False

# Cargar GIF del knockout
try:
    ok_image = pygame.image.load("img/ok.png").convert_alpha()
    ok_image = pygame.transform.scale(ok_image, (320, 180))
    has_ok_image = True
except:
    print("No se pudo cargar ok.png, se usará texto alternativo")
    has_ok_image = False

# --- Música y sonidos ---
try:
    pygame.mixer.music.load("sound/waidmanns_heil.mp3")
    pygame.mixer.music.set_volume(0.5)
    has_music = True
except:
    print("No se pudo cargar waidmanns_heil.mp3")
    has_music = False

# Sonidos
sonido_inicio = pygame.mixer.Sound("sound/inicio1.mp3") if pygame.mixer.get_init() else None
sonido_daño = pygame.mixer.Sound("sound/hit.mp3") if pygame.mixer.get_init() else None
sonido_coin = pygame.mixer.Sound("sound/coin2.mp3") if pygame.mixer.get_init() else None
sonido_victoria = pygame.mixer.Sound("sound/victoria.mp3") if pygame.mixer.get_init() else None
sonido_misil = pygame.mixer.Sound("sound/misil.mp3") if pygame.mixer.get_init() else None
sonido_fase = pygame.mixer.Sound("sound/coin.mp3") if pygame.mixer.get_init() else None
sonido_texto = pygame.mixer.Sound("sound/text.mp3") if pygame.mixer.get_init() else None

# Efectos especiales
try:
    sonido_trueno = pygame.mixer.Sound("sound/trueno.mp3")
    sonido_trueno.set_volume(1.5)  # CAMBIADO: Aumentado de 1.0 a 1.5
    has_trueno_sound = True
except:
    print("No se pudo cargar trueno.mp3")
    has_trueno_sound = False

try:
    sonido_disparo = pygame.mixer.Sound("sound/disparo.mp3")
    has_disparo_sound = True
except:
    print("No se pudo cargar disparo.mp3")
    has_disparo_sound = False

try:
    sonido_knockout = pygame.mixer.Sound("sound/kn.mp3")
    has_knockout_sound = True
except:
    print("No se pudo cargar kn.mp3")
    has_knockout_sound = False

# --- Sistema de Scroll Horizontal ---
class HorizontalScroll:
    def __init__(self):
        self.scroll_x = 0
        self.base_speed = 100
        self.current_speed = self.base_speed
        self.max_speed = 800
        self.target_speed = self.base_speed
        self.acceleration = 0
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        
    def activate_speed_boost(self, target_speed=600, duration=9999.0):
        self.target_speed = target_speed
        self.speed_boost_active = True
        self.speed_boost_timer = duration
        self.acceleration = (target_speed - self.current_speed) / 1.0
        
    def deactivate_speed_boost(self):
        self.speed_boost_active = False
        self.target_speed = self.base_speed
        self.acceleration = (self.base_speed - self.current_speed) / 2.0
        
    def update(self, dt):
        self.scroll_x -= self.current_speed * dt
        
        if self.scroll_x <= -WIDTH:
            self.scroll_x = 0
            
        if self.speed_boost_active:
            self.speed_boost_timer -= dt
                
        if abs(self.current_speed - self.target_speed) > 1:
            self.current_speed += self.acceleration * dt
            self.current_speed = max(self.base_speed, min(self.max_speed, self.current_speed))
        else:
            self.current_speed = self.target_speed
            
    def get_scroll_offset(self):
        return self.scroll_x
        
    def is_high_speed(self):
        return self.current_speed > 400

# --- Sistema de Partículas para efecto de sangre/hojas ---
class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.max_particles = 100
        
    def create_blood_burst(self, x, y, count=15):
        for _ in range(min(count, self.max_particles - len(self.particles))):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 200)
            lifetime = random.uniform(1.0, 3.0)
            size = random.randint(3, 8)
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': random.choice([BLOOD_RED, DARK_RED, RED]),
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'size': size,
                'type': 'blood'
            })
            
    def create_leaf_particles(self, count=5):
        for _ in range(min(count, self.max_particles - len(self.particles))):
            self.particles.append({
                'x': random.randint(0, WIDTH),
                'y': -10,
                'vx': random.uniform(-20, 20),
                'vy': random.uniform(30, 80),
                'color': random.choice([BROWN, FOREST_GREEN, HUNTER_GREEN]),
                'lifetime': random.uniform(3.0, 6.0),
                'max_lifetime': 6.0,
                'size': random.randint(2, 4),
                'type': 'leaf',
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-1, 1)
            })
            
    def create_bat_particles(self, x, y, count=8):
        for _ in range(min(count, self.max_particles - len(self.particles))):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(20, 100)
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': (50, 50, 50),
                'lifetime': random.uniform(0.5, 1.5),
                'max_lifetime': 1.5,
                'size': random.randint(2, 4),
                'type': 'bat_dust'
            })
            
    def create_speed_lines(self, count=10):
        for _ in range(min(count, self.max_particles - len(self.particles))):
            self.particles.append({
                'x': WIDTH,
                'y': random.randint(0, HEIGHT),
                'vx': random.uniform(-800, -400),
                'vy': 0,
                'color': BRIGHT_YELLOW,
                'lifetime': random.uniform(0.5, 1.0),
                'max_lifetime': 1.0,
                'size': random.randint(2, 5),
                'type': 'speed_line'
            })
            
    def update(self, dt):
        for p in self.particles[:]:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['lifetime'] -= dt
            
            if p['type'] == 'blood':
                p['vy'] += 50 * dt
                
            if p['type'] == 'leaf':
                p['vy'] += 10 * dt
                p['vx'] += math.sin(pygame.time.get_ticks() * 0.001) * 20 * dt
                p['rotation'] += p['rotation_speed']
                
            if p['type'] == 'bat_dust':
                p['vy'] -= 20 * dt
                
            if p['lifetime'] <= 0:
                self.particles.remove(p)
                
    def draw(self, surf):
        for p in self.particles:
            alpha = int(255 * (p['lifetime'] / p['max_lifetime']))
            color = p['color']
            
            if p['type'] == 'blood':
                pygame.draw.circle(surf, color, (int(p['x']), int(p['y'])), p['size'])
            elif p['type'] == 'leaf':
                leaf_surf = pygame.Surface((p['size']*3, p['size']), pygame.SRCALPHA)
                pygame.draw.ellipse(leaf_surf, color, (0, 0, p['size']*3, p['size']))
                rotated_leaf = pygame.transform.rotate(leaf_surf, p['rotation'])
                surf.blit(rotated_leaf, (p['x'] - rotated_leaf.get_width()//2, 
                                       p['y'] - rotated_leaf.get_height()//2))
            elif p['type'] == 'bat_dust':
                pygame.draw.circle(surf, color, (int(p['x']), int(p['y'])), p['size'])
            elif p['type'] == 'speed_line':
                line_length = int(p['size'] * 3 * (p['lifetime'] / p['max_lifetime']))
                if line_length > 0:
                    pygame.draw.line(surf, (*color, alpha), 
                                   (int(p['x']), int(p['y'])), 
                                   (int(p['x'] + line_length), int(p['y'])), 
                                   max(1, p['size']))

# --- Efectos de Ambiente Tétrico ---
class AtmosphereEffects:
    def __init__(self):
        self.active = True
        self.fog_layers = []
        self.moon_phase = 0
        self.creepy_timer = 0
        self.flash_alpha = 0
        self.flash_active = False
        self.flash_timer = 0
        self.flash_interval = 0.05  # Flashs rápidos cada 0.05 segundos
        self.flash_interval_timer = 0  # CORREGIDO: Inicializar aquí
        self.flash_duration = 2.0  # Duración total de flashs (segundos 7-9)
        
        # Crear capas de niebla
        for i in range(3):
            self.fog_layers.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'speed': random.uniform(5, 15),
                'alpha': random.randint(30, 70),
                'size': random.randint(100, 300)
            })
    
    def start_flash_sequence(self):
        self.flash_active = True
        self.flash_timer = 0
        self.flash_alpha = 150
        self.flash_interval_timer = 0  # Reiniciar el timer del intervalo
        
    def stop_flash_sequence(self):
        self.flash_active = False
        self.flash_alpha = 0
        
    def update(self, dt):
        self.moon_phase += dt * 0.5
        self.creepy_timer += dt
        
        # Actualizar niebla
        for fog in self.fog_layers:
            fog['x'] += fog['speed'] * dt
            if fog['x'] > WIDTH + fog['size']:
                fog['x'] = -fog['size']
                fog['y'] = random.randint(0, HEIGHT)
            
        # Efecto de flash aleatorio (como relámpago)
        if not self.flash_active and self.creepy_timer >= random.uniform(3.0, 8.0):
            self.creepy_timer = 0
            self.flash_alpha = random.randint(50, 150)
            
        # Control de flashs rápidos
        if self.flash_active:
            self.flash_timer += dt
            if self.flash_timer >= self.flash_duration:
                self.stop_flash_sequence()
            else:
                self.flash_interval_timer += dt
                if self.flash_interval_timer >= self.flash_interval:
                    self.flash_interval_timer = 0
                    self.flash_alpha = 150 if self.flash_alpha == 0 else 0
            
        if not self.flash_active and self.flash_alpha > 0:
            self.flash_alpha -= dt * 100
            if self.flash_alpha < 0:
                self.flash_alpha = 0
                
    def draw(self, surf):
        # Dibujar niebla
        for fog in self.fog_layers:
            fog_surf = pygame.Surface((fog['size'], fog['size']), pygame.SRCALPHA)
            pygame.draw.circle(fog_surf, (200, 200, 200, fog['alpha']), 
                            (fog['size']//2, fog['size']//2), fog['size']//2)
            surf.blit(fog_surf, (fog['x'], fog['y']))
            
        # Efecto de flash
        if self.flash_alpha > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, int(self.flash_alpha)))
            surf.blit(flash_surf, (0, 0))
            
        # Dibujar luna (si hay fondo)
        if not has_fondo_img:
            moon_size = 60
            moon_x = WIDTH - 100
            moon_y = 80
            moon_alpha = 100 + int(50 * math.sin(self.moon_phase))
            
            moon_surf = pygame.Surface((moon_size * 2, moon_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(moon_surf, (MOONLIGHT[0], MOONLIGHT[1], MOONLIGHT[2], moon_alpha),
                            (moon_size, moon_size), moon_size)
            surf.blit(moon_surf, (moon_x - moon_size, moon_y - moon_size))

# --- Efectos de Fase 3 (Oscuridad y Truenos) ---
class ThunderEffects:
    def __init__(self):
        self.active = False
        self.darkness_alpha = 0
        self.target_darkness = 0
        self.thunder_timer = 0
        self.flash_active = False
        self.flash_timer = 0
        self.flash_duration = 0.3
        self.thunder_interval = random.uniform(2.0, 5.0)
        
    def activate(self):
        self.active = True
        self.target_darkness = 180
        self.thunder_timer = 0
        if has_trueno_sound:
            sonido_trueno.play()
        
    def deactivate(self):
        self.active = False
        self.target_darkness = 0
        
    def update(self, dt):
        if not self.active:
            return
            
        # Transición de oscuridad
        if self.darkness_alpha < self.target_darkness:
            self.darkness_alpha += dt * 100
        elif self.darkness_alpha > self.target_darkness:
            self.darkness_alpha -= dt * 100
            
        # Control de truenos
        self.thunder_timer += dt
        if self.thunder_timer >= self.thunder_interval:
            self.thunder_timer = 0
            self.thunder_interval = random.uniform(2.0, 5.0)
            self.flash_active = True
            self.flash_timer = self.flash_duration
            if has_trueno_sound:
                sonido_trueno.play()
                
        if self.flash_active:
            self.flash_timer -= dt
            if self.flash_timer <= 0:
                self.flash_active = False
                
    def draw(self, surf):
        if self.darkness_alpha > 0:
            darkness_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            darkness_surf.fill((0, 0, 0, int(self.darkness_alpha)))
            surf.blit(darkness_surf, (0, 0))
            
        if self.flash_active:
            flash_alpha = int(255 * (self.flash_timer / self.flash_duration))
            flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, flash_alpha))
            surf.blit(flash_surf, (0, 0))

# --- Sistema de Introducción MODIFICADO (IMÁGENES CENTRADAS VERTICALMENTE) ---
class IntroductionSystem:
    def __init__(self):
        self.active = True
        self.current_dialogue = 0
        self.dialogues = [
            {
                "speaker": "laynes",
                "image": "laynes",
                "text": "¡Ayudaaa Por favor!!!",
                "position": "right",
                "character_pos": "right"
            },
            {
                "speaker": "niño", 
                "image": "niño",
                "text": "¿Qué te pasa?",
                "position": "left",
                "character_pos": "left"
            },
            {
                "speaker": "laynes",
                "image": "laynes",
                "text": "Un cazador me encerró en esta jaula y ahora me quiere comer.",
                "position": "right",
                "character_pos": "right"
            },
            {
                "speaker": "niño",
                "image": "niño",
                "text": "Eso es terrible. Déjame ayudarte, te sacaré de aquí.",
                "position": "left",
                "character_pos": "left"
            },
            {
                "speaker": "cazador", 
                "image": "cazador",
                "text": "¡Uy! Otro niño. Creo que cenaré doble jajaja",
                "position": "right",
                "character_pos": "right"
            },
            {
                "speaker": "niño",
                "image": "niño",
                "text": "¡Déjala libre, o verás las consecuencias!",
                "position": "left",
                "character_pos": "left"
            },
            {
                "speaker": "cazador",
                "image": "cazador_jaula",
                "text": "Déjate de bromas y entra a la jaula. ¿O quieres pelear conmigo?",
                "position": "right",
                "character_pos": "right"
            },
            {
                "speaker": "niño",
                "image": "niño",
                "text": "No sería mala idea. Un duelo, tú y yo. Si te gano, la dejas libre. Si pierdo, ¿también me comes?",
                "position": "left",
                "character_pos": "left"
            },
            {
                "speaker": "cazador",
                "image": "cazador_jaula",
                "text": "Jajaja, ya rugiste, mocoso. Veremos qué tan buen cazador eres. ¡SUERTE CAZADOR!",
                "position": "center",
                "character_pos": "both"
            }
        ]
        self.text_speed = 35
        self.current_char = 0
        self.text_timer = 0
        self.sound_played = False
        self.text_complete = False
        self.can_advance = False

    def update(self, dt):
        if self.current_dialogue >= len(self.dialogues):
            return
            
        current_dialogue = self.dialogues[self.current_dialogue]
        
        if not self.text_complete:
            self.text_timer += dt
            target_chars = int(self.text_timer * self.text_speed)
            
            if target_chars > self.current_char:
                chars_to_add = target_chars - self.current_char
                old_char = self.current_char
                self.current_char = min(self.current_char + chars_to_add, len(current_dialogue["text"]))
                
                if old_char == 0 and self.current_char > 0 and not self.sound_played:
                    if sonido_texto:
                        sonido_texto.play()
                    self.sound_played = True
                
                if self.current_char >= len(current_dialogue["text"]):
                    self.text_complete = True
                    self.can_advance = True

    def draw(self, surf):
        # Fondo con efecto de bosque
        surf.fill((10, 15, 10))
        
        # Dibujar árboles en el fondo
        for i in range(5):
            tree_x = (i * 200) % WIDTH
            tree_width = 60
            tree_height = 250
            # Tronco
            pygame.draw.rect(surf, DARK_BROWN, 
                           (tree_x, HEIGHT - tree_height + 100, tree_width, tree_height - 100))
            # Copa del árbol
            pygame.draw.ellipse(surf, HUNTER_GREEN,
                              (tree_x - 30, HEIGHT - tree_height - 50, tree_width + 60, 150))
        
        # Marco decorativo
        pygame.draw.rect(surf, DARK_BROWN, (20, 20, WIDTH-40, HEIGHT-40), 4, border_radius=10)
        pygame.draw.rect(surf, FOREST_GREEN, (30, 30, WIDTH-60, HEIGHT-60), 2, border_radius=8)
        
        if self.current_dialogue >= len(self.dialogues):
            return
            
        current_dialogue = self.dialogues[self.current_dialogue]
        
        # Dibujar imagen del personaje según su posición
        if current_dialogue["character_pos"] == "both":
            # Mostrar ambas imágenes en el centro VERTICAL
            if has_niño_img:
                niño_x = WIDTH//2 - niño_img.get_width() - 50
                niño_y = HEIGHT//2 - niño_img.get_height()//2  # CENTRADO VERTICALMENTE
                shadow = pygame.Surface((niño_img.get_width() + 10, niño_img.get_height() + 10), pygame.SRCALPHA)
                shadow.fill((0, 0, 0, 100))
                surf.blit(shadow, (niño_x - 5, niño_y - 5))
                surf.blit(niño_img, (niño_x, niño_y))
                
            if has_cazador_jaula_img:
                cazador_x = WIDTH//2 + 50
                cazador_y = HEIGHT//2 - cazador_jaula_img.get_height()//2  # CENTRADO VERTICALMENTE
                shadow = pygame.Surface((cazador_jaula_img.get_width() + 10, cazador_jaula_img.get_height() + 10), pygame.SRCALPHA)
                shadow.fill((0, 0, 0, 100))
                surf.blit(shadow, (cazador_x - 5, cazador_y - 5))
                surf.blit(cazador_jaula_img, (cazador_x, cazador_y))
        else:
            image_to_draw = None
            if current_dialogue["image"] == "laynes" and has_laynes_img:
                image_to_draw = laynes_img
            elif current_dialogue["image"] == "niño" and has_niño_img:
                image_to_draw = niño_img
            elif current_dialogue["image"] == "cazador" and has_cazador_img:
                image_to_draw = cazador_img
            elif current_dialogue["image"] == "cazador_jaula" and has_cazador_jaula_img:
                image_to_draw = cazador_jaula_img
                
            if image_to_draw:
                if current_dialogue["character_pos"] == "left":
                    char_x = 50
                    char_y = HEIGHT//2 - image_to_draw.get_height()//2  # CENTRADO VERTICALMENTE
                    # Efecto de sombra
                    shadow = pygame.Surface((image_to_draw.get_width() + 10, image_to_draw.get_height() + 10), pygame.SRCALPHA)
                    shadow.fill((0, 0, 0, 100))
                    surf.blit(shadow, (char_x - 5, char_y - 5))
                    surf.blit(image_to_draw, (char_x, char_y))
                    
                elif current_dialogue["character_pos"] == "right":
                    char_x = WIDTH - image_to_draw.get_width() - 50
                    char_y = HEIGHT//2 - image_to_draw.get_height()//2  # CENTRADO VERTICALMENTE
                    # Efecto de sombra
                    shadow = pygame.Surface((image_to_draw.get_width() + 10, image_to_draw.get_height() + 10), pygame.SRCALPHA)
                    shadow.fill((0, 0, 0, 100))
                    surf.blit(shadow, (char_x - 5, char_y - 5))
                    surf.blit(image_to_draw, (char_x, char_y))
        
        # Diálogo
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
        
        # Fondo del diálogo con transparencia
        dialog_bg = pygame.Surface((dialog_rect.width, dialog_rect.height), pygame.SRCALPHA)
        dialog_bg.fill((0, 0, 0, 200))
        surf.blit(dialog_bg, dialog_rect.topleft)
        
        pygame.draw.rect(surf, DARK_BROWN, dialog_rect, 3, border_radius=15)
        
        speaker_names = {
            "laynes": "LAYNES",
            "niño": "EL NIÑO",
            "cazador": "EL CAZADOR"
        }
        
        name_colors = {
            "laynes": PINK,
            "niño": BLUE, 
            "cazador": DARK_BROWN
        }
        
        name_text = large_font.render(speaker_names[current_dialogue["speaker"]], True, name_colors[current_dialogue["speaker"]])
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
            
        if sonido_texto:
            sonido_texto.play()
        
        self.current_dialogue += 1
        self.current_char = 0
        self.text_timer = 0
        self.text_complete = False
        self.can_advance = False
        self.sound_played = False
        
        if self.current_dialogue >= len(self.dialogues):
            self.active = False
            return "start_battle"
        
        return "continue"

# --- Sistema de Presentación ---
class TitleScreen:
    def __init__(self):
        self.active = True
        self.timer = 0
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
        surf.fill((5, 10, 5))  # Fondo más oscuro
        
        # Título principal con efecto de sombra
        shadow_offset = 3
        title_shadow = title_font.render("NIVEL 5", True, (0, 0, 0))
        title_surface = title_font.render("NIVEL 5", True, DARK_BROWN)
        title_surface.set_alpha(self.alpha)
        title_shadow.set_alpha(self.alpha)
        
        title_x = WIDTH//2 - title_surface.get_width()//2
        title_y = HEIGHT//2 - 100
        
        surf.blit(title_shadow, (title_x + shadow_offset, title_y + shadow_offset))
        surf.blit(title_surface, (title_x, title_y))
        
        # Subtítulo con efecto de sombra
        subtitle_shadow = dialogue_font.render("Suerte de Cazador", True, (0, 0, 0))
        subtitle_surface = dialogue_font.render("Suerte de Cazador", True, FOREST_GREEN)
        subtitle_surface.set_alpha(self.alpha)
        subtitle_shadow.set_alpha(self.alpha)
        
        subtitle_x = WIDTH//2 - subtitle_surface.get_width()//2
        subtitle_y = HEIGHT//2 - 20
        
        surf.blit(subtitle_shadow, (subtitle_x + shadow_offset, subtitle_y + shadow_offset))
        surf.blit(subtitle_surface, (subtitle_x, subtitle_y))
        
        # Efecto de luciérnagas
        if self.phase in [0, 1, 2]:
            for i in range(20):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                size = random.randint(1, 4)
                brightness = random.randint(150, 255)
                alpha = random.randint(100, 200)
                glow_size = size + 3
                
                # Glow exterior
                glow_surf = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (brightness, brightness, brightness, alpha//2),
                                 (glow_size, glow_size), glow_size)
                surf.blit(glow_surf, (x - glow_size, y - glow_size))
                
                # Núcleo brillante
                core_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(core_surf, (brightness, brightness, brightness, alpha),
                                 (size, size), size)
                surf.blit(core_surf, (x - size, y - size))
        
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
                ko_text = ko_font.render("KNOCKOUT!", True, (255, 50, 50))
                ko_rect = ko_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
                effect_surface.blit(ko_text, ko_rect)
        else:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            effect_surface.blit(overlay, (0, 0))
            
            victory_font = pygame.font.SysFont("Arial", 48)
            victory_text = victory_font.render("¡VICTORIA!", True, DARK_BROWN)
            effect_surface.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, HEIGHT//2 - 100))
            
            continue_font = pygame.font.SysFont("Arial", 24)
            continue_text = continue_font.render("Presiona ESPACIO para ver estadísticas", True, WHITE)
            effect_surface.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 50))
        
        surf.blit(effect_surface, (0, 0))

# --- Sistema de Imagen "MORIR" con terremoto ---
class MorirEffect:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.duration = 3.0
        self.alpha = 0
        self.shake_intensity = 0
        self.max_shake = 15
        self.sound_played = False
        
    def activate(self):
        self.active = True
        self.timer = 0
        self.alpha = 0
        self.shake_intensity = 0
        self.sound_played = False
        
    def update(self, dt):
        if not self.active:
            return False
            
        self.timer += dt
        progress = min(1.0, self.timer / self.duration)
        
        if progress < 0.3:
            # Aparece
            self.alpha = int(progress / 0.3 * 255)
            self.shake_intensity = int((progress / 0.3) * self.max_shake)
        elif progress < 0.7:
            # Se mantiene con terremoto
            self.alpha = 255
            self.shake_intensity = self.max_shake
        elif progress < 1.0:
            # Desaparece
            self.alpha = int((1.0 - (progress - 0.7) / 0.3) * 255)
            self.shake_intensity = int((1.0 - (progress - 0.7) / 0.3) * self.max_shake)
        else:
            self.active = False
            return True
        return False
    
    def get_shake_offset(self):
        if self.shake_intensity > 0:
            return (
                random.randint(-self.shake_intensity, self.shake_intensity),
                random.randint(-self.shake_intensity, self.shake_intensity)
            )
        return (0, 0)
    
    def draw(self, surf):
        if not self.active or self.alpha <= 0:
            return
            
        if has_morir_img:
            # Crear superficie para la imagen con transparencia
            morir_surface = morir_img.copy()
            morir_surface.set_alpha(self.alpha)
            
            # Posición central
            img_rect = morir_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
            
            # Aplicar shake
            shake_offset = self.get_shake_offset()
            img_rect.x += shake_offset[0]
            img_rect.y += shake_offset[1]
            
            surf.blit(morir_surface, img_rect)
        else:
            # Texto alternativo si no hay imagen
            text_surface = title_font.render("MORIR", True, (255, 0, 0, self.alpha))
            text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
            
            # Aplicar shake
            shake_offset = self.get_shake_offset()
            text_rect.x += shake_offset[0]
            text_rect.y += shake_offset[1]
            
            # Crear superficie con alpha
            text_with_alpha = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            text_with_alpha.blit(text_surface, (0, 0))
            text_with_alpha.set_alpha(self.alpha)
            
            surf.blit(text_with_alpha, text_rect)

# --- Efectos de Cámara ---
class CameraEffect:
    def __init__(self):
        self.shake_intensity = 0
        self.shake_timer = 0
        self.zoom_level = 1.0
        self.target_zoom = 1.0
        self.screen_shake_active = False
        self.screen_shake_timer = 0
        self.screen_shake_duration = 0.3
        self.screen_shake_intensity = 5
        
    def shake(self, intensity=10, duration=0.5):
        self.shake_intensity = intensity
        self.shake_timer = duration
        
    def screen_shake(self, intensity=5, duration=0.3):
        self.screen_shake_active = True
        self.screen_shake_timer = duration
        self.screen_shake_intensity = intensity
        
    def update(self, dt):
        if self.shake_timer > 0:
            self.shake_timer -= dt
            if self.shake_timer <= 0:
                self.shake_intensity = 0
                
        if self.screen_shake_active:
            self.screen_shake_timer -= dt
            if self.screen_shake_timer <= 0:
                self.screen_shake_active = False
                
        # Suavizar zoom
        if abs(self.zoom_level - self.target_zoom) > 0.01:
            self.zoom_level += (self.target_zoom - self.zoom_level) * dt * 5
            
    def get_offset(self):
        offset_x, offset_y = 0, 0
        
        if self.shake_intensity > 0:
            offset_x += random.uniform(-self.shake_intensity, self.shake_intensity)
            offset_y += random.uniform(-self.shake_intensity, self.shake_intensity)
            
        if self.screen_shake_active:
            offset_x += random.uniform(-self.screen_shake_intensity, self.screen_shake_intensity)
            offset_y += random.uniform(-self.screen_shake_intensity, self.screen_shake_intensity)
            
        return (offset_x, offset_y)

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
        if not has_nave_img:
            pygame.draw.rect(surf, BLUE, self.rect)
        else:
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
            if sonido_misil:
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
            if sonido_daño:
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
    def __init__(self, x, y, vx, vy, color=CYAN, owner="player", damage=10):  # CAMBIADO: De GREEN a CYAN
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

# --- Clase Murciélago (Fase 2) - MODIFICADO: TAMAÑO AUMENTADO ---
class Bat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60  # CAMBIADO: De 40 a 60
        self.height = 45  # CAMBIADO: De 30 a 45
        self.speed_x = random.uniform(-150, -80)
        self.speed_y = random.uniform(-50, 50)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.animation_timer = 0
        self.wing_up = True
        
    def update(self, dt):
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt
        
        # Movimiento sinusoidal
        self.x += math.sin(pygame.time.get_ticks() * 0.001) * 30 * dt
        self.y += math.cos(pygame.time.get_ticks() * 0.001) * 20 * dt
        
        # Animación de alas
        self.animation_timer += dt
        if self.animation_timer >= 0.2:
            self.animation_timer = 0
            self.wing_up = not self.wing_up
            
        # Mantener dentro de los límites verticales
        if self.y < 50:
            self.y = 50
            self.speed_y = abs(self.speed_y)
        elif self.y > HEIGHT - 100:
            self.y = HEIGHT - 100
            self.speed_y = -abs(self.speed_y)
            
        self.rect.topleft = (int(self.x), int(self.y))
        
    def draw(self, surf):
        if has_bat_img:
            bat_surf = bat_img.copy()
            if self.wing_up:
                # Pequeña rotación para efecto de aleteo
                bat_surf = pygame.transform.rotate(bat_surf, 10)
            surf.blit(bat_surf, (self.x, self.y))
        else:
            pygame.draw.ellipse(surf, (50, 50, 50), self.rect)
            # Dibujar alas
            if self.wing_up:
                wing_rect = pygame.Rect(self.x - 10, self.y + 5, 20, 15)
                pygame.draw.ellipse(surf, (30, 30, 30), wing_rect)

# --- Clase Cazador (Boss) MODIFICADA: VELOCIDAD DE DISPAROS REDUCIDA EN FASE 3 ---
class Cazador:
    def __init__(self):
        self.width = 150
        self.height = 200
        self.x = WIDTH + 100
        self.y = HEIGHT // 2 - self.height // 2
        self.max_hp = 6000
        self.hp = self.max_hp
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.entering = True
        self.exiting = False
        self.active = True
        self.phase = 1
        self.phase_change_timer = 0
        
        # Fase 1: Mira y disparo
        self.aim_timer = 0
        self.aiming = False
        self.aim_x = 0
        self.aim_y = 0
        self.shoot_delay = 2.5
        self.shoot_timer = 0
        self.multiple_shots = 0
        
        # Fase 2: Escopeta y murciélagos
        self.shotgun_timer = 0
        self.shotgun_cooldown = 1.8
        self.bats = []
        self.bat_spawn_timer = 0
        self.bat_spawn_interval = 1.2
        
        # Fase 3: Oscuridad y rifle - MODIFICADO: MÁS LENTO
        self.darkness_active = False
        self.rifle_timer = 0
        self.rifle_cooldown = 1.2  # CAMBIADO: De 0.8 a 1.2 (más lento)
        self.rapid_fire_timer = 0
        self.rapid_fire_duration = 10.0
        
        self.move_speed = 120
        self.move_direction = 1
        self.move_timer = 0
        self.move_interval = 0.8
        
        self.color = DARK_BROWN
        self.bullet_color = ORANGE
        
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
            if sonido_fase:
                sonido_fase.play()
            return True
        return False
    
    def update(self, dt, enemy_bullets, player, camera_effect, thunder_effects, particle_system):
        if self.entering:
            self.x -= 200 * dt
            if self.x <= WIDTH - self.width - 50:
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
        if phase_changed and self.phase == 3:
            thunder_effects.activate()
            self.darkness_active = True
            
        # Movimiento vertical
        self.move_timer += dt
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.move_direction *= -1
            
        self.y += self.move_direction * self.move_speed * dt
        self.y = max(100, min(HEIGHT - self.height - 50, self.y))
        
        # Comportamiento por fase
        if self.phase == 1:
            self.update_phase1(dt, enemy_bullets, player, camera_effect)
        elif self.phase == 2:
            self.update_phase2(dt, enemy_bullets, player, particle_system, camera_effect)
        elif self.phase == 3:
            self.update_phase3(dt, enemy_bullets, player, camera_effect)
            
        # Actualizar murciélagos (fase 2)
        for bat in self.bats[:]:
            bat.update(dt)
            if bat.x < -50:
                self.bats.remove(bat)
                particle_system.create_bat_particles(bat.x, bat.y)
                
        self.rect.topleft = (int(self.x), int(self.y))
        
    def update_phase1(self, dt, enemy_bullets, player, camera_effect):
        self.aim_timer += dt
        self.shoot_timer += dt
        
        if not self.aiming and self.aim_timer >= 1.0:
            self.aiming = True
            self.aim_timer = 0
            self.aim_x = player.x + player.size // 2
            self.aim_y = player.y + player.size // 2
            self.multiple_shots = 0
            
        if self.aiming and self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            
            # Disparar bala dirigida
            dx = self.aim_x - (self.x + self.width // 2)
            dy = self.aim_y - (self.y + self.height // 2)
            dist = math.hypot(dx, dy) or 1
            
            spread = random.uniform(-0.15, 0.15)
            
            enemy_bullets.append(Bullet(
                self.x + self.width // 2,
                self.y + self.height // 2,
                (dx / dist + spread) * 450,
                (dy / dist + spread) * 450,
                color=RED,
                owner="boss",
                damage=25
            ))
            
            # Disparos múltiples
            self.multiple_shots += 1
            if self.multiple_shots < 3:
                self.shoot_timer = self.shoot_delay * 0.3
            else:
                self.aiming = False
                self.multiple_shots = 0
                self.shoot_timer = -0.5
                
            if has_disparo_sound:
                sonido_disparo.play()
            camera_effect.shake(3, 0.2)
                
    def update_phase2(self, dt, enemy_bullets, player, particle_system, camera_effect):
        self.shotgun_timer += dt
        self.bat_spawn_timer += dt
        
        # Disparar escopeta hacia la IZQUIERDA
        if self.shotgun_timer >= self.shotgun_cooldown:
            self.shotgun_timer = 0
            
            # Disparo de escopeta
            for i in range(9):
                angle = math.radians(-40 + i * 10)
                enemy_bullets.append(Bullet(
                    self.x + self.width // 2,
                    self.y + self.height // 2,
                    -math.cos(angle) * 350,
                    math.sin(angle) * 300,
                    color=ORANGE,
                    owner="boss",
                    damage=20
                ))
                
            if has_disparo_sound:
                sonido_disparo.play()
            camera_effect.shake(6, 0.4)
            
        # Generar murciélagos
        if self.bat_spawn_timer >= self.bat_spawn_interval and len(self.bats) < 7:
            self.bat_spawn_timer = 0
            self.bats.append(Bat(
                WIDTH + random.randint(20, 100),
                random.randint(50, HEIGHT - 100)
            ))
            
    def update_phase3(self, dt, enemy_bullets, player, camera_effect):
        self.rifle_timer += dt
        self.rapid_fire_timer += dt
        
        # Disparos rápidos del rifle - MODIFICADO: MÁS LENTO
        if self.rifle_timer >= self.rifle_cooldown:
            self.rifle_timer = 0
            
            # Disparo del rifle (más lento)
            for i in range(5):
                dx = player.x + player.size // 2 - (self.x + self.width // 2)
                dy = player.y + player.size // 2 - (self.y + self.height // 2)
                dist = math.hypot(dx, dy) or 1
                
                spread = random.uniform(-0.05, 0.05)
                
                enemy_bullets.append(Bullet(
                    self.x + self.width // 2,
                    self.y + self.height // 2,
                    (dx / dist + spread) * 350,  # CAMBIADO: De 500 a 350 (más lento)
                    (dy / dist + spread) * 350,  # CAMBIADO: De 500 a 350 (más lento)
                    color=YELLOW,
                    owner="boss",
                    damage=30
                ))
                
            if has_disparo_sound:
                sonido_disparo.play()
            camera_effect.shake(4, 0.3)
                
        # Aumentar velocidad de disparo gradualmente (más lento)
        if self.rapid_fire_timer < self.rapid_fire_duration:
            self.rifle_cooldown = max(0.4, 1.2 - (self.rapid_fire_timer / self.rapid_fire_duration) * 0.8)
            
    def take_damage(self, damage, particle_system):
        self.hp -= damage
        particle_system.create_blood_burst(self.x + self.width // 2, self.y + self.height // 2)
        return self.hp <= 0
        
    def start_exit(self):
        self.exiting = True
        self.active = False
        
    def draw(self, surf, player):
        if not self.active and self.exiting:
            return
            
        if has_boss_img:
            boss_colored = boss_img.copy()
            if self.phase == 2:
                boss_colored.fill((200, 100, 50, 255), special_flags=pygame.BLEND_RGBA_MULT)
            elif self.phase == 3:
                boss_colored.fill((150, 50, 50, 255), special_flags=pygame.BLEND_RGBA_MULT)
            surf.blit(boss_colored, (self.x, self.y))
        else:
            color = self.color
            if self.phase == 2:
                color = BROWN
            elif self.phase == 3:
                color = DARK_RED
            pygame.draw.rect(surf, color, self.rect)
            
        # Dibujar mira en fase 1
        if self.phase == 1 and self.aiming and has_mira_img:
            self.aim_x = player.x + player.size // 2
            self.aim_y = player.y + player.size // 2
            surf.blit(mira_img, (self.aim_x - 20, self.aim_y - 20))
            
            if pygame.time.get_ticks() % 500 < 250:
                pygame.draw.circle(surf, RED, (int(self.aim_x), int(self.aim_y)), 30, 2)
                pygame.draw.circle(surf, RED, (int(self.aim_x), int(self.aim_y)), 20, 2)
        elif self.phase == 1 and self.aiming:
            self.aim_x = player.x + player.size // 2
            self.aim_y = player.y + player.size // 2
            pygame.draw.circle(surf, RED, (int(self.aim_x), int(self.aim_y)), 20, 2)
            pygame.draw.line(surf, RED, (self.aim_x - 25, self.aim_y), (self.aim_x + 25, self.aim_y), 2)
            pygame.draw.line(surf, RED, (self.aim_x, self.aim_y - 25), (self.aim_x, self.aim_y + 25), 2)
            
        # Dibujar murciélagos
        for bat in self.bats:
            bat.draw(surf)
            
        # Barra de vida
        bar_width = 250
        bar_height = 20
        bar_x = self.x + self.width // 2 - bar_width // 2
        bar_y = self.y - 30
        
        pygame.draw.rect(surf, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        hp_fraction = max(0, self.hp / self.max_hp)
        
        bar_color = FOREST_GREEN
        if self.phase == 2:
            bar_color = ORANGE
        elif self.phase == 3:
            bar_color = RED
            
        pygame.draw.rect(surf, bar_color, (bar_x, bar_y, int(bar_width * hp_fraction), bar_height), border_radius=5)
        pygame.draw.rect(surf, WHITE, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=5)
        
        phase_names = ["Fase 1: Puntería", "Fase 2: Escopeta", "Fase 3: Oscuridad"]
        name_text = font.render(f"{phase_names[self.phase-1]}: {self.hp}/{self.max_hp}", True, WHITE)
        surf.blit(name_text, (bar_x, bar_y - 25))

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
            return "A+", GOLD, "¡PERFECTO! Salvaste a Laynes"
        elif score >= 85:
            return "A", GREEN, "¡Excelente! Derrotaste al cazador"
        elif score >= 75:
            return "B", BLUE, "¡Buen trabajo! Venciste la oscuridad"
        elif score >= 60:
            return "C", YELLOW, "¡Bien hecho! Superaste el desafío"
        else:
            return "D", ORANGE, "¡Logrado! El cazador ha sido derrotado"
            
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
        
        title_text = title_font.render("¡VICTORIA! - NIVEL 5", True, DARK_BROWN)
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
            f"Cazador derrotado: {'Sí' if self.boss_defeated else 'No'}"
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
        pygame.mixer.music.load("sound/victoria.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except:
        print("No se pudo cargar la música de victoria")

def play_normal_music():
    if has_music:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sound/waidmanns_heil.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except:
            print("No se pudo cargar la música normal")

# --- Estado del juego ---
player = Player()
player_bullets = []
enemy_bullets = []
missiles = []
cazador = Cazador()
title_screen = TitleScreen()
introduction = IntroductionSystem()
energy_ui = EnergyUI()
results_system = ResultsSystem()
camera_effect = CameraEffect()
knockout_effect = KnockoutEffect()
atmosphere_effects = AtmosphereEffects()
thunder_effects = ThunderEffects()
particle_system = ParticleSystem()
horizontal_scroll = HorizontalScroll()
morir_effect = MorirEffect()

score = 0
game_over = False
level_cleared = False
fight_started = False
boss_defeated = 0
victory_sound_played = False
knockout_shown = False
battle_start_time = 0
flash_sequence_started = False
speed_boost_activated = False

# Variables para controlar los efectos "MORIR"
morir_times = [53.0, 62.0, 117.0, 126.0]
morir_active_times = []
morir_cooldown = 5.0

continue_countdown = 0
continue_time = 10.0
coins_inserted = 0
continues_used = 0
continue_available = True
lives_per_coin = 3

start_time = pygame.time.get_ticks()
completion_time = 0

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
                if sonido_coin:
                    sonido_coin.play()
                player.add_lives(lives_per_coin)
                if coins_inserted >= 1:
                    continue_countdown = 0
                    player.invulnerable = True
                    player.invulnerable_timer = 3.0
                    enemy_bullets.clear()
                    cazador.bats.clear()
                    player.x = 80
                    player.y = HEIGHT // 2
            if event.key == pygame.K_RETURN and results_system.active:
                running = False
                pygame.quit()
                try:
                    subprocess.run([sys.executable, "ines.py"])
                except:
                    print("No se pudo cargar el siguiente nivel")
                sys.exit()
            if event.key == pygame.K_SPACE and knockout_effect.active and knockout_effect.show_stats:
                knockout_effect.active = False
                knockout_effect.freeze_game = False
                results_system.show_results(player, continues_used, score, completion_time, boss_defeated)
            if event.key == pygame.K_x and introduction.active:
                result = introduction.advance_text()
                if result == "start_battle":
                    play_normal_music()
                    player.activate()
                    cazador.entering = True
                    fight_started = True
                    battle_start_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    # Pantalla de título
    if title_screen.active:
        if title_screen.update(dt):
            pass
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

    # Efecto "MORIR"
    if morir_effect.active:
        morir_effect.update(dt)

    # Juego principal
    if not game_over and not level_cleared and fight_started and not results_system.active and not knockout_effect.freeze_game:
        current_battle_time = (pygame.time.get_ticks() - battle_start_time) / 1000.0
        
        # EFECTOS ESPECIALES EN SEGUNDO 7 Y 9
        if current_battle_time >= 7.0 and not flash_sequence_started:
            flash_sequence_started = True
            atmosphere_effects.start_flash_sequence()
            
        if current_battle_time >= 9.0 and not speed_boost_activated:
            speed_boost_activated = True
            atmosphere_effects.stop_flash_sequence()
            horizontal_scroll.activate_speed_boost(800, 9999.0)
            camera_effect.screen_shake(8, 1.0)
        
        # EFECTOS "MORIR" en tiempos específicos
        for morir_time in morir_times:
            if (abs(current_battle_time - morir_time) < 0.5 and 
                morir_time not in morir_active_times and 
                not morir_effect.active):
                morir_effect.activate()
                morir_active_times.append(morir_time)
                camera_effect.shake(20, 3.0)
        
        # Limpiar tiempos antiguos
        morir_active_times = [t for t in morir_active_times if current_battle_time - t < morir_cooldown]
        
        # Actualizar sistemas
        player.update(dt, keys)
        camera_effect.update(dt)
        atmosphere_effects.update(dt)
        thunder_effects.update(dt)
        particle_system.update(dt)
        horizontal_scroll.update(dt)
        
        # Generar partículas de hojas
        if random.random() < 0.1:
            particle_system.create_leaf_particles(1)
            
        # Generar líneas de velocidad durante el boost
        if speed_boost_activated and random.random() < 0.3:
            particle_system.create_speed_lines(3)
        
        # Disparar balas normales (CON NUEVO COLOR CYAN)
        if keys[pygame.K_x] and player.can_shoot():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            bullet = Bullet(bx, by, 600, 0, color=CYAN, owner="player")  # Usa color CYAN
            player_bullets.append(bullet)
            player.shoot()

        # Lanzar misil
        if keys[pygame.K_z] and player.can_launch_missile():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            missile = Missile(bx, by)
            missiles.append(missile)
            player.launch_missile()

        # Actualizar cazador
        if cazador.active or cazador.entering or cazador.exiting:
            cazador.update(dt, enemy_bullets, player, camera_effect, thunder_effects, particle_system)

        # Actualizar balas del jugador
        for b in player_bullets[:]:
            b.update(dt)
            if b.x > WIDTH + 50:
                player_bullets.remove(b)
                continue
            if cazador.active and rect_circle_collide(cazador.rect, b.x, b.y, b.radius):
                if cazador.take_damage(b.damage, particle_system):
                    cazador.start_exit()
                    boss_defeated = 1
                    score += 1000
                    player.add_energy(100)
                    player.activate_victory_invincibility(10.0)
                    # ACTIVAR KNOCKOUT EFFECT
                    if not knockout_shown:
                        knockout_effect.activate()
                        knockout_shown = True
                        completion_time = (pygame.time.get_ticks() - start_time) / 1000.0
                        if has_music:
                            pygame.mixer.music.stop()
                        if not victory_sound_played and sonido_victoria:
                            sonido_victoria.play()
                            victory_sound_played = True
                else:
                    player.add_energy(15)
                player.bullets_hit += 1
                if b in player_bullets:
                    player_bullets.remove(b)

        # Actualizar misiles
        for m in missiles[:]:
            m.update(dt)
            if m.x > WIDTH + 50:
                missiles.remove(m)
                continue
            if cazador.active and rect_circle_collide(cazador.rect, m.x, m.y, m.radius):
                if cazador.take_damage(m.damage, particle_system):
                    cazador.start_exit()
                    boss_defeated = 1
                    score += 1000
                    player.add_energy(150)
                    player.activate_victory_invincibility(10.0)
                    if not knockout_shown:
                        knockout_effect.activate()
                        knockout_shown = True
                        completion_time = (pygame.time.get_ticks() - start_time) / 1000.0
                        if has_music:
                            pygame.mixer.music.stop()
                        if not victory_sound_played and sonido_victoria:
                            sonido_victoria.play()
                            victory_sound_played = True
                else:
                    player.add_energy(40)
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
                particle_system.create_blood_burst(b.x, b.y, 8)
                if b in enemy_bullets:
                    enemy_bullets.remove(b)
                    
        # Colisión con murciélagos
        for bat in cazador.bats[:]:
            if player.rect.colliderect(bat.rect):
                player.take_damage()
                particle_system.create_bat_particles(bat.x, bat.y)
                if bat in cazador.bats:
                    cazador.bats.remove(bat)

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

    # --- DIBUJADO ---
    screen.fill(BLACK)
    
    # Dibujar fondo con scroll horizontal
    scroll_offset = horizontal_scroll.get_scroll_offset()
    
    if has_fondo_img:
        for i in range(3):
            bg_x = int(scroll_offset + i * WIDTH)
            screen.blit(fondo_img_original, (bg_x, 0), (0, 0, WIDTH, HEIGHT))
    else:
        for i in range(3):
            bg_x = int(scroll_offset + i * WIDTH)
            for y in range(0, HEIGHT, 20):
                alpha = max(50, int(255 * (y / HEIGHT)))
                pygame.draw.line(screen, (20, 40, 20, alpha), 
                               (bg_x, y), (bg_x + WIDTH, y), 20)
            
            for j in range(5):
                tree_x = bg_x + (j * 200) % WIDTH
                tree_width = 60
                tree_height = 300
                pygame.draw.rect(screen, DARK_BROWN, 
                               (tree_x, HEIGHT - tree_height + 100, tree_width, tree_height - 100))
                for layer in range(3):
                    layer_height = 50 - layer * 10
                    layer_width = tree_width + 60 - layer * 20
                    layer_y = HEIGHT - tree_height - 50 + layer * 15
                    layer_color = (HUNTER_GREEN[0], HUNTER_GREEN[1] + layer * 10, HUNTER_GREEN[2])
                    pygame.draw.ellipse(screen, layer_color,
                                      (tree_x - layer_width//2 + tree_width//2, 
                                       layer_y, layer_width, layer_height))
    
    # Aplicar efectos de ambiente
    atmosphere_effects.draw(screen)
    
    # Aplicar efectos de trueno
    thunder_effects.draw(screen)
    
    # Aplicar offset de cámara
    camera_offset = camera_effect.get_offset()
    
    # Crear superficie para el juego
    game_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    # Dibujar todos los elementos del juego
    if not knockout_effect.freeze_game:
        cazador.draw(game_surface, player)

        for b in player_bullets:
            b.draw(game_surface)
        for b in enemy_bullets:
            b.draw(game_surface)
        for m in missiles:
            m.draw(game_surface)
        
        if continue_countdown == 0:
            player.draw(game_surface)
    
    # Dibujar partículas
    particle_system.draw(game_surface)
    
    # Aplicar la superficie del juego a la pantalla principal con offset
    screen.blit(game_surface, camera_offset)
    
    # Dibujar efecto "MORIR"
    morir_effect.draw(screen)

    # Dibujar efecto de knockout
    if knockout_effect.active:
        knockout_effect.draw(screen)

    # UI
    energy_ui.draw(screen, player)
    
    lives_text = font.render(f"Vidas: {player.lives}", True, WHITE)
    screen.blit(lives_text, (12, 12))
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (12, 36))
    
    boss_text = font.render(f"Cazador: {'Derrotado' if boss_defeated else 'Vivo'}", True, DARK_BROWN)
    screen.blit(boss_text, (WIDTH//2 - boss_text.get_width()//2, 12))
    
    # Tiempo actual
    if fight_started:
        current_time = (pygame.time.get_ticks() - battle_start_time) / 1000.0
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        time_text = font.render(f"Tiempo: {minutes:02d}:{seconds:02d}", True, WHITE)
        screen.blit(time_text, (WIDTH - 150, 12))
    
    # Indicador de fase y efectos especiales
    if fight_started and not level_cleared and not knockout_effect.freeze_game:
        phase_text = font.render(f"Fase: {cazador.phase}/3", True, FOREST_GREEN)
        screen.blit(phase_text, (WIDTH - 120, 60))
        
        if cazador.phase == 3:
            dark_text = font.render("¡OSCURIDAD ACTIVA!", True, RED)
            screen.blit(dark_text, (WIDTH//2 - dark_text.get_width()//2, HEIGHT - 40))
            
        if speed_boost_activated:
            speed_text = font.render(f"¡VELOCIDAD EXTREMA! {int(horizontal_scroll.current_speed)}", True, NEON_RED)
            screen.blit(speed_text, (WIDTH//2 - speed_text.get_width()//2, HEIGHT - 70))
            if pygame.time.get_ticks() % 200 < 100:
                blur_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                blur_overlay.fill((255, 255, 255, 30))
                screen.blit(blur_overlay, (0, 0))

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