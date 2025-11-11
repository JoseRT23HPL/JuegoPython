import pygame
import random
import math
import subprocess
import sys
from pygame import Rect

# --- Configuración inicial ---
WIDTH, HEIGHT = 960, 540
FPS = 60

# Colores Tetris
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (220, 40, 40)
GREEN = (80, 200, 120)
YELLOW = (240, 220, 80)
BLUE = (80, 160, 240)
GREY = (200,200,200)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
PURPLE = (180, 80, 220)
CYAN = (0, 255, 255)

# Colores adicionales para misiles
MISSILE_COLOR = (255, 50, 255)  # Color morado para el misil
ENERGY_COLOR = (0, 200, 255)    # Color azul para la energía

# Colores piezas Tetris
TETRIS_COLORS = [
    (0, 255, 255),    # I - Cyan
    (0, 0, 255),      # J - Blue
    (255, 165, 0),    # L - Orange
    (255, 255, 0),    # O - Yellow
    (0, 255, 0),      # S - Green
    (128, 0, 128),    # T - Purple
    (255, 0, 0)       # Z - Red
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nivel 4 - Tetris")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 36)
title_font = pygame.font.SysFont("Arial", 48)
dialogue_font = pygame.font.SysFont("Arial", 28)

# --- Recursos ---
try:
    fondo_img = pygame.image.load("img/ciudad2.png").convert()
    fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))
except:
    print("No se pudo cargar ciudad2.png, usando fondo negro")
    fondo_img = pygame.Surface((WIDTH, HEIGHT))
    fondo_img.fill(BLACK)

nave_img_original = pygame.image.load("img/nave.png").convert_alpha()

# Cargar imagen del jefe Tetris
try:
    boss_img = pygame.image.load("img/tetris.png").convert_alpha()
    boss_img = pygame.transform.scale(boss_img, (180, 220))
except:
    print("No se pudo cargar robot.png, creando jefe temporal")
    boss_img = pygame.Surface((180, 220), pygame.SRCALPHA)
    pygame.draw.rect(boss_img, PURPLE, (0, 0, 180, 220), border_radius=20)

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
    robot_img = pygame.image.load("img/tetris.png").convert_alpha()
    robot_img = pygame.transform.scale(robot_img, (300, 300))
    has_robot_img = True
except:
    print("No se pudo cargar la imagen del robot")
    has_robot_img = False

try:
    player_nave_img = pygame.image.load("img/nave.png").convert_alpha()
    player_nave_img = pygame.transform.scale(player_nave_img, (200, 200))
    has_player_nave_img = True
except:
    print("No se pudo cargar la imagen de la nave")
    has_player_nave_img = False

# Música y sonidos
pygame.mixer.music.load("sound/Tetris.mp3")   
pygame.mixer.music.set_volume(0.4)

sonido_inicio = pygame.mixer.Sound("sound/inicio1.mp3")   
sonido_derrota = pygame.mixer.Sound("sound/kn.mp3")       
sonido_daño = pygame.mixer.Sound("sound/hit.mp3")        
sonido_coin = pygame.mixer.Sound("sound/coin.mp3")       
sonido_victoria = pygame.mixer.Sound("sound/victoria.mp3")
sonido_texto = pygame.mixer.Sound("sound/text.mp3")

# Sonido especial Tetris
try:
    sonido_linea = pygame.mixer.Sound("sound/linea.mp3")
    has_linea_sound = True
except:
    print("No se pudo cargar sonido de línea")
    has_linea_sound = False

# Sonido de misil
try:
    sonido_misil = pygame.mixer.Sound("sound/misil.mp3")
    has_missile_sound = True
except:
    print("No se pudo cargar sonido de misil")
    has_missile_sound = False

# Nueva música de victoria
victory_music = "sound/vic.mp3"
intro_music = "sound/vic.mp3"

# --- Efecto Flash ---
class FlashEffect:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.duration = 0.1  # Duración muy corta para flash rápido
        self.alpha = 0
        self.color = WHITE
        self.flash_sequence = []
        self.current_sequence_index = 0
        self.sequence_timer = 0
        
    def activate_sequence(self, sequence_type="battle_start"):
        self.active = True
        self.timer = 0
        self.current_sequence_index = 0
        self.sequence_timer = 0
        
        if sequence_type == "battle_start":
            # Flash en segundo 6, segundo 8, y flash continuo rápido del 9 al 11
            self.flash_sequence = [
                {"time": 6.0, "duration": 0.1, "color": WHITE, "intensity": 200},
                {"time": 8.0, "duration": 0.1, "color": WHITE, "intensity": 200},
                {"time": 9.0, "duration": 2.0, "color": WHITE, "intensity": 150, "rapid": True}
            ]
        
    def update(self, dt, battle_time):
        if not self.active:
            return False
            
        self.timer += dt
        self.sequence_timer += dt
        
        # Buscar si hay algún flash que deba activarse en este momento
        current_flash = None
        for flash in self.flash_sequence:
            if flash["time"] <= battle_time < flash["time"] + flash["duration"]:
                current_flash = flash
                break
        
        if current_flash:
            if "rapid" in current_flash and current_flash["rapid"]:
                # Flash rápido continuo - parpadeo cada 0.1 segundos
                flash_progress = battle_time - current_flash["time"]
                if flash_progress <= current_flash["duration"]:
                    # Parpadeo rápido: 0.1s encendido, 0.1s apagado
                    cycle_time = 0.2  # 0.1s on + 0.1s off
                    cycle_progress = (flash_progress % cycle_time) / cycle_time
                    self.alpha = current_flash["intensity"] if cycle_progress < 0.5 else 0
                else:
                    self.alpha = 0
            else:
                # Flash normal - fade in/out suave
                flash_progress = (battle_time - current_flash["time"]) / current_flash["duration"]
                if flash_progress < 0.5:
                    # Fade in
                    self.alpha = int(current_flash["intensity"] * (flash_progress * 2))
                else:
                    # Fade out
                    self.alpha = int(current_flash["intensity"] * ((1 - flash_progress) * 2))
            
            self.color = current_flash["color"]
        else:
            self.alpha = 0
            
        # Verificar si la secuencia completa ha terminado
        last_flash = max(self.flash_sequence, key=lambda x: x["time"] + x["duration"])
        if battle_time >= last_flash["time"] + last_flash["duration"] + 0.5:
            self.active = False
            return True
            
        return False

    def draw(self, surf):
        if self.alpha > 0:
            flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((self.color[0], self.color[1], self.color[2], self.alpha))
            surf.blit(flash_surface, (0, 0))

# --- Efecto de Transición de Batalla MEJORADO ---
class BattleTransition:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.phase = 0  # 0: blanco y negro, 1: normal
        self.duration_black_white = 3.0
        self.black_white_alpha = 0
        self.flash_effects = []
        
    def activate(self):
        self.active = True
        self.timer = 0
        self.phase = 0
        self.black_white_alpha = 255
        self.flash_effects = []
        # Crear efectos de flash iniciales
        for _ in range(10):
            self.flash_effects.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.randint(30, 80),
                'alpha': 255,
                'color': random.choice(TETRIS_COLORS),
                'lifetime': random.uniform(0.4, 1.2)
            })
        
    def update(self, dt):
        if not self.active:
            return False
            
        self.timer += dt
        
        if self.phase == 0:  # Blanco y negro con flashes
            progress = self.timer / self.duration_black_white
            self.black_white_alpha = int(255 * (1.0 - progress))
            
            # Actualizar flashes
            for flash in self.flash_effects[:]:
                flash['alpha'] -= int(255 * dt / flash['lifetime'])
                if flash['alpha'] <= 0:
                    self.flash_effects.remove(flash)
            
            # Agregar nuevos flashes aleatorios
            if random.random() < 0.4:
                self.flash_effects.append({
                    'x': random.randint(0, WIDTH),
                    'y': random.randint(0, HEIGHT),
                    'size': random.randint(20, 60),
                    'alpha': 255,
                    'color': random.choice(TETRIS_COLORS),
                    'lifetime': random.uniform(0.3, 0.8)
                })
            
            if self.timer >= self.duration_black_white:
                self.phase = 1
                self.timer = 0
                
        elif self.phase == 1:  # Finalizado
            self.active = False
            return True
            
        return False

    def draw(self, surf):
        if not self.active:
            return
            
        # Dibujar efectos de flash
        for flash in self.flash_effects:
            flash_surface = pygame.Surface((flash['size'], flash['size']), pygame.SRCALPHA)
            pygame.draw.rect(flash_surface, (*flash['color'], flash['alpha']), 
                           (0, 0, flash['size'], flash['size']), border_radius=8)
            surf.blit(flash_surface, (flash['x'] - flash['size']//2, flash['y'] - flash['size']//2))
        
        # Aplicar efecto blanco y negro
        if self.black_white_alpha > 0:
            bw_surface = pygame.Surface((WIDTH, HEIGHT))
            bw_surface.fill(BLACK)
            
            # Convertir a escala de grises
            for x in range(0, WIDTH, 4):
                for y in range(0, HEIGHT, 4):
                    if x < WIDTH and y < HEIGHT:
                        try:
                            color = surf.get_at((x, y))
                            gray = int(color.r * 0.299 + color.g * 0.587 + color.b * 0.114)
                            bw_surface.set_at((x, y), (gray, gray, gray))
                        except:
                            pass
            
            bw_surface.set_alpha(self.black_white_alpha)
            surf.blit(bw_surface, (0, 0))

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
                "speaker": "robot",
                "text": "JEJEJE… ¡BIENVENIDO AL TABLERO FINAL, PILOTO!",
                "position": "right"
            },
            {
                "speaker": "player", 
                "text": "¿Qué es este lugar? Todo parece… un rompecabezas roto.",
                "position": "left"
            },
            {
                "speaker": "robot",
                "text": "¡No un rompecabezas, un juego perfecto! Cada pieza encaja, excepto tú.",
                "position": "right"
            },
            {
                "speaker": "player",
                "text": "No pienso convertirme en otra ficha de tu colección.",
                "position": "left"
            },
            {
                "speaker": "both",
                "text": "¡INICIANDO PROTOCOLO TETRIS!",
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
        
        # Fondo temático Tetris
        for i in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            color = random.choice(TETRIS_COLORS)
            size = random.randint(2, 5)
            pygame.draw.rect(surf, color, (x, y, size, size))
        
        # Marco decorativo
        pygame.draw.rect(surf, GREY, (20, 20, WIDTH-40, HEIGHT-40), 4, border_radius=10)
        pygame.draw.rect(surf, CYAN, (30, 30, WIDTH-60, HEIGHT-60), 2, border_radius=8)
        
        current_dialogue = self.dialogues[self.current_dialogue]
        
        # Dibujar personajes según quién habla
        if current_dialogue["speaker"] == "robot" or current_dialogue["speaker"] == "both":
            if has_robot_img:
                char_x = WIDTH - 350
                char_y = HEIGHT//2 - 150
                robot_colored = robot_img.copy()
                robot_colored.fill(random.choice(TETRIS_COLORS), special_flags=pygame.BLEND_RGBA_MULT)
                surf.blit(robot_colored, (char_x, char_y))
        
        if current_dialogue["speaker"] == "player" or current_dialogue["speaker"] == "both":
            if has_player_nave_img:
                char_x = 50
                char_y = HEIGHT//2 - 100
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
        
        # Dibujar cuadro de diálogo
        pygame.draw.rect(surf, (30, 30, 50), dialog_rect, border_radius=15)
        pygame.draw.rect(surf, CYAN, dialog_rect, 3, border_radius=15)
        
        # Nombre del personaje
        speaker_names = {
            "robot": "TETRIS MASTER",
            "player": "TU NAVE",
            "both": "ENFRENTAMIENTO TETRIS"
        }
        
        name_colors = {
            "robot": RED,
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
        
        # Fondo con piezas Tetris cayendo
        for i in range(20):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            color = random.choice(TETRIS_COLORS)
            size = random.randint(10, 30)
            pygame.draw.rect(surf, color, (x, y, size, size))
        
        title_surface = title_font.render("NIVEL 4", True, CYAN)
        title_surface.set_alpha(self.alpha)
        surf.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, HEIGHT//2 - 100))
        
        subtitle_surface = dialogue_font.render("TETRIS", True, YELLOW)
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

# --- Línea de Bloques con Huecos MEJORADA - HUECOS MÁS GRANDES ---
class BlockLine:
    def __init__(self, direction="vertical"):
        self.direction = direction
        self.blocks = []
        self.speed = 300
        self.active = True
        self.color = random.choice(TETRIS_COLORS)
        self.block_size = 30
        
        # Crear huecos aleatorios MÁS GRANDES (3 huecos de 2 cuadros cada uno en fase 3)
        if direction == "vertical":
            self.x = WIDTH  # Comienza desde la derecha
            self.y = 0
            self.width = self.block_size
            self.height = HEIGHT
            
            # Crear lista de bloques con huecos
            num_blocks = HEIGHT // self.block_size
            self.block_positions = list(range(num_blocks))
            
            # En fase 3, crear 3 huecos de 2 cuadros cada uno (más espacio para esquivar)
            if len(self.block_positions) >= 6:
                # Elegir 3 posiciones iniciales aleatorias para huecos dobles
                gap_starts = []
                for _ in range(3):
                    available_positions = [pos for pos in range(num_blocks - 1) 
                                         if all(abs(pos - existing) > 2 for existing in gap_starts)]
                    if available_positions:
                        gap_start = random.choice(available_positions)
                        gap_starts.append(gap_start)
                        # Remover 2 posiciones consecutivas
                        for i in range(2):
                            if gap_start + i in self.block_positions:
                                self.block_positions.remove(gap_start + i)
            
            # Crear rectángulos para cada bloque
            for pos in self.block_positions:
                block_rect = pygame.Rect(
                    self.x, 
                    pos * self.block_size, 
                    self.block_size, 
                    self.block_size
                )
                self.blocks.append(block_rect)
                
        else:  # horizontal
            self.x = 0
            self.y = HEIGHT  # Comienza desde abajo
            self.width = WIDTH
            self.height = self.block_size
            
            # Crear lista de bloques con huecos
            num_blocks = WIDTH // self.block_size
            self.block_positions = list(range(num_blocks))
            
            # En fase 3, crear 3 huecos de 2 cuadros cada uno (más espacio para esquivar)
            if len(self.block_positions) >= 6:
                # Elegir 3 posiciones iniciales aleatorias para huecos dobles
                gap_starts = []
                for _ in range(3):
                    available_positions = [pos for pos in range(num_blocks - 1) 
                                         if all(abs(pos - existing) > 2 for existing in gap_starts)]
                    if available_positions:
                        gap_start = random.choice(available_positions)
                        gap_starts.append(gap_start)
                        # Remover 2 posiciones consecutivas
                        for i in range(2):
                            if gap_start + i in self.block_positions:
                                self.block_positions.remove(gap_start + i)
            
            # Crear rectángulos para cada bloque
            for pos in self.block_positions:
                block_rect = pygame.Rect(
                    pos * self.block_size,
                    self.y, 
                    self.block_size, 
                    self.block_size
                )
                self.blocks.append(block_rect)

    def update(self, dt):
        if self.direction == "vertical":
            self.x -= self.speed * dt
            # Actualizar posición de todos los bloques
            for block in self.blocks:
                block.x = self.x
        else:  # horizontal
            self.y -= self.speed * dt
            # Actualizar posición de todos los bloques
            for block in self.blocks:
                block.y = self.y
        
        # Desactivar si sale de la pantalla
        if self.direction == "vertical" and self.x < -self.block_size:
            self.active = False
        elif self.direction == "horizontal" and self.y < -self.block_size:
            self.active = False

    def draw(self, surf):
        for block in self.blocks:
            pygame.draw.rect(surf, self.color, block)
            pygame.draw.rect(surf, WHITE, block, 2)

# --- Piezas de Tetris Mejoradas CON CAÍDA CONTINUA ---
class TetrisPiece:
    def __init__(self, piece_type=None):
        if piece_type is None:
            piece_type = random.choice(["I", "J", "L", "O", "S", "T", "Z"])
        
        self.piece_type = piece_type
        self.color = TETRIS_COLORS[["I", "J", "L", "O", "S", "T", "Z"].index(piece_type)]
        self.blocks = []
        self.x = random.randint(50, WIDTH - 100)  # Distribuido en toda la pantalla
        self.y = -100
        self.speed = random.randint(200, 300)  # Velocidad más constante
        self.rotation = 0
        self.size = 25
        
        # Sistema de movimiento CONTINUO (sin pausas)
        self.rotate_timer = 0
        self.rotate_delay = random.uniform(0.8, 1.5)  # Tiempo entre rotaciones
        
        # Definir formas de las piezas para cada rotación
        self.shapes = self.get_shapes(piece_type)
        self.current_shape = self.shapes[0]
        self.update_blocks()
        
    def get_shapes(self, piece_type):
        # Definir todas las rotaciones posibles para cada pieza
        shapes_dict = {
            "I": [
                [[1, 1, 1, 1]],
                [[1], [1], [1], [1]]
            ],
            "J": [
                [[1, 0, 0], [1, 1, 1]],
                [[1, 1], [1, 0], [1, 0]],
                [[1, 1, 1], [0, 0, 1]],
                [[0, 1], [0, 1], [1, 1]]
            ],
            "L": [
                [[0, 0, 1], [1, 1, 1]],
                [[1, 0], [1, 0], [1, 1]],
                [[1, 1, 1], [1, 0, 0]],
                [[1, 1], [0, 1], [0, 1]]
            ],
            "O": [
                [[1, 1], [1, 1]]
            ],
            "S": [
                [[0, 1, 1], [1, 1, 0]],
                [[1, 0], [1, 1], [0, 1]]
            ],
            "T": [
                [[0, 1, 0], [1, 1, 1]],
                [[1, 0], [1, 1], [1, 0]],
                [[1, 1, 1], [0, 1, 0]],
                [[0, 1], [1, 1], [0, 1]]
            ],
            "Z": [
                [[1, 1, 0], [0, 1, 1]],
                [[0, 1], [1, 1], [1, 0]]
            ]
        }
        return shapes_dict.get(piece_type, shapes_dict["I"])
        
    def update_blocks(self):
        self.blocks = []
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    block_x = self.x + x * self.size
                    block_y = self.y + y * self.size
                    self.blocks.append(pygame.Rect(block_x, block_y, self.size, self.size))
    
    def rotate(self):
        if len(self.shapes) > 1:  # Solo rotar si tiene múltiples formas
            self.rotation = (self.rotation + 1) % len(self.shapes)
            self.current_shape = self.shapes[self.rotation]
            self.update_blocks()
    
    def update(self, dt):
        self.rotate_timer += dt
        
        # Rotación periódica
        if self.rotate_timer >= self.rotate_delay:
            self.rotate()
            self.rotate_timer = 0
            self.rotate_delay = random.uniform(0.8, 1.5)  # Variar el tiempo entre rotaciones
        
        # CAÍDA CONTINUA - sin pausas, movimiento fluido
        self.y += self.speed * dt
        
        self.update_blocks()
        return self.y > HEIGHT + 100
    
    def draw(self, surf):
        for block in self.blocks:
            pygame.draw.rect(surf, self.color, block)
            pygame.draw.rect(surf, WHITE, block, 2)

# --- NUEVO ATAQUE: Patrón de Tetris que se mueve ---
class TetrisPattern:
    def __init__(self):
        self.blocks = []
        self.speed = 200
        self.active = True
        self.color = random.choice(TETRIS_COLORS)
        self.block_size = 30
        self.direction = random.choice(["left", "right", "down"])
        
        # Crear un patrón de Tetris (una pieza L grande)
        self.pattern = [
            [1, 0, 0],
            [1, 0, 0],
            [1, 1, 1]
        ]
        
        # Posición inicial según la dirección
        if self.direction == "left":
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT - len(self.pattern) * self.block_size)
        elif self.direction == "right":
            self.x = -len(self.pattern[0]) * self.block_size
            self.y = random.randint(0, HEIGHT - len(self.pattern) * self.block_size)
        else:  # down
            self.x = random.randint(0, WIDTH - len(self.pattern[0]) * self.block_size)
            self.y = -len(self.pattern) * self.block_size
        
        self.create_blocks()
        
    def create_blocks(self):
        self.blocks = []
        for y, row in enumerate(self.pattern):
            for x, cell in enumerate(row):
                if cell:
                    block_x = self.x + x * self.block_size
                    block_y = self.y + y * self.block_size
                    self.blocks.append(pygame.Rect(block_x, block_y, self.block_size, self.block_size))
    
    def update(self, dt):
        # Mover según la dirección
        if self.direction == "left":
            self.x -= self.speed * dt
        elif self.direction == "right":
            self.x += self.speed * dt
        else:  # down
            self.y += self.speed * dt
        
        # Actualizar posición de todos los bloques
        self.create_blocks()
        
        # Desactivar si sale de la pantalla
        if (self.direction == "left" and self.x < -len(self.pattern[0]) * self.block_size) or \
           (self.direction == "right" and self.x > WIDTH) or \
           (self.direction == "down" and self.y > HEIGHT):
            self.active = False

    def draw(self, surf):
        for block in self.blocks:
            pygame.draw.rect(surf, self.color, block)
            pygame.draw.rect(surf, WHITE, block, 2)

# --- Ambiente Retro Tetris MEJORADO con efectos de luz ---
class RetroTetrisAmbience:
    def __init__(self):
        self.grid_visible = True
        self.grid_timer = 0
        self.grid_alpha = 100
        self.light_effects = []
        self.light_timer = 0
        
    def update(self, dt):
        # Parpadeo de la grid
        self.grid_timer += dt
        if self.grid_timer >= 0.5:
            self.grid_alpha = random.randint(80, 120)
            self.grid_timer = 0
            
        # Efectos de luz aleatorios
        self.light_timer += dt
        if self.light_timer >= 0.2 and random.random() < 0.3:
            self.light_effects.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'radius': random.randint(5, 15),
                'alpha': random.randint(100, 200),
                'color': random.choice(TETRIS_COLORS),
                'lifetime': random.uniform(0.5, 1.5)
            })
            self.light_timer = 0
            
        # Actualizar efectos de luz
        for light in self.light_effects[:]:
            light['lifetime'] -= dt
            if light['lifetime'] <= 0:
                self.light_effects.remove(light)
            else:
                light['alpha'] = int(light['alpha'] * 0.95)
                
    def draw(self, surf):
        # Dibujar grid de fondo estilo Tetris
        if self.grid_visible:
            grid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            
            # Líneas verticales
            for x in range(0, WIDTH, 30):
                pygame.draw.line(grid_surface, (GREY[0], GREY[1], GREY[2], self.grid_alpha), 
                               (x, 0), (x, HEIGHT), 1)
            
            # Líneas horizontales  
            for y in range(0, HEIGHT, 30):
                pygame.draw.line(grid_surface, (GREY[0], GREY[1], GREY[2], self.grid_alpha), 
                               (0, y), (WIDTH, y), 1)
                
            surf.blit(grid_surface, (0, 0))
            
        # Dibujar efectos de luz
        for light in self.light_effects:
            light_surface = pygame.Surface((light['radius']*2, light['radius']*2), pygame.SRCALPHA)
            pygame.draw.circle(light_surface, (*light['color'], light['alpha']), 
                             (light['radius'], light['radius']), light['radius'])
            surf.blit(light_surface, (light['x'] - light['radius'], light['y'] - light['radius']))
            
        # Efecto de scanlines retro
        scanlines = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(0, HEIGHT, 3):
            pygame.draw.line(scanlines, (0, 0, 0, 30), (0, y), (WIDTH, y), 1)
        surf.blit(scanlines, (0, 0))

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
            score -= continues_used * 25
        
        if damage_taken > 0:
            score -= min(damage_taken * 5, 30)
        
        if accuracy < 0.7:
            score -= 10
        
        if completion_time > 120:
            score -= 10

        if score >= 95:
            return "A+", GOLD, "¡PERFECTO! Eres un maestro del Tetris"
        elif score >= 85:
            return "A", GREEN, "¡Excelente! Dominas el tablero espacial"
        elif score >= 75:
            return "B", BLUE, "¡Buen trabajo! Piezas bien encajadas"
        elif score >= 60:
            return "C", YELLOW, "¡Bien hecho! Sigue mejorando tu estrategia"
        else:
            return "D", ORANGE, "¡Sigue practicando! El tablero te espera"
            
    def update(self, dt):
        if not self.active:
            return False
            
        self.animation_timer += dt
        return self.animation_timer >= self.animation_duration
        
    def draw(self, surf):
        if not self.active:
            return
            
        progress = min(1.0, self.animation_timer / self.animation_duration)
        
        # Fondo con animación de fade in
        overlay_alpha = int(200 * progress)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, overlay_alpha))
        surf.blit(overlay, (0, 0))
        
        # Título con animación de escala
        title_scale = 0.5 + 0.5 * progress
        title_text = title_font.render("¡LÍNEA COMPLETA!", True, CYAN)
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
            instruction_text = font.render("Presiona ENTER para continuar al siguiente nivel", True, YELLOW)
            instruction_text.set_alpha(instruction_alpha)
            instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT - 60))
            surf.blit(instruction_text, instruction_rect)

# --- Clase Missile ---
class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.speed = 400
        self.color = MISSILE_COLOR
        self.trail_particles = []
        self.rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)
        self.damage = 200
        self.glow_timer = 0
        self.explosion_radius = 80  # Radio de explosión para daño en área

    def update(self, dt):
        self.x += self.speed * dt
        
        # Partículas de estela
        if random.random() < 0.7:
            self.trail_particles.append({
                'x': self.x - 10,
                'y': self.y + random.uniform(-5, 5),
                'size': random.randint(3, 6),
                'life': 1.0,
                'color': random.choice([MISSILE_COLOR, (255, 100, 255), (200, 80, 255)])
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

# --- Sistema de UI para Energía ---
class EnergyUI:
    def __init__(self):
        self.bar_width = 300
        self.bar_height = 20
        self.x = WIDTH - self.bar_width - 20
        self.y = 60  # Debajo de la barra de vida del boss
        self.pulse_timer = 0

    def draw(self, surf, player):
        self.pulse_timer += 0.05
        
        # Fondo de la barra
        pygame.draw.rect(surf, (50, 50, 50), (self.x, self.y, self.bar_width, self.bar_height), border_radius=10)
        
        energy_ratio = player.energy / player.max_energy
        energy_width = int(self.bar_width * energy_ratio)
        
        # Color de la barra según la energía disponible
        if energy_ratio >= 1.0:
            bar_color = MISSILE_COLOR
            # Efecto de pulso cuando está llena
            pulse = (math.sin(self.pulse_timer) * 0.2 + 0.8)
            energy_width = int(self.bar_width * pulse)
        elif energy_ratio >= 0.2:
            bar_color = ENERGY_COLOR
        else:
            bar_color = RED
            
        # Barra de energía
        pygame.draw.rect(surf, bar_color, (self.x, self.y, energy_width, self.bar_height), border_radius=10)
        pygame.draw.rect(surf, WHITE, (self.x, self.y, self.bar_width, self.bar_height), 2, border_radius=10)
        
        # Texto de energía
        energy_text = font.render(f"Energía: {int(player.energy)}/{player.max_energy}", True, WHITE)
        surf.blit(energy_text, (self.x, self.y - 25))
        
        # Indicador de misil listo
        if player.energy >= 100:
            missile_text = font.render("MISIL LISTO (Z)", True, GREEN)
        else:
            missile_text = font.render(f"Necesitas {100 - int(player.energy)} más para misil", True, YELLOW)
        surf.blit(missile_text, (self.x, self.y + 25))

# --- Clases del Juego ---
class Player:
    def __init__(self):
        self.base_size = 48
        self.size = self.base_size
        self.x = 80
        self.y = HEIGHT // 2
        self.speed = 5.0
        self.base_speed = 5.0
        self.shrink_speed = 7.0
        self.lives = 3
        self.max_lives = 3
        self.shoot_cooldown = 0.12
        self.shoot_timer = 0.0
        self.is_shrunk = False
        self.rect = Rect(self.x, self.y, self.size, self.size)
        self.invulnerable = False
        self.invulnerable_timer = 0.0
        self.damage_taken = 0
        self.bullets_shot = 0
        self.bullets_hit = 0
        
        # NUEVO: Sistema de energía y misiles
        self.energy = 0
        self.max_energy = 500
        self.missile_cooldown = 0.0
        self.missile_cooldown_time = 2.0
        self.energy_gain_rate = 10  # Energía ganada por segundo
        self.energy_gain_timer = 0.0

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

        self.x += vx * speed
        self.y += vy * speed
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))
        self.rect = Rect(int(self.x), int(self.y), self.size, self.size)

        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        # NUEVO: Actualizar energía y cooldown de misil
        if self.missile_cooldown > 0:
            self.missile_cooldown -= dt
            
        # Ganar energía gradualmente
        self.energy_gain_timer += dt
        if self.energy_gain_timer >= 0.1:  # Cada 0.1 segundos
            self.add_energy(self.energy_gain_rate * 0.1)
            self.energy_gain_timer = 0

        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

    def draw(self, surf):
        nave_scaled = pygame.transform.scale(nave_img_original, (self.size, self.size))
        if self.invulnerable and int(self.invulnerable_timer * 10) % 2 == 0:
            return
        surf.blit(nave_scaled, (self.x, self.y))

    def can_shoot(self):
        return (not self.is_shrunk) and self.shoot_timer <= 0

    def shoot(self):
        self.shoot_timer = self.shoot_cooldown
        self.bullets_shot += 1

    # NUEVO: Métodos para el sistema de misiles
    def can_launch_missile(self):
        return (self.energy >= 100 and 
                self.missile_cooldown <= 0 and 
                not self.is_shrunk)

    def launch_missile(self):
        if self.can_launch_missile():
            self.energy -= 100
            self.missile_cooldown = self.missile_cooldown_time
            if has_missile_sound:
                sonido_misil.play()
            return True
        return False

    def add_energy(self, amount):
        self.energy = min(self.max_energy, self.energy + amount)

    def take_damage(self):
        if not self.invulnerable:
            self.lives -= 1
            self.damage_taken += 1
            sonido_daño.play()
            self.invulnerable = True
            self.invulnerable_timer = 3.0
            self.x = max(0, self.x - 40)

    def add_lives(self, amount):
        self.lives += amount
        if self.lives > self.max_lives:
            self.lives = self.max_lives

class Bullet:
    def __init__(self, x, y, vx, vy, color=YELLOW, owner="player"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 6 if owner=="player" else 8
        self.color = color
        self.owner = owner
        self.rect = Rect(int(self.x-self.radius), int(self.y-self.radius), self.radius*2, self.radius*2)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)

class Boss:
    def __init__(self):
        self.w = 180
        self.h = 220
        self.x = WIDTH + 200
        self.y = (HEIGHT - self.h) // 2
        self.max_hp = 4000
        self.hp = self.max_hp
        self.phase = 1
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.timer = 0.0
        self.attack_cooldown = 2.0
        self.attack_timer = 1.0
        self.dir = 1
        self.move_timer = 0.0
        self.move_cooldown = 0.8
        self.entering = True
        self.exiting = False
        self.nucleo_visible = False
        self.nucleo_timer = 0.0
        self.nucleo_cooldown = 8.0
        self.nucleo_hp = 500
        
        # NUEVAS ANIMACIONES
        self.pulse_timer = 0.0
        self.pulse_scale = 1.0
        self.glow_alpha = 0
        self.glow_timer = 0.0
        self.particle_effects = []

        # Fase 1: Piezas que caen - LIMITADO A 4-5 PIEZAS
        self.falling_pieces = []
        self.piece_spawn_timer = 0.0
        self.piece_spawn_cooldown = 2.0  # Más lento
        self.max_falling_pieces = 5  # MÁXIMO 5 PIEZAS A LA VEZ

        # Fase 2: Líneas de bloques
        self.block_lines = []
        self.line_attack_timer = 0.0
        self.line_attack_cooldown = 4.0

        # Fase 3: Ataque final MEJORADO - líneas con MÁS HUECOS
        self.final_attack_timer = 0.0
        self.final_attack_cooldown = 10.0
        
        # NUEVO: Patrones de Tetris (solo en fase 3, menos frecuentes)
        self.tetris_patterns = []
        self.pattern_timer = 0.0
        self.pattern_cooldown = 8.0

    def update(self, dt, bullets, player, enemy_bullets, fight_started):
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

        ratio = self.hp / self.max_hp
        if ratio > 0.66:
            self.phase = 1
        elif ratio > 0.33:
            self.phase = 2
        else:
            self.phase = 3

        # Movimiento del jefe
        self.move_timer -= dt
        if self.move_timer <= 0:
            self.move_timer = self.move_cooldown
            self.y += 40 * self.dir
            if self.y < 10 or self.y + self.h > HEIGHT - 10:
                self.dir *= -1
                self.y += 40 * self.dir
        self.rect.topleft = (int(self.x), int(self.y))

        # NUEVAS ANIMACIONES
        self.pulse_timer += dt
        self.pulse_scale = 1.0 + 0.05 * math.sin(self.pulse_timer * 3)
        
        self.glow_timer += dt
        self.glow_alpha = 50 + int(50 * math.sin(self.glow_timer * 2))
        
        # Actualizar partículas
        for particle in self.particle_effects[:]:
            particle['lifetime'] -= dt
            if particle['lifetime'] <= 0:
                self.particle_effects.remove(particle)
            else:
                particle['x'] += particle['vx'] * dt
                particle['y'] += particle['vy'] * dt
                particle['alpha'] = int(255 * (particle['lifetime'] / particle['max_lifetime']))

        if not fight_started:
            return

        # Sistema de núcleo en fase 3
        if self.phase == 3:
            self.nucleo_timer += dt
            if self.nucleo_timer >= self.nucleo_cooldown and not self.nucleo_visible:
                self.nucleo_visible = True
                self.nucleo_timer = 0
                # Efecto especial cuando aparece el núcleo
                for _ in range(15):
                    self.particle_effects.append({
                        'x': self.x + self.w//2,
                        'y': self.y + self.h//2,
                        'vx': random.uniform(-100, 100),
                        'vy': random.uniform(-100, 100),
                        'color': random.choice(TETRIS_COLORS),
                        'size': random.randint(3, 8),
                        'alpha': 255,
                        'lifetime': random.uniform(0.5, 1.5),
                        'max_lifetime': 1.5
                    })
            elif self.nucleo_visible and self.nucleo_timer >= 5.0:
                self.nucleo_visible = False
                self.nucleo_timer = 0

        # Ataques según fase
        if self.phase == 1:
            self.phase_attack_1(dt, enemy_bullets)
        elif self.phase == 2:
            self.phase_attack_2(dt, enemy_bullets)
        else:
            self.phase_attack_3(dt, enemy_bullets)

        # Actualizar piezas que caen (fases 1 y 3) - LIMITADO
        for piece in self.falling_pieces[:]:
            if piece.update(dt):
                self.falling_pieces.remove(piece)
            elif player.rect.collidelist(piece.blocks) != -1:
                player.take_damage()
                if piece in self.falling_pieces:
                    self.falling_pieces.remove(piece)

        # Actualizar líneas de bloques (fase 2 y 3)
        for line in self.block_lines[:]:
            line.update(dt)
            if not line.active:
                self.block_lines.remove(line)
            else:
                # Colisión jugador con bloques
                for block in line.blocks:
                    if player.rect.colliderect(block):
                        player.take_damage()
                        # No remover el bloque para mantener consistencia visual
                        
        # Actualizar patrones de Tetris (fase 3, menos frecuentes)
        for pattern in self.tetris_patterns[:]:
            pattern.update(dt)
            if not pattern.active:
                self.tetris_patterns.remove(pattern)
            else:
                # Colisión jugador con patrones
                for block in pattern.blocks:
                    if player.rect.colliderect(block):
                        player.take_damage()
                        # No remover el bloque para mantener consistencia visual

    def phase_attack_1(self, dt, enemy_bullets):
        # Fase 1: Piezas de Tetris cayendo distribuidas en toda la pantalla - LIMITADO
        self.piece_spawn_timer += dt
        if self.piece_spawn_timer >= self.piece_spawn_cooldown and len(self.falling_pieces) < self.max_falling_pieces:
            # Crear solo 1 pieza a la vez, no múltiples
            self.falling_pieces.append(TetrisPiece())
            self.piece_spawn_timer = 0
            self.piece_spawn_cooldown = random.uniform(1.5, 2.5)  # Más lento

        # Disparos ocasionales
        self.attack_timer -= dt
        if self.attack_timer <= 0:
            self.attack_timer = self.attack_cooldown
            cx = self.x
            cy = self.y + self.h * 0.5
            for angle_deg in (-15, 0, 15):
                rad = math.radians(angle_deg)
                vx = -300 * math.cos(rad)
                vy = 300 * math.sin(rad)
                enemy_bullets.append(Bullet(cx, cy, vx, vy, color=RED, owner="boss"))

    def phase_attack_2(self, dt, enemy_bullets):
        # Fase 2: Líneas de bloques con huecos MÁS GRANDES
        self.line_attack_timer += dt
        if self.line_attack_timer >= self.line_attack_cooldown:
            # Crear línea vertical que avanza desde la derecha
            self.block_lines.append(BlockLine("vertical"))
            self.line_attack_timer = 0
            self.line_attack_cooldown = random.uniform(3.0, 5.0)
            
            if has_linea_sound:
                sonido_linea.play()

        # Disparos más frecuentes
        self.attack_timer -= dt
        if self.attack_timer <= 0:
            self.attack_timer = self.attack_cooldown * 0.7
            cx = self.x
            cy = self.y + self.h * 0.5
            num_bullets = 5
            for i in range(num_bullets):
                angle = (i / num_bullets) * math.pi - math.pi/2
                vx = -350 * math.cos(angle)
                vy = 350 * math.sin(angle)
                enemy_bullets.append(Bullet(cx, cy, vx, vy, color=random.choice(TETRIS_COLORS), owner="boss"))

    def phase_attack_3(self, dt, enemy_bullets):
        # Fase 3: Ataque final MEJORADO - líneas con MÁS HUECOS (3 huecos de 2 cuadros)
        self.final_attack_timer += dt
        if self.final_attack_timer >= self.final_attack_cooldown:
            # En fase 3, crear 2 líneas con MÁS HUECOS (3 huecos de 2 cuadros cada uno)
            for i in range(2):
                self.block_lines.append(BlockLine("vertical"))
            self.final_attack_timer = 0
            
            if has_linea_sound:
                sonido_linea.play()

        # Piezas que caen (como en fase 1 pero más frecuentes) - LIMITADO
        self.piece_spawn_timer += dt
        if self.piece_spawn_timer >= self.piece_spawn_cooldown * 0.5 and len(self.falling_pieces) < self.max_falling_pieces:
            # Solo 1 pieza a la vez
            self.falling_pieces.append(TetrisPiece())
            self.piece_spawn_timer = 0
            self.piece_spawn_cooldown = random.uniform(1.0, 2.0)  # Aún limitado

        # NUEVO: Patrones de Tetris (menos frecuentes en fase 3)
        self.pattern_timer += dt
        if self.pattern_timer >= self.pattern_cooldown:
            self.tetris_patterns.append(TetrisPattern())
            self.pattern_timer = 0
            self.pattern_cooldown = random.uniform(6.0, 9.0)  # Más espaciados

        # Disparos en espiral
        self.attack_timer -= dt
        if self.attack_timer <= 0:
            self.attack_timer = self.attack_cooldown * 0.5
            cx = self.x
            cy = self.y + self.h * 0.5
            num_bullets = 8
            base_angle = random.uniform(0, math.pi*2)
            for i in range(num_bullets):
                angle = base_angle + (i/num_bullets) * math.pi * 2
                vx = -400 * math.cos(angle)
                vy = 400 * math.sin(angle)
                enemy_bullets.append(Bullet(cx, cy, vx, vy, color=random.choice(TETRIS_COLORS), owner="boss"))

    def draw(self, surf):
        # Dibujar partículas
        for particle in self.particle_effects:
            particle_surface = pygame.Surface((particle['size']*2, particle['size']*2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*particle['color'], particle['alpha']), 
                             (particle['size'], particle['size']), particle['size'])
            surf.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))
        
        if self.hp > 0:
            # Efecto de glow alrededor del jefe
            if self.glow_alpha > 0:
                glow_surface = pygame.Surface((int(self.w * 1.2), int(self.h * 1.2)), pygame.SRCALPHA)
                phase_colors = {1: (0, 255, 0), 2: (255, 255, 0), 3: (255, 0, 0)}
                glow_color = phase_colors.get(self.phase, (255, 255, 255))
                pygame.draw.rect(glow_surface, (*glow_color, self.glow_alpha), 
                               (0, 0, int(self.w * 1.2), int(self.h * 1.2)), 
                               border_radius=25)
                surf.blit(glow_surface, (self.x - self.w * 0.1, self.y - self.h * 0.1))
            
            # Dibujar jefe base con efecto de pulso
            scaled_boss = pygame.transform.scale(boss_img, 
                                               (int(self.w * self.pulse_scale), 
                                                int(self.h * self.pulse_scale)))
            boss_rect = scaled_boss.get_rect(center=(self.x + self.w//2, self.y + self.h//2))
            surf.blit(scaled_boss, boss_rect)
            
            # Dibujar núcleo en fase 3 si es visible
            if self.phase == 3 and self.nucleo_visible:
                nucleo_rect = pygame.Rect(self.x + self.w//2 - 20, self.y + self.h//2 - 20, 40, 40)
                pygame.draw.rect(surf, GOLD, nucleo_rect)
                pygame.draw.rect(surf, YELLOW, nucleo_rect, 3)
                
                # Efecto de brillo pulsante
                pulse_alpha = 100 + int(100 * math.sin(self.pulse_timer * 5))
                glow_rect = pygame.Rect(self.x + self.w//2 - 25, self.y + self.h//2 - 25, 50, 50)
                pygame.draw.rect(surf, (255, 255, 200, pulse_alpha), glow_rect, border_radius=10)

        # Dibujar líneas de bloques
        for line in self.block_lines:
            line.draw(surf)
            
        # Dibujar patrones de Tetris
        for pattern in self.tetris_patterns:
            pattern.draw(surf)

        # Barra de vida
        bar_w = 200
        bar_h = 18
        bar_x = WIDTH - bar_w - 20
        bar_y = 12
        pygame.draw.rect(surf, (80,80,80), (bar_x, bar_y, bar_w, bar_h))
        hp_fraction = max(0, self.hp / self.max_hp)
        
        # Color de la barra según la fase
        if self.phase == 1:
            bar_color = GREEN
        elif self.phase == 2:
            bar_color = YELLOW
        else:
            bar_color = RED
            
        pygame.draw.rect(surf, bar_color, (bar_x, bar_y, int(bar_w*hp_fraction), bar_h))
        
        phase_names = {1: "PIEZAS CAYENDO", 2: "LÍNEAS CON HUECOS", 3: "ATAQUE FINAL"}
        hp_text = font.render(f"TETRIS MASTER - {phase_names[self.phase]}", True, WHITE)
        surf.blit(hp_text, (bar_x, bar_y + bar_h + 2))
        
        # Mostrar HP del núcleo en fase 3
        if self.phase == 3 and self.nucleo_visible:
            nucleo_text = font.render(f"NÚCLEO: {self.nucleo_hp}/500", True, YELLOW)
            surf.blit(nucleo_text, (bar_x, bar_y + bar_h + 24))

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
        pygame.mixer.music.load("sound/Tetris.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except:
        print("No se pudo cargar la música normal")

# --- Estado del juego ---
player = Player()
boss = Boss()
player_bullets = []
enemy_bullets = []
missiles = []  # NUEVO: Lista para misiles
score = 0
game_over = False
level_cleared = False
fight_timer = 0.0
fight_started = False
boss_defeated_sound_played = False

# Sistema de continuación
continue_countdown = 0
continue_time = 10.0
coins_inserted = 0
continues_used = 0
continue_available = True
lives_per_coin = 3

# Estadísticas
game_start_time = 0
completion_time = 0
victory_sound_played = False
victory_music_playing = False

# Efectos
scroll_x = 0
vel_fondo = 100

# Nuevos sistemas
title_screen = TitleScreen()
introduction = IntroductionSystem()
battle_transition = BattleTransition()
retro_ambience = RetroTetrisAmbience()
knockout_effect = KnockoutEffect()
results_system = ResultsSystem()
flash_effect = FlashEffect()  # NUEVO: Efecto flash
energy_ui = EnergyUI()  # NUEVO: UI de energía

# Efectos de cámara
camera_shake = 0
camera_shake_intensity = 0

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
                    boss.falling_pieces.clear()
                    boss.block_lines.clear()
                    boss.tetris_patterns.clear()
                    missiles.clear()  # NUEVO: Limpiar misiles también
                    player.x = 80
                    player.y = HEIGHT // 2
            if event.key == pygame.K_RETURN and results_system.active and results_system.animation_timer >= results_system.animation_duration:
                running = False
                pygame.quit()
                try:
                    subprocess.run([sys.executable, "nivel5.py"])  # Cambiar por tu siguiente nivel
                except:
                    print("No se pudo cargar el siguiente nivel")
                sys.exit()
            if event.key == pygame.K_x and introduction.active:
                result = introduction.advance_text()
                if result == "start_battle":
                    play_normal_music()
                    battle_transition.activate()
                    fight_started = True
                    sonido_inicio.play()
                    # ACTIVAR SECUENCIA DE FLASHES
                    flash_effect.activate_sequence("battle_start")

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

    # Transición de batalla
    if battle_transition.active:
        battle_transition_finished = battle_transition.update(dt)
        if battle_transition_finished:
            battle_transition.active = False

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

    # Actualizar conteo regresivo
    if continue_countdown > 0:
        continue_countdown -= dt
        if continue_countdown <= 0:
            continue_countdown = 0
            game_over = True

    # Efecto de sacudida de cámara
    if camera_shake > 0:
        camera_shake -= dt
        camera_shake_intensity = camera_shake * 10

    # Actualizar ambiente retro
    retro_ambience.update(dt)

    # Actualizar efecto flash si está activo
    if flash_effect.active:
        flash_effect.update(dt, fight_timer)

    if not game_over and not level_cleared and continue_countdown == 0 and not results_system.active:
        fight_timer += dt
        
        # Actualizar jugador
        player.update(dt, keys)

        # Disparar balas normales
        if fight_started and keys[pygame.K_x] and player.can_shoot():
            bx = player.x + player.size + 6
            by = player.y + player.size/2
            bullet = Bullet(bx, by, 600, 0, color=GREEN, owner="player")
            player_bullets.append(bullet)
            player.shoot()

        # NUEVO: Lanzar misil con Z
        if fight_started and keys[pygame.K_z] and player.can_launch_missile():
            bx = player.x + player.size + 6
            by = player.y + player.size/2
            missile = Missile(bx, by)
            missiles.append(missile)
            player.launch_missile()
            # Efecto de pantalla al lanzar misil
            camera_shake = 0.2

        boss.update(dt, player_bullets, player, enemy_bullets, fight_started)

        # Colisión balas jugador con jefe
        for b in player_bullets[:]:
            b.update(dt)
            if b.x > WIDTH+50:
                player_bullets.remove(b)
                continue
            if rect_circle_collide(boss.rect, b.x, b.y, b.radius) and not boss.entering:
                boss.hp -= 10
                player.bullets_hit += 1
                if b in player_bullets:
                    player_bullets.remove(b)
                score += 5
                camera_shake = 0.1
                
                # Efecto de partículas al golpear
                for _ in range(5):
                    boss.particle_effects.append({
                        'x': b.x,
                        'y': b.y,
                        'vx': random.uniform(-50, 50),
                        'vy': random.uniform(-50, 50),
                        'color': random.choice(TETRIS_COLORS),
                        'size': random.randint(2, 5),
                        'alpha': 255,
                        'lifetime': random.uniform(0.3, 0.8),
                        'max_lifetime': 0.8
                    })
                
                if boss.hp <= 0 and not boss_defeated_sound_played:
                    boss_defeated_sound_played = True
                    knockout_effect.activate()

        # NUEVO: Actualizar misiles
        for missile in missiles[:]:
            missile.update(dt)
            if missile.x > WIDTH + 50:
                missiles.remove(missile)
                continue
                
            # Colisión misil con boss
            if rect_circle_collide(boss.rect, missile.x, missile.y, missile.radius) and not boss.entering:
                boss.hp -= missile.damage
                player.bullets_hit += 1
                score += 50
                camera_shake = 0.5
                
                # Efecto de explosión grande
                for _ in range(15):
                    boss.particle_effects.append({
                        'x': missile.x,
                        'y': missile.y,
                        'vx': random.uniform(-100, 100),
                        'vy': random.uniform(-100, 100),
                        'color': MISSILE_COLOR,
                        'size': random.randint(4, 8),
                        'alpha': 255,
                        'lifetime': random.uniform(0.5, 1.2),
                        'max_lifetime': 1.2
                    })
                
                if missile in missiles:
                    missiles.remove(missile)
                    
                if boss.hp <= 0 and not boss_defeated_sound_played:
                    boss_defeated_sound_played = True
                    knockout_effect.activate()

            # Colisión misil con núcleo
            if boss.phase == 3 and boss.nucleo_visible:
                nucleo_rect = pygame.Rect(boss.x + boss.w//2 - 20, boss.y + boss.h//2 - 20, 40, 40)
                if nucleo_rect.collidepoint(missile.x, missile.y):
                    boss.nucleo_hp -= missile.damage * 2  # Doble daño al núcleo
                    player.bullets_hit += 1
                    score += 100
                    camera_shake = 0.8
                    
                    # Efecto de explosión nuclear
                    for _ in range(20):
                        boss.particle_effects.append({
                            'x': missile.x,
                            'y': missile.y,
                            'vx': random.uniform(-150, 150),
                            'vy': random.uniform(-150, 150),
                            'color': GOLD,
                            'size': random.randint(5, 10),
                            'alpha': 255,
                            'lifetime': random.uniform(0.7, 1.5),
                            'max_lifetime': 1.5
                        })
                    
                    if missile in missiles:
                        missiles.remove(missile)
                        
                    if boss.nucleo_hp <= 0:
                        boss.hp = 0
                        if not boss_defeated_sound_played:
                            boss_defeated_sound_played = True
                            knockout_effect.activate()

        # Colisión balas enemigas con jugador
        for b in enemy_bullets[:]:
            b.update(dt)
            if b.x < -50 or b.y < -50 or b.y > HEIGHT+50:
                enemy_bullets.remove(b)
                continue
            if rect_circle_collide(player.rect, b.x, b.y, b.radius):
                player.take_damage()
                if b in enemy_bullets:
                    enemy_bullets.remove(b)
                camera_shake = 0.3

        if player.lives <= 0 and continue_available:
            continue_countdown = continue_time
            coins_inserted = 0

        if boss.hp <= 0 and not boss.exiting:
            boss.exiting = True
            pygame.mixer.music.stop()
            completion_time = (pygame.time.get_ticks() - game_start_time) / 1000.0

    # --- Dibujado ---
    # Aplicar efecto de sacudida de cámara
    shake_x = random.uniform(-camera_shake_intensity, camera_shake_intensity) if camera_shake > 0 else 0
    shake_y = random.uniform(-camera_shake_intensity, camera_shake_intensity) if camera_shake > 0 else 0
    
    scroll_x -= vel_fondo * dt
    if scroll_x <= -WIDTH:
        scroll_x = 0
    
    screen.blit(fondo_img, (int(scroll_x + shake_x), int(shake_y)))
    screen.blit(fondo_img, (int(scroll_x + shake_x)+WIDTH, int(shake_y)))

    # Dibujar ambiente retro
    retro_ambience.draw(screen)

    # Dibujar piezas cayendo
    for piece in boss.falling_pieces:
        piece.draw(screen)

    for b in player_bullets:
        b.draw(screen)
    for b in enemy_bullets:
        b.draw(screen)

    # NUEVO: Dibujar misiles
    for missile in missiles:
        missile.draw(screen)

    boss.draw(screen)
    
    # Dibujar efecto de knockout
    knockout_effect.draw(screen)
    
    # Dibujar efecto flash
    flash_effect.draw(screen)
    
    # Dibujar transición de batalla
    if battle_transition.active:
        battle_transition.draw(screen)
    
    if continue_countdown == 0 and not results_system.active:
        player.draw(screen)

    # NUEVO: Dibujar UI de energía
    energy_ui.draw(screen, player)

    lives_text = font.render(f"Vidas: {player.lives}", True, WHITE)
    screen.blit(lives_text, (12, 12))
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (12, 36))

    if not fight_started and not introduction.active and not battle_transition.active:
        wait_txt = font.render("Presiona X para comenzar la batalla", True, GREY)
        screen.blit(wait_txt, (WIDTH//2 - wait_txt.get_width()//2, HEIGHT-30))

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