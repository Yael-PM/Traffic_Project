from mesa import Model, Agent
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from Agentes import *

matrizTotal = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10)]

intransitables = [(0, 10), (1, 10), (2, 10), (3, 10), (7, 10), (8, 10), (9, 10), (10, 10),
                  (0, 9), (1, 9), (2, 9), (3, 9), (7, 9), (8, 9), (9, 9), (10, 9),
                  (0, 8), (1, 8), (2, 8), (3, 8), (7, 8), (8, 8), (9, 8), (10, 8),
                  (0, 7), (1, 7), (2, 7), (3, 7), (7, 7), (8, 7), (9, 7), (10, 7),
                  (0, 3), (1, 3), (2, 3), (3, 3), (7, 3), (8, 3), (9, 3), (10, 3),
                  (0, 2), (1, 2), (2, 2), (3, 2), (7, 2), (8, 2), (9, 2), (10, 2),
                  (0, 1), (1, 1), (2, 1), (3, 1), (7, 1), (8, 1), (9, 1), (10, 1),
                  (0, 0), (1, 0), (2, 0), (3, 0), (7, 0), (8, 0), (9, 0), (10, 0),
                  ]

transitables = [(0, 4), (0, 5), (0, 6), (1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (7, 4), (7, 5), (7, 6), (8, 4), (8, 5), (8, 6), (9, 4), (9, 5), (9, 6), (10, 4), (10, 5), (10, 6)]

banquetas = [(0, 3), (1, 3), (2, 3), (3, 3), (7, 3), (8, 3), (9, 3), (10, 3),
             (0, 2), (1, 2), (2, 2), (3, 2), (7, 2), (8, 2), (9, 2), (10, 2),
             (2, 2), (2, 1), (2, 0), (3, 2), (3, 1), (3, 0), (7, 2), (7, 1), (7, 0), (8, 2), (8, 1), (8, 0),
             
             (0, 7), (1, 7), (2, 7), (3, 7), (7, 7), (8, 7), (9, 7), (10, 7),
             (0, 8), (1, 8), (2, 8), (3, 8), (7, 8), (8, 8), (9, 8), (10, 8),
             (2, 2), (2, 1), (2, 0), (3, 2), (3, 1), (3, 0), (7, 2), (7, 1), (7, 0), (8, 2), (8, 1), (8, 0),
             ]

semaforos = [(3,3),(7,3),(3,7),(7,7)]

destino = [ (0, 7), (1, 7), (2, 7), (3, 7), (7, 7), (8, 7), (9, 7), (10, 7)]

class Celda(Agent):
    """Agente que representa un cuadro fijo de color verde."""
    def __init__(self, unique_id, model, direction, color):
        super().__init__(unique_id, model)
        self.direccion = direction
        self.color = color  # Color inicial de la celda

    def move(self):
        x, y = self.pos
        possible_moves=[
            (x + 1, y), (x -1, y),
            (x, y + 1), (x, y -1)
        ]

        possible_moves = [(nx,ny)for nx, ny in possible_moves if 0<= nx < self.model.grid.width and 0 <= ny <self.model.grid.height]

        possible_moves = [move for move in possible_moves if move in self.model.transitable]

        if possible_moves:
            new_pos = random.choice(possible_moves)
            self.model.grid.move_agent(self, new_pos)

class Mapa(Model):
    """Modelo que fija cuadros verdes en posiciones específicas del grid."""
    def __init__(self, width, height, transitables, intransitables, banquetas, num_peatones, semaforos, destino = None):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.transitables = transitables + banquetas
        self.intransitables = intransitables
        self.banquetas = banquetas
        self.semaforos = semaforos
        self.destino = destino
    
        # Agregar agentes transitables
        for idx, (x, y) in enumerate(transitables):
            color = "white"  # Color para celdas transitables
            agente = Celda(idx, self, "T", color)  # T para "Transitable"
            self.grid.place_agent(agente, (x, y))
            self.schedule.add(agente)

        # Agregar agentes intransitables
        for idx, (x, y) in enumerate(intransitables):
            color = "blue"  # Color para celdas intransitables
            agente = Celda(idx + len(transitables), self, "I", color)  # I para "Intransitable"
            self.grid.place_agent(agente, (x, y))
            self.schedule.add(agente)
        # Banquetas
        for idx, (x, y) in enumerate(self.banquetas):
            color = "gray"
            agente = Celda(idx + len(transitables) + len(intransitables), self, "B", color)
            self.grid.place_agent(agente, (x, y))
            self.schedule.add(agente)
        
        for idx, pos in enumerate(semaforos):
            semaforo = SemaforoPeatonal(
                unique_id=idx+500,
                model=self,
                pos=pos,
                radio_detencion=0
            )
            self.grid.place_agent(semaforo,pos)
            self.schedule.add(semaforo)


        for i in range(num_peatones):
            inicio = random.choice(banquetas)
            destino = random.choice(banquetas)
            peaton = Peaton(unique_id= i+1000,
                            model=self,
                            destino=destino,
                            transitables=transitables,
                            semaforos=semaforos
                            )
            self.grid.place_agent(peaton,inicio)
            self.schedule.add(peaton)

    def step(self):
        self.schedule.step()

def agentPortrayal(agent):
    """Función de representación de los agentes."""
    if isinstance(agent, Celda):
        return {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": agent.color,  # Utiliza el color definido en el agente
            "w": 1,
            "h": 1
        }
    elif isinstance(agent, Peaton):
        return{
            "Shape": "circle",
            "Filled": "true",
            "Layer": 1,
            "Color": agent.color,
            "r":0.5
        }
    elif isinstance(agent, SemaforoPeatonal):
        color = "green" if agent.estado == "verde" else "red"
        return {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 1,
            "Color": color,
            "w" : 1,
            "h":1
        }


# Crear el modelo y configurar el servidor
canvas_element = CanvasGrid(agentPortrayal, 11, 11, 500, 500)
model_params = {
    "width": 11,
    "height": 11,
    "transitables": transitables,
    "intransitables": intransitables,
    "banquetas":banquetas,
    "num_peatones":5,
    "semaforos":semaforos,
    "destino":destino
}
server = ModularServer(Mapa, [canvas_element], "Traffic Simulation", model_params)
server.port = 8521
server.launch()