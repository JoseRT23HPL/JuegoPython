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
DARK_BLUE = (20, 30, 60)
LIGHT_YELLOW = (255, 255, 150)
PURPLE = (180, 80, 220)
CYAN = (80, 220, 220)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Un Héroe Más - 2 Minutos de Supervivencia")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 32)
dialogue_font = pygame.font.SysFont("Arial", 22)

# --- Cargar Recursos ---
fondo_img = pygame.image.load("img/museo.png").convert()
fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))

nave_img_original = pygame.image.load("img/nave.png").convert_alpha()
enemy_img = pygame.image.load("img/fantasma.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 40))
jar_img = pygame.image.load("img/diosa.png").convert_alpha()
jar_img = pygame.transform.scale(jar_img, (60, 80))

# Cargar imagen para el nuevo enemigo de sombra
try:
    shadow_enemy_img = pygame.image.load("img/fantasma2.png").convert_alpha()
    shadow_enemy_img = pygame.transform.scale(shadow_enemy_img, (50, 50))
    has_shadow_img = True
except:
    print("No se pudo cargar sombra.png, se usará un círculo morado")
    has_shadow_img = False

# Imagen para la pantalla de introducción
girl_img = pygame.image.load("img/Afrodita.png").convert_alpha()
girl_img = pygame.transform.scale(girl_img, (300, 400))

# Cargar imagen para efecto KO
try:
    ok_image = pygame.image.load("img/bravo.png").convert_alpha()
    ok_image = pygame.transform.scale(ok_image, (320, 180))
    has_ok_image = True
except:
    print("No se pudo cargar bravo.png, se usará texto alternativo")
    has_ok_image = False

# Música y sonidos
pygame.mixer.music.load("sound/heroe.mp3")   
pygame.mixer.music.set_volume(0.4)

intro_music = "sound/vic.mp3"

sonido_inicio = pygame.mixer.Sound("sound/inicio1.mp3")   
sonido_daño = pygame.mixer.Sound("sound/hit.mp3")        
sonido_coin = pygame.mixer.Sound("sound/coin2.mp3")     
sonido_energia = pygame.mixer.Sound("sound/energia.mp3")   
sonido_victoria = pygame.mixer.Sound("sound/bravo.mp3") 
sonido_texto = pygame.mixer.Sound("sound/text.mp3")
victory_music = "sound/vic.mp3"

# Cargar sonido de KO
try:
    sonido_knockout = pygame.mixer.Sound("sound/bravo.mp3")
    has_knockout_sound = True
except:
    print("No se pudo carbar el sonido de knockout")
    has_knockout_sound = False

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
            # Fase 4: Mostrar mensaje de continuación
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
                ko_text = ko_font.render("¡NIVEL COMPLETADO!", True, (255, 50, 50))
                ko_rect = ko_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
                effect_surface.blit(ko_text, ko_rect)
        else:
            # Dibujar mensaje de continuación
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            effect_surface.blit(overlay, (0, 0))
            
            victory_font = pygame.font.SysFont("Arial", 48)
            victory_text = victory_font.render("¡VICTORIA!", True, GOLD)
            effect_surface.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, HEIGHT//2 - 100))
            
            continue_font = pygame.font.SysFont("Arial", 24)
            continue_text = continue_font.render("Presiona ESPACIO para continuar", True, WHITE)
            effect_surface.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 50))
        
        surf.blit(effect_surface, (0, 0))

# --- Sistema de Resultados ---
class ResultsSystem:
    def __init__(self):
        self.active = False
        self.grade = ""
        self.grade_color = WHITE
        self.motivational_phrase = ""
        
    def calculate_grade(self, continues_used, damage_taken, accuracy, completion_time, enemies_defeated):
        score = 100
        
        if continues_used > 0:
            score -= continues_used * 15
            
        if damage_taken > 0:
            score -= min(damage_taken * 2, 20)
            
        if accuracy < 0.5:
            score -= 5
            
        if completion_time > 120:
            score -= 5
            
        if enemies_defeated < 20:
            score -= 5

        if score >= 95:
            return "A+", GOLD, "¡PERFECTO! Eres un verdadero guardián del museo"
        elif score >= 85:
            return "A", GREEN, "¡Excelente! Defensa impecable del jarrón"
        elif score >= 75:
            return "B", BLUE, "¡Buen trabajo! El jarrón está a salvo"
        elif score >= 60:
            return "C", YELLOW, "¡Bien hecho! Misión cumplida"
        else:
            return "D", ORANGE, "¡Logrado! El jarrón sobrevivió"
            
    def show_results(self, player, jar, continues_used, score, completion_time, enemies_defeated):
        self.active = True
        
        accuracy = player.bullets_hit / player.bullets_shot if player.bullets_shot > 0 else 0
        
        self.grade, self.grade_color, self.motivational_phrase = self.calculate_grade(
            continues_used, player.damage_taken, accuracy, completion_time, enemies_defeated
        )
        
        self.player_lives = player.lives
        self.player_max_lives = player.max_lives
        self.jar_hp = jar.hp
        self.jar_max_hp = jar.max_hp
        self.accuracy = accuracy
        self.score = score
        self.continues_used = continues_used
        self.completion_time = completion_time
        self.player_damage_taken = player.damage_taken
        self.player_bullets_hit = player.bullets_hit
        self.player_bullets_shot = player.bullets_shot
        self.enemies_defeated = enemies_defeated
        
    def draw(self, surf):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surf.blit(overlay, (0, 0))
        
        title_text = title_font.render("RESULTADOS - UN HÉROE MÁS", True, GOLD)
        surf.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 40))
        
        grade_text = large_font.render(f"Calificación: {self.grade}", True, self.grade_color)
        surf.blit(grade_text, (WIDTH//2 - grade_text.get_width()//2, 100))
        
        stats_y = 160
        stats = [
            f"Tiempo completado: {self.completion_time:.1f} segundos",
            f"Puntuación final: {self.score} puntos",
            f"Continues usados: {self.continues_used}",
            f"Daño recibido: {self.player_damage_taken} veces",
            f"Precisión: {self.accuracy*100:.1f}% ({self.player_bullets_hit}/{self.player_bullets_shot})",
            f"Vidas restantes: {self.player_lives}/{self.player_max_lives}",
            f"Vida del jarrón: {self.jar_hp}/{self.jar_max_hp}",
            f"Enemigos derrotados: {self.enemies_defeated}",
            f"Rayos de energía recolectados: {self.score // 20}"  # Estimado basado en puntos
        ]
        
        for stat in stats:
            stat_text = font.render(stat, True, WHITE)
            surf.blit(stat_text, (WIDTH//2 - stat_text.get_width()//2, stats_y))
            stats_y += 35
        
        phrase_text = font.render(self.motivational_phrase, True, GREEN)
        surf.blit(phrase_text, (WIDTH//2 - phrase_text.get_width()//2, stats_y + 20))
        
        reward_text = font.render("¡Has demostrado ser un verdadero héroe!", True, YELLOW)
        surf.blit(reward_text, (WIDTH//2 - reward_text.get_width()//2, stats_y + 60))
        
        instruction_text = font.render("Presiona ENTER para continuar", True, WHITE)
        surf.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 60))

# --- Vista de Presentación ---
class TitleScreen:
    def __init__(self):
        self.active = True
        self.timer = 0
        self.display_time = 3.0
        self.fade_in_time = 1.0
        self.fade_out_time = 1.0
        self.phase = "fade_in"
        
    def update(self, dt):
        self.timer += dt
        
        if self.phase == "fade_in" and self.timer >= self.fade_in_time:
            self.phase = "display"
            self.timer = 0
        elif self.phase == "display" and self.timer >= self.display_time:
            self.phase = "fade_out"
            self.timer = 0
        elif self.phase == "fade_out" and self.timer >= self.fade_out_time:
            self.active = False
            return True
        return False
            
    def get_alpha(self):
        if self.phase == "fade_in":
            return int(255 * (self.timer / self.fade_in_time))
        elif self.phase == "display":
            return 255
        elif self.phase == "fade_out":
            return int(255 * (1 - (self.timer / self.fade_out_time)))
        return 0
            
    def draw(self, surf):
        surf.fill(BLACK)
        
        title_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        main_title = title_font.render("UN HÉROE MÁS", True, GOLD)
        title_rect = main_title.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
        
        subtitle = large_font.render("2 Minutos de Supervivencia", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
        
        pygame.draw.rect(title_surface, GOLD, 
                        (title_rect.x - 20, title_rect.y - 15, 
                         title_rect.width + 40, title_rect.height + subtitle_rect.height + 50), 
                        3, border_radius=10)
        
        alpha = self.get_alpha()
        title_surface.set_alpha(alpha)
        
        title_surface.blit(main_title, title_rect)
        title_surface.blit(subtitle, subtitle_rect)
        
        surf.blit(title_surface, (0, 0))

# --- Sistema de Fondo con Scroll ---
class ScrollingBackground:
    def __init__(self):
        self.scroll_speed = 30
        self.offset = 0
        
    def update(self, dt):
        self.offset = (self.offset + self.scroll_speed * dt) % WIDTH
        
    def draw(self, surf):
        # Dibujar el fondo dos veces para efecto de scroll continuo
        surf.blit(fondo_img, (-self.offset, 0))
        surf.blit(fondo_img, (-self.offset + WIDTH, 0))

# --- Sistema de Iluminación (MODIFICADO: 10 segundos de duración) ---
class LightingSystem:
    def __init__(self):
        self.base_brightness = 1.0
        self.current_brightness = 1.0
        self.min_brightness = 0.3
        self.darken_speed = 0.07  # Más lento para que dure 10 segundos
        self.light_timer = 0
        self.light_duration = 10.0  # 10 segundos de duración
        self.has_light = True
        
    def update(self, dt):
        if self.has_light:
            self.light_timer -= dt
            if self.light_timer <= 0:
                self.has_light = False
        
        if not self.has_light:
            self.current_brightness = max(self.min_brightness, 
                                        self.current_brightness - self.darken_speed * dt)
        else:
            self.current_brightness = min(1.0, 
                                        self.current_brightness + self.darken_speed * dt)
    
    def add_light(self):
        self.has_light = True
        self.light_timer = self.light_duration
        sonido_energia.play()
    
    def draw_lighting(self, surf):
        # Crear superficie de oscurecimiento
        dark_surface = pygame.Surface((WIDTH, HEIGHT))
        dark_surface.fill(BLACK)
        alpha = int(255 * (1 - self.current_brightness))
        dark_surface.set_alpha(alpha)
        surf.blit(dark_surface, (0, 0))
        
        # Dibujar barra de luz
        bar_w = 200
        bar_h = 12
        bar_x = WIDTH - bar_w - 20
        bar_y = 20
        
        pygame.draw.rect(surf, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h))
        if self.has_light:
            time_ratio = self.light_timer / self.light_duration
            light_width = int(bar_w * time_ratio)
            pygame.draw.rect(surf, LIGHT_YELLOW, (bar_x, bar_y, light_width, bar_h))
        
        light_text = font.render("LUZ", True, LIGHT_YELLOW if self.has_light else GREY)
        surf.blit(light_text, (bar_x - 40, bar_y - 2))

# --- Rayos de Energía (AUMENTADA PROBABILIDAD) ---
class EnergyRay:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.pulse_timer = 0
        self.collected = False
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                               self.radius * 2, self.radius * 2)
        self.lifetime = 8.0  # Los rayos desaparecen después de 8 segundos
        self.age = 0
        
    def update(self, dt):
        self.pulse_timer += dt
        self.age += dt
        # Efecto de pulsación
        self.radius = 15 + math.sin(self.pulse_timer * 5) * 3
        
    def is_expired(self):
        return self.age >= self.lifetime
        
    def draw(self, surf):
        if not self.collected:
            # Efecto de parpadeo cuando está por desaparecer
            alpha_mod = 1.0
            if self.age > 6.0:  # Últimos 2 segundos parpadea
                alpha_mod = (math.sin(self.pulse_timer * 10) + 1) / 2
                
            # Dibujar rayo de energía
            pulse_alpha = int((150 + math.sin(self.pulse_timer * 8) * 100) * alpha_mod)
            ray_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(ray_surface, (255, 255, 100, pulse_alpha), 
                             (self.radius, self.radius), self.radius)
            surf.blit(ray_surface, (self.x - self.radius, self.y - self.radius))
            
            # Efecto de destello
            flash_radius = self.radius + math.sin(self.pulse_timer * 10) * 5
            pygame.draw.circle(surf, YELLOW, (int(self.x), int(self.y)), 
                             int(flash_radius), 1)

# --- Jarrón Móvil (más a la izquierda y se esconde) ---
class MovingJar:
    def __init__(self):
        # Comienza más a la izquierda
        self.x = 100
        self.y = HEIGHT // 2 - 40
        self.w = 60
        self.h = 80
        self.max_hp = 400
        self.hp = self.max_hp
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.speed = 45
        self.move_timer = 0
        self.scared_timer = 0
        self.is_scared = False
        self.float_timer = 0
        self.hiding_timer = 0
        self.is_hiding = False
        self.base_x = 100  # Posición base más a la izquierda
        self.base_y = HEIGHT // 2 - 40
        
    def update(self, dt):
        self.float_timer += dt
        
        # Movimiento de flotación suave
        float_offset = math.sin(self.float_timer * 2) * 3
        
        if self.is_hiding:
            self.hiding_timer -= dt
            # Moverse hacia atrás (más a la izquierda) cuando se esconde
            target_x = max(50, self.base_x - 30)
            dx = target_x - self.x
            self.x += dx * 0.1
            
            if self.hiding_timer <= 0:
                self.is_hiding = False
                
        elif self.is_scared:
            self.scared_timer -= dt
            # Movimiento errático cuando está asustado
            self.x += random.randint(-40, 10) * dt  # Tiende a moverse a la izquierda
            self.y += random.randint(-30, 30) * dt
            
            if self.scared_timer <= 0:
                self.is_scared = False
                # Después de asustarse, se esconde por un tiempo
                self.is_hiding = True
                self.hiding_timer = 2.0
        else:
            # Movimiento normal por la pantalla
            self.move_timer += dt
            
            # Patrón de movimiento más amplio por toda la pantalla
            if self.move_timer > 3.0:  # Cambiar dirección cada 3 segundos
                self.move_timer = 0
            
            # Moverse por diferentes áreas de la pantalla
            time_factor = self.float_timer * 0.3
            area_width = WIDTH - 200  # Área disponible para moverse
            target_x = 100 + (math.sin(time_factor) + 1) * 0.5 * area_width * 0.6
            target_y = 100 + (math.cos(time_factor * 0.7) + 1) * 0.5 * (HEIGHT - 250)
            
            # Movimiento suave hacia la posición objetivo
            dx = target_x - self.x
            dy = target_y - self.y
            dist = max(0.1, math.hypot(dx, dy))
            
            move_speed = min(self.speed * dt, dist)
            self.x += (dx / dist) * move_speed
            self.y += (dy / dist) * move_speed + float_offset
        
        # Limitar movimiento dentro de la pantalla (permitiendo más a la izquierda)
        self.x = max(50, min(WIDTH - 160, self.x))
        self.y = max(80, min(HEIGHT - 180, self.y))
        
        self.rect.topleft = (int(self.x), int(self.y))
    
    def take_damage(self):
        self.hp -= 20
        self.is_scared = True
        self.scared_timer = 1.5
        sonido_daño.play()
        
        # Cuando le pegan, se esconde inmediatamente hacia atrás
        self.is_hiding = True
        self.hiding_timer = 3.0
    
    def draw(self, surf):
        # Dibujar jarrón con efecto de flotación
        surf.blit(jar_img, (self.x, self.y))
        
        # Barra de vida
        bar_w = 80
        bar_h = 6
        bar_x = self.x - 10
        bar_y = self.y - 15
        
        pygame.draw.rect(surf, (80, 80, 80), (bar_x, bar_y, bar_w, bar_h))
        hp_ratio = max(0, self.hp / self.max_hp)
        bar_color = GREEN if hp_ratio > 0.5 else YELLOW if hp_ratio > 0.2 else RED
        pygame.draw.rect(surf, bar_color, (bar_x, bar_y, int(bar_w * hp_ratio), bar_h))
        
        # Indicador visual cuando se está escondiendo
        if self.is_hiding:
            hide_text = font.render("¡Escondiéndose!", True, BLUE)
            surf.blit(hide_text, (self.x - 25, self.y - 35))

# --- Barra de Progreso del Tiempo ---
class ProgressBar:
    def __init__(self, total_time=120):
        self.total_time = total_time
        self.width = WIDTH - 100
        self.height = 20
        self.x = 50
        self.y = HEIGHT - 40
        self.color = BLUE
        self.bg_color = (50, 50, 50)
        
    def draw(self, surf, elapsed_time):
        # Fondo de la barra
        pygame.draw.rect(surf, self.bg_color, (self.x, self.y, self.width, self.height))
        
        # Progreso actual
        progress = min(1.0, elapsed_time / self.total_time)
        progress_width = int(self.width * progress)
        
        # Cambiar color según el progreso
        if progress < 0.3:
            color = GREEN
        elif progress < 0.7:
            color = YELLOW
        else:
            color = RED
            
        pygame.draw.rect(surf, color, (self.x, self.y, progress_width, self.height))
        
        # Borde
        pygame.draw.rect(surf, WHITE, (self.x, self.y, self.width, self.height), 2)
        
        # Texto del tiempo
        time_left = max(0, self.total_time - elapsed_time)
        time_text = font.render(f"{int(time_left)}s", True, WHITE)
        surf.blit(time_text, (self.x + self.width + 10, self.y))

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
        return self.active and (not self.is_shrunk) and self.shoot_timer <= 0

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

    def activate(self):
        self.active = True

# --- Balas ---
class Bullet:
    def __init__(self, x, y, vx, vy, color=YELLOW, owner="player"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 6 if owner == "player" else 8
        self.color = color
        self.owner = owner
        self.rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), 
                               self.radius * 2, self.radius * 2)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)

# --- Enemigo de Sombra (NUEVO) ---
class ShadowEnemy:
    def __init__(self, jar, elapsed_time):
        self.w = 50
        self.h = 50
        # Aparece desde la derecha
        self.x = WIDTH + 50
        self.y = random.randint(50, HEIGHT - 50)
        self.active = False
        
        time_factor = min(2.0, 1.0 + (elapsed_time / 120))
        
        self.hp = int(60 * time_factor)  # Más vida que los enemigos normales
        self.speed = int(40 * time_factor)  # Más lento que los enemigos normales
        self.enemy_type = "shadow"
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color = PURPLE
        self.jar = jar
        self.has_energy = random.random() < 0.15  # 15% de chance de soltar energía
        self.pulse_timer = 0
        self.alpha = 255

    def update(self, dt, lighting_system):
        if not self.active:
            return
            
        self.pulse_timer += dt
        
        # Solo se actualiza si no hay luz
        if lighting_system.has_light:
            # Si hay luz, desaparece gradualmente
            self.alpha = max(0, self.alpha - 200 * dt)
            if self.alpha <= 0:
                self.active = False
                return
        else:
            # Si no hay luz, aparece gradualmente
            self.alpha = min(255, self.alpha + 200 * dt)
            
            # Perseguir el jarrón
            dx = self.jar.x - self.x
            dy = self.jar.y - self.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx /= dist
                dy /= dist

            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt
            self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        if self.alpha > 0:
            if has_shadow_img:
                # Usar imagen con efecto de transparencia
                shadow_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
                shadow_surface.fill((0, 0, 0, 0))
                shadow_surface.blit(shadow_enemy_img, (0, 0))
                shadow_surface.set_alpha(self.alpha)
                surf.blit(shadow_surface, (self.x, self.y))
            else:
                # Dibujar círculo morado como fallback
                shadow_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
                pygame.draw.circle(shadow_surface, (*PURPLE, self.alpha), 
                                 (self.w//2, self.h//2), self.w//2)
                surf.blit(shadow_surface, (self.x, self.y))
                
                # Efecto de pulsación
                pulse_radius = self.w//2 + math.sin(self.pulse_timer * 5) * 3
                pulse_surface = pygame.Surface((int(pulse_radius*2), int(pulse_radius*2)), pygame.SRCALPHA)
                pygame.draw.circle(pulse_surface, (*PURPLE, self.alpha//2), 
                                 (int(pulse_radius), int(pulse_radius)), int(pulse_radius))
                surf.blit(pulse_surface, (self.x + self.w//2 - pulse_radius, self.y + self.h//2 - pulse_radius))

        # Barra de vida
        if self.hp < 60:
            max_hp = 60
            health_width = (self.w * self.hp) // max_hp
            health_rect = Rect(self.x, self.y - 8, health_width, 4)
            health_surface = pygame.Surface((health_width, 4), pygame.SRCALPHA)
            pygame.draw.rect(health_surface, (0, 255, 0, self.alpha), (0, 0, health_width, 4))
            surf.blit(health_surface, (self.x, self.y - 8))

    def activate(self):
        self.active = True

# --- Enemigos (solo aparecen por la derecha) ---
class Enemy:
    def __init__(self, jar, elapsed_time, hp=25, speed=90, enemy_type="basic"):
        self.w = 40
        self.h = 40
        # Aparecen solo por la derecha
        self.x = WIDTH + 40
        self.y = random.randint(50, HEIGHT - 50)
        self.active = False
        
        time_factor = min(2.0, 1.0 + (elapsed_time / 120))
        
        self.hp = int(hp * time_factor)
        self.speed = int(speed * time_factor)
        self.enemy_type = enemy_type
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color = RED
        self.jar = jar
        self.has_energy = random.random() < 0.15  # AUMENTADO: 15% de chance de soltar energía

        if enemy_type == "fast":
            self.speed = int(140 * time_factor)
            self.hp = int(15 * time_factor)
        elif enemy_type == "tank":
            self.speed = int(60 * time_factor)
            self.hp = int(50 * time_factor)
        elif enemy_type == "elite":
            self.speed = int(120 * time_factor)
            self.hp = int(40 * time_factor)

    def update(self, dt):
        if not self.active:
            return
            
        # Perseguir el jarrón
        dx = self.jar.x - self.x
        dy = self.jar.y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist

        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        enemy_scaled = pygame.transform.scale(enemy_img, (self.w, self.h))
        surf.blit(enemy_scaled, (self.x, self.y))
        
        # Barra de vida para enemigos fuertes
        if self.enemy_type in ["tank", "elite"] and self.hp < (50 if self.enemy_type == "tank" else 40):
            max_hp = 50 if self.enemy_type == "tank" else 40
            health_width = (self.w * self.hp) // max_hp
            health_rect = Rect(self.x, self.y - 8, health_width, 4)
            pygame.draw.rect(surf, GREEN, health_rect)

    def activate(self):
        self.active = True

# --- Sistema de Diálogos ---
class DialogueSystem:
    def __init__(self):
        self.dialogue_active = False
        self.current_line = 0
        self.lines = [
            "¡La energía del museo se está agotando!",
            "Debes proteger a la pequeña diosa, llévala a la salida.",
            "Las sombras atacarán desde la derecha, intentando destruir a la diosa.",
            "Recoge los rayos de energía para mantener la luz encendida.",
            "¡Cuidado! Ahora hay enemigos de sombra que solo atacan en la oscuridad.",
            "Los rayos de energía aparecerán en el museo, ¡úsalos sabiamente!",
            "La luz dura 10 segundos pero se va apagando poco a poco.",
            "¡Salva a la diosa y serás un verdadero héroe!",
            "Mantén la pequeña diosa a salvo hasta que salgan del museo..."
        ]
        self.victory_lines = [
            "¡FELICIDADES! ¡Has salvado a la pequeña diosa!",
            "Ella te mira con gratitud y te sonríe, su luz vuelve a brillar entre las estrellas.",
            "Como recompensa por tu valentía, la diosa te otorga un poderoso misil celestial.",
            "Podrás usarlo cuando tu energía alcance los 100 puntos, canalizando el poder divino.",
            "Presiona la tecla 'Z' para liberar su fuerza y arrasar con tus enemigos.",
            "Cada enemigo derrotado aumentará tu energía... ¡usa tu poder con sabiduría!",
            "Tu valor ha restaurado el equilibrio entre la luz y la oscuridad.",
            "El universo ahora reconoce tu nombre como el Guardián de la Diosa Dorada.",
            "Pero este no es el final... es solo el comienzo de tu verdadera leyenda."
        ]

        self.is_victory_dialogue = False
        self.text_speed = 0
        self.current_char = 0
        self.text_timer = 0
        self.music_started = False
        self.sound_played = False

    def set_victory_dialogue(self):
        self.is_victory_dialogue = True
        self.lines = self.victory_lines
        self.current_line = 0
        self.current_char = 0
        self.text_timer = 0
        self.dialogue_active = True
        self.sound_played = False
        self.calculate_text_speed()

    def calculate_text_speed(self):
        if self.current_line < len(self.lines):
            line_length = len(self.lines[self.current_line])
            self.text_speed = line_length / 4.0

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
        self.text_timer += dt
        
        target_chars = int(self.text_timer * self.text_speed)
        
        if target_chars > self.current_char:
            chars_to_add = target_chars - self.current_char
            old_char = self.current_char
            self.current_char = min(self.current_char + chars_to_add, len(self.lines[self.current_line]))
            
            if old_char == 0 and self.current_char > 0 and not self.sound_played:
                sonido_texto.play()
                self.sound_played = True

    def draw(self, surf):
        surf.fill(BLACK)
        
        pygame.draw.rect(surf, BROWN, (20, 20, WIDTH-40, HEIGHT-40), 4, border_radius=10)
        pygame.draw.rect(surf, GOLD, (30, 30, WIDTH-60, HEIGHT-60), 2, border_radius=8)
        
        girl_x = 50
        girl_y = HEIGHT//2 - 200
        surf.blit(girl_img, (girl_x, girl_y))
        
        dialog_rect = pygame.Rect(400, HEIGHT//2 - 150, WIDTH - 450, 300)
        pygame.draw.rect(surf, (30, 30, 50), dialog_rect, border_radius=15)
        pygame.draw.rect(surf, BLUE, dialog_rect, 3, border_radius=15)
        
        if self.is_victory_dialogue:
            title = title_font.render("LEYENDA DEL GUARDIÁN", True, GOLD)
        else:
            title = title_font.render("2 Minutos de Supervivencia", True, GOLD)
        surf.blit(title, (dialog_rect.centerx - title.get_width()//2, dialog_rect.y + 20))
        
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
        
        text_y = dialog_rect.y + 70
        for line in lines:
            if line.strip():
                line_surface = dialogue_font.render(line, True, WHITE)
                surf.blit(line_surface, (dialog_rect.x + 20, text_y))
                text_y += 35
        
        if self.current_char >= len(self.lines[self.current_line]):
            if self.is_victory_dialogue:
                prompt_text = "Presiona X para continuar" if self.current_line < len(self.lines) - 1 else "Presiona X para ver resultados"
            else:
                prompt_text = "Presiona X para continuar" if self.current_line < len(self.lines) - 1 else "Presiona X para comenzar"
            prompt = dialogue_font.render(prompt_text, True, GREEN)
            surf.blit(prompt, (dialog_rect.centerx - prompt.get_width()//2, dialog_rect.bottom - 50))
        else:
            if pygame.time.get_ticks() % 600 < 300:
                dots_text = dialogue_font.render("...", True, YELLOW)
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
                if self.is_victory_dialogue:
                    return "results"
                return "start"
            else:
                self.calculate_text_speed()
        return "continue"

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
        pygame.mixer.music.load("sound/heroe.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except:
        print("No se pudo cargar la música normal")

# --- Inicialización del juego ---
player = Player()
jar = MovingJar()
lighting = LightingSystem()
background = ScrollingBackground()
progress_bar = ProgressBar(120)  # 2 minutos
player_bullets = []
enemies = []
shadow_enemies = []  # NUEVO: lista para enemigos de sombra
energy_rays = []
title_screen = TitleScreen()
dialogue = DialogueSystem()
knockout_effect = KnockoutEffect()
results_system = ResultsSystem()

score = 0
game_over = False
level_cleared = False
enemies_defeated = 0
victory_sound_played = False
knockout_shown = False
victory_dialogue_shown = False

continue_countdown = 0
continue_time = 12.0
coins_inserted = 0
continues_used = 0
continue_available = True
lives_per_coin = 3

start_time = pygame.time.get_ticks()
fight_started = False
victory_music_playing = False
countdown_timer = 0
countdown_active = False

# Calcular velocidad inicial para la primera línea
dialogue.calculate_text_speed()

# --- Main loop ---
running = True
while running:
    dt_ms = clock.tick(FPS)
    dt = dt_ms / 1000.0
    elapsed = (pygame.time.get_ticks() - start_time) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_x:
                if title_screen.active:
                    title_screen.active = False
                    dialogue.dialogue_active = True
                elif dialogue.dialogue_active:
                    result = dialogue.advance_text()
                    if result == "start":
                        start_time = pygame.time.get_ticks()
                        play_normal_music()
                        countdown_timer = 5.0
                        countdown_active = True
                        sonido_inicio.play()
                    elif result == "results":
                        results_system.show_results(player, jar, continues_used, score, elapsed, enemies_defeated)
                elif continue_countdown > 0 and continue_available:
                    coins_inserted += 1
                    continues_used += 1
                    sonido_coin.play()
                    player.add_lives(lives_per_coin)
                    if coins_inserted >= 1:
                        continue_countdown = 0
                        player.invulnerable = True
                        player.invulnerable_timer = 3.0
                        if len(enemies) > 3:
                            enemies = enemies[:3]
                        if len(shadow_enemies) > 2:
                            shadow_enemies = shadow_enemies[:2]
                        player.x = 80
                        player.y = HEIGHT // 2
            if event.key == pygame.K_RETURN and results_system.active:
                running = False
                pygame.quit()
                try:
                    subprocess.run([sys.executable, "nivel4.py"])  # Cambia por tu siguiente nivel
                except:
                    print("No se pudo cargar el siguiente nivel")
                sys.exit()
            if event.key == pygame.K_SPACE and knockout_effect.active and knockout_effect.show_stats:
                # Saltar directamente a los diálogos de victoria
                knockout_effect.active = False
                knockout_effect.freeze_game = False
                dialogue.set_victory_dialogue()

    keys = pygame.key.get_pressed()

    # Pantalla de título
    if title_screen.active:
        if title_screen.update(dt):
            title_screen.active = False
            dialogue.dialogue_active = True
        title_screen.draw(screen)
        pygame.display.flip()
        continue

    # Sistema de resultados
    if results_system.active:
        results_system.draw(screen)
        pygame.display.flip()
        continue

    # Sistema de diálogos (incluyendo diálogos de victoria extendidos)
    if dialogue.dialogue_active:
        dialogue.start_intro_music()
        dialogue.update(dt)
        dialogue.draw(screen)
        pygame.display.flip()
        continue

    # Efecto de knockout
    if knockout_effect.active:
        knockout_finished = knockout_effect.update(dt)
        if knockout_finished and not victory_dialogue_shown:
            # Después del knockout, mostrar diálogos de victoria extendidos
            knockout_effect.active = False
            knockout_effect.freeze_game = False
            dialogue.set_victory_dialogue()
            victory_dialogue_shown = True

    # Cuenta regresiva inicial
    if countdown_active:
        countdown_timer -= dt
        if countdown_timer <= 0:
            countdown_active = False
            fight_started = True
            player.activate()
            for enemy in enemies:
                enemy.activate()
            for shadow_enemy in shadow_enemies:
                shadow_enemy.activate()

    # Juego principal
    if not countdown_active and elapsed > 0 and not fight_started:
        fight_started = True
        player.activate()

    # Condición de victoria - 2 minutos completos
    if elapsed >= 120 and not game_over and not level_cleared and not dialogue.dialogue_active and not knockout_shown:
        level_cleared = True
        pygame.mixer.music.stop()
        play_victory_music()
        # Activar efecto knockout en lugar de mostrar resultados directamente
        knockout_effect.activate()
        knockout_shown = True

    if continue_countdown > 0:
        continue_countdown -= dt
        if continue_countdown <= 0:
            continue_countdown = 0
            game_over = True

    # Juego principal (batalla) - CONGELADO durante knockout
    if not game_over and not level_cleared and continue_countdown == 0 and fight_started and not dialogue.dialogue_active and not knockout_effect.freeze_game:
        # Actualizar sistemas
        background.update(dt)
        lighting.update(dt)
        player.update(dt, keys)
        jar.update(dt)

        # Disparar
        if keys[pygame.K_x] and player.can_shoot():
            bx = player.x + player.size + 6
            by = player.y + player.size / 2
            bullet = Bullet(bx, by, 600, 0, color=GREEN, owner="player")
            player_bullets.append(bullet)
            player.shoot()

        # Spawn de enemigos normales (solo por la derecha)
        if fight_started and not countdown_active and elapsed < 120:
            base_spawn_chance = 0.02
            time_factor = min(2.0, 1.0 + (elapsed / 120))
            
            spawn_chance = base_spawn_chance * time_factor
            
            if random.random() < spawn_chance:
                rand = random.random()
                if elapsed < 30:
                    enemy_type = "basic"
                elif elapsed < 60:
                    if rand < 0.6:
                        enemy_type = "basic"
                    elif rand < 0.9:
                        enemy_type = "fast"
                    else:
                        enemy_type = "tank"
                else:
                    if rand < 0.4:
                        enemy_type = "basic"
                    elif rand < 0.7:
                        enemy_type = "fast"
                    elif rand < 0.9:
                        enemy_type = "tank"
                    else:
                        enemy_type = "elite"
                
                new_enemy = Enemy(jar, elapsed, enemy_type=enemy_type)
                if not countdown_active:
                    new_enemy.activate()
                enemies.append(new_enemy)

        # Spawn de enemigos de sombra (NUEVO: solo cuando no hay luz)
        if fight_started and not countdown_active and elapsed < 120 and not lighting.has_light:
            shadow_spawn_chance = 0.015  # Probabilidad de spawn para sombras
            time_factor = min(2.0, 1.0 + (elapsed / 120))
            
            shadow_spawn_chance = shadow_spawn_chance * time_factor
            
            if random.random() < shadow_spawn_chance and len(shadow_enemies) < 3:  # Máximo 3 sombras a la vez
                new_shadow = ShadowEnemy(jar, elapsed)
                if not countdown_active:
                    new_shadow.activate()
                shadow_enemies.append(new_shadow)

        # Spawn de rayos de energía (AUMENTADA PROBABILIDAD: 0.2% por frame)
        if random.random() < 0.002 and len(energy_rays) < 3:  # Aumentado y máximo 3 rayos
            ray_x = random.randint(80, WIDTH - 80)
            ray_y = random.randint(80, HEIGHT - 80)
            energy_rays.append(EnergyRay(ray_x, ray_y))

        # Actualizar balas
        for b in player_bullets[:]:
            b.update(dt)
            if b.x > WIDTH + 50:
                player_bullets.remove(b)
                continue
                
            # Colisión con enemigos normales
            for e in enemies[:]:
                if rect_circle_collide(e.rect, b.x, b.y, b.radius):
                    e.hp -= 25
                    player.bullets_hit += 1
                    if b in player_bullets:
                        player_bullets.remove(b)
                    if e.hp <= 0:
                        # Posiblemente soltar energía al morir
                        if e.has_energy and random.random() < 0.4:  # 40% de los que pueden soltar energía lo harán
                            energy_rays.append(EnergyRay(e.x, e.y))
                        enemies.remove(e)
                        score += 15 if e.enemy_type == "basic" else 25 if e.enemy_type == "fast" else 50 if e.enemy_type == "tank" else 75
                        enemies_defeated += 1
                    break
                    
            # Colisión con enemigos de sombra (NUEVO)
            for se in shadow_enemies[:]:
                if rect_circle_collide(se.rect, b.x, b.y, b.radius) and se.alpha > 100:
                    se.hp -= 25
                    player.bullets_hit += 1
                    if b in player_bullets:
                        player_bullets.remove(b)
                    if se.hp <= 0:
                        # Posiblemente soltar energía al morir
                        if se.has_energy and random.random() < 0.5:  # 50% de chance para sombras
                            energy_rays.append(EnergyRay(se.x, se.y))
                        shadow_enemies.remove(se)
                        score += 60  # Más puntos por derrotar sombras
                        enemies_defeated += 1
                    break

        # Actualizar enemigos normales
        for e in enemies[:]:
            e.update(dt)
            if e.rect.colliderect(player.rect):
                player.take_damage()
                enemies.remove(e)
            if e.rect.colliderect(jar.rect):
                jar.take_damage()
                enemies.remove(e)

        # Actualizar enemigos de sombra (NUEVO)
        for se in shadow_enemies[:]:
            se.update(dt, lighting)
            if not se.active:  # Si se desactivó (por la luz), removerlo
                shadow_enemies.remove(se)
                continue
            if se.rect.colliderect(player.rect) and se.alpha > 100:
                player.take_damage()
                shadow_enemies.remove(se)
            if se.rect.colliderect(jar.rect) and se.alpha > 100:
                jar.take_damage()
                shadow_enemies.remove(se)

        # Actualizar rayos de energía (eliminar los que expiran)
        for ray in energy_rays[:]:
            ray.update(dt)
            if ray.is_expired():
                energy_rays.remove(ray)
            elif ray.rect.colliderect(player.rect) and not ray.collected:
                lighting.add_light()
                ray.collected = True
                energy_rays.remove(ray)
                score += 30  # Muchos más puntos por encontrar energía

        # Condiciones de derrota
        if player.lives <= 0 and continue_available:
            continue_countdown = continue_time
            coins_inserted = 0
        elif jar.hp <= 0:
            game_over = True

    # --- Dibujado ---
    background.draw(screen)
    
    # Dibujar elementos del juego (solo si no está congelado)
    if not knockout_effect.freeze_game:
        for b in player_bullets:
            b.draw(screen)
        for e in enemies:
            e.draw(screen)
        for se in shadow_enemies:  # NUEVO: dibujar enemigos de sombra
            se.draw(screen)
        for ray in energy_rays:
            ray.draw(screen)
            
        jar.draw(screen)
        
        if continue_countdown == 0:
            player.draw(screen)

    # Aplicar sistema de iluminación
    lighting.draw_lighting(screen)
    
    # Dibujar efecto de knockout (encima de todo)
    if knockout_effect.active:
        knockout_effect.draw(screen)

    # UI
    lives_text = font.render(f"Vidas: {player.lives}", True, WHITE)
    screen.blit(lives_text, (12, 12))
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (12, 36))

    # Dibujar barra de progreso del tiempo
    progress_bar.draw(screen, elapsed)

    # Mostrar cuenta regresiva
    if countdown_active:
        countdown_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        countdown_overlay.fill((0, 0, 0, 150))
        screen.blit(countdown_overlay, (0, 0))
        
        countdown_text = title_font.render(f"{int(countdown_timer) + 1}", True, YELLOW)
        screen.blit(countdown_text, (WIDTH//2 - countdown_text.get_width()//2, HEIGHT//2 - 50))
        
        message_text = large_font.render("¡Prepárate para sobrevivir 2 minutos!", True, WHITE)
        screen.blit(message_text, (WIDTH//2 - message_text.get_width()//2, HEIGHT//2 + 20))

    if not fight_started and not dialogue.dialogue_active and not countdown_active:
        wait_txt = font.render("¡Sobrevive 2 minutos protegiendo el Jarrón! Usa X para disparar", True, GREEN)
        screen.blit(wait_txt, (WIDTH // 2 - wait_txt.get_width() // 2, HEIGHT - 80))

    # Pantalla de continuación
    if continue_countdown > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        continue_text = large_font.render("¡HAS MUERTO!", True, RED)
        screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 - 100))
        
        countdown_text = large_font.render(f"Tiempo: {int(continue_countdown)}", True, ORANGE)
        screen.blit(countdown_text, (WIDTH//2 - countdown_text.get_width()//2, HEIGHT//2 - 40))
        
        instruction_text = font.render("Presiona X para insertar moneda y continuar", True, WHITE)
        screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 20))

    # Game Over
    if game_over and continue_countdown == 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        over_surf = large_font.render("GAME OVER - Jarrón Destruido", True, RED)
        screen.blit(over_surf, (WIDTH//2 - over_surf.get_width()//2, HEIGHT//2 - 50))
        
        instruction_text = font.render("Presiona ESC para salir", True, WHITE)
        screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()

pygame.quit()