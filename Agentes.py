from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random

"""
Clase Vehiculo:
    - Atributos:
        - Estado: Inicializado en 2, que es vehiculo estacionado en un estacionamiento y 1 es en movimiento
        - Origen: Coordenadas del estacionamiento de origen
        - Destino: Coordenadas del estacionamiento de destino
        - Direcciones: Lista de direcciones que se pueden tomar
    - Metodos:
        - Moverse()
        - Cambiar_Direccion(pos_actual, pos_siguiente, direccion_actual, direccion_siguiente)
        - Buscar_Destion(origen, destino)
        - Detectar_Obstaculo(pos_siguiente)
        - Validar_Semaforo(pos siguiente)
        - Step()
"""
from queue import PriorityQueue
import random

class Vehiculo(Agent):
    """Vehicle agent with speed, direction, type, state, and destination attributes."""
    
    def __init__(self, unique_id, model, direccion, transitables, estacionamientos):
        super().__init__(unique_id, model)
        self.velocidad = random.randint(1, 5)  # Velocidad aleatoria entre 1 y 5
        self.direccion = direccion
        self.tipo = random.randint(1, 4)  # Tipo de vehículo
        self.estado = 1
        self.transitables = transitables
        self.destino = None  # Destino final del vehículo
        self.ruta = []  # Almacena los pasos del camino hacia el destino
        print(transitables.extend(estacionamientos))
        

    def establecer_destino(self, destino):
        """Set the destination for the vehicle and adjust direction."""
        self.destino = destino
        
        # Ajustar la dirección en función del destino
        self.direccion = self.calcular_direccion(self.pos, destino)
        
        # Calcular la ruta en función de la nueva dirección
        self.ruta = self.calcular_ruta(destino)

    def calcular_direccion(self, origen, destino):
        """Calculate the direction vector from the current position to the destination."""
        dx = destino[0] - origen[0]
        dy = destino[1] - origen[1]
        
        if abs(dx) > abs(dy):
            return (1, 0) if dx > 0 else (-1, 0)  # Movimiento horizontal
        elif abs(dy) > abs(dx):
            return (0, 1) if dy > 0 else (0, -1)  # Movimiento vertical
        else:
            return (1, 0) if dx > 0 else (-1, 0)  # En caso de empate, horizontal

    def calcular_ruta(self, destino):
        """Find the shortest path to the destination using A*."""
        if destino not in [(x, y) for x, y, _ in self.transitables]:
            return []  # Destino no válido
        
        # A* algorithm
        start = self.pos
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.distancia(start, destino)}

        while not open_set.empty():
            _, current = open_set.get()
            
            if current == destino:
                return self.reconstruir_camino(came_from, current)

            for dx, dy, _ in self.transitables_direcciones(current):
                neighbor = (current[0] + dx, current[1] + dy)
                if neighbor not in [(x, y) for x, y, _ in self.transitables]:
                    continue
                tentative_g_score = g_score[current] + 1
                
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.distancia(neighbor, destino)
                    open_set.put((f_score[neighbor], neighbor))
        return []  # No se encontró un camino

    def transitables_direcciones(self, pos):
        """Get valid directions based on transitables."""
        return [
            (dx, dy, d) for x, y, d in self.transitables
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if (pos[0] + dx, pos[1] + dy) == (x, y)
        ]


    def reconstruir_camino(self, came_from, current):
        """Reconstruct the path from start to destination."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def distancia(self, pos1, pos2):
        """Calculate Manhattan distance."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def moverse(self):
        """Move towards the next step in the route."""
        if self.estado == 1 and self.ruta:
            siguiente_pos = self.ruta.pop(0)
            if siguiente_pos in [(x, y) for x, y, _ in self.transitables]:
                self.model.grid.move_agent(self, siguiente_pos)

    def step(self):
        """Perform one step in the simulation."""
        self.moverse()
        
"""
Clase semaforo:
    - Atributos:
        - Estado: Random entre 1 y 3, en verde, en amarillo y en rojo
    - Metodos:
        - Cambiar de estado
"""
class Semaforo(Agent):
    estados = ["verde", "amarillo", "rojo"]

    def __init__(self, unique_id, model, direccion):
        super().__init__(unique_id, model)
        self.state = random.choice(["verde", "rojo"])
        self.timer = 0
        self.direccion = direccion

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