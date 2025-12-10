import pygame
import sys
import os
import math
import subprocess
import random  # Para las frases aleatorias

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla - MENÚ a 960x540
MENU_WIDTH, MENU_HEIGHT = 1200, 540
WIDTH, HEIGHT = 960, 540  # Mantenemos la resolución original para las pantallas de presentación
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BIT HUNTER")

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
YELLOW = (255, 255, 0)

# Fuentes - Mejoradas para diseño más atractivo
title_font = pygame.font.SysFont("Arial", 64, bold=True)
subtitle_font = pygame.font.SysFont("Arial", 36)
menu_font = pygame.font.SysFont("Arial", 38, bold=True)
level_font = pygame.font.SysFont("Arial", 28, bold=True)
info_font = pygame.font.SysFont("Arial", 20)
credits_name_font = pygame.font.SysFont("Arial", 32, bold=True)  # Nueva fuente para nombres
credits_role_font = pygame.font.SysFont("Arial", 24)  # Nueva fuente para roles
secret_font = pygame.font.SysFont("Arial", 40, bold=True)  # Nueva fuente para clave secreta

# Estados del programa - AGREGADO NUEVO ESTADO
STATE_LOADING = 0
STATE_CREATOR_1 = 1
STATE_CREATOR_2 = 2
STATE_LOGO = 3
STATE_DIRECTOR = 4
STATE_UNIVERSITY = 5
STATE_MAIN_MENU = 6
STATE_LEVEL_SELECT = 7
STATE_CREDITS = 8
STATE_SECRET_KEY = 9  # Nuevo estado para entrada de clave secreta
STATE_SECRET_CONFIRM = 10  # Nuevo estado para confirmación de nivel secreto

# Variables de estado
current_state = STATE_LOADING
fade_alpha = 0
fade_direction = 1  # 1 para aparecer, -1 para desaparecer
transition_timer = 0
loading_progress = 0
loading_time = 0
music_started = False

# Variables para clave secreta
secret_code = "2307"  # La clave secreta
input_code = ""  # Lo que el usuario va ingresando
error_message = ""  # Mensaje de error
error_timer = 0  # Temporizador para mensaje de error
error_phrases = [  # Frases aleatorias para errores
    "No eres apto para esto, Vete",
    "¡Acceso Denegado!",
    "Clave incorrecta, inténtalo de nuevo",
    "No tienes permiso para pasar",
    "¡Eso no es correcto!"
]

# Efectos de flash
flash_alpha = 0
flash_duration = 0

# Tiempos de transición (en milisegundos) - AJUSTABLES SEGÚN TU CANCIÓN
LOADING_TIME = 3000           # 5 segundos para la pantalla de carga
FADE_TIME_CREATOR_1 = 2000    # 3 segundos para vista 1 - AJUSTA ESTE VALOR
FADE_TIME_CREATOR_2 = 2000    # 3 segundos para vista 2 - AJUSTA ESTE VALOR
FADE_TIME_LOGO = 1000         # 3 segundos para logo - AJUSTA ESTE VALOR
FADE_TIME_DIRECTOR = 1000     # 3 segundos para director - AJUSTA ESTE VALOR
FADE_TIME_UNIVERSITY = 1000   # 3 segundos para universidad - AJUSTA ESTE VALOR
CREDITS_TIME = 5000           # 5 segundos para cada vista de créditos (aumentado)

# Datos para las vistas
vistas = [
    # Vista 1 - Creado por Jose Miguel, Angel, Maria Fernanda
    {
        "titulo": "Creado por",
        "integrantes": [
            "Jose Miguel Rodriguez Tinoco",
            "Ángel Valentín Flores Eduardo", 
            "María Fernanda Andrade Herrera"
        ],
        "tiempo": FADE_TIME_CREATOR_1
    },
    # Vista 2 - Creado por Antonio, Ines, Hector  
    {
        "titulo": "Creado por",
        "integrantes": [
            "Antonio Arellano Morales",
            "Inés Osorio Garcia",
            "Héctor Agustín Castillo Pérez"
        ],
        "tiempo": FADE_TIME_CREATOR_2
    },
    # Vista 3 - Logo de la empresa
    {
        "tipo": "imagen",
        "titulo": "Empresa Innova",
        "imagen": "img/intellisoft.jpg",
        "tiempo": FADE_TIME_LOGO
    },
    # Vista 4 - Director
    {
        "tipo": "imagen", 
        "titulo": "Python Production",
        "imagen": "img/python.png",
        "tiempo": FADE_TIME_DIRECTOR
    },
    # Vista 5 - Universidad
    {
        "tipo": "imagen",
        "titulo": ["Por La Universidad "],  # Lista con dos líneas
        "imagen": "img/utt.png", 
        "tiempo": FADE_TIME_UNIVERSITY
    }
]

# Datos para las vistas de créditos - MEJORADO CON DISEÑO ALTERNANTE Y NOMBRES AJUSTADOS
creditos_vistas = [
    # Vistas individuales de creadores con diseño alternante
    {
        "nombre": "Jose Miguel\nRodriguez Tinoco",
        "rol": "Programador Principal",
        "lado": "izquierda",  # Texto a la izquierda, imagen a la derecha
        "imagen": "img/e3.png"
    },
    {
        "nombre": "Ángel Valentín\nFlores Eduardo",
        "rol": "Diseñador de Niveles", 
        "lado": "derecha",  # Imagen a la izquierda, texto a la derecha
        "imagen": "img/clonM.png"
    },
    {
        "nombre": "María Fernanda\nAndrade Herrera",
        "rol": "Artista Gráfica",
        "lado": "izquierda",
        "imagen": "img/fantasma.png"
    },
    {
        "nombre": "Inés Osorio\nGarcia",
        "rol": "Diseñadora de UI",
        "lado": "derecha",
        "imagen": "img/robot.png"
    },
    {
        "nombre": "Antonio Arellano\nMorales",
        "rol": "Programador de Gameplay",
        "lado": "izquierda",
        "imagen": "img/nave.png"
    },
    {
        "nombre": "Héctor Agustín\nCastillo Pérez",
        "rol": "Compositor Musical",
        "lado": "derecha",
        "imagen": "img/numero1.png"
    },
    # Vistas de autores de canciones (estilo imagen 2)
    {
        "tipo": "autores",
        "titulo": "Autores de Canciones",
        "nombres": ["Autor 1", "Autor 2", "Autor 3"],
        "lado": "centro"
    },
    {
        "tipo": "autores", 
        "titulo": "Autores de Canciones",
        "nombres": ["Autor 4", "Autor 5", "Autor 6"],
        "lado": "centro"
    },
    {
        "tipo": "autores",
        "titulo": "Autores de Canciones", 
        "nombres": ["Autor 7", "Autor 8"],
        "lado": "centro"
    }
]

# Variables para créditos
current_credit_view = 0
credit_timer = 0

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
        surf = pygame.Surface((300, 300))
        surf.fill((30, 30, 60))
        pygame.draw.rect(surf, GOLD, (0, 0, 300, 300), 3)
        
        # Dibujar icono de usuario
        pygame.draw.circle(surf, LIGHT_BLUE, (150, 120), 60)
        pygame.draw.circle(surf, LIGHT_BLUE, (150, 120), 50)
        
        # Dibujar torso
        pygame.draw.rect(surf, LIGHT_BLUE, (100, 170, 100, 80))
        
        text = info_font.render("Imagen", True, WHITE)
        surf.blit(text, (150 - text.get_width()//2, 270))
        return surf

# Cargar imágenes de presentación
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

# Opciones del menú principal - CAMBIADO: "Opciones" por "Clave Secreta"
menu_options = ["Iniciar Juego", "Clave Secreta", "Créditos", "Salir"]
selected_option = 0

# Niveles disponibles con sus archivos correspondientes
levels = [
    {"name": "Nivel 1", "locked": False, "difficulty": "Fácil", "color": GREEN, "file": "historia.py"},
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

# Función para ejecutar el nivel secreto
def ejecutar_nivel_secreto():
    return ejecutar_nivel("secreto.py")

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

# Función para dibujar pantalla de entrada de clave secreta
def draw_secret_key_screen(surface):
    # Limpiar la superficie del menú
    menu_surface.fill(BLACK)
    
    # Dibujar el fondo actual en la superficie del menú
    bg = backgrounds[current_bg]
    menu_surface.blit(bg, (0, 0))
    
    # Dibujar la porción visible del menú en la pantalla principal
    surface.blit(menu_surface, (0, 0), (camera_x, camera_y, WIDTH, HEIGHT))
    
    # Capa semitransparente para mejor legibilidad
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(150)
    surface.blit(overlay, (0, 0))
    
    # Título
    title_text = "CLAVE SECRETA"
    title_surface = title_font.render(title_text, True, GOLD)
    surface.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 80))
    
    # Instrucciones
    instruction = subtitle_font.render("Ingresa la Clave Secreta:", True, LIGHT_BLUE)
    surface.blit(instruction, (WIDTH//2 - instruction.get_width()//2, 160))
    
    # Caja para ingresar código
    input_box_width = 300
    input_box_height = 80
    input_box_x = WIDTH//2 - input_box_width//2
    input_box_y = 220
    
    # Dibujar caja de entrada
    input_bg = pygame.Surface((input_box_width, input_box_height), pygame.SRCALPHA)
    pygame.draw.rect(input_bg, (30, 30, 60, 200), (0, 0, input_box_width, input_box_height), border_radius=15)
    pygame.draw.rect(input_bg, GOLD, (0, 0, input_box_width, input_box_height), 3, border_radius=15)
    surface.blit(input_bg, (input_box_x, input_box_y))
    
    # Mostrar código ingresado (con asteriscos)
    display_code = "*" * len(input_code)
    code_surface = secret_font.render(display_code, True, GREEN)
    surface.blit(code_surface, (WIDTH//2 - code_surface.get_width()//2, input_box_y + 25))
    
    # Mostrar mensaje de error si existe
    if error_message and error_timer > 0:
        # Efecto de temblor para el mensaje de error
        shake_offset = random.randint(-3, 3) if pygame.time.get_ticks() % 100 < 50 else 0
        
        error_surface = subtitle_font.render(error_message, True, RED)
        surface.blit(error_surface, (WIDTH//2 - error_surface.get_width()//2 + shake_offset, 320))
    
    # Botones de control
    button_width = 180
    button_height = 50
    button_y = 380
    
    # Botón para borrar
    clear_color = ORANGE
    clear_bg = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    pygame.draw.rect(clear_bg, (clear_color[0]//4, clear_color[1]//4, clear_color[2]//4, 200), 
                    (0, 0, button_width, button_height), border_radius=10)
    pygame.draw.rect(clear_bg, clear_color, (0, 0, button_width, button_height), 2, border_radius=10)
    surface.blit(clear_bg, (WIDTH//2 - button_width - 20, button_y))
    
    clear_text = menu_font.render("BORRAR", True, clear_color)
    surface.blit(clear_text, (WIDTH//2 - button_width - 20 + (button_width - clear_text.get_width())//2, 
                            button_y + 10))
    
    # Botón para intentar
    try_color = GREEN
    try_bg = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    pygame.draw.rect(try_bg, (try_color[0]//4, try_color[1]//4, try_color[2]//4, 200), 
                    (0, 0, button_width, button_height), border_radius=10)
    pygame.draw.rect(try_bg, try_color, (0, 0, button_width, button_height), 2, border_radius=10)
    surface.blit(try_bg, (WIDTH//2 + 20, button_y))
    
    try_text = menu_font.render("INTENTAR", True, try_color)
    surface.blit(try_text, (WIDTH//2 + 20 + (button_width - try_text.get_width())//2, 
                          button_y + 10))
    
    # Instrucciones en la parte inferior
    instructions_bg = pygame.Surface((WIDTH - 100, 50), pygame.SRCALPHA)
    pygame.draw.rect(instructions_bg, (0, 0, 0, 150), (0, 0, WIDTH - 100, 50), border_radius=10)
    surface.blit(instructions_bg, (50, HEIGHT - 70))
    
    instructions = info_font.render("Ingresa números (0-9) • ENTER para intentar • ESC para volver", True, SILVER)
    surface.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT - 55))

# Función para dibujar pantalla de confirmación de nivel secreto
def draw_secret_confirm_screen(surface):
    # Limpiar la superficie del menú
    menu_surface.fill(BLACK)
    
    # Dibujar el fondo actual en la superficie del menú
    bg = backgrounds[current_bg]
    menu_surface.blit(bg, (0, 0))
    
    # Dibujar la porción visible del menú en la pantalla principal
    surface.blit(menu_surface, (0, 0), (camera_x, camera_y, WIDTH, HEIGHT))
    
    # Capa semitransparente para mejor legibilidad
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(180)
    surface.blit(overlay, (0, 0))
    
    # Marco dorado para el mensaje
    frame_width = 500
    frame_height = 300
    frame_x = WIDTH//2 - frame_width//2
    frame_y = HEIGHT//2 - frame_height//2
    
    # Dibujar marco con efecto dorado
    frame_bg = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
    pygame.draw.rect(frame_bg, (30, 30, 30, 220), (0, 0, frame_width, frame_height), border_radius=20)
    pygame.draw.rect(frame_bg, GOLD, (0, 0, frame_width, frame_height), 4, border_radius=20)
    
    # Efecto de brillo en el marco
    for i in range(3):
        glow_rect = pygame.Rect(-i*2, -i*2, frame_width + i*4, frame_height + i*4)
        pygame.draw.rect(frame_bg, (*GOLD, 30 - i*10), glow_rect, border_radius=20+i*2)
    
    surface.blit(frame_bg, (frame_x, frame_y))
    
    # Mensaje de éxito
    success_text = "¡HAS CONSEGUIDO LA ENTRADA AL NIVEL SECRETO!"
    success_lines = []
    
    # Dividir el texto si es muy largo
    words = success_text.split()
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        # Verificar ancho aproximado
        if len(test_line) > 30:  # Aproximadamente 30 caracteres por línea
            success_lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line
    if current_line:
        success_lines.append(current_line.strip())
    
    # Dibujar cada línea del mensaje
    for i, line in enumerate(success_lines):
        line_surface = subtitle_font.render(line, True, GREEN)
        surface.blit(line_surface, (WIDTH//2 - line_surface.get_width()//2, 
                                  frame_y + 70 + i * 40))
    
    # Pregunta
    question = "¿QUIERES CONTINUAR?"
    question_surface = menu_font.render(question, True, GOLD)
    surface.blit(question_surface, (WIDTH//2 - question_surface.get_width()//2, 
                                  frame_y + 160))
    
    # Botones de opción
    button_width = 140
    button_height = 50
    button_y = frame_y + 210
    
    # Botón NO
    no_color = RED
    no_bg = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    pygame.draw.rect(no_bg, (no_color[0]//4, no_color[1]//4, no_color[2]//4, 200), 
                    (0, 0, button_width, button_height), border_radius=10)
    pygame.draw.rect(no_bg, no_color, (0, 0, button_width, button_height), 2, border_radius=10)
    surface.blit(no_bg, (WIDTH//2 - button_width - 30, button_y))
    
    no_text = menu_font.render("NO", True, no_color)
    surface.blit(no_text, (WIDTH//2 - button_width - 30 + (button_width - no_text.get_width())//2, 
                         button_y + 10))
    
    # Botón SÍ
    yes_color = GREEN
    yes_bg = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    pygame.draw.rect(yes_bg, (yes_color[0]//4, yes_color[1]//4, yes_color[2]//4, 200), 
                    (0, 0, button_width, button_height), border_radius=10)
    pygame.draw.rect(yes_bg, yes_color, (0, 0, button_width, button_height), 2, border_radius=10)
    surface.blit(yes_bg, (WIDTH//2 + 30, button_y))
    
    yes_text = menu_font.render("SÍ", True, yes_color)
    surface.blit(yes_text, (WIDTH//2 + 30 + (button_width - yes_text.get_width())//2, 
                          button_y + 10))
    
    # Instrucciones
    instructions = info_font.render("Presiona S para SÍ • N para NO • ESC para cancelar", True, SILVER)
    surface.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT - 40))

# Función para verificar la clave secreta
def check_secret_code():
    global input_code, error_message, error_timer, current_state
    
    if input_code == secret_code:
        # Clave correcta
        print("¡Clave secreta correcta! Accediendo al nivel secreto...")
        trigger_flash(800, 200)
        current_state = STATE_SECRET_CONFIRM
        input_code = ""  # Limpiar el código
    else:
        # Clave incorrecta
        error_message = random.choice(error_phrases)
        error_timer = 2000  # Mostrar error por 2 segundos
        print(f"Clave incorrecta. Mostrando: {error_message}")
        
        # Efecto de flash rojo
        trigger_flash(300, 100)
        
        # Limpiar el código después de un error
        input_code = ""

# Función para dibujar pantalla de creadores con estilo clásico
def draw_creator_screen(surface, alpha, vista_index):
    vista = vistas[vista_index]
    
    # Fondo negro clásico
    surface.fill(BLACK)
    
    # Efecto de estrellas en el fondo (muy sutil)
    for i in range(20):
        x = (pygame.time.get_ticks() * 0.1 + i * 100) % WIDTH
        y = (i * 30 + pygame.time.get_ticks() * 0.05) % HEIGHT
        size = 1 + (i % 2)
        brightness = 100 + (i % 155)
        pygame.draw.circle(surface, (brightness, brightness, brightness), 
                         (int(x), int(y)), size)
    
    # Dibujar título (común para todas las vistas)
    if isinstance(vista["titulo"], list):
        # Título multilínea (para la universidad)
        for i, linea in enumerate(vista["titulo"]):
            titulo_text = title_font.render(linea, True, GOLD)
            titulo_text.set_alpha(alpha)
            
            # Efecto de brillo dorado en el título
            titulo_glow = title_font.render(linea, True, (255, 200, 0))
            titulo_glow.set_alpha(alpha // 2)
            
            # Dibujar línea centrada
            y_pos = 30 + i * 70  # Espacio entre líneas
            surface.blit(titulo_glow, (WIDTH//2 - titulo_glow.get_width()//2 + 2, y_pos + 2))
            surface.blit(titulo_text, (WIDTH//2 - titulo_text.get_width()//2, y_pos))
        
        # Línea decorativa simple (más abajo para acomodar las dos líneas)
        line_y = 160
    else:
        # Título de una sola línea (para las demás vistas)
        titulo_text = title_font.render(vista["titulo"], True, GOLD)
        titulo_text.set_alpha(alpha)
        
        # Efecto de brillo dorado en el título
        titulo_glow = title_font.render(vista["titulo"], True, (255, 200, 0))
        titulo_glow.set_alpha(alpha // 2)
        
        # Dibujar título centrado
        surface.blit(titulo_glow, (WIDTH//2 - titulo_glow.get_width()//2 + 2, 52))
        surface.blit(titulo_text, (WIDTH//2 - titulo_text.get_width()//2, 50))
        
        # Línea decorativa simple
        line_y = 130

    pygame.draw.line(surface, GOLD, (WIDTH//2 - 100, line_y), (WIDTH//2 + 100, line_y), 2)
    
    if "tipo" in vista and vista["tipo"] == "imagen":
        # Dibujar vista con imagen (empresa, director, universidad)
        try:
            imagen = load_image(vista["imagen"], 0.6)
            img_rect = imagen.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
            imagen.set_alpha(alpha)
            surface.blit(imagen, img_rect)
        except:
            # Si no se puede cargar la imagen, mostrar placeholder
            placeholder = pygame.Surface((300, 200))
            placeholder.fill((50, 50, 50))
            placeholder_text = info_font.render(vista["imagen"], True, WHITE)
            placeholder.blit(placeholder_text, (10, 10))
            placeholder.set_alpha(alpha)
            surface.blit(placeholder, (WIDTH//2 - 150, HEIGHT//2 - 50))
        
    else:
        # Dibujar vista con nombres de creadores
        # Dibujar nombres de integrantes
        for i, nombre in enumerate(vista["integrantes"]):
            y_pos = 180 + i * 80
            
            # Efecto de resplandor para cada nombre
            nombre_glow = subtitle_font.render(nombre, True, (50, 50, 100))
            nombre_glow.set_alpha(alpha // 3)
            surface.blit(nombre_glow, (WIDTH//2 - nombre_glow.get_width()//2 + 3, y_pos + 3))
            
            # Nombre principal
            nombre_text = subtitle_font.render(nombre, True, LIGHT_BLUE)
            nombre_text.set_alpha(alpha)
            surface.blit(nombre_text, (WIDTH//2 - nombre_text.get_width()//2, y_pos))
            
            # Efecto de partículas alrededor de los nombres
            if alpha > 200:  # Solo cuando está casi completamente visible
                for j in range(3):
                    part_x = WIDTH//2 - nombre_text.get_width()//2 - 20 + j * (nombre_text.get_width() + 40) / 2
                    part_y = y_pos + 25
                    part_size = 1 + (pygame.time.get_ticks() % 3)
                    part_alpha = min(alpha, 150 + (pygame.time.get_ticks() % 105))
                    pygame.draw.circle(surface, (100, 180, 255, part_alpha), 
                                     (int(part_x), int(part_y)), part_size)

# Función para dibujar texto multilínea centrado
def draw_multiline_text(surface, text, font, color, x, y, alpha=255):
    """Dibuja texto multilínea centrado en la posición x"""
    lines = text.split('\n')
    total_height = len(lines) * font.get_height()
    
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        line_surface.set_alpha(alpha)
        line_x = x - line_surface.get_width() // 2
        line_y = y - total_height // 2 + i * font.get_height()
        surface.blit(line_surface, (line_x, line_y))

# Función para dibujar pantalla de créditos - MEJORADA CON CENTRADO PERFECTO
def draw_credits_screen(surface, alpha):
    vista = creditos_vistas[current_credit_view]
    
    # Fondo negro clásico
    surface.fill(BLACK)
    
    # Efecto de estrellas en el fondo (muy sutil)
    for i in range(30):
        x = (pygame.time.get_ticks() * 0.1 + i * 70) % WIDTH
        y = (i * 25 + pygame.time.get_ticks() * 0.03) % HEIGHT
        size = 1 + (i % 3)
        brightness = 80 + (i % 175)
        pygame.draw.circle(surface, (brightness, brightness, brightness), 
                         (int(x), int(y)), size)
    
    if "tipo" in vista and vista["tipo"] == "autores":
        # Vista de autores de canciones (estilo imagen 2)
        titulo_text = title_font.render(vista["titulo"], True, GOLD)
        titulo_text.set_alpha(alpha)
        
        # Efecto de brillo dorado en el título
        titulo_glow = title_font.render(vista["titulo"], True, (255, 200, 0))
        titulo_glow.set_alpha(alpha // 2)
        
        # Dibujar título centrado
        surface.blit(titulo_glow, (WIDTH//2 - titulo_glow.get_width()//2 + 2, 52))
        surface.blit(titulo_text, (WIDTH//2 - titulo_text.get_width()//2, 50))
        
        # Línea decorativa simple
        line_y = 130
        pygame.draw.line(surface, GOLD, (WIDTH//2 - 150, line_y), (WIDTH//2 + 150, line_y), 2)
        
        # Dibujar nombres de autores
        for i, nombre in enumerate(vista["nombres"]):
            y_pos = 180 + i * 80
            
            # Efecto de resplandor para cada nombre
            nombre_glow = subtitle_font.render(nombre, True, (50, 50, 100))
            nombre_glow.set_alpha(alpha // 3)
            surface.blit(nombre_glow, (WIDTH//2 - nombre_glow.get_width()//2 + 3, y_pos + 3))
            
            # Nombre principal
            nombre_text = subtitle_font.render(nombre, True, LIGHT_BLUE)
            nombre_text.set_alpha(alpha)
            surface.blit(nombre_text, (WIDTH//2 - nombre_text.get_width()//2, y_pos))
    else:
        # Vista individual de creador con diseño alternante y centrado perfecto
        lado = vista["lado"]
        
        # Cargar imagen del creador (tamaño fijo para consistencia)
        imagen_creador = load_image(vista["imagen"], 0.7)  # Tamaño reducido para mejor ajuste
        imagen_creador.set_alpha(alpha)
        
        # Configurar posiciones según el lado
        if lado == "izquierda":
            # Texto a la izquierda, imagen a la derecha
            imagen_x = WIDTH - 350  # Imagen a la derecha
            texto_x = 150  # Texto a la izquierda (centrado verticalmente)
        else:  # derecha
            # Imagen a la izquierda, texto a la derecha
            imagen_x = 50  # Imagen a la izquierda
            texto_x = WIDTH - 300  # Texto a la derecha (centrado verticalmente)
        
        # Posición vertical centrada para ambos elementos
        centro_y = HEIGHT // 2
        imagen_y = centro_y - imagen_creador.get_height() // 2
        texto_y = centro_y
        
        # Dibujar imagen del creador
        surface.blit(imagen_creador, (imagen_x, imagen_y))
        
        # Dibujar nombre del creador (multilínea si es necesario)
        draw_multiline_text(surface, vista["nombre"], credits_name_font, GOLD, texto_x, texto_y - 30, alpha)
        
        # Dibujar rol del creador
        rol_text = credits_role_font.render(vista["rol"], True, LIGHT_BLUE)
        rol_text.set_alpha(alpha)
        surface.blit(rol_text, (texto_x - rol_text.get_width() // 2, texto_y + 40))
        
        # Línea decorativa
        line_width = 200
        pygame.draw.line(surface, GOLD, 
                        (texto_x - line_width // 2, texto_y + 80),
                        (texto_x + line_width // 2, texto_y + 80), 2)
    
    # Información de navegación
    if alpha > 200:  # Solo mostrar cuando esté completamente visible
        # Progreso de créditos
        progreso_text = info_font.render(f"Vista {current_credit_view + 1} de {len(creditos_vistas)}", True, CYAN)
        surface.blit(progreso_text, (WIDTH//2 - progreso_text.get_width()//2, HEIGHT - 80))
        
        # Instrucciones
        esc_text = info_font.render("Presiona ESC para volver al menú", True, SILVER)
        surface.blit(esc_text, (WIDTH//2 - esc_text.get_width()//2, HEIGHT - 50))
        
        # Instrucciones de navegación
        nav_text = info_font.render("Flechas ← → para navegar", True, SILVER)
        surface.blit(nav_text, (WIDTH//2 - nav_text.get_width()//2, HEIGHT - 30))

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
                    elif selected_option == 1:  # Clave Secreta (antes Opciones)
                        trigger_flash(600, 180)
                        current_state = STATE_SECRET_KEY
                        input_code = ""  # Limpiar código anterior
                        error_message = ""  # Limpiar mensajes de error
                        print("Accediendo a clave secreta...")
                    elif selected_option == 2:  # Créditos
                        trigger_flash(600, 180)
                        current_state = STATE_CREDITS
                        current_credit_view = 0
                        credit_timer = 0
                        fade_alpha = 0
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
        
        elif current_state == STATE_CREDITS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    trigger_flash(400, 150)
                    current_state = STATE_MAIN_MENU
                    print("Volviendo al menú principal desde créditos...")
                elif event.key == pygame.K_RIGHT:
                    # Avanzar manualmente a la siguiente vista
                    current_credit_view = (current_credit_view + 1) % len(creditos_vistas)
                    credit_timer = 0
                    fade_alpha = 0
                    print(f"Avanzando a crédito {current_credit_view + 1}")
                elif event.key == pygame.K_LEFT:
                    # Retroceder manualmente a la vista anterior
                    current_credit_view = (current_credit_view - 1) % len(creditos_vistas)
                    credit_timer = 0
                    fade_alpha = 0
                    print(f"Retrocediendo a crédito {current_credit_view + 1}")
        
        elif current_state == STATE_SECRET_KEY:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    trigger_flash(400, 150)
                    current_state = STATE_MAIN_MENU
                    input_code = ""
                    error_message = ""
                    print("Volviendo al menú principal desde clave secreta...")
                elif event.key == pygame.K_RETURN:
                    # Intentar verificar el código
                    check_secret_code()
                elif event.key == pygame.K_BACKSPACE:
                    # Borrar el último carácter
                    if input_code:
                        input_code = input_code[:-1]
                elif event.key in [pygame.K_0, pygame.K_KP0]:
                    if len(input_code) < 4:
                        input_code += "0"
                elif event.key in [pygame.K_1, pygame.K_KP1]:
                    if len(input_code) < 4:
                        input_code += "1"
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    if len(input_code) < 4:
                        input_code += "2"
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    if len(input_code) < 4:
                        input_code += "3"
                elif event.key in [pygame.K_4, pygame.K_KP4]:
                    if len(input_code) < 4:
                        input_code += "4"
                elif event.key in [pygame.K_5, pygame.K_KP5]:
                    if len(input_code) < 4:
                        input_code += "5"
                elif event.key in [pygame.K_6, pygame.K_KP6]:
                    if len(input_code) < 4:
                        input_code += "6"
                elif event.key in [pygame.K_7, pygame.K_KP7]:
                    if len(input_code) < 4:
                        input_code += "7"
                elif event.key in [pygame.K_8, pygame.K_KP8]:
                    if len(input_code) < 4:
                        input_code += "8"
                elif event.key in [pygame.K_9, pygame.K_KP9]:
                    if len(input_code) < 4:
                        input_code += "9"
        
        elif current_state == STATE_SECRET_CONFIRM:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Volver al menú principal
                    trigger_flash(400, 150)
                    current_state = STATE_MAIN_MENU
                    print("Cancelando nivel secreto...")
                elif event.key == pygame.K_s or event.key == pygame.K_y:
                    # Sí - Ejecutar nivel secreto
                    trigger_flash(800, 200)
                    print("🚀 Ejecutando nivel secreto...")
                    
                    # Ejecutar el nivel secreto
                    nivel_ejecutado = ejecutar_nivel_secreto()
                    
                    if nivel_ejecutado:
                        print("✅ Regresando del nivel secreto")
                        trigger_flash(300, 100)
                    
                    # Volver al menú principal después de ejecutar
                    current_state = STATE_MAIN_MENU
                elif event.key == pygame.K_n:
                    # No - Volver al menú principal
                    trigger_flash(400, 150)
                    current_state = STATE_MAIN_MENU
                    print("Nivel secreto cancelado...")
    
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
            current_state = STATE_CREATOR_1
            transition_timer = 0
            fade_alpha = 0
            fade_direction = 1
    
    elif current_state in [STATE_CREATOR_1, STATE_CREATOR_2, STATE_LOGO, STATE_DIRECTOR, STATE_UNIVERSITY]:
        transition_timer += dt
        
        # Determinar el tiempo total según el estado actual
        if current_state == STATE_CREATOR_1:
            total_time = FADE_TIME_CREATOR_1
        elif current_state == STATE_CREATOR_2:
            total_time = FADE_TIME_CREATOR_2
        elif current_state == STATE_LOGO:
            total_time = FADE_TIME_LOGO
        elif current_state == STATE_DIRECTOR:
            total_time = FADE_TIME_DIRECTOR
        elif current_state == STATE_UNIVERSITY:
            total_time = FADE_TIME_UNIVERSITY
        
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
            if current_state == STATE_CREATOR_1:
                current_state = STATE_CREATOR_2
                print("Mostrando equipo 2...")
            elif current_state == STATE_CREATOR_2:
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
    
    elif current_state == STATE_CREDITS:
        credit_timer += dt
        
        # Controlar efecto de fade (aparecer y desaparecer cada 5 segundos)
        half_time = CREDITS_TIME / 2
        
        if credit_timer < half_time:
            # Fade-in durante la primera mitad del tiempo
            fade_alpha = min(255, (credit_timer / half_time) * 255)
        else:
            # Fade-out durante la segunda mitad del tiempo
            fade_alpha = max(0, 255 - ((credit_timer - half_time) / half_time) * 255)
        
        # Cambiar a la siguiente vista cuando se complete el tiempo
        if credit_timer >= CREDITS_TIME:
            current_credit_view = (current_credit_view + 1) % len(creditos_vistas)
            credit_timer = 0
            fade_alpha = 0
            print(f"Mostrando crédito {current_credit_view + 1}/{len(creditos_vistas)}")
    
    elif current_state in [STATE_MAIN_MENU, STATE_LEVEL_SELECT, STATE_SECRET_KEY, STATE_SECRET_CONFIRM]:
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
    
    # Actualizar temporizador de mensaje de error
    if error_timer > 0:
        error_timer -= dt
        if error_timer <= 0:
            error_message = ""
    
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
    
    elif current_state == STATE_CREATOR_1:
        draw_creator_screen(screen, int(fade_alpha), 0)
    
    elif current_state == STATE_CREATOR_2:
        draw_creator_screen(screen, int(fade_alpha), 1)
    
    elif current_state == STATE_LOGO:
        draw_creator_screen(screen, int(fade_alpha), 2)
    
    elif current_state == STATE_DIRECTOR:
        draw_creator_screen(screen, int(fade_alpha), 3)
    
    elif current_state == STATE_UNIVERSITY:
        draw_creator_screen(screen, int(fade_alpha), 4)
    
    elif current_state == STATE_CREDITS:
        draw_credits_screen(screen, int(fade_alpha))
    
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
        title_text = "BIT HUNTER"
        
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
    
    elif current_state == STATE_SECRET_KEY:
        # Dibujar pantalla de clave secreta
        draw_secret_key_screen(screen)
    
    elif current_state == STATE_SECRET_CONFIRM:
        # Dibujar pantalla de confirmación de nivel secreto
        draw_secret_confirm_screen(screen)
    
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