from mesa import Model, Agent
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


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

class Celda(Agent):
    """Agente que representa un cuadro fijo de color verde."""
    def __init__(self, unique_id, model, direction, color):
        super().__init__(unique_id, model)
        self.direccion = direction
        self.color = color  # Color inicial de la celda

class Mapa(Model):
    """Modelo que fija cuadros verdes en posiciones específicas del grid."""
    def __init__(self, width, height, transitables, intransitables):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.transitables = transitables
        self.intransitables = intransitables

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


# Crear el modelo y configurar el servidor
canvas_element = CanvasGrid(agentPortrayal, 11, 11, 500, 500)
model_params = {
    "width": 11,
    "height": 11,
    "transitables": transitables,
    "intransitables": intransitables,
}
server = ModularServer(Mapa, [canvas_element], "Traffic Simulation", model_params)
server.port = 8521
server.launch()