import pygame
import sys
from jugador import Jugador

pygame.init()

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Defensa del Hormiguero - Test Jugador")

reloj = pygame.time.Clock()

hormiga = Jugador(
    x=ANCHO_PANTALLA // 2 - 25,
    y=ALTO_PANTALLA // 2 - 25,
    ancho=50,
    alto=50,
    velocidad=5,
    ancho_pantalla=ANCHO_PANTALLA,
    alto_pantalla=ALTO_PANTALLA
)

COLOR_ARENA = (225, 206, 154)

ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_h:
                hormiga.recibir_daño(15)

    teclas = pygame.key.get_pressed()
    
    hormiga.mover(teclas)
    
    if teclas[pygame.K_SPACE]:
        hormiga.disparar()

    hormiga.actualizar_balas()
    pantalla.fill(COLOR_ARENA)  
    
    hormiga.dibujar(pantalla)
    pygame.display.flip()
    reloj.tick(60)
    
pygame.quit()
sys.exit()
