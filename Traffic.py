from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random

class Vehiculo(Agent):
    """Agente de vehículo con comportamiento para moverse entre estacionamientos, evitar obstáculos y respetar semáforos."""

    def __init__(self, unique_id, model, direccion):
        super().__init__(unique_id, model)
        self.velocidad = random.randint(1, 5)  # Velocidad aleatoria entre 1 y 5
        self.direccion = direccion
        self.tipo = random.randint(1, 4)  # Tipo de vehículo
        self.estado = 1
        self.pos = None  # La posición del vehículo aún no está definida
        self.destino = None  # El vehículo no tiene un destino asignado

    def inicializar_posicion(self, posicion_inicial):
        """ Asignar una posición inicial al vehículo. """
        self.pos = posicion_inicial
        self.model.grid.place_agent(self, self.pos)  # Coloca al vehículo en la rejilla
    
    def asignar_destino(self, destino):
        """ Asigna un destino al vehículo. """
        self.destino = destino
    
    def moverse(self):
        if self.estado == 1:  # Solo se mueve si está en estado "avanzando"
            nueva_pos = (self.pos[0] + self.direccion[0], self.pos[1] + self.direccion[1])
            
            # Verificar si la nueva posición es válida
            if self.model.grid.is_cell_empty(nueva_pos) or self.es_transitable(nueva_pos):
                # Mover al vehículo si la celda es vacía o transitables
                self.model.grid.move_agent(self, nueva_pos)
                self.pos = nueva_pos  # Actualizar la posición del vehículo
            else:
                # Cambiar dirección si no puede avanzar
                self.cambiar_direccion()

    def cambiar_direccion(self):
        """ Cambiar la dirección a una dirección válida. """
        posibles_direcciones = [
            (dx, dy) 
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if self.model.grid.is_cell_empty((self.pos[0] + dx, self.pos[1] + dy)) or self.es_transitable((self.pos[0] + dx, self.pos[1] + dy))
        ]
        
        if posibles_direcciones:
            self.direccion = random.choice(posibles_direcciones)

    def buscar_destino(self):
        """Busca un estacionamiento diferente al actual y ajusta su dirección."""
        estacionamientos_disponibles = [
            (x, y) for x, y, _ in self.model.estacionamientos if (x, y) != self.pos
        ]
        if estacionamientos_disponibles:
            self.destino = random.choice(estacionamientos_disponibles)

    def detectar_obstaculo(self, nueva_pos):
        """Detecta si hay otro vehículo en la posición hacia la que se desea mover."""
        agentes = self.model.grid.get_cell_list_contents([nueva_pos])
        return any(isinstance(agente, Vehiculo) for agente in agentes)

    def respetar_semaforo(self):
        """Detiene el vehículo si hay un semáforo en rojo frente a él."""
        siguiente_pos = (self.pos[0] + self.direccion[0], self.pos[1] + self.direccion[1])
        agentes = self.model.grid.get_cell_list_contents([siguiente_pos])
        for agente in agentes:
            if isinstance(agente, Semaforo) and agente.color == "rojo":
                self.estado = 0  # Detener el vehículo
                return
        self.estado = 1  # Continuar si no hay semáforo en rojo

    def es_transitable(self, pos):
        """Verifica si la posición es transitable."""
        return pos in [(x, y) for x, y, _ in self.model.transitables]

    def step(self):
        """Ejecuta un paso en la simulación."""
        self.respetar_semaforo()  # Primero verifica semáforos
        if self.destino:  # Si tiene un destino asignado, ajusta la dirección
            self.ajustar_direccion_hacia_destino()
        self.moverse()

    def ajustar_direccion_hacia_destino(self):
        """Ajusta la dirección para moverse hacia el destino utilizando una heurística simple."""
        dx = self.destino[0] - self.pos[0]
        dy = self.destino[1] - self.pos[1]
        if abs(dx) > abs(dy):
            self.direccion = (1 if dx > 0 else -1, 0)
        else:
            self.direccion = (0, 1 if dy > 0 else -1)

"""
Clase semaforo:
    - Atributos:
        - Estado: Random entre 1 y 3, en verde, en amarillo y en rojo
    - Metodos:
        - Cambiar de estado
"""
class Semaforo(Agent):
    estados = ["verde", "amarillo", "rojo"]

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = random.choice(["verde", "rojo"])
        self.timer = 0

    def step(self):
        self.timer += 1
        if self.timer >= 5:  # Ciclo de cambio de estado
            current_index = self.estados.index(self.state)
            self.state = self.estados[(current_index + 1) % len(self.estados)]
            self.timer = 0

class Celda(Agent):
    """Agente que representa un cuadro fijo de color verde."""
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.direccion = direction

class ModeloTrafico(Model):
    """Modelo que fija cuadros verdes en posiciones específicas del grid."""
    def __init__(self, width, height, transitables, estacionamientos, intransitables, semaforos):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        # Asignar las listas como atributos de la instancia
        self.transitables = transitables
        self.estacionamientos = estacionamientos
        self.intransitables = intransitables
        self.semaforos = semaforos
        # Agregar semáforos
        self.inicializar_semaforos(semaforos)

        # Agregar agentes en posiciones específicas
        for idx, (x, y, direccion) in enumerate(transitables):
            agente = Celda(idx, self, direccion)
            self.grid.place_agent(agente, (x, y))
            self.schedule.add(agente)

        for idx, (x, y, direccion) in enumerate(estacionamientos):
            agente = Celda(idx, self, direccion)
            self.grid.place_agent(agente, (x, y))
            self.schedule.add(agente)

        for idx, (x, y, direccion) in enumerate(intransitables):
            agente = Celda(idx, self, direccion)
            self.grid.place_agent(agente, (x, y))
            self.schedule.add(agente)

        # Agregar autos al modelo
        for i in range(1):
            # Seleccionar una posición transitable aleatoria con dirección cardinal
            x, y, direccion_cardinal = random.choice(estacionamientos)
            
            # Traducir dirección cardinal a desplazamiento
            direccion = direcciones[direccion_cardinal]
            
            # Crear el auto y asignar dirección
            auto = Vehiculo(i, self, direccion)
            
            # Colocar el auto en la rejilla y agregarlo al scheduler
            self.grid.place_agent(auto, (x, y))
            self.schedule.add(auto)

    # Agregar semáforos
    def inicializar_semaforos(self, semaforos):
        for i, (x, y, _) in enumerate(semaforos):
            semaforo = Semaforo(i, self)
            self.grid.place_agent(semaforo, (x, y))
            self.schedule.add(semaforo)
    
    def step(self):
        self.schedule.step()


def agentPortrayal(agent):
    if isinstance(agent, Celda):
        
        if agent.direccion == "P":
            color = "yellow"
        elif agent.direccion == "I":
            color = "blue"
        else:
            color = "white"
        
        return {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": color,
            "w": 1,
            "h": 1
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
    elif isinstance(agent, Vehiculo):
        return {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 1,
            "Color": "purple",
            "r": 1
        }
    
# Coordenadas específicas para la parte transitable, semáforos y estacionamientos del grid
transitables = [(1, 24, 'S'), (2, 24, 'O'), (3, 24, 'O'), (4, 24, 'O'), (5, 24, 'O'), (6, 24, 'O'), (7, 24, 'O'), (8, 24, 'O'), (9, 24, 'O'), (10, 24, 'O'), (11, 24, 'O'), (12, 24, 'O'), (13, 24, 'O'), (14, 24, 'O'), (15, 24, 'O'), (16, 24, 'O'), (17, 24, 'O'), (18, 24, 'O'), (19, 24, 'O'), (20, 24, 'O'), (21, 24, 'O'), (22, 24, 'O'), (23, 24, 'O'), (24, 24, 'O'), (1, 23, 'S'), (2, 23, 'O'), (3, 23, 'O'), (4, 23, 'O'), (5, 23, 'O'), (6, 23, 'O'), (7, 23, 'O'), (8, 23, 'O'), (9, 23, 'O'), (10, 23, 'O'), (11, 23, 'O'), (12, 23, 'O'), (13, 23, 'O'), (14, 23, 'O'), (15, 23, 'O'), (16, 23, 'O'), (17, 23, 'O'), (18, 23, 'O'), (19, 23, 'O'), (20, 23, 'O'), (21, 23, 'O'), (22, 23, 'O'), (23, 23, 'N'), (24, 23, 'N'), (1, 22, 'S'), (2, 22, 'S'), (7, 22, 'N'), (8, 22, 'N'), (13, 22, 'S'), (14, 22, 'S'), (15, 22, 'N'), (16, 22, 'N'), (23, 22, 'N'), (24, 22, 'N'), (1, 21, 'S'), (2, 21, 'S'), (7, 21, 'N'), (8, 21, 'N'), (13, 21, 'S'), (14, 21, 'S'), (15, 21, 'N'), (16, 21, 'N'), (23, 21, 'N'), (24, 21, 'N'), (1, 20, 'S'), (2, 20, 'S'), (7, 20, 'N'), (8, 20, 'N'), (13, 20, 'S'), (14, 20, 'S'), (15, 20, 'N'), (16, 20, 'N'), (23, 20, 'N'), (24, 20, 'N'), (1, 19, 'S'), (2, 19, 'S'), (7, 19, 'N'), (8, 19, 'N'), (9, 19, 'O'), (10, 19, 'O'), (11, 19, 'O'), (12, 19, 'O'), (13, 19, 'S'), (14, 19, 'S'), (15, 19, 'N'), (16, 19, 'N'), (23, 19, 'N'), (24, 19, 'N'), (1, 18, 'S'), (2, 18, 'S'), (7, 18, 'N'), (8, 18, 'N'), (9, 18, 'O'), (10, 18, 'O'), (11, 18, 'O'), (12, 18, 'O'), (13, 18, 'S'), (14, 18, 'S'), (15, 18, 'N'), (16, 18, 'N'), (17, 18, 'O'), (18, 18, 'O'), (19, 18, 'O'), (20, 18, 'O'), (21, 18, 'O'), (22, 18, 'O'), (23, 18, 'N'), (24, 18, 'N'), (1, 17, 'S'), (2, 17, 'S'), (7, 17, 'N'), (8, 17, 'N'), (13, 17, 'S'), (14, 17, 'S'), (15, 17, 'N'), (16, 17, 'N'), (17, 17, 'O'), (18, 17, 'O'), (19, 17, 'O'), (20, 17, 'O'), (21, 17, 'O'), (22, 17, 'O'), (23, 17, 'N'), (24, 17, 'N'), (1, 16, 'S'), (2, 16, 'S'), (7, 16, 'N'), (8, 16, 'N'), (13, 16, 'S'), (14, 16, 'S'), (15, 16, 'N'), (16, 16, 'N'), (23, 16, 'N'), (24, 16, 'N'), (1, 15, 'S'), (2, 15, 'S'), (7, 15, 'N'), (8, 15, 'N'), (13, 15, 'S'), (14, 15, 'S'), (15, 15, 'N'), (16, 15, 'N'), (23, 15, 'N'), (24, 15, 'N'), (1, 14, 'S'), (2, 14, 'S'), (7, 14, 'N'), (8, 14, 'N'), (13, 14, 'S'), (14, 14, 'S'), (15, 14, 'N'), (16, 14, 'N'), (23, 14, 'N'), (24, 14, 'N'), (1, 13, 'S'), (2, 13, 'S'), (7, 13, 'N'), (8, 13, 'N'), (13, 13, 'S'), (14, 13, 'S'), (15, 13, 'N'), (16, 13, 'N'), (23, 13, 'N'), (24, 13, 'N'), (1, 12, 'S'), (2, 12, 'S'), (3, 12, 'O'), (4, 12, 'O'), (5, 12, 'O'), (6, 12, 'O'), (7, 12, 'O'), (8, 12, 'O'), (9, 12, 'O'), (10, 12, 'O'), (11, 12, 'O'), (12, 12, 'O'), (13, 12, 'O'), (14, 12, 'O'), (15, 12, 'O'), (16, 12, 'N'), (17, 12, 'O'), (18, 12, 'O'), (19, 12, 'O'), (20, 12, 'O'), (21, 12, 'O'), (22, 12, 'O'), (23, 12, 'N'), (24, 12, 'N'), (1, 11, 'S'), (2, 11, 'S'), (3, 11, 'O'), (4, 11, 'O'), (5, 11, 'O'), (6, 11, 'O'), (7, 11, 'O'), (8, 11, 'O'), (9, 11, 'O'), (10, 11, 'O'), (11, 11, 'O'), (12, 11, 'O'), (13, 11, 'S'), (16, 11, 'N'), (17, 11, 'O'), (18, 11, 'O'), (19, 11, 'O'), (20, 11, 'O'), (21, 11, 'O'), (22, 11, 'O'), (23, 11, 'N'), (24, 11, 'N'), (1, 10, 'S'), (2, 10, 'S'), (3, 10, 'E'), (4, 10, 'E'), (5, 10, 'E'), (6, 10, 'E'), (7, 10, 'E'), (8, 10, 'E'), (9, 10, 'E'), (10, 10, 'E'), (11, 10, 'E'), (12, 10, 'E'), (13, 10, 'S'), (16, 10, 'N'), (17, 10, 'E'), (18, 10, 'E'), (19, 10, 'E'), (20, 10, 'E'), (21, 10, 'E'), (22, 10, 'E'), (23, 10, 'N'), (24, 10, 'N'), (1, 9, 'S'), (2, 9, 'S'), (3, 9, 'E'), (4, 9, 'E'), (5, 9, 'E'), (6, 9, 'E'), (7, 9, 'E'), (8, 9, 'E'), (9, 9, 'E'), (10, 9, 'E'), (11, 9, 'E'), (12, 9, 'E'), (13, 9, 'S'), (14, 9, 'E'), (15, 9, 'E'), (16, 9, 'E'), (17, 9, 'E'), (18, 9, 'E'), (19, 9, 'E'), (20, 9, 'E'), (21, 9, 'E'), (22, 9, 'E'), (23, 9, 'N'), (24, 9, 'N'), (1, 8, 'S'), (2, 8, 'S'), (7, 8, 'S'), (8, 8, 'S'), (13, 8, 'S'), (14, 8, 'S'), (15, 8, 'N'), (16, 8, 'N'), (19, 8, 'N'), (20, 8, 'N'), (23, 8, 'N'), (24, 8, 'N'), (1, 7, 'S'), (2, 7, 'S'), (7, 7, 'S'), (8, 7, 'S'), (13, 7, 'S'), (14, 7, 'S'), (15, 7, 'N'), (16, 7, 'N'), (19, 7, 'N'), (20, 7, 'N'), (23, 7, 'N'), (24, 7, 'N'), (1, 6, 'S'), (2, 6, 'S'), (3, 6, 'O'), (4, 6, 'O'), (5, 6, 'O'), (6, 6, 'O'), (7, 6, 'S'), (8, 6, 'S'), (9, 6, 'E'), (10, 6, 'E'), (11, 6, 'E'), (12, 6, 'E'), (13, 6, 'S'), (14, 6, 'S'), (15, 6, 'N'), (16, 6, 'N'), (19, 6, 'N'), (20, 6, 'N'), (23, 6, 'N'), (24, 6, 'N'), (1, 5, 'S'), (2, 5, 'S'), (3, 5, 'O'), (4, 5, 'O'), (5, 5, 'O'), (6, 5, 'O'), (7, 5, 'S'), (8, 5, 'S'), (9, 5, 'E'), (10, 5, 'E'), (11, 5, 'E'), (12, 5, 'E'), (13, 5, 'S'), (14, 5, 'S'), (15, 5, 'N'), (16, 5, 'N'), (19, 5, 'N'), (20, 5, 'N'), (23, 5, 'N'), (24, 5, 'N'), (1, 4, 'S'), (2, 4, 'S'), (7, 4, 'S'), (8, 4, 'S'), (13, 4, 'S'), (14, 4, 'S'), (15, 4, 'N'), (16, 4, 'N'), (19, 4, 'N'), (20, 4, 'N'), (23, 4, 'N'), (24, 4, 'N'), (1, 3, 'S'), (2, 3, 'S'), (7, 3, 'S'), (8, 3, 'S'), (13, 3, 'S'), (14, 3, 'S'), (15, 3, 'N'), (16, 3, 'N'), (19, 3, 'N'), (20, 3, 'N'), (23, 3, 'N'), (24, 3, 'N'), (1, 2, 'S'), (2, 2, 'S'), (3, 2, 'E'), (4, 2, 'E'), (5, 2, 'E'), (6, 2, 'E'), (7, 2, 'E'), (8, 2, 'E'), (9, 2, 'E'), (10, 2, 'E'), (11, 2, 'E'), (12, 2, 'E'), (13, 2, 'E'), (14, 2, 'E'), (15, 2, 'E'), (16, 2, 'E'), (17, 2, 'E'), (18, 2, 'E'), (19, 2, 'E'), (20, 2, 'E'), (21, 2, 'E'), (22, 2, 'E'), (23, 2, 'E'), (24, 2, 'N'), (1, 1, 'E'), (2, 1, 'E'), (3, 1, 'E'), (4, 1, 'E'), (5, 1, 'E'), (6, 1, 'E'), (7, 1, 'E'), (8, 1, 'E'), (9, 1, 'E'), (10, 1, 'E'), (11, 1, 'E'), (12, 1, 'E'), (13, 1, 'E'), (14, 1, 'E'), (15, 1, 'E'), (16, 1, 'E'), (17, 1, 'E'), (18, 1, 'E'), (19, 1, 'E'), (20, 1, 'E'), (21, 1, 'E'), (22, 1, 'E'), (23, 1, 'E'), (24, 1, 'N')]  
semaforos = [(1, 7, 'H'), (7, 3, 'H'), (19, 8, 'H'), (7, 17, 'H'), (7, 22, 'H'), (3, 6, 'V'), (6, 2, 'V'), (18, 10, 'V'), (9, 19, 'V'), (9, 24, 'V')]
estacionamientos = [(4, 22, 'P'), (18, 22, 'P'), (11, 20, 'P'), (6, 18, 'P'), (21, 19, 'P'), (9, 16, 'P'), (21, 16, 'P'), (3, 15, 'P'), (5, 13, 'P'), (11, 13, 'P'), (11, 8, 'P'), (4, 7, 'P'), (18, 7, 'P'), (5, 4, 'P'), (18, 5, 'P'), (21, 5, 'P'), (10, 3, 'P')] 
intransitables = [(3, 3, 'I'), (3, 4, 'I'), (3, 7, 'I'), (3, 8, 'I'), (3, 13, 'I'), (3, 14, 'I'), (3, 16, 'I'), (3, 17, 'I'), (3, 18, 'I'), (3, 19, 'I'), (3, 20, 'I'), (3, 21, 'I'), (3, 22, 'I'), (4, 3, 'I'), (4, 4, 'I'), (4, 8, 'I'), (4, 13, 'I'), (4, 14, 'I'), (4, 15, 'I'), (4, 16, 'I'), (4, 17, 'I'), (4, 18, 'I'), (4, 19, 'I'), (4, 20, 'I'), (4, 21, 'I'), (5, 3, 'I'), (5, 7, 'I'), (5, 8, 'I'), (5, 14, 'I'), (5, 15, 'I'), (5, 16, 'I'), (5, 17, 'I'), (5, 18, 'I'), (5, 19, 'I'), (5, 20, 'I'), (5, 21, 'I'), (5, 22, 'I'), (6, 3, 'I'), (6, 4, 'I'), (6, 7, 'I'), (6, 8, 'I'), (6, 13, 'I'), (6, 14, 'I'), (6, 15, 'I'), (6, 16, 'I'), (6, 17, 'I'), (6, 19, 'I'), (6, 20, 'I'), (6, 21, 'I'), (6, 22, 'I'), (9, 3, 'I'), (9, 4, 'I'), (9, 7, 'I'), (9, 8, 'I'), (9, 13, 'I'), (9, 14, 'I'), (9, 15, 'I'), (9, 17, 'I'), (9, 20, 'I'), (9, 21, 'I'), (9, 22, 'I'), (10, 4, 'I'), (10, 7, 'I'), (10, 8, 'I'), (10, 13, 'I'), (10, 14, 'I'), (10, 15, 'I'), (10, 16, 'I'), (10, 17, 'I'), (10, 20, 'I'), (10, 21, 'I'), (10, 22, 'I'), (11, 3, 'I'), (11, 4, 'I'), (11, 7, 'I'), (11, 14, 'I'), (11, 15, 'I'), (11, 16, 'I'), (11, 17, 'I'), (11, 21, 'I'), (11, 22, 'I'), (12, 3, 'I'), (12, 4, 'I'), (12, 7, 'I'), (12, 8, 'I'), (12, 13, 'I'), (12, 14, 'I'), (12, 15, 'I'), (12, 16, 'I'), (12, 17, 'I'), (12, 20, 'I'), (12, 21, 'I'), (12, 22, 'I'), (14, 10, 'I'), (14, 11, 'I'), (15, 10, 'I'), (15, 11, 'I'), (17, 3, 'I'), (17, 4, 'I'), (17, 5, 'I'), (17, 6, 'I'), (17, 7, 'I'), (17, 8, 'I'), (17, 13, 'I'), (17, 14, 'I'), (17, 15, 'I'), (17, 16, 'I'), (17, 19, 'I'), (17, 20, 'I'), (17, 21, 'I'), (17, 22, 'I'), (18, 3, 'I'), (18, 4, 'I'), (18, 6, 'I'), (18, 8, 'I'), (18, 13, 'I'), (18, 14, 'I'), (18, 15, 'I'), (18, 16, 'I'), (18, 19, 'I'), (18, 20, 'I'), (18, 21, 'I'), (19, 13, 'I'), (19, 14, 'I'), (19, 15, 'I'), (19, 16, 'I'), (19, 19, 'I'), (19, 20, 'I'), (19, 21, 'I'), (19, 22, 'I'), (20, 13, 'I'), (20, 14, 'I'), (20, 15, 'I'), (20, 16, 'I'), (20, 19, 'I'), (20, 20, 'I'), (20, 21, 'I'), (20, 22, 'I'), (21, 3, 'I'), (21, 4, 'I'), (21, 6, 'I'), (21, 7, 'I'), (21, 8, 'I'), (21, 13, 'I'), (21, 14, 'I'), (21, 15, 'I'), (21, 20, 'I'), (21, 21, 'I'), (21, 22, 'I'), (22, 3, 'I'), (22, 4, 'I'), (22, 5, 'I'), (22, 6, 'I'), (22, 7, 'I'), (22, 8, 'I'), (22, 13, 'I'), (22, 14, 'I'), (22, 15, 'I'), (22, 16, 'I'), (22, 19, 'I'), (22, 20, 'I'), (22, 21, 'I'), (22, 22, 'I')]
direcciones = {
    "N": (0, -1),  # N
    "S": (0, 1),   # S
    "E": (1, 0),   # E
    "O": (-1, 0),   # O
    "P": (0, 0)   # P
}
# Creacion del modelo
model = ModeloTrafico(25, 25, transitables, estacionamientos, intransitables, semaforos)
# Configuracion del CanvasGrid
canvas_element = CanvasGrid(agentPortrayal, 25, 25, 500, 500)
# Crear y correr el servidor
server = ModularServer(ModeloTrafico, [canvas_element], "Traffic Simulation", {"width": 25, "height": 25, "transitables": transitables, "estacionamientos": estacionamientos, "intransitables": intransitables, "semaforos": semaforos})
server.port = 852
server.launch() 