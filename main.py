import pygame
import sys
from jugador import Jugador
from proyectiles import GestorProyectiles
from gestor_enemigos import GestorEnemigos
pygame.init()

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Defensa del Hormiguero - EID")

reloj = pygame.time.Clock()

# Carga segura del fondo
try:
    fondo_original = pygame.image.load("assets/fondo1.jpg").convert()
    imagen_fondo = pygame.transform.scale(fondo_original, (ANCHO_PANTALLA, ALTO_PANTALLA))
except (pygame.error, FileNotFoundError):
    imagen_fondo = None
COLOR_ARENA = (225, 206, 154)
fuente = pygame.font.SysFont("Arial", 24)
fuente_grande = pygame.font.SysFont("Arial", 48)

hormiga = Jugador(
    x=ANCHO_PANTALLA // 2 - 25,
    y=ALTO_PANTALLA // 2 - 25,
    ancho=50,
    alto=50,
    velocidad=5,
    ancho_pantalla=ANCHO_PANTALLA,
    alto_pantalla=ALTO_PANTALLA
)

gestor_proyectiles = GestorProyectiles(ANCHO_PANTALLA, ALTO_PANTALLA)
gestor_enemigos = GestorEnemigos(ANCHO_PANTALLA, ALTO_PANTALLA)


ejecutando = True
juego_ganado = False
juego_perdido = False
fase_actual = 1

gestor_enemigos.configurar_fase(fase_actual)

boton_reiniciar = pygame.Rect(ANCHO_PANTALLA - 160, 20, 140, 35)

while ejecutando:
    reloj.tick(60)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_h:
                hormiga.recibir_daño(15)
            if evento.key == pygame.K_j:
                gestor_proyectiles.disparar_parabolico(hormiga.rect.centerx, hormiga.rect.top, direccion=1)
            if evento.key == pygame.K_l:
                gestor_proyectiles.disparar_parabolico(hormiga.rect.centerx, hormiga.rect.top, direccion=-1)
            if evento.key == pygame.K_k:
                gestor_proyectiles.disparar_conico(hormiga.rect.centerx, hormiga.rect.top)
            
            if (juego_ganado or juego_perdido) and evento.key in (pygame.K_r, pygame.K_RETURN):
                fase_actual = 1
                juego_ganado = False
                juego_perdido = False
                hormiga.vida = 100
                gestor_proyectiles.proyectiles.clear()
                gestor_enemigos.configurar_fase(fase_actual)

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos_mouse = pygame.mouse.get_pos()
            if boton_reiniciar.collidepoint(pos_mouse):
                fase_actual = 1
                juego_ganado = False
                juego_perdido = False
                hormiga.vida = 100
                gestor_proyectiles.proyectiles.clear()
                gestor_enemigos.configurar_fase(fase_actual)

    if not juego_ganado and not juego_perdido:
        teclas = pygame.key.get_pressed()
        hormiga.mover(teclas)
        
        if teclas[pygame.K_SPACE]:
            gestor_proyectiles.disparar_basico(hormiga.rect.centerx, hormiga.rect.top)

        gestor_proyectiles.actualizar()
        gestor_enemigos.actualizar()
        
        gestor_enemigos.verificar_colisiones(gestor_proyectiles)

        for pe in gestor_enemigos.proyectiles_enemigos:
            if pe.activo and hormiga.rect.colliderect(pe.rect):
                hormiga.recibir_daño(pe.danio)
                pe.activo = False

        if hormiga.vida <= 0:
            juego_perdido = True

        if len(gestor_enemigos.enemigos) == 0:
            if fase_actual < 4:
                fase_actual += 1
                gestor_enemigos.configurar_fase(fase_actual)
            elif fase_actual == 4:
                juego_ganado = True

    if imagen_fondo is not None:
        pantalla.blit(imagen_fondo, (0, 0))
    else:
        pantalla.fill(COLOR_ARENA)

    hormiga.dibujar(pantalla)
    gestor_proyectiles.dibujar(pantalla)
    gestor_enemigos.dibujar(pantalla)

    texto_fase = fuente.render(f"Fase: {fase_actual} / 4", True, (50, 50, 50))
    pantalla.blit(texto_fase, (20, 20))

    texto_vida = fuente.render(f"HP: {max(0, hormiga.vida)}", True, (150, 0, 0))
    pantalla.blit(texto_vida, (20, 55))

    pygame.draw.rect(pantalla, (100, 150, 100), boton_reiniciar, border_radius=5)
    pygame.draw.rect(pantalla, (50, 80, 50), boton_reiniciar, 2, border_radius=5)
    texto_boton = fuente.render("Reiniciar", True, (255, 255, 255))
    pantalla.blit(texto_boton, (boton_reiniciar.x + 25, boton_reiniciar.y + 5))

    if juego_perdido:
        s = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        s.set_alpha(190)
        s.fill((0, 0, 0))
        pantalla.blit(s, (0, 0))

        texto_go = fuente_grande.render("¡GAME OVER!", True, (220, 50, 50))
        texto_sub = fuente.render("Tu hormiga ha caído en combate", True, (255, 255, 255))
        texto_inst = fuente.render("Presiona R o el botón para Reintentar", True, (200, 200, 200))
        
        pantalla.blit(texto_go, (ANCHO_PANTALLA // 2 - texto_go.get_width() // 2, 200))
        pantalla.blit(texto_sub, (ANCHO_PANTALLA // 2 - texto_sub.get_width() // 2, 280))
        pantalla.blit(texto_inst, (ANCHO_PANTALLA // 2 - texto_inst.get_width() // 2, 330))

    if juego_ganado:
        s = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        s.set_alpha(180)
        s.fill((0, 0, 0))
        pantalla.blit(s, (0, 0))

        texto_vic = fuente_grande.render("¡VICTORIA!", True, (255, 215, 0))
        texto_sub = fuente.render("Has derrotado a la Mantis y defendido el hormiguero!", True, (255, 255, 255))
        texto_inst = fuente.render("Presiona R o el botón para Jugar de Nuevo", True, (200, 200, 200))
        
        pantalla.blit(texto_vic, (ANCHO_PANTALLA // 2 - texto_vic.get_width() // 2, 200))
        pantalla.blit(texto_sub, (ANCHO_PANTALLA // 2 - texto_sub.get_width() // 2, 280))
        pantalla.blit(texto_inst, (ANCHO_PANTALLA // 2 - texto_inst.get_width() // 2, 330))

    pygame.display.flip()
    
pygame.quit()
sys.exit()