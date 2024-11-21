"""
Clase que define los agentes del sistema
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
    pass

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
    def __init__(self, unique_id, model, destino, transitables, semaforos):
        super().__init__(unique_id,model)
        self.destino = destino
        self.transitables = transitables
        self.semaforos = semaforos
        self.ruta = self.calcular_ruta(destino)

    def calcular_ruta(self, destino):
        if destino not in [(x, y) for x, y, _ in self.transitables]:
            return []
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
    
    def detectar_semaforo(self, pos_siguiente):
        for semaforo in self.semaforos:
            sem_pos = (semaforo[0],semaforo[1])
            if pos_siguiente == sem_pos:
                semaforo_agente = self.model.grid.get_cell_list_contents([sem_pos][0])
                if isinstance(semaforo_agente, SemaforoPeatonal) and semaforo_agente.state == "rojo":
                    return True
        return False


    def moverse(self):
        if self.ruta:
            siguiente_pos = self.ruta[0]

            if self.detectar_semaforo(siguiente_pos):
                return
            
            self.ruta.pop(0)
            self.model.grid.move_agent(self, siguiente_pos)
    
    def step(self):
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
    def __init__(self, unique_id, model, radio_detencion=3, tiempo_verde=5):
        super().__init__(unique_id,model)
        self.estado = "rojo"
        self.tiempo_rojo = radio_detencion
        self.tiempo_verde = tiempo_verde
        self.contador = 0
    def detectar_peatones(self):
        vecinos = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=self.radio_detection
        )
        for agente in vecinos:
            if isinstance(agente,Peaton):
                return True
        return False
    
    def cambiar_estado(self):
        if self.estado == "rojo" and self.detectar_peatones():
            self.estado = "verde"
            self.contador = 0
        elif self.estado == "verde" and self.contador >= self.tiempo_verde:
            self.estado = "rojo"
            self.contador = 0

    def step(self):
        if self.estado == "verde":
            self.contador += 1
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




