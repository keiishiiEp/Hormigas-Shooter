import math
import random
import pygame

class ProyectilEnemigo:
    def __init__(self, x, y, dx, dy):
        self.x = float(x)
        self.y = float(y)
        self.vx = dx
        self.vy = dy
        self.radio = 5
        self.danio = 10
        self.activo = True
        self.rect = pygame.Rect(int(self.x - self.radio), int(self.y - self.radio), self.radio * 2, self.radio * 2)

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x - self.radio)
        self.rect.y = int(self.y - self.radio)

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, (200, 50, 50), (int(self.x), int(self.y)), self.radio)


class Enemigo:
    def __init__(self, tipo, carril_base_y, ancho_pantalla, lado="derecha"):
            self.tipo = tipo
            self.carril_base = carril_base_y
            self.ancho_pantalla = ancho_pantalla
            self.lado = lado
            
            if tipo == "pulgon":
                self.vida_maxima = 15
                self.amplitud, self.frecuencia, self.velocidad_x = 25, 0.04, 2.5
                self.ancho, self.alto = 30, 20
                self.nombre_archivo = "assets/pulgon.png"
            elif tipo == "escarabajo":
                self.vida_maxima = 40
                self.amplitud, self.frecuencia, self.velocidad_x = 50, 0.08, 2.0
                self.ancho, self.alto = 40, 40
                self.nombre_archivo = "assets/escarabajo.png"
            elif tipo == "arana":
                self.vida_maxima = 60
                self.amplitud, self.frecuencia, self.velocidad_x = 15, 0.15, 3.0
                self.ancho, self.alto = 35, 35
                self.nombre_archivo = "assets/araña.webp"
            elif tipo == "jefe":
                self.vida_maxima = 300
                self.amplitud, self.frecuencia, self.velocidad_x = 80, 0.02, 1.0
                self.ancho, self.alto = 90, 100
                self.nombre_archivo = "assets/mantis.png"

            self.vida = self.vida_maxima

            self.imagen = None
            try:
                img_cargada = pygame.image.load(self.nombre_archivo).convert_alpha()
                self.imagen = pygame.transform.scale(img_cargada, (self.ancho, self.alto))
            except (pygame.error, FileNotFoundError):
                self.imagen = None

            self.descendiendo = False
            if lado == "superior":
                self.x = float(ancho_pantalla // 2 - self.ancho // 2)
                self.y = float(-self.alto - 10)
                self.direccion = 1
                self.descendiendo = True
                self.velocidad_descenso = 3.0
            elif lado == "derecha":
                self.x = float(ancho_pantalla - self.ancho - 30)
                self.y = float(carril_base_y)
                self.direccion = 1
            else:
                self.x = float(30)
                self.y = float(carril_base_y)
                self.direccion = -1

            self.rect = pygame.Rect(int(self.x), int(self.y), self.ancho, self.alto)
            self.temporizador_disparo = 0
            self.frecuencia_disparo = random.randint(120, 200)
    def actualizar(self):
        if self.descendiendo:
            self.y += self.velocidad_descenso
            if self.y >= self.carril_base:
                self.y = float(self.carril_base)
                self.descendiendo = False
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
            return

        self.x -= self.velocidad_x * self.direccion
        
        if self.x <= 0:
            self.x = 0
            self.direccion = -1
        elif self.x >= self.ancho_pantalla - self.ancho:
            self.x = self.ancho_pantalla - self.ancho
            self.direccion = 1

        self.y = self.carril_base + self.amplitud * math.sin(self.frecuencia * self.x)
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def intentar_atacar(self, lista_proyectiles_enemigos):
        self.temporizador_disparo += 1
        if self.temporizador_disparo >= self.frecuencia_disparo:
            self.temporizador_disparo = 0
            self.frecuencia_disparo = random.randint(120, 200)
            
            dx_base = -1 if self.direccion == 1 else 1
            
            if self.tipo == "pulgon":
                lista_proyectiles_enemigos.append(ProyectilEnemigo(self.rect.centerx, self.rect.bottom, dx=0, dy=2.5))
            elif self.tipo == "escarabajo":
                lista_proyectiles_enemigos.append(ProyectilEnemigo(self.rect.centerx, self.rect.bottom, dx=dx_base * 1, dy=2))
            elif self.tipo == "arana":
                lista_proyectiles_enemigos.append(ProyectilEnemigo(self.rect.centerx, self.rect.bottom, dx=dx_base * 2, dy=1))
            elif self.tipo == "jefe":
                lista_proyectiles_enemigos.append(ProyectilEnemigo(self.rect.centerx, self.rect.bottom, dx=-2, dy=2))
                lista_proyectiles_enemigos.append(ProyectilEnemigo(self.rect.centerx, self.rect.bottom, dx=0, dy=2.5))
                lista_proyectiles_enemigos.append(ProyectilEnemigo(self.rect.centerx, self.rect.bottom, dx=2, dy=2))

    def recibir_impacto(self, proyectil):
        multiplicador = 1.0
        tipo_proyectil = "basico"
        if hasattr(proyectil, 'g'):
            tipo_proyectil = "parabolico"
        elif hasattr(proyectil, 'radio_giro'):
            tipo_proyectil = "conico"

        if self.tipo == "pulgon":
            if tipo_proyectil == "basico": multiplicador = 3.0
            elif tipo_proyectil == "conico": multiplicador = 0.5
        elif self.tipo == "escarabajo":
            if tipo_proyectil == "parabolico": multiplicador = 2.0
            elif tipo_proyectil == "basico": multiplicador = 0.5
        elif self.tipo == "arana":
            if tipo_proyectil == "conico": multiplicador = 3.0
            elif tipo_proyectil == "parabolico": multiplicador = 0.5
        elif self.tipo == "jefe":
            if tipo_proyectil in ["parabolico", "conico"]: multiplicador = 2.0

        daño_final = int(proyectil.danio * multiplicador)
        self.vida -= daño_final
        proyectil.activo = False
        return self.vida <= 0

    def dibujar(self, superficie):
        if self.tipo == "arana" and (self.descendiendo or self.lado == "superior"):
            pygame.draw.line(superficie, (220, 220, 220), (self.rect.centerx, 0), (self.rect.centerx, self.rect.top), 1)

        if self.imagen is not None:
            superficie.blit(self.imagen, self.rect)
        else:
            if self.tipo == "pulgon":
                pygame.draw.ellipse(superficie, (150, 220, 100), self.rect)
            elif self.tipo == "escarabajo":
                pygame.draw.rect(superficie, (80, 50, 30), self.rect, border_radius=8)
            elif self.tipo == "arana":
                pygame.draw.circle(superficie, (40, 40, 40), (self.rect.centerx, self.rect.centery), self.ancho // 2)
            elif self.tipo == "jefe":
                pygame.draw.rect(superficie, (34, 139, 34), self.rect, border_radius=12)

        ancho_barra = self.ancho
        alto_barra = 5
        x_barra = self.rect.x
        y_barra = self.rect.y - 8
        
        pygame.draw.rect(superficie, (200, 50, 50), (x_barra, y_barra, ancho_barra, alto_barra))
        proporcional_vida = max(0, self.vida / self.vida_maxima)
        ancho_actual = int(ancho_barra * proporcional_vida)
        pygame.draw.rect(superficie, (50, 200, 50), (x_barra, y_barra, ancho_actual, alto_barra))