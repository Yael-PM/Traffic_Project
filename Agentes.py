from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random

estacionamientos = []
transitables = [(1, 1, "Oeste"), (1, 2, "Oeste"), (1, 3, "Oeste"), (1, 4, "Oeste"), (1, 5, "Oeste"), (1, 6, "Oeste"), (1, 7, "Oeste"), (1, 8, "Oeste"), (1, 9, "Oeste"), (1, 10, "Oeste"), (1, 11, "Oeste"), (1, 12, "Oeste"), (1, 13, "Oeste"), (1, 14, "Oeste"), (1, 15, "Oeste"), (1, 16, "Oeste"), (1, 17, "Oeste"), (1, 18, "Oeste"), (1, 19, "Oeste"), (1, 20, "Oeste"), (1, 21, "Oeste"), (1, 22, "Oeste"), (1, 23, "Oeste"), (1, 24, "Oeste"),
                (2, 1, "Oeste"), (2, 2, "Oeste"), (2, 3, "Oeste"), (2, 4, "Oeste"), (2, 5, "Oeste"), (2, 6, "Oeste"), (2, 7, "Oeste"), (2, 8, "Oeste"), (2, 9, "Oeste"), (2, 10, "Oeste"), (2, 11, "Oeste"), (2, 12, "Oeste"), (2, 13, "Oeste"), (2, 14, "Oeste"), (2, 15, "Oeste"), (2, 16, "Oeste"), (2, 17, "Oeste"), (2, 18, "Oeste"), (2, 19, "Oeste"), (2, 20, "Oeste"), (2, 21, "Oeste"), (2, 22, "Oeste"), (2, 23, "Oeste"), (2, 24, "Oeste"),
                (3, 1, "Sur"), (3, 2, "Sur"), (3, 7, "Norte"), (3, 8, "Norte"), (3, 13, "Sur"), (3, 14, "Sur"), (3, 15, "Norte"), (3, 16, "Norte"), (3, 23, "Norte"), (3, 24, "Norte"),
                (4, 1, "Sur"), (4, 2, "Sur"), (4, 7, "Norte"), (4, 8, "Norte"), (4, 13, "Sur"), (4, 14, "Sur"), (4, 15, "Norte"), (4, 16, "Norte"), (4, 23, "Norte"), (4, 24, "Norte"),
                (5, 1, "Sur"), (5, 2, "Sur"), (5, 7, "Norte"), (5, 8, "Norte"), (5, 13, "Sur"), (5, 14, "Sur"), (5, 15, "Norte"), (5, 16, "Norte"), (5, 23, "Norte"), (5, 24, "Norte"),
                (6, 1, "Sur"), (6, 2, "Sur"), (6, 7, "Norte"), (6, 8, "Norte"), (6, 9, "Oeste"), (6, 10, "Oeste"), (6, 11, "Oeste"), (6, 12, "Oeste"), (6, 13, "Sur"), (6, 14, "Sur"), (6, 15, "Norte"), (6, 16, "Norte"), (6, 23, "Norte"), (6, 24, "Norte"),
                (7, 1, "Sur"), (7, 2, "Sur"), (7, 7, "Norte"), (7, 8, "Norte"), (7, 9, "Oeste"), (7, 10, "Oeste"), (7, 11, "Oeste"), (7, 12, "Oeste"), (7, 13, "Sur"), (7, 14, "Sur"), (7, 15, "Norte"), (7, 16, "Norte"), (7, 17, "Oeste"), (7, 18, "Oeste"), (7, 19, "Oeste"), (7, 20, "Oeste"), (7, 21, "Oeste"), (7, 22, "Oeste"), (7, 23, "Norte"), (7, 24, "Norte"),
                (8, 1, "Sur"), (8, 2, "Sur"), (8, 7, "Norte"), (8, 8, "Norte"), (8, 13, "Sur"), (8, 14, "Sur"), (8, 15, "Norte"), (8, 16, "Norte"), (8, 17, "Oeste"), (8, 18, "Oeste"), (8, 19, "Oeste"), (8, 20, "Oeste"), (8, 21, "Oeste"), (8, 22, "Oeste"), (8, 23, "Norte"), (8, 24, "Norte"),
                (9, 1, "Sur"), (9, 2, "Sur"), (9, 7, "Norte"), (9, 8, "Norte"), (9, 13, "Sur"), (9, 14, "Sur"), (9, 15, "Norte"), (9, 16, "Norte"), (9, 23, "Norte"), (9, 24, "Norte"),
                (10, 1, "Sur"), (10, 2, "Sur"), (10, 7, "Norte"), (10, 8, "Norte"), (10, 13, "Sur"), (10, 14, "Sur"), (10, 15, "Norte"), (10, 16, "Norte"), (10, 23, "Norte"), (10, 24, "Norte"),
                (11, 1, "Sur"), (11, 2, "Sur"), (11, 7, "Norte"), (11, 8, "Norte"), (11, 13, "Sur"), (11, 14, "Sur"), (11, 15, "Norte"), (11, 16, "Norte"), (11, 23, "Norte"), (11, 24, "Norte"),
                (12, 1, "Sur"), (12, 2, "Sur"), (12, 7, "Norte"), (12, 8, "Norte"), (12, 13, "Sur"), (12, 14, "Sur"), (12, 15, "Norte"), (12, 16, "Norte"), (12, 23, "Norte"), (12, 24, "Norte"),
                (13, 1, "Sur"), (13, 2, "Sur"), (13, 3, "Oeste"), (13, 4, "Oeste"), (13, 5, "Oeste"), (13, 6, "Oeste"), (13, 7, "Oeste"), (13, 8, "Oeste"), (13, 9, "Oeste"), (13, 10, "Oeste"), (13, 11, "Oeste"), (13, 12, "Oeste"), (13, 13, "Oeste"), (13, 14, "Oeste"), (13, 15, "Norte"), (13, 16, "Oeste"), (13, 17, "Oeste"), (13, 18, "Oeste"), (13, 19, "Oeste"), (13, 20, "Oeste"), (13, 21, "Oeste"), (13, 22, "Oeste"), (13, 23, "Norte"), (13, 24, "Norte"),
                (14, 1, "Sur"), (14, 2, "Sur"), (14, 3, "Oeste"), (14, 4, "Oeste"), (14, 5, "Oeste"), (14, 6, "Oeste"), (14, 7, "Oeste"), (14, 8, "Oeste"), (14, 9, "Oeste"), (14, 10, "Oeste"), (14, 11, "Oeste"), (14, 12, "Oeste"), (14, 13, "Sur"), (14, 16, "Norte"), (14, 17, "Oeste"), (14, 18, "Oeste"), (14, 19, "Oeste"), (14, 20, "Oeste"), (14, 21, "Oeste"), (14, 22, "Oeste"), (14, 23, "Norte"), (14, 24, "Norte"),
                ]

no_transitables = [(3, 3, "Oeste"), (3, 4, "Oeste"), (3, 5, "Oeste"), (3, 6, "Oeste"), (3, 9, "Oeste"), (3, 10, "Oeste"), (3, 11, "Oeste"), (3, 12, "Oeste"), (3, 17, "Oeste"), (3, 18, "Oeste"), (3, 19, "Oeste"), (3, 20, "Oeste"), (3, 21, "Oeste"), (3, 22, "Oeste"),]

"""
Clase banqueta:
    - Atributos:
        - Tipo: Entero que indica que tipo de celda es si es transitable, si no lo es o si es un estacionamiento
"""
class Celda:
    def __init__(self, tipo):
        self.tipo = tipo

"""
Clase vehiculo:
    - Atributos:
        - Velocidad: Random entre 1 y 5 donde 5 es la velocidad máxima
        - Direccion: Random entre (1, 1), (-1, 0), (0, 1), (0, -1)
        - Tipo de vehiculo: Random entre 1 y 4
        - Estado: Random entre 1 y 3, avanzando, en alto y estacionado
    - Metodos:
        - Moverse
        - Cambiar de direccion
"""
class Vehiculo(Agent):
    def __init__(self, model, destino):
        super().__init__(id, model)
        self.velocidad = random.randint(1, 5)
        self.direccion = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def move(self):
        x, y = self.pos
        dx, dy = self.direccion
        new_pos = (x + dx, y + dy)
        self.model.grid.move_agent(self, new_pos)

    def step(self):
        self.move()

"""
Clase semaforo:
    - Atributos:
        - Estado: Random entre 1 y 3, en verde, en amarillo y en rojo
    - Metodos:
        - Cambiar de estado
"""
class Semaforo(Agent):
    def __init__(self, model):
        super().__init__(id, model)
        self.estado = random.randint(1, 3)