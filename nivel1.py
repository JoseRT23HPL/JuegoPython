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
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
PURPLE = (180, 80, 220)
CYAN = (0, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nivel 1 - Luchando con Robots")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 36)
title_font = pygame.font.SysFont("Arial", 48)
dialogue_font = pygame.font.SysFont("Arial", 28)

# --- Recursos ---
fondo_img = pygame.image.load("img/ciudad2.png").convert()
fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))

nave_img_original = pygame.image.load("img/nave.png").convert_alpha()
boss_img = pygame.image.load("img/robot.png").convert_alpha()
boss_img = pygame.transform.scale(boss_img, (180, 220))

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
    robot_img = pygame.image.load("img/robot.png").convert_alpha()
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
pygame.mixer.music.load("sound/f2.mp3")   
pygame.mixer.music.set_volume(0.4)

sonido_inicio = pygame.mixer.Sound("sound/inicio1.mp3")   
sonido_derrota = pygame.mixer.Sound("sound/kn.mp3")       
sonido_daño = pygame.mixer.Sound("sound/hit.mp3")        
sonido_coin = pygame.mixer.Sound("sound/coin.mp3")       
sonido_victoria = pygame.mixer.Sound("sound/victoria.mp3")
sonido_texto = pygame.mixer.Sound("sound/text.mp3")
sonido_iman = pygame.mixer.Sound("sound/terremoto.mp3")

# Nueva música de victoria
victory_music = "sound/vic.mp3"
intro_music = "sound/vic.mp3"

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
        "text": "Detectando intruso... ¿Otra vez tú? No aprendes, humano.",
        "position": "right"
    },
    {
        "speaker": "player",
        "text": "No vine a hablar contigo. Solo quiero recuperar lo que robaste.",
        "position": "left"
    },
    {
        "speaker": "robot",
        "text": "Tu amigo eligió el destino equivocado. Ahora pertenece al sistema.",
        "position": "right"
    },
    {
        "speaker": "player",
        "text": "¡Él no es una máquina! No voy a dejar que lo conviertas en una.",
        "position": "left"
    },
    {
        "speaker": "robot",
        "text": "Emociones... una falla en tu programación. Te hacen predecible.",
        "position": "right"
    },
    {
        "speaker": "player",
        "text": "¿Falla? No. Son lo único que me mantiene en pie.",
        "position": "left"
    },
    {
        "speaker": "robot",
        "text": "Entonces caerás de pie. Qué conveniente para mí.",
        "position": "right"
    },
    {
        "speaker": "player",
        "text": "Ya hablaste demasiado, montón de chatarra. Es hora de callarte.",
        "position": "left"
    },
    {
        "speaker": "robot",
        "text": "Procesando amenaza... Resultado: insignificante.",
        "position": "right"
    },
    {
        "speaker": "player",
        "text": "Veremos si sigues pensando eso cuando te derrita el núcleo.",
        "position": "left"
    },
    {
        "speaker": "both",
        "text": "¡INICIANDO PROTOCOLO DE COMBATE!",
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
        
        # Marco decorativo
        pygame.draw.rect(surf, GREY, (20, 20, WIDTH-40, HEIGHT-40), 4, border_radius=10)
        pygame.draw.rect(surf, SILVER, (30, 30, WIDTH-60, HEIGHT-60), 2, border_radius=8)
        
        current_dialogue = self.dialogues[self.current_dialogue]
        
        # Dibujar personajes según quién habla
        if current_dialogue["speaker"] == "robot" or current_dialogue["speaker"] == "both":
            if has_robot_img:
                char_x = WIDTH - 350
                char_y = HEIGHT//2 - 150
                robot_colored = robot_img.copy()
                robot_colored.fill(RED, special_flags=pygame.BLEND_RGBA_MULT)
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
        pygame.draw.rect(surf, SILVER, dialog_rect, 3, border_radius=15)
        
        # Nombre del personaje
        speaker_names = {
            "robot": "ROBOT ENEMIGO",
            "player": "TU NAVE",
            "both": "ENFRENTAMIENTO"
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
        
        title_surface = title_font.render("NIVEL 1", True, SILVER)
        title_surface.set_alpha(self.alpha)
        surf.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, HEIGHT//2 - 100))
        
        subtitle_surface = dialogue_font.render("Luchando con Robots", True, RED)
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

# --- Efecto de Iman Mejorado ---
class ImanEffect:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.duration = 8.0
        self.strength = 150  # Reducida la fuerza para que no sea tan fuerte
        self.particles = []
        self.sound_played = False
        self.wave_timer = 0

    def activate(self):
        self.active = True
        self.timer = 0
        self.wave_timer = 0
        self.particles = []
        self.sound_played = False
        sonido_iman.play()

    def update(self, dt):
        if not self.active:
            return False
            
        self.timer += dt
        self.wave_timer += dt
        
        # Generar partículas de efecto magnético
        if random.random() < 0.4:
            self.particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.randint(3, 8),
                'life': 1.0,
                'speed': random.uniform(50, 150),
                'color': random.choice([BLUE, CYAN, (100, 100, 255)])
            })
        
        for particle in self.particles[:]:
            particle['life'] -= dt * 1.5
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
        if self.timer >= self.duration:
            self.active = False
            return True
        return False

    def draw(self, surf):
        if not self.active:
            return
            
        # Dibujar campo magnético (efecto visual mejorado)
        magnetic_field = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Efecto de ondas concéntricas
        wave_radius = int(self.wave_timer * 100) % 400
        wave_alpha = max(0, 100 - abs(wave_radius - 200) // 2)
        pygame.draw.circle(magnetic_field, (100, 100, 255, wave_alpha), 
                         (WIDTH, HEIGHT//2), wave_radius, 3)
        
        # Partículas
        for particle in self.particles:
            alpha = int(particle['life'] * 200)
            color = (*particle['color'], alpha)
            pygame.draw.circle(magnetic_field, color, 
                             (int(particle['x']), int(particle['y'])), 
                             int(particle['size']))
        
        # Líneas de fuerza magnética
        for i in range(10):
            y = i * (HEIGHT // 10)
            start_x = WIDTH - 100
            end_x = WIDTH - 200 - math.sin(self.wave_timer * 5 + i) * 50
            pygame.draw.line(magnetic_field, (100, 150, 255, 150), 
                           (start_x, y), (end_x, y), 2)
        
        surf.blit(magnetic_field, (0, 0))
        
        # Texto de advertencia con efecto de parpadeo
        if int(self.timer * 3) % 2 == 0:
            warning_font = pygame.font.SysFont("Arial", 36)
            warning_text = warning_font.render("¡CAMPO MAGNÉTICO ACTIVADO!", True, CYAN)
            warning_rect = warning_text.get_rect(center=(WIDTH//2, 50))
            surf.blit(warning_text, warning_rect)

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
            return "A+", GOLD, "¡PERFECTO! Eres una leyenda del espacio"
        elif score >= 85:
            return "A", GREEN, "¡Excelente! Dominas el combate espacial"
        elif score >= 75:
            return "B", BLUE, "¡Buen trabajo! Eres un piloto habilidoso"
        elif score >= 60:
            return "C", YELLOW, "¡Bien hecho! Puedes mejorar aún más"
        else:
            return "D", ORANGE, "¡Sigue practicando! La galaxia te necesita"
            
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
        title_text = title_font.render("¡VICTORIA!", True, GOLD)
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

    def update(self, dt, keys, iman_active=False, iman_strength=0):
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

        # Aplicar efecto de imán si está activo - MEJORADO
        if iman_active:
            # Fuerza que atrae hacia la derecha (hacia el jefe)
            # Pero permitiendo que el jugador pueda contrarrestarla
            iman_force = iman_strength * dt
            
            # Solo aplicar si el jugador no está presionando fuertemente en dirección contraria
            if not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                vx += iman_force
            else:
                # Reducir la fuerza del imán si el jugador está luchando contra él
                vx += iman_force * 0.3

        self.x += vx * speed
        self.y += vy * speed
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))
        self.rect = Rect(int(self.x), int(self.y), self.size, self.size)

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

class MetalObstacle:
    def __init__(self, phase=1):
        self.w = random.randint(20, 40)
        self.h = random.randint(20, 40)
        self.x = -random.randint(20, 120)  # Aparecen por la izquierda
        self.y = random.randint(50, HEIGHT-100)
        base_speed = random.randint(200, 300)
        if phase == 3:
            base_speed = random.randint(300, 400)
        self.speed = base_speed
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.color = (150, 150, 200)  # Color metálico

    def update(self, dt, iman_active=False, iman_strength=0):
        # Los obstáculos se mueven hacia la derecha (atraídos por el imán)
        if iman_active:
            self.x += (self.speed + iman_strength) * dt
        else:
            self.x += self.speed * dt
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=5)
        # Efecto metálico
        highlight = pygame.Rect(self.x + 2, self.y + 2, self.w//3, self.h//3)
        pygame.draw.rect(surf, (200, 200, 255), highlight, border_radius=2)

class Boss:
    def __init__(self):
        self.w = 180
        self.h = 220
        self.x = WIDTH + 200
        self.y = (HEIGHT - self.h) // 2
        self.max_hp = 5000
        self.hp = self.max_hp
        self.phase = 1
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.timer = 0.0
        self.attack_cooldown = 1.2
        self.attack_timer = 1.0
        self.dir = 1
        self.move_timer = 0.0
        self.move_cooldown = 0.8
        self.entering = True
        self.exiting = False
        self.iman_timer = 0.0
        self.iman_cooldown = 15.0  # Cada 15 segundos activa el imán
        self.iman_active = False

    def update(self, dt, bullets, player, enemy_bullets, obstacles, fight_started, iman_effect):
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

        # Sistema de imán en fase 3
        if self.phase == 3 and fight_started:
            self.iman_timer += dt
            if self.iman_timer >= self.iman_cooldown and not self.iman_active:
                self.iman_active = True
                iman_effect.activate()
                self.iman_timer = 0
            
            if self.iman_active and iman_effect.timer >= iman_effect.duration:
                self.iman_active = False

        self.move_timer -= dt
        if self.move_timer <= 0:
            self.move_timer = self.move_cooldown
            self.y += 30 * self.dir
            if self.y < 10 or self.y + self.h > HEIGHT - 10:
                self.dir *= -1
                self.y += 30 * self.dir
        self.rect.topleft = (int(self.x), int(self.y))

        if not fight_started:
            return

        self.attack_timer -= dt
        if self.attack_timer <= 0:
            self.attack_timer = self.attack_cooldown
            if self.phase == 1:
                self.attack_cooldown = 1.2
                self.phase_attack_easy(enemy_bullets)
            elif self.phase == 2:
                self.attack_cooldown = 0.9
                self.phase_attack_medium(enemy_bullets, player)
                if random.random() < 0.25:
                    obstacles.append(MetalObstacle(self.phase))
            elif self.phase == 3:
                self.attack_cooldown = 0.6
                self.phase_attack_hard(enemy_bullets, player)
                # En fase 3, generar obstáculos metálicos más frecuentemente
                if random.random() < 0.4 or self.iman_active:
                    obstacles.append(MetalObstacle(self.phase))

    def phase_attack_easy(self, enemy_bullets):
        cx = self.x
        cy = self.y + self.h * 0.5
        for angle_deg in (-20, 0, 20):
            rad = math.radians(angle_deg)
            vx = -300 * math.cos(rad)
            vy = 300 * math.sin(rad)
            enemy_bullets.append(Bullet(cx, cy, vx, vy, color=RED, owner="boss"))

    def phase_attack_medium(self, enemy_bullets, player):
        cx = self.x
        cy = self.y + self.h * 0.5
        for angle in range(-40, 41, 20):
            rad = math.radians(angle)
            vx = -320 * math.cos(rad)
            vy = 320 * math.sin(rad)
            enemy_bullets.append(Bullet(cx, cy, vx, vy, color=RED, owner="boss"))

        dx = player.x + player.size/2 - cx
        dy = player.y + player.size/2 - cy
        dist = math.hypot(dx,dy) or 1
        speed = 370
        enemy_bullets.append(Bullet(cx, cy, speed * dx/dist * -1, speed * dy/dist * -1, color=RED, owner="boss"))

    def phase_attack_hard(self, enemy_bullets, player):
        cx = self.x
        cy = self.y + self.h * 0.5
        num = 7
        base_angle = random.uniform(0, math.pi*2)
        for i in range(num):
            ang = base_angle + (i/num) * math.pi
            vx = -420 * math.cos(ang)
            vy = 420 * math.sin(ang)
            enemy_bullets.append(Bullet(cx, cy, vx, vy, color=RED, owner="boss"))

    def draw(self, surf):
        if self.hp > 0:
            surf.blit(boss_img, (self.x, self.y))
        bar_w = 200
        bar_h = 18
        bar_x = WIDTH - bar_w - 20
        bar_y = 12
        pygame.draw.rect(surf, (80,80,80), (bar_x, bar_y, bar_w, bar_h))
        hp_fraction = max(0, self.hp / self.max_hp)
        pygame.draw.rect(surf, (200,40,40), (bar_x, bar_y, int(bar_w*hp_fraction), bar_h))
        hp_text = font.render(f"Jefe HP: {self.hp}/{self.max_hp}  Fase: {self.phase}", True, WHITE)
        surf.blit(hp_text, (bar_x, bar_y + bar_h + 2))

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
        pygame.mixer.music.load("sound/f2.mp3")
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
iman_effect = ImanEffect()
knockout_effect = KnockoutEffect()
results_system = ResultsSystem()

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
                    obstacles.clear()
                    player.x = 80
                    player.y = HEIGHT // 2
            if event.key == pygame.K_RETURN and results_system.active and results_system.animation_timer >= results_system.animation_duration:
                running = False
                pygame.quit()
                try:
                    subprocess.run([sys.executable, "nivel2.py"])
                except:
                    print("No se pudo cargar el siguiente nivel")
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

    # Actualizar conteo regresivo
    if continue_countdown > 0:
        continue_countdown -= dt
        if continue_countdown <= 0:
            continue_countdown = 0
            game_over = True

    if not game_over and not level_cleared and continue_countdown == 0 and not results_system.active:
        fight_timer += dt
        
        # Actualizar efectos
        iman_effect.update(dt)
        
        # Actualizar jugador con efecto de imán si está activo
        player.update(dt, keys, boss.iman_active, iman_effect.strength)

        if fight_started and keys[pygame.K_x] and player.can_shoot():
            bx = player.x + player.size + 6
            by = player.y + player.size/2
            bullet = Bullet(bx, by, 600, 0, color=GREEN, owner="player")
            player_bullets.append(bullet)
            player.shoot()

        boss.update(dt, player_bullets, player, enemy_bullets, obstacles, fight_started, iman_effect)

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
                if boss.hp <= 0 and not boss_defeated_sound_played:
                    boss_defeated_sound_played = True
                    knockout_effect.activate()

        for b in enemy_bullets[:]:
            b.update(dt)
            if b.x < -50 or b.y < -50 or b.y > HEIGHT+50:
                enemy_bullets.remove(b)
                continue
            if rect_circle_collide(player.rect, b.x, b.y, b.radius):
                player.take_damage()
                if b in enemy_bullets:
                    enemy_bullets.remove(b)

        for obs in obstacles[:]:
            obs.update(dt, boss.iman_active, iman_effect.strength)
            if obs.x > WIDTH + 100:
                obstacles.remove(obs)
                continue
            if player.rect.colliderect(obs.rect):
                player.take_damage()
                obstacles.remove(obs)

        # Colisión con el jefe cuando el imán está activo
        if player.rect.colliderect(boss.rect) and not boss.entering and boss.iman_active:
            player.take_damage()
            # Empujar al jugador lejos del jefe
            player.x = max(0, player.x - 100)

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
    screen.blit(fondo_img, (int(scroll_x), 0))
    screen.blit(fondo_img, (int(scroll_x)+WIDTH, 0))

    for b in player_bullets:
        b.draw(screen)
    for b in enemy_bullets:
        b.draw(screen)
    for obs in obstacles:
        obs.draw(screen)

    boss.draw(screen)
    
    # Dibujar efecto de imán
    iman_effect.draw(screen)
    
    # Dibujar efecto de knockout
    knockout_effect.draw(screen)
    
    if continue_countdown == 0 and not results_system.active:
        player.draw(screen)

    lives_text = font.render(f"Vidas: {player.lives}", True, WHITE)
    screen.blit(lives_text, (12, 12))
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (12, 36))

    if not fight_started and not introduction.active:
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