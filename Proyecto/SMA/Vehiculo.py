# Importamos las librerías necesarias
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from Agentes import SemaforoVehicular
from queue import PriorityQueue
import networkx as nx

"""
Clase Vehiculo:

La clase Vehiculo representa un vehículo que puede moverse entre diferentes coordenadas, 
considerando su estado, origen, destino, y direcciones disponibles. Además, puede detectar
a otros agentes vehiculos y semáforos en su camino.

Atributos:
    estado (int): Indica el estado del vehículo. 2 representa un vehículo estacionado, 1 representa un vehículo en movimiento.
    origen (tuple): Coordenadas del estacionamiento de origen.
    destino (tuple): Coordenadas del estacionamiento de destino.
    direcciones (list): Lista de direcciones posibles que el vehículo puede tomar.
    tiempo_arrivo (float): Tiempo estimado de llegada al destino.

Métodos:
    moverse(): Cambia el estado del vehículo a "en movimiento" y actualiza su posición.
    cambiar_direccion(pos_actual, pos_siguiente, direccion_actual, direccion_siguiente): Cambia la dirección del vehículo entre posiciones.
    buscar_destino(origen, destino): Encuentra una ruta desde el origen hasta el destino.
    detectar_obstaculo(pos_siguiente): Detecta si hay un obstáculo en la siguiente posición.
    validar_dirección(pos_siguiente): Valida si la dirección del vehículo es correcta respecto al mapa.
    validar_semaforo(pos_siguiente): Valida si el semáforo permite el paso en la siguiente posición.
    validar_vuelta: Valida si el vehículo en sus 4 celdas adyacentes puede quiere realizar un giro.
    validar_freno: Valida si el vehículo delante en su celda siguiente puede frenar.
    step(): Realiza un paso del movimiento del vehículo, verificando todas las condiciones necesarias.
"""
class Vehiculo(Agent):
    """Agente vehículo que navega hacia su destino utilizando un grafo conectado."""

    def __init__(self, unique_id, model, origen, destino, semaforosV, transitables, estacionamientos):
        super().__init__(unique_id, model)
        self.origen = origen
        self.pos_actual = origen
        self.destino = destino
        self.semaforosV = semaforosV
        self.transitables = transitables
        self.estacionamientos = estacionamientos
        self.grafo = self.crear_grafo_conectado()
        self.ruta = []

    def crear_grafo_conectado(self):
        """Construye un grafo dirigido basado en las celdas transitables y estacionamientos."""
        grafo = nx.DiGraph()

        # Agregar nodos y conexiones para transitables
        for direccion, nodos in self.transitables.items():
            for nodo in nodos:
                if direccion == "N":
                    vecino = (nodo[0], nodo[1] + 1)
                elif direccion == "S":
                    vecino = (nodo[0], nodo[1] - 1)
                elif direccion == "E":
                    vecino = (nodo[0] + 1, nodo[1])
                elif direccion == "O":
                    vecino = (nodo[0] - 1, nodo[1])
                else:
                    continue
                if vecino in nodos or vecino in [c for lista in self.transitables.values() for c in lista]:
                    grafo.add_edge(nodo, vecino, direccion=direccion)

        # Agregar estacionamientos
        for estacionamiento in self.estacionamientos.values():
            grafo.add_node(estacionamiento)

        return grafo
    
    def validar_estado_semaforo(self, pos):
        """
        Verifica si el semáforo en la posición dada permite el paso.

        Args:
            pos (tuple): Coordenada de la próxima posición.

        Returns:
            bool: True si el semáforo está en verde o si no hay semáforo en la posición, False de lo contrario.
        """
        # Obtener los agentes en la posición objetivo
        agentes_en_pos = self.model.grid.get_cell_list_contents([pos])
        
        # Filtrar los semáforos vehiculares en la posición
        semaforos = [agente for agente in agentes_en_pos if isinstance(agente, SemaforoVehicular)]

        # Si no hay semáforos en la posición, el paso está permitido
        if not semaforos:
            print(f"Vehículo {self.unique_id}: No hay semáforo en {pos}, paso permitido.")
            return True

        # Verificar el estado de los semáforos
        for semaforo in semaforos:
            if semaforo.state == "rojo":
                print(f"Vehículo {self.unique_id}: Semáforo en {pos} está en ROJO, paso no permitido.")
                return False  # Detenerse si al menos un semáforo está en rojo

        # Si todos los semáforos permiten el paso
        print(f"Vehículo {self.unique_id}: Semáforo en {pos} está en VERDE, paso permitido.")
        return True

    def validar_vecinos(self, radio=2, filtro=None):
        """Valida los vecinos dentro de un radio y aplica un filtro opcional."""
        vecinos = self.model.grid.get_neighborhood(
            self.pos_actual, moore=False, include_center=False, radius=radio
        )
        if filtro:
            vecinos = [v for v in vecinos if filtro(v)]
        return vecinos

    def calcular_ruta(self):
        """Calcula la ruta más corta al destino utilizando A*."""
        if self.destino not in self.grafo.nodes:
            print(f"Destino {self.destino} no es transitable ni un estacionamiento.")
            return []
        try:
            ruta = nx.astar_path(
                self.grafo, source=self.pos_actual, target=self.destino, heuristic=self.distancia, weight='weight'
            )
            print(f"Ruta calculada para el vehículo {self.unique_id}: {ruta}")
            return ruta
        except nx.NetworkXNoPath:
            print(f"No hay ruta del origen {self.pos_actual} al destino {self.destino}.")
            return []

    def moverse(self):
        """Realiza el movimiento del vehículo, incluyendo validaciones."""
        if self.pos_actual in self.estacionamientos.values():
            if self.salir_estacionamiento():
                return

        if not self.ruta or self.pos_actual not in self.ruta:
            self.ruta = self.calcular_ruta()

        siguiente_pos = None
        if self.ruta:
            siguiente_pos = self.ruta.pop(0)
        else:
            vecinos_validos = self.validar_vecinos(
                filtro=lambda v: (self.pos_actual, v) in self.grafo.edges
            )
            if vecinos_validos:
                siguiente_pos = min(
                    vecinos_validos, key=lambda v: self.distancia(v, self.destino)
                )

        if siguiente_pos:
            # Validar estado del semáforo antes de moverse
            if not self.validar_estado_semaforo(siguiente_pos):
                print(f"Vehículo {self.unique_id}: Detenido en {self.pos_actual} por semáforo en rojo.")
                return  # Detenerse si el semáforo no permite el paso

            self.model.grid.move_agent(self, siguiente_pos)
            self.pos_actual = siguiente_pos
            print(f"Vehículo {self.unique_id}: Se movió a {self.pos_actual}")

    def validar_semaforo(self, pos):
        """
        Verifica si el semáforo en la posición dada está en verde.

        Args:
            pos (tuple): Coordenada de la próxima posición.

        Returns:
            bool: True si el semáforo permite el paso, False de lo contrario.
        """
        agentes_en_pos = self.model.grid.get_cell_list_contents([pos])
        semaforos = [a for a in agentes_en_pos if isinstance(a, SemaforoVehicular)]

        if not semaforos:
            # Si no hay semáforo, se asume que el paso está permitido
            return True

        for semaforo in semaforos:
            if semaforo.state == "rojo":
                return False  # Semáforo en rojo, no se permite el paso

        return True  # Todos los semáforos en verde


    def validar_restricciones(self, celda):
        """
        Valida si el vehículo puede moverse a la celda especificada.
        Se asegura de que no haya vehículos en conflicto en las celdas ortogonales
        y en las celdas adyacentes.
        """
        print(f"Vehículo {self.unique_id}: Verificando restricciones para moverse a {celda}.")

        # Determinar la dirección de movimiento
        direccion = (celda[0] - self.pos_actual[0], celda[1] - self.pos_actual[1])

        # Primera fase: Verificar celdas ortogonales
        celdas_ortogonales = {
            (0, 1): [(self.pos_actual[0], self.pos_actual[1] + 1)],  # Norte
            (0, -1): [(self.pos_actual[0], self.pos_actual[1] - 1)],  # Sur
            (1, 0): [(self.pos_actual[0] + 1, self.pos_actual[1])],  # Este
            (-1, 0): [(self.pos_actual[0] - 1, self.pos_actual[1])],  # Oeste
        }.get(direccion, [])

        for celda_ortogonal in celdas_ortogonales:
            agentes_en_celda = self.model.grid.get_cell_list_contents([celda_ortogonal])
            agentes_carros = [agente for agente in agentes_en_celda if isinstance(agente, Vehiculo) and agente != self]
            for agente in agentes_carros:
                # Asegurarse de no detenerse por vehículos detrás
                if (agente.pos_actual[0] - self.pos_actual[0], agente.pos_actual[1] - self.pos_actual[1]) == (-direccion[0], -direccion[1]):
                    print(f"Vehículo {self.unique_id}: Ignorando vehículo detrás ({agente.unique_id}).")
                    continue

                if agente.pos_actual[0] == celda_ortogonal[0] or agente.pos_actual[1] == celda_ortogonal[1]:
                    print(f"Vehículo {self.unique_id}: Encontró conflicto con {agente.unique_id} en {celda_ortogonal}")
                    return False  # Esperar si hay un vehículo en la celda ortogonal alineado

        # Segunda fase: Verificar vecinos adyacentes (8 celdas alrededor de la posición actual)
        vecinos = self.model.grid.get_neighborhood(
            self.pos_actual, moore=True, include_center=False, radius=1
        )
        for vecino in vecinos:
            agentes_en_vecino = self.model.grid.get_cell_list_contents([vecino])
            agentes_carros_vecino = [agente for agente in agentes_en_vecino if isinstance(agente, Vehiculo) and agente != self]
            if agentes_carros_vecino:
                print(f"Vehículo {self.unique_id}: Esperando porque encontró vehículos cruzando en vecino {vecino}: {agentes_carros_vecino}")
                return False

        # Si pasa ambas fases, se permite el movimiento
        print(f"Vehículo {self.unique_id}: No se encontraron restricciones para moverse a {celda}.")
        return True

    def salir_estacionamiento(self):
        """Mueve al vehículo desde el estacionamiento a una celda conectada al grafo o transitable."""
        vecinos_conectados = self.validar_vecinos(filtro=lambda v: v in self.grafo.nodes)
        if vecinos_conectados:
            siguiente_pos = vecinos_conectados[0]
        else:
            vecinos_transitables = self.validar_vecinos(filtro=lambda v: v in [c for lista in self.transitables.values() for c in lista])
            siguiente_pos = vecinos_transitables[0] if vecinos_transitables else None

        if siguiente_pos and self.validar_restricciones(siguiente_pos):
            self.model.grid.move_agent(self, siguiente_pos)
            self.pos_actual = siguiente_pos
            print(f"Vehículo {self.unique_id}: Salió del estacionamiento hacia {self.pos_actual}")
            return True
        return False

    def distancia(self, pos1, pos2):
        """Calcula la distancia Manhattan entre dos posiciones."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def step(self):
        """Realiza un paso en la simulación."""
        print(f"Vehículo {self.unique_id}: Posición actual: {self.pos_actual}, Destino: {self.destino}")
        self.moverse()
