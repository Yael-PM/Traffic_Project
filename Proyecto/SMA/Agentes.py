"""
Módulo que define los agentes del sistema
Autores: 
    - Emiliano Caballero Mendoza A017
    - Yael Octavio Pérez Méndez A01799842
    - José Eduardo Rosas Ponciano A017
    - Manuel Olmos A01750748

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
#from mesa.visualization.modules import CanvasGrid
#from mesa.visualization.ModularVisualization import ModularServer
import random
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
            #print(f"Peatón {self.unique_id}: Origen o destino inválidos.") 
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
                #print(f"Peatón {self.unique_id}: Ruta encontrada.")
                return self.reconstruir_camino(came_from,current)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)

                if neighbor not in self.model.banquetas :
                    #print(f"Peatón {self.unique_id}: Celda vecina {neighbor} no es transitable.") 
                    continue

                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.distancia(neighbor, destino)
                    open_set.put((f_score[neighbor], neighbor))

        #print(f"Peatón {self.unique_id} no encontró una ruta válida.")
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
        if not self.ruta:
            #print(f"Peatón {self.unique_id} no tiene ruta para moverse.")
            self.ruta = self.calcular_ruta(self.destino)
            if not self.ruta:
                #print(f"Peatón {self.unique_id}: No puede llegar a {self.destino}, asignando nuevo destino.")
                self.asignar_nuevo_destino()
            return
        
        siguiente_pos = self.ruta[0]
        if self.model.grid.is_cell_empty(siguiente_pos) or isinstance(self.model.grid.get_cell_list_contents(siguiente_pos)[0], Celda):
            self.model.grid.move_agent(self, siguiente_pos)
            self.ruta.pop(0)
            #print(f"Peatón {self.unique_id} se movió a {siguiente_pos}.")
        else:
            #print(f"Peatón {self.unique_id} no puede moverse a {siguiente_pos} porque está ocupado.")
            self.ruta = self.calcular_ruta(self.destino)
            if not self.ruta:
                self.asignar_nuevo_destino()
    
    def asignar_nuevo_destino(self):
        nuevo_destino = random.choice(self.model.banquetas)
        while nuevo_destino == self.destino:
            nuevo_destino = random.choice(self.model.banquetas)
        self.destino = nuevo_destino
        #print(f"Peatón {self.unique_id}: Nuevo destino asignado {self.destino}.")
        self.ruta = self.calcular_ruta(self.destino)

    def step(self):
        """Ejecución de un paso del agente."""
        if self.pos == self.destino:
            #print(f"Peatón {self.unique_id} alcanzó su destino: {self.destino}")
            self.asignar_nuevo_destino()
        else:
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
    def __init__(self, unique_id, model, pos, radio_detencion=0, tiempo_cambio=5):
        super().__init__(unique_id, model)
        self.pos = pos
        self.state = "rojo"
        self.radio_detencion = radio_detencion
        self.tiempo_cambio = tiempo_cambio
        self.contador = 0  # Para controlar el tiempo mínimo en cada estado

    def detectar_peatones(self):
        """"Detecta peatones cerca """
        vecinos = self.model.grid.get_neighbors(
            self.pos,
            moore=False,
            include_center=True,
            radius=self.radio_detencion
        )
        return any(isinstance(agente, Peaton) for agente in vecinos)

    def cambiar_estado(self):
        if self.contador < self.tiempo_cambio:
            self.contador += 1
            return

        if self.state == "rojo" and self.detectar_peatones():
            self.state = "verde"
            self.contador = 0  # Reiniciar contador
            print(f"Semáforo peatonal {self.unique_id}: Cambiando a VERDE.")
        elif self.state == "verde" and not self.detectar_peatones():
            self.state = "rojo"
            self.contador = 0  # Reiniciar contador
            print(f"Semáforo peatonal {self.unique_id}: Cambiando a ROJO.")

    def step(self):
        self.cambiar_estado()
        print(f"Semáforo peatonal {self.unique_id}: {self.state}")


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
    estados = ["verde", "amarillo", "rojo"]

    def __init__(self, unique_id, model, pos, direccion, grupo, tiempo_amarillo=2):
        super().__init__(unique_id, model)
        self.pos = pos
        self.direccion = direccion
        self.semaforoP = SemaforoPeatonal(unique_id, model, pos)
        self.grupo = grupo
        self.state = self.estados[2]  # Inicialmente en "rojo"
        self.timer = 0
        self.tiempo_amarillo = tiempo_amarillo

    def obtener_semaforos_adyacentes(self):
        """Obtiene los semáforos vehiculares adyacentes."""
        adyacentes = self.model.grid.get_neighbors(
            self.pos,
            moore=False,
            include_center=False,
            radius=1
        )
        return [agente for agente in adyacentes if isinstance(agente, SemaforoVehicular)]
    
    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado del semáforo y de los semáforos adyacentes."""
        self.state = nuevo_estado
        print(f"Semáforo vehicular {self.unique_id}: Cambiando a {nuevo_estado.upper()}.")
        for semaforo in self.obtener_semaforos_adyacentes():
            semaforo.state = nuevo_estado
            print(f"Semáforo vehicular: Cambiando a {nuevo_estado.upper()}.")

    def step(self):
        """Controla los cambios de estado."""
        # Verificar si el semáforo peatonal ha detectado peatones
        if self.semaforoP.detectar_peatones():
            print(f"Semáforo vehicular {self.unique_id}: Peatones detectados, cambiando a ROJO.")
            self.state = self.estados[2]  # Cambiar a "rojo"
            self.semaforoP.state = self.semaforoP.estados[0]  # Cambiar semáforo peatonal a "verde"
        else:
            # Actualiza el estado del semáforo vehicular basado en el grupo activo del modelo
            nuevo_estado = "verde" if self.grupo == self.model.grupo_activo else "rojo"
            self.cambiar_estado(nuevo_estado)
            print(f"Semáforo vehicular {self.unique_id}: {self.state}")
    
            # Asegurarse de que todos los semáforos vehiculares cambien de estado
            for semaforo in self.model.schedule.agents:
                if isinstance(semaforo, SemaforoVehicular):
                    nuevo_estado = "verde" if semaforo.grupo == self.model.grupo_activo else "rojo"
                    semaforo.cambiar_estado(nuevo_estado)
                    print(f"Semáforo vehicular {semaforo.unique_id}: {semaforo.state}")
    
            semaforos = [agent for agent in self.model.schedule.agents if isinstance(agent, SemaforoVehicular) or isinstance(agent, SemaforoPeatonal)]
    
            print("Lista de todos los semáforos en el mapa")
            for semaforo in semaforos:
                tipo = "Vehicular" if isinstance(semaforo, SemaforoVehicular) else "Peatonal"
                print(f"{tipo} {semaforo.unique_id}: {semaforo.state}")

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