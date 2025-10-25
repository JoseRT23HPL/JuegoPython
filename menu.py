import pygame
import sys
import os
import math
import subprocess

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla - MENÚ a 960x540
MENU_WIDTH, MENU_HEIGHT = 1200, 540
WIDTH, HEIGHT = 960, 540  # Mantenemos la resolución original para las pantallas de presentación
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cazador De Sueños")

# Superficie para el menú con la dimensión solicitada
menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 180, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
PURPLE = (150, 50, 200)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Fuentes - Mejoradas para diseño más atractivo
title_font = pygame.font.SysFont("Arial", 64, bold=True)
subtitle_font = pygame.font.SysFont("Arial", 36)
menu_font = pygame.font.SysFont("Arial", 38, bold=True)
level_font = pygame.font.SysFont("Arial", 28, bold=True)
info_font = pygame.font.SysFont("Arial", 20)

# Estados del programa
STATE_LOADING = 0
STATE_CREATOR = 1
STATE_LOGO = 2
STATE_DIRECTOR = 3
STATE_UNIVERSITY = 4
STATE_MAIN_MENU = 5
STATE_LEVEL_SELECT = 6

# Variables de estado
current_state = STATE_LOADING
fade_alpha = 0
fade_direction = 1  # 1 para aparecer, -1 para desaparecer
transition_timer = 0
loading_progress = 0
loading_time = 0
music_started = False

# Efectos de flash
flash_alpha = 0
flash_duration = 0

# Tiempos de transición (en milisegundos)
LOADING_TIME = 5000  # 5 segundos para la pantalla de carga

# Tiempos modificados según tu solicitud
FADE_TIME_CREATOR = 3000     # 3 segundos para el creador (incluyendo fade)
FADE_TIME_LOGO = 2000        # 2 segundos para el logo (incluyendo fade)  
FADE_TIME_OTHERS = 1000      # 1 segundo para los demás (incluyendo fade)

# Cargar imágenes (reemplaza con tus propias imágenes)
def load_image(name, scale=1.0, fit_screen=False, fit_menu=False):
    try:
        image = pygame.image.load(name)
        if scale != 1.0:
            new_width = int(image.get_width() * scale)
            new_height = int(image.get_height() * scale)
            image = pygame.transform.scale(image, (new_width, new_height))
        elif fit_screen:
            # Redimensionar para que cubra toda la pantalla manteniendo relación de aspecto
            scale_x = WIDTH / image.get_width()
            scale_y = HEIGHT / image.get_height()
            scale = max(scale_x, scale_y)  # Para cubrir toda la pantalla
            
            new_width = int(image.get_width() * scale)
            new_height = int(image.get_height() * scale)
            image = pygame.transform.scale(image, (new_width, new_height))
        elif fit_menu:
            # Redimensionar para que cubra el área del menú (960x540) manteniendo relación de aspecto
            scale_x = MENU_WIDTH / image.get_width()
            scale_y = MENU_HEIGHT / image.get_height()
            scale = max(scale_x, scale_y)  # Para cubrir toda el área del menú
            
            new_width = int(image.get_width() * scale)
            new_height = int(image.get_height() * scale)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image
    except:
        # Si no se puede cargar la imagen, crear una placeholder
        print(f"Error al cargar: {name}. Usando placeholder.")
        surf = pygame.Surface((300, 200))
        surf.fill((50, 50, 50))
        text = info_font.render(name, True, WHITE)
        surf.blit(text, (10, 10))
        return surf

# Cargar imágenes de presentación (centradas, sin cubrir toda la pantalla)
creator_image = load_image("img/jose.png", 0.6)  # Ajusta el scale según necesites
logo_image = load_image("img/empresa.png", 0.5)
director_image = load_image("img/python.png", 0.6)
university_image = load_image("img/utt.png", 0.5)

# Cargar fondos para el menú principal (estos SÍ cubren toda el área del menú 960x540)
backgrounds = []
try:
    # Reemplaza estos nombres con tus imágenes reales
    menu_backgrounds = [
        "img/bosque.png",
        "img/ciudad.png", 
        "img/ciudad2.png",
        "img/espectaculo.png",
        "img/museo.png"
    ]
    
    for bg_file in menu_backgrounds:
        bg = load_image(bg_file, fit_menu=True)  # Estas sí cubren toda el área del menú
        backgrounds.append(bg)
        
except Exception as e:
    print(f"Error al cargar fondos del menú: {e}. Usando fondos por defecto.")
    # Si no se pueden cargar, usa los fondos originales
    backgrounds = []
    for i in range(5):
        bg = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
        
        # Patrón de fondo diferente para cada uno
        if i == 0:
            # Gradiente azul
            for y in range(MENU_HEIGHT):
                color = (0, 0, 100 + int(155 * y / MENU_HEIGHT))
                pygame.draw.line(bg, color, (0, y), (MENU_WIDTH, y))
        elif i == 1:
            # Gradiente rojo
            for y in range(MENU_HEIGHT):
                color = (100 + int(155 * y / MENU_HEIGHT), 0, 0)
                pygame.draw.line(bg, color, (0, y), (MENU_WIDTH, y))
        elif i == 2:
            # Gradiente verde
            for y in range(MENU_HEIGHT):
                color = (0, 100 + int(155 * y / MENU_HEIGHT), 0)
                pygame.draw.line(bg, color, (0, y), (MENU_WIDTH, y))
        elif i == 3:
            # Patrón de estrellas
            bg.fill((10, 10, 40))
            for _ in range(100):
                x = pygame.time.get_ticks() % MENU_WIDTH
                y = pygame.time.get_ticks() % MENU_HEIGHT
                pygame.draw.circle(bg, WHITE, (x, y), 1)
        else:
            # Patrón de líneas diagonales
            bg.fill((20, 20, 60))
            for i in range(0, MENU_WIDTH + MENU_HEIGHT, 20):
                pygame.draw.line(bg, (50, 50, 100), (i, 0), (0, i), 2)
        
        backgrounds.append(bg)

current_bg = 0
# Variables para el efecto de cámara avanzando (más dinámico)
camera_x = 0
camera_y = 0
camera_speed_x = 0.3  # Velocidad horizontal (avance)
camera_speed_y = 0.1  # Velocidad vertical (ligero movimiento arriba/abajo)
camera_direction_x = 1  # Dirección horizontal (1 = derecha, -1 = izquierda)
camera_direction_y = 1  # Dirección vertical (1 = abajo, -1 = arriba)
bg_timer = 0
bg_flash_alpha = 0

# Opciones del menú principal
menu_options = ["Iniciar Juego", "Opciones", "Créditos", "Salir"]
selected_option = 0

# Niveles disponibles con sus archivos correspondientes
levels = [
    {"name": "Nivel 1", "locked": False, "difficulty": "Fácil", "color": GREEN, "file": "nivel1.py"},
    {"name": "Nivel 2", "locked": False, "difficulty": "Fácil", "color": GREEN, "file": "nivel2.py"},
    {"name": "Nivel 3", "locked": False, "difficulty": "Medio", "color": ORANGE, "file": "nivel3.py"},
    {"name": "Nivel 4", "locked": False, "difficulty": "Medio", "color": ORANGE, "file": "nivel4.py"},
    {"name": "Nivel 5", "locked": False, "difficulty": "Difícil", "color": RED, "file": "nivel5.py"},
    {"name": "Nivel 6", "locked": False, "difficulty": "Difícil", "color": RED, "file": "nivel6.py"},
    {"name": "Nivel 7", "locked": False, "difficulty": "Experto", "color": PURPLE, "file": "nivel7.py"},
    {"name": "Nivel 8", "locked": True, "difficulty": "Experto", "color": PURPLE, "file": "nivel8.py"}
]
selected_level = 0

# Efectos de partículas para el título
particles = []
for i in range(50):
    particles.append({
        'x': pygame.time.get_ticks() % WIDTH,
        'y': pygame.time.get_ticks() % 150,
        'speed': 0.5 + pygame.time.get_ticks() % 100 * 0.01,
        'size': 2 + pygame.time.get_ticks() % 3,
        'color': (LIGHT_BLUE if i % 3 == 0 else GOLD if i % 3 == 1 else SILVER)
    })

# Cargar música (reemplaza "tu_musica.mp3" con tu archivo de música)
try:
    pygame.mixer.music.load("sound/fondoM.mp3")
    pygame.mixer.music.set_volume(0.7)
    print("Música cargada correctamente - Esperando al 100% de carga")
except:
    print("Error al cargar la música. Verifica que el archivo existe.")

# Función para activar efecto flash
def trigger_flash(duration=500, alpha=255):
    global flash_alpha, flash_duration
    flash_alpha = alpha
    flash_duration = duration

# Función para ejecutar un nivel
def ejecutar_nivel(archivo_nivel):
    try:
        print(f"🔄 Ejecutando {archivo_nivel}...")
        
        # Detener la música antes de cambiar de programa
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
        # Cerrar la ventana actual de Pygame
        pygame.quit()
        
        # Ejecutar el archivo del nivel usando subprocess
        if os.path.exists(archivo_nivel):
            subprocess.run([sys.executable, archivo_nivel])
        else:
            print(f"❌ Error: El archivo {archivo_nivel} no existe")
            input("Presiona Enter para continuar...")
        
        # Reiniciar Pygame después de que termine el nivel
        pygame.init()
        pygame.mixer.init()
        
        # Restaurar la configuración de la pantalla
        global screen
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Presentación con Menú")
        
        # Reanudar la música
        try:
            pygame.mixer.music.load("fondoM.mp3")
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
        except:
            print("Error al recargar la música")
            
        return True
        
    except Exception as e:
        print(f"❌ Error al ejecutar {archivo_nivel}: {e}")
        # En caso de error, reiniciar Pygame
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        return False

# Función para dibujar botón con diseño moderno
def draw_button(surface, text, x, y, width, height, color, is_selected=False, is_locked=False):
    # Colores según el estado
    if is_locked:
        bg_color = (50, 50, 50, 200)
        border_color = (100, 100, 100)
        text_color = (150, 150, 150)
    elif is_selected:
        bg_color = (color[0]//3, color[1]//3, color[2]//3, 200)
        border_color = color
        text_color = GOLD
    else:
        bg_color = (30, 30, 60, 180)
        border_color = (70, 70, 100)
        text_color = color
    
    # Fondo del botón con bordes redondeados
    button_bg = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(button_bg, bg_color, (0, 0, width, height), border_radius=12)
    pygame.draw.rect(button_bg, border_color, (0, 0, width, height), 2, border_radius=12)
    surface.blit(button_bg, (x, y))
    
    # Efecto de brillo para botón seleccionado
    if is_selected and not is_locked:
        glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*color, 30), (0, 0, width, height), border_radius=15)
        surface.blit(glow_surface, (x, y))
    
    # Texto del botón
    text_surf = level_font.render(text, True, text_color)
    text_x = x + (width - text_surf.get_width()) // 2
    text_y = y + (height - text_surf.get_height()) // 2
    surface.blit(text_surf, (text_x, text_y))
    
    # Indicador de candado para niveles bloqueados
    if is_locked:
        lock_text = info_font.render("BLOQUEADO", True, SILVER)
        surface.blit(lock_text, (x + width - 25, y + 10))
    
    return pygame.Rect(x, y, width, height)

# Bucle principal
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)  # Delta time en milisegundos
    
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if current_state == STATE_MAIN_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Iniciar Juego
                        trigger_flash(600, 180)
                        current_state = STATE_LEVEL_SELECT
                        selected_level = 0
                        print("Abriendo selección de niveles...")
                    elif selected_option == 1:
                        print("Abriendo opciones...")
                    elif selected_option == 2:
                        print("Mostrando créditos...")
                    elif selected_option == 3:
                        running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        elif current_state == STATE_LEVEL_SELECT:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_level = max(0, selected_level - 1)
                elif event.key == pygame.K_RIGHT:
                    selected_level = min(len(levels) - 1, selected_level + 1)
                elif event.key == pygame.K_UP:
                    selected_level = max(0, selected_level - 2)
                elif event.key == pygame.K_DOWN:
                    selected_level = min(len(levels) - 1, selected_level + 2)
                elif event.key == pygame.K_RETURN:
                    selected_level_info = levels[selected_level]
                    if not selected_level_info["locked"]:
                        trigger_flash(400, 150)
                        print(f"🎮 Iniciando {selected_level_info['name']}...")
                        print(f"📁 Archivo: {selected_level_info['file']}")
                        
                        # Ejecutar el nivel correspondiente
                        nivel_ejecutado = ejecutar_nivel(selected_level_info["file"])
                        
                        if nivel_ejecutado:
                            print(f"✅ Regresando del {selected_level_info['name']}")
                            trigger_flash(300, 100)
                        else:
                            print(f"❌ Error al ejecutar {selected_level_info['name']}")
                            
                    else:
                        print("🔒 ¡Nivel bloqueado! Completa los niveles anteriores.")
                elif event.key == pygame.K_ESCAPE:
                    trigger_flash(400, 150)
                    current_state = STATE_MAIN_MENU
                    print("Volviendo al menú principal...")
    
    # Lógica de estados
    if current_state == STATE_LOADING:
        loading_time += dt
        loading_progress = min(100, loading_time / LOADING_TIME * 100)
        
        # Cuando la carga llega al 100%, comenzar música y cambiar estado
        if loading_progress >= 100 and not music_started:
            # Iniciar música en bucle - SOLO AQUÍ SE REPRODUCE
            pygame.mixer.music.play(-1)  # -1 para que se repita indefinidamente
            music_started = True
            print("¡Música iniciada! Comenzando presentación...")
            current_state = STATE_CREATOR
            transition_timer = 0
            fade_alpha = 0
            fade_direction = 1
    
    elif current_state in [STATE_CREATOR, STATE_LOGO, STATE_DIRECTOR, STATE_UNIVERSITY]:
        transition_timer += dt
        
        # Determinar el tiempo total según el estado actual
        if current_state == STATE_CREATOR:
            total_time = FADE_TIME_CREATOR
        elif current_state == STATE_LOGO:
            total_time = FADE_TIME_LOGO
        else:
            total_time = FADE_TIME_OTHERS
        
        # Controlar efecto de fade (aparecer y desaparecer en el tiempo total)
        half_time = total_time / 2
        
        if transition_timer < half_time:
            # Fade-in durante la primera mitad del tiempo
            fade_alpha = min(255, (transition_timer / half_time) * 255)
        else:
            # Fade-out durante la segunda mitad del tiempo
            fade_alpha = max(0, 255 - ((transition_timer - half_time) / half_time) * 255)
        
        # Cambiar al siguiente estado cuando se complete el tiempo
        if transition_timer >= total_time:
            if current_state == STATE_CREATOR:
                current_state = STATE_LOGO
                print("Mostrando logo de la empresa...")
            elif current_state == STATE_LOGO:
                current_state = STATE_DIRECTOR
                print("Mostrando director...")
            elif current_state == STATE_DIRECTOR:
                current_state = STATE_UNIVERSITY
                print("Mostrando universidad...")
            elif current_state == STATE_UNIVERSITY:
                # Activar flash antes de entrar al menú
                trigger_flash(800, 200)
                current_state = STATE_MAIN_MENU
                print("Entrando al menú principal...")
            
            # Reiniciar temporizadores para el nuevo estado
            transition_timer = 0
            fade_alpha = 0
    
    elif current_state in [STATE_MAIN_MENU, STATE_LEVEL_SELECT]:
        # Efecto de cámara avanzando (movimiento más dinámico)
        # Movimiento horizontal principal (como si avanzáramos)
        camera_x += camera_speed_x * camera_direction_x * dt / 16
        
        # Movimiento vertical más suave (como ligero bamboleo)
        camera_y += camera_speed_y * camera_direction_y * dt / 16
        
        # Cambiar dirección horizontal cuando llegamos a los bordes
        if camera_x > MENU_WIDTH - WIDTH or camera_x < 0:
            camera_direction_x *= -1
        
        # Cambiar dirección vertical cuando llegamos a los bordes
        if camera_y > MENU_HEIGHT - HEIGHT or camera_y < 0:
            camera_direction_y *= -1
        
        # Asegurar que la cámara no se salga de los límites
        camera_x = max(0, min(camera_x, MENU_WIDTH - WIDTH))
        camera_y = max(0, min(camera_y, MENU_HEIGHT - HEIGHT))
        
        # Cambio de fondo cada 15 segundos con efecto flash
        bg_timer += dt
        if bg_timer >= 15000:  # 15 segundos
            bg_timer = 0
            current_bg = (current_bg + 1) % len(backgrounds)
            trigger_flash(600, 180)  # Flash más suave para cambio de fondo
            # Reiniciar posición de cámara al cambiar fondo
            camera_x = 0
            camera_y = 0
            camera_direction_x = 1
            camera_direction_y = 1
        
        # Actualizar partículas del título
        for particle in particles:
            particle['y'] += particle['speed']
            if particle['y'] > 150:
                particle['y'] = 0
                particle['x'] = pygame.time.get_ticks() % WIDTH
    
    # Actualizar efecto flash
    if flash_alpha > 0:
        flash_alpha = max(0, flash_alpha - dt * (255 / flash_duration))
    
    # Dibujado
    screen.fill(BLACK)
    
    if current_state == STATE_LOADING:
        # Dibujar pantalla de carga
        title = title_font.render("CARGANDO", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        
        # Dibujar barra de carga
        bar_width = 400
        bar_height = 30
        bar_x = WIDTH//2 - bar_width//2
        bar_y = HEIGHT//2
        
        # Fondo de la barra
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Barra de progreso
        progress_width = int(bar_width * loading_progress / 100)
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, progress_width, bar_height))
        
        # Porcentaje
        percent_text = info_font.render(f"{int(loading_progress)}%", True, WHITE)
        screen.blit(percent_text, (WIDTH//2 - percent_text.get_width()//2, bar_y + bar_height + 10))
        
        # Indicador de música
        if not music_started:
            music_text = info_font.render("Esapere un Momento", True, GREEN)
            screen.blit(music_text, (WIDTH//2 - music_text.get_width()//2, bar_y + bar_height + 40))
        else:
            music_text = info_font.render("♪ Música reproduciéndose ♪", True, GREEN)
            screen.blit(music_text, (WIDTH//2 - music_text.get_width()//2, bar_y + bar_height + 40))
    
    elif current_state == STATE_CREATOR:
        # Fondo negro para las pantallas de presentación
        screen.fill(BLACK)
        
        # Dibujar imagen del creador con efecto fade (centrada)
        if creator_image:
            img_rect = creator_image.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            creator_image.set_alpha(int(fade_alpha))
            screen.blit(creator_image, img_rect)
        
        # Texto del creador
        creator_text = subtitle_font.render("Creado Por Jose Miguel", True, WHITE)
        creator_text.set_alpha(int(fade_alpha))
        screen.blit(creator_text, (WIDTH//2 - creator_text.get_width()//2, HEIGHT//2 + 100))
    
    elif current_state == STATE_LOGO:
        # Fondo negro para las pantallas de presentación
        screen.fill(BLACK)
        
        # Dibujar logo de la empresa con efecto fade (centrada)
        if logo_image:
            img_rect = logo_image.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            logo_image.set_alpha(int(fade_alpha))
            screen.blit(logo_image, img_rect)
        
        # Texto de la empresa
        logo_text = subtitle_font.render("Empresa innova", True, BLUE)
        logo_text.set_alpha(int(fade_alpha))
        screen.blit(logo_text, (WIDTH//2 - logo_text.get_width()//2, HEIGHT//2 + 100))
    
    elif current_state == STATE_DIRECTOR:
        # Fondo negro para las pantallas de presentación
        screen.fill(BLACK)
        
        # Dibujar imagen del director con efecto fade (centrada)
        if director_image:
            img_rect = director_image.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            director_image.set_alpha(int(fade_alpha))
            screen.blit(director_image, img_rect)
        
        # Texto del director
        director_text = subtitle_font.render("Python Production", True, WHITE)
        director_text.set_alpha(int(fade_alpha))
        screen.blit(director_text, (WIDTH//2 - director_text.get_width()//2, HEIGHT//2 + 100))
    
    elif current_state == STATE_UNIVERSITY:
        # Fondo negro para las pantallas de presentación
        screen.fill(BLACK)
        
        # Dibujar logo de la universidad con efecto fade (centrada)
        if university_image:
            img_rect = university_image.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            university_image.set_alpha(int(fade_alpha))
            screen.blit(university_image, img_rect)
        
        # Texto de la universidad
        uni_text = subtitle_font.render("Universidad Tecnologica de Tecamachalco", True, GREEN)
        uni_text.set_alpha(int(fade_alpha))
        screen.blit(uni_text, (WIDTH//2 - uni_text.get_width()//2, HEIGHT//2 + 100))
    
    elif current_state == STATE_MAIN_MENU:
        # Limpiar la superficie del menú
        menu_surface.fill(BLACK)
        
        # Dibujar el fondo actual en la superficie del menú (960x540)
        bg = backgrounds[current_bg]
        menu_surface.blit(bg, (0, 0))
        
        # Dibujar la porción visible del menú en la pantalla principal (efecto cámara)
        screen.blit(menu_surface, (0, 0), (camera_x, camera_y, WIDTH, HEIGHT))
        
        # Capa negra semitransparente para mejor legibilidad del texto
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(120)  # Transparencia ajustada
        screen.blit(overlay, (0, 0))
        
        # Dibujar partículas de fondo para el título
        for particle in particles:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
        
        # Título con diseño mejorado
        title_text = "MENÚ PRINCIPAL"
        
        # Sombra del título
        title_shadow = title_font.render(title_text, True, (30, 30, 60))
        screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + 3, 53))
        
        # Título principal con gradiente
        title_surface = title_font.render(title_text, True, LIGHT_BLUE)
        screen.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 50))
        
        # Efecto de brillo en el título
        title_highlight = title_font.render(title_text, True, WHITE)
        title_highlight.set_alpha(80)
        screen.blit(title_highlight, (WIDTH//2 - title_highlight.get_width()//2, 48))
        
        # Línea decorativa bajo el título
        line_y = 120
        pygame.draw.line(screen, GOLD, (WIDTH//2 - 150, line_y), (WIDTH//2 - 20, line_y), 3)
        pygame.draw.line(screen, GOLD, (WIDTH//2 + 150, line_y), (WIDTH//2 + 20, line_y), 3)
        
        # Dibujar opciones del menú con diseño mejorado
        for i, option in enumerate(menu_options):
            # Colores y efectos según si está seleccionada
            if i == selected_option:
                # Opción seleccionada - diseño destacado
                color = GOLD
                bg_color = (30, 30, 60, 200)
                border_color = LIGHT_BLUE
                text_shadow = True
                
                # Efecto de brillo para la opción seleccionada
                glow_surface = pygame.Surface((400, 60), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (100, 180, 255, 30), 
                               (0, 0, 400, 60), border_radius=15)
                screen.blit(glow_surface, (WIDTH//2 - 200, 180 + i * 70))
            else:
                # Opción normal
                color = LIGHT_BLUE
                bg_color = (20, 20, 40, 180)
                border_color = (70, 70, 100)
                text_shadow = False
            
            # Fondo de la opción con bordes redondeados
            option_bg = pygame.Surface((400, 60), pygame.SRCALPHA)
            pygame.draw.rect(option_bg, bg_color, (0, 0, 400, 60), border_radius=12)
            pygame.draw.rect(option_bg, border_color, (0, 0, 400, 60), 2, border_radius=12)
            screen.blit(option_bg, (WIDTH//2 - 200, 180 + i * 70))
            
            # Texto de la opción
            option_text = menu_font.render(option, True, color)
            
            # Sombra del texto para mejor legibilidad
            if text_shadow:
                text_shadow_surf = menu_font.render(option, True, (0, 0, 30))
                screen.blit(text_shadow_surf, 
                          (WIDTH//2 - option_text.get_width()//2 + 2, 
                           182 + i * 70 + 2))
            
            screen.blit(option_text, 
                      (WIDTH//2 - option_text.get_width()//2, 
                       180 + i * 70 + 10))
            
            # Indicador de selección (triángulo)
            if i == selected_option:
                triangle_points = [
                    (WIDTH//2 - 220, 190 + i * 70 + 15),
                    (WIDTH//2 - 200, 190 + i * 70 + 25),
                    (WIDTH//2 - 220, 190 + i * 70 + 35)
                ]
                pygame.draw.polygon(screen, GOLD, triangle_points)
                
                triangle_points = [
                    (WIDTH//2 + 220, 190 + i * 70 + 15),
                    (WIDTH//2 + 200, 190 + i * 70 + 25),
                    (WIDTH//2 + 220, 190 + i * 70 + 35)
                ]
                pygame.draw.polygon(screen, GOLD, triangle_points)
        
        # Panel de instrucciones con diseño mejorado
        instructions_bg = pygame.Surface((WIDTH - 100, 50), pygame.SRCALPHA)
        pygame.draw.rect(instructions_bg, (0, 0, 0, 150), (0, 0, WIDTH - 100, 50), border_radius=10)
        screen.blit(instructions_bg, (50, HEIGHT - 70))
        
        instructions = info_font.render("Usa las flechas ↑↓ para navegar y ENTER para seleccionar", True, SILVER)
        screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT - 55))
        
        # Indicador del fondo actual
        bg_indicator = info_font.render(f"Fondo {current_bg + 1}/{len(backgrounds)}", True, SILVER)
        screen.blit(bg_indicator, (WIDTH - bg_indicator.get_width() - 10, 10))
    
    elif current_state == STATE_LEVEL_SELECT:
        # Limpiar la superficie del menú
        menu_surface.fill(BLACK)
        
        # Dibujar el fondo actual en la superficie del menú (960x540)
        bg = backgrounds[current_bg]
        menu_surface.blit(bg, (0, 0))
        
        # Dibujar la porción visible del menú en la pantalla principal (efecto cámara)
        screen.blit(menu_surface, (0, 0), (camera_x, camera_y, WIDTH, HEIGHT))
        
        # Capa negra semitransparente para mejor legibilidad del texto
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(120)  # Transparencia ajustada
        screen.blit(overlay, (0, 0))
        
        # Dibujar partículas de fondo para el título
        for particle in particles:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
        
        # Título de selección de niveles
        title_text = "SELECCIÓN DE NIVELES"
        
        # Sombra del título
        title_shadow = title_font.render(title_text, True, (30, 30, 60))
        screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + 3, 53))
        
        # Título principal
        title_surface = title_font.render(title_text, True, LIGHT_BLUE)
        screen.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 50))
        
        # Efecto de brillo en el título
        title_highlight = title_font.render(title_text, True, WHITE)
        title_highlight.set_alpha(80)
        screen.blit(title_highlight, (WIDTH//2 - title_highlight.get_width()//2, 48))
        
        # Línea decorativa bajo el título
        line_y = 120
        pygame.draw.line(screen, GOLD, (WIDTH//2 - 180, line_y), (WIDTH//2 - 20, line_y), 3)
        pygame.draw.line(screen, GOLD, (WIDTH//2 + 180, line_y), (WIDTH//2 + 20, line_y), 3)
        
        # Diseño de la cuadrícula de niveles (2 filas x 4 columnas)
        level_width = 160
        level_height = 100
        margin = 20
        start_x = (WIDTH - (4 * level_width + 3 * margin)) // 2
        start_y = 150
        
        # Dibujar niveles en cuadrícula
        for i, level in enumerate(levels):
            row = i // 4
            col = i % 4
            
            x = start_x + col * (level_width + margin)
            y = start_y + row * (level_height + margin)
            
            is_selected = (i == selected_level)
            is_locked = level["locked"]
            
            # Dibujar botón del nivel
            level_rect = draw_button(
                screen, 
                level["name"], 
                x, y, 
                level_width, level_height, 
                level["color"], 
                is_selected, 
                is_locked
            )
            
            # Información adicional del nivel (dificultad)
            if not is_locked:
                diff_text = info_font.render(level["difficulty"], True, SILVER)
                screen.blit(diff_text, (x + (level_width - diff_text.get_width()) // 2, y + level_height - 25))
        
        # Información del nivel seleccionado
        selected_level_info = levels[selected_level]
        info_bg = pygame.Surface((400, 80), pygame.SRCALPHA)
        pygame.draw.rect(info_bg, (0, 0, 0, 180), (0, 0, 400, 80), border_radius=10)
        screen.blit(info_bg, (WIDTH//2 - 200, HEIGHT - 120))
        
        level_name_text = subtitle_font.render(selected_level_info["name"], True, selected_level_info["color"])
        screen.blit(level_name_text, (WIDTH//2 - level_name_text.get_width()//2, HEIGHT - 110))
        
        status_text = "BLOQUEADO" if selected_level_info["locked"] else "DISPONIBLE"
        status_color = RED if selected_level_info["locked"] else GREEN
        status_surface = info_font.render(f"Estado: {status_text}", True, status_color)
        screen.blit(status_surface, (WIDTH//2 - status_surface.get_width()//2, HEIGHT - 70))
        
        # Mostrar archivo del nivel
        file_text = info_font.render(f"Archivo: {selected_level_info['file']}", True, CYAN)
        screen.blit(file_text, (WIDTH//2 - file_text.get_width()//2, HEIGHT - 50))
        
        # Panel de instrucciones
        instructions_bg = pygame.Surface((WIDTH - 100, 50), pygame.SRCALPHA)
        pygame.draw.rect(instructions_bg, (0, 0, 0, 150), (0, 0, WIDTH - 100, 50), border_radius=10)
        screen.blit(instructions_bg, (50, HEIGHT - 60))
        
        if selected_level_info["locked"]:
            instructions = info_font.render("Flechas para navegar • ESC para volver • Completa niveles anteriores", True, SILVER)
        else:
            instructions = info_font.render("Flechas para navegar • ENTER para jugar • ESC para volver", True, SILVER)
        screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT - 45))
    
    # Aplicar efecto flash si está activo
    if flash_alpha > 0:
        flash_surface = pygame.Surface((WIDTH, HEIGHT))
        flash_surface.fill(WHITE)
        flash_surface.set_alpha(int(flash_alpha))
        screen.blit(flash_surface, (0, 0))
    
    # Actualizar pantalla
    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()