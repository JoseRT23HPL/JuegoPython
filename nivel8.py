import pygame
import random
import math
import subprocess
import sys
from pygame import Rect

# --- Configuración ---
WIDTH, HEIGHT = 960, 540
FPS = 60

# Colores en blanco y negro
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)
MEDIUM_GRAY = (100, 100, 100)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nivel 8 - Americana en Blanco y Negro")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 48)
dialogue_font = pygame.font.SysFont("Arial", 28)

# --- Recursos ---
# Crear fondo procedural en blanco y negro con patrones de caricatura
def create_cartoon_background():
    background = pygame.Surface((WIDTH * 2, HEIGHT))  # Doble ancho para scroll
    background.fill(BLACK)
    
    # Patrones estilo caricatura antigua
    for i in range(50):
        x = random.randint(0, WIDTH * 2)
        y = random.randint(0, HEIGHT)
        size = random.randint(2, 8)
        gray = random.choice([DARK_GRAY, MEDIUM_GRAY, LIGHT_GRAY])
        pygame.draw.circle(background, gray, (x, y), size)
    
    # Líneas horizontales para efecto de TV antigua
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(background, DARK_GRAY, (0, y), (WIDTH * 2, y), 1)
    
    return background

fondo_img = create_cartoon_background()

# Cargar o crear imagen de la nave en blanco y negro
try:
    nave_img_original = pygame.image.load("img/nave.png").convert_alpha()
    # Convertir a blanco y negro
    nave_bw = pygame.Surface(nave_img_original.get_size(), pygame.SRCALPHA)
    for x in range(nave_img_original.get_width()):
        for y in range(nave_img_original.get_height()):
            r, g, b, a = nave_img_original.get_at((x, y))
            gray = (r + g + b) // 3
            nave_bw.set_at((x, y), (gray, gray, gray, a))
    nave_img_original = nave_bw
except:
    print("No se pudo cargar nave.png, creando nave por defecto")
    nave_img_original = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.circle(nave_img_original, WHITE, (24, 24), 20)
    pygame.draw.circle(nave_img_original, BLACK, (24, 24), 15)

# Crear imagen del enemigo "Americano" si no existe
try:
    boss_img = pygame.image.load("img/e1.png").convert_alpha()
    boss_img = pygame.transform.scale(boss_img, (120, 120))
    # Convertir a blanco y negro
    boss_bw = pygame.Surface(boss_img.get_size(), pygame.SRCALPHA)
    for x in range(boss_img.get_width()):
        for y in range(boss_img.get_height()):
            r, g, b, a = boss_img.get_at((x, y))
            gray = (r + g + b) // 3
            boss_bw.set_at((x, y), (gray, gray, gray, a))
    boss_img = boss_bw
except:
    print("No se pudo cargar americano.png, creando enemigo por defecto")
    boss_img = pygame.Surface((120, 120), pygame.SRCALPHA)
    pygame.draw.rect(boss_img, WHITE, (10, 10, 100, 100), border_radius=20)
    pygame.draw.rect(boss_img, BLACK, (20, 20, 80, 80), border_radius=15)
    pygame.draw.rect(boss_img, WHITE, (35, 35, 50, 50), border_radius=10)

# Crear imágenes para la introducción
try:
    americano_img = pygame.image.load("img/e1.png").convert_alpha()
    americano_img = pygame.transform.scale(americano_img, (300, 300))
    # Convertir a blanco y negro
    americano_bw = pygame.Surface(americano_img.get_size(), pygame.SRCALPHA)
    for x in range(americano_img.get_width()):
        for y in range(americano_img.get_height()):
            r, g, b, a = americano_img.get_at((x, y))
            gray = (r + g + b) // 3
            americano_bw.set_at((x, y), (gray, gray, gray, a))
    americano_img = americano_bw
    has_americano_img = True
except:
    print("No se pudo cargar la imagen del americano, usando por defecto")
    americano_img = pygame.Surface((300, 300), pygame.SRCALPHA)
    pygame.draw.rect(americano_img, WHITE, (50, 50, 200, 200), border_radius=40)
    pygame.draw.rect(americano_img, BLACK, (70, 70, 160, 160), border_radius=30)
    has_americano_img = True

try:
    player_nave_img = pygame.image.load("img/niño.png").convert_alpha()
    player_nave_img = pygame.transform.scale(player_nave_img, (200, 200))
    # Convertir a blanco y negro
    player_bw = pygame.Surface(player_nave_img.get_size(), pygame.SRCALPHA)
    for x in range(player_nave_img.get_width()):
        for y in range(player_nave_img.get_height()):
            r, g, b, a = player_nave_img.get_at((x, y))
            gray = (r + g + b) // 3
            player_bw.set_at((x, y), (gray, gray, gray, a))
    player_nave_img = player_bw
    has_player_nave_img = True
except:
    print("No se pudo cargar la imagen del niño, usando por defecto")
    player_nave_img = pygame.Surface((200, 200), pygame.SRCALPHA)
    pygame.draw.circle(player_nave_img, WHITE, (100, 100), 80)
    pygame.draw.circle(player_nave_img, BLACK, (100, 100), 60)
    has_player_nave_img = True

# Cargar GIF del OK
try:
    ok_image = pygame.image.load("img/ok.png").convert_alpha()
    ok_image = pygame.transform.scale(ok_image, (320, 180))
    has_ok_image = True
except:
    print("No se pudo cargar ok.png, se usará texto alternativo")
    has_ok_image = False

# Música y sonidos (usar sonidos existentes si no hay específicos)
try:
    pygame.mixer.music.load("sound/we.mp3")  # Usar música existente
    pygame.mixer.music.set_volume(0.4)
except:
    print("No se pudo cargar la música específica")

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

# --- Sistema de Scroll ---
class ScrollSystem:
    def __init__(self):
        self.scroll_x = 0
        self.scroll_speed = 100
        
    def update(self, dt):
        self.scroll_x -= self.scroll_speed * dt
        if self.scroll_x <= -WIDTH:
            self.scroll_x = 0
            
    def get_offset(self):
        return self.scroll_x

# --- Sistema de Partículas Estilo Caricatura Antigua ---
class CartoonParticleSystem:
    def __init__(self):
        self.particles = []
        self.gray_values = [WHITE, LIGHT_GRAY, MEDIUM_GRAY]
        
    def create_dust_burst(self, x, y, count=15):
        """Crea partículas de polvo estilo caricatura"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 200)
            lifetime = random.uniform(1.0, 2.5)
            size = random.randint(2, 6)
            particle_type = random.choice(['dot', 'line', 'squiggle'])
            
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': random.choice(self.gray_values),
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'size': size,
                'type': particle_type,
                'rotation': random.uniform(0, 360),
                'wiggle': random.uniform(-2, 2)
            })
            
    def create_smoke_trail(self, x, y, count=8):
        """Crea efecto de humo estilo dibujos animados"""
        for _ in range(count):
            self.particles.append({
                'x': x + random.uniform(-10, 10),
                'y': y + random.uniform(-10, 10),
                'vx': random.uniform(-20, 20),
                'vy': random.uniform(-30, -10),
                'color': random.choice([LIGHT_GRAY, MEDIUM_GRAY]),
                'lifetime': random.uniform(2.0, 4.0),
                'max_lifetime': 4.0,
                'size': random.randint(3, 8),
                'type': 'smoke',
                'rotation': 0,
                'growth': random.uniform(0.5, 1.5)
            })
            
    def create_impact_lines(self, x, y, count=12):
        """Crea líneas de impacto estilo cómic"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            length = random.randint(10, 30)
            width = random.randint(1, 3)
            
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * 100,
                'vy': math.sin(angle) * 100,
                'color': WHITE,
                'lifetime': random.uniform(0.5, 1.0),
                'max_lifetime': 1.0,
                'size': length,
                'width': width,
                'type': 'impact_line',
                'angle': angle
            })
            
    def update(self, dt):
        for p in self.particles[:]:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['lifetime'] -= dt
            
            # Efectos específicos por tipo
            if p['type'] == 'smoke':
                p['size'] += p.get('growth', 0) * dt * 10
                p['vy'] -= 20 * dt  # Flotar hacia arriba
                
            elif p['type'] in ['dot', 'line', 'squiggle']:
                p['x'] += math.sin(pygame.time.get_ticks() * 0.01) * p.get('wiggle', 0) * dt
                
            if p['lifetime'] <= 0:
                self.particles.remove(p)
                
    def draw(self, surf):
        for p in self.particles:
            alpha = int(255 * (p['lifetime'] / p['max_lifetime']))
            color = p['color']
            
            if p['type'] == 'dot':
                pygame.draw.circle(surf, color, (int(p['x']), int(p['y'])), p['size'])
                
            elif p['type'] == 'line':
                # Línea que gira
                end_x = p['x'] + math.cos(p['rotation']) * p['size']
                end_y = p['y'] + math.sin(p['rotation']) * p['size']
                pygame.draw.line(surf, color, (p['x'], p['y']), (end_x, end_y), 2)
                
            elif p['type'] == 'squiggle':
                # Línea ondulada
                points = []
                for i in range(3):
                    px = p['x'] + i * p['size'] / 2
                    py = p['y'] + math.sin(i * 1.5) * 3
                    points.append((px, py))
                if len(points) > 1:
                    pygame.draw.lines(surf, color, False, points, 2)
                    
            elif p['type'] == 'smoke':
                # Círculo de humo
                smoke_surf = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
                pygame.draw.circle(smoke_surf, (*color, alpha), 
                                 (p['size'], p['size']), p['size'])
                surf.blit(smoke_surf, (p['x'] - p['size'], p['y'] - p['size']))
                
            elif p['type'] == 'impact_line':
                # Línea de impacto recta
                end_x = p['x'] + math.cos(p['angle']) * p['size']
                end_y = p['y'] + math.sin(p['angle']) * p['size']
                pygame.draw.line(surf, color, (p['x'], p['y']), (end_x, end_y), p['width'])

# --- Efectos Especiales en Blanco y Negro ---
class BWEffects:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.flash_timer = 0
        self.flash_visible = False
        self.static_timer = 0
        self.static_lines = []
        
    def activate(self):
        self.active = True
        self.timer = 0
        self.flash_timer = 0
        self.flash_visible = False
        self.generate_static_lines()
        
    def generate_static_lines(self):
        """Genera líneas de estática para efecto TV antigua"""
        self.static_lines = []
        for _ in range(20):
            y = random.randint(0, HEIGHT)
            height = random.randint(1, 3)
            brightness = random.choice([DARK_GRAY, MEDIUM_GRAY, LIGHT_GRAY])
            self.static_lines.append({
                'y': y,
                'height': height,
                'brightness': brightness,
                'speed': random.uniform(0.5, 2.0)
            })

    def update(self, dt):
        if not self.active:
            return
            
        self.timer += dt
        self.flash_timer += dt
        self.static_timer += dt
        
        # Flash aleatorio
        if self.flash_timer >= random.uniform(1.0, 3.0):
            self.flash_timer = 0
            self.flash_visible = True
            
        if self.flash_visible and self.flash_timer > 0.1:
            self.flash_visible = False
            
        # Mover líneas de estática
        if self.static_timer >= 0.1:
            self.static_timer = 0
            for line in self.static_lines:
                line['y'] += line['speed']
                if line['y'] > HEIGHT:
                    line['y'] = 0
                    line['brightness'] = random.choice([DARK_GRAY, MEDIUM_GRAY, LIGHT_GRAY])
            
    def draw(self, surf):
        if not self.active:
            return
            
        # Líneas de estática (efecto TV antigua)
        for line in self.static_lines:
            pygame.draw.rect(surf, line['brightness'], 
                           (0, line['y'], WIDTH, line['height']))
        
        # Flash blanco ocasional
        if self.flash_visible:
            flash_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_overlay.fill((255, 255, 255, 80))
            surf.blit(flash_overlay, (0, 0))

# --- Sistema de Introducción para Nivel 8 ---
class IntroductionSystem:
    def __init__(self):
        self.active = True
        self.current_dialogue = 0
        self.dialogues = [
            {
                "speaker": "americano",
                "text": "¡Hola! Gusto de verte",
                "position": "right"
            },
            {
                "speaker": "player", 
                "text": "¿Por qué estamos en blanco y negro?",
                "position": "left"
            },
            {
                "speaker": "americano",
                "text": "La verdad no se, el creador que nos desarrollo",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "¿Creador?",
                "position": "left"
            },
            {
                "speaker": "americano",
                "text": "Bueno, veo que pudiste pasar el bosque enbrujado",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "Sí",
                "position": "left"
            },
            {
                "speaker": "americano", 
                "text": "¿Qué te parece una batalla conmigo?",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "¡Va!",
                "position": "left"
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
        
        pygame.draw.rect(surf, MEDIUM_GRAY, (20, 20, WIDTH-40, HEIGHT-40), 4, border_radius=10)
        pygame.draw.rect(surf, WHITE, (30, 30, WIDTH-60, HEIGHT-60), 2, border_radius=8)
        
        current_dialogue = self.dialogues[self.current_dialogue]
        
        if current_dialogue["speaker"] == "americano":
            if has_americano_img:
                char_x = WIDTH - 350
                char_y = HEIGHT//2 - 150
                surf.blit(americano_img, (char_x, char_y))
        
        if current_dialogue["speaker"] == "player":
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
        
        pygame.draw.rect(surf, (30, 30, 30), dialog_rect, border_radius=15)
        pygame.draw.rect(surf, WHITE, dialog_rect, 3, border_radius=15)
        
        speaker_names = {
            "americano": "AMERICANO",
            "player": "TU NAVE"
        }
        
        name_colors = {
            "americano": WHITE,
            "player": LIGHT_GRAY
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
            prompt = dialogue_font.render(prompt_text, True, WHITE)
            
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
                pygame.draw.polygon(surf, WHITE, triangle_points)
        else:
            if pygame.time.get_ticks() % 600 < 300:
                dots_text = dialogue_font.render("...", True, WHITE)
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
        
        title_surface = title_font.render("NIVEL 8", True, WHITE)
        title_surface.set_alpha(self.alpha)
        surf.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, HEIGHT//2 - 100))
        
        subtitle_surface = dialogue_font.render("Americana en Blanco y Negro", True, WHITE)
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
                ok_text = ok_font.render("OK", True, WHITE)
                ok_rect = ok_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
                effect_surface.blit(ok_text, ok_rect)
                
                ko_font = pygame.font.SysFont("Arial", int(40 * self.scale))
                ko_text = ko_font.render("KNOCKOUT!", True, LIGHT_GRAY)
                ko_rect = ko_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
                effect_surface.blit(ko_text, ko_rect)
        else:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            effect_surface.blit(overlay, (0, 0))
            
            victory_font = pygame.font.SysFont("Arial", 48)
            victory_text = victory_font.render("¡VICTORIA!", True, WHITE)
            effect_surface.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, HEIGHT//2 - 100))
            
            continue_font = pygame.font.SysFont("Arial", 24)
            continue_text = continue_font.render("Presiona ESPACIO para ver estadísticas", True, WHITE)
            effect_surface.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 50))
        
        surf.blit(effect_surface, (0, 0))

# --- CLASES DEL JUEGO (Player, Bullet, Missile, Obstacle, Americano) ---
# [Aquí van las clases Player, Bullet, Missile, Obstacle, y Americano del código anterior]
# Para ahorrar espacio, mantengo la misma funcionalidad pero adaptada al blanco y negro

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
    def __init__(self, x, y, vx, vy, color=WHITE, owner="player", damage=10):
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
        self.color = MEDIUM_GRAY
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
            color = (200, 200, 200, alpha)
            particle_surf = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, (particle['size']//2, particle['size']//2), particle['size']//2)
            surf.blit(particle_surf, (particle['x'], particle['y']))
        
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surf, WHITE, (int(self.x + 8), int(self.y)), 4)

class Obstacle:
    def __init__(self, x, y, obstacle_type="meteor"):
        self.x = x
        self.y = y
        self.type = obstacle_type
        self.speed = random.uniform(200, 350)
        self.size = random.randint(25, 35)
        self.color = LIGHT_GRAY if obstacle_type == "meteor" else MEDIUM_GRAY
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)
        self.direction = -1

    def update(self, dt):
        self.x += self.direction * self.speed * dt
        self.rotation += self.rotation_speed
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        meteor_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(meteor_surface, self.color, (self.size//2, self.size//2), self.size//2)
        pygame.draw.circle(meteor_surface, WHITE, (self.size//2, self.size//2), self.size//4)
        
        rotated_meteor = pygame.transform.rotate(meteor_surface, self.rotation)
        new_rect = rotated_meteor.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
        surf.blit(rotated_meteor, new_rect.topleft)

class Americano:
    def __init__(self):
        self.w = 120
        self.h = 120
        self.x = WIDTH + 200
        self.y = HEIGHT // 3
        self.max_hp = 6000
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
        
        self.phase_attack_cooldowns = [1.5, 1.0, 0.7]
        self.phase_move_speeds = [100, 180, 250]
        
        self.color = WHITE
        self.bullet_color = LIGHT_GRAY

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

    def update(self, dt, enemy_bullets, player, obstacles, particle_system):
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
            particle_system.create_dust_burst(self.x + self.w//2, self.y + self.h//2, 30)

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
                self.attack_phase1(enemy_bullets)
            elif self.phase == 2:
                self.attack_phase2(enemy_bullets, player)
            elif self.phase == 3:
                self.attack_phase3(enemy_bullets, player, obstacles)

        self.rect.topleft = (int(self.x), int(self.y))

    def attack_phase1(self, enemy_bullets):
        # Ataque en espiral
        for i in range(8):
            angle = math.radians(pygame.time.get_ticks() / 20 + i * 45)
            enemy_bullets.append(Bullet(
                self.x + self.w//2, self.y + self.h//2,
                math.cos(angle) * 250, math.sin(angle) * 250,
                color=self.bullet_color, owner="boss", damage=15
            ))

    def attack_phase2(self, enemy_bullets, player):
        # Ataque en onda
        for i in range(5):
            offset = (i - 2) * 0.3
            dx = player.x - self.x + offset * 100
            dy = player.y - self.y
            dist = math.hypot(dx, dy) or 1
            enemy_bullets.append(Bullet(
                self.x + self.w//2, self.y + self.h//2,
                (dx/dist) * 350, (dy/dist) * 350,
                color=self.bullet_color, owner="boss", damage=20
            ))

    def attack_phase3(self, enemy_bullets, player, obstacles):
        attack_type = random.choice(["cross", "circle", "targeted", "obstacles"])
        
        if attack_type == "cross":
            for angle in [0, 90, 180, 270]:
                rad_angle = math.radians(angle)
                enemy_bullets.append(Bullet(
                    self.x + self.w//2, self.y + self.h//2,
                    math.cos(rad_angle) * 400, math.sin(rad_angle) * 400,
                    color=self.bullet_color, owner="boss", damage=25
                ))
                
        elif attack_type == "circle":
            for i in range(12):
                angle = math.radians(i * 30)
                enemy_bullets.append(Bullet(
                    self.x + self.w//2, self.y + self.h//2,
                    math.cos(angle) * 300, math.sin(angle) * 300,
                    color=self.bullet_color, owner="boss", damage=20
                ))
                
        elif attack_type == "targeted":
            for i in range(3):
                dx = player.x - self.x + random.uniform(-20, 20)
                dy = player.y - self.y + random.uniform(-20, 20)
                dist = math.hypot(dx, dy) or 1
                enemy_bullets.append(Bullet(
                    self.x + self.w//2, self.y + self.h//2,
                    (dx/dist) * 450, (dy/dist) * 450,
                    color=WHITE, owner="boss", damage=30
                ))
        
        elif attack_type == "obstacles":
            for i in range(3):
                obstacles.append(Obstacle(
                    random.randint(WIDTH + 50, WIDTH + 200),
                    random.randint(100, HEIGHT - 100),
                    "meteor"
                ))

    def take_damage(self, damage, particle_system):
        self.hp -= damage
        # Crear partículas de impacto
        particle_system.create_impact_lines(self.x + self.w//2, self.y + self.h//2, 8)
        particle_system.create_dust_burst(self.x + self.w//2, self.y + self.h//2, 10)
        return self.hp <= 0

    def start_exit(self):
        self.exiting = True
        self.active = False

    def draw(self, surf):
        if not self.active and self.exiting:
            return
            
        surf.blit(boss_img, (self.x, self.y))
        
        # Barra de vida
        bar_width = 200
        bar_height = 15
        bar_x = self.x + self.w//2 - bar_width//2
        bar_y = self.y - 25
        
        pygame.draw.rect(surf, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        hp_fraction = max(0, self.hp / self.max_hp)
        pygame.draw.rect(surf, WHITE, (bar_x, bar_y, int(bar_width * hp_fraction), bar_height))
        
        names = ["Americano", "Modo Clásico", "Furia Antigua"]
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
        pygame.draw.rect(surf, DARK_GRAY, (self.x, self.y, self.bar_width, self.bar_height), border_radius=10)
        
        energy_ratio = player.energy / player.max_energy
        energy_width = int(self.bar_width * energy_ratio)
        
        if energy_ratio >= 1.0:
            bar_color = MEDIUM_GRAY
        elif energy_ratio >= 0.2:
            bar_color = LIGHT_GRAY
        else:
            bar_color = WHITE
            
        pygame.draw.rect(surf, bar_color, (self.x, self.y, energy_width, self.bar_height), border_radius=10)
        pygame.draw.rect(surf, WHITE, (self.x, self.y, self.bar_width, self.bar_height), 2, border_radius=10)
        
        energy_text = font.render(f"Energía: {player.energy}/{player.max_energy}", True, WHITE)
        surf.blit(energy_text, (self.x, self.y - 25))
        
        if player.energy >= 100:
            missile_text = font.render("MISIL LISTO (Z)", True, WHITE)
        else:
            missile_text = font.render(f"Necesitas {100 - player.energy} más para misil", True, LIGHT_GRAY)
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
            return "A+", WHITE, "¡PERFECTO! El americano ha caído"
        elif score >= 85:
            return "A", LIGHT_GRAY, "¡Excelente! Derrotaste al clásico"
        elif score >= 75:
            return "B", MEDIUM_GRAY, "¡Buen trabajo! Venciste al americano"
        elif score >= 60:
            return "C", LIGHT_GRAY, "¡Bien hecho! Superaste el desafío"
        else:
            return "D", DARK_GRAY, "¡Logrado! El americano ha sido derrotado"
            
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
        
        title_text = title_font.render("¡VICTORIA! - NIVEL 8", True, WHITE)
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
            f"Americano derrotado: {'Sí' if self.boss_defeated else 'No'}"
        ]
        
        for stat in stats:
            stat_text = font.render(stat, True, WHITE)
            surf.blit(stat_text, (WIDTH//2 - stat_text.get_width()//2, stats_y))
            stats_y += 35
        
        phrase_text = font.render(self.motivational_phrase, True, WHITE)
        surf.blit(phrase_text, (WIDTH//2 - phrase_text.get_width()//2, stats_y + 20))
        
        instruction_text = font.render("Presiona ENTER para continuar al siguiente nivel", True, LIGHT_GRAY)
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
        pygame.mixer.music.load("sound/we.mp3")
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
americano = Americano()
title_screen = TitleScreen()
introduction = IntroductionSystem()
energy_ui = EnergyUI()
results_system = ResultsSystem()
knockout_effect = KnockoutEffect()

# Nuevos sistemas
scroll_system = ScrollSystem()
cartoon_particles = CartoonParticleSystem()
bw_effects = BWEffects()

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

effects_activated = False

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
                    subprocess.run([sys.executable, "nivel9.py"])
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
                    americano.entering = True
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

    # Juego principal
    if not game_over and not level_cleared and fight_started and not results_system.active and not knockout_effect.freeze_game:
        current_battle_time = (pygame.time.get_ticks() - battle_start_time) / 1000.0
        
        # Activar efectos especiales después de un tiempo
        if current_battle_time >= 5.0 and not effects_activated:
            bw_effects.activate()
            effects_activated = True
        
        # Actualizar sistemas
        player.update(dt, keys)
        scroll_system.update(dt)
        bw_effects.update(dt)
        cartoon_particles.update(dt)

        # Disparar balas normales
        if keys[pygame.K_x] and player.can_shoot():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            bullet = Bullet(bx, by, 600, 0, color=WHITE, owner="player")
            player_bullets.append(bullet)
            player.shoot()
            # Humo al disparar
            cartoon_particles.create_smoke_trail(bx, by, 3)

        # Lanzar misil
        if keys[pygame.K_z] and player.can_launch_missile():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            missile = Missile(bx, by)
            missiles.append(missile)
            player.launch_missile()
            # Explosión al lanzar misil
            cartoon_particles.create_dust_burst(bx, by, 15)

        # Actualizar americano
        if americano.active or americano.entering or americano.exiting:
            americano.update(dt, enemy_bullets, player, obstacles, cartoon_particles)

        # Actualizar obstáculos
        for obstacle in obstacles[:]:
            obstacle.update(dt)
            if obstacle.x < -50:
                obstacles.remove(obstacle)
                continue
            if player.rect.colliderect(obstacle.rect):
                player.take_damage()
                cartoon_particles.create_impact_lines(obstacle.x, obstacle.y, 10)
                if obstacle in obstacles:
                    obstacles.remove(obstacle)

        # Actualizar balas del jugador
        for b in player_bullets[:]:
            b.update(dt)
            if b.x > WIDTH + 50:
                player_bullets.remove(b)
                continue
            if americano.active and rect_circle_collide(americano.rect, b.x, b.y, b.radius):
                if americano.take_damage(b.damage, cartoon_particles):
                    americano.start_exit()
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
                player.bullets_hit += 1
                if b in player_bullets:
                    player_bullets.remove(b)

        # Actualizar misiles
        for m in missiles[:]:
            m.update(dt)
            if m.x > WIDTH + 50:
                missiles.remove(m)
                continue
            if americano.active and rect_circle_collide(americano.rect, m.x, m.y, m.radius):
                if americano.take_damage(m.damage, cartoon_particles):
                    americano.start_exit()
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
                cartoon_particles.create_impact_lines(b.x, b.y, 8)
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

    # --- DIBUJADO ---
    screen.fill(BLACK)
    
    # Dibujar fondo con scroll
    scroll_offset = scroll_system.get_offset()
    screen.blit(fondo_img, (scroll_offset, 0))
    screen.blit(fondo_img, (scroll_offset + WIDTH, 0))
    
    # Aplicar efectos de blanco y negro
    bw_effects.draw(screen)

    # Dibujar todos los elementos del juego
    americano.draw(screen)

    for b in player_bullets:
        b.draw(screen)
    for b in enemy_bullets:
        b.draw(screen)
    for m in missiles:
        m.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

    if continue_countdown == 0:
        player.draw(screen)
    
    # Dibujar partículas estilo caricatura
    cartoon_particles.draw(screen)
    
    # Dibujar efecto de knockout (encima de todo)
    if knockout_effect.active:
        knockout_effect.draw(screen)

    # UI
    energy_ui.draw(screen, player)
    
    lives_text = font.render(f"Vidas: {player.lives}", True, WHITE)
    screen.blit(lives_text, (12, 12))
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (12, 36))
    
    boss_text = font.render(f"Americano: {'Derrotado' if boss_defeated else 'Vivo'}", True, WHITE)
    screen.blit(boss_text, (WIDTH//2 - boss_text.get_width()//2, 12))
    
    # Indicador de efectos activos
    if effects_activated:
        effect_text = font.render("¡MODO CLÁSICO ACTIVADO!", True, WHITE)
        screen.blit(effect_text, (WIDTH//2 - effect_text.get_width()//2, HEIGHT - 100))
    
    # Indicador de invencibilidad por victoria
    if player.victory_invincible:
        invincible_text = font.render("INVENCIBLE", True, LIGHT_GRAY)
        screen.blit(invincible_text, (WIDTH//2 - invincible_text.get_width()//2, 40))
    
    # Indicador de fase
    if fight_started and not level_cleared and not knockout_effect.freeze_game:
        phase_text = font.render(f"Fase: {americano.phase}/3", True, WHITE)
        screen.blit(phase_text, (WIDTH - 120, 60))

    # Pantalla de continuación
    if continue_countdown > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        continue_text = large_font.render("¡HAS MUERTO!", True, WHITE)
        screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 - 100))
        
        countdown_text = large_font.render(f"Tiempo: {int(continue_countdown)}", True, LIGHT_GRAY)
        screen.blit(countdown_text, (WIDTH//2 - countdown_text.get_width()//2, HEIGHT//2 - 40))
        
        instruction_text = font.render("Presiona C para insertar moneda y continuar", True, WHITE)
        screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 20))
        
        coins_text = font.render(f"Monedas insertadas: {coins_inserted}", True, WHITE)
        screen.blit(coins_text, (WIDTH//2 - coins_text.get_width()//2, HEIGHT//2 + 60))
        
        lives_info = font.render(f"Cada moneda te da {lives_per_coin} vidas", True, LIGHT_GRAY)
        screen.blit(lives_info, (WIDTH//2 - lives_info.get_width()//2, HEIGHT//2 + 90))

    # Game Over
    if game_over and continue_countdown == 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        over_surf = large_font.render("GAME OVER", True, WHITE)
        screen.blit(over_surf, (WIDTH//2 - over_surf.get_width()//2, HEIGHT//2 - 50))
        
        instruction_text = font.render("Presiona ESC para salir", True, WHITE)
        screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()

pygame.quit()