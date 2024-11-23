"""
Módulo que define los agentes del sistema
Autores: 
    - Emiliano Caballero Mendoza A017
    - Yael Octavio Pérez Méndez A01799842
    - José Eduardo Rosas Ponciano A017
    - Manuel Olmos A017

Este modulo contiene la definición de los agentes que se utilizarán en el sistema de tráfico

Con las clases:
    -> Vehículo
    -> Peatón
    -> Semáforo vehicular
    -> Semáforo peatonal
    -> Celda
"""

# Importamos las librerías necesarias
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue


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
    def __init__(self, unique_id, model, origen, destino, semaforosV, transitables, estacionamientos):
        super().__init__(unique_id, model)
        self.origen = origen
        self.destino = destino
        self.semaforosV = semaforosV
        self.transitables = transitables
        self.estacionamientos = estacionamientos

    def validar_direccion(self):
        """
        Verifica si existe una celda transitable adyacente al origen del vehículo.
        Retorna la celda a la que se puede mover o None si no hay celdas transitables.
        """
        x, y = self.origen
        adyacentes = [
            (x - 1, y), (x + 1, y),  # Coordenadas arriba y abajo
            (x, y - 1), (x, y + 1),  # Coordenadas izquierda y derecha
        ]

        for coordenada in adyacentes:
            for direccion, celdas in self.transitables.items():
                if coordenada in celdas:
                    print(f"Puedo moverme a la coordenada {coordenada} en dirección {direccion}.")
                    return coordenada  # Retorna la primera celda válida encontrada
        print(f"No hay direcciones transitables desde el origen {self.origen}.")
        return None

    def step(self):
        """
        Método ejecutado en cada paso de la simulación.
        El agente valida direcciones, se mueve y actualiza su posición.
        """
        nueva_posicion = self.validar_direccion()
        if nueva_posicion:
            # Mover el agente a la nueva posición
            self.model.grid.move_agent(self, nueva_posicion)
            # Actualizar el origen a la nueva posición
            self.origen = nueva_posicion
            print(f"Me moví a la posición {self.origen}.")
        else:
            print(f"El agente {self.unique_id} no puede moverse en este paso.")


"""
Clase Peaton:

La clase Peaton representa un peatón que puede moverse entre diferentes coordenadas, su estado de origen es aleatorio
y no tiene destino. Su propósito es transitar por la ciudad y evitar ser atropellado por los vehículos.

Atributos:
    estado (int): Indica el estado del peatón. 1 representa un peatón en movimiento. 2 peatón queriendo cruzar.
    decision(int): Indica la decisión del peatón. 1 representa que el peatón aprieta el botón para cruzar, 2 que el peatón no quiere cruzar.

Métodos:
    moverse(): Cambia el estado del peatón a "en movimiento" y actualiza su posición.
    cruzar(): Cambia el estado del peatón a "queriendo cruzar".
    obersevar_semaforo(): Observa el tiempo de espera al apretar el botón del semáforo peatonal y decide si cruzar o no.
    step(): Realiza un paso del movimiento del peatón, verificando todas las condiciones necesarias.
"""
class Peaton(Agent):
    def __init__(self, unique_id, model, origen, destino):
        super().__init__(unique_id, model)
        self.origen = origen
        self.destino = destino
        self.ruta = self.calcular_ruta(destino)
        self.color = "blue"  # Color para representar al peatón en el mapa

    def calcular_ruta(self, destino):
        """
        Calcula la ruta desde el origen hasta el destino usando un algoritmo simple de A*.
        """
        if destino is None or self.origen is None:
            return []
        
        start = self.origen
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.distancia(start, destino)}

        while not open_set.empty():
            _, current = open_set.get()

            if current == destino:
                return self.reconstruir_camino(came_from, current)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if neighbor not in self.model.banquetas:  # Solo moverse por banquetas
                    continue
                
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.distancia(neighbor, destino)
                    open_set.put((f_score[neighbor], neighbor))

        return []  # No se encontró un camino

    def reconstruir_camino(self, came_from, current):
        """Reconstruye el camino desde el origen al destino."""
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        return total_path

    def distancia(self, a, b):
        """Calcula la distancia Manhattan entre dos puntos."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def moverse(self):
        """Movimiento del peatón siguiendo la ruta."""
        if self.ruta:
            siguiente_pos = self.ruta.pop(0)
            self.model.grid.move_agent(self, siguiente_pos)

    def step(self):
        """Ejecución de un paso del agente."""
        self.moverse()


"""
Clase SemaforoPeatonal:

La clase SemaforoPeatonal representa un semáforo peatonal que puede cambiar su estado entre "verde" y "rojo".
El peatón puede interactuar con el semáforo para decidir si cruzar la calle o no. Este semáforo se comunicará con 
el semáforo vehicular para regular el tráfico en la ciudad. Decidiendo con base en que el número de autos(NA) sea
menor a el número de  peatones(NP) en la intersección.

Atributos:
    estado(str): Indica el estado del semáforo. "verde" representa que los peatones pueden cruzar, "rojo" representa que los peatones no pueden cruzar.
    evento(int): Indica si el bóton del cruce del semáforo peatonal ha sido presionado. 

Métodos:
    sensar_peatones(): Sensa el número de peatones en la intersección y lo manda al semáforo vehicular.
    cambiar_estado(): Cambia el estado del semáforo entre "verde", "amarillo" y "rojo".
    mostrar_tiempo(): Muestra el tiempo restante para cambiar de estado.
    step(): Realiza un paso del movimiento del semáforo, verificando todas las condiciones necesarias.
"""
class SemaforoPeatonal(Agent):
    def __init__(self, unique_id, model, pos, radio_detencion=3):
        super().__init__(unique_id,model)
        self.pos = pos
        self.estado = "rojo"
        self.radio_detencion = radio_detencion

    def detectar_peatones(self):
        """"Detecta peatones cerca """
        vecinos = self.model.grid.get_neighbors(
            self.pos,
            moore=False,
            include_center=True,
            radius=self.radio_detencion
        )
        for agente in vecinos:
            if isinstance(agente,Peaton):
                return True
        return False
    
    def cambiar_estado(self):
        if self.detectar_peatones():
            self.estado = "verde"
        else:
            self.estado = "rojo"

    def step(self):
        self.cambiar_estado()


"""
Clase SemaforoVehicular:

La clase SemaforoVehicular representa un semáforo vehicular que puede cambiar su estado entre "verde", "amarillo" y "rojo".
Su propósito es regular el tráfico vehicular en la ciudad. pero no se comunica con los vehiculos, solo con el semáforo peatonal.

Atributos: 
    estado(str): Indica el estado del semáforo. "verde" , "amarillo" y "rojo".
    evento(int): Indica si el semáforo peatonal ha mandado una petición.
    tiempo(int): Indica el tiempo restante para cambiar de estado y es mandado al semáforo peatonal.

Métodos:
    sensar_vehiculos(): Sensa el número de vehículos en la intersección y lo manda al semáforo peatonal.
    cambiar_estado(): Cambia el estado del semáforo entre "verde", "amarillo" y "rojo".
    step(): Realiza un paso del movimiento del semáforo, verificando todas las condiciones necesarias.
"""
class SemaforoVehicular(Agent):
    pass

"""
Clase Celda:

Nos sirve para representar un cuadro fijo en el grid.
"""
class Celda(Agent):
    """Agente que representa un cuadro fijo en el grid."""
    
    def __init__(self, unique_id, model, direction, color, layer, width=1, height=1):
        """
        Inicializa un agente Celda.
        
        Args:
            unique_id: Identificador único del agente.
            model: El modelo donde se encuentra el agente.
            direction: Dirección de la celda.
            color: Color de la celda.
            layer: Capa de la celda.
            shape: Forma de la celda, por defecto es "rect".
            width: Ancho de la celda, por defecto es 1.
            height: Alto de la celda, por defecto es 1.
        """
        super().__init__(unique_id, model)
        self.direccion = direction
        self.color = color  # Color inicial de la celda
        self.layer = layer  # Capa del agente
        self.width = width  # Ancho de la celda
        self.height = height  # Alto de la celda
