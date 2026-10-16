import pygame

class Bala:
    def __init__(self, x, y):
        self.ancho = 6
        self.alto = 12
        self.rect = pygame.Rect(x - self.ancho // 2, y, self.ancho, self.alto)
        self.velocidad = 8
        self.color = (0, 0, 0)

    def mover(self):
        self.rect.y -= self.velocidad

    def dibujar(self, superficie):
        pygame.draw.ellipse(superficie, self.color, self.rect)


class Jugador:
    def __init__(self, x, y, ancho, alto, velocidad, ancho_pantalla, alto_pantalla):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.velocidad = velocidad
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.vida_maxima = 100
        self.vida = 100
        self.balas = []
        self.ultimo_disparo = 0
        self.cooldown_disparo = 250 


        imagen_original = pygame.image.load('assets/hormiga.png').convert_alpha()
        self.imagen = pygame.transform.scale(imagen_original, (ancho, alto))

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidad

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self.ancho_pantalla, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(self.alto_pantalla, self.rect.bottom)

    def disparar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo >= self.cooldown_disparo:
          
            nueva_bala = Bala(self.rect.centerx, self.rect.top)
            self.balas.append(nueva_bala)
            self.ultimo_disparo = tiempo_actual

    def actualizar_balas(self):
        for bala in self.balas[:]:
            bala.mover()
            if bala.rect.bottom < 0:
                self.balas.remove(bala)

    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    def dibujar_barra_vida(self, superficie):
        ancho_barra = self.rect.width
        alto_barra = 6
        x = self.rect.x
        y = self.rect.y - 10  

        porcentaje_vida = self.vida / self.vida_maxima
        ancho_actual = int(ancho_barra * porcentaje_vida)

        pygame.draw.rect(superficie, (200, 0, 0), (x, y, ancho_barra, alto_barra))
        if ancho_actual > 0:
            pygame.draw.rect(superficie, (0, 220, 0), (x, y, ancho_actual, alto_barra))


    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)
        self.dibujar_barra_vida(superficie)
        for bala in self.balas:
            bala.dibujar(superficie)