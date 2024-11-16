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
        - Direccion: Random entre (1, 1), (-1, 0), (0, 1), (0, -1)
        - Tipo de vehiculo: Random entre 1 y 4
        - Estado: Random entre 1 y 3, avanzando, en alto y estacionado
    - Metodos:
        - Moverse
        - Cambiar de direccion
"""
transitables = [(1, 2, 'S'), (2, 2, 'O'), (3, 2, 'O'), (4, 2, 'O'), (5, 2, 'O'), (6, 2, 'O'), (7, 2, 'O'), (8, 2, 'O'), (9, 2, 'O'), (10, 2, 'O'), (11, 2, 'O'), (12, 2, 'O'), (13, 2, 'O'), (14, 2, 'O'), (15, 2, 'O'), (16, 2, 'O'), (17, 2, 'O'), (18, 2, 'O'), (19, 2, 'O'), (20, 2, 'O'), (21, 2, 'O'), (22, 2, 'O'), (23, 2, 'O'), (24, 2, 'O'), (1, 3, 'S'), (2, 3, 'O'), (3, 3, 'O'), (4, 3, 'O'), (5, 3, 'O'), (6, 3, 'O'), (7, 3, 'O'), (8, 3, 'O'), (9, 3, 'O'), (10, 3, 'O'), (11, 3, 'O'), (12, 3, 'O'), (13, 3, 'O'), (14, 3, 'O'), (15, 3, 'O'), (16, 3, 'O'), (17, 3, 'O'), (18, 3, 'O'), (19, 3, 'O'), (20, 3, 'O'), (21, 3, 'O'), (22, 3, 'O'), (23, 3, 'N'), (24, 3, 'N'), (1, 4, 'S'), (2, 4, 'S'), (7, 4, 'N'), (8, 4, 'N'), (13, 4, 'S'), (14, 4, 'S'), (15, 4, 'N'), (16, 4, 'N'), (23, 4, 'N'), (24, 4, 'N'), (1, 5, 'S'), (2, 5, 'S'), (7, 5, 'N'), (8, 5, 'N'), (13, 5, 'S'), (14, 5, 'S'), (15, 5, 'N'), (16, 5, 'N'), (23, 5, 'N'), (24, 5, 'N'), (1, 6, 'S'), (2, 6, 'S'), (7, 6, 'N'), (8, 6, 'N'), (13, 6, 'S'), (14, 6, 'S'), (15, 6, 'N'), (16, 6, 'N'), (23, 6, 'N'), (24, 6, 'N'), (1, 7, 'S'), (2, 7, 'S'), (7, 7, 'N'), (8, 7, 'N'), (9, 7, 'O'), (10, 7, 'O'), (11, 7, 'O'), (12, 7, 'O'), (13, 7, 'S'), (14, 7, 'S'), (15, 7, 'N'), (16, 7, 'N'), (23, 7, 'N'), (24, 7, 'N'), (1, 8, 'S'), (2, 8, 'S'), (7, 8, 'N'), (8, 8, 'N'), (9, 8, 'O'), (10, 8, 'O'), (11, 8, 'O'), (12, 8, 'O'), (13, 8, 'S'), (14, 8, 'S'), (15, 8, 'N'), (16, 8, 'N'), (17, 8, 'O'), (18, 8, 'O'), (19, 8, 'O'), (20, 8, 'O'), (21, 8, 'O'), (22, 8, 'O'), (23, 8, 'N'), (24, 8, 'N'), (1, 9, 'S'), (2, 9, 'S'), (7, 9, 'N'), (8, 9, 'N'), (13, 9, 'S'), (14, 9, 'S'), (15, 9, 'N'), (16, 9, 'N'), (17, 9, 'O'), (18, 9, 'O'), (19, 9, 'O'), (20, 9, 'O'), (21, 9, 'O'), (22, 9, 'O'), (23, 9, 'N'), (24, 9, 'N'), (1, 10, 'S'), (2, 10, 'S'), (7, 10, 'N'), (8, 10, 'N'), (13, 10, 'S'), (14, 10, 'S'), (15, 10, 'N'), (16, 10, 'N'), (23, 10, 'N'), (24, 10, 'N'), (1, 11, 'S'), (2, 11, 'S'), (7, 11, 'N'), (8, 11, 'N'), (13, 11, 'S'), (14, 11, 'S'), (15, 11, 'N'), (16, 11, 'N'), (23, 11, 'N'), (24, 11, 'N'), (1, 12, 'S'), (2, 12, 'S'), (7, 12, 'N'), (8, 12, 'N'), (13, 12, 'S'), (14, 12, 'S'), (15, 12, 'N'), (16, 12, 'N'), (23, 12, 'N'), (24, 12, 'N'), (1, 13, 'S'), (2, 13, 'S'), (7, 13, 'N'), (8, 13, 'N'), (13, 13, 'S'), (14, 13, 'S'), (15, 13, 'N'), (16, 13, 'N'), (23, 13, 'N'), (24, 13, 'N'), (1, 14, 'S'), (2, 14, 'S'), (3, 14, 'O'), (4, 14, 'O'), (5, 14, 'O'), (6, 14, 'O'), (7, 14, 'O'), (8, 14, 'O'), (9, 14, 'O'), (10, 14, 'O'), (11, 14, 'O'), (12, 14, 'O'), (13, 14, 'O'), (14, 14, 'O'), (15, 14, 'O'), (16, 14, 'N'), (17, 14, 'O'), (18, 14, 'O'), (19, 14, 'O'), (20, 14, 'O'), (21, 14, 'O'), (22, 14, 'O'), (23, 14, 'N'), (24, 14, 'N'), (1, 15, 'S'), (2, 15, 'S'), (3, 15, 'O'), (4, 15, 'O'), (5, 15, 'O'), (6, 15, 'O'), (7, 15, 'O'), (8, 15, 'O'), (9, 15, 'O'), (10, 15, 'O'), (11, 15, 'O'), (12, 15, 'O'), (13, 15, 'S'), (16, 15, 'N'), (17, 15, 'O'), (18, 15, 'O'), (19, 15, 'O'), (20, 15, 'O'), (21, 15, 'O'), (22, 15, 'O'), (23, 15, 'N'), (24, 15, 'N'), (1, 16, 'S'), (2, 16, 'S'), (3, 16, 'E'), (4, 16, 'E'), (5, 16, 'E'), (6, 16, 'E'), (7, 16, 'E'), (8, 16, 'E'), (9, 16, 'E'), (10, 16, 'E'), (11, 16, 'E'), (12, 16, 'E'), (13, 16, 'S'), (16, 16, 'N'), (17, 16, 'E'), (18, 16, 'E'), (19, 16, 'E'), (20, 16, 'E'), (21, 16, 'E'), (22, 16, 'E'), (23, 16, 'N'), (24, 16, 'N'), (1, 17, 'S'), (2, 17, 'S'), (3, 17, 'E'), (4, 17, 'E'), (5, 17, 'E'), (6, 17, 'E'), (7, 17, 'E'), (8, 17, 'E'), (9, 17, 'E'), (10, 17, 'E'), (11, 17, 'E'), (12, 17, 'E'), (13, 17, 'S'), (14, 17, 'E'), (15, 17, 'E'), (16, 17, 'E'), (17, 17, 'E'), (18, 17, 'E'), (19, 17, 'E'), (20, 17, 'E'), (21, 17, 'E'), (22, 17, 'E'), (23, 17, 'N'), (24, 17, 'N'), (1, 18, 'S'), (2, 18, 'S'), (7, 18, 'S'), (8, 18, 'S'), (13, 18, 'S'), (14, 18, 'S'), (15, 18, 'N'), (16, 18, 'N'), (19, 18, 'N'), (20, 18, 'N'), (23, 18, 'N'), (24, 18, 'N'), (1, 19, 'S'), (2, 19, 'S'), (7, 19, 'S'), (8, 19, 'S'), (13, 19, 'S'), (14, 19, 'S'), (15, 19, 'N'), (16, 19, 'N'), (19, 19, 'N'), (20, 19, 'N'), (23, 19, 'N'), (24, 19, 'N'), (1, 20, 'S'), (2, 20, 'S'), (3, 20, 'O'), (4, 20, 'O'), (5, 20, 'O'), (6, 20, 'O'), (7, 20, 'S'), (8, 20, 'S'), (9, 20, 'E'), (10, 20, 'E'), (11, 20, 'E'), (12, 20, 'E'), (13, 20, 'S'), (14, 20, 'S'), (15, 20, 'N'), (16, 20, 'N'), (19, 20, 'N'), (20, 20, 'N'), (23, 20, 'N'), (24, 20, 'N'), (1, 21, 'S'), (2, 21, 'S'), (3, 21, 'O'), (4, 21, 'O'), (5, 21, 'O'), (6, 21, 'O'), (7, 21, 'S'), (8, 21, 'S'), (9, 21, 'E'), (10, 21, 'E'), (11, 21, 'E'), (12, 21, 'E'), (13, 21, 'S'), (14, 21, 'S'), (15, 21, 'N'), (16, 21, 'N'), (19, 21, 'N'), (20, 21, 'N'), (23, 21, 'N'), (24, 21, 'N'), (1, 22, 'S'), (2, 22, 'S'), (7, 22, 'S'), (8, 22, 'S'), (13, 22, 'S'), (14, 22, 'S'), (15, 22, 'N'), (16, 22, 'N'), (19, 22, 'N'), (20, 22, 'N'), (23, 22, 'N'), (24, 22, 'N'), (1, 23, 'S'), (2, 23, 'S'), (7, 23, 'S'), (8, 23, 'S'), (13, 23, 'S'), (14, 23, 'S'), (15, 23, 'N'), (16, 23, 'N'), (19, 23, 'N'), (20, 23, 'N'), (23, 23, 'N'), (24, 23, 'N'), (1, 24, 'S'), (2, 24, 'S'), (3, 24, 'E'), (4, 24, 'E'), (5, 24, 'E'), (6, 24, 'E'), (7, 24, 'E'), (8, 24, 'E'), (9, 24, 'E'), (10, 24, 'E'), (11, 24, 'E'), (12, 24, 'E'), (13, 24, 'E'), (14, 24, 'E'), (15, 24, 'E'), (16, 24, 'E'), (17, 24, 'E'), (18, 24, 'E'), (19, 24, 'E'), (20, 24, 'E'), (21, 24, 'E'), (22, 24, 'E'), (23, 24, 'E'), (24, 24, 'N'), (1, 25, 'E'), (2, 25, 'E'), (3, 25, 'E'), (4, 25, 'E'), (5, 25, 'E'), (6, 25, 'E'), (7, 25, 'E'), (8, 25, 'E'), (9, 25, 'E'), (10, 25, 'E'), (11, 25, 'E'), (12, 25, 'E'), (13, 25, 'E'), (14, 25, 'E'), (15, 25, 'E'), (16, 25, 'E'), (17, 25, 'E'), (18, 25, 'E'), (19, 25, 'E'), (20, 25, 'E'), (21, 25, 'E'), (22, 25, 'E'), (23, 25, 'E'), (24, 25, 'N'), (4, 4, 'P'), (18, 4, 'P'), (11, 6, 'P'), (18, 4, 'P'), (21, 7, 'P'), (6, 8, 'P'), (9, 10, 'P'), (21, 10, 'P'), (3, 11, 'P'), (5, 13, 'P'), (11, 13, 'P'), (11, 18, 'P'), (4, 19, 'P'), (18, 19, 'P'), (18, 21, 'P'), (21, 21, 'P'), (5, 22, 'P'), (10, 23, 'P')]  
estacionamientos = [(4, 4, 'P'), (18, 4, 'P'), (11, 6, 'P'), (18, 4, 'P'), (21, 7, 'P'), (6, 8, 'P'), (9, 10, 'P'), (21, 10, 'P'), (3, 11, 'P'), (5, 13, 'P'), (11, 13, 'P'), (11, 18, 'P'), (4, 19, 'P'), (18, 19, 'P'), (18, 21, 'P'), (21, 21, 'P'), (5, 22, 'E'), (10, 23, 'E')]
no_transitable = [(3, 4, 'I'), (3, 5, 'I'), (3, 6, 'I'), (3, 7, 'I'), (3, 8, 'I'), (3, 9, 'I'), (3, 10, 'I'), (3, 12, 'I'), (3, 13, 'I'), (3, 18, 'I'), (3, 19, 'I'), (3, 22, 'I'), (3, 23, 'I'), (4, 5, 'I'), (4, 6, 'I'), (4, 7, 'I'), (4, 8, 'I'), (4, 9, 'I'), (4, 10, 'I'), (4, 11, 'I'), (4, 12, 'I'), (4, 13, 'I'), (4, 18, 'I'), (4, 22, 'I'), (4, 23, 'I'), (5, 4, 'I'), (5, 5, 'I'), (5, 6, 'I'), (5, 7, 'I'), (5, 8, 'I'), (5, 9, 'I'), (5, 10, 'I'), (5, 11, 'I'), (5, 12, 'I'), (5, 18, 'I'), (5, 19, 'I'), (5, 23, 'I'), (6, 4, 'I'), (6, 5, 'I'), (6, 6, 'I'), (6, 7, 'I'), (6, 9, 'I'), (6, 10, 'I'), (6, 11, 'I'), (6, 12, 'I'), (6, 13, 'I'), (6, 18, 'I'), (6, 19, 'I'), (6, 22, 'I'), (6, 23, 'I'), (9, 4, 'I'), (9, 5, 'I'), (9, 6, 'I'), (9, 9, 'I'), (9, 11, 'I'), (9, 12, 'I'), (9, 13, 'I'), (9, 18, 'I'), (9, 19, 'I'), (9, 22, 'I'), (9, 23, 'I'), (10, 4, 'I'), (10, 5, 'I'), (10, 6, 'I'), (10, 9, 'I'), (10, 10, 'I'), (10, 11, 'I'), (10, 12, 'I'), (10, 13, 'I'), (10, 18, 'I'), (10, 19, 'I'), (10, 22, 'I'), (11, 4, 'I'), (11, 5, 'I'), (11, 9, 'I'), (11, 10, 'I'), (11, 11, 'I'), (11, 12, 'I'), (11, 19, 'I'), (11, 22, 'I'), (11, 23, 'I'), (12, 4, 'I'), (12, 5, 'I'), (12, 6, 'I'), (12, 9, 'I'), (12, 10, 'I'), (12, 11, 'I'), (12, 12, 'I'), (12, 13, 'I'), (12, 18, 'I'), (12, 19, 'I'), (12, 22, 'I'), (12, 23, 'I'), (14, 15, 'I'), (14, 16, 'I'), (15, 15, 'I'), (15, 16, 'I'), (17, 4, 'I'), (17, 5, 'I'), (17, 6, 'I'), (17, 7, 'I'), (17, 10, 'I'), (17, 11, 'I'), (17, 12, 'I'), (17, 13, 'I'), (17, 18, 'I'), (17, 19, 'I'), (17, 20, 'I'), (17, 21, 'I'), (17, 22, 'I'), (17, 23, 'I'), (18, 5, 'I'), (18, 6, 'I'), (18, 7, 'I'), (18, 10, 'I'), (18, 11, 'I'), (18, 12, 'I'), (18, 13, 'I'), (18, 18, 'I'), (18, 20, 'I'), (18, 22, 'I'), (18, 23, 'I'), (19, 4, 'I'), (19, 5, 'I'), (19, 6, 'I'), (19, 7, 'I'), (19, 10, 'I'), (19, 11, 'I'), (19, 12, 'I'), (19, 13, 'I'), (20, 4, 'I'), (20, 5, 'I'), (20, 6, 'I'), (20, 7, 'I'), (20, 10, 'I'), (20, 11, 'I'), (20, 12, 'I'), (20, 13, 'I'), (21, 4, 'I'), (21, 5, 'I'), (21, 6, 'I'), (21, 11, 'I'), (21, 12, 'I'), (21, 13, 'I'), (21, 18, 'I'), (21, 19, 'I'), (21, 20, 'I'), (21, 22, 'I'), (21, 23, 'I'), (22, 4, 'I'), (22, 5, 'I'), (22, 6, 'I'), (22, 7, 'I'), (22, 10, 'I'), (22, 11, 'I'), (22, 12, 'I'), (22, 13, 'I'), (22, 18, 'I'), (22, 19, 'I'), (22, 20, 'I'), (22, 21, 'I'), (22, 22, 'I'), (22, 23, 'I')]
semaforos = []

class Vehiculo(Agent):
    """ Vehicle agent with speed, direction, type, and state attributes. """
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.speed = random.randint(1, 5)  # Speed between 1 and 5
        self.direction = random.choice([(1, 1), (-1, 0), (0, 1), (0, -1)])  # Random direction
        self.vehicle_type = random.randint(1, 4)  # Random vehicle type (1-4)
        self.state = random.randint(1, 3)  # Random state (1: moving, 2: idle, 3: parked)
    
    def move(self):
        """ Move the vehicle in the current direction. """
        if self.state == 1:  # If the vehicle is moving
            x, y = self.pos
            dx, dy = self.direction
            new_pos = (x + dx * self.speed, y + dy * self.speed)

            # Ensure the vehicle moves within the grid bounds
            if self.model.grid.is_cell_empty(new_pos):
                self.model.grid.move_agent(self, new_pos)
    
    def change_direction(self):
        """ Change direction randomly. """
        self.direction = random.choice([(1, 1), (-1, 0), (0, 1), (0, -1)])
    
    def step(self):
        """ Perform one step in the simulation. """
        self.move()
        # Add logic to change direction or state if necessary (optional)
        if random.random() < 0.1:  # Example: 10% chance to change direction
            self.change_direction()

"""
Clase semaforo:
    - Atributos:
        - Estado: Random entre 1 y 3, en verde, en amarillo y en rojo
    - Metodos:
        - Cambiar de estado
"""
class Semaforo(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = random.choice(["verde", "rojo"])  # Estado inicial del semáforo
        self.timer = 0

    def step(self):
        # Cambiar de estado cada ciertos pasos
        self.timer += 1
        if self.timer >= 5:  # Cambiar cada 5 pasos
            self.state = "verde" if self.state == "rojo" else "rojo"
            self.timer = 0

"""

"""
class Celda(Agent):
    """Agente que representa un cuadro fijo."""
    def __init__(self, unique_id, model, direction, tipo):
        super().__init__(unique_id, model)
        self.direccion = direction
        self.tipo = tipo  # Define el tipo de celda

"""
"""
class Parking(Agent):
    """Estacionamiento en el grid."""
    def __init__(self, model, pos):
        super().__init__(model)
        self.pos = pos
    
    def step(self):
        pass  # Los estacionamientos no necesitan hacer nada, solo se dibujan

class TraficoModel(Model):
    """Modelo que incluye vehículos, semáforos y celdas transitables."""
    def __init__(self, N, width, height, transitables, estacionamientos, no_transitable):
        super().__init__()
        self.num_autos = N
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)

        # Agregar celdas para transitables tipo 1
        for idx, (x, y, direccion) in enumerate(transitables):
            agente = Celda(idx, self, direccion, "tipo1")
            self.grid.place_agent(agente, (x, y))
            self.schedule.add(agente)

        # Agregar celdas para transitables tipo 2
        for idx, (x, y, direccion) in enumerate(estacionamientos):
            agente = Celda(idx + len(transitables), self, direccion, "tipo2")
            self.grid.place_agent(agente, (x, y))
            self.schedule.add(agente)

        # Agregar celdas para transitables tipo 3
        for idx, (x, y, direccion) in enumerate(no_transitable):
            agente = Celda(idx + len(transitables) + len(estacionamientos), self, direccion, "tipo3")
            self.grid.place_agent(agente, (x, y))
            self.schedule.add(agente)

        
        # Agregar autos
        for i in range(self.num_autos):
            auto = Vehiculo(i, self)
            # Seleccionar una posición transitable aleatoria con dirección
            x, y, direccion = random.choice(transitables)  # Asegúrate de que 'transitables' tenga tripletas (x, y, dirección)
            auto.direccion = direccion  # Almacena la dirección en el auto
            self.grid.place_agent(auto, (x, y))  # Coloca el auto en la rejilla usando solo (x, y)
            self.schedule.add(auto)  # Agrega el auto al scheduler

        # Agregar semáforos
        for i in range(1):  # Agregar 1 semáforo (puedes agregar más)
            semaforo = Semaforo(self.num_autos + i, self)
            x, y, direccion = random.choice(transitables)  # Asegúrate de que 'transitables' tenga tripletas (x, y, dirección)
            self.grid.place_agent(semaforo, (x, y))
            self.schedule.add(semaforo)

    def step(self):
        """Avanzar un paso en la simulación."""
        self.schedule.step()

def agentPortrayal(agent):
    """Definir cómo se dibujan los agentes en el canvas."""
    if isinstance(agent, Celda):
        # Asignar color según el tipo
        if agent.tipo == "tipo1":
            color = "white"
        elif agent.tipo == "tipo2":
            color = "yellow"
        elif agent.tipo == "tipo3":
            color = "blue"
        else:
            color = "gray"  # Color predeterminado para tipos desconocidos
        
        return {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": color,
            "w": 1,
            "h": 1
        }
    elif isinstance(agent, Vehiculo):
        return {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 1,
            "Color": "purple",
            "r": 1
        }
    elif isinstance(agent, Semaforo):
        color = "red" if agent.state == "rojo" else "green" if agent.state == "verde" else "yellow"
        return {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 2,
            "Color": color,
            "w": 2,
            "h": 1
        }

# Crear el modelo
model = TraficoModel(1, 26, 26, transitables, estacionamientos, no_transitable)
for _ in range(10):  # Run for 10 steps
    model.step()

canvas_element = CanvasGrid(agentPortrayal, 26, 26, 500, 500)
server = ModularServer(
    TraficoModel,
    [canvas_element],
    "Simulación de Tráfico",
    {"N": 1, "width": 26, "height": 26, "transitables": transitables, "estacionamientos": estacionamientos, "no_transitable": no_transitable}
)

# Ejecutar el servidor
server.port = 852
server.launch()