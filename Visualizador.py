import mesa
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

class CuadroVerdeAgent(Agent):
    """Agente que representa un cuadro fijo de color verde."""
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.direccion = direction

class CuadroVerdeModel(Model):
    """Modelo que fija cuadros verdes en posiciones específicas del grid."""
    def __init__(self, width, height, posiciones_verdes):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        
        # Agregar agentes en posiciones específicas
        for idx, (x, y, direccion) in enumerate(posiciones_verdes):
            agente = CuadroVerdeAgent(idx, self, direccion)
            self.grid.place_agent(agente, (x, y))
            self.schedule.add(agente)
    
    def step(self):
        self.schedule.step()

def agentPortrayal(agent):
    if isinstance(agent, CuadroVerdeAgent):
        color = "green"
        if agent.direccion == "Sur":
            color = "blue"
        elif agent.direccion == "Oeste":
            color = "red"
        # Añadir más condiciones si es necesario.
        return {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": color,
            "w": 1,
            "h": 1
        }

# Coordenadas específicas para los cuadros verdes
transitables = [(1, 1, "Sur"), (1, 2, "Oeste"), (1, 3, "Oeste"), (1, 4, "Oeste"), (1, 5, "Oeste"), (1, 6, "Oeste"), (1, 7, "Oeste"), (1, 8, "Oeste"), (1, 9, "Oeste"), (1, 10, "Oeste"), (1, 11, "Oeste"), (1, 12, "Oeste"), (1, 13, "Oeste"), (1, 14, "Oeste"), (1, 15, "Oeste"), (1, 16, "Oeste"), (1, 17, "Oeste"), (1, 18, "Oeste"), (1, 19, "Oeste"), (1, 20, "Oeste"), (1, 21, "Oeste"), (1, 22, "Oeste"), (1, 23, "Oeste"), (1, 24, "Oeste"),
                (2, 1, "Sur"), (2, 2, "Oeste"), (2, 3, "Oeste"), (2, 4, "Oeste"), (2, 5, "Oeste"), (2, 6, "Oeste"), (2, 7, "Oeste"), (2, 8, "Oeste"), (2, 9, "Oeste"), (2, 10, "Oeste"), (2, 11, "Oeste"), (2, 12, "Oeste"), (2, 13, "Oeste"), (2, 14, "Oeste"), (2, 15, "Oeste"), (2, 16, "Oeste"), (2, 17, "Oeste"), (2, 18, "Oeste"), (2, 19, "Oeste"), (2, 20, "Oeste"), (2, 21, "Oeste"), (2, 22, "Oeste"), (2, 23, "Norte"), (2, 24, "Norte"),
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
                (13, 1, "Sur"), (13, 2, "Sur"), (13, 3, "Oeste"), (13, 4, "Oeste"), (13, 5, "Oeste"), (13, 6, "Oeste"), (13, 7, "Oeste"), (13, 8, "Oeste"), (13, 9, "Oeste"), (13, 10, "Oeste"), (13, 11, "Oeste"), (13, 12, "Oeste"), (13, 13, "Oeste"), (13, 14, "Oeste"), (13, 15, "Oeste"), (13, 16, "Norte"), (13, 17, "Oeste"), (13, 18, "Oeste"), (13, 19, "Oeste"), (13, 20, "Oeste"), (13, 21, "Oeste"), (13, 22, "Oeste"), (13, 23, "Norte"), (13, 24, "Norte"),
                (14, 1, "Sur"), (14, 2, "Sur"), (14, 3, "Oeste"), (14, 4, "Oeste"), (14, 5, "Oeste"), (14, 6, "Oeste"), (14, 7, "Oeste"), (14, 8, "Oeste"), (14, 9, "Oeste"), (14, 10, "Oeste"), (14, 11, "Oeste"), (14, 12, "Oeste"), (14, 13, "Sur"), (14, 16, "Norte"), (14, 17, "Oeste"), (14, 18, "Oeste"), (14, 19, "Oeste"), (14, 20, "Oeste"), (14, 21, "Oeste"), (14, 22, "Oeste"), (14, 23, "Norte"), (14, 24, "Norte"),
                (15, 1, "Sur"), (15, 2, "Sur"), (15, 3, "Este"), (15, 4, "Este"), (15, 5, "Este"), (15, 6, "Este"), (15, 7, "Este"), (15, 8, "Este"), (15, 9, "Este"), (15, 10, "Este"), (15, 11, "Este"), (15, 12, "Este"), (15, 13, "Sur"), (15, 16, "Norte"), (15, 17, "Este"), (15, 18, "Este"), (15, 19, "Este"), (15, 20, "Este"), (15, 21, "Este"), (15, 22, "Este"), (15, 23, "Norte"), (15, 24, "Norte"),
                (16, 1, "Sur"), (16, 2, "Sur"), (16, 3, "Este"), (16, 4, "Este"), (16, 5, "Este"), (16, 6, "Este"), (16, 7, "Este"), (16, 8, "Este"), (16, 9, "Este"), (16, 10, "Este"), (16, 11, "Este"), (16, 12, "Este"), (16, 13, "Sur"), (16, 14, "Este"), (16, 15, "Este"), (16, 16, "Este"), (16, 17, "Este"), (16, 18, "Este"), (16, 19, "Este"), (16, 20, "Oeste"), (16, 21, "Oeste"), (16, 22, "Oeste"), (16, 23, "Norte"), (16, 24, "Norte"),
                (17, 1, "Sur"), (17, 2, "Sur"), (17, 7, "Sur"), (17, 8, "Sur"), (17, 13, "Sur"), (17, 14, "Sur"), (17, 15, "Norte"), (17, 16, "Norte"), (17, 19, "Norte"), (17, 20, "Norte"),(17, 23, "Norte"), (17, 24, "Norte"),
                (18, 1, "Sur"), (18, 2, "Sur"), (18, 7, "Sur"), (18, 8, "Sur"), (18, 13, "Sur"), (18, 14, "Sur"), (18, 15, "Norte"), (18, 16, "Norte"), (18, 19, "Norte"), (18, 20, "Norte"),(18, 23, "Norte"), (18, 24, "Norte"),
                (19, 1, "Sur"), (19, 2, "Sur"), (19, 3, "Oeste"), (19, 4, "Oeste"), (19, 5, "Oeste"), (19, 6, "Oeste"), (19, 7, "Sur"), (19, 8, "Sur"), (19, 9, "Este"), (19, 10, "Este"), (19, 11, "Este"), (19, 12, "Este"), (19, 13, "Sur"), (19, 14, "Sur"), (19, 15, "Norte"), (19, 16, "Norte"), (19, 19, "Norte"), (19, 20, "Norte"),(19, 23, "Norte"), (19, 24, "Norte"),
                (20, 1, "Sur"), (20, 2, "Sur"), (20, 3, "Oeste"), (20, 4, "Oeste"), (20, 5, "Oeste"), (20, 6, "Oeste"), (20, 7, "Sur"), (20, 8, "Sur"), (20, 9, "Este"), (20, 10, "Este"), (20, 11, "Este"), (20, 12, "Este"), (20, 13, "Sur"), (20, 14, "Sur"), (20, 15, "Norte"), (20, 16, "Norte"), (20, 19, "Norte"), (20, 20, "Norte"),(20, 23, "Norte"), (20, 24, "Norte"),
                (21, 1, "Sur"), (21, 2, "Sur"), (21, 7, "Sur"), (21, 8, "Sur"), (21, 13, "Sur"), (21, 14, "Sur"), (21, 15, "Norte"), (21, 16, "Norte"), (21, 19, "Norte"), (21, 20, "Norte"),(21, 23, "Norte"), (21, 24, "Norte"),
                (22, 1, "Sur"), (22, 2, "Sur"), (22, 7, "Sur"), (22, 8, "Sur"), (22, 13, "Sur"), (22, 14, "Sur"), (22, 15, "Norte"), (22, 16, "Norte"), (22, 19, "Norte"), (22, 20, "Norte"),(22, 23, "Norte"), (22, 24, "Norte"),
                (23, 1, "Sur"), (23, 2, "Sur"), (23, 3, "Este"), (23, 4, "Este"), (23, 5, "Este"), (23, 6, "Este"), (23, 7, "Este"), (23, 8, "Este"), (23, 9, "Este"), (23, 10, "Este"), (23, 11, "Este"), (23, 12, "Este"), (23, 13, "Este"), (23, 14, "Este"), (23, 15, "Este"), (23, 16, "Este"), (23, 17, "Este"), (23, 18, "Este"), (23, 19, "Este"), (23, 20, "Este"), (23, 21, "Este"), (23, 22, "Este"), (23, 23, "Este"), (23, 24, "Norte"),
                (24, 1, "Este"), (24, 2, "Este"), (24, 3, "Este"), (24, 4, "Este"), (24, 5, "Este"), (24, 6, "Este"), (24, 7, "Este"), (24, 8, "Este"), (24, 9, "Este"), (24, 10, "Este"), (24, 11, "Este"), (24, 12, "Este"), (24, 13, "Este"), (24, 14, "Este"), (24, 15, "Este"), (24, 16, "Este"), (24, 17, "Este"), (24, 18, "Este"), (24, 19, "Este"), (24, 20, "Este"), (24, 21, "Este"), (24, 22, "Este"), (24, 23, "Este"), (24, 24, "Norte"),]

# Crear el modelo
model = CuadroVerdeModel(25, 25, transitables)

# Configurar el CanvasGrid
canvas_element = CanvasGrid(agentPortrayal, 25, 25, 500, 500)

# Crear y correr el servidor
server = ModularServer(CuadroVerdeModel, [canvas_element], "Cuadros Verdes", {"width": 25, "height": 25, "posiciones_verdes": transitables})
server.port = 8521  # O el puerto que prefieras
server.launch()
