import math
import pygame

class ProyectilBasico:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.velocidad = 10
        self.radio = 4
        self.danio = 1
        self.activo = True
        self.rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

    def actualizar(self):
        self.y -= self.velocidad
        self.rect.x = int(self.x - self.radio)
        self.rect.y = int(self.y - self.radio)

    def dibujar(self, superficie):
        pygame.draw.line(superficie, (160, 240, 50), (int(self.x), int(self.y)), (int(self.x), int(self.y + 10)), 3)
        pygame.draw.circle(superficie, (220, 255, 120), (int(self.x), int(self.y)), self.radio)


class ProyectilParabolico:
    def __init__(self, x, y, direccion=1):
        self.x_inicio = float(x)
        self.y_inicio = float(y)
        self.x = float(x)
        self.y = float(y)
        self.vx = 5.0 * direccion
        self.vy = -10.0
        self.g = 0.35
        self.tiempo = 0
        self.radio = 7
        self.danio = 3
        self.activo = True
        self.rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

    def actualizar(self):
        self.tiempo += 1
        self.x = self.x_inicio + self.vx * self.tiempo
        self.y = self.y_inicio + (self.vy * self.tiempo + 0.5 * self.g * (self.tiempo ** 2))
        self.rect.x = int(self.x - self.radio)
        self.rect.y = int(self.y - self.radio)

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, (230, 160, 255), (int(self.x), int(self.y)), self.radio + 3, 2)
        pygame.draw.circle(superficie, (186, 85, 211), (int(self.x), int(self.y)), self.radio)


class ProyectilConico:
    def __init__(self, x, y):
        self.x_origen = float(x)
        self.y_origen = float(y)
        self.radio_giro = 30.0
        self.velocidad_avance = 4.0
        self.angulo = 0.0
        self.velocidad_angular = 0.15
        self.x = float(x)
        self.y = float(y)
        self.radio = 8
        self.danio = 5
        self.activo = True
        self.rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

    def actualizar(self):
        self.y_origen -= self.velocidad_avance
        self.angulo += self.velocidad_angular
        self.x = self.x_origen + self.radio_giro * math.cos(self.angulo)
        self.y = self.y_origen + self.radio_giro * math.sin(self.angulo)
        self.rect.x = int(self.x - self.radio)
        self.rect.y = int(self.y - self.radio)

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, (255, 140, 0), (int(self.x), int(self.y)), self.radio)
        px1 = int(self.x + 10 * math.cos(self.angulo))
        py1 = int(self.y + 10 * math.sin(self.angulo))
        pygame.draw.circle(superficie, (255, 215, 0), (px1, py1), 3)


class GestorProyectiles:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.proyectiles = []
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.cooldown_parabolico = 300
        self.ultimo_disparo_parabolico = 0
        self.municion_conica = 10

    def disparar_basico(self, x, y):
        self.proyectiles.append(ProyectilBasico(x, y))

    def disparar_parabolico(self, x, y, direccion=1):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo_parabolico >= self.cooldown_parabolico:
            self.proyectiles.append(ProyectilParabolico(x, y, direccion))
            self.ultimo_disparo_parabolico = tiempo_actual
            return True
        return False

    def disparar_conico(self, x, y):
        if self.municion_conica > 0:
            self.proyectiles.append(ProyectilConico(x, y))
            self.municion_conica -= 1
            return True
        return False

    def actualizar(self):
        for p in self.proyectiles:
            p.actualizar()
            if p.x > self.ancho_pantalla or p.x < 0 or p.y > self.alto_pantalla or p.y < 0:
                p.activo = False

        self.proyectiles = [p for p in self.proyectiles if p.activo]

    def dibujar(self, superficie):
        for p in self.proyectiles:
            p.dibujar(superficie)