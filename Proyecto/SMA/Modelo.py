from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from Agentes import Vehiculo, Celda, SemaforoVehicular, SemaforoPeatonal
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
        self.random = random.Random()
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.semaforosV = semaforosV
        self.semaforosP = semaforosP
        self.transitables = transitables
        self.intransitables = intransitables
        self.banquetas = banquetas
        self.estacionamientos = estacionamientos

        for idx, (x, y, direction) in enumerate(transitables):
            celda = Celda(idx, self, direction, color="green", layer=1)  # Definir color y capa según sea necesario
            self.grid.place_agent(celda, (x, y))  # Colocar la celda en el grid
            self.schedule.add(celda)  # Añadir el agente al planificador
        
        for idx, (x, y, _) in enumerate(intransitables):
            celda = Celda(idx + len(transitables), self, None, color="blue", layer=2)
            self.grid.place_agent(celda, (x, y))  # Place the agent on the grid at position (x, y)
            self.schedule.add(celda)  # Add the agent to the scheduler
        
        for idx, (x, y, _) in enumerate(banquetas):
            celda = Celda(idx + len(transitables) + len(intransitables), self, None, color="gray", layer=3)
            self.grid.place_agent(celda, (x, y))
            self.schedule.add(celda)

        # Inicializar semáforos
        self.inicializar_semaforos(semaforosV, semaforosP)

    def inicializar_semaforos(self, semaforosV, semaforosP):
        for i, (x, y, direccion) in enumerate(semaforosV):
            semaforo = SemaforoVehicular(i, self, direccion)
            self.grid.place_agent(semaforo, (x, y))
            self.schedule.add(semaforo)

        for i, (x, y) in enumerate(semaforosP):
            semaforo = SemaforoPeatonal(i, self)
            self.grid.place_agent(semaforo, (x, y))
            self.schedule.add(semaforo)

    def step(self):
        self.schedule.step()