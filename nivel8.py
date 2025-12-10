import pygame
import sys
import os
import math
import random
import webbrowser
import subprocess

# Inicializar Pygame y mixer para audio
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Créditos - Gracias por Jugar")

# URL de la página web para encuesta
WEBSITE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc_w89Qb-OZgeym4QtEuGU8-k7QGpbW2VGQNWbRMbr6-VlZDw/viewform?usp=dialog"  # Reemplaza con tu enlace real

# Colores
BACKGROUND = (0, 0, 0)  # Fondo negro como solicitaste
TEXT_COLOR = (255, 255, 255)  # Blanco para texto
ACCENT_COLOR = (255, 215, 0)  # Oro para acentos
SECONDARY_ACCENT = (0, 255, 255)  # Cian para efectos
CREDIT_COLOR = (200, 230, 255)  # Azul claro para créditos
FADE_COLOR = (0, 0, 0)  # Negro para fade
SONG_COLOR = (100, 255, 100)  # Verde brillante para canciones
SPECIAL_COLOR = (255, 100, 255)  # Magenta para elementos especiales
WEB_COLOR = (100, 200, 255)  # Azul para enlace web

# Fuentes
title_font = pygame.font.SysFont("Arial", 72, bold=True)
subtitle_font = pygame.font.SysFont("Arial", 42)
text_font = pygame.font.SysFont("Arial", 32)
credit_font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 24)
tiny_font = pygame.font.SysFont("Arial", 20)

# Mensaje de agradecimiento
thank_you_text = "¡GRACIAS POR JUGAR!"
working_text = "El desarrollo del juego continúa con nuevas actualizaciones"

# Lista de créditos expandida (mucho más contenido)
credits = [
    ("PRODUCCIÓN EJECUTIVA", "Enrique Segoviano"),
    ("", ""),
    ("DIRECCIÓN CREATIVA", "Jose Miguel Rodriguez Tinoco"),
    ("DIRECCIÓN DE ARTE", "Gemini"),
    ("DIRECCIÓN TÉCNICA", "Jose Miguel Rodriguez Tinoco"),
    ("", ""),
    ("DISEÑO DE JUEGO", "Maria Fernanda Andrade Herrera "),
    ("DISEÑO DE NIVELES", "Angel Valentin Flores Eduardo"),
    ("DISEÑO DE MECÁNICAS", "Antonio Arellano Morales"),
    ("DISEÑO DE SISTEMAS", "Herctor Agustin Castillo Perez"),
    ("", ""),
]

# Lista de canciones expandida
songs = [
    "1. TEMA PRINCIPAL - 'AVENTURA ÉPICA' - Composición: Compositor",
    "2. MENÚ PRINCIPAL - 'MELODÍA DE INICIO' - Composición: Compositor",
    "3. NIVEL 1 - 'luchando Con Robots' - Composición: Compositor", 
    "4. NIVEL 2 - 'El diablo Bajo A Georgia' - Composición: Compositor",
    "5. NIVEL 3 - 'Holding Out For Hero' - Composición: Compositor",
    "6. NIVEL 4 - 'Tetris remix' - Composición: Compositor",
    "7. NIVEL 5 - 'Waidmannss Heil' - Composición: Compositor",
    "8. BATALLA FINAL - 'Mein Teil' - Composición: Compositor",
    "9. CRÉDITOS - 'Ocea Man' - Composición: Compositor",
    "",
    "EFECTOS DE SONIDO",
    "Diseño de Sonido: Diseñador de Sonido",
    "Grabación de Foley: Técnico de Foley",
    "Mezcla de Audio: Ingeniero de Sonido",
    "Masterización: Ingeniero de Mastering",
]

# Agregar canciones a los créditos
for song in songs:
    credits.append(("", song))

# Más créditos
credits.extend([
    ("", ""),
    ("VOZ Y DOBLAJE", "Director de Doblaje"),
    ("PROTAGONISTA", "Actor/Actriz Principal"),
    ("ANTAGONISTA", "Actor/Actriz de Villano"),
    ("PERSONAJES SECUNDARIOS", "Actores de Reparto"),
    ("NARRACIÓN", "Narrador"),
    ("", ""),
    ("TESTEO Y CALIDAD", "Director de QA"),
    ("TESTERS PRINCIPALES", "Testers Principales"),
    ("TESTERS BETA", "Comunidad Beta"),
    ("CONTROL DE CALIDAD", "Equipo de Calidad"),
    ("", ""),
    ("PRODUCCIÓN", "Productor Ejecutivo"),
    ("GERENCIA DE PROYECTO", "Project Manager"),
    ("COORDINACIÓN", "Coordinador de Proyecto"),
    ("PLANEACIÓN", "Planificador"),
    ("", ""),
    ("MARKETING Y COMUNIDAD", "Director de Marketing"),
    ("COMUNICACIÓN", "Community Manager"),
    ("REDES SOCIALES", "Especialista en Redes"),
    ("TRAILERS Y PROMO", "Editor de Video"),
    ("", ""),
    ("AGRADECIMIENTOS ESPECIALES", ""),
    ("", "Nuestras Familias"),
    ("", "Amigos y Apoyos"),
    ("", "Comunidad de Jugadores"),
    ("", "Patrocinadores"),
    ("", "Colaboradores Externos"),
    ("", ""),
    ("DESARROLLADO CON", "PyGame - Python"),
    ("MOTOR DE JUEGO", "Motor Propietario"),
    ("HERRAMIENTAS", "Blender, GIMP, Audacity"),
    ("", ""),
    ("© 2023-2024 NOMBRE DEL JUEGO™", "Todos los derechos reservados"),
    ("PUBLICADO POR", "Estudio de Desarrollo"),
    ("VERSIÓN", "1.5.2 - 'Edición Especial'"),
    ("FECHA DE LANZAMIENTO", "Diciembre 2023"),
    ("", ""),
    ("DEDICATORIA", ""),
    ("", "Para todos los que creen en los sueños"),
    ("", "y persiguen sus pasiones."),
    ("", "¡Gracias por ser parte de esta aventura!"),
])

# Configuración de la animación de créditos
credit_scroll_speed = 0.7  # Velocidad más lenta para más contenido

# Estados del programa
class GameState:
    def __init__(self):
        self.state = "ENTRADA"
        self.alpha = 0
        self.fade_speed = 3
        self.scroll_y = HEIGHT
        self.final_image_alpha = 0
        self.final_text_alpha = 0
        self.final_delay = 0
        self.particles = []
        self.stars = [Star() for _ in range(150)]  # Más estrellas
        self.time = 0
        self.pulse_value = 0
        self.showing_website_info = False
        self.website_info_timer = 0
        self.website_info_text = ""
        
        # Efectos especiales
        self.glow_particles = []
        self.background_particles = []
        self.init_background_particles()
        
        # Cargar imagen final
        self.load_final_image()
        
        # Cargar música
        self.load_music()
    
    def load_music(self):
        """Cargar música de fondo"""
        try:
            if os.path.exists("sound/creditos.mp3"):
                pygame.mixer.music.load('sound/creditos.mp3')
                pygame.mixer.music.set_volume(0.6)
                print("Música de créditos cargada correctamente")
            elif os.path.exists("creditos.mp3"):
                pygame.mixer.music.load('creditos.mp3')
                pygame.mixer.music.set_volume(0.6)
                print("Música de créditos cargada correctamente (raíz)")
            else:
                print("Advertencia: No se encontró creditos.mp3")
        except Exception as e:
            print(f"No se pudo cargar la música de fondo: {e}")
    
    def init_background_particles(self):
        """Inicializar partículas de fondo"""
        for _ in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 3)
            speed = random.uniform(0.1, 0.5)
            color = random.choice([(100, 100, 255), (255, 100, 100), (100, 255, 100)])
            self.background_particles.append({
                'x': x, 'y': y, 'size': size, 'speed': speed, 'color': color
            })
    
    def load_final_image(self):
        """Cargar o crear imagen final"""
        try:
            if os.path.exists("img/intellisoft.jpg"):
                self.final_image = pygame.image.load("img/intellisoft.jpg").convert_alpha()
                # Escalar manteniendo proporción
                original_width, original_height = self.final_image.get_size()
                scale = min(400/original_width, 300/original_height)
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
                self.final_image = pygame.transform.scale(self.final_image, (new_width, new_height))
            elif os.path.exists("intellisoft.jpg"):
                self.final_image = pygame.image.load("intellisoft.jpg").convert_alpha()
                original_width, original_height = self.final_image.get_size()
                scale = min(400/original_width, 300/original_height)
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
                self.final_image = pygame.transform.scale(self.final_image, (new_width, new_height))
            else:
                self.create_dynamic_logo()
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            self.create_dynamic_logo()
    
    def create_dynamic_logo(self):
        """Crear un logo animado y atractivo"""
        self.final_image = pygame.Surface((400, 300), pygame.SRCALPHA)
        # Fondo gradiente
        for y in range(300):
            alpha = int(150 * (y / 300))
            color = (20, 20, 40, alpha)
            pygame.draw.line(self.final_image, color, (0, y), (400, y))
        
        # Logo central
        center_x, center_y = 200, 150
        pygame.draw.circle(self.final_image, (255, 215, 0, 200), (center_x, center_y), 100)
        pygame.draw.circle(self.final_image, (0, 0, 0, 150), (center_x, center_y), 80)
        
        # Texto del logo
        font = pygame.font.SysFont("Arial", 48, bold=True)
        text = font.render("GD", True, (255, 255, 255))
        text_rect = text.get_rect(center=(center_x, center_y))
        self.final_image.blit(text, text_rect)
        
        # Efecto de brillo
        for i in range(10):
            radius = 100 + i*5
            alpha = 50 - i*5
            pygame.draw.circle(self.final_image, (255, 255, 200, alpha), 
                             (center_x, center_y), radius, 2)
    
    def show_website_message(self, message):
        """Mostrar mensaje sobre la acción de abrir página web"""
        self.showing_website_info = True
        self.website_info_timer = 180  # 3 segundos a 60 FPS
        self.website_info_text = message

class Star:
    """Clase para estrellas mejoradas"""
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(0.5, 2.5)
        self.speed = random.uniform(0.05, 0.2)
        self.brightness = random.randint(100, 255)
        self.twinkle_speed = random.uniform(0.02, 0.05)
        self.twinkle_offset = random.uniform(0, math.pi * 2)
        
    def move(self):
        self.y -= self.speed
        if self.y < -10:
            self.y = HEIGHT + 10
            self.x = random.randint(0, WIDTH)
        
        # Efecto de centelleo
        self.brightness = 150 + int(105 * math.sin(pygame.time.get_ticks() * self.twinkle_speed + self.twinkle_offset))
            
    def draw(self, surface):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)
        
        # Brillo adicional para estrellas grandes
        if self.size > 1.5:
            glow_radius = self.size * 1.5
            glow_surface = pygame.Surface((int(glow_radius * 2), int(glow_radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 255, 200, 50), 
                             (int(glow_radius), int(glow_radius)), glow_radius)
            surface.blit(glow_surface, (int(self.x - glow_radius), int(self.y - glow_radius)))

class Particle:
    """Partículas para efectos especiales"""
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-2, -1)
        self.life = 100
        self.size = random.uniform(1, 3)
        if color:
            self.color = color
        else:
            self.color = random.choice([ACCENT_COLOR, SECONDARY_ACCENT, SPECIAL_COLOR])
        self.alpha = 255
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05  # Gravedad
        self.life -= 1
        self.alpha = int(255 * (self.life / 100))
    
    def draw(self, surface):
        if self.life > 0:
            s = pygame.Surface((int(self.size * 3), int(self.size * 3)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, self.alpha), 
                             (int(self.size * 1.5), int(self.size * 1.5)), self.size)
            surface.blit(s, (int(self.x - self.size * 1.5), int(self.y - self.size * 1.5)))

def create_glow_effect(surface, rect, color, intensity=20):
    """Crear efecto de brillo alrededor de un rectángulo"""
    glow_surf = pygame.Surface((rect.width + intensity*2, rect.height + intensity*2), pygame.SRCALPHA)
    
    for i in range(intensity, 0, -1):
        alpha = int(100 * (i / intensity))
        glow_color = (*color[:3], alpha)
        glow_rect = pygame.Rect(i, i, rect.width + (intensity-i)*2, rect.height + (intensity-i)*2)
        pygame.draw.rect(glow_surf, glow_color, glow_rect, border_radius=10)
    
    surface.blit(glow_surf, (rect.x - intensity, rect.y - intensity))

def draw_background(game_state):
    """Dibuja el fondo con efectos especiales"""
    screen.fill(BACKGROUND)
    
    # Actualizar tiempo
    game_state.time += 1
    game_state.pulse_value = 100 + int(155 * abs(math.sin(game_state.time * 0.01)))
    
    # Partículas de fondo
    for particle in game_state.background_particles:
        particle['y'] -= particle['speed']
        if particle['y'] < -10:
            particle['y'] = HEIGHT + 10
            particle['x'] = random.randint(0, WIDTH)
        
        color_with_alpha = (*particle['color'], 100)
        s = pygame.Surface((particle['size']*2, particle['size']*2), pygame.SRCALPHA)
        pygame.draw.circle(s, color_with_alpha, (particle['size'], particle['size']), particle['size'])
        screen.blit(s, (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))
    
    # Estrellas
    for star in game_state.stars:
        star.move()
        star.draw(screen)
    
    # Efecto de neblina sutil
    fog_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for y in range(0, HEIGHT, 2):
        alpha = int(30 * abs(math.sin(y/100 + game_state.time*0.001)))
        pygame.draw.line(fog_surf, (100, 100, 200, alpha), (0, y), (WIDTH, y))
    screen.blit(fog_surf, (0, 0))

def draw_thank_you_screen(game_state, alpha):
    """Pantalla de agradecimiento con efectos"""
    draw_background(game_state)
    
    # Efecto de partículas
    if random.random() < 0.3:
        game_state.particles.append(
            Particle(random.randint(100, WIDTH-100), HEIGHT, ACCENT_COLOR)
        )
    
    # Actualizar y dibujar partículas
    for particle in game_state.particles[:]:
        particle.update()
        particle.draw(screen)
        if particle.life <= 0:
            game_state.particles.remove(particle)
    
    # Título con efecto de pulso
    pulse_alpha = min(alpha, 255)
    pulse_size = 1 + 0.1 * math.sin(game_state.time * 0.02)
    
    thank_you_surface = title_font.render(thank_you_text, True, ACCENT_COLOR)
    thank_you_rect = thank_you_surface.get_rect(center=(WIDTH//2, HEIGHT//3))
    
    # Efecto de brillo
    create_glow_effect(screen, thank_you_rect, ACCENT_COLOR, 15)
    
    # Escalar para efecto de pulso
    scaled_surface = pygame.transform.scale_by(thank_you_surface, pulse_size)
    scaled_rect = scaled_surface.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(scaled_surface, scaled_rect)
    
    # Subtítulo
    if alpha > 150:
        working_surface = subtitle_font.render(working_text, True, TEXT_COLOR)
        working_rect = working_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(working_surface, working_rect)
        
        # Línea decorativa animada
        line_length = 150 + 50 * math.sin(game_state.time * 0.03)
        pygame.draw.line(screen, SECONDARY_ACCENT, 
                        (WIDTH//2 - line_length, HEIGHT//2 + 40), 
                        (WIDTH//2 + line_length, HEIGHT//2 + 40), 4)
    
    # Instrucción con efecto de parpadeo
    if alpha > 200 and int(game_state.time * 0.1) % 2 == 0:
        instruction = text_font.render("▼ Los créditos comenzarán en breve ▼", True, SECONDARY_ACCENT)
        instruction_rect = instruction.get_rect(center=(WIDTH//2, HEIGHT - 100))
        create_glow_effect(screen, instruction_rect, SECONDARY_ACCENT, 10)
        screen.blit(instruction, instruction_rect)

def draw_credits_screen(game_state, scroll_y):
    """Dibuja la pantalla de créditos con efectos"""
    draw_background(game_state)
    
    # Título de créditos con efectos
    credits_title = title_font.render("CRÉDITOS", True, ACCENT_COLOR)
    credits_title_rect = credits_title.get_rect(center=(WIDTH//2, scroll_y))
    create_glow_effect(screen, credits_title_rect, ACCENT_COLOR, 20)
    screen.blit(credits_title, credits_title_rect)
    
    # Línea decorativa bajo el título
    line_y = scroll_y + 50
    line_length = 200 + 50 * math.sin(game_state.time * 0.02)
    pygame.draw.line(screen, SECONDARY_ACCENT,
                    (WIDTH//2 - line_length, line_y),
                    (WIDTH//2 + line_length, line_y), 3)
    
    # Dibujar cada crédito con efectos
    for i, (role, name) in enumerate(credits):
        y_pos = scroll_y + 120 + (i * 55)
        
        # Efecto de entrada suave
        screen_y = y_pos
        if screen_y > 0 and screen_y < HEIGHT:
            # Partículas ocasionales
            if random.random() < 0.01 and screen_y > HEIGHT//2:
                game_state.particles.append(
                    Particle(WIDTH//2 + random.randint(-200, 200), screen_y, SPECIAL_COLOR)
                )
            
            # Determinar colores
            if role and "MÚSICA" in role:
                role_color = SONG_COLOR
                name_color = SONG_COLOR
            elif name and any(str(num) in name for num in range(1, 10)):
                role_color = SONG_COLOR
                name_color = SONG_COLOR
            elif role and any(word in role for word in ["DIRECCIÓN", "PRODUCCIÓN"]):
                role_color = SPECIAL_COLOR
                name_color = SPECIAL_COLOR
            else:
                role_color = CREDIT_COLOR
                name_color = TEXT_COLOR
            
            # Dibujar rol
            if role:
                role_surface = credit_font.render(role, True, role_color)
                role_rect = role_surface.get_rect(center=(WIDTH//2, screen_y))
                
                # Efecto de brillo para roles importantes
                if role and any(word in role for word in ["DIRECCIÓN", "PRODUCCIÓN", "PRINCIPAL"]):
                    create_glow_effect(screen, role_rect, role_color, 5)
                
                screen.blit(role_surface, role_rect)
            
            # Dibujar nombre
            if name:
                name_size = text_font if role else credit_font
                name_surface = name_size.render(name, True, name_color)
                name_rect = name_surface.get_rect(center=(WIDTH//2, screen_y + 35))
                screen.blit(name_surface, name_rect)
    
    # Instrucción para saltar con efecto de parpadeo
    if int(game_state.time * 0.08) % 3 != 0:
        skip_text = small_font.render("║ ESPACIO: Saltar créditos ║", True, SECONDARY_ACCENT)
        skip_rect = skip_text.get_rect(center=(WIDTH//2, HEIGHT - 30))
        create_glow_effect(screen, skip_rect, SECONDARY_ACCENT, 5)
        screen.blit(skip_text, skip_rect)

def draw_final_screen(game_state):
    """Pantalla final mejorada"""
    draw_background(game_state)
    
    # Mostrar mensaje de página web si está activo
    if game_state.showing_website_info:
        if game_state.website_info_timer > 0:
            game_state.website_info_timer -= 1
            
            # Fondo semitransparente para el mensaje
            msg_bg = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
            msg_bg.fill((0, 0, 0, 200))
            screen.blit(msg_bg, (0, HEIGHT//2 - 50))
            
            # Mensaje
            msg_font = pygame.font.SysFont("Arial", 32)
            msg_surface = msg_font.render(game_state.website_info_text, True, WEB_COLOR)
            msg_rect = msg_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
            create_glow_effect(screen, msg_rect, WEB_COLOR, 10)
            screen.blit(msg_surface, msg_rect)
            
            # Instrucción para continuar
            cont_font = pygame.font.SysFont("Arial", 24)
            cont_surface = cont_font.render("Presiona cualquier tecla para continuar...", True, SECONDARY_ACCENT)
            cont_rect = cont_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
            screen.blit(cont_surface, cont_rect)
            return  # Salir para que no se muestren los otros elementos
    
    # Efecto de partículas especiales
    if random.random() < 0.2:
        for _ in range(5):
            game_state.particles.append(
                Particle(random.randint(WIDTH//2 - 150, WIDTH//2 + 150),
                        HEIGHT, 
                        random.choice([ACCENT_COLOR, SECONDARY_ACCENT, SPECIAL_COLOR]))
            )
    
    # Actualizar partículas
    for particle in game_state.particles[:]:
        particle.update()
        particle.draw(screen)
        if particle.life <= 0:
            game_state.particles.remove(particle)
    
    # Fade in de la imagen
    if game_state.final_image_alpha < 255:
        game_state.final_image_alpha += 2
    
    # Dibujar imagen con efectos
    if game_state.final_image_alpha > 0:
        image_surface = game_state.final_image.copy()
        image_surface.set_alpha(game_state.final_image_alpha)
        image_rect = image_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
        
        # Efecto de brillo alrededor de la imagen
        glow_intensity = int(30 * (game_state.final_image_alpha / 255))
        create_glow_effect(screen, image_rect, ACCENT_COLOR, glow_intensity)
        
        # Efecto de pulso suave
        pulse = 1 + 0.05 * math.sin(game_state.time * 0.015)
        scaled_image = pygame.transform.scale_by(image_surface, pulse)
        scaled_rect = scaled_image.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
        screen.blit(scaled_image, scaled_rect)
    
    # Fade in del texto
    if game_state.final_image_alpha >= 255 and game_state.final_text_alpha < 255:
        game_state.final_delay += 1
        if game_state.final_delay > 30:
            game_state.final_text_alpha += 3
    
    # Texto "Gracias por jugar"
    if game_state.final_text_alpha > 0:
        thank_text = "¡GRACIAS POR SER PARTE DE ESTA AVENTURA!"
        thank_surface = subtitle_font.render(thank_text, True, ACCENT_COLOR)
        thank_surface.set_alpha(game_state.final_text_alpha)
        thank_rect = thank_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 180))
        create_glow_effect(screen, thank_rect, ACCENT_COLOR, 
                          int(10 * (game_state.final_text_alpha / 255)))
        screen.blit(thank_surface, thank_rect)
        
        # Instrucciones finales
        if game_state.final_text_alpha >= 255:
            # Efecto de parpadeo alternado
            if int(game_state.time * 0.1) % 4 < 2:
                space_text = text_font.render("ESPACIO: Participar en encuesta de satisfacción", True, WEB_COLOR)
                space_rect = space_text.get_rect(center=(WIDTH//2, HEIGHT - 100))
                create_glow_effect(screen, space_rect, WEB_COLOR, 5)
                screen.blit(space_text, space_rect)
            
            if int(game_state.time * 0.1) % 4 >= 2:
                menu_text = text_font.render("X: Volver al menú principal", True, SPECIAL_COLOR)
                menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT - 60))
                create_glow_effect(screen, menu_rect, SPECIAL_COLOR, 5)
                screen.blit(menu_text, menu_rect)
            
            # Instrucción ESC
            esc_text = small_font.render("ESC: Salir del juego", True, TEXT_COLOR)
            esc_rect = esc_text.get_rect(center=(WIDTH//2, HEIGHT - 20))
            screen.blit(esc_text, esc_rect)

def fade_in(surface, alpha):
    """Fade in mejorado"""
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(FADE_COLOR)
    fade_surface.set_alpha(255 - alpha)
    surface.blit(fade_surface, (0, 0))
    return alpha + 3

def fade_out(surface, alpha):
    """Fade out mejorado"""
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(FADE_COLOR)
    fade_surface.set_alpha(alpha)
    surface.blit(fade_surface, (0, 0))
    return alpha + 3

def open_website(url):
    """Abrir página web en el navegador"""
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error al abrir la página web: {e}")
        return False

def load_menu():
    """Cargar el archivo menu.py"""
    try:
        # Detener música
        pygame.mixer.music.fadeout(500)
        pygame.time.wait(500)
        
        # Cerrar la ventana actual
        pygame.quit()
        
        # Intentar ejecutar menu.py usando subprocess
        if os.name == 'nt':  # Windows
            subprocess.Popen(['python', 'menu.py'])
        else:  # Linux/Mac
            subprocess.Popen(['python3', 'menu.py'])
        
        sys.exit(0)
        
    except Exception as e:
        print(f"Error al cargar menu.py: {e}")
        print("Asegúrate de que menu.py esté en el mismo directorio")
        return False

def main():
    global game_state
    game_state = GameState()
    clock = pygame.time.Clock()
    
    # Reproducir música si está cargada
    try:
        pygame.mixer.music.play(-1, fade_ms=2000)
    except:
        pass
    
    # Bucle principal
    running = True
    while running:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if game_state.state == "CREDITOS":
                        # Saltar créditos
                        game_state.state = "FINAL"
                        game_state.final_image_alpha = 0
                        game_state.final_text_alpha = 0
                        game_state.final_delay = 0
                        # Efecto de partículas al saltar
                        for _ in range(50):
                            game_state.particles.append(
                                Particle(WIDTH//2, HEIGHT//2, ACCENT_COLOR)
                            )
                    elif game_state.state == "FINAL" and game_state.final_text_alpha >= 255:
                        if not game_state.showing_website_info:
                            # Abrir página web de encuesta
                            print(f"Abriendo página web: {WEBSITE_URL}")
                            if open_website(WEBSITE_URL):
                                game_state.show_website_message("¡Página web abierta en tu navegador!")
                            else:
                                game_state.show_website_message("Error al abrir la página web")
                    elif game_state.state == "FINAL" and game_state.showing_website_info:
                        # Cerrar mensaje de página web
                        game_state.showing_website_info = False
                
                elif event.key == pygame.K_x:
                    if game_state.state == "FINAL" and game_state.final_text_alpha >= 255:
                        if not game_state.showing_website_info:
                            # Cargar menu.py
                            print("Cargando menú principal...")
                            if load_menu():
                                # Si load_menu tuvo éxito, ya se cerró PyGame
                                return
                            else:
                                # Si falló, mostrar mensaje
                                game_state.show_website_message("Error: No se pudo cargar menu.py")
                    elif game_state.state == "FINAL" and game_state.showing_website_info:
                        # Cerrar mensaje
                        game_state.showing_website_info = False
                
                elif game_state.state == "FINAL" and game_state.showing_website_info:
                    # Cualquier tecla cierra el mensaje
                    game_state.showing_website_info = False
        
        # Lógica de estados
        if game_state.state == "ENTRADA":
            draw_background(game_state)
            game_state.alpha = fade_in(screen, game_state.alpha)
            if game_state.alpha >= 255:
                game_state.state = "THANK_YOU"
                game_state.alpha = 0
                
        elif game_state.state == "THANK_YOU":
            game_state.alpha += 2
            draw_thank_you_screen(game_state, game_state.alpha)
            
            # Cambiar a créditos después de tiempo
            if game_state.alpha > 500:  # Más tiempo para apreciar
                game_state.state = "CREDITOS"
                game_state.alpha = 0
                game_state.scroll_y = HEIGHT
                
        elif game_state.state == "CREDITOS":
            game_state.scroll_y -= credit_scroll_speed
            draw_credits_screen(game_state, game_state.scroll_y)
            
            # Verificar si los créditos han terminado
            total_credits_height = len(credits) * 55 + 500
            if game_state.scroll_y < -total_credits_height:
                game_state.state = "FINAL"
                game_state.alpha = 0
                
        elif game_state.state == "FINAL":
            draw_final_screen(game_state)
            
        elif game_state.state == "SALIDA":
            draw_background(game_state)
            game_state.alpha = fade_out(screen, game_state.alpha)
            if game_state.alpha >= 255:
                running = False
        
        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)
    
    # Detener música
    try:
        pygame.mixer.music.fadeout(1000)
    except:
        pass
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()