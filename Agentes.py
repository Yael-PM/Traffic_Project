from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random

"""
Clase vehiculo:
    - Atributos:
        - Velocidad: Random entre 1 y 5 donde 5 es la velocidad máxima
        - Direccion: Random entre (1, 0), (-1, 0), (0, 1), (0, -1)
        - Tipo de vehiculo: Random entre 1 y 4
        - Estado: Random entre 1 y 3, avanzando, en alto y estacionado
    - Metodos:
        - Moverse
        - Cambiar de direccion
"""
class Vehiculo(Agent):
    def __init__(self, unique_id, model, destino):
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
    def __init__(self, unique_id, model):
        super().__init__(id, model)
        self.estado = random.randint(1, 3)

    