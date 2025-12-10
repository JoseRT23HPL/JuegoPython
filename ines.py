import pygame
import cv2
import numpy as np
import sys
import os
import subprocess
from pygame.locals import *

# --- Configuración inicial ---
WIDTH, HEIGHT = 960, 540
FPS = 60

class Introduccion:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene_index = 0
        self.transition_alpha = 0  # Para transición suave
        
        # Inicializar mixer para música
        pygame.mixer.init()
        
        # Textos para la escena
        self.textos = [
            "Felicidades Rescataste a Ines",
            "Muchas gracias por averme liberado\nestoy tan agradecida contigo",
            "Vamonos de aqui, conozco la salida"
        ]
        
        # Configuración de la escena - Video a la izquierda, texto a la derecha
        self.scenes = [
            {
                "video": "video/Laynes.mp4",  # Cambia esto por tu video
                "layout": "vertical_left_full",
                "video_rect": pygame.Rect(20, 20, 460, HEIGHT-40),
                "text_rect": pygame.Rect(500, 20, WIDTH-520, HEIGHT-40)
            }
        ]
        
        # Fuente para el texto
        try:
            self.font = pygame.font.Font(None, 32)
            self.title_font = pygame.font.Font(None, 40)
            self.large_font = pygame.font.Font(None, 48)
        except:
            # Fallback si no se puede cargar la fuente
            self.font = pygame.font.SysFont('arial', 32)
            self.title_font = pygame.font.SysFont('arial', 40)
            self.large_font = pygame.font.SysFont('arial', 48)
        
        # Colores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BG_COLOR = self.BLACK
        self.TEXT_BG = (20, 20, 30, 230)
        self.BORDER_COLOR = (50, 150, 255)
        
        # Color especial para Ines
        self.INES_COLOR = (255, 105, 180)  # Rosa para Ines
        
        # Capturas de video de OpenCV
        self.video_captures = []
        self.current_video_frames = []
        self.video_timers = []
        
        # Variables para controlar el texto actual
        self.current_text_index = 0
        
        # Cargar videos con OpenCV
        self.cargar_videos_cv2()
        
        # Cargar música de fondo
        self.cargar_musica()
        
        # Instrucción para continuar
        self.continue_text = self.font.render("Presiona X para continuar", True, (255, 215, 0))
        
        # Tiempo para controlar FPS del video
        self.last_frame_time = pygame.time.get_ticks()
        self.video_frame_delay = 1000 // 30  # 30 FPS para video
        
        # Para la transición final
        self.transition_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.transition_speed = 5
        self.transition_active = False
        self.transition_direction = "out"  # "in" o "out"
        
    def cargar_musica(self):
        """Carga y reproduce música de fondo"""
        try:
            # Intentar cargar archivo de música
            music_files = ["musica/intro.mp3", "musica/fondo.mp3", "sound/vic.mp3"]
            
            for music_file in music_files:
                if os.path.exists(music_file):
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    print(f"Música cargada: {music_file}")
                    return
            
            print("Advertencia: No se encontró archivo de música. Continuando sin música.")
            
        except Exception as e:
            print(f"Error cargando música: {e}")
    
    def cargar_videos_cv2(self):
        """Carga los videos usando OpenCV"""
        for i, scene in enumerate(self.scenes):
            video_path = scene["video"]
            
            # Verificar si el archivo existe
            if not os.path.exists(video_path):
                print(f"Advertencia: No se encontró el video {video_path}")
                self.crear_frame_error(scene["video_rect"].size, i)
                self.video_captures.append(None)
                continue
            
            try:
                # Abrir video con OpenCV
                cap = cv2.VideoCapture(video_path)
                if cap.isOpened():
                    self.video_captures.append(cap)
                    # Leer primer frame
                    ret, frame = cap.read()
                    if ret:
                        # Convertir BGR de OpenCV a RGB para PyGame
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        # Redimensionar al tamaño del rectángulo
                        frame_resized = cv2.resize(frame_rgb, scene["video_rect"].size)
                        self.current_video_frames.append(frame_resized)
                        self.video_timers.append(0)
                    else:
                        self.crear_frame_error(scene["video_rect"].size, i)
                else:
                    self.crear_frame_error(scene["video_rect"].size, i)
                    
            except Exception as e:
                print(f"Error cargando video {video_path}: {e}")
                self.crear_frame_error(scene["video_rect"].size, i)
                self.video_captures.append(None)
    
    def crear_frame_error(self, size, scene_index):
        """Crea un frame de error cuando no se puede cargar el video"""
        width, height = size
        error_frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Color de fondo
        color = (80, 30, 80)  # Púrpura oscuro para Ines
        error_frame[:] = color
        
        # Añadir texto de error
        font = cv2.FONT_HERSHEY_SIMPLEX
        video_name = os.path.basename(self.scenes[scene_index]['video'])
        text = f"Video: {video_name}"
        text_size = cv2.getTextSize(text, font, 0.5, 1)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2
        
        cv2.putText(error_frame, text, (text_x, text_y), font, 0.5, (255, 255, 255), 1)
        cv2.putText(error_frame, "No encontrado", (text_x-20, text_y+30), font, 0.4, (200, 200, 200), 1)
        
        self.current_video_frames.append(error_frame)
        self.video_timers.append(0)
    
    def update_video_frame(self, scene_index):
        """Actualiza el frame del video actual"""
        current_time = pygame.time.get_ticks()
        
        # Actualizar frame si ha pasado el tiempo suficiente
        if current_time - self.video_timers[scene_index] > self.video_frame_delay:
            self.video_timers[scene_index] = current_time
            
            cap = self.video_captures[scene_index]
            if cap is not None and cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    # Convertir BGR a RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # Redimensionar al tamaño del rectángulo
                    scene = self.scenes[scene_index]
                    frame_resized = cv2.resize(frame_rgb, scene["video_rect"].size)
                    self.current_video_frames[scene_index] = frame_resized
                else:
                    # Reiniciar video cuando termina
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = cap.read()
                    if ret:
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        scene = self.scenes[scene_index]
                        frame_resized = cv2.resize(frame_rgb, scene["video_rect"].size)
                        self.current_video_frames[scene_index] = frame_resized
    
    def iniciar_transicion(self):
        """Inicia la transición para cambiar al nivel 1"""
        self.transition_active = True
        self.transition_direction = "out"
        self.transition_alpha = 0
    
    def actualizar_transicion(self):
        """Actualiza la transición"""
        if not self.transition_active:
            return False
        
        if self.transition_direction == "out":
            self.transition_alpha += self.transition_speed
            if self.transition_alpha >= 255:
                self.transition_alpha = 255
                self.transition_direction = "in"
                return True
        else:
            # Aquí podrías añadir más lógica si necesitas
            pass
        
        return False
    
    def dibujar_transicion(self):
        """Dibuja la transición"""
        if self.transition_active:
            self.transition_surface.fill((0, 0, 0, self.transition_alpha))
            self.screen.blit(self.transition_surface, (0, 0))
            
            # Dibujar texto "CARGANDO NIVEL 1..."
            if self.transition_alpha >= 150:
                loading_text = self.large_font.render("CARGANDO NIVEL 6...", True, (255, 215, 0))
                loading_rect = loading_text.get_rect(center=(WIDTH//2, HEIGHT//2))
                self.screen.blit(loading_text, loading_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.cleanup()
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
                if event.key == K_x and not self.transition_active:
                    # Avanzar al siguiente texto o iniciar transición
                    self.current_text_index += 1
                    if self.current_text_index >= len(self.textos):
                        # Iniciar transición al terminar todos los textos
                        self.iniciar_transicion()
                        return None
                
                # Opcional: tecla ESC para saltar
                if event.key == K_ESCAPE and not self.transition_active:
                    self.iniciar_transicion()
                    return None
                
                # Opcional: Espacio para pausar/reanudar música
                if event.key == K_SPACE:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
        
        return None
    
    def draw_text_box(self, text, rect, scene_index):
        """Dibuja un cuadro de texto con fondo semitransparente"""
        # Crear superficie semitransparente
        text_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        text_surface.fill(self.TEXT_BG)
        
        # Renderizar el texto actual
        rendered_text = self.font.render(text, True, self.WHITE)
        
        # Centrar el texto en el cuadro
        text_rect = rendered_text.get_rect(center=(rect.width//2, rect.height//2))
        
        # Dibujar el texto
        text_surface.blit(rendered_text, text_rect)
        
        # Dibujar borde con color especial para Ines
        border_color = self.INES_COLOR
            
        pygame.draw.rect(text_surface, border_color, text_surface.get_rect(), 3)
        
        # Esquinas decorativas
        corner_size = 15
        corners = [
            (0, 0), (rect.width - corner_size, 0),
            (0, rect.height - corner_size), (rect.width - corner_size, rect.height - corner_size)
        ]
        
        for x, y in corners:
            pygame.draw.rect(text_surface, border_color, (x, y, corner_size, corner_size), 2)
        
        return text_surface
    
    def clamp_color_value(self, value):
        """Asegura que un valor de color esté en el rango [0, 255]"""
        return max(0, min(255, int(value)))
    
    def get_brighter_color(self, color):
        """Devuelve una versión más brillante del color, asegurando que esté en rango"""
        if len(color) == 3:
            r, g, b = color
            # Aumentar brillo pero asegurarse de no exceder 255
            return (
                self.clamp_color_value(r + 50),
                self.clamp_color_value(g + 50),
                self.clamp_color_value(b + 50)
            )
        elif len(color) == 4:
            r, g, b, a = color
            # Aumentar brillo pero asegurarse de no exceder 255
            return (
                self.clamp_color_value(r + 50),
                self.clamp_color_value(g + 50),
                self.clamp_color_value(b + 50),
                a
            )
        return color
    
    def draw(self):
        """Dibuja toda la escena actual"""
        # Fondo negro
        self.screen.fill(self.BG_COLOR)
        
        # Verificar que scene_index sea válido
        if self.scene_index >= len(self.scenes):
            return
        
        # Obtener la escena actual
        scene = self.scenes[self.scene_index]
        
        # Actualizar y dibujar video
        if self.scene_index < len(self.current_video_frames):
            self.update_video_frame(self.scene_index)
            
            # Convertir frame de numpy array a superficie de PyGame
            frame = self.current_video_frames[self.scene_index]
            if frame is not None:
                try:
                    # Transponer las dimensiones para PyGame
                    if frame.shape[0] > 0 and frame.shape[1] > 0:
                        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                        
                        # Dibujar el video
                        self.screen.blit(frame_surface, scene["video_rect"])
                        
                        # Dibujar borde alrededor del video
                        border_color = self.INES_COLOR
                        
                        pygame.draw.rect(self.screen, border_color, scene["video_rect"], 3)
                        
                        # Efecto de brillo en las esquinas
                        corner_size = 15
                        corners = [
                            (scene["video_rect"].left, scene["video_rect"].top),
                            (scene["video_rect"].right - corner_size, scene["video_rect"].top),
                            (scene["video_rect"].left, scene["video_rect"].bottom - corner_size),
                            (scene["video_rect"].right - corner_size, scene["video_rect"].bottom - corner_size)
                        ]
                        
                        brighter_color = self.get_brighter_color(border_color)
                        
                        for x, y in corners:
                            pygame.draw.rect(self.screen, brighter_color, 
                                           (x, y, corner_size, corner_size), 2)
                        
                except Exception as e:
                    print(f"Error dibujando video: {e}")
        
        # Dibujar cuadro de texto con el texto actual
        if self.current_text_index < len(self.textos):
            text_box = self.draw_text_box(self.textos[self.current_text_index], scene["text_rect"], self.scene_index)
            self.screen.blit(text_box, scene["text_rect"])
        
        # Dibujar indicador para continuar con efecto de parpadeo
        if not self.transition_active:
            current_time = pygame.time.get_ticks()
            if (current_time // 500) % 2 == 0:  # Parpadeo cada 500ms
                # Continuar en esquina inferior derecha
                continue_rect = self.continue_text.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))
                self.screen.blit(self.continue_text, continue_rect)
        
        # Mostrar progreso de texto
        progress_text = self.font.render(f"Texto {self.current_text_index + 1}/{len(self.textos)}", True, self.INES_COLOR)
        progress_rect = progress_text.get_rect(topright=(WIDTH - 20, 20))
        self.screen.blit(progress_text, progress_rect)
        
        # Indicador de música
        music_text = self.font.render("Espacio: Pausa/Música", True, (150, 150, 150))
        music_rect = music_text.get_rect(bottomleft=(20, HEIGHT - 20))
        self.screen.blit(music_text, music_rect)
        
        # Indicador de salto
        skip_text = self.font.render("ESC: Saltar", True, (150, 150, 150))
        skip_rect = skip_text.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))
        self.screen.blit(skip_text, skip_rect)
    
    def ejecutar_nivel1(self):
        """Ejecuta el archivo nivel1.py"""
        try:
            print("Cerrando escena y abriendo nivel6.py...")
            
            # Determinar el comando según el sistema operativo
            python_cmd = sys.executable  # Usa el mismo intérprete de Python
            
            # Asegurarse de que nivel1.py existe
            if not os.path.exists("nivel6.py"):
                print("Error: nivel1.py no encontrado")
                # Crear un archivo de ejemplo si no existe
                with open("nivel6.py", "w") as f:
                    f.write("print('Nivel 6 cargado - Este es un archivo de ejemplo')\n")
                print("Archivo nivel6.py creado como ejemplo")
            
            # Limpiar recursos antes de salir
            self.cleanup()
            pygame.quit()
            
            # Ejecutar nivel1.py
            subprocess.run([python_cmd, "nivel6.py"])
            
            # Salir del programa actual
            sys.exit(0)
            
        except Exception as e:
            print(f"Error ejecutando nivel6.py: {e}")
            import traceback
            traceback.print_exc()
            input("Presiona Enter para salir...")
            sys.exit(1)
    
    def run(self):
        """Bucle principal de la escena"""
        while self.running:
            # Manejar eventos
            next_state = self.handle_events()
            
            # Actualizar transición si está activa
            if self.transition_active:
                transicion_completa = self.actualizar_transicion()
                if transicion_completa:
                    # Cuando la transición está completa, ejecutar nivel1.py
                    self.ejecutar_nivel1()
                    return
            
            # Dibujar
            self.draw()
            
            # Dibujar transición si está activa
            self.dibujar_transicion()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        self.cleanup()
    
    def cleanup(self):
        """Liberar recursos de los videos y música"""
        # Detener música
        pygame.mixer.music.stop()
        
        # Liberar videos de OpenCV
        for cap in self.video_captures:
            if cap is not None:
                cap.release()
        
        # Cerrar ventanas de OpenCV si hay alguna abierta
        try:
            cv2.destroyAllWindows()
        except:
            pass


# Punto de entrada principal
if __name__ == "__main__":
    def main():
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rescate de Ines - Bit Hunter")
        
        try:
            intro = Introduccion(screen)
            intro.run()
        except KeyboardInterrupt:
            print("\nInterrumpido por el usuario")
        except Exception as e:
            print(f"Error ejecutando la escena: {e}")
            import traceback
            traceback.print_exc()
            input("Presiona Enter para salir...")
        finally:
            # Asegurarse de que PyGame se cierre correctamente
            pygame.quit()
    
    # Ejecutar el programa principal
    main()