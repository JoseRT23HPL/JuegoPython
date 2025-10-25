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
BROWN = (139, 69, 19)
PURPLE = (180, 80, 220)
DARK_BLUE = (20, 30, 60)
LIGHT_BLUE = (100, 150, 255)
NEON_PURPLE = (200, 60, 255)
NEON_GREEN = (60, 255, 150)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial - Misil Sagrado")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 32, bold=True)
dialogue_font = pygame.font.SysFont("Arial", 22)

# --- Recursos ---
fondo_img = pygame.image.load("img/pasillo.jpg").convert()
fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))

nave_img_original = pygame.image.load("img/nave.png").convert_alpha()
enemy_img = pygame.image.load("img/e1.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 40))
girl_img = pygame.image.load("img/niña.jpeg").convert_alpha()
girl_img = pygame.transform.scale(girl_img, (300, 400))

# Música y sonidos
pygame.mixer.music.load("sound/cosmo.mp3")   
pygame.mixer.music.set_volume(0.4)

intro_music = "sound/vic.mp3"

sonido_inicio = pygame.mixer.Sound("sound/inicio1.mp3")   
sonido_daño = pygame.mixer.Sound("sound/hit.mp3")        
sonido_victoria = pygame.mixer.Sound("sound/bravo.mp3") 
sonido_texto = pygame.mixer.Sound("sound/text.mp3")
sonido_misil = pygame.mixer.Sound("sound/misil.mp3")
sonido_seleccion = pygame.mixer.Sound("sound/coin.mp3")  # Sonido de selección
sonido_energy = pygame.mixer.Sound("sound/coin.mp3")  # Sonido para ganar energía

victory_music = "sound/vic.mp3"

# --- Sistema de Diálogos Mejorado ---
class DialogueSystem:
    def __init__(self):
        self.dialogue_active = True
        self.current_line = 0
        self.lines = [
            "¡Bienvenido, guerrero! Ahora aprenderás a usar el Misil Sagrado.",
            "El Misil Sagrado es un arma poderosa que consume ENERGÍA.",
            "Cada misil cuesta 100 puntos de energía para ser lanzado.",
            "La energía se consigue haciendo daño a los enemigos.",
            "Cada golpe a un enemigo te dará entre 5 y 15 puntos de energía.",
            "Tu medidor de energía puede almacenar hasta 500 puntos.",
            "Usa la tecla Z para lanzar un Misil Sagrado.",
            "¡Practica en este campo de tiro! Los enemigos no te atacarán."
        ]
        self.text_speed = 0
        self.current_char = 0
        self.text_timer = 0
        self.music_started = False
        self.sound_played = False
        self.pulse_effect = 0
        self.stars = []

    def create_stars(self):
        """Crea estrellas de fondo para el diálogo"""
        self.stars = []
        for _ in range(50):
            self.stars.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.1, 0.5),
                'brightness': random.randint(100, 255)
            })

    def calculate_text_speed(self):
        """Calcula la velocidad para que cada línea dure 4 segundos"""
        if self.current_line < len(self.lines):
            line_length = len(self.lines[self.current_line])
            self.text_speed = line_length / 4.0

    def start_intro_music(self):
        """Inicia la música de introducción"""
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
        """Detiene la música de introducción"""
        pygame.mixer.music.stop()
        self.music_started = False

    def update(self, dt):
        self.text_timer += dt
        self.pulse_effect = (self.pulse_effect + dt * 5) % (2 * math.pi)
        
        # Actualizar estrellas
        for star in self.stars:
            star['brightness'] = 100 + int(100 * math.sin(star['speed'] * pygame.time.get_ticks() / 1000))
        
        target_chars = int(self.text_timer * self.text_speed)
        
        if target_chars > self.current_char:
            chars_to_add = target_chars - self.current_char
            old_char = self.current_char
            self.current_char = min(self.current_char + chars_to_add, len(self.lines[self.current_line]))
            
            if old_char == 0 and self.current_char > 0 and not self.sound_played:
                sonido_texto.play()
                self.sound_played = True

    def draw(self, surf):
        # Fondo espacial animado
        surf.fill(DARK_BLUE)
        
        # Dibujar estrellas
        for star in self.stars:
            brightness = star['brightness']
            color = (brightness, brightness, brightness)
            pygame.draw.circle(surf, color, (star['x'], star['y']), star['size'])
        
        # Efecto de gradiente
        for y in range(HEIGHT):
            alpha = int(100 * (1 - y / HEIGHT))
            color = (20, 30, 80, alpha)
            pygame.draw.line(surf, color, (0, y), (WIDTH, y))
        
        # Marco decorativo
        pulse = int(50 * (1 + math.sin(self.pulse_effect)))
        pygame.draw.rect(surf, (30, 20, 60), (10, 10, WIDTH-20, HEIGHT-20), border_radius=15)
        pygame.draw.rect(surf, (pulse + 50, 40, pulse + 100), (15, 15, WIDTH-30, HEIGHT-30), 4, border_radius=12)
        
        # Imagen de la guía
        girl_x = 50
        girl_y = HEIGHT//2 - 180
        surf.blit(girl_img, (girl_x, girl_y))
        
        # Efecto de brillo alrededor de la imagen
        glow_size = 20
        for i in range(glow_size, 0, -2):
            alpha = 100 - (i * 5)
            glow_surf = pygame.Surface((300 + i*2, 400 + i*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (100, 50, 150, alpha), (0, 0, 300 + i*2, 400 + i*2), border_radius=10)
            surf.blit(glow_surf, (girl_x - i, girl_y - i))
        
        # Panel de diálogo mejorado
        dialog_rect = pygame.Rect(380, HEIGHT//2 - 150, WIDTH - 430, 300)
        
        # Fondo con gradiente
        for i, y in enumerate(range(dialog_rect.top, dialog_rect.bottom)):
            progress = (y - dialog_rect.top) / dialog_rect.height
            r = int(30 + 20 * progress)
            g = int(20 + 10 * progress)
            b = int(50 + 30 * progress)
            pygame.draw.line(surf, (r, g, b), (dialog_rect.left, y), (dialog_rect.right, y))
        
        pygame.draw.rect(surf, (80, 60, 140), dialog_rect, 3, border_radius=15)
        pygame.draw.rect(surf, (40, 30, 80), dialog_rect, 1, border_radius=15)
        
        # Título con efecto
        title_shadow = title_font.render("Tutorial - Misil Sagrado", True, (100, 50, 150))
        title_text = title_font.render("Tutorial - Misil Sagrado", True, GOLD)
        surf.blit(title_shadow, (dialog_rect.centerx - title_shadow.get_width()//2 + 2, dialog_rect.y + 22))
        surf.blit(title_text, (dialog_rect.centerx - title_text.get_width()//2, dialog_rect.y + 20))
        
        # Línea decorativa bajo el título
        line_y = dialog_rect.y + 60
        pygame.draw.line(surf, PURPLE, (dialog_rect.x + 20, line_y), (dialog_rect.right - 20, line_y), 2)
        
        # Texto del diálogo
        current_text = self.lines[self.current_line][:self.current_char]
        
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
        
        text_y = dialog_rect.y + 80
        for line in lines:
            if line.strip():
                # Sombra del texto
                shadow_surface = dialogue_font.render(line, True, (20, 10, 40))
                surf.blit(shadow_surface, (dialog_rect.x + 22, text_y + 2))
                
                # Texto principal
                line_surface = dialogue_font.render(line, True, WHITE)
                surf.blit(line_surface, (dialog_rect.x + 20, text_y))
                text_y += 35
        
        # Indicador de continuación
        if self.current_char >= len(self.lines[self.current_line]):
            prompt_text = "Presiona X para continuar" if self.current_line < len(self.lines) - 1 else "Presiona X para comenzar práctica"
            
            # Efecto de parpadeo
            if pygame.time.get_ticks() % 1000 < 800:
                prompt_shadow = dialogue_font.render(prompt_text, True, (30, 80, 30))
                prompt = dialogue_font.render(prompt_text, True, NEON_GREEN)
                surf.blit(prompt_shadow, (dialog_rect.centerx - prompt_shadow.get_width()//2 + 1, dialog_rect.bottom - 47))
                surf.blit(prompt, (dialog_rect.centerx - prompt.get_width()//2, dialog_rect.bottom - 50))
                
                # Triángulo animado
                triangle_size = 10 + int(3 * math.sin(pygame.time.get_ticks() * 0.01))
                triangle_points = [
                    (dialog_rect.centerx + prompt.get_width()//2 + 25, dialog_rect.bottom - 40),
                    (dialog_rect.centerx + prompt.get_width()//2 + 25 + triangle_size, dialog_rect.bottom - 40),
                    (dialog_rect.centerx + prompt.get_width()//2 + 25 + triangle_size//2, dialog_rect.bottom - 25)
                ]
                pygame.draw.polygon(surf, YELLOW, triangle_points)
        else:
            # Puntos suspensivos animados
            dots_alpha = int(150 * (1 + math.sin(pygame.time.get_ticks() * 0.005)))
            dots_text = dialogue_font.render("...", True, (YELLOW[0], YELLOW[1], YELLOW[2], dots_alpha))
            surf.blit(dots_text, (dialog_rect.right - 50, dialog_rect.bottom - 50))

    def advance_text(self):
        sonido_texto.play()
        
        if self.current_char < len(self.lines[self.current_line]):
            self.current_char = len(self.lines[self.current_line])
        else:
            self.current_line += 1
            self.current_char = 0
            self.text_timer = 0
            self.sound_played = False
            
            if self.current_line >= len(self.lines):
                self.dialogue_active = False
                self.stop_intro_music()
                return "start_practice"
        return "continue"

# --- Sistema de Confirmación de Salida Mejorado ---
class ExitConfirmation:
    def __init__(self):
        self.active = False
        self.selected_option = 0  # 0: Quedarse, 1: Salir
        self.fade_alpha = 0
        self.fading_out = False
        self.pulse = 0
        
    def show(self):
        self.active = True
        self.selected_option = 0
        self.fade_alpha = 0
        self.fading_out = False
        sonido_seleccion.play()
        
    def update(self, dt):
        self.pulse = (self.pulse + dt * 6) % (2 * math.pi)
        if self.fading_out:
            self.fade_alpha = min(255, self.fade_alpha + int(500 * dt))
            return self.fade_alpha >= 255
        return False
        
    def handle_input(self, event):
        if not self.active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.selected_option = 1 - self.selected_option  # Cambiar entre 0 y 1
                sonido_seleccion.play()
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 1:  # Salir seleccionado
                    self.fading_out = True
                    sonido_seleccion.play()
                    return True
                else:  # Quedarse seleccionado
                    self.active = False
                    sonido_seleccion.play()
            elif event.key == pygame.K_ESCAPE:
                self.active = False
                sonido_seleccion.play()
        return False
        
    def draw(self, surf):
        if not self.active and not self.fading_out:
            return
            
        # Fondo semitransparente con efecto
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(0, HEIGHT, 4):
            alpha = 150 + int(50 * math.sin(y * 0.02 + self.pulse))
            pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (WIDTH, y), 4)
        surf.blit(overlay, (0, 0))
        
        # Panel de confirmación con efecto de brillo
        panel_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 100, 400, 200)
        
        # Fondo del panel con gradiente
        for y in range(panel_rect.top, panel_rect.bottom):
            progress = (y - panel_rect.top) / panel_rect.height
            r = int(40 + 30 * progress)
            g = int(30 + 20 * progress)
            b = int(60 + 40 * progress)
            pygame.draw.line(surf, (r, g, b), (panel_rect.left, y), (panel_rect.right, y))
        
        # Borde animado
        border_color = (100 + int(50 * math.sin(self.pulse)), 
                       60 + int(30 * math.sin(self.pulse + 1)), 
                       150 + int(50 * math.sin(self.pulse + 2)))
        pygame.draw.rect(surf, border_color, panel_rect, 4, border_radius=20)
        pygame.draw.rect(surf, (200, 180, 255), panel_rect, 2, border_radius=20)
        
        # Título con efecto
        title_shadow = title_font.render("¿Estás listo?", True, (80, 40, 120))
        title = title_font.render("¿Estás listo?", True, GOLD)
        surf.blit(title_shadow, (panel_rect.centerx - title_shadow.get_width()//2 + 2, panel_rect.y + 22))
        surf.blit(title, (panel_rect.centerx - title.get_width()//2, panel_rect.y + 20))
        
        # Mensaje
        message = dialogue_font.render("¿Te sientes preparado para el Nivel 5?", True, WHITE)
        surf.blit(message, (panel_rect.centerx - message.get_width()//2, panel_rect.y + 70))
        
        # Opciones
        options = ["Seguir practicando", "¡Al Nivel 5!"]
        option_y = panel_rect.y + 120
        
        for i, option in enumerate(options):
            if i == self.selected_option:
                # Opción seleccionada con efecto
                color = NEON_GREEN
                glow = large_font.render(option, True, (30, 100, 30))
                surf.blit(glow, (panel_rect.centerx - glow.get_width()//2 + 1, option_y + 1))
                
                # Indicadores animados
                indicator_size = 8 + int(2 * math.sin(self.pulse * 2))
                left_indicator = [
                    (panel_rect.x + 40, option_y + 10),
                    (panel_rect.x + 40 + indicator_size, option_y + 10 - indicator_size//2),
                    (panel_rect.x + 40 + indicator_size, option_y + 10 + indicator_size//2)
                ]
                right_indicator = [
                    (panel_rect.right - 40, option_y + 10),
                    (panel_rect.right - 40 - indicator_size, option_y + 10 - indicator_size//2),
                    (panel_rect.right - 40 - indicator_size, option_y + 10 + indicator_size//2)
                ]
                pygame.draw.polygon(surf, NEON_GREEN, left_indicator)
                pygame.draw.polygon(surf, NEON_GREEN, right_indicator)
            else:
                color = GREY
                
            option_text = large_font.render(option, True, color)
            surf.blit(option_text, (panel_rect.centerx - option_text.get_width()//2, option_y))
            option_y += 40
        
        # Instrucciones
        instructions = font.render("← → para seleccionar, ENTER para confirmar", True, YELLOW)
        surf.blit(instructions, (panel_rect.centerx - instructions.get_width()//2, panel_rect.bottom - 30))
        
        # Aplicar fade out si está activo
        if self.fading_out:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill(BLACK)
            fade_surface.set_alpha(self.fade_alpha)
            surf.blit(fade_surface, (0, 0))

# --- Clases del Juego (con mejoras visuales) ---
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
        
        # Sistema de energía para misiles
        self.energy = 0
        self.max_energy = 500
        self.missile_cooldown = 0.0
        self.missile_cooldown_time = 2.0
        self.energy_particles = []

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

        # Actualizar partículas de energía
        for p in self.energy_particles[:]:
            p['life'] -= dt
            if p['life'] <= 0:
                self.energy_particles.remove(p)

    def draw(self, surf):
        nave_scaled = pygame.transform.scale(nave_img_original, (self.size, self.size))
        if self.invulnerable and int(self.invulnerable_timer * 10) % 2 == 0:
            return
            
        # Efecto de brillo cuando tiene energía para misil
        if self.energy >= 100:
            glow_size = 5
            for i in range(glow_size, 0, -1):
                alpha = 50 - i * 8
                glow_surf = pygame.Surface((self.size + i*4, self.size + i*4), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (100, 200, 255, alpha), 
                               (0, 0, self.size + i*4, self.size + i*4), 
                               border_radius=10)
                surf.blit(glow_surf, (self.x - i*2, self.y - i*2))
        
        surf.blit(nave_scaled, (self.x, self.y))
        
        # Dibujar partículas de energía
        for p in self.energy_particles:
            alpha = int(p['life'] * 255)
            size = int(p['size'] * p['life'])
            energy_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            pygame.draw.circle(energy_surf, (100, 200, 255, alpha), (size, size), size)
            surf.blit(energy_surf, (p['x'] - size, p['y'] - size))

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
        old_energy = self.energy
        self.energy = min(self.max_energy, self.energy + amount)
        
        # Crear partículas cuando se gana energía
        if amount > 0:
            for _ in range(5):
                self.energy_particles.append({
                    'x': self.x + random.randint(0, self.size),
                    'y': self.y + random.randint(0, self.size),
                    'size': random.randint(2, 4),
                    'life': 1.0
                })
            sonido_energy.play()

    def activate(self):
        self.active = True

class Bullet:
    def __init__(self, x, y, vx, vy, color=NEON_GREEN, owner="player", damage=10):
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

    def update(self, dt):
        # Guardar posición para la estela
        if len(self.trail) < 5:
            self.trail.append((self.x, self.y))
        else:
            self.trail.pop(0)
            self.trail.append((self.x, self.y))
            
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))

    def draw(self, surf):
        # Dibujar estela
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(100 * (i / len(self.trail)))
            size = int(self.radius * 0.7 * (i / len(self.trail)))
            trail_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (*self.color[:3], alpha), (size, size), size)
            surf.blit(trail_surf, (trail_x - size, trail_y - size))
        
        # Dibujar bala principal
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y)), self.radius - 2)

class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.speed = 400
        self.color = NEON_PURPLE
        self.trail_particles = []
        self.rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)
        self.glow_effect = 0

    def update(self, dt):
        self.glow_effect = (self.glow_effect + dt * 10) % (2 * math.pi)
        self.x += self.speed * dt
        
        # Añadir partículas de estela
        if random.random() < 0.7:
            self.trail_particles.append({
                'x': self.x - 10,
                'y': self.y + random.uniform(-5, 5),
                'size': random.randint(3, 6),
                'life': 1.0,
                'color': random.choice([NEON_PURPLE, (255, 100, 255), (200, 60, 255)])
            })
        
        # Actualizar partículas
        for particle in self.trail_particles[:]:
            particle['life'] -= dt * 2
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
                
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))

    def draw(self, surf):
        # Dibujar estela
        for particle in self.trail_particles:
            alpha = int(particle['life'] * 255)
            color = (*particle['color'][:3], alpha)
            particle_surf = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, (particle['size']//2, particle['size']//2), particle['size']//2)
            surf.blit(particle_surf, (particle['x'], particle['y']))
        
        # Efecto de brillo
        glow_size = self.radius + int(3 * math.sin(self.glow_effect))
        glow_surf = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*self.color[:3], 100), (glow_size, glow_size), glow_size)
        surf.blit(glow_surf, (self.x - glow_size, self.y - glow_size))
        
        # Dibujar misil
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)
        # Detalles del misil
        pygame.draw.circle(surf, YELLOW, (int(self.x + 8), int(self.y)), 4)
        pygame.draw.circle(surf, WHITE, (int(self.x + 8), int(self.y)), 2)

class Enemy:
    def __init__(self, x, y, enemy_type="basic"):
        self.w = 40
        self.h = 40
        self.x = x
        self.y = y
        self.hp = 30
        self.max_hp = 30
        self.enemy_type = enemy_type
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color = RED
        self.respawn_timer = 0
        self.active = True
        self.hit_effect = 0
        
        if enemy_type == "fast":
            self.hp = 20
            self.max_hp = 20
            self.color = BLUE
        elif enemy_type == "tank":
            self.hp = 60
            self.max_hp = 60
            self.color = ORANGE

    def update(self, dt):
        if not self.active:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.respawn()
            return
                
        if self.hit_effect > 0:
            self.hit_effect -= dt
                
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        if not self.active:
            return
            
        # Efecto de golpe
        if self.hit_effect > 0:
            glow_surf = pygame.Surface((self.w + 10, self.h + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (255, 100, 100, 150), (0, 0, self.w + 10, self.h + 10), border_radius=8)
            surf.blit(glow_surf, (self.x - 5, self.y - 5))
            
        enemy_scaled = pygame.transform.scale(enemy_img, (self.w, self.h))
        surf.blit(enemy_scaled, (self.x, self.y))
        
        # Barra de vida mejorada
        if self.hp < self.max_hp:
            health_bg = Rect(self.x, self.y - 12, self.w, 6)
            health_width = (self.w * self.hp) // self.max_hp
            health_rect = Rect(self.x, self.y - 12, health_width, 6)
            
            pygame.draw.rect(surf, (50, 50, 50), health_bg, border_radius=3)
            pygame.draw.rect(surf, GREEN, health_rect, border_radius=3)
            pygame.draw.rect(surf, WHITE, health_bg, 1, border_radius=3)

    def take_damage(self, damage):
        if not self.active:
            return 0
            
        self.hp -= damage
        self.hit_effect = 0.3  # Activar efecto visual
        # Energía reducida: 5-15 puntos en lugar de 10-30
        energy_gained = random.randint(5, 15)
        
        if self.hp <= 0:
            self.active = False
            self.respawn_timer = 2.0
            return energy_gained * 2  # Doble energía por eliminar
            
        return energy_gained

    def respawn(self):
        self.active = True
        self.hp = self.max_hp
        self.x = random.randint(WIDTH // 2, WIDTH - 100)
        self.y = random.randint(50, HEIGHT - 50)

# --- Sistema de UI para Energía Mejorado ---
class EnergyUI:
    def __init__(self):
        self.bar_width = 300
        self.bar_height = 25
        self.x = WIDTH - self.bar_width - 20
        self.y = 15
        self.pulse_effect = 0

    def draw(self, surf, player):
        self.pulse_effect = (self.pulse_effect + 0.1) % (2 * math.pi)
        
        # Fondo de la barra con efecto 3D
        pygame.draw.rect(surf, (30, 30, 50), (self.x, self.y, self.bar_width, self.bar_height), border_radius=8)
        pygame.draw.rect(surf, (60, 60, 80), (self.x, self.y, self.bar_width, self.bar_height), 2, border_radius=8)
        
        # Barra de energía
        energy_ratio = player.energy / player.max_energy
        energy_width = int(self.bar_width * energy_ratio)
        
        if energy_ratio >= 1.0:
            # Efecto especial cuando está llena
            pulse = int(50 * (1 + math.sin(self.pulse_effect)))
            bar_color = (150 + pulse, 60, 200 + pulse)
        elif energy_ratio >= 0.2:
            bar_color = LIGHT_BLUE
        else:
            bar_color = RED
            
        if energy_width > 0:
            pygame.draw.rect(surf, bar_color, (self.x, self.y, energy_width, self.bar_height), border_radius=8)
            
            # Efecto de brillo interior
            if energy_ratio >= 0.3:
                highlight_height = self.bar_height // 2
                highlight_rect = Rect(self.x, self.y, energy_width, highlight_height)
                highlight_surf = pygame.Surface((energy_width, highlight_height), pygame.SRCALPHA)
                highlight_surf.fill((255, 255, 255, 60))
                surf.blit(highlight_surf, highlight_rect)
        
        # Borde exterior
        border_color = WHITE
        if energy_ratio >= 1.0:
            border_color = (255, 215, 0)  # Dorado cuando está lleno
        elif energy_ratio >= 0.2:
            border_color = BLUE
            
        pygame.draw.rect(surf, border_color, (self.x, self.y, self.bar_width, self.bar_height), 2, border_radius=8)
        
        # Texto mejorado
        energy_shadow = font.render(f"Energía: {player.energy}/{player.max_energy}", True, (20, 20, 40))
        energy_text = font.render(f"Energía: {player.energy}/{player.max_energy}", True, WHITE)
        surf.blit(energy_shadow, (self.x + 1, self.y - 26))
        surf.blit(energy_text, (self.x, self.y - 27))
        
        # Indicador de misil con efectos
        if player.energy >= 100:
            missile_shadow = font.render("MISIL LISTO (Z)", True, (30, 80, 30))
            missile_text = font.render("MISIL LISTO (Z)", True, NEON_GREEN)
            
            # Efecto de parpadeo cuando está listo
            if pygame.time.get_ticks() % 1000 < 800:
                surf.blit(missile_shadow, (self.x + 1, self.y + 31))
                surf.blit(missile_text, (self.x, self.y + 30))
        else:
            needed = 100 - player.energy
            missile_text = font.render(f"Necesitas {needed} más para misil", True, YELLOW)
            surf.blit(missile_text, (self.x, self.y + 30))

# --- Funciones auxiliares ---
def rect_circle_collide(rect, circle_x, circle_y, radius):
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))
    dx = circle_x - closest_x
    dy = circle_y - closest_y
    return dx * dx + dy * dy <= radius * radius

def play_normal_music():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("cosmo.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except:
        print("No se pudo cargar la música normal")

# --- Estado del juego ---
player = Player()
player_bullets = []
missiles = []
enemies = []
dialogue = DialogueSystem()
dialogue.create_stars()  # Crear estrellas para el fondo
energy_ui = EnergyUI()
exit_confirmation = ExitConfirmation()

# Crear enemigos de práctica
for i in range(5):
    enemy_type = random.choice(["basic", "fast", "tank"])
    x = random.randint(WIDTH // 2, WIDTH - 100)
    y = random.randint(50, HEIGHT - 50)
    enemies.append(Enemy(x, y, enemy_type))

score = 0
practice_started = False
tutorial_completed = False

# Calcular velocidad inicial para la primera línea
dialogue.calculate_text_speed()

# --- Main loop ---
running = True
while running:
    dt_ms = clock.tick(FPS)
    dt = dt_ms / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if exit_confirmation.active:
            if exit_confirmation.handle_input(event):
                # Fade completado, ir al nivel 5
                running = False
                pygame.quit()
                try:
                    subprocess.run([sys.executable, "nivel5.py"])
                except:
                    print("No se pudo cargar el nivel 5")
                sys.exit()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_x:
                    if dialogue.dialogue_active:
                        result = dialogue.advance_text()
                        if result == "start_practice":
                            play_normal_music()
                            player.activate()
                            practice_started = True
                if event.key == pygame.K_RETURN and practice_started:
                    # Mostrar confirmación de salida
                    exit_confirmation.show()

    keys = pygame.key.get_pressed()

    # Actualizar confirmación de salida
    if exit_confirmation.update(dt):
        continue

    # Sistema de diálogos
    if dialogue.dialogue_active:
        dialogue.start_intro_music()
        dialogue.update(dt)
        dialogue.draw(screen)
        pygame.display.flip()
        continue

    # Juego principal (campo de práctica)
    if practice_started and not exit_confirmation.active:
        player.update(dt, keys)

        # Disparar balas normales
        if keys[pygame.K_x] and player.can_shoot():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            bullet = Bullet(bx, by, 600, 0, color=NEON_GREEN, owner="player")
            player_bullets.append(bullet)
            player.shoot()

        # Lanzar misil
        if keys[pygame.K_z] and player.can_launch_missile():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            missile = Missile(bx, by)
            missiles.append(missile)
            player.launch_missile()

        # Actualizar balas
        for b in player_bullets[:]:
            b.update(dt)
            if b.x > WIDTH + 50:
                player_bullets.remove(b)
                continue
            for e in enemies:
                if e.active and rect_circle_collide(e.rect, b.x, b.y, b.radius):
                    energy_gained = e.take_damage(b.damage)
                    player.add_energy(energy_gained)
                    player.bullets_hit += 1
                    if b in player_bullets:
                        player_bullets.remove(b)
                    break

        # Actualizar misiles
        for m in missiles[:]:
            m.update(dt)
            if m.x > WIDTH + 50:
                missiles.remove(m)
                continue
            for e in enemies:
                if e.active and rect_circle_collide(e.rect, m.x, m.y, m.radius):
                    energy_gained = e.take_damage(50)
                    player.add_energy(energy_gained)
                    if m in missiles:
                        missiles.remove(m)
                    break

        # Actualizar enemigos
        for e in enemies:
            e.update(dt)

        # Verificar si el tutorial está completado
        if player.bullets_shot >= 10 and len(missiles) >= 3 and not tutorial_completed:
            tutorial_completed = True

    # --- Dibujado ---
    screen.blit(fondo_img, (0, 0))

    # Dibujar enemigos
    for e in enemies:
        e.draw(screen)

    # Dibujar balas y misiles
    for b in player_bullets:
        b.draw(screen)
    for m in missiles:
        m.draw(screen)

    # Dibujar jugador
    player.draw(screen)

    # UI de energía
    energy_ui.draw(screen, player)

    # Instrucciones mejoradas
    if practice_started and not exit_confirmation.active:
        instructions = [
            "DISPARA (X) para ganar energía",
            "LANZA MISILES (Z) cuando tengas 100 de energía", 
            "Presiona ENTER cuando quieras ir al Nivel 5"
        ]
        
        # Fondo semitransparente para instrucciones
        instructions_bg = pygame.Rect(10, HEIGHT - 110, 400, 100)
        instructions_surf = pygame.Surface((400, 100), pygame.SRCALPHA)
        instructions_surf.fill((0, 0, 0, 128))
        screen.blit(instructions_surf, instructions_bg)
        pygame.draw.rect(screen, (100, 100, 200), instructions_bg, 2, border_radius=5)
        
        for i, instruction in enumerate(instructions):
            color = NEON_GREEN if i == 0 else YELLOW if i == 1 else WHITE
            text = font.render(instruction, True, color)
            screen.blit(text, (20, HEIGHT - 100 + i * 25))

    # Estadísticas del tutorial con mejor diseño
    if tutorial_completed and not exit_confirmation.active:
        stats_bg = pygame.Rect(WIDTH//2 - 150, HEIGHT - 50, 300, 40)
        stats_surf = pygame.Surface((300, 40), pygame.SRCALPHA)
        stats_surf.fill((0, 0, 0, 150))
        screen.blit(stats_surf, stats_bg)
        pygame.draw.rect(screen, GREEN, stats_bg, 2, border_radius=5)
        
        stats_text = font.render(f"Balas: {player.bullets_shot} | Misiles: {len(missiles)} | Energía: {player.energy}", True, YELLOW)
        screen.blit(stats_text, (WIDTH//2 - stats_text.get_width()//2, HEIGHT - 40))

    # Dibujar confirmación de salida
    exit_confirmation.draw(screen)

    pygame.display.flip()

pygame.quit()