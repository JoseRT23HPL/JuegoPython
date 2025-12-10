import pygame
import random
import math
import subprocess
import sys
from pygame import Rect

# --- Configuración ---
WIDTH, HEIGHT = 960, 540
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
DARK_RED = (139, 0, 0)
BLOOD_RED = (138, 3, 3)
NEON_RED = (255, 20, 20)
GREEN = (80, 200, 120)
YELLOW = (240, 220, 80)
BLUE = (80, 160, 240)
GREY = (200, 200, 200)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
PURPLE = (180, 80, 220)
CYAN = (80, 220, 220)
BROWN = (139, 69, 19)
PINK = (255, 105, 180)
LIME = (50, 255, 50)
DARK_BROWN = (101, 67, 33)
DARK_GREY = (60, 60, 70)
MEAT_RED = (170, 40, 40)
BONE_WHITE = (240, 240, 220)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NIVEL SECRETO - Mein Teil")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 48)
dialogue_font = pygame.font.SysFont("Arial", 28)

# --- Cargar imágenes ---
try:
    niño_img = pygame.image.load("img/nave.png").convert_alpha()
    niño_img = pygame.transform.scale(niño_img, (250, 250))
    has_niño_img = True
except:
    print("No se pudo cargar nave.png")
    has_niño_img = False

try:
    carnicero_img = pygame.image.load("img/carnizero.png").convert_alpha()
    carnicero_img = pygame.transform.scale(carnicero_img, (300, 300))
    has_carnicero_img = True
except:
    print("No se pudo cargar carnicero.png")
    has_carnicero_img = False

# Cargar imagen "MORIR"
try:
    morir_img = pygame.image.load("img/morir.png").convert_alpha()
    morir_img = pygame.transform.scale(morir_img, (400, 200))
    has_morir_img = True
except:
    print("No se pudo cargar morir.png")
    has_morir_img = False

# Imágenes del juego
try:
    fondo_img_original = pygame.image.load("img/carniceria.png").convert()
    # Ajustamos el fondo para que sea 3x más ancho para scroll horizontal suave
    fondo_img_original = pygame.transform.scale(fondo_img_original, (WIDTH * 3, HEIGHT))
    has_fondo_img = True
except:
    try:
        fondo_img_original = pygame.image.load("img/carniceria.jpg").convert()
        fondo_img_original = pygame.transform.scale(fondo_img_original, (WIDTH * 3, HEIGHT))
        has_fondo_img = True
    except:
        print("No se pudo cargar fondo de carnicería, usando fondo por defecto")
        has_fondo_img = False

try:
    nave_img_original = pygame.image.load("img/nave.png").convert_alpha()
    has_nave_img = True
except:
    print("No se pudo cargar nave.png")
    has_nave_img = False

try:
    boss_img = pygame.image.load("img/carnizero.png").convert_alpha()
    boss_img = pygame.transform.scale(boss_img, (200, 250))
    has_boss_img = True
except:
    print("No se pudo cargar carnicero.png")
    boss_img = pygame.Surface((200, 250))
    boss_img.fill(DARK_RED)
    has_boss_img = False

# Cargar imagen de hueso
try:
    hueso_img = pygame.image.load("img/hueso.png").convert_alpha()
    hueso_img = pygame.transform.scale(hueso_img, (40, 20))
    has_hueso_img = True
except:
    print("No se pudo cargar hueso.png")
    has_hueso_img = False

# Cargar imagen de cuchillo
try:
    cuchillo_img = pygame.image.load("img/cuchillo.png").convert_alpha()
    cuchillo_img = pygame.transform.scale(cuchillo_img, (30, 60))
    has_cuchillo_img = True
except:
    print("No se pudo cargar cuchillo.png")
    has_cuchillo_img = False

# Cargar imagen de cráneo
try:
    craneo_img = pygame.image.load("img/craneo.png").convert_alpha()
    craneo_img = pygame.transform.scale(craneo_img, (50, 50))
    has_craneo_img = True
except:
    print("No se pudo cargar craneo.png")
    has_craneo_img = False

# Cargar imagen de moneda
try:
    coin_img = pygame.image.load("img/coin.png").convert_alpha()
    coin_img = pygame.transform.scale(coin_img, (30, 30))
    has_coin_img = True
except:
    print("No se pudo cargar coin.png")
    has_coin_img = False

# Cargar imagen para los minions
try:
    minion_img = pygame.image.load("img/minion.png").convert_alpha()
    minion_img = pygame.transform.scale(minion_img, (50, 50))
    has_minion_img = True
except:
    try:
        minion_img = pygame.image.load("img/enemigo.png").convert_alpha()
        minion_img = pygame.transform.scale(minion_img, (50, 50))
        has_minion_img = True
    except:
        print("No se pudo cargar minion.png o enemigo.png")
        has_minion_img = False

# Cargar GIF del knockout
try:
    ok_image = pygame.image.load("img/ok.png").convert_alpha()
    ok_image = pygame.transform.scale(ok_image, (320, 180))
    has_ok_image = True
except:
    print("No se pudo cargar ok.png")
    has_ok_image = False

# --- Cargar imagen de screamer ---
try:
    screamer_img = pygame.image.load("img/mi.jpg").convert()
    screamer_img = pygame.transform.scale(screamer_img, (WIDTH, HEIGHT))
    has_screamer_img = True
except:
    try:
        screamer_img = pygame.image.load("img/screamer.jpg").convert()
        screamer_img = pygame.transform.scale(screamer_img, (WIDTH, HEIGHT))
        has_screamer_img = True
    except:
        print("No se pudo cargar screamer.png/.jpg, usando imagen por defecto")
        has_screamer_img = False

# --- Música y sonidos ---
try:
    pygame.mixer.music.load("sound/Mein Teil.mp3")
    pygame.mixer.music.set_volume(0.6)
    has_music = True
except:
    print("No se pudo cargar mein_teil.mp3, usando música por defecto")
    try:
        pygame.mixer.music.load("sound/rammstein.mp3")
        pygame.mixer.music.set_volume(0.6)
        has_music = True
    except:
        has_music = False

# Sonidos (QUITADO: sonido_victoria)
try:
    sonido_inicio = pygame.mixer.Sound("sound/inicio1.mp3")
except:
    sonido_inicio = None

try:
    sonido_daño = pygame.mixer.Sound("sound/hit.mp3")
except:
    sonido_daño = None

try:
    sonido_coin = pygame.mixer.Sound("sound/coin.mp3")
except:
    sonido_coin = None

# Sonido de victoria ELIMINADO
sonido_victoria = None

try:
    sonido_misil = pygame.mixer.Sound("sound/misil.mp3")
except:
    sonido_misil = None

try:
    sonido_cuchillo = pygame.mixer.Sound("sound/cuchillomp3")
except:
    sonido_cuchillo = None

try:
    sonido_hueso = pygame.mixer.Sound("sound/hueso.mp3")
except:
    sonido_hueso = None

# Sonido de grito para screamer
try:
    sonido_grito = pygame.mixer.Sound("sound/grito.mp3")
    has_grito_sound = True
except:
    print("No se pudo cargar grito.mp3")
    has_grito_sound = False

try:
    sonido_fase = pygame.mixer.Sound("sound/phase_change.mp3")
except:
    sonido_fase = None

try:
    sonido_terror = pygame.mixer.Sound("sound/coin.mp3")
except:
    sonido_terror = None

try:
    sonido_knockout = pygame.mixer.Sound("sound/kn.mp3")
    has_knockout_sound = True
except:
    print("No se pudo cargar kn.mp3")
    has_knockout_sound = False

# --- Sistema de Scroll Horizontal MEJORADO ---
class HorizontalScroll:
    def __init__(self):
        self.scroll_x = 0
        self.speed = 80  # Velocidad de scroll más lenta para mejor visibilidad
        self.background_width = WIDTH * 3  # El fondo es 3x más ancho que la ventana
        
    def update(self, dt):
        self.scroll_x -= self.speed * dt
        
        # Reiniciar scroll cuando llega al final
        if self.scroll_x <= -self.background_width:
            self.scroll_x = 0
            
    def get_scroll_offset(self):
        return self.scroll_x
        
    def get_draw_x(self, x_in_world):
        return x_in_world + self.scroll_x

# --- Sistema de Partículas para sangre ---
class BloodParticleSystem:
    def __init__(self):
        self.particles = []
        self.max_particles = 200
        
    def create_blood_burst(self, x, y, count=20):
        for _ in range(min(count, self.max_particles - len(self.particles))):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(100, 400)
            lifetime = random.uniform(1.0, 2.5)
            size = random.randint(2, 6)
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': random.choice([BLOOD_RED, DARK_RED, (150, 0, 0)]),
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'size': size
            })
            
    def update(self, dt):
        for p in self.particles[:]:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['vy'] += 200 * dt  # Gravedad
            p['lifetime'] -= dt
            
            if p['lifetime'] <= 0:
                self.particles.remove(p)
                
    def draw(self, surf, scroll_offset=0):
        for p in self.particles:
            alpha = int(255 * (p['lifetime'] / p['max_lifetime']))
            color = p['color']
            pygame.draw.circle(surf, color, (int(p['x'] + scroll_offset), int(p['y'])), p['size'])

# --- Efectos de Pantalla Roja ---
class BloodScreenEffect:
    def __init__(self):
        self.active = False
        self.alpha = 0
        self.timer = 0
        self.duration = 0.3
        self.max_alpha = 150
        
    def trigger(self):
        self.active = True
        self.timer = self.duration
        self.alpha = self.max_alpha
        
    def update(self, dt):
        if self.active:
            self.timer -= dt
            if self.timer <= 0:
                self.active = False
            else:
                self.alpha = int(self.max_alpha * (self.timer / self.duration))
                
    def draw(self, surf):
        if self.active and self.alpha > 0:
            blood_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            blood_surf.fill((200, 0, 0, self.alpha))
            surf.blit(blood_surf, (0, 0))

# --- Sistema de Introducción ---
class IntroductionSystem:
    def __init__(self):
        self.active = True
        self.current_dialogue = 0
        self.dialogues = [
            {
                "speaker": "NARRADOR",
                "text": "NIVEL SECRETO",
                "position": "center",
                "character_pos": "none"
            },
            {
                "speaker": "NARRADOR", 
                "text": "MEIN TEIL",
                "position": "center",
                "character_pos": "none"
            },
            {
                "speaker": "niño",
                "image": "niño",
                "text": "¿Qué lugar es este? Huele a carne podrida...",
                "position": "left",
                "character_pos": "left"
            },
            {
                "speaker": "carnicero",
                "image": "carnicero",
                "text": "¡JAJAJA! ¡Bienvenido a mi carnicería, pequeño!",
                "position": "right",
                "character_pos": "right"
            },
            {
                "speaker": "niño",
                "image": "niño", 
                "text": "¿Tu carnicería? Esto parece más una cámara de torturas...",
                "position": "left",
                "character_pos": "left"
            },
            {
                "speaker": "carnicero",
                "image": "carnicero",
                "text": "¡Exacto! Y tú serás mi próxima especialidad.",
                "position": "right",
                "character_pos": "right"
            },
            {
                "speaker": "niño",
                "image": "niño",
                "text": "¡No pienso ser la cena de nadie!",
                "position": "left",
                "character_pos": "left"
            },
            {
                "speaker": "carnicero",
                "image": "carnicero",
                "text": "¡DEMUÉSTRALO! ¡LA LUCHA EMPIEZA AHORA!",
                "position": "center",
                "character_pos": "both"
            }
        ]
        self.text_speed = 35
        self.current_char = 0
        self.text_timer = 0
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
                self.current_char = min(self.current_char + chars_to_add, len(current_dialogue["text"]))
                
                if self.current_char >= len(current_dialogue["text"]):
                    self.text_complete = True
                    self.can_advance = True

    def draw(self, surf):
        # Fondo de carnicería
        surf.fill((30, 0, 0))
        
        # Dibujar ganchos de carne
        for i in range(6):
            hook_x = 100 + i * 130
            hook_y = 150
            # Cadena
            pygame.draw.line(surf, (100, 100, 100), (hook_x, 50), (hook_x, hook_y), 3)
            # Gancho
            pygame.draw.polygon(surf, (150, 150, 150), [
                (hook_x - 5, hook_y), (hook_x + 5, hook_y), 
                (hook_x + 3, hook_y + 20), (hook_x - 3, hook_y + 20)
            ])
            # Carne colgante
            pygame.draw.ellipse(surf, MEAT_RED, (hook_x - 15, hook_y + 20, 30, 40))
        
        if self.current_dialogue >= len(self.dialogues):
            return
            
        current_dialogue = self.dialogues[self.current_dialogue]
        
        # Dibujar personajes
        if current_dialogue["character_pos"] == "both":
            if has_niño_img:
                niño_x = WIDTH//2 - niño_img.get_width() - 50
                niño_y = HEIGHT//2 - niño_img.get_height()//2
                surf.blit(niño_img, (niño_x, niño_y))
                
            if has_carnicero_img:
                carnicero_x = WIDTH//2 + 50
                carnicero_y = HEIGHT//2 - carnicero_img.get_height()//2
                surf.blit(carnicero_img, (carnicero_x, carnicero_y))
        elif current_dialogue["character_pos"] == "left" and has_niño_img:
            niño_x = 50
            niño_y = HEIGHT//2 - niño_img.get_height()//2
            surf.blit(niño_img, (niño_x, niño_y))
        elif current_dialogue["character_pos"] == "right" and has_carnicero_img:
            carnicero_x = WIDTH - carnicero_img.get_width() - 50
            carnicero_y = HEIGHT//2 - carnicero_img.get_height()//2
            surf.blit(carnicero_img, (carnicero_x, carnicero_y))
        
        # Diálogo
        if current_dialogue["position"] == "center":
            dialog_rect = pygame.Rect(WIDTH//4, HEIGHT - 200, WIDTH//2, 150)
            text_align = "center"
        elif current_dialogue["position"] == "left":
            dialog_rect = pygame.Rect(50, HEIGHT - 200, WIDTH//2 - 80, 150)
            text_align = "left"
        else:
            dialog_rect = pygame.Rect(WIDTH//2 + 30, HEIGHT - 200, WIDTH//2 - 80, 150)
            text_align = "left"
        
        # Fondo del diálogo
        dialog_bg = pygame.Surface((dialog_rect.width, dialog_rect.height), pygame.SRCALPHA)
        dialog_bg.fill((0, 0, 0, 200))
        surf.blit(dialog_bg, dialog_rect.topleft)
        pygame.draw.rect(surf, DARK_RED, dialog_rect, 3, border_radius=15)
        
        # Nombre del hablante
        name_colors = {
            "niño": BLUE,
            "carnicero": RED,
            "NARRADOR": GOLD
        }
        
        name_text = large_font.render(current_dialogue["speaker"], True, 
                                    name_colors.get(current_dialogue["speaker"], WHITE))
        surf.blit(name_text, (dialog_rect.x + 20, dialog_rect.y + 15))
        
        # Texto del diálogo
        current_text = current_dialogue["text"][:self.current_char]
        lines = []
        current_line = ""
        
        for word in current_text.split(' '):
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
        
        # Indicador para avanzar
        if self.can_advance:
            prompt = dialogue_font.render("Presiona X para comenzar", True, GREEN)
            surf.blit(prompt, (dialog_rect.centerx - prompt.get_width()//2, dialog_rect.bottom - 40))

    def advance_text(self):
        if not self.can_advance:
            return
            
        self.current_dialogue += 1
        self.current_char = 0
        self.text_timer = 0
        self.text_complete = False
        self.can_advance = False
        
        if self.current_dialogue >= len(self.dialogues):
            self.active = False
            return "start_battle"
        return "continue"

# --- Pantalla de Presentación ---
class TitleScreen:
    def __init__(self):
        self.active = True
        self.timer = 0
        self.phase = 0
        self.alpha = 0
        
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
                self.active = False
                return True
        return False
        
    def draw(self, surf):
        surf.fill((10, 0, 0))
        
        # Título con efecto sangriento
        title_shadow = title_font.render("NIVEL SECRETO", True, (50, 0, 0))
        title_surface = title_font.render("NIVEL SECRETO", True, RED)
        title_surface.set_alpha(self.alpha)
        title_shadow.set_alpha(self.alpha)
        
        title_x = WIDTH//2 - title_surface.get_width()//2
        title_y = HEIGHT//2 - 80
        
        surf.blit(title_shadow, (title_x + 3, title_y + 3))
        surf.blit(title_surface, (title_x, title_y))
        
        # Subtítulo
        subtitle = dialogue_font.render("MEIN TEIL", True, BLOOD_RED)
        subtitle.set_alpha(self.alpha)
        surf.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, title_y + 70))
        
        # Goteo de sangre
        if self.phase == 1:
            for i in range(5):
                drop_x = random.randint(100, WIDTH-100)
                drop_y = random.randint(50, HEIGHT-100)
                drop_size = random.randint(3, 8)
                pygame.draw.circle(surf, BLOOD_RED, (drop_x, drop_y), drop_size)

# --- Efectos de Cámara ---
class CameraEffect:
    def __init__(self):
        self.shake_intensity = 0
        self.shake_timer = 0
        
    def shake(self, intensity=10, duration=0.5):
        self.shake_intensity = intensity
        self.shake_timer = duration
        
    def update(self, dt):
        if self.shake_timer > 0:
            self.shake_timer -= dt
            if self.shake_timer <= 0:
                self.shake_intensity = 0
            
    def get_offset(self):
        if self.shake_intensity > 0:
            return (
                random.uniform(-self.shake_intensity, self.shake_intensity),
                random.uniform(-self.shake_intensity, self.shake_intensity)
            )
        return (0, 0)

# --- Sistema de Screamer (10 segundos) ---
class ScreamerEffect:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.duration = 10.0  # 10 segundos de screamer
        self.alpha = 255
        self.flash_timer = 0
        self.flash_interval = 0.2  # Intervalo para parpadeo de pantalla
        self.flash_visible = True
        self.sound_played = False
        self.sound_start_time = 0
        
    def activate(self):
        self.active = True
        self.timer = 0
        self.alpha = 255
        self.flash_timer = 0
        self.flash_visible = True
        self.sound_played = False
        self.sound_start_time = 0
        
        # Reproducir sonido de grito
        if has_grito_sound:
            sonido_grito.play()
            self.sound_start_time = pygame.time.get_ticks()
            
    def update(self, dt):
        if not self.active:
            return False
            
        self.timer += dt
        
        # Parpadeo de pantalla (flash) más lento
        self.flash_timer += dt
        if self.flash_timer >= self.flash_interval:
            self.flash_timer = 0
            self.flash_visible = not self.flash_visible
        
        # Desvanecer al final
        if self.timer >= self.duration * 0.8:
            fade_progress = (self.timer - self.duration * 0.8) / (self.duration * 0.2)
            self.alpha = max(0, int(255 * (1 - fade_progress)))
            
        if self.timer >= self.duration:
            self.active = False
            if has_grito_sound:
                sonido_grito.stop()
            return True
        return False
        
    def draw(self, surf):
        if not self.active:
            return
            
        # Crear superficie para el screamer
        screamer_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Aplicar imagen de screamer si existe
        if has_screamer_img:
            screamer_surface.blit(screamer_img, (0, 0))
        else:
            # Si no hay imagen, usar fondo rojo con texto aterrador
            screamer_surface.fill((255, 0, 0))
            screamer_font = pygame.font.SysFont("Arial", 72)
            screamer_text = screamer_font.render("¡SURPRISE!", True, WHITE)
            text_rect = screamer_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screamer_surface.blit(screamer_text, text_rect)
            
            # Texto adicional
            warning_font = pygame.font.SysFont("Arial", 36)
            warning_text = warning_font.render("¡EL CARNICERO HA SIDO DERROTADO!", True, BLACK)
            warning_rect = warning_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
            screamer_surface.blit(warning_text, warning_rect)
        
        # Aplicar efecto de parpadeo (flash)
        if self.flash_visible:
            flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, 150))  # Flash blanco
            screamer_surface.blit(flash_surface, (0, 0))
        
        # Aplicar desvanecimiento
        screamer_surface.set_alpha(self.alpha)
        
        # Dibujar sobre la pantalla
        surf.blit(screamer_surface, (0, 0))

# --- Jugador ---
class Player:
    def __init__(self):
        self.base_size = 48
        self.size = self.base_size
        self.x = 80
        self.y = HEIGHT // 2
        self.speed = 5.0
        self.shrink_speed = 7.0
        self.lives = 5
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
        
        # Sistema de parpadeo mejorado
        self.blink_interval = 0.1
        self.blink_timer = 0
        self.blink_visible = True
        
        self.energy = 0
        self.max_energy = 500
        self.missile_cooldown = 0.0
        self.missile_cooldown_time = 2.0

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

        # Actualizar sistema de parpadeo cuando es invulnerable
        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.blink_visible = True
            else:
                self.blink_timer += dt
                if self.blink_timer >= self.blink_interval:
                    self.blink_timer = 0
                    self.blink_visible = not self.blink_visible

    def draw(self, surf):
        if not has_nave_img:
            if self.invulnerable:
                if self.blink_visible:
                    pygame.draw.rect(surf, BLUE, self.rect)
            else:
                pygame.draw.rect(surf, BLUE, self.rect)
        else:
            if self.invulnerable:
                if self.blink_visible:
                    nave_scaled = pygame.transform.scale(nave_img_original, (self.size, self.size))
                    surf.blit(nave_scaled, (self.x, self.y))
            else:
                nave_scaled = pygame.transform.scale(nave_img_original, (self.size, self.size))
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
        if not self.invulnerable:
            self.lives -= 1
            self.damage_taken += 1
            if sonido_daño:
                sonido_daño.play()
            self.invulnerable = True
            self.invulnerable_timer = 3.0
            self.blink_timer = 0
            self.blink_visible = False
            return True
        return False

    def activate(self):
        self.active = True

# --- Proyectiles ---
class Bullet:
    def __init__(self, x, y, vx, vy, color=CYAN, owner="player", damage=10):
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

class Cuchillo:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 60
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy) or 1
        self.vx = (dx / dist) * 400
        self.vy = (dy / dist) * 400
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.rotation = 0
        self.damage = 25

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rotation += 10 * dt * 360
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        if has_cuchillo_img:
            rotated = pygame.transform.rotate(cuchillo_img, self.rotation)
            rect = rotated.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
            surf.blit(rotated, rect)
        else:
            pygame.draw.rect(surf, GREY, self.rect)

class Hueso:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.vx = random.uniform(-300, -150)
        self.vy = random.uniform(-100, 100)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)
        self.damage = 15

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 50 * dt  # Gravedad
        self.rotation += self.rotation_speed
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        if has_hueso_img:
            rotated = pygame.transform.rotate(hueso_img, self.rotation)
            rect = rotated.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
            surf.blit(rotated, rect)
        else:
            pygame.draw.ellipse(surf, BONE_WHITE, self.rect)

class Craneo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 25
        self.vx = random.uniform(-100, 100)
        self.vy = random.uniform(200, 400)
        self.rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), 
                              self.radius * 2, self.radius * 2)
        self.damage = 30

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))

    def draw(self, surf):
        if has_craneo_img:
            surf.blit(craneo_img, (self.x - self.radius, self.y - self.radius))
        else:
            pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y)), self.radius)

# --- Enemigos ---
class Minion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 50
        self.speed = 80
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.hp = 30
        self.color = DARK_GREY
        self.damage = 10
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self, dt, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.hypot(dx, dy) or 1
        
        self.x += (dx / dist) * self.speed * dt
        self.y += (dy / dist) * self.speed * dt
        
        self.rotation += self.rotation_speed
        
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        if has_minion_img:
            rotated_minion = pygame.transform.rotate(minion_img, self.rotation)
            rotated_rect = rotated_minion.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
            surf.blit(rotated_minion, rotated_rect)
            
            health_width = int((self.hp / 30) * self.size)
            pygame.draw.rect(surf, RED, (self.x, self.y - 10, self.size, 5))
            pygame.draw.rect(surf, GREEN, (self.x, self.y - 10, health_width, 5))
        else:
            pygame.draw.rect(surf, DARK_GREY, self.rect)
            pygame.draw.rect(surf, RED, self.rect, 2)
            
            pygame.draw.circle(surf, RED, (int(self.x + self.size//3), int(self.y + self.size//3)), 4)
            pygame.draw.circle(surf, RED, (int(self.x + 2*self.size//3), int(self.y + self.size//3)), 4)

    def take_damage(self, damage):
        self.hp -= damage
        return self.hp <= 0

# --- Carnicero (BOSS) ---
class Carnicero:
    def __init__(self):
        self.width = 200
        self.height = 250
        self.x = WIDTH - 250
        self.y = HEIGHT // 2 - self.height // 2
        self.max_hp = 6000
        self.hp = self.max_hp
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.entering = False
        self.active = True
        self.phase = 1
        
        self.cuchillo_timer = 0
        self.cuchillo_cooldown = 2.0
        self.hueso_timer = 0
        self.hueso_cooldown = 1.5
        self.cuchillos = []
        self.huesos = []
        
        self.minions = []
        self.minion_spawn_timer = 0
        self.minion_spawn_cooldown = 3.0
        
        self.craneo_timer = 0
        self.craneo_cooldown = 1.5
        self.craneos = []
        self.shake_active = False
        self.shake_timer = 0
        self.cuchillo_dirigido_timer = 0
        self.cuchillo_dirigido_cooldown = 2.0
        
        self.lluvia_timer = 0
        self.lluvia_cooldown = 0.5
        self.lluvia_active = False
        self.lluvia_duration = 12.0
        self.lluvia_total_time = 0
        
        self.move_speed = 80
        self.move_direction = 1
        self.move_timer = 0
        self.move_interval = 1.5

    def update_phase(self):
        hp_percentage = self.hp / self.max_hp
        
        if hp_percentage > 0.75:
            return 1
        elif hp_percentage > 0.5:
            return 2
        elif hp_percentage > 0.25:
            return 3
        else:
            return 4

    def update(self, dt, player, camera_effect, blood_effect, blood_particles, scroll_system):
        self.x = WIDTH - 250
        
        old_phase = self.phase
        self.phase = self.update_phase()
        
        if old_phase != self.phase:
            if sonido_fase:
                sonido_fase.play()
            blood_effect.trigger()
            camera_effect.shake(15, 1.0)
            
            if self.phase == 3:
                self.shake_active = True
                self.shake_timer = 999
            elif self.phase == 4:
                self.lluvia_active = True
                self.lluvia_total_time = 0

        self.move_timer += dt
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.move_direction *= -1
            
        self.y += self.move_direction * self.move_speed * dt
        self.y = max(100, min(HEIGHT - self.height - 50, self.y))
        
        if self.phase == 1:
            self.update_fase1(dt, player, camera_effect)
        elif self.phase == 2:
            self.update_fase2(dt, player)
        elif self.phase == 3:
            self.update_fase3(dt, player, camera_effect)
        elif self.phase == 4:
            self.update_fase4(dt, player, camera_effect)
            
        for c in self.cuchillos[:]:
            c.update(dt)
            if c.x < -100 or c.x > WIDTH + 100 or c.y < -100 or c.y > HEIGHT + 100:
                self.cuchillos.remove(c)
                
        for h in self.huesos[:]:
            h.update(dt)
            if h.x < -100 or h.x > WIDTH + 100 or h.y < -100 or h.y > HEIGHT + 100:
                self.huesos.remove(h)
                
        for c in self.craneos[:]:
            c.update(dt)
            if c.y > HEIGHT + 100:
                self.craneos.remove(c)
                
        for m in self.minions[:]:
            m.update(dt, player.x, player.y)
            if m.x < -50 or m.x > WIDTH + 50 or m.y < -50 or m.y > HEIGHT + 50:
                self.minions.remove(m)
                
        if self.shake_active:
            self.shake_timer -= dt
            if self.shake_timer <= 0:
                self.shake_active = False
                
        if self.lluvia_active:
            self.lluvia_total_time += dt
            if self.lluvia_total_time >= self.lluvia_duration:
                self.lluvia_active = False
                
        self.rect.topleft = (int(self.x), int(self.y))

    def update_fase1(self, dt, player, camera_effect):
        self.cuchillo_timer += dt
        self.hueso_timer += dt
        
        if self.cuchillo_timer >= self.cuchillo_cooldown:
            self.cuchillo_timer = 0
            for i in range(2):
                cuchillo = Cuchillo(
                    self.x + self.width//2,
                    self.y + self.height//2,
                    player.x + random.uniform(-50, 50),
                    player.y + random.uniform(-50, 50)
                )
                self.cuchillos.append(cuchillo)
                if sonido_cuchillo:
                    sonido_cuchillo.play()
            camera_effect.shake(5, 0.2)
            
        if self.hueso_timer >= self.hueso_cooldown:
            self.hueso_timer = 0
            for i in range(3):
                hueso = Hueso(
                    self.x + self.width//2,
                    self.y + self.height//2
                )
                self.huesos.append(hueso)
                if sonido_hueso:
                    sonido_hueso.play()

    def update_fase2(self, dt, player):
        self.minion_spawn_timer += dt
        
        if self.minion_spawn_timer >= self.minion_spawn_cooldown and len(self.minions) < 4:
            self.minion_spawn_timer = 0
            side = random.choice(["left", "top", "bottom"])
            
            if side == "left":
                x, y = -50, random.randint(0, HEIGHT)
            elif side == "top":
                x, y = random.randint(0, WIDTH), -50
            else:
                x, y = random.randint(0, WIDTH), HEIGHT + 50
                
            self.minions.append(Minion(x, y))

    def update_fase3(self, dt, player, camera_effect):
        self.craneo_timer += dt
        self.cuchillo_dirigido_timer += dt
        
        if self.shake_active:
            camera_effect.shake(5, 0.1)
            
        if self.craneo_timer >= self.craneo_cooldown:
            self.craneo_timer = 0
            craneo = Craneo(
                random.randint(100, WIDTH-100),
                -50
            )
            self.craneos.append(craneo)
                
        if self.cuchillo_dirigido_timer >= self.cuchillo_dirigido_cooldown:
            self.cuchillo_dirigido_timer = 0
            cuchillo = Cuchillo(
                self.x + self.width//2,
                self.y + self.height//2,
                player.x,
                player.y
            )
            self.cuchillos.append(cuchillo)
            if sonido_cuchillo:
                sonido_cuchillo.play()

    def update_fase4(self, dt, player, camera_effect):
        self.lluvia_timer += dt
        
        if self.lluvia_active and self.lluvia_timer >= self.lluvia_cooldown:
            self.lluvia_timer = 0
            
            if random.random() < 0.5:
                craneo = Craneo(
                    random.randint(0, WIDTH),
                    -50
                )
                craneo.vy = 400
                self.craneos.append(craneo)
                
            if random.random() < 0.3:
                x, y = -50, random.randint(0, HEIGHT)
                    
                cuchillo = Cuchillo(x, y, player.x, player.y)
                cuchillo.vx *= 1.2
                cuchillo.vy *= 1.2
                self.cuchillos.append(cuchillo)
                
            if sonido_cuchillo and random.random() < 0.5:
                sonido_cuchillo.play()
            camera_effect.shake(2, 0.1)

    def take_damage(self, damage, blood_particles):
        self.hp -= damage
        blood_particles.create_blood_burst(
            self.x + self.width//2,
            self.y + self.height//2,
            20
        )
        return self.hp <= 0

    def draw(self, surf):
        if has_boss_img:
            surf.blit(boss_img, (self.x, self.y))
        else:
            pygame.draw.rect(surf, DARK_RED, (self.x, self.y, self.width, self.height))
        
        for c in self.cuchillos:
            c.draw(surf)
        for h in self.huesos:
            h.draw(surf)
        for c in self.craneos:
            c.draw(surf)
            
        for m in self.minions:
            m.draw(surf)

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
        
    def calculate_grade(self, continues_used, damage_taken, accuracy, completion_time, carnicero_defeated):
        if not carnicero_defeated:
            return "F", RED, "¡DERROTA! El Carnicero te ha devorado"
            
        score = 100
        
        if continues_used > 0:
            score -= continues_used * 20
            
        if damage_taken > 0:
            score -= min(damage_taken * 5, 30)
            
        if accuracy < 0.5:
            score -= 15
            
        if completion_time > 180:
            score -= 10

        if score >= 95:
            return "S+", GOLD, "¡PERFECTO! Has cocinado al Carnicero"
        elif score >= 85:
            return "A", GREEN, "¡Excelente! Derrotaste al monstruo"
        elif score >= 75:
            return "B", BLUE, "¡Buen trabajo! Sobreviviste al infierno"
        elif score >= 60:
            return "C", YELLOW, "¡Bien hecho! Saliste con vida"
        else:
            return "D", ORANGE, "¡Logrado! Pero a un alto costo"
            
    def show_results(self, player, continues_used, completion_time, carnicero_defeated):
        self.active = True
        
        accuracy = player.bullets_hit / player.bullets_shot if player.bullets_shot > 0 else 0
        
        self.grade, self.grade_color, self.message = self.calculate_grade(
            continues_used, player.damage_taken, accuracy, completion_time, carnicero_defeated
        )
        
        self.player_lives = player.lives
        self.accuracy = accuracy
        self.continues_used = continues_used
        self.completion_time = completion_time
        self.player_damage_taken = player.damage_taken
        self.player_bullets_hit = player.bullets_hit
        self.player_bullets_shot = player.bullets_shot
        self.carnicero_defeated = carnicero_defeated
        
    def draw(self, surf):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surf.blit(overlay, (0, 0))
        
        title_text = title_font.render("RESULTADOS - NIVEL SECRETO", True, RED)
        surf.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 40))
        
        grade_text = large_font.render(f"Calificación: {self.grade}", True, self.grade_color)
        surf.blit(grade_text, (WIDTH//2 - grade_text.get_width()//2, 100))
        
        stats_y = 160
        stats = [
            f"Tiempo: {self.completion_time:.1f} segundos",
            f"Continues usados: {self.continues_used}",
            f"Daño recibido: {self.player_damage_taken} veces",
            f"Precisión: {self.accuracy*100:.1f}% ({self.player_bullets_hit}/{self.player_bullets_shot})",
            f"Vidas restantes: {self.player_lives}/5",
            f"Carnicero derrotado: {'SÍ' if self.carnicero_defeated else 'NO'}"
        ]
        
        for stat in stats:
            stat_text = font.render(stat, True, WHITE)
            surf.blit(stat_text, (WIDTH//2 - stat_text.get_width()//2, stats_y))
            stats_y += 35
        
        message_text = font.render(self.message, True, GREEN if self.carnicero_defeated else RED)
        surf.blit(message_text, (WIDTH//2 - message_text.get_width()//2, stats_y + 20))
        
        instruction_text = font.render("Presiona ENTER para salir", True, YELLOW)
        surf.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 60))

# --- Colisiones ---
def rect_circle_collide(rect, circle_x, circle_y, radius):
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))
    dx = circle_x - closest_x
    dy = circle_y - closest_y
    return dx * dx + dy * dy <= radius * radius

# --- Inicialización ---
player = Player()
player_bullets = []
missiles = []
carnicero = Carnicero()
title_screen = TitleScreen()
introduction = IntroductionSystem()
results_system = ResultsSystem()
camera_effect = CameraEffect()
blood_effect = BloodScreenEffect()
blood_particles = BloodParticleSystem()
energy_ui = EnergyUI()
scroll_system = HorizontalScroll()

# Instancia del efecto screamer
screamer_effect = ScreamerEffect()

score = 0
game_over = False
level_cleared = False
fight_started = False
carnicero_defeated = False
victory_sound_played = False

# Variable para controlar si ya se activó el screamer
screamer_activated = False

continue_countdown = 0
continue_time = 10.0
coins_inserted = 0
continues_used = 0
continue_available = True
lives_per_coin = 3

start_time = pygame.time.get_ticks()
completion_time = 0

# --- Bucle principal ---
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
            if event.key == pygame.K_x and introduction.active:
                result = introduction.advance_text()
                if result == "start_battle":
                    if has_music:
                        pygame.mixer.music.play(-1)
                    player.activate()
                    fight_started = True
                    start_time = pygame.time.get_ticks()
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
                    carnicero.cuchillos.clear()
                    carnicero.huesos.clear()
                    carnicero.craneos.clear()
                    carnicero.minions.clear()
                    player.x = 80
                    player.y = HEIGHT // 2
            if event.key == pygame.K_RETURN and results_system.active:
                running = False

    keys = pygame.key.get_pressed()

    if title_screen.active:
        if title_screen.update(dt):
            pass
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

    if screamer_effect.active:
        screamer_finished = screamer_effect.update(dt)
        if screamer_finished:
            screamer_effect.active = False
            completion_time = (pygame.time.get_ticks() - start_time) / 1000.0
            results_system.show_results(player, continues_used, completion_time, carnicero_defeated)
    
    if not game_over and not level_cleared and fight_started and not results_system.active and not screamer_effect.active:
        current_time = (pygame.time.get_ticks() - start_time) / 1000.0
        
        player.update(dt, keys)
        camera_effect.update(dt)
        blood_effect.update(dt)
        blood_particles.update(dt)
        scroll_system.update(dt)
        
        if keys[pygame.K_x] and player.can_shoot():
            bullet = Bullet(player.x + player.size + 6, player.y + player.size / 2, 600, 0, color=CYAN, owner="player")
            player_bullets.append(bullet)
            player.shoot()

        if keys[pygame.K_z] and player.can_launch_missile():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            missile = Missile(bx, by)
            missiles.append(missile)
            player.launch_missile()

        if carnicero.active:
            carnicero.update(dt, player, camera_effect, blood_effect, blood_particles, scroll_system)
            
            if carnicero.hp <= 0:
                carnicero.active = False
                carnicero_defeated = True
                level_cleared = True
                score += 5000
                player.add_energy(200)
                
                if not screamer_activated:
                    screamer_effect.activate()
                    screamer_activated = True
                    if has_music:
                        pygame.mixer.music.stop()
                    # ELIMINADO: sonido_victoria ya no se reproduce

        for b in player_bullets[:]:
            b.update(dt)
            if b.x > WIDTH + 50:
                player_bullets.remove(b)
                continue
                
            if carnicero.active and rect_circle_collide(carnicero.rect, b.x, b.y, b.radius):
                if carnicero.take_damage(b.damage, blood_particles):
                    carnicero.active = False
                    carnicero_defeated = True
                    level_cleared = True
                    score += 5000
                    player.add_energy(200)
                    
                    if not screamer_activated:
                        screamer_effect.activate()
                        screamer_activated = True
                        if has_music:
                            pygame.mixer.music.stop()
                else:
                    player.add_energy(15)
                player.bullets_hit += 1
                if b in player_bullets:
                    player_bullets.remove(b)
                    
            for m in carnicero.minions[:]:
                if rect_circle_collide(m.rect, b.x, b.y, b.radius):
                    if m.take_damage(b.damage):
                        blood_particles.create_blood_burst(m.x + m.size//2, m.y + m.size//2, 10)
                        carnicero.minions.remove(m)
                        score += 50
                        player.add_energy(10)
                    player.bullets_hit += 1
                    if b in player_bullets:
                        player_bullets.remove(b)
                    break

        for m in missiles[:]:
            m.update(dt)
            if m.x > WIDTH + 50:
                missiles.remove(m)
                continue
            if carnicero.active and rect_circle_collide(carnicero.rect, m.x, m.y, m.radius):
                if carnicero.take_damage(m.damage, blood_particles):
                    carnicero.active = False
                    carnicero_defeated = True
                    level_cleared = True
                    score += 5000
                    player.add_energy(200)
                    
                    if not screamer_activated:
                        screamer_effect.activate()
                        screamer_activated = True
                        if has_music:
                            pygame.mixer.music.stop()
                else:
                    player.add_energy(40)
                if m in missiles:
                    missiles.remove(m)

        for c in carnicero.cuchillos:
            if player.rect.colliderect(c.rect):
                if player.take_damage():
                    blood_effect.trigger()
                    blood_particles.create_blood_burst(player.x + player.size//2, player.y + player.size//2, 15)
                    camera_effect.shake(8, 0.3)
                break
                
        for h in carnicero.huesos:
            if player.rect.colliderect(h.rect):
                if player.take_damage():
                    blood_effect.trigger()
                    blood_particles.create_blood_burst(player.x + player.size//2, player.y + player.size//2, 10)
                    camera_effect.shake(6, 0.2)
                break
                
        for c in carnicero.craneos:
            if player.rect.colliderect(c.rect):
                if player.take_damage():
                    blood_effect.trigger()
                    blood_particles.create_blood_burst(player.x + player.size//2, player.y + player.size//2, 20)
                    camera_effect.shake(10, 0.4)
                break
                
        for m in carnicero.minions:
            if player.rect.colliderect(m.rect):
                if player.take_damage():
                    blood_effect.trigger()
                    blood_particles.create_blood_burst(player.x + player.size//2, player.y + player.size//2, 10)
                    camera_effect.shake(4, 0.2)
                break

        if player.lives <= 0 and continue_available and continue_countdown == 0:
            continue_countdown = continue_time
            coins_inserted = 0

    if continue_countdown > 0:
        continue_countdown -= dt
        if continue_countdown <= 0:
            continue_countdown = 0
            game_over = True
            level_cleared = True
            if has_music:
                pygame.mixer.music.stop()
            if sonido_terror:
                sonido_terror.play()
            completion_time = (pygame.time.get_ticks() - start_time) / 1000.0
            results_system.show_results(player, continues_used, completion_time, carnicero_defeated)

    # --- DIBUJADO ---
    screen.fill((20, 0, 0))
    
    # Dibujar fondo con scroll horizontal suave
    scroll_offset = scroll_system.get_scroll_offset()
    
    if has_fondo_img:
        # El fondo es 3x más ancho que la ventana para scroll infinito
        # Dibujamos 2 copias para crear el efecto de scroll continuo
        for i in range(2):
            bg_x = int(scroll_offset + i * WIDTH * 3)
            # Solo dibujamos si está visible en pantalla
            if bg_x > -WIDTH * 3 and bg_x < WIDTH:
                screen.blit(fondo_img_original, (bg_x, 0))
    else:
        # Fondo alternativo con scroll
        for i in range(3):
            bg_x = int(scroll_offset + i * WIDTH)
            for y in range(0, HEIGHT, 40):
                color_intensity = max(20, min(60, 40 + math.sin(bg_x * 0.01 + y * 0.1) * 20))
                pygame.draw.line(screen, (color_intensity, 0, 0), 
                               (bg_x, y), (bg_x + WIDTH, y), 40)
    
    if carnicero.active:
        carnicero.draw(screen)
        
    for b in player_bullets:
        b.draw(screen)
        
    for m in missiles:
        m.draw(screen)
        
    player.draw(screen)
    
    blood_particles.draw(screen)
    
    blood_effect.draw(screen)
    
    if screamer_effect.active:
        screamer_effect.draw(screen)
    
    offset = camera_effect.get_offset()
    if offset != (0, 0):
        shake_surface = screen.copy()
        screen.fill((20, 0, 0))
        screen.blit(shake_surface, offset)
    
    energy_ui.draw(screen, player)
    
    lives_text = font.render(f"VIDAS: {player.lives}", True, RED)
    screen.blit(lives_text, (20, 20))
    
    score_text = font.render(f"PUNTOS: {score}", True, WHITE)
    screen.blit(score_text, (20, 50))
    
    time_text = font.render(f"TIEMPO: {current_time:.1f}s", True, YELLOW)
    screen.blit(time_text, (WIDTH - 150, 20))
    
    if carnicero.active:
        bar_width = 300
        bar_height = 25
        bar_x = WIDTH//2 - bar_width//2
        bar_y = 20
        
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        hp_fraction = max(0, carnicero.hp / carnicero.max_hp)
        
        if carnicero.phase == 1:
            bar_color = RED
        elif carnicero.phase == 2:
            bar_color = ORANGE
        elif carnicero.phase == 3:
            bar_color = PURPLE
        else:
            bar_color = NEON_RED
            
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, int(bar_width * hp_fraction), bar_height), border_radius=5)
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=5)
        
        phase_names = ["FASE 1: CUCHILLOS", "FASE 2: MINIONS", "FASE 3: CRÁNEOS", "FASE 4: LLUVIA MORTAL"]
        name_text = font.render(f"{phase_names[carnicero.phase-1]} - HP: {int(carnicero.hp)}/{carnicero.max_hp}", True, WHITE)
        screen.blit(name_text, (bar_x, bar_y - 25))
    
    if fight_started and not level_cleared:
        inst_text = font.render("X: DISPARAR   Z: MISIL   SHIFT: PEQUEÑO", True, LIME)
        screen.blit(inst_text, (WIDTH//2 - inst_text.get_width()//2, HEIGHT - 40))

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
        
        if has_coin_img:
            coin_x = WIDTH//2 - 15
            coin_y = HEIGHT//2 + 120
            screen.blit(coin_img, (coin_x, coin_y))

    if game_over and continue_countdown == 0 and not results_system.active:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        over_surf = large_font.render("GAME OVER", True, RED)
        screen.blit(over_surf, (WIDTH//2 - over_surf.get_width()//2, HEIGHT//2 - 50))
        
        instruction_text = font.render("Se acabó el tiempo para continuar", True, WHITE)
        screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()

pygame.quit()