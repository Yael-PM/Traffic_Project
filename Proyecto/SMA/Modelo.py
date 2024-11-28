from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from Agentes import Vehiculo, Celda, SemaforoVehicular, SemaforoPeatonal, Peaton
import random

class ModeloTrafico(Model):
    """
    Clase Modelo:
    
    La clase Modelo representa el sistema de tráfico, el cual contiene la lógica del sistema y los agentes que interactúan en él.
    
    Atributos:
        grid (MultiGrid): Grid que contiene a los agentes.
        schedule (SimultaneousActivation): Programa de activación de los agentes.
        semaforos (list): Lista de semáforos en el sistema.
        vehiculos (list): Lista de vehículos en el sistema.
        celdas (list): Lista de celdas en el sistema.
    
    Métodos:
        __init__(self, n, m, semaforos, vehiculos, celdas): Constructor de la clase Modelo.
        step(self): Realiza un paso de la simulación.
    """
    
    def __init__(self, width, height, semaforosV, semaforosP, transitables, intransitables, banquetas, estacionamientos):
        """
        Constructor de la clase Modelo.
        
        Parámetros:
            n (int): Número de columnas del grid.
            m (int): Número de filas del grid.
            semaforosV (list): Lista de semáforos vehiculares en el sistema.
            semaforosP (list): Lista de semáforos peatonales en el sistema.
            transitables (list): Lista de celdas transitables en el sistema.
            intransitables (list): Lista de celdas intransitables en el sistema.
            banquetas (list): Lista de banquetas en el sistema.
            estacionamientos (list): Lista de estacionamientos en el sistema.
        """
        super().__init__()
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.semaforosV = semaforosV
        self.semaforosP = semaforosP
        self.transitables = transitables
        self.intransitables = intransitables
        self.banquetas = banquetas
        self.estacionamientos = estacionamientos
        self.grupo_semaforos = []
        self.semaforos_peatonales = {}
        self.step_count = 0
        self.grupo_activo = 1  # Inicializa el primer grupo activo

        # Crear agentes para las celdas transitables
        for direction, celdas in transitables.items():
            for x, y in celdas:
                # Crear el agente Celda para cada coordenada (x, y)
                celda = Celda((x, y), self, direction, color="green", layer=1, width=1, height=1)  # Definir color, capa y dimensiones
                self.grid.place_agent(celda, (x, y))  # Colocar la celda en el grid
                self.schedule.add(celda)  # Añadir el agente al planificador

        # Crear agentes para las celdas intransitables
        for x, y in intransitables:
            # Crear el agente Celda para cada coordenada (x, y)
            celda = Celda((x, y), self, None, color="blue", layer=2, width=1, height=1)  # Definir color, capa y dimensiones
            self.grid.place_agent(celda, (x, y))
            self.schedule.add(celda)

        # Crear agentes para las banquetas
        for x, y in banquetas:
            # Crear el agente Celda para cada coordenada (x, y)
            celda = Celda((x, y), self, None, color="gray", layer=3, width=1, height=1)  # Definir color, capa y dimensiones
            self.grid.place_agent(celda, (x, y))
            self.schedule.add(celda)

        # Crear agentes para los semáforos de peatones
        for idx, (x, y) in enumerate(semaforosP):
            semaforo_peatonal = SemaforoPeatonal(f"semaforoP_{x}_{y}", self, (x, y))
            grupo = 1 if (x, y) == semaforosP[0] else 2
            if self.grid.is_cell_empty((x, y)):
                self.grid.place_agent(semaforo_peatonal, (x, y))
            else:
                self.grid.remove_agent(self.grid.get_cell_list_contents((x, y))[0])
                self.grid.place_agent(semaforo_peatonal, (x, y))
            self.grupo_semaforos.append({"peatonales": (x, y), "grupo": 1})

        # Crear semaforos vehiculares
        for direccion, semaforos in semaforosV.items():
            for idx, (x,y) in enumerate(semaforos):
                grupo = 1 if idx % 2 == 0 else 2
                semaforo_vehicular = SemaforoVehicular(f"semaforoV_{x}_{y}", self, (x, y), direccion, None, grupo)
                if self.grid.is_cell_empty((x, y)):
                    self.grid.place_agent(semaforo_vehicular,(x, y))
                    self.schedule.add(semaforo_vehicular)
                else:
                    self.grid.remove_agent(self.grid.get_cell_list_contents((x, y))[0])
                    self.grid.place_agent(semaforo_vehicular, (x, y))
                    self.schedule.add(semaforo_vehicular)
            self.grupo_semaforos.append({"vehiculares": (x, y), "grupo": grupo})

        # Crear agentes para los estacionamientos
        for nombre, (x, y) in estacionamientos.items():
            # Usamos el nombre como dirección (esto puede ser modificado según tu necesidad)
            direction = nombre  # La dirección podría ser el nombre del estacionamiento (A, B, C, D)
            
            # Crear el agente Celda para cada estacionamiento con las coordenadas (x, y)
            celda = Celda((x, y), self, direction, color="yellow", layer=6, width=1, height=1)  # Definir color, capa y dimensiones
            self.grid.place_agent(celda, (x, y))  # Colocar la celda en el grid
            self.schedule.add(celda)  # Añadir el agente al planificador

        # Crear agentes para los peatones
        # Inicializar peatones en el modelo
        for i in range(5):  # Cambia el rango según el número de peatones deseado
            origen = random.choice(self.banquetas)
            destino = random.choice(self.banquetas)

            # Asegurarse de que el destino no sea igual al origen
            while destino == origen:
                destino = random.choice(self.banquetas)

            print(f"Peatón {i}: Origen = {origen}, Destino = {destino}")
            peaton = Peaton(i, self, origen, destino)
            self.grid.place_agent(peaton, origen)
            self.schedule.add(peaton)

        # Crear agentes para los vehículos
        for i in range(5):  # Cambia el rango según el número de vehículos deseado
            origen = random.choice(list(estacionamientos.values()))  # Coordenada (x, y)
            destino = random.choice(list(estacionamientos.values()))  # Coordenada (x, y)

            # Asegúrate de que el destino no sea igual al origen
            while destino == origen:
                destino = random.choice(list(estacionamientos.values()))

            # Crear y colocar el vehículo
            print(f"Vehículo {i}: origen={origen}, destino={destino}")  # Agregado para mostrar origen y destino
            vehiculo = Vehiculo(i, self, origen, destino, self.semaforosV, self.transitables, self.estacionamientos)
            self.grid.place_agent(vehiculo, origen)  # Coloca el vehículo en el origen
            self.schedule.add(vehiculo)  # Añade el vehículo al planificador

    def step(self):
        """ Realiza un paso de la simulación con depuración."""

        print(f"Iniciando step {self.step_count}...")
        self.schedule.step()  # Avanza los agentes

        # Incrementa el contador de pasos
        self.step_count += 1

        self.grupo_activo = 1 if (self.step_count // 10) % 2 == 0 else 2
        print(f"Grupo activo: {self.grupo_activo}")

            
        # Actualiza semáforos
        for grupo in self.grupo_semaforos:
            if "vehiculares" in grupo:
                vehicular_pos = grupo["vehiculares"]
                vehicular = next(
                    (agent for agent in self.grid.get_cell_list_contents(vehicular_pos)
                    if isinstance(agent, SemaforoVehicular)),
                    None
                )
                if vehicular:
                    nuevo_estado = "verde" if grupo["grupo"] == self.grupo_activo else "rojo"
                    vehicular.cambiar_estado(nuevo_estado)
                    #vehicular.state = "verde" if grupo["grupo"] == self.grupo_activo else "rojo"
                    print(f"Semáforo vehicular en {vehicular_pos}: {vehicular.state}")

            if "peatonales" in grupo:
                peatonal_pos = grupo["peatonales"]
                peatonal = next(
                    (agent for agent in self.grid.get_cell_list_contents(peatonal_pos)
                    if isinstance(agent, SemaforoPeatonal)),
                    None
                )
                if peatonal:
                    peatonal.estado = "verde" if grupo["grupo"] == self.grupo_activo else "rojo"
                    print(f"Semáforo peatonal en {peatonal_pos}: {peatonal.estado}")