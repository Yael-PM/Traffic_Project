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
    def _init_(self, unique_id, model, origen, destino, semaforosV, transitables, estacionamientos):
        super()._init_(unique_id, model)
        self.origen = origen
        self.destino = destino
        self.semaforosV = semaforosV
        self.transitables = transitables
        self.estacionamientos = estacionamientos
        self.ruta = self.generar_ruta()  # Calculamos la ruta inicial
        self.visitadas = set()  # Conjunto para almacenar celdas visitadas

    def determinar_direccion(self):
        """
        Determina hacia qué dirección (N, S, E, O, NE, NO, SE, SO) debe moverse el vehículo
        con respecto a su posición actual y el destino.
        """
        x_actual, y_actual = self.origen
        x_destino, y_destino = self.destino

        delta_x = x_destino - x_actual
        delta_y = y_destino - y_actual

        # Determinar la dirección principal
        if delta_x > 0 and delta_y > 0:
            direccion = "Noreste"
        elif delta_x > 0 and delta_y < 0:
            direccion = "Sureste"
        elif delta_x < 0 and delta_y > 0:
            direccion = "Noroeste"
        elif delta_x < 0 and delta_y < 0:
            direccion = "Suroeste"
        elif delta_x > 0:
            direccion = "Norte"
        elif delta_x < 0:
            direccion = "Sur"
        elif delta_y > 0:
            direccion = "Este"
        elif delta_y < 0:
            direccion = "Oeste"
        else:
            direccion = "Estás en el destino"

        print(f"Dirección hacia el destino: {direccion}")
        return direccion

    def generar_ruta(self):
        """
        Genera una ruta desde el origen hasta el destino respetando las direcciones transitables.
        Retorna una lista de coordenadas que representan la ruta calculada.
        """
        origen = self.origen
        destino = self.destino
        transitables = self.transitables

        # Usamos una cola de prioridad para almacenar las celdas por explorar
        frontera = PriorityQueue()
        frontera.put((0, origen))  # (prioridad, celda)

        # Diccionarios para rastrear rutas y costos
        came_from = {}  # De dónde venimos
        cost_so_far = {}  # Costo acumulado hasta cada celda
        came_from[origen] = None
        cost_so_far[origen] = 0

        while not frontera.empty():
            _, current = frontera.get()

            # Si alcanzamos el destino, reconstruimos la ruta
            if current == destino:
                ruta = []
                while current:
                    ruta.append(current)
                    current = came_from[current]
                ruta.reverse()
                print(f"Ruta generada para el vehículo {self.unique_id}: {ruta}")
                return ruta

            # Explorar las celdas adyacentes transitables
            x, y = current
            adyacentes = [
                ((x - 1, y), "N"),  # Norte
                ((x + 1, y), "S"),  # Sur
                ((x, y - 1), "O"),  # Oeste
                ((x, y + 1), "E"),  # Este
            ]

            for next_celda, direccion in adyacentes:
                if next_celda in transitables.get(direccion, []):  # Respetar las direcciones
                    new_cost = cost_so_far[current] + 1  # Costo acumulado
                    if next_celda not in cost_so_far or new_cost < cost_so_far[next_celda]:
                        cost_so_far[next_celda] = new_cost
                        priority = new_cost + abs(next_celda[0] - destino[0]) + abs(next_celda[1] - destino[1])
                        frontera.put((priority, next_celda))
                        came_from[next_celda] = current

        # Si no se encuentra ruta, retorna None
        print(f"No se pudo encontrar una ruta desde {origen} hasta {destino}.")
        return None

    def moverse(self, coordenada):
        """
        Mueve al agente a la coordenada especificada si está en las celdas transitables.

        Parámetros:
            coordenada (tuple): La nueva posición a la que se moverá.
        """
        if coordenada not in self.visitadas:
            # Mueve al agente en el modelo
            self.model.grid.move_agent(self, coordenada)
            self.origen = coordenada  # Actualiza el origen
            self.visitadas.add(coordenada)  # Marca la celda como visitada
            print(f"Me moví directamente a la posición {self.origen}.")
        else:
            print(f"La posición {coordenada} ya fue visitada, no me moveré.")

    def buscar_celda_transitable(self):
        """
        Busca la celda transitable más cercana al destino desde la posición actual.
        Selecciona la celda que minimiza la distancia Manhattan.
        """
        x, y = self.origen
        adyacentes = [
            ((x - 1, y), "N"),  # Norte
            ((x + 1, y), "S"),  # Sur
            ((x, y - 1), "O"),  # Oeste
            ((x, y + 1), "E"),  # Este
        ]

        # Filtrar celdas transitables adyacentes
        transitables_adyacentes = [
            coord for coord, direccion in adyacentes
            if coord not in self.visitadas and coord in self.transitables.get(direccion, [])
        ]

        # Si hay celdas transitables adyacentes, priorizar las que reduzcan la distancia Manhattan
        if transitables_adyacentes:
            transitables_adyacentes.sort(key=lambda coord: abs(coord[0] - self.destino[0]) + abs(coord[1] - self.destino[1]))
            return transitables_adyacentes[0]  # Seleccionar la mejor celda

        # Si no hay celdas adyacentes disponibles, buscar en el resto de transitables
        for direccion, celdas in self.transitables.items():
            for celda in celdas:
                if celda not in self.visitadas:
                    return celda

        return None  # Si no hay celdas disponibles
    
    def validar_direccion(self):
        """
        Verifica las celdas transitables adyacentes y selecciona la más cercana al destino.
        Retorna la coordenada de la celda válida más cercana al destino o None si no hay opciones.
        """
        x, y = self.origen
        adyacentes = [
            (x - 1, y), (x + 1, y),  # Coordenadas arriba y abajo
            (x, y - 1), (x, y + 1),  # Coordenadas izquierda y derecha
        ]

        # Filtrar las celdas transitables
        celdas_validas = [
            coord for coord in adyacentes
            if any(coord in celdas for celdas in self.transitables.values())
        ]

        # Si no hay celdas válidas, retorna None
        if not celdas_validas:
            print(f"No hay direcciones transitables desde el origen {self.origen}.")
            return None

        # Ordenar celdas válidas según su distancia Manhattan al destino
        celdas_validas.sort(key=lambda coord: abs(coord[0] - self.destino[0]) + abs(coord[1] - self.destino[1]))

        # Seleccionar la celda que reduce la distancia al destino
        mejor_celda = celdas_validas[0]

        # Evitar ciclos: no regresar inmediatamente a una celda reciente
        if hasattr(self, 'ultima_posicion') and mejor_celda == self.ultima_posicion:
            if len(celdas_validas) > 1:  # Si hay otras opciones, elige la segunda mejor
                mejor_celda = celdas_validas[1]

        print(f"Puedo moverme a la coordenada {mejor_celda}.")
        return mejor_celda


    def step(self):
        """
        Método ejecutado en cada paso de la simulación.
        El agente valida direcciones y se mueve hacia su destino.
        """
        if self.origen == self.destino:
            print(f"El vehículo {self.unique_id} ha llegado a su destino {self.destino}.")
            return  # Detener el movimiento si ya llegó al destino

        # Obtener la mejor coordenada para avanzar hacia el destino
        coordenada = self.validar_direccion()
        if coordenada:
            # Almacena la posición actual antes de moverse
            self.ultima_posicion = self.origen
            self.moverse(coordenada)
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
    def _init_(self, unique_id, model, origen, destino):
        super()._init_(unique_id, model)
        self.origen = origen
        self.destino = destino
        self.ruta = self.calcular_ruta(destino)
        self.color = "blue"  # Color para representar al peatón en el mapa

    def calcular_ruta(self, destino):
        """
        Calcula la ruta desde el origen hasta el destino usando un algoritmo simple de A*.
        """
        if destino is None or self.origen is None:
            print(f"Peatón {self.unique_id}: Origen o destino inválidos.") 
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
                print(f"Peatón {self.unique_id}: Ruta encontrada.")
                return self.reconstruir_camino(came_from,current)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)

                if neighbor not in self.model.banquetas :
                    print(f"Peatón {self.unique_id}: Celda vecina {neighbor} no es transitable.") 
                    continue

                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.distancia(neighbor, destino)
                    open_set.put((f_score[neighbor], neighbor))

        print(f"Peatón {self.unique_id} no encontró una ruta válida.")
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
            print(f"Peatón {self.unique_id} no tiene ruta para moverse.")
            self.ruta = self.calcular_ruta(self.destino)
            if not self.ruta:
                print(f"Peatón {self.unique_id}: No puede llegar a {self.destino}, asignando nuevo destino.")
                self.asignar_nuevo_destino()
            return
        
        siguiente_pos = self.ruta[0]
        if self.model.grid.is_cell_empty(siguiente_pos) or isinstance(self.model.grid.get_cell_list_contents(siguiente_pos)[0], Celda):
            self.model.grid.move_agent(self, siguiente_pos)
            self.ruta.pop(0)
            print(f"Peatón {self.unique_id} se movió a {siguiente_pos}.")
        else:
            print(f"Peatón {self.unique_id} no puede moverse a {siguiente_pos} porque está ocupado.")
            self.ruta = self.calcular_ruta(self.destino)
            if not self.ruta:
                self.asignar_nuevo_destino()
    
    def asignar_nuevo_destino(self):
        nuevo_destino = random.choice(self.model.banquetas)
        while nuevo_destino == self.destino:
            nuevo_destino = random.choice(self.model.banquetas)
        self.destino = nuevo_destino
        print(f"Peatón {self.unique_id}: Nuevo destino asignado {self.destino}.")
        self.ruta = self.calcular_ruta(self.destino)

    def step(self):
        """Ejecución de un paso del agente."""
        if self.pos == self.destino:
            print(f"Peatón {self.unique_id} alcanzó su destino: {self.destino}")
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
    def _init_(self, unique_id, model, pos, radio_detencion=0):
        super()._init_(unique_id,model)
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
        return any(isinstance(agente, Peaton)for agente in vecinos)

    def cambiar_estado(self):
        if self.estado == "rojo" and self.detectar_peatones():
            self.estado = "verde"
            print(f"Semáforo peatonal {self.unique_id}: Cambiando a VERDE.")
        elif self.estado == "verde" and not self.detectar_peatones():
            self.estado = "rojo"
            print(f"Semáforo peatonal {self.unique_id}: Cambiando a ROJO.")

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
    estados = ["verde","amarillo","rojo"]

    def _init_(self, unique_id, model, pos, direccion, semaforoP, grupo, tiempo_amarillo=2):
        super()._init_(unique_id, model)
        self.pos = pos
        self.direccion = direccion
        self.semaforoP = semaforoP
        self.grupo = grupo
        self.state = "rojo"
        self.timer = 0
        self.tiempo_amarillo = tiempo_amarillo

    def step(self):
        """Controla los cambios de estado."""
        # Controlar el cambio de estado basado en el grupo
        if self.grupo == 1 and self.model.grupo_activo == 1:
            if self.state == "verde":
                self.timer += 1
                if self.timer >= 5:  # Cambiar a amarillo después de 5 pasos
                    self.state = "amarillo"
                    self.timer = 0
            elif self.state == "amarillo":
                self.timer += 1
                if self.timer >= self.tiempo_amarillo:
                    self.state = "rojo"
        elif self.grupo == 2 and self.model.grupo_activo == 2:
            if self.state == "verde":
                self.timer += 1
                if self.timer >= 5:  # Cambiar a amarillo después de 5 pasos
                    self.state = "amarillo"
                    self.timer = 0
            elif self.state == "amarillo":
                self.timer += 1
                if self.timer >= self.tiempo_amarillo:
                    self.state = "rojo"
        elif self.state == "rojo":
            if self.grupo == self.model.grupo_activo:
                self.state = "verde"

"""
Clase Celda:

Nos sirve para representar un cuadro fijo en el grid.
"""
class Celda(Agent):
    """Agente que representa un cuadro fijo en el grid."""

    def _init_(self, unique_id, model, direction, color, layer, width=1, height=1):
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
        super()._init_(unique_id, model)
        self.direccion = direction
        self.color = color  # Color inicial de la celda
        self.layer = layer  # Capa del agente
        self.width = width  # Ancho de la celda
        self.height = height  # Alto de la celda