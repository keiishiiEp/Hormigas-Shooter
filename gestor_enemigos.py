import random
from enemigo import Enemigo

class GestorEnemigos:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.enemigos = []
        self.proyectiles_enemigos = []
        self.fase_actual = 1
        self.temporizador_acompanantes = 0

    def configurar_fase(self, fase):
        self.fase_actual = fase
        self.enemigos.clear()
        self.proyectiles_enemigos.clear()
        
        if fase == 1:
            self.enemigos.append(Enemigo("pulgon", 180, self.ancho_pantalla, lado="derecha"))
            self.enemigos.append(Enemigo("pulgon", 350, self.ancho_pantalla, lado="izquierda"))
        elif fase == 2:
            self.enemigos.append(Enemigo("pulgon", 150, self.ancho_pantalla, lado="derecha"))
            self.enemigos.append(Enemigo("escarabajo", 300, self.ancho_pantalla, lado="izquierda"))
            self.enemigos.append(Enemigo("pulgon", 420, self.ancho_pantalla, lado="derecha"))
        elif fase == 3:
            self.enemigos.append(Enemigo("pulgon", 150, self.ancho_pantalla, lado="izquierda"))
            self.enemigos.append(Enemigo("escarabajo", 260, self.ancho_pantalla, lado="derecha"))
            self.enemigos.append(Enemigo("arana", 250, self.ancho_pantalla, lado="superior"))
        
        elif fase == 4:
            self.enemigos.append(Enemigo("jefe", 220, self.ancho_pantalla, lado="derecha"))

    def actualizar(self):
        jefe_presente = any(e.tipo == "jefe" for e in self.enemigos)
        jefe_derrotado = jefe_presente and not any(e.tipo == "jefe" and e.vida > 0 for e in self.enemigos)

        for enemigo in self.enemigos:
            enemigo.actualizar()
            enemigo.intentar_atacar(self.proyectiles_enemigos)
            
            if self.fase_actual == 4:
                self.temporizador_acompanantes += 1
                if self.temporizador_acompanantes >= 180:
                    self.temporizador_acompanantes = 0
                    pulgones_actuales = sum(1 for e in self.enemigos if e.tipo == "pulgon" and e.vida > 0)
                    if pulgones_actuales < 25:
                        lado_aleatorio = random.choice(["derecha", "izquierda"])
                        self.enemigos.append(Enemigo("pulgon", random.randint(100, 450), self.ancho_pantalla, lado=lado_aleatorio))

        for pe in self.proyectiles_enemigos:
            pe.actualizar()
            if pe.x < -50 or pe.x > self.ancho_pantalla + 50 or pe.y < 0 or pe.y > self.alto_pantalla:
                pe.activo = False

        self.proyectiles_enemigos = [pe for pe in self.proyectiles_enemigos if pe.activo]
        self.enemigos = [e for e in self.enemigos if e.vida > 0]

        if self.fase_actual == 4 and jefe_derrotado:
            self.enemigos.clear()

    def verificar_colisiones(self, gestor_proyectiles):
        for proyectil in gestor_proyectiles.proyectiles:
            if not proyectil.activo:
                continue
            for enemigo in self.enemigos:
                if enemigo.rect.colliderect(proyectil.rect):
                    enemigo.recibir_impacto(proyectil)
                    break

    def dibujar(self, superficie):
        for enemigo in self.enemigos:
            enemigo.dibujar(superficie)
        for pe in self.proyectiles_enemigos:
            pe.dibujar(superficie)